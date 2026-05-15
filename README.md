# PRD Maker

> An interactive Claude Code skill that guides you through writing production-grade PRDs. Section by section, with built-in validation, user story, and Gherkin acceptance criteria.

Built on the **Common PRD Standards** — 12 core sections, 4 optional sections, full rules per section.

---

## What It Does

- **Runs an upfront intake** to gather product type, platform, team structure, compliance exposure, and discovery maturity before any section begins — so every subsequent question is targeted and context-aware
- **Identifies applicable regulations** when compliance signals are present (payments, eKYC, PII, regulated data) — maps them to GDPR, PCI-DSS, HIPAA, OJK, and others, confirms the list with you, and propagates them into Background, Scope, and Risks automatically
- **Interviews** you section by section with focused, contextual questions
- **Validates** every answer against the section rules before moving on
- **Enforces** user story format for all requirements
- **Generates** Gherkin acceptance criteria automatically
- **Never fabricates content** — if you don't have an answer, it writes `[TBD]` instead of inventing metrics, names, dates, or evidence
- **Scores** the completed PRD out of 100 with a detailed validation report
- **Outputs** a production-ready `docs/prd.md` file

---

## Installation

### Claude Code (CLI, Desktop, or VS Code extension) — recommended

**Terminal (developers):**
```bash
git clone https://github.com/anatasof/NatPRD.git ~/.claude/skills/natprd
```
Restart Claude Code — the skill loads automatically.

