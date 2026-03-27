---
name: NatPRD
description: Activate this skill when the user wants to create, update, validate, or review a Product Requirement Document. Triggers on mentions of PRD, product requirements, user stories, acceptance criteria, or initiative documentation, or when the user describes a feature and asks for structured documentation.
compatibility: "Claude Code CLI and Desktop — install to ~/.claude/skills/NatPRD/"
license: "BSD-3-Clause"
metadata:
  version: "1.0.0"
  author: "Anata"
---

# PRD Maker

An interactive, guided PRD generation skill for writing production-grade PRDs.
Produces fully structured PRDs with user stories, Gherkin acceptance criteria,
section-level rules, and optional sections — all in markdown format.

---

## What This Skill Does

When activated, this skill:

1. **Interviews** the user section by section using focused questions
2. **Validates** each answer against the section rules before moving on
3. **Writes** the PRD incrementally, showing each section as it's completed
4. **Enforces** the PRD standard — no placeholders, no rule violations allowed
5. **Outputs** a complete `prd.md` file saved to `docs/prd.md` in the current project

---

## How to Activate

In Claude Code, simply say:
- `"I want a PRD for [feature/initiative name]"`
- `"Help me write a PRD"`
- `"Create a PRD for [description]"`
- `"Review my PRD"` — to validate an existing PRD file

Claude will detect the intent and load this skill automatically.

---

## PRD Standard

### Structure

The PRD has **12 core sections** (always required) and **4 optional sections** (include when triggered).

**Core Sections:**
1. Initiative Name
2. Document Status
3. Background
4. Objective
5. Scope & Boundaries
6. Hypothesis
7. Success Metrics
8. Requirements
9. Solution
10. Metric Monitoring
11. Event & Data Tracking
12. FAQ

**Optional Sections** (include only when trigger condition is met):
13. Risks & Mitigations — when initiative touches payments, compliance, regulated data, or multi-team dependencies
14. Dependencies — when blocked by or blocking another team, or relies on a third-party system
15. Launch Plan — when feature requires coordinated rollout, staged release, or compliance gate
16. Stakeholder Map — when initiative spans more than 3 teams or requires executive visibility

### Requirements Format
All requirements are **user stories**:
> "As a [specific role], I want to [action], so that [benefit]."

All acceptance criteria are in **Gherkin syntax** with minimum 2 scenarios per story:
- Scenario 1: Happy path
- Scenario 2: Edge case or failure path

### Section Rules Summary (full rules in `prompts/section-rules.md`)
- **§1 Name:** Max 8 words, noun phrase, matches Jira/roadmap
- **§2 Status:** Fixed vocabulary only, no dev before Approved, named reviewers
- **§3 Background:** Lead with pain not solution, cite evidence, state cost of inaction
- **§4 Objective:** One outcome, numeric KRs with baseline+target, traceable to company OKR
- **§5 Scope:** Explicit In + Out of scope, Out items must have reasons
- **§6 Hypothesis:** Template required, must be falsifiable, include confidence level
- **§7 Metrics:** Primary (leading+lagging) + guardrail, all need baseline/target/method/owner
- **§8 Requirements:** User stories with specific role, Gherkin min 2 scenarios, MoSCoW
- **§9 Solution:** Link designs not prose, coverage map per US, rejected alternatives required
- **§10 Monitoring:** Named DRI, alert thresholds pre-launch, rollback trigger defined
- **§11 Tracking:** noun_verb naming, every event maps to §7 metric, data team sign-off
- **§12 FAQ:** Add questions immediately, open items need owner, never delete resolved

---

## Version and Date Auto-Update Rules

These rules apply automatically whenever Claude writes or saves `docs/prd.md`. No manual entry is needed.

### Last Updated

- Always set `Last Updated` to today's date in `YYYY-MM-DD` format.
- Apply on every write: new PRD creation, section edit, status change, or validation fix.
- Use the current date from your context (`currentDate`). Do not invent a date.

### Version

Use the `vX.Y` format. Read the existing `Version` field from `docs/prd.md` before writing. Parse `vX.Y` into X and Y as integers and apply the matching rule:

| Trigger | Rule | Example |
|---|---|---|
| New PRD created (Mode 1) | Set to `v0.1` | — |
| Any section added or edited (no status change) | Increment Y by 1 | `v0.2` → `v0.3` |
| Status change: `Draft` → `In Review` | Increment Y by 1 | `v0.3` → `v0.4` |
| Status change: `In Review` → `Approved` | Increment X by 1, reset Y to 0 | `v0.4` → `v1.0` |
| Status change: `Approved` → `In Execution` | Increment X by 1, reset Y to 0 | `v1.0` → `v2.0` |
| Status change: any → `Deprecated` | Increment Y by 1 | `v2.1` → `v2.2` |

**Precedence:** When a status change and a content edit occur in the same save, apply the status-change rule only. Do not double-increment.

**Fallback:** If the existing Version field is absent or unreadable, treat it as `v0.0` before applying the rule (first increment → `v0.1`).

---

## Workflow

### Mode 1: Generate (default)
Used when user wants to create a new PRD from scratch.

