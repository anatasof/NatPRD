# [Initiative Name]

> **One-line summary of what this initiative is and why it matters.**

---

## How to Use This Template

- Fill in every **Core Section**. Do not skip or leave placeholders.
- Add **Optional Sections** only when the trigger condition is met.
- All requirements are written as **user stories**. All acceptance criteria are written in **Gherkin syntax**.
- Rules under each section are non-negotiable standards — they exist to prevent rework and stakeholder confusion.
- Move Document Status to `In Review` only when all Core Sections are complete.
- This document is the single source of truth. If it is not written here, it does not exist.

---

# CORE SECTIONS

---

## 1. Initiative Name

`[Name]`

### Rules
- Maximum 8 words.
- Use a noun phrase, not a verb phrase.
- Must be unique and match Jira, Confluence, and roadmap exactly.
- If phased, suffix with phase number.

---

## 2. Document Status

| Field | Detail |
|---|---|
| **Status** | `Draft` |
| **Version** | v0.1 |
| **Last Updated** | YYYY-MM-DD |
| **Author** | [Name] |
| **Owner** | [Name] |
| **Reviewers** | [Engineering Lead], [Business Stakeholder] |
| **Approval Date** | — |

### Rules
- Fixed status vocabulary only: Draft → In Review → Approved → In Execution → Deprecated.
- Named individuals as reviewers, not teams.
- No development before Approved.

---

## 3. Background

### Problem Statement
[Describe the user or business pain. Who is affected? How often? How severely? Lead with the problem — never the solution.]

### Evidence & Data
[Cite data, research, support tickets, NPS feedback, or incidents. No unsubstantiated claims.]

### Context & History
[Prior work, failed attempts, or related initiatives. Link to prior PRDs or post-mortems.]

### Cost of Inaction
[What is lost if this is not pursued — revenue, users, compliance, competitive position?]

### Regulatory Context
*(Include this subsection when compliance signals were confirmed at intake. Remove this subsection if no compliance signals apply — note its removal explicitly: "No regulatory requirements identified.")*

| Regulation | Jurisdiction | Key Requirements for This Initiative | Status |
|---|---|---|---|
| [Regulation name, e.g., GDPR Art. 6] | [EU/EEA] | [Specific obligation — e.g., lawful basis for data processing required] | `Confirmed` / `[TBD — compliance review required]` |
| [Regulation name] | [Region] | [Specific obligation] | `Confirmed` / `[TBD — compliance review required]` |

**Compliance Review Owner:** [Name — individual, not team]
**Review Deadline:** [Date or `[TBD]`]

### Rules
- Lead with pain, not solution.
- Every claim needs a cited source.
- 3–5 paragraphs. Link to longer docs rather than embedding.
- Cost of inaction is mandatory.
- Regulatory Context is mandatory when any compliance signal was confirmed at intake. Write `[TBD — compliance review required: [regulation name]]` if specifics are unknown — do not omit the subsection entirely.

---

## 4. Objective

### Primary Objective
> [One outcome statement. No feature descriptions. No "improve" without a measurable qualifier.]

### Key Results

| # | Key Result | Baseline | Target | Timeline |
|---|---|---|---|---|
| KR1 | [Measurable outcome] | [Value] | [Value] | [Date] |
| KR2 | [Measurable outcome] | [Value] | [Value] | [Date] |
| KR3 | [Measurable outcome] | [Value] | [Value] | [Date] |

### Company OKR Alignment
[Name the parent company OKR. If none exists, escalate before proceeding.]

### Rules
- One primary objective. Multiple = scope that needs splitting.
- Every KR needs a numeric baseline and target.
- Traceable to company OKR.

---

## 5. Scope & Boundaries

### In Scope
- [Item]
- [Item]

### Out of Scope

| Item | Reason | Future Plan |
|---|---|---|
| [Item] | [Reason] | [Plan or none] |

### Platform & Segment Coverage

| Dimension | Coverage |
|---|---|
| **Platform** | [iOS / Android / Web / API / All] |
| **User Segment** | [Segment] |
| **Geography** | [Geography] |
| **Phase** | [Phase] |

### Rules
- Both In and Out of Scope must be explicitly listed.
- Every Out item needs a reason.
- Platform and segment are mandatory.

---

## 6. Hypothesis

> *"We believe that **[X]** for **[segment]** will result in **[Y]**, because **[Z]**."*

[Write hypothesis here.]

### Confidence Level
`High` / `Medium` / `Low`

**Reasoning:** [Why this level?]

### Falsification Condition
[What result would prove this hypothesis wrong?]

### Post-Launch Learning Plan
[Who owns the retrospective? When?]

### Rules
- Template is mandatory. All four components required.
- Must be falsifiable.
- Confidence level needs written rationale.

---

## 7. Success Metrics

### Primary Metrics

| Metric | Type | Baseline | Target | Measurement Method | Timeline | Owner |
|---|---|---|---|---|---|---|
| [Metric] | Leading | [Value] | [Value] | [Method] | [Date] | [Name] |
| [Metric] | Lagging | [Value] | [Value] | [Method] | [Date] | [Name] |

