# prd-maker

> An interactive Claude Code skill that guides you through writing production-grade PRDs. Section by section, with built-in validation, user story, and Gherkin acceptance criteria.

Built on the **Common PRD Standards** — 12 core sections, 4 optional sections, full rules per section.

---

## What It Does

- **Runs an upfront intake** to gather product type, platform, team structure, compliance exposure, and discovery maturity before any section begins — so every subsequent question is targeted and context-aware
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

The skill loads automatically. Just say what you need and Claude handles the rest.

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
2. Document Status
3. Background
4. Objective
5. Scope & Boundaries
6. Hypothesis
7. Success Metrics
8. Requirements ← user stories + Gherkin AC
9. Solution
10. Metric Monitoring
11. Event & Data Tracking
12. FAQ

### Optional Sections
13. Risks & Mitigations — for compliance, payments, regulated data
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
prd-maker/
├── SKILL.md                          ← Skill entry point (Claude Code reads this)
├── README.md                         ← This file
├── templates/
│   ├── prd-template.md               ← Blank PRD template
│   └── prd-summary-template.md       ← One-page stakeholder summary
├── prompts/
│   ├── interview-questions.md        ← Questions asked per section during generation
│   ├── section-rules.md              ← Full rules per section (used in validation)
│   └── validation-rules.md           ← Scoring rubric and report format
└── examples/
    └── prd-example.md                ← Filled example PRD for reference
```

---

## Modes

| Mode | Trigger | What Happens |
|---|---|---|
| **Generate** | "I want a PRD for..." | Upfront intake → guided section interview → optional sections → full PRD output |
| **Review** | "Review my PRD" | Reads existing file → validates → scores → report |
| **Update** | "Update [section]" | Targets one section → re-interviews → rewrites → re-validates |

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
