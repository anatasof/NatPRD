#!/usr/bin/env python3
"""Deterministic baseline validator for NatPRD PRDs.

Usage:
    python3 scripts/validate.py <path-to-prd.md>

Outputs JSON to stdout with per-section scores, violations, and warnings.
Exits 0 on success, 2 on file-not-found, 3 on parse/crash.

This script implements the *structural* checks from prompts/validation-rules.md.
Checks that need judgment (pain-led background, outcome-vs-feature objectives,
named-individual-vs-team owners, coverage-map completeness against §8) are
intentionally NOT implemented — the model layers those on top. Every section
keeps some semantic checks, so the JSON here is the baseline, not the final
verdict.

[TBD] policy (mirrors SKILL.md "[TBD] handling in validation"): a [TBD] field
is scored as if the field were absent — the same deduction applies — but it is
reported as a warning, not a violation. Exception: hard status gates (a PRD
marked Approved with a [TBD] approver) stay violations, because the status
itself asserts the field is resolved.

Unfilled template placeholders ("[Name]", "[Value]", "[Name], [Name]",
"YYYY-MM-DD") count as empty, including values composed of several
placeholders.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

SECTION_MAX = {
    "§1": 3, "§2": 5, "§3": 10, "§4": 10, "§5": 8, "§6": 8,
    "§7": 10, "§8": 20, "§9": 8, "§10": 5, "§11": 8, "§12": 5,
}

SECTION_NAMES = {
    "§1": "Initiative Name", "§2": "Document Status", "§3": "Background",
    "§4": "Objective", "§5": "Scope & Boundaries", "§6": "Hypothesis",
    "§7": "Success Metrics", "§8": "Requirements", "§9": "Solution",
    "§10": "Metric Monitoring", "§11": "Event & Data Tracking", "§12": "FAQ",
}

VALID_STATUSES = {"Draft", "In Review", "Approved", "In Execution", "Deprecated"}
APPROVED_OR_BEYOND = {"Approved", "In Execution", "Deprecated"}

TBD_PATTERN = re.compile(r"\[TBD[^\]]*\]")
H2_PATTERN = re.compile(r"^## (\d+)\.\s+(.+?)\s*$", re.MULTILINE)
PLACEHOLDER_TOKEN = re.compile(r"\[[^\]]*\]")
SEPARATOR_CHARS = re.compile(r"[\s,;/&+·—–-]+")
DATE_PLACEHOLDERS = {"YYYY-MM-DD", "YYYY-MM", "DD-MM-YYYY", "MM/DD/YYYY"}
USER_STORY_PATTERN = re.compile(
    r"As an?\s+(?P<role>[^,]+?),\s+I want\s+.+?,\s+so that\s+.+",
    re.IGNORECASE,
)
HYPOTHESIS_PATTERN = re.compile(
    r"[Ww]e believe\s+.+?\s+for\s+.+?\s+will result in\s+.+?\s+because\s+.+",
    re.DOTALL,
)
EVENT_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9]*(_[a-z0-9]+)+$")
SOURCE_PATTERN = re.compile(r"\[source:\s*([^\]]+)\]", re.IGNORECASE)
REFERENCES_HEADING = re.compile(r"^#{1,4}\s+(references|sources)\b", re.IGNORECASE | re.MULTILINE)
GENERIC_ROLES = {"user", "a user", "the user", "users", "customer", "customers", "client"}

# Anchored to line start so inline-code mentions of ```mermaid in prose (e.g. the template's
# own guidance notes) are not mistaken for a real fenced block.
MERMAID_BLOCK = re.compile(r"^```mermaid[ \t]*\r?\n(.*?)^```[ \t]*$", re.DOTALL | re.MULTILINE)
MERMAID_OPEN = re.compile(r"^```mermaid[ \t]*$", re.MULTILINE)
# Two supported types (flowchart, sequenceDiagram) plus the `graph` alias of flowchart.
VALID_DIAGRAM_HEADERS = ("flowchart", "graph", "sequencediagram")
# Narrow: matches leftover skeleton tokens only — NOT legitimate Mermaid node labels like
# `[Member confirms cancellation]`, and NOT the sanctioned `[TBD]` label (diagram-rules.md).
DIAGRAM_PLACEHOLDER = re.compile(
    r"\[(?:name|value|action|role|benefit|metric|component|screen|title|step|node|actor|"
    r"system|event[ _]?name|happy[ _]?path|edge[ _]?case)\]",
    re.IGNORECASE,
)


def split_sections(content: str) -> Dict[str, str]:
    """Split the PRD by top-level numbered H2 headings."""
    sections: Dict[str, str] = {}
    matches = list(H2_PATTERN.finditer(content))
    for i, m in enumerate(matches):
        key = f"§{m.group(1)}"
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        sections[key] = content[start:end]
    return sections


def parse_kv_table(section_text: str) -> Dict[str, str]:
    """Parse | **Field** | Value | rows. Returns {field: value}."""
    kv: Dict[str, str] = {}
    for line in section_text.splitlines():
        m = re.match(r"\|\s*\*\*([^*]+)\*\*\s*\|\s*(.+?)\s*\|", line)
        if m:
            kv[m.group(1).strip()] = m.group(2).strip()
    return kv


def parse_tables(section_text: str) -> List[Dict[str, str]]:
    """Parse all markdown tables in a section. Returns list of row dicts."""
    rows: List[Dict[str, str]] = []
    lines = section_text.splitlines()
    i = 0
    while i < len(lines):
        if (
            lines[i].startswith("|")
            and i + 1 < len(lines)
            and re.match(r"^\|[-\s|:]+\|$", lines[i + 1])
        ):
            headers = [h.strip() for h in lines[i].strip().strip("|").split("|")]
            j = i + 2
            while j < len(lines) and lines[j].startswith("|"):
                cells = [c.strip() for c in lines[j].strip().strip("|").split("|")]
                if len(cells) == len(headers):
                    rows.append(dict(zip(headers, cells)))
                j += 1
            i = j
        else:
            i += 1
    return rows


def field_state(value: str) -> str:
    """Classify a field value.

    'filled' — carries real content.
    'tbd'    — entirely [TBD …] placeholder(s): deduct like missing, report as warning.
    'empty'  — blank, a dash, a date placeholder, or composed entirely of
               [bracket placeholders] and separators (covers "[Name], [Name]").
    """
    if not value:
        return "empty"
    v = value.strip().strip("`").strip()
    v = v.strip("*").strip()  # markdown emphasis wrappers
    if not v or v in {"—", "-", "–"}:
        return "empty"
    if v.upper() in DATE_PLACEHOLDERS:
        return "empty"
    tokens = PLACEHOLDER_TOKEN.findall(v)
    residue = SEPARATOR_CHARS.sub("", PLACEHOLDER_TOKEN.sub("", v))
    if residue:
        return "filled"
    if any(t.upper().startswith("[TBD") for t in tokens):
        return "tbd"
    return "empty"


def is_filled(value: str) -> bool:
    return field_state(value) == "filled"


def deduct_unfilled(
    value: str,
    points: int,
    message: str,
    violations: List[str],
    warnings: List[str],
    hard: bool = False,
) -> int:
    """Apply the rubric deduction when a field is not genuinely filled.

    'empty' → violation. 'tbd' → warning with the same deduction, unless
    hard=True (status-gate fields keep TBD a violation). Returns the points
    to deduct (0 when filled).
    """
    state = field_state(value)
    if state == "filled":
        return 0
    if state == "tbd" and not hard:
        warnings.append(f"{message} (marked [TBD] — scored as missing)")
    else:
        violations.append(message)
    return points


def find_subsection(text: str, title_pattern: str) -> Optional[str]:
    """Body of the first heading whose line matches title_pattern, up to the
    next heading. None when no such heading exists."""
    m = re.search(
        rf"^#{{2,5}}\s+.*{title_pattern}.*$", text, re.IGNORECASE | re.MULTILINE
    )
    if m is None:
        return None
    rest = text[m.end():]
    nxt = re.search(r"^#{2,5}\s", rest, re.MULTILINE)
    return rest[: nxt.start()] if nxt else rest


def block_state(block: str) -> str:
    """State of a prose block: 'filled' if any non-structural line carries real
    content, else 'tbd' if a [TBD …] marker is present, else 'empty'. Table
    rows, blockquotes, and headings are ignored (tables are judged separately);
    italic instruction notes like *(Optional — …)* are skipped."""
    states = set()
    for line in block.splitlines():
        s = line.strip()
        if not s or s.startswith(("#", "|", ">")):
            continue
        if re.match(r"\*\(.*\)\*$", s):
            continue
        states.add(field_state(s))
    if "filled" in states:
        return "filled"
    if "tbd" in states:
        return "tbd"
    return "empty"


def prose_or_tbd(
    section: str,
    title_pattern: str,
    points: int,
    missing_msg: str,
    tbd_msg: str,
    violations: List[str],
    warnings: List[str],
) -> int:
    """Deduct when a subsection is absent, empty, or TBD-only."""
    body = find_subsection(section, title_pattern)
    state = block_state(body) if body is not None else "empty"
    if state == "filled":
        return 0
    if state == "tbd":
        warnings.append(tbd_msg)
    else:
        violations.append(missing_msg)
    return points


def count_tbd(text: str) -> int:
    return len(TBD_PATTERN.findall(text))


def score_band(score: int) -> str:
    if score >= 90:
        return "Excellent"
    if score >= 75:
        return "Good"
    if score >= 60:
        return "Needs Work"
    return "Not Ready"


# ---------- Per-section deterministic checks ----------

def check_section_1(text: str) -> Tuple[int, List[str], List[str]]:
    violations: List[str] = []
    warnings: List[str] = []
    name = ""
    for line in text.splitlines()[1:]:
        s = line.strip()
        if not s or s.startswith(("#", "|", ">")) or re.match(r"[-*]\s", s):
            continue
        name = s.strip("`").strip().strip("*").strip()
        break
    state = field_state(name)
    if state == "empty":
        violations.append(
            "§1: Initiative name is missing or still a placeholder"
            + (f": {name}" if name else "")
        )
        return 0, violations, warnings
    if state == "tbd":
        warnings.append(f"§1: Initiative name is [TBD] (scored as missing): {name}")
        return 0, violations, warnings
    word_count = len(name.split())
    if word_count > 8:
        violations.append(f"§1: Name exceeds 8 words (got {word_count}): {name!r}")
        return 1, violations, warnings
    common_verbs = {"add", "build", "create", "fix", "improve", "remove", "update", "enable", "launch", "ship"}
    if name.split()[0].lower().strip(":,.") in common_verbs:
        warnings.append(f"§1: Name starts with a verb — consider a noun phrase: {name!r}")
    return 3, violations, warnings


def check_section_2(text: str) -> Tuple[int, List[str], List[str]]:
    violations: List[str] = []
    warnings: List[str] = []
    kv = parse_kv_table(text)
    score = 5
    status = kv.get("Status", "").strip("`").strip()
    if status not in VALID_STATUSES:
        violations.append(f"§2: Status '{status}' not in valid vocabulary {sorted(VALID_STATUSES)}")
        score -= 1
    if not is_filled(kv.get("Version", "")):
        warnings.append("§2: Version field is missing or placeholder")
        score -= 1
    score -= deduct_unfilled(
        kv.get("Reviewers", ""), 2,
        "§2: Reviewers field is empty or placeholder (named individuals required)",
        violations, warnings,
    )
    if status in APPROVED_OR_BEYOND:
        score -= deduct_unfilled(
            kv.get("Approvers", ""), 2,
            "§2: Approvers required when Status is Approved or beyond",
            violations, warnings, hard=True,
        )
        score -= deduct_unfilled(
            kv.get("Approval Date", ""), 1,
            "§2: Approval Date required when Status is Approved or beyond",
            violations, warnings, hard=True,
        )
    for field in ("Author", "Owner"):
        if not is_filled(kv.get(field, "")):
            warnings.append(f"§2: {field} field is empty or placeholder")
            score -= 1
    return max(0, score), violations, warnings


def check_section_3(text: str) -> Tuple[int, List[str], List[str]]:
    """Structural: Evidence & Data and Cost of Inaction must carry content.
    Pain-led ordering, paragraph counts, and the Regulatory Context requirement
    stay with the model (it knows the intake state; this script does not)."""
    violations: List[str] = []
    warnings: List[str] = []
    score = 10
    score -= prose_or_tbd(
        text, r"Evidence", 3,
        "§3: Evidence & Data subsection is missing or has no cited evidence — every claim needs a source",
        "§3: Evidence & Data is [TBD] (scored as missing)",
        violations, warnings,
    )
    score -= prose_or_tbd(
        text, r"Cost of Inaction", 2,
        "§3: Cost of Inaction is missing or empty — it is mandatory",
        "§3: Cost of Inaction is [TBD] (scored as missing)",
        violations, warnings,
    )
    return max(0, score), violations, warnings


def check_section_4(text: str) -> Tuple[int, List[str], List[str]]:
    """Structural: KR rows need a filled baseline and target; OKR alignment must
    have content. Outcome-vs-feature phrasing stays with the model."""
    violations: List[str] = []
    warnings: List[str] = []
    score = 10
    kr_rows = [r for r in parse_tables(text) if "Baseline" in r and "Target" in r]
    real_krs = [
        r for r in kr_rows
        if any(field_state(r.get(k, "")) == "filled" for k in ("Key Result", "Baseline", "Target"))
    ]
    if not real_krs:
        violations.append("§4: No key results with content — each KR needs a numeric baseline and target")
        score -= 6
    for r in real_krs:
        label = r.get("#") or (r.get("Key Result", "")[:40] or "<KR>")
        states = {col: field_state(r.get(col, "")) for col in ("Baseline", "Target")}
        missing = [c for c, s in states.items() if s != "filled"]
        if missing:
            msg = f"§4: {label} missing {' and '.join(m.lower() for m in missing)}"
            if all(states[c] == "tbd" for c in missing):
                warnings.append(msg + " (marked [TBD] — scored as missing)")
            else:
                violations.append(msg)
            score -= 2
        else:
            for col in ("Baseline", "Target"):
                if not re.search(r"\d", r.get(col, "")):
                    warnings.append(f"§4: {label} {col.lower()} is not numeric: {r.get(col)!r}")
    score -= prose_or_tbd(
        text, r"OKR", 2,
        "§4: Company OKR alignment is missing or empty",
        "§4: Company OKR alignment is [TBD] (scored as missing)",
        violations, warnings,
    )
    return max(0, score), violations, warnings


def check_section_5(text: str) -> Tuple[int, List[str], List[str]]:
    """Structural: Out of Scope must exist with content and reasons; platform
    and segment coverage must be stated. Regulatory scope items stay with the
    model."""
    violations: List[str] = []
    warnings: List[str] = []
    score = 8
    out = find_subsection(text, r"Out of Scope")
    if out is None:
        violations.append("§5: Out of Scope subsection is absent — state it explicitly even if empty")
        score -= 3
    else:
        out_rows = [r for r in parse_tables(out) if "Item" in r]
        real_out = [r for r in out_rows if field_state(r.get("Item", "")) == "filled"]
        if not real_out and block_state(out) != "filled":
            violations.append("§5: Out of Scope has no content — list items, or state 'None' with an explanation")
            score -= 3
        elif real_out:
            reason_states = {field_state(r.get("Reason", "")) for r in real_out}
            if "empty" in reason_states:
                violations.append("§5: One or more Out of Scope items have no reason attached")
                score -= 2
            elif "tbd" in reason_states:
                warnings.append("§5: One or more Out of Scope reasons are [TBD] (scored as missing)")
                score -= 2
    kv = parse_kv_table(text)
    platform_state = field_state(kv.get("Platform", ""))
    segment_state = field_state(kv.get("User Segment", "") or kv.get("Segment", ""))
    if "empty" in (platform_state, segment_state):
        violations.append("§5: Platform and user segment coverage must be stated")
        score -= 2
    elif "tbd" in (platform_state, segment_state):
        warnings.append("§5: Platform or user segment coverage is [TBD] (scored as missing)")
        score -= 2
    return max(0, score), violations, warnings


def check_section_6(text: str) -> Tuple[int, List[str], List[str]]:
    violations: List[str] = []
    warnings: List[str] = []
    score = 8
    # A hypothesis only counts when its placeholders are gone. The template
    # sentence ("We believe that [X] for [segment] …") must not pass as real.
    hyp_state = "empty"
    for paragraph in re.split(r"\n\s*\n", text):
        if not HYPOTHESIS_PATTERN.search(paragraph):
            continue
        tokens = PLACEHOLDER_TOKEN.findall(paragraph)
        if not tokens:
            hyp_state = "filled"
            break
        if all(t.upper().startswith("[TBD") for t in tokens):
            hyp_state = "tbd"
    if hyp_state == "empty":
        violations.append("§6: Hypothesis does not match 'We believe X for [segment] will result in Y because Z' (or is still the unfilled template)")
        score -= 3
    elif hyp_state == "tbd":
        warnings.append("§6: Hypothesis contains [TBD] components (scored as missing)")
        score -= 3
    fals = find_subsection(text, r"Falsification")
    if fals is not None:
        state = block_state(fals)
        if state == "empty":
            violations.append("§6: Falsification condition is empty")
            score -= 3
        elif state == "tbd":
            warnings.append("§6: Falsification condition is [TBD] (scored as missing)")
            score -= 3
    elif not re.search(r"falsif|prove\s+(it\s+)?wrong|disprov", text, re.IGNORECASE):
        violations.append("§6: No falsification condition stated")
        score -= 3
    if not re.search(r"\bconfidence\b", text, re.IGNORECASE):
        warnings.append("§6: Confidence level appears to be missing")
        score -= 1
    return max(0, score), violations, warnings


def check_section_7(text: str) -> Tuple[int, List[str], List[str]]:
    violations: List[str] = []
    warnings: List[str] = []
    score = 10
    rows = parse_tables(text)
    if not rows:
        violations.append("§7: No metric rows found")
        return 0, violations, warnings
    # Ignore untouched template rows (only the pre-filled Type column carries text).
    real_rows = [
        r for r in rows
        if any(field_state(v) == "filled" for k, v in r.items() if k.lower() != "type")
    ]
    if not real_rows:
        violations.append("§7: Metric tables contain only unfilled placeholder rows")
    has_leading = has_lagging = has_guardrail = False
    for row in real_rows:
        identifier = row.get("Metric") or next(iter(row.values()), "<row>")
        is_guardrail_row = any("threshold" in k.lower() for k in row)
        target = (
            row.get("Target")
            or row.get("Alert Threshold")
            or row.get("Threshold")
            or ""
        )
        score -= deduct_unfilled(
            row.get("Baseline", ""), 1,
            f"§7: Metric row missing baseline: {identifier}", violations, warnings,
        )
        score -= deduct_unfilled(
            target, 1,
            f"§7: Metric row missing target/threshold: {identifier}", violations, warnings,
        )
        type_val = row.get("Type", "").lower()
        if "leading" in type_val:
            has_leading = True
        if "lagging" in type_val:
            has_lagging = True
        if is_guardrail_row or "guardrail" in type_val:
            has_guardrail = True
    if not has_leading:
        violations.append("§7: No leading indicator metric identified")
        score -= 3
    if not has_lagging:
        violations.append("§7: No lagging indicator metric identified")
        score -= 3
    if not has_guardrail:
        violations.append("§7: No guardrail metric with content identified")
        score -= 2
    return max(0, score), violations, warnings


def _real_story_matches(block: str) -> List["re.Match"]:
    """User-story matches whose role is actually filled in — the template's
    own '\"As a [specific role], I want to [action]…\"' line must not count."""
    return [
        m for m in USER_STORY_PATTERN.finditer(block)
        if field_state(m.group("role")) == "filled"
    ]


def check_section_8(text: str) -> Tuple[int, List[str], List[str]]:
    violations: List[str] = []
    warnings: List[str] = []
    score = 20
    blocks = re.split(r"(?=^#{3,4}\s+(?:US-|User Story|Story))", text, flags=re.MULTILINE)
    story_blocks = [b for b in blocks if _real_story_matches(b)]
    if not story_blocks:
        if _real_story_matches(text):
            story_blocks = [text]
        else:
            violations.append(
                "§8: No user stories found in 'As a [role], I want [action], so that [benefit]' format"
            )
            return 0, violations, warnings
    for block in story_blocks:
        story_id_match = re.search(r"US-\d+|Story\s+\d+", block)
        story_id = story_id_match.group(0) if story_id_match else "<unidentified>"
        role = _real_story_matches(block)[0].group("role")
        role_clean = role.strip().strip("*").strip().lower()
        if role_clean in GENERIC_ROLES:
            violations.append(f"§8: {story_id} uses generic role '{role_clean}' — must be specific")
            score -= 2
        scenarios = re.findall(r"^\s*Scenario\b[^\n]*", block, re.MULTILINE | re.IGNORECASE)
        if not scenarios:
            scenarios = re.findall(r"^\s*Given\s+", block, re.MULTILINE)
        if len(scenarios) < 2:
            violations.append(f"§8: {story_id} has fewer than 2 Gherkin scenarios (found {len(scenarios)})")
            score -= 3
        if not re.search(r"Must[-\s]?have|Should[-\s]?have|Could[-\s]?have|Won.t[-\s]?have", block, re.IGNORECASE):
            # section-rules.md §8 lists missing MoSCoW as a VIOLATION, not a warning.
            violations.append(f"§8: {story_id} missing MoSCoW priority")
            score -= 1
    nfr_rows = [r for r in parse_tables(text) if "Verification Method" in r]
    for r in nfr_rows:
        if field_state(r.get("Requirement", "")) != "filled":
            continue
        score -= deduct_unfilled(
            r.get("Verification Method", ""), 2,
            f"§8: NFR {r.get('ID', '<row>')} has no verification method",
            violations, warnings,
        )
    return max(0, score), violations, warnings


def check_section_9(text: str) -> Tuple[int, List[str], List[str]]:
    """Structural: at least one real design link, a non-empty coverage map, and
    at least one alternative with a rejection reason. Whether the coverage map
    spans every §8 story stays with the model."""
    violations: List[str] = []
    warnings: List[str] = []
    score = 8
    rows = parse_tables(text)
    link_states = [field_state(r.get("Link", "")) for r in rows if "Link" in r]
    if "filled" not in link_states:
        if "tbd" in link_states:
            warnings.append("§9: Design artifact links are [TBD] (scored as missing)")
        else:
            violations.append("§9: No design artifact links present — prose without a link is not sufficient")
        score -= 3
    coverage_rows = [r for r in rows if "User Story" in r and "Solution Component" in r]
    real_coverage = [
        r for r in coverage_rows
        if field_state(r.get("Solution Component", "")) == "filled"
        or field_state(r.get("Design Reference", "")) == "filled"
    ]
    if not real_coverage:
        violations.append("§9: User story coverage map is missing or empty")
        score -= 2
    alt_rows = [r for r in rows if "Why Rejected" in r]
    real_alts = [r for r in alt_rows if field_state(r.get("Description", "")) == "filled"]
    if not real_alts:
        violations.append("§9: No considered alternatives with content — at least one is required")
        score -= 2
    else:
        for r in real_alts:
            score -= deduct_unfilled(
                r.get("Why Rejected", ""), 1,
                f"§9: Alternative {r.get('Option', '<row>')} is listed without a rejection reason",
                violations, warnings,
            )
    return max(0, score), violations, warnings


def check_section_10(text: str) -> Tuple[int, List[str], List[str]]:
    """Structural checks for Metric Monitoring. Named-vs-team DRI stays semantic."""
    violations: List[str] = []
    warnings: List[str] = []
    score = 5
    kv = parse_kv_table(text)
    tool = kv.get("Dashboard / Tool") or kv.get("Dashboard/Tool") or kv.get("Dashboard") or ""
    score -= deduct_unfilled(tool, 1, "§10: No monitoring tool or dashboard named", violations, warnings)
    score -= deduct_unfilled(kv.get("DRI", ""), 1, "§10: Monitoring DRI is missing", violations, warnings)
    threshold = (
        kv.get("Primary Metric Alert Threshold")
        or kv.get("Alert Threshold")
        or ""
    )
    score -= deduct_unfilled(threshold, 1, "§10: No alert threshold defined for primary metrics", violations, warnings)
    score -= deduct_unfilled(kv.get("Rollback Trigger", ""), 1, "§10: No rollback trigger defined", violations, warnings)
    date_states = {field_state(row.get("Date", "")) for row in parse_tables(text) if "Date" in row}
    if "filled" not in date_states:
        if "tbd" in date_states:
            warnings.append("§10: Post-launch review dates are [TBD] (scored as missing)")
        else:
            violations.append("§10: No post-launch review dates set")
        score -= 1
    return max(0, score), violations, warnings


def check_section_11(text: str) -> Tuple[int, List[str], List[str]]:
    violations: List[str] = []
    warnings: List[str] = []
    score = 8
    rows = parse_tables(text)
    if not rows:
        warnings.append("§11: No event rows found in tables")
        return score, violations, warnings
    real_events = 0
    for row in rows:
        name = (row.get("Event Name") or row.get("Event") or row.get("Name") or "").strip("`").strip()
        if field_state(name) != "filled":
            continue
        real_events += 1
        if not EVENT_NAME_PATTERN.match(name):
            violations.append(f"§11: Event name '{name}' does not match noun_verb convention")
            score -= 2
    if real_events == 0:
        warnings.append("§11: No event rows with content yet — every §7 metric needs a feeding event")
    if not re.search(r"sign[-\s]?off|signoff", text, re.IGNORECASE):
        violations.append("§11: Data team sign-off not found")
        score -= 2
    return max(0, score), violations, warnings


def check_section_12(text: str) -> Tuple[int, List[str], List[str]]:
    """FAQ: present + at least one real entry + open items have owners = full marks."""
    violations: List[str] = []
    warnings: List[str] = []
    faq_rows = [
        r for r in parse_tables(text)
        if "Status" in r and field_state(r.get("Question", "")) == "filled"
    ]
    if not faq_rows:
        warnings.append("§12: FAQ has zero entries (acceptable only for brand-new drafts)")
        return 3, violations, warnings
    open_missing_owner = False
    for row in faq_rows:
        status = row.get("Status", "").strip("`").strip().lower()
        if "open" in status:
            owner = row.get("Answered By") or row.get("Owner") or ""
            if not is_filled(owner):
                open_missing_owner = True
                warnings.append("§12: Open FAQ item has no assigned owner")
    return (3 if open_missing_owner else 5), violations, warnings


def check_citations(content: str) -> List[str]:
    """Cross-cutting (not scored): every [source: …] needs a retrieved: date and a
    References/Sources section to consolidate provenance."""
    warnings: List[str] = []
    sources = SOURCE_PATTERN.findall(content)
    flagged: set = set()
    for raw in sources:
        inner = raw.strip()
        if "retrieved:" not in inner.lower():
            key = inner.split(",")[0].strip()[:60]
            if key not in flagged:
                warnings.append(f"§citations: source missing 'retrieved:' date — {key}")
                flagged.add(key)
    if sources and not REFERENCES_HEADING.search(content):
        warnings.append("§citations: inline sources present but no References/Sources section found")
    return warnings


def check_compliance(sections: Dict[str, str]) -> Tuple[List[str], List[str]]:
    """Cross-cutting (not scored, blocks Approved): §13 regulatory-risk rows must
    name a specific regulation and a named owner. Scoped to what is verifiable from
    the document — the validator cannot know the intake state, so it only checks
    §13 when it is present. Untouched template rows (no regulation, no description)
    are skipped."""
    violations: List[str] = []
    warnings: List[str] = []
    s13 = sections.get("§13", "")
    if not s13:
        return violations, warnings
    for row in parse_tables(s13):
        if "Regulation" not in row:  # operational-risk rows have no Regulation column
            continue
        reg = row.get("Regulation", "").strip("`").strip()
        reg_state = field_state(reg)
        desc_state = field_state(row.get("Risk Description", ""))
        if reg_state == "empty" and desc_state != "filled":
            continue  # unfilled template row
        rid = row.get("ID") or "<row>"
        if reg_state == "empty" or reg.lower() in {"regulatory risk", "compliance risk", "regulation"}:
            violations.append(f"§13: Regulatory risk row {rid} does not name a specific regulation")
        owner_state = field_state(row.get("Owner", ""))
        if owner_state == "empty":
            violations.append(f"§13: Regulatory risk row {rid} has no named owner")
        elif owner_state == "tbd":
            warnings.append(
                f"§13: Regulatory risk row {rid} owner is [TBD] — a TBD owner needs a deadline for assignment"
            )
    return violations, warnings


def check_diagrams(content: str) -> List[str]:
    """Cross-cutting (not scored): Mermaid diagrams are an advisory enhancement and
    never change the score. Each ```mermaid block must close, start with a supported
    header (flowchart / graph / sequenceDiagram), have a non-empty body with at least
    one node or message, and carry no leftover skeleton placeholders. A `[TBD]` node
    label is allowed (per prompts/diagram-rules.md) and is not flagged here."""
    warnings: List[str] = []
    blocks = MERMAID_BLOCK.findall(content)
    if len(MERMAID_OPEN.findall(content)) > len(blocks):
        warnings.append("§diagrams: a ```mermaid block is not closed with a matching ```")
    for idx, body in enumerate(blocks, start=1):
        lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
        if not lines:
            warnings.append(f"§diagrams: mermaid block {idx} is empty")
            continue
        if not lines[0].lower().startswith(VALID_DIAGRAM_HEADERS):
            warnings.append(
                f"§diagrams: mermaid block {idx} has an unrecognized type "
                f"'{lines[0].split()[0]}' — use flowchart or sequenceDiagram"
            )
        if len(lines) < 2:
            warnings.append(
                f"§diagrams: mermaid block {idx} has a header but no nodes or messages"
            )
        placeholder = DIAGRAM_PLACEHOLDER.search(body)
        if placeholder:
            warnings.append(
                f"§diagrams: mermaid block {idx} contains an unfilled placeholder "
                f"'{placeholder.group(0)}'"
            )
    return warnings


CHECKERS = {
    "§1": check_section_1,
    "§2": check_section_2,
    "§3": check_section_3,
    "§4": check_section_4,
    "§5": check_section_5,
    "§6": check_section_6,
    "§7": check_section_7,
    "§8": check_section_8,
    "§9": check_section_9,
    "§10": check_section_10,
    "§11": check_section_11,
    "§12": check_section_12,
}


def validate(path: Path) -> Dict[str, Any]:
    content = path.read_text(encoding="utf-8")
    sections = split_sections(content)
    results: Dict[str, Any] = {
        "path": str(path),
        "note": (
            "Structural baseline only — the model layers semantic checks "
            "(see prompts/validation-rules.md) on top of every section."
        ),
        "sections": {},
        "violations": [],
        "warnings": [],
    }
    total = 0
    for key, max_pts in SECTION_MAX.items():
        section_text = sections.get(key, "")
        if not section_text:
            msg = f"{key}: Section is missing entirely"
            results["sections"][key] = {
                "name": SECTION_NAMES[key],
                "score": 0,
                "max": max_pts,
                "violations": [msg],
                "warnings": [],
                "tbd": 0,
            }
            results["violations"].append(msg)
            continue
        score, viol, warn = CHECKERS[key](section_text)
        results["sections"][key] = {
            "name": SECTION_NAMES[key],
            "score": score,
            "max": max_pts,
            "violations": viol,
            "warnings": warn,
            "tbd": count_tbd(section_text),
        }
        results["violations"].extend(viol)
        results["warnings"].extend(warn)
        total += score
    # Cross-cutting checks (not scored — advisory, or approval-blocking for compliance).
    citation_warnings = check_citations(content)
    compliance_violations, compliance_warnings = check_compliance(sections)
    diagram_warnings = check_diagrams(content)
    results["warnings"].extend(citation_warnings)
    results["warnings"].extend(compliance_warnings)
    results["warnings"].extend(diagram_warnings)
    results["violations"].extend(compliance_violations)
    results["cross_checks"] = {
        "citation_warnings": citation_warnings,
        "compliance_violations": compliance_violations,
        "compliance_warnings": compliance_warnings,
        "diagram_warnings": diagram_warnings,
    }
    results["score"] = total
    results["max_score"] = sum(SECTION_MAX.values())
    results["band"] = score_band(total)
    results["tbd_count"] = sum(s["tbd"] for s in results["sections"].values())
    return results


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Deterministic baseline validator for NatPRD PRDs.",
    )
    parser.add_argument("path", help="Path to the PRD markdown file")
    args = parser.parse_args()
    path = Path(args.path)
    if not path.is_file():
        print(json.dumps({"error": f"File not found: {path}"}), file=sys.stderr)
        return 2
    try:
        results = validate(path)
    except Exception as e:
        print(
            json.dumps({"error": f"Validation crashed: {type(e).__name__}: {e}"}),
            file=sys.stderr,
        )
        return 3
    json.dump(results, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