### Guardrail Metrics

| Metric | Baseline | Alert Threshold | Measurement Method | Owner |
|---|---|---|---|---|
| [Metric] | [Value] | [Threshold] | [Method] | [Name] |

### Rules
- Min one leading + one lagging metric.
- Guardrail metrics are mandatory.
- All fields required per row.
- Owner = named individual, not team.

---

## 8. Requirements

> User stories: *"As a [specific role], I want to [action], so that [benefit]."*
> Acceptance criteria: Gherkin syntax, minimum 2 scenarios per story.

---

### Functional Requirements

#### US-001 — [Title]

**Priority:** `Must-have`

**User Story:**
> As a **[specific role]**, I want to **[action]**, so that **[benefit]**.

**Acceptance Criteria:**
```gherkin
Scenario: [Happy path]
  Given [precondition]
  When [action]
  Then [outcome]

Scenario: [Edge case or failure]
  Given [precondition]
  When [action]
  Then [outcome]
```

**Dependencies:** [None / US-XXX / External system]
**Notes:** [Constraints, open questions]

---

#### US-002 — [Title]

**Priority:** `Must-have`

**User Story:**
> As a **[specific role]**, I want to **[action]**, so that **[benefit]**.

**Acceptance Criteria:**
```gherkin
Scenario: [Happy path]
  Given [precondition]
  When [action]
  Then [outcome]

Scenario: [Edge case or failure]
  Given [precondition]
  When [action]
  Then [outcome]
```

**Dependencies:** [None / US-XXX / External system]
**Notes:** [Constraints, open questions]

---

### Non-Functional Requirements

| ID | Category | Requirement | Priority | Verification Method |
|---|---|---|---|---|
| NFR-001 | Performance | [Requirement] | `Must-have` | [Method] |
| NFR-002 | Security | [Requirement] | `Must-have` | [Method] |
| NFR-003 | Compliance | [Requirement] | `Must-have` | [Method] |

### Rules
- User stories only. Specific roles. Min 2 Gherkin scenarios each.
- MoSCoW priority on every story.
- NFRs need verification methods.

---

## 9. Solution

### Proposed Approach
[Product-level description. Reference designs — do not describe UI in prose.]

### Design Artifacts

| Artifact | Link | Status |
|---|---|---|
| User Flow | [Link] | `Draft` / `Final` |
| Wireframes | [Link] | `Draft` / `Final` |
| Mockups | [Link] | `Draft` / `Final` |

### User Story Coverage Map

| User Story | Solution Component | Design Reference |
|---|---|---|
| US-001 | [Component] | [Screen / link] |
| US-002 | [Component] | [Screen / link] |

### Considered Alternatives

| Option | Description | Why Rejected |
|---|---|---|
| Option A | [Description] | [Reason] |
| Option B | [Description] | [Reason] |

### Technical Constraints & Decisions
[Architectural decisions or constraints that shaped the solution.]

### Rules
- Design links required.
- All user stories must appear in coverage map.
- Alternatives section is mandatory — always include at least one.

---

## 10. Metric Monitoring

| Field | Detail |
|---|---|
| **Dashboard / Tool** | [Tool + link] |
| **DRI** | [Named individual] |
| **Monitoring Cadence** | Daily launch week → Weekly month 1 → Bi-weekly after |
| **Primary Metric Alert Threshold** | [Threshold] |
| **Guardrail Metric Alert Threshold** | [Threshold] |
| **Rollback Trigger** | [Specific observable condition] |
| **Escalation Path** | [Who, in what order, through what channel] |

### Post-Launch Review Schedule

| Review | Date | Participants | Owner |
|---|---|---|---|
| 2-Week Check-in | YYYY-MM-DD | [PM, Eng Lead, Data] | [Name] |
| 30-Day Review | YYYY-MM-DD | [PM, Eng Lead, Business] | [Name] |
| Quarterly Retrospective | YYYY-MM-DD | [Stakeholders] | [Name] |

### Rules
- Named DRI, not a team.
- Alert thresholds defined pre-launch.
- Rollback trigger must be observable, not vague.
- Review dates set at Approved and put in calendar.

---

## 11. Event & Data Tracking

> Naming: `noun_verb`. Every event maps to a metric in §7. Data team sign-off required before dev.

| Event Name | Trigger Condition | Properties | Side | Destination | Maps to Metric | Compliance Flag |
|---|---|---|---|---|---|---|
| `[noun_verb]` | [Trigger] | `{ key: value }` | Client / Server | [Tool] | [Metric] | Yes / No |

**Data Team Sign-off:**
- [ ] Pending
- [ ] Approved — [Name], [Date]

### Rules
- noun_verb naming, no exceptions.
- Every event traces to §7 metric.
- Trigger conditions are specific, not generic.
- Client vs. server-side distinguished.
- Sign-off required before dev starts.

---

## 12. FAQ

| # | Question | Answer | Date | Answered By | Status |
|---|---|---|---|---|---|
| 1 | [Question] | [Answer] | YYYY-MM-DD | [Name] | `Resolved` |
| 2 | [Open question] | — | — | [Owner] | `Open` |

