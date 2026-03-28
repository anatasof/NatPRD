# Section Rules — PRD

These rules are used during validation (Mode 2) and inline checking during generation (Mode 1).
A violation blocks progression to the next section. Warnings are noted but do not block.

---

## §1 — Initiative Name

**VIOLATIONS (block):**
- Name exceeds 8 words
- Name is a verb phrase (e.g., "Add Dark Mode") instead of a noun phrase

**WARNINGS (flag but don't block):**
- Name contains an internal codename or acronym that external stakeholders may not recognise
- Name does not match what's in Jira, Confluence, or roadmap (ask user to confirm)

---

## §2 — Document Status

**VIOLATIONS (block):**
- Status is not one of: Draft / In Review / Approved / In Execution / Deprecated
- Status is `In Review` but no named reviewers are listed (team names are not sufficient — individual names required)
- Status is `Approved` or beyond but no named approver(s) are listed (individual names required — not team names)
- Status is `Approved` or beyond but no approval date is recorded

**WARNINGS:**
- No version number present
- Author and owner are the same person with no explanation

---

## §3 — Background

**VIOLATIONS (block):**
- Section opens with a proposed solution rather than a problem or pain
- No evidence or data source cited for any claim
- Cost of inaction is absent
- Compliance signals were confirmed in §0.3 but no Regulatory Context subsection is present (even a TBD entry is required)

**WARNINGS:**
- Section is shorter than 3 paragraphs (may be underdeveloped)
- Section is longer than 5 paragraphs without links to supporting documents
- Context & History is absent for an initiative that appears to be a continuation of prior work

---

## §4 — Objective

**VIOLATIONS (block):**
- Primary objective describes a feature or deliverable instead of a business or user outcome
- A key result has no numeric baseline or no numeric target
- No company OKR alignment is named
- More than one primary objective is listed

**WARNINGS:**
- The word "improve" appears in a KR without a measurable qualifier
- Timeline is absent from one or more KRs

---

## §5 — Scope & Boundaries

**VIOLATIONS (block):**
- Out of Scope section is absent (even if intentionally empty, it must be stated as empty and explained)
- An Out of Scope item has no reason attached
- Platform or user segment coverage is not stated
- Compliance signals were confirmed in §0.3 but no regulatory-driven scope items are present or explicitly noted as not applicable

**WARNINGS:**
- In Scope list contains only one item (may be underdeveloped or scope is too narrow)
- No geography is specified for initiatives with a regional component

---

## §6 — Hypothesis

**VIOLATIONS (block):**
- Hypothesis does not follow the template: "We believe [X] for [segment] will result in [Y] because [Z]"
- One or more of the four template components (X, segment, Y, Z) is missing
- No falsification condition is stated
- Hypothesis is not falsifiable (e.g., "We believe users will appreciate this")

**WARNINGS:**
- Confidence level is present but has no written rationale
- Post-launch learning plan / retrospective owner is not named

---

## §7 — Success Metrics

**VIOLATIONS (block):**
- No leading indicator metric is present
- No lagging indicator metric is present
- Guardrail metrics section is absent
- Any metric row is missing one of: baseline, target, measurement method, or owner

**WARNINGS:**
- A metric uses a vanity measure (page views, installs, registrations) without a paired quality metric
- Metric owner is listed as a team name instead of an individual

---

## §8 — Requirements

**VIOLATIONS (block):**
- Any requirement is not written as a user story
- User role is "user" without further specification
- A user story has fewer than 2 Gherkin scenarios
- A Gherkin scenario has an ambiguous or non-deterministic Then clause
- A user story has no MoSCoW priority assigned
- A non-functional requirement has no verification method

**WARNINGS:**
- A user story appears too large to be delivered in a single sprint (suggest splitting)
- A dependency between stories is described in prose rather than listed in the Dependencies field

---

## §9 — Solution

**VIOLATIONS (block):**
- No design artifact links are present (prose description without a link is not sufficient)
- No user story coverage map is present
- No considered alternatives section is present
- An alternative is listed as rejected but no reason is given

**WARNINGS:**
- A design artifact link is present but marked as Draft (flag for reviewer attention)
- One or more user stories from §8 are not covered in the coverage map

---

## §10 — Metric Monitoring

**VIOLATIONS (block):**
- No monitoring tool or dashboard is named
- DRI is listed as a team name instead of an individual
- No alert threshold is defined for primary metrics
- No rollback trigger is defined
- No post-launch review dates are set

**WARNINGS:**
- Escalation path is absent
- Guardrail metric alert threshold is missing

---

## §11 — Event & Data Tracking

**VIOLATIONS (block):**
- Any event name does not follow noun_verb convention
- An event cannot be traced to a metric in §7
- A trigger condition is ambiguous or generic (e.g., "when user does something")
- Data team sign-off checkbox is not present

**WARNINGS:**
- Client-side vs. server-side distinction is not made for any event
- Compliance flag column is absent (required for eKYC / AML / fintech initiatives)
- Data team sign-off checkbox is present but marked Pending (flag for reviewer)

---

## §12 — FAQ

**VIOLATIONS (block):**
- Section is completely absent

**WARNINGS:**
- An Open item has no assigned owner
- FAQ has zero entries (acceptable only for brand new, unreviewed drafts)

---

## §13 — Risks & Mitigations (Optional)

**VIOLATIONS (block):**
- A risk has a mitigation but no contingency
- A risk has no named owner (individual, not team)
- Initiative touches eKYC, AML, or financial transactions but no regulatory risk row is present
- A regulatory risk row is present but does not name the specific regulation it relates to (e.g., writing "regulatory risk" without citing GDPR, PCI-DSS, OJK POJK 12/2018, etc.)
- A regulatory risk row has a TBD owner with no deadline for owner assignment

**WARNINGS:**
- Pre-launch and post-launch risks are not distinguished
- Legal or compliance team has not been flagged to review this section before In Review
- Confirmed regulations from §0.3b are not all represented — each confirmed regulation should have at least one corresponding risk row (even if TBD)

---

## §14 — Dependencies (Optional)

**VIOLATIONS (block):**
- Upstream dependencies are listed but "Confirmed" column is blank or No
- A hard dependency has no mitigation and no corresponding risk in §13
- PRD is marked Approved but unconfirmed hard dependencies remain

**WARNINGS:**
- Downstream dependencies are absent (may be intentional — ask user to confirm)
- Escalation path is missing for any upstream dependency

---

## §15 — Launch Plan (Optional)

**VIOLATIONS (block):**
- No rollback trigger is defined
- No rollback decision maker is named
- No communications plan is present
- Launch DRI is named as the PM (must be a separate role)
- Initiative is in a regulated industry but compliance sign-off is absent

**WARNINGS:**
- Customer support is absent from the communications plan
- Go / No-Go criteria are absent for one or more rollout stages

---

## §16 — Stakeholder Map (Optional)

**VIOLATIONS (block):**
- More than one person is listed as Accountable (A)
- No one is listed as Accountable
- A stakeholder is listed by role only, with no individual name

**WARNINGS:**
- Communication cadence is absent for one or more stakeholders
- External stakeholders are not distinguished from internal ones
- A Consulted (C) stakeholder appears to be receiving only Informed (I) treatment based on context
