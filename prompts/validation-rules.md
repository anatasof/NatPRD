# Validation Rules — PRD Scoring

Run this validation after generation (Mode 1) or during review (Mode 2).
Score the PRD out of 100. Report score, violations, and warnings separately.

---

## Scoring Rubric

| Section | Max Points | How to Score |
|---|---|---|
| §1 Initiative Name | 3 | 3 = valid noun phrase ≤8 words. 1 = present but has issues. 0 = absent or invalid. |
| §2 Document Status | 5 | 5 = valid status + named reviewers + named approvers + version. Deduct 2 for unnamed reviewers. Deduct 2 if status is Approved or beyond and no named approver is listed. Deduct 1 per missing field. |
| §3 Background | 10 | 10 = pain-led, evidence cited, cost of inaction present. Deduct 3 if solution-led. Deduct 3 if no evidence. Deduct 2 if no cost of inaction. |
| §4 Objective | 10 | 10 = outcome statement + numeric KRs + company OKR link. Deduct 4 if objective is feature-based. Deduct 2 per KR missing baseline or target. Deduct 2 if no OKR link. |
| §5 Scope & Boundaries | 8 | 8 = both In + Out scope present, Out has reasons, platform/segment stated. Deduct 3 if Out scope absent. Deduct 2 if Out items have no reasons. Deduct 2 if no platform/segment. |
| §6 Hypothesis | 8 | 8 = template used, falsifiable, confidence level + falsification condition present. Deduct 3 if template not followed. Deduct 3 if not falsifiable. Deduct 1 each for missing confidence or falsification condition. |
| §7 Success Metrics | 10 | 10 = leading + lagging + guardrail, all rows complete. Deduct 3 if no leading metric. Deduct 3 if no lagging metric. Deduct 2 if no guardrail. Deduct 1 per incomplete metric row. |
| §8 Requirements | 20 | 20 = all user stories with specific roles, ≥2 Gherkin scenarios each, MoSCoW tagged, NFRs with verification. Deduct 3 per story that is not a user story. Deduct 2 per story with generic role. Deduct 3 per story with <2 Gherkin scenarios. Deduct 1 per story with no MoSCoW. Deduct 2 per NFR without verification method. |
| §9 Solution | 8 | 8 = design links present, coverage map complete, alternatives listed with reasons. Deduct 3 if no design links. Deduct 2 if no coverage map. Deduct 2 if no alternatives. Deduct 1 per alternative with no reason. |
| §10 Metric Monitoring | 5 | 5 = named DRI, alert thresholds, rollback trigger, review dates. Deduct 1 per missing field. |
| §11 Event & Data Tracking | 8 | 8 = noun_verb naming, events map to metrics, sign-off present. Deduct 2 per event with invalid naming. Deduct 2 per event with no metric mapping. Deduct 2 if sign-off checkbox is absent. |
| §12 FAQ | 5 | 5 = at least one entry, open items have owners. 3 = present but no owners on open items. 0 = absent. |
| **Total** | **100** | |

---

## Score Bands

| Score | Band | Recommendation |
|---|---|---|
| 90–100 | **Excellent** | Ready to move to `In Review` |
| 75–89 | **Good** | Fix flagged warnings before circulating |
| 60–74 | **Needs Work** | Several sections incomplete — revise before sharing |
| Below 60 | **Not Ready** | Major gaps — do not circulate |

---

## Validation Report Format

After scoring, output the report in this format:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PRD VALIDATION REPORT
Initiative: [Name]
Score: [X]/100 — [Band]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VIOLATIONS (must fix before In Review):
  §3 Background — No evidence cited for problem claim
  §8 Requirements — US-002 has only 1 Gherkin scenario (minimum 2 required)
  §8 Requirements — US-003 user role is "user" — must be a specific role

WARNINGS (should fix, do not block):
  §7 Metrics — Metric owner listed as "Data Team" — name an individual
  §9 Solution — Design artifacts marked as Draft — flag for reviewers
  §11 Tracking — Data team sign-off is Pending

SECTIONS PASSING:
  ✓ §1 Initiative Name (3/3)
  ✓ §2 Document Status (5/5)
  ✓ §4 Objective (10/10)
  ✓ §5 Scope & Boundaries (8/8)
  ...

Next Steps:
  1. Fix all VIOLATIONS listed above
  2. Re-run validation: "validate my PRD"
  3. Address WARNINGS before circulating to stakeholders
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Optional Section Validation

If optional sections are present, validate them against their rules in `section-rules.md`.
Add their violations and warnings to the report.
Optional sections are not scored (they do not contribute to the 100-point total)
but violations in them block the PRD from being marked `Approved`.

---

## Deterministic Validator Coverage

`scripts/validate.py` enforces the *structural* subset of this rubric. The scoring total is
unchanged at **100** — the checks below enforce existing rubric items; they do not add points.

| Section | Deterministic check | Notes |
|---|---|---|
| §1, §2, §6, §7, §8, §11 | As before | — |
| §8 MoSCoW | Missing MoSCoW is a **violation** (−1) | Now matches `section-rules.md` §8 (was previously emitted as a warning) |
| §10 Metric Monitoring | DRI / dashboard / primary alert threshold / rollback trigger / ≥1 review date present (−1 each) | Named-vs-team DRI stays a semantic check for the model |
| §12 FAQ | ≥1 entry and open items have owners → 5; present but missing → 3 | Zero entries warns; absent scores 0 |
| §3, §4, §5, §9 | None (semantic-only) | Full marks; model layers checks on top |

**Cross-cutting checks** (emitted under a `cross_checks` object, not added to the section score):

- **Citations** (`citation_warnings`): every inline `[source: …]` should carry a `retrieved:` date,
  and a `References / Sources` section should exist. Reported as warnings.
- **Compliance** (`compliance_violations`): when §13 contains a regulatory-risk table, each row must
  name a specific regulation (not generic "regulatory risk") and a named owner. Reported as
  violations — these block `Approved` but do not change the score (§13 is optional/unscored). The
  validator only checks §13 when present; it cannot know the intake state, so the model still
  enforces "compliance signals confirmed → Regulatory Context required".