**No terminal (everyone else):**
1. Go to [github.com/anatasof/NatPRD](https://github.com/anatasof/NatPRD)
2. Click the green **Code** button → **Download ZIP**
3. Unzip it and rename the folder to `natprd` (lowercase)
4. Move it into your Claude skills folder:
   - **Mac:** Open Finder → press `⌘ Shift G` → paste `~/.claude/skills` → drop the folder in
   - **Windows:** Navigate to `C:\Users\[your name]\.claude\skills\`
5. Restart Claude Code

The skill loads automatically. Just say what you need and Claude handles the rest.

> **Migrating from an earlier version?** If you previously installed at `~/.claude/skills/NatPRD/`, rename it to `~/.claude/skills/natprd/` (or `mv ~/.claude/skills/NatPRD ~/.claude/skills/natprd`). The frontmatter name was lowercased to match Claude Code's skill conventions.

### Claude app (web, desktop, and mobile)

No native skill install — load it manually instead:

**Option A — Project instructions (recommended, available on all platforms):**
1. Create a new Project in the Claude app
2. Open the project → click **Edit project instructions**
3. Copy the full contents of `SKILL.md` from this repo and paste it in
4. Save — every conversation in that project follows the PRD workflow

**Option B — Customize Claude (applies to all your chats):**
1. Click your profile → **Customize Claude**
2. Paste the contents of `SKILL.md` into the instructions field
3. Save

**Note:** The Claude app has no file system access. Claude generates the PRD content in chat — copy it and save it yourself as `docs/prd.md`.

---

## Usage

Start Claude Code in any project directory, then use natural language:

```
# Create a new PRD
"I want a PRD for adding two-factor authentication"
"Help me write a PRD for the merchant onboarding flow"
"Create a PRD for our loyalty points system"

# Review an existing PRD
"Review my PRD"
"Validate the PRD at docs/prd.md"

# Update a specific section
"Update the hypothesis in the PRD"
"Add a new user story to the requirements section"

# Generate a stakeholder summary
"Generate a summary of the PRD for stakeholders"
```

---

## PRD Structure

### Core Sections (always required)
1. Initiative Name
2. Document Status ← status, version, author, owner, reviewers, approvers, approval date
3. Background
4. Objective
5. Scope & Boundaries
6. Hypothesis
7. Success Metrics
8. Requirements ← user stories + Gherkin AC + NFRs
9. Solution
10. Metric Monitoring
11. Event & Data Tracking
12. FAQ

### Optional Sections
13. Risks & Mitigations — regulatory risk rows (one per confirmed regulation) + operational risks; legal sign-off checkpoint included
14. Dependencies — for cross-team or third-party work
15. Launch Plan — for coordinated rollouts
16. Stakeholder Map — for cross-functional initiatives

---

## Validation Scoring

After generation, the PRD is scored out of 100:

| Band | Score | Meaning |
|---|---|---|
| Excellent | 90–100 | Ready for `In Review` |
| Good | 75–89 | Fix warnings before circulating |
| Needs Work | 60–74 | Several sections incomplete |
| Not Ready | <60 | Major gaps — do not circulate |

---

## File Structure

```
natprd/
├── SKILL.md                          ← Skill entry point (Claude Code reads this)
├── README.md                         ← This file
├── templates/
│   ├── prd-template.md               ← Blank PRD template
│   └── prd-summary-template.md       ← One-page stakeholder summary
├── prompts/
│   ├── interview-questions.md        ← Questions asked per section during generation
│   ├── section-rules.md              ← Full rules per section (used in validation)
│   └── validation-rules.md           ← Scoring rubric and report format
└── scripts/
    └── validate.py                   ← Deterministic baseline validator (Python 3, stdlib only)
```

### Validation script

You can also run the deterministic baseline validator directly:

```bash
python3 scripts/validate.py docs/prd.md
```

Outputs JSON with per-section scores, violations, and warnings. No dependencies — stdlib only.

---

## Network Access

The skill declares `WebFetch` in its `allowed-tools` so it can fetch public URLs the user explicitly references during the interview (research articles, regulatory body pages, vendor docs). Every fetched fact is shown to you for confirmation before it lands in the PRD, carries an inline `[source: …, retrieved: YYYY-MM-DD]` annotation, and is quoted directly — never paraphrased.

The skill never goes searching for sources on its own (no `WebSearch`). Auth-walled tools (Confluence, Jira, internal wikis) cannot be fetched — you'll be asked to paste the relevant excerpt instead.

If you don't want any outbound network calls, remove `WebFetch` from the `allowed-tools` line in `SKILL.md`. The skill will still work — it'll just ask you to paste excerpts for every URL.

---

## Modes

| Mode | Trigger | What Happens |
|---|---|---|
| **Generate** | "I want a PRD for..." | Upfront intake → guided section interview → optional sections → full PRD output |
| **Review** | "Review my PRD" | Reads existing file → validates → scores → report |
| **Update** | "Update [section]" | Targets one section → re-interviews → rewrites → re-validates |

---

## Compliance-Aware Workflow

When a compliance signal is confirmed at intake (payments, eKYC, KYB, PII, biometrics, healthcare, or cross-border data), the skill runs a dedicated regulation identification step before the main interview. It presents a signal-to-regulation mapping (GDPR, PCI-DSS, HIPAA, OJK, PDPA, and more), confirms the list with you, and carries the confirmed regulations forward automatically:

- **Background** — adds a Regulatory Context table with jurisdiction, key obligations, and review status
- **Scope** — flags regulatory-driven in/out-of-scope items separately so reviewers can trace them
- **Risks & Mitigations** — adds one risk row per confirmed regulation with mitigation, contingency, named owner, and a legal/compliance sign-off checkbox

If you don't know which regulations apply, the skill writes `[TBD — legal/compliance to confirm]` and flags it as an open item rather than inventing requirements.

---

## Output

- **PRD file:** `docs/prd.md`
- **Validation report:** Printed inline after generation
- **Summary (optional):** `docs/prd-summary.md`

---

## FAQ

**Q: Does this work outside Claude Code?**
A: Yes, with a manual step. Paste the contents of `SKILL.md` into a Project's instructions on Claude.ai (web or mobile), or into the **Customize** feature. The PRD workflow works the same way — the only difference is Claude cannot save files for you, so you copy the output yourself.

**Q: Why does it ask so many questions upfront before the PRD sections start?**
A: The intake phase gathers context about your product type, platform, team structure, compliance exposure, and discovery maturity. Without it, Claude would have to guess — and guessing leads to invented metrics, fabricated design links, and hallucinated evidence. The intake makes every subsequent question more specific and the output more accurate.

**Q: Can I customise the template?**
A: Yes. Edit `templates/prd-template.md` and `prompts/section-rules.md` to match your team's standards.

---

## License
BSD 3-Clause — free to use and redistribute, with attribution. Do not use the author's name to endorse derived works.
