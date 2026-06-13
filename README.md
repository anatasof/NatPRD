# PRD Maker

> A friendly assistant for **Claude** that interviews you and writes a professional **Product Requirements Document (PRD)**, the plan behind a product or feature, without ever making up facts.

You talk, it asks smart questions, and a complete, well-structured document comes out the other end. No template wrangling. No blank-page paralysis. And above all, no invented numbers, names, or evidence.

---

## Contents

- [What is this, in plain words?](#what-is-this-in-plain-words)
- [Who is it for?](#who-is-it-for)
- [Why people use it](#why-people-use-it)
- [How it works](#how-it-works)
- [A quick example](#a-quick-example)
- [Installation](#installation)
- [How to use it](#how-to-use-it)
- [What's inside a PRD](#whats-inside-a-prd)
- [Diagrams](#diagrams)
- [Smart research features](#smart-research-features)
- [The honesty guarantee](#the-honesty-guarantee)
- [Quality score](#quality-score)
- [Where your files go](#where-your-files-go)
- [Does it use the internet?](#does-it-use-the-internet)
- [For the technically curious](#for-the-technically-curious)
- [Customize it for your team](#customize-it-for-your-team)
- [Glossary](#glossary)
- [FAQ](#faq)
- [License](#license)

---

## What is this, in plain words?

A **PRD** (Product Requirements Document) is the single document a team agrees on *before* building something. It answers: What are we building? Who is it for? Why now? How will we know it worked? What's in scope, and what isn't?

Writing a good one is hard. It's easy to leave gaps or describe a solution before you've explained the problem. And when you're in a hurry, it's easy to write down a number you *think* is right but never actually measured.

**PRD Maker** is a "skill" (an add-on) for Claude that fixes this. It:

1. **Interviews you** one question at a time, in plain language.
2. **Writes the document for you** as you answer, following a proven structure.
3. **Refuses to invent things.** If you don't know a number, it writes a clearly-marked "to be determined" placeholder instead of guessing.
4. **Checks its own work** and gives the finished document a score out of 100, with a list of anything still missing.

You end up with a document that looks like it came from an experienced product manager, because the rules of an experienced product manager are baked in.

---

## Who is it for?

- **Product managers** who want a faster path to a rigorous PRD.
- **Founders and solo builders** who've never written a PRD and want guardrails.
- **Engineers, designers, and analysts** asked to "write up" a feature.
- **Anyone in a regulated industry** (finance, health, anything touching personal data) who needs the compliance angle handled carefully.

You do **not** need to be technical. If you can have a conversation, you can use this.

---

## Why people use it

| What you might struggle with | How PRD Maker helps |
|---|---|
| Staring at a blank page | It asks you questions instead, so you just answer |
| Forgetting important sections | It walks through every required section in order |
| Vague requirements | It turns each one into a clear "user story" with testable conditions |
| Made-up or fuzzy numbers | It never fabricates; unknowns become visible `[TBD]` markers |
| "Is this good enough to share?" | It scores the document 0 to 100 and lists what's missing |
| Regulations you're unsure about | It looks up likely rules, shows you the official source, and asks you to confirm |
| Claims with no backing | Every sourced fact is quoted and linked, never paraphrased from memory |

---

## How it works

PRD Maker has three modes. You don't pick them; Claude figures out which one you want from how you ask.

| Mode | You say something like… | What happens |
|---|---|---|
| **Generate** | "I want a PRD for…" | A short intake, then a guided section-by-section interview, then a finished document |
| **Review** | "Review my PRD" | It reads an existing document, scores it, and tells you what to fix |
| **Update** | "Update the hypothesis" | It edits just one section and re-checks it |

In **Generate** mode there's a deliberate two-step rhythm:

1. **Intake first.** Before writing anything, it asks a handful of orienting questions: what kind of product, which platforms, how many teams, whether any sensitive data is involved, how far along the idea is. This is so it never has to guess later.
2. **Then the interview.** It works through each section in order, validates your answer, shows you the finished section, and moves on.

Two nice touches happen automatically: the document's **version number** ticks up as it changes (v0.1 → v0.2 → … → v1.0 when approved), and the **"last updated" date** is always kept current.

---

## A quick example

Here's the flavor of a Generate session (shortened):

```
You:  I want a PRD for letting customers pay with a QR code.

PRD Maker:  Great. A few quick questions before we start the document.
            1. What's a working name for this?
            2. In one sentence: what is it trying to do, and for whom?

You:  "QR Pay." It lets shoppers pay merchants by scanning a code.

PRD Maker:  You mentioned payments, so some financial regulations probably
            apply. Based on your market (Indonesia), these likely matter:
            PCI-DSS, Bank Indonesia's SNAP open-payment standard, and the
            personal-data law UU PDP. This is a starting point, not legal
            advice. Does that look right, or should I add/remove any?

You:  That's right.

PRD Maker:  Noted. I'll carry those into Background, Scope, and Risks.
            Now, what problem are we solving, and who feels it today?
...
```

Notice what it did: it gathered context first, flagged the compliance angle, **showed you its sources for you to confirm**, and only then started writing.

---

## Installation

### What you need

- **Claude.** Either **Claude Code** (an app that runs on your computer and works directly with your project's files) or the **Claude app** (claude.ai on the web, or the desktop app).
- That's it. There's nothing else to install. In the Claude app, the skill's helper scripts run on Claude's side. In Claude Code they use **Python 3** if your computer has it, and are skipped gracefully if not (Claude still scores the document itself either way).

### Option 1: Claude Code (recommended; it saves the PRD straight into your project)

**If you're comfortable with a terminal:**
```bash
git clone https://github.com/anatasof/NatPRD.git ~/.claude/skills/natprd
```
Restart Claude Code (or just start a new session) and the skill loads automatically.

**If you'd rather not use a terminal:**
1. Go to [github.com/anatasof/NatPRD](https://github.com/anatasof/NatPRD).
2. Click the green **Code** button → **Download ZIP**.
3. Unzip it, and rename the folder to `natprd` (all lowercase).
4. Move that folder into your Claude skills folder, creating the folder first if it doesn't exist yet:
   - **Mac:** in Finder, press `⌘ Shift G`, paste `~/.claude/skills`, press Enter, and drop the folder in. If Finder says the folder can't be found, go to `~/.claude` instead, make a new folder there named `skills` (`⌘ Shift N`), and drop `natprd` inside it.
   - **Windows:** go to `C:\Users\[your name]\.claude\`, create a folder named `skills` if there isn't one, and drop `natprd` inside it.
5. Restart Claude Code (or just start a new session).

**Check it worked:** type `/natprd` (it should autocomplete) or ask Claude *"What skills are available?"* and look for `natprd` in the answer. Then just say what you need; Claude handles the rest.

> **Upgrading from an old install?** If you previously had it at `~/.claude/skills/NatPRD/` (capital letters), rename it to lowercase `natprd`. On Mac/Linux: `mv ~/.claude/skills/NatPRD ~/.claude/skills/natprd`.

> **Installing for a whole team?** Put the same folder inside your project's repository at `.claude/skills/natprd` and commit it. Everyone who opens that project in Claude Code then gets the skill automatically.

### Option 2: Claude app (claude.ai and desktop)

The Claude app installs skills as a **ZIP upload**. It's a one-time setup that takes about two minutes.

1. **Turn on the capability (once).** In the app, open **Settings → Capabilities** and enable **Code execution and file creation**. Skills don't run without it.
2. **Get the ZIP into the right shape.** Download the repo ZIP (green **Code** button → **Download ZIP**), unzip it, rename the folder to `natprd` (all lowercase), then compress that folder back into a ZIP (right-click → **Compress** on Mac, **Send to → Compressed (zipped) folder** on Windows).
   - *Why the re-zip?* The app requires the folder inside the ZIP to match the skill's lowercase name, and GitHub's download is named `NatPRD-main`, so uploading it as-is will fail.
3. **Upload it.** In the app's settings, find **Skills** (under **Capabilities** or **Customize**, depending on version), choose **Upload skill**, and pick your `natprd` ZIP. The app reads `SKILL.md` and shows a summary; make sure the skill's toggle is **on**.

That's the whole install. Everything rides along in the ZIP: templates, rules, the regulation list, and even the helper scripts (they run on Claude's side). So scoring and regulation lookup work just like in Claude Code.

> **One difference from Claude Code:** the app can't write into a folder on your computer. The finished PRD arrives as a **downloadable file** instead; save it wherever you like (e.g. as `docs/prd.md` in your project).

> **Can't enable code execution?** Some workplaces switch it off. The older Project-based setup still works: create a **Project**, paste the entire contents of `SKILL.md` into the project instructions, and upload `prompts/interview-questions.md`, `prompts/section-rules.md`, `prompts/validation-rules.md`, `templates/prd-template.md`, and `templates/prd-summary-template.md` (plus `references/api-docs.md` if your PRDs name outside vendors) as project knowledge. Scoring uses the rubric in those files, regulation lookup falls back to the built-in table in `interview-questions.md`, and you copy the finished PRD out of the chat.

---

## How to use it

Once installed, just talk to Claude naturally:

```
Create a new PRD
  "I want a PRD for adding two-factor authentication"
  "Help me write a PRD for the merchant onboarding flow"
  "Create a PRD for our loyalty points system"

Review an existing PRD
  "Review my PRD"
  "Validate the PRD at docs/prd.md"

Change one part
  "Update the hypothesis in the PRD"
  "Add a new user story to the requirements section"

Make a short version for stakeholders
  "Generate a one-page summary of the PRD"
```

In Claude Code you can also invoke it directly by typing `/natprd`.

---

## What's inside a PRD

Every PRD has **12 core sections** (always included) and up to **4 optional sections** (added only when they're relevant; for example, the Risks section appears automatically when sensitive data is involved).

### Core sections (always)

| # | Section | In plain words |
|---|---|---|
| 1 | Initiative Name | A short, clear name for the thing you're building |
| 2 | Document Status | Who wrote it, who owns it, who reviews/approves it, and which version this is |
| 3 | Background | The problem, who it hurts, and proof it's real (plus any regulations and benchmarks) |
| 4 | Objective | The single business outcome you want, with measurable targets |
| 5 | Scope & Boundaries | What's included, what's deliberately left out, and why |
| 6 | Hypothesis | Your bet, written so it can be proven right *or* wrong |
| 7 | Success Metrics | The numbers that tell you it worked (and the ones that must not get worse) |
| 8 | Requirements | Each need written as a "user story" with testable pass/fail conditions |
| 9 | Solution | How it works for the user, with links to designs and the alternatives you rejected |
| 10 | Metric Monitoring | Who watches the dashboards after launch, and when to pull the plug |
| 11 | Event & Data Tracking | Exactly what gets measured, so the metrics in §7 actually have data |
| 12 | FAQ | Questions people have asked, with answers and owners for the open ones |

### Optional sections (only when relevant)

| # | Section | Added when… |
|---|---|---|
| 13 | Risks & Mitigations | Payments, regulated data, or multiple teams are involved |
| 14 | Dependencies | You rely on another team or an outside vendor |
| 15 | Launch Plan | The rollout is staged, phased, or needs sign-offs |
| 16 | Stakeholder Map | Several teams or external parties need to be kept in the loop |

---

## Diagrams

A wall of text is hard to picture. At a few natural points the skill can add a small **diagram**
right next to the part it illustrates, so reviewers can see a flow at a glance. Two kinds are
supported:

- A **flowchart** of a user flow (in the Requirements and Solution sections), built from the
  pass/fail scenarios you already described.
- A **sequence diagram** of how an event travels (in the Solution and Tracking sections), built
  from the event you already mapped (who triggers it, whether it is client or server side, and
  where it lands).

Three things matter about how this works:

1. **It asks first.** The skill offers a diagram, shows you the diagram text, and adds it only
   after you say yes. Nothing is drawn behind your back.
2. **It only draws what you confirmed.** A diagram is a picture of facts already in the PRD, never
   a source of new ones. It will not invent a step, a branch, or a system you did not mention; if
   something is unknown it labels it `[TBD]`, the same as everywhere else.
3. **It is just text.** Diagrams are written in **Mermaid**, a plain-text format that renders as a
   real picture on GitHub and in most Markdown viewers. There is nothing to install, and the
   diagram stays readable even where it is not rendered.

Diagrams are an optional extra. They do not change your [quality score](#quality-score); the
checker only flags a diagram that is malformed (for example, an unfinished placeholder), as a
gentle warning.

---

## Smart research features

PRD Maker can pull in real, verifiable facts, but only from sources **you point it to** or from a small built-in list of official references. It **never goes searching the web on its own**, because that's how AI tools end up citing things that don't exist.

### 1. Regulation look-up

When your idea touches money, identity, health, or personal data, the skill consults a **built-in, dated list of regulations** (`references/regulations.json`) and suggests the ones likely to apply, each with a link to the **official source**. It covers common rules across regions, including:

> GDPR, PCI-DSS, HIPAA, PSD2, CCPA/CPRA, Singapore's PDPA & MAS Notice 626, Thailand's PDPA, Indonesia's UU PDP & OJK rules & Bank Indonesia SNAP, China's PIPL, Illinois BIPA, COPPA, India's RBI rules, and the FATF anti-money-laundering standards.

It then **asks you to confirm** the list (it's a starting point, not legal advice), and can optionally fetch the official page to quote the exact obligation. If you're unsure, it writes `[TBD — legal/compliance to confirm]` rather than inventing requirements.

### 2. Benchmarks

If you want to ground a target in an industry or competitor number ("top apps in our space convert at X%"), it records it with the **source, the date, and a comparability note** (because a benchmark from a different market or definition can mislead). It will never invent a benchmark figure.

### 3. Reading API / vendor docs

If your feature relies on an outside service (a payment processor, an identity checker, a cloud vendor), the skill can read that vendor's **official documentation** and pull real limits (rate limits, quotas, uptime promises) straight into the relevant sections. If the docs don't say, it writes `[TBD — confirm with vendor docs]`.

### 4. Citations

Every fact that comes from a source is **quoted directly** (never paraphrased from memory) and tagged inline like `[source: …, retrieved: 2026-06-03]`. All sources are also collected into a single **References / Sources** list at the bottom, so a reviewer can audit where every claim came from.

---

## The honesty guarantee

This is the feature people care about most, so it's worth stating plainly:

**PRD Maker will not make things up.**

If you don't have a number, a name, a date, a design link, or evidence, it writes a visible placeholder (like `[TBD — baseline needed]` or `[No design link — status: Draft]`) instead of inventing something plausible. Those placeholders are deliberately ugly so they're easy to spot and fix, and they pull the document's score down until they're resolved.

It also pushes back gently when you're vague, and it never paraphrases a source; it quotes the exact words or number. The result is a document you can trust: anything stated as fact is either something you confirmed or something clearly marked as still-open.

---

## Quality score

When the document is done (or when you ask it to review one), PRD Maker scores it out of 100 and tells you the band:

| Score | Band | What it means |
|---|---|---|
| 90 to 100 | **Excellent** | Ready to circulate for review |
| 75 to 89 | **Good** | Solid; fix the flagged warnings first |
| 60 to 74 | **Needs Work** | Several sections are incomplete |
| Below 60 | **Not Ready** | Major gaps; don't share yet |

The report separates hard problems (**violations**: things that must be fixed) from softer ones (**warnings**: things you should look at), and lists exactly where each one is.

---

## Where your files go

- **Your PRD:** `docs/prd.md` (or any path you ask for, e.g. "save it to `prds/2026-q3-auth.md`").
- **The quality report:** shown right in the chat after it's written.
- **Optional one-page summary:** `docs/prd-summary.md`, for stakeholders who won't read the full thing.

*(In the Claude app, the PRD arrives as a downloadable file instead, and the quality report still appears in the chat.)*

---

## Does it use the internet?

**Yes, because Claude does.** The skill is just a set of instructions that Claude follows, and Claude runs by talking to Anthropic's servers over the internet (in both Claude Code and the Claude app). So this isn't an offline tool: you need a connection for it to work at all, and your conversation (including any files or text you share) is sent to Claude exactly like in a normal chat.

What the skill itself **won't** do is wander off and browse the web on its own. That part is deliberately locked down:

- It only opens a **web page you named** (or an official source it suggested and you confirmed), and it shows you every fetched fact before using it.
- It **never runs open-ended web searches.** If you didn't name a source, the skill treats it as not existing and writes a `[TBD]` instead.
- Reading **files on your computer** and the **built-in reference lists** pulls nothing extra from the web. Their contents are still processed by Claude like everything else in the chat.
- Private/locked pages (Confluence, Jira, internal wikis) can't be fetched, so it'll ask you to paste the relevant text instead.

Want to tighten that further? In Claude Code, removing `WebFetch` from the `allowed-tools` line at the top of `SKILL.md` means Claude must ask your permission before each fetch; to block fetching outright, add a `disallowed-tools: WebFetch` line below it. The skill keeps working either way; it just asks you to paste anything it would otherwise fetch. In the Claude app, web access is controlled by the app's own settings instead. (None of this makes Claude itself run offline.)

---

## For the technically curious

Everything below is optional; the skill works without you ever opening these files.

### File structure

```
natprd/
├── SKILL.md                      ← The skill's brain: instructions Claude reads
├── README.md                     ← This file
├── templates/
│   ├── prd-template.md           ← The blank PRD structure
│   └── prd-summary-template.md   ← The one-page summary structure
├── prompts/
│   ├── interview-questions.md    ← The questions asked for each section
│   ├── section-rules.md          ← The pass/fail rules for each section
│   ├── validation-rules.md       ← How the 0 to 100 score is calculated
│   └── diagram-rules.md          ← How Mermaid diagrams are proposed and drawn
├── references/
│   ├── regulations.json          ← The dated regulation list (rules → official URLs)
│   └── api-docs.md               ← Official documentation links for common vendors
└── scripts/
    ├── validate.py               ← Scores a PRD automatically (Python 3, no extra installs)
    └── lookup_regulation.py      ← Suggests regulations from the list (Python 3, no extra installs)
```

The folder follows Anthropic's open **Agent Skills** format, so the same unchanged folder also works beyond the two install options above. For example, you can upload it via the [Skills API](https://platform.claude.com/docs/en/agents-and-tools/skills) for use in agents you build on the Claude API.

### Run the checks yourself

Score any PRD file (prints a detailed JSON report: per-section scores, violations, warnings):
```bash
python3 scripts/validate.py docs/prd.md
```

See which regulations the built-in list suggests for a given situation:
```bash
# signals: payments, ekyc, pii, credit, insurance, biometric, healthcare, cross_border, children
# geo: a country code such as ID, SG, EU, US, US-CA
python3 scripts/lookup_regulation.py --signals payments,pii --geo ID
```

Both scripts use only Python's standard library, so there's nothing to install. The automated score is the *structural* baseline; Claude layers human-judgment checks (is the problem really stated before the solution? is the owner a real person, not a team?) on top.

### How the score is split

The validator checks structure deterministically (valid status, named reviewers, two test scenarios per requirement, events that map to metrics, monitoring fields filled in, open FAQ items having owners, regulation rows naming a *specific* regulation, citations carrying a date, and so on). Anything that needs judgment is left to Claude. The total is always out of 100; optional sections are checked but don't change the number.

---

## Customize it for your team

PRD Maker ships with sensible, opinionated defaults, but every team has its own house style, its own definition of "done," and its own regulations. The skill is built to be **molded to your workflow**. There are two ways in: ask Claude to make the change for you, or **fork the project** to get your own copy that you fully control. A fork lets you change whatever you like and still pull in future improvements from the original.

Everything that drives the skill is a plain **text file**, and no programming is required for most changes. If you can edit a document, you can customize the skill. If you'd rather not touch a file at all, the first route below is for you.

### The no-edit route: just ask Claude

The skill's files are instructions written in plain English, and Claude is good at editing its own instructions. Describe the change you want in Claude Code, in your own words:

```
"In the natprd skill, add an accessibility question to the Requirements
 interview, and make the score check for it."

"Change the PRD template so Document Status sits in a table at the top."

"Add Brazil's LGPD to the skill's regulation list, with its official URL."
```

Claude finds the right file (or files), makes the edit, and keeps the scoring files in sync (see [the chain below](#keep-the-four-scoring-files-in-sync)). Claude Code picks up skill edits immediately, so the very next PRD follows your new rules.

> **Using the Claude app?** Uploaded skills are a snapshot; they don't update themselves. Make your changes to the `natprd` folder on your computer first (ask Claude for help, or use any text editor), then re-zip the folder and upload it again under **Skills** in the app's settings, replacing the old copy.

The steps below are the edit-it-yourself route. It's also the better setup for teams, because a fork gives everyone one shared, versioned copy.

### Step 1: Fork the repo (make your own copy)

A "fork" is your personal copy of this project on GitHub. You own it, you can change anything in it, and it stays linked to the original so you can pull updates later.

1. Go to [github.com/anatasof/NatPRD](https://github.com/anatasof/NatPRD) and click **Fork** (top-right). You now have your own `github.com/your-username/NatPRD`.
2. Install **your fork** instead of the original, using the same steps as [Installation](#installation), just with your URL:
   ```bash
   git clone https://github.com/your-username/NatPRD.git ~/.claude/skills/natprd
   ```
   No terminal? Download **your fork's** ZIP and drop it into `~/.claude/skills/` exactly as in the install steps.
3. Edit the files and save. Claude Code picks up skill edits right away, with no reinstall needed. (In the Claude app, re-zip and re-upload the folder, as in the note above.)

> **Just trying things out?** You can also edit the installed files in `~/.claude/skills/natprd/` directly, without forking. Forking is the better long-term choice if you want to keep your changes safe, share them with teammates, or pull in future updates.

### Step 2: Change what you need

You don't need any special software. Every file except `scripts/validate.py` is plain text, so any editor works (TextEdit on Mac, Notepad on Windows). If you forked, you can even edit on the GitHub website itself: open a file and click the pencil icon. For `validate.py` (the one Python file), describe the check you want and let Claude write it.

Here's everything you can tailor, along with **what you gain** by doing it:

| File | What it controls | A change you might make | What you gain |
|---|---|---|---|
| `templates/prd-template.md` | The shape of the final document: sections, headings, tables | Add a "Localization" section, add your company header, or drop a section you never use | Output matches your house style, with no reformatting after the fact |
| `templates/prd-summary-template.md` | The one-page stakeholder summary | Add the three numbers your execs always ask for | Leadership gets exactly what they scan for |
| `prompts/interview-questions.md` | The questions Claude asks for each section | Add probes your team always forgets (accessibility, fraud, data retention) | Those gaps get captured every time instead of slipping through |
| `prompts/section-rules.md` | The pass/fail rules per section | Tighten or relax a standard; require a field you care about | The skill enforces *your* definition of "done" |
| `prompts/validation-rules.md` | How the 0 to 100 score is weighted | Make Requirements worth more; add a rule for a section you added | The score reflects *your* priorities, not the defaults |
| `references/regulations.json` | The built-in regulation list | Add your country's rules, fix a source URL, update `last_reviewed` | Compliance suggestions fit your market and stay current |
| `references/api-docs.md` | Official documentation links for vendors | Add the payment / identity / cloud vendors you actually use | Real API limits get pulled from your real stack |
| `scripts/validate.py` | The automated structural checker | Add a check for a mistake your team keeps making | Recurring errors get caught automatically, before human review |
| `SKILL.md` | The skill's overall behavior and trigger phrases | Change the default save path, the tone, or how it's activated | The workflow fits how your team already talks and works |

### Customization recipes (by workflow)

Each of these works word for word as a request to Claude, or as a map of what to edit by hand (the files involved are named in each one).

- **"We're a fintech in Indonesia."** Ask Claude to *add OJK and Bank Indonesia entries to `regulations.json`, make Indonesia the default geography, and add interview probes about duplicate charges and settlement timing to `interview-questions.md`*. → The compliance and edge cases you care about are handled by default.
- **"We don't use Gherkin."** Ask Claude to *replace the Given/When/Then block in `prd-template.md` with your scenario format, and update the matching rules in `section-rules.md` and the check in `validate.py`*. → Requirements come out in your preferred format.
- **"Our execs only read summaries."** Ask Claude to *expand `prd-summary-template.md` with your KPIs and a one-line risk callout*. → One-pagers land without extra editing.
- **"We always forget accessibility."** Ask Claude to *add an accessibility question to the Requirements interview and a matching rule*. → Every PRD now covers it.
- **"We live in Jira / Linear."** Ask Claude to *add ticket-link fields to the template and a question that prompts for them*. → Traceability to your tracker is built in.

### Keep the four "scoring" files in sync

If you **add, rename, or remove a section**, update these four together so the score stays correct. They form a chain:

`templates/prd-template.md` (defines the section) → `prompts/section-rules.md` (defines pass/fail) → `prompts/validation-rules.md` (sets the points) → `scripts/validate.py` (does the automatic check)

This chain is exactly what Claude maintains for you on [the no-edit route](#the-no-edit-route-just-ask-claude), which is why that route is the safest one for structural changes.

After any change, run a quick self-test to make sure the checker still works:
```bash
python3 scripts/validate.py docs/prd.md
```
Not comfortable with a terminal? Ask Claude instead: *"re-score the PRD and check that the four scoring files still agree."*

### Pull in future updates (optional)

Because you forked, you can keep your copy fresh without losing your edits:
```bash
git remote add upstream https://github.com/anatasof/NatPRD.git   # one time only
git fetch upstream
git merge upstream/main      # bring in new features; resolve any overlap with your changes
```

No terminal? On your fork's GitHub page, click **Sync fork** to pull in the latest changes, then reinstall the same way you installed the first time: re-download the ZIP and replace your installed folder (Claude Code), or re-zip and re-upload it (Claude app).

And if you build something broadly useful, consider opening a **pull request** back to the original, so other teams benefit and your change rides along with future releases.

---

## Glossary

New to product-doc jargon? Here's what the terms mean.

| Term | Plain meaning |
|---|---|
| **PRD** | Product Requirements Document: the plan for what you're building and why |
| **User story** | A requirement written as "As a [type of user], I want to [do something], so that [benefit]" |
| **Gherkin / acceptance criteria** | A simple "Given / When / Then" recipe describing exactly what counts as the feature working |
| **NFR** | Non-Functional Requirement: qualities like speed, security, or uptime (not a feature itself) |
| **Leading vs. lagging metric** | Leading moves early and predicts success; lagging confirms it later |
| **Guardrail metric** | A number that must *not* get worse as a side effect of your change |
| **MoSCoW** | Priority labels: Must-have / Should-have / Could-have / Won't-have-this-time |
| **Baseline / target** | Where a metric is today vs. where you want it to be |
| **Hypothesis** | Your testable bet about what will happen and why |
| **Scope** | What's included; **out of scope** is what you're deliberately leaving out |
| **PII** | Personally Identifiable Information: data that can identify a person |
| **eKYC** | Electronic "Know Your Customer": verifying someone's identity online |
| **DRI** | Directly Responsible Individual: the one named person on the hook |
| **`[TBD]`** | "To be determined": a visible placeholder for something not yet known |

---

## FAQ

**Do I need to be technical to use this?**
No. You answer plain questions in a chat. The technical files run behind the scenes: on your computer in Claude Code, or on Claude's side in the Claude app.

**Does it work in the regular Claude app, not just Claude Code?**
Yes. The app installs skills directly now: upload the `natprd` folder as a ZIP (see [Installation](#installation), Option 2). Scoring and regulation lookup work fully there, because the helper scripts run on Claude's side. The one difference: the finished PRD arrives as a downloadable file rather than being saved into your project folder.

**Why does it ask so many questions before it starts writing?**
So it never has to guess. A few minutes of context up front is what lets it avoid invented metrics, fake design links, and made-up evidence later.

**Will it ever invent a number or a name to fill a gap?**
No. That's the core promise. Gaps become visible `[TBD]` markers that lower the score until you fill them.

**Can I change the template or rules to match my company's standards?**
Yes, that's encouraged. See [Customize it for your team](#customize-it-for-your-team) for the full list of what you can change (and the upside of each). The easiest way is to ask Claude to make the change for you; forking the repo is the sturdier setup for teams.

**Is the regulation list legal advice?**
No. It's a helpful, dated starting point that always asks you to confirm and points to official sources. Treat it as a prompt to check with legal/compliance, not a substitute for them.

**Is my data sent anywhere?**
Your conversation is processed by Claude over the internet, just like any other Claude chat; that's how Claude works at all. Beyond that, the skill fetches only the pages you explicitly name (or confirm), shows you every fetched fact before using it, and never runs background web searches. See [Does it use the internet?](#does-it-use-the-internet).

---

## License

BSD 3-Clause: free to use and redistribute, with attribution. Don't use the author's name to endorse derived works.