```
Step 1 — Intake
  Ask for initiative name and one-line summary.
  Determine which optional sections are needed.

Step 2 — Guided Interview
  Work through each section in order.
  Ask focused questions per section (see prompts/interview-questions.md).
  Validate each answer against section rules before proceeding.
  Show the completed section output before moving to the next.

Step 3 — Requirements Deep Dive
  For Section 8, collect all user stories one at a time.
  For each story: role → action → benefit → scenarios.
  Ask "Any more stories?" after each one until the user signals done.

Step 4 — Optional Sections Check
  Based on intake answers, recommend which optional sections to include.
  Generate each one if confirmed.

Step 5 — Output
  Apply Version and Date Auto-Update Rules: set Version to v0.1, set Last Updated to today's date.
  Assemble and write the complete PRD to docs/prd.md.
  Run quality validation (see prompts/validation-rules.md).
  Report validation score and any warnings.
  Offer a summary of what was generated.
```

### Mode 2: Review
Used when the user says "review my PRD" or provides an existing PRD file.

```
Step 1 — Read the existing PRD file.
Step 2 — Run validation against all section rules.
Step 3 — Report: score, issues found, sections that need work.
Step 4 — Offer to fix specific sections interactively.
  After each fix is written to the file: apply Version and Date Auto-Update Rules
  (content-edit rule, or status-change rule if the Status field was modified).
```

### Mode 3: Update
Used when the user wants to revise a specific section of an existing PRD.

```
Step 1 — Identify the target section.
Step 2 — Show the current content of that section.
Step 3 — Ask focused questions to gather new/updated content.
Step 4 — Rewrite the section and update the file. Apply Version and Date Auto-Update Rules
  before saving (content-edit rule, or status-change rule if the Status field was modified).
Step 5 — Re-run validation on the updated section.
```

---

## Output

- PRD file: `docs/prd.md`
- Validation report: printed inline after generation
- Optional: `docs/prd-summary.md` — one-page summary for stakeholders

---

## File References

| File | Purpose |
|---|---|
| `SKILL.md` | This file — skill entry point and workflow |
| `templates/prd-template.md` | The blank PRD template |
| `templates/prd-summary-template.md` | One-page stakeholder summary template |
| `prompts/interview-questions.md` | Questions to ask per section during generation |
| `prompts/section-rules.md` | Full rules for every section — used for validation |
| `prompts/validation-rules.md` | Scoring rubric and validation logic |
| `examples/prd-example.md` | A filled example PRD for reference |

---

## Installation

### Claude Code (CLI, Desktop, or VS Code extension) — recommended

**Terminal (developers):**
```bash
git clone https://github.com/anatasof/NatPRD.git ~/.claude/skills/NatPRD
```
Restart Claude Code — the skill loads automatically.

**No terminal (everyone else):**
1. Go to [github.com/anatasof/NatPRD](https://github.com/anatasof/NatPRD)
2. Click the green **Code** button → **Download ZIP**
3. Unzip it and rename the folder to `NatPRD`
4. Move it into your Claude skills folder:
   - **Mac:** Open Finder → press `⌘ Shift G` → paste `~/.claude/skills` → drop the folder in
   - **Windows:** Navigate to `C:\Users\[your name]\.claude\skills\`
5. Restart Claude Code

Once installed, start Claude Code in any project and say:
> "I want a PRD for [your feature]"

### Claude.ai web and Claude mobile app

Skills aren't natively supported, but you can load this via the **Customize** feature or a **Project**:

**Option A — Project instructions (recommended):**
1. Open Claude.ai or the Claude mobile app and create a new Project
2. Open the project → click **Edit project instructions**
3. Copy the full contents of this `SKILL.md` file and paste it in
4. Save — every conversation in that project follows the PRD workflow

**Option B — Customize Claude (applies to all your chats):**
1. Open Claude.ai → click your profile → **Customize Claude**
2. Paste the contents of this `SKILL.md` into the instructions field
3. Save

**Note:** Claude.ai and mobile have no file system access. Claude generates the PRD content in chat — copy it and save it as `docs/prd.md`.

---

## Quality Validation Scoring

After generation, the skill scores the PRD out of 100:

| Section | Points | Key Check |
|---|---|---|
| Initiative Name | 3 | ≤8 words, noun phrase |
| Document Status | 5 | Valid status, named reviewers |
| Background | 10 | Evidence cited, cost of inaction present |
| Objective | 10 | Numeric KRs, company OKR link |
| Scope & Boundaries | 8 | Both In + Out scope, reasons on Out |
| Hypothesis | 8 | Template used, falsification condition present |
| Success Metrics | 10 | Leading + lagging + guardrail, all fields complete |
| Requirements | 20 | User stories, specific roles, ≥2 Gherkin scenarios each |
| Solution | 8 | Design links present, coverage map complete, alternatives listed |
| Metric Monitoring | 5 | Named DRI, alert thresholds, rollback trigger |
| Event & Data Tracking | 8 | noun_verb naming, events map to metrics, sign-off checkbox |
| FAQ | 5 | At least one entry, open items have owners |
| **Total** | **100** | |

Score bands:
- **90–100:** Excellent — ready for `In Review`
- **75–89:** Good — minor fixes needed
- **60–74:** Needs work — several sections incomplete
- **Below 60:** Not ready — major gaps, do not circulate

---

## License
BSD 3-Clause — free to use and redistribute, with attribution. Do not use the author's name to endorse derived works.