### Rules
- Add questions immediately when raised.
- Open items need an owner.
- Never delete resolved questions.
- At Approved: zero Open items without a resolution plan.

---

---

# OPTIONAL SECTIONS

> Include only when trigger condition is met. Delete this instruction block in the final document.

---

## 13. Risks & Mitigations
*(Include when: payments, compliance, regulated data, or multi-team dependencies)*

### Regulatory Risks
*(Mandatory when compliance signals were confirmed at intake. One row per confirmed regulation minimum.)*

| ID | Regulation | Risk Description | Likelihood | Impact | Mitigation | Contingency | Owner | Phase |
|---|---|---|---|---|---|---|---|---|
| RR-001 | [Regulation name, e.g., GDPR] | [Specific risk — e.g., processing personal data without valid lawful basis] | `H/M/L` | `H/M/L` | [Prevention — e.g., legal review, consent flow implementation] | [Response if it materializes — e.g., cease processing, notify DPA] | [Name] | Pre-launch |

**Legal/Compliance Sign-off on Regulatory Risks:**
- [ ] Pending — [Name, Title to review]
- [ ] Approved — [Name, Title], [Date]

### Operational & Technical Risks

| ID | Risk | Likelihood | Impact | Mitigation | Contingency | Owner | Phase |
|---|---|---|---|---|---|---|---|
| R-001 | [Risk] | `H/M/L` | `H/M/L` | [Prevention] | [Response if it happens] | [Name] | Pre-launch |

### Rules
- Both mitigation and contingency required per risk row.
- Named individual owner per row, not team.
- Distinguish pre-launch vs. post-launch risks.
- Every confirmed regulation from §3 Regulatory Context must have at least one row in Regulatory Risks.
- Each regulatory risk row must name the specific regulation — not "regulatory risk" generically.
- Legal/compliance sign-off checkbox is required in this section when regulatory risks are present.

---

## 14. Dependencies
*(Include when: blocked by or blocking another team, or relies on third-party system)*

### Upstream Dependencies

| ID | Dependency | Team / Vendor | What Is Needed | Expected Date | Confirmed | Risk if Delayed | Escalation |
|---|---|---|---|---|---|---|---|
| DEP-001 | [Name] | [Team] | [Deliverable] | YYYY-MM-DD | Yes / No | [Impact] | [Path] |

### Downstream Dependencies

| ID | Dependent Initiative | Team | What They Need | Expected Date |
|---|---|---|---|---|
| DEP-D01 | [Name] | [Team] | [What they need] | YYYY-MM-DD |

### Rules
- Confirmed column must be Yes before Approved.
- Hard unconfirmed dependencies block Approved status.
- Keep this section live during execution.

---

## 15. Launch Plan
*(Include when: coordinated rollout, staged release, or compliance gate required)*

### Rollout Strategy
`[Full Release / Feature Flag / Percentage Rollout / Regional Rollout / Invite-Only]`

[Rationale for chosen strategy.]

### Go / No-Go Criteria

| Stage | Go Condition | No-Go Condition | Decision Maker |
|---|---|---|---|
| Internal | [Condition] | [Condition] | [Name] |
| Limited Rollout | [Condition] | [Condition] | [Name] |
| Full Release | [Condition] | [Condition] | [Name] |

### Communications Plan

| Audience | Channel | Message Summary | Timing | Owner |
|---|---|---|---|---|
| Internal teams | [Channel] | [Summary] | [Timing] | [Name] |
| End users | [Channel] | [Summary] | [Timing] | [Name] |
| Customer support | [Channel] | [What to handle] | [X days before] | [Name] |

### Rollback Plan

| Field | Detail |
|---|---|
| **Rollback Trigger** | [Specific observable condition] |
| **Decision Maker** | [Name] |
| **Execution Time** | [Duration] |
| **Rollback Steps** | [Steps or link to runbook] |

**Launch DRI:** [Name — not the PM]

**Compliance Sign-off:**
- [ ] Pending
- [ ] Approved — [Name, Title], [Date]

### Rules
- Rollback plan required.
- Go/No-Go criteria defined before launch day.
- Customer support in comms plan always.
- Launch DRI ≠ PM.

---

## 16. Stakeholder Map
*(Include when: >3 teams involved, executive visibility needed, or external parties present)*

### RACI Matrix

| Name | Role / Title | Team / Org | RACI | Comms Cadence | Preferred Channel |
|---|---|---|---|---|---|
| [Name] | [Title] | [Team] | `A` | Weekly | [Channel] |
| [Name] | [Title] | [Team] | `R` | Daily during execution | [Channel] |
| [Name] | [Title] | [Team] | `C` | At milestones | [Channel] |
| [Name] | [Title] | [Team] | `I` | At milestones | [Channel] |

> `R` Responsible · `A` Accountable · `C` Consulted · `I` Informed
> Exactly one Accountable. Named individuals only.

### Rules
- Exactly one A.
- Named individuals, not roles.
- Comms cadence + channel for every stakeholder.
- External parties clearly labeled.

---

*— PRD Template — PRD Maker skill —*
