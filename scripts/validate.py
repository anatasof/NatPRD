#!/usr/bin/env python3
"""Deterministic baseline validator for NatPRD PRDs.

Usage:
    python3 scripts/validate.py <path-to-prd.md>

Outputs JSON to stdout with per-section scores, violations, and warnings.
Exits 0 on success, 2 on file-not-found, 3 on parse/crash.

This script implements the *structural* checks from prompts/validation-rules.md.
Semantic checks (pain-led background, coverage map completeness, named DRI vs
team name) are intentionally NOT implemented — those require the model. Sections
without deterministic checks return full marks here and are flagged
"semantic_only": true. The model layers its own checks on top.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

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
SEMANTIC_ONLY = {"§3", "§4", "§5", "§9", "§10", "§12"}

TBD_PATTERN = re.compile(r"\[TBD[^\]]*\]")
H2_PATTERN = re.compile(r"^## (\d+)\.\s+(.+?)\s*$", re.MULTILINE)
PLACEHOLDER_PATTERN = re.compile(r"^\[[A-Z][^\]]*\]$")
USER_STORY_PATTERN = re.compile(
    r"As an?\s+(?P<role>[^,]+?),\s+I want\s+.+?,\s+so that\s+.+",
    re.IGNORECASE,
)
EVENT_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9]*(_[a-z0-9]+)+$")


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


def is_filled(value: str) -> bool:
    """A value is 'filled' if not empty, not a dash, and not an unfilled placeholder."""
    if not value:
        return False
    v = value.strip().strip("`").strip()
    if not v or v in {"—", "-", "–"}:
        return False
    if v.upper().startswith("[TBD"):
        return True  # TBD counts as filled for rubric purposes; surfaced as warning elsewhere.
    if PLACEHOLDER_PATTERN.match(v):
        return False
    return True


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
        if not s or s.startswith(("#", "|", ">", "-", "*")):
            continue
        name = s.strip("`").strip()
        break
    if not name:
        violations.append("§1: Initiative name is empty")
        return 0, violations, warnings
    if PLACEHOLDER_PATTERN.match(name):
        violations.append(f"§1: Initiative name is still a placeholder: {name}")
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
    if not is_filled(kv.get("Reviewers", "")):
        violations.append("§2: Reviewers field is empty or placeholder")
        score -= 2
    if status in APPROVED_OR_BEYOND:
        if not is_filled(kv.get("Approvers", "")):
            violations.append("§2: Approvers required when Status is Approved or beyond")
            score -= 2
        if not is_filled(kv.get("Approval Date", "")):
            violations.append("§2: Approval Date required when Status is Approved or beyond")
            score -= 1
    for field in ("Author", "Owner"):
        if not is_filled(kv.get(field, "")):
            warnings.append(f"§2: {field} field is empty or placeholder")
            score -= 1
    return max(0, score), violations, warnings


def check_section_6(text: str) -> Tuple[int, List[str], List[str]]:
    violations: List[str] = []
    warnings: List[str] = []
    score = 8
    template = re.search(
        r"[Ww]e believe\s+.+?\s+for\s+.+?\s+will result in\s+.+?\s+because\s+.+",
        text,
        re.DOTALL,
    )
    if not template:
        violations.append("§6: Hypothesis does not match 'We believe X for [segment] will result in Y because Z'")
        score -= 3
    if not re.search(r"falsif|prove\s+(it\s+)?wrong|disprov", text, re.IGNORECASE):
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
    has_leading = has_lagging = False
    for row in rows:
        identifier = row.get("Metric") or next(iter(row.values()), "<row>")
        baseline = row.get("Baseline", "")
        # Guardrail rows often use "Alert Threshold" / "Threshold" in place of "Target".
        target = (
            row.get("Target")
            or row.get("Alert Threshold")
            or row.get("Threshold")
            or ""
        )
        if not is_filled(baseline):
            violations.append(f"§7: Metric row missing baseline: {identifier}")
            score -= 1
        if not is_filled(target):
            violations.append(f"§7: Metric row missing target/threshold: {identifier}")
            score -= 1
        type_val = row.get("Type", "").lower()
        if "leading" in type_val:
            has_leading = True
        if "lagging" in type_val:
            has_lagging = True
    if not has_leading:
        violations.append("§7: No leading indicator metric identified")
        score -= 3
    if not has_lagging:
        violations.append("§7: No lagging indicator metric identified")
        score -= 3
    if not re.search(r"guardrail", text, re.IGNORECASE):
        violations.append("§7: No guardrail metric section identified")
        score -= 2
    return max(0, score), violations, warnings


def check_section_8(text: str) -> Tuple[int, List[str], List[str]]:
    violations: List[str] = []
    warnings: List[str] = []
    score = 20
    story_blocks = re.split(r"(?=^###\s+(?:US-|User Story|Story))", text, flags=re.MULTILINE)
    story_blocks = [b for b in story_blocks if USER_STORY_PATTERN.search(b)]
    if not story_blocks:
        if USER_STORY_PATTERN.search(text):
            story_blocks = [text]
        else:
            violations.append(
                "§8: No user stories found in 'As a [role], I want [action], so that [benefit]' format"
            )
            return 0, violations, warnings
    for block in story_blocks:
        story_id_match = re.search(r"US-\d+|Story\s+\d+", block)
        story_id = story_id_match.group(0) if story_id_match else "<unidentified>"
        role_match = re.search(r"As an?\s+([^,]+?),", block, re.IGNORECASE)
        if role_match:
            role = role_match.group(1).strip().lower()
            if role in {"user", "a user", "the user", "users", "customer"}:
                violations.append(f"§8: {story_id} uses generic role '{role}' — must be specific")
                score -= 2
        scenarios = re.findall(r"^\s*Scenario\b[^\n]*", block, re.MULTILINE | re.IGNORECASE)
        if not scenarios:
            scenarios = re.findall(r"^\s*Given\s+", block, re.MULTILINE)
        if len(scenarios) < 2:
            violations.append(f"§8: {story_id} has fewer than 2 Gherkin scenarios (found {len(scenarios)})")
            score -= 3
        if not re.search(r"Must[-\s]?have|Should[-\s]?have|Could[-\s]?have|Won.t[-\s]?have", block, re.IGNORECASE):
            warnings.append(f"§8: {story_id} missing MoSCoW priority")
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
    for row in rows:
        name = (row.get("Event Name") or row.get("Event") or row.get("Name") or "").strip("`").strip()
        if not name or PLACEHOLDER_PATTERN.match(name):
            continue
        if not EVENT_NAME_PATTERN.match(name):
            violations.append(f"§11: Event name '{name}' does not match noun_verb convention")
            score -= 2
    if not re.search(r"sign[-\s]?off|signoff", text, re.IGNORECASE):
        violations.append("§11: Data team sign-off not found")
        score -= 2
    return max(0, score), violations, warnings


CHECKERS = {
    "§1": check_section_1,
    "§2": check_section_2,
    "§6": check_section_6,
    "§7": check_section_7,
    "§8": check_section_8,
    "§11": check_section_11,
}


def validate(path: Path) -> Dict[str, Any]:
    content = path.read_text(encoding="utf-8")
    sections = split_sections(content)
    results: Dict[str, Any] = {
        "path": str(path),
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
                "semantic_only": key in SEMANTIC_ONLY,
            }
            results["violations"].append(msg)
            continue
        tbd = count_tbd(section_text)
        if key in CHECKERS:
            score, viol, warn = CHECKERS[key](section_text)
        else:
            score, viol, warn = max_pts, [], []
        results["sections"][key] = {
            "name": SECTION_NAMES[key],
            "score": score,
            "max": max_pts,
            "violations": viol,
            "warnings": warn,
            "tbd": tbd,
            "semantic_only": key in SEMANTIC_ONLY,
        }
        results["violations"].extend(viol)
        results["warnings"].extend(warn)
        total += score
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
