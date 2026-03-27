# Interview Questions by Section

These are the questions Claude asks the user during Mode 1 (Generate).
Ask them conversationally — one at a time, not as a dump.
Validate each answer before moving to the next section.

---

## §0 — Intake (Run Before Everything Else)

This section runs BEFORE the section-by-section interview. Complete all §0 questions first.
Do not begin §1 until §0 is finished.
Use the answers to configure which optional sections to include and how to tailor later questions.

---

### §0.1 — Initiative Identity

1. What is the working name for this initiative? (This will be refined into a proper noun phrase in §1 — any name is fine for now.)
2. Give me one sentence: what is this initiative trying to do, and for whom?

---

### §0.2 — Product and Platform Context

3. What type of initiative is this?
   (new feature / redesign or UX improvement / internal tool / API or platform / marketplace / B2B SaaS / backend-only / other)
   - _Why this matters:_ Consumer apps require UX-heavy requirement stories. Internal tools need admin flows and permission levels. APIs need non-functional requirements up front.

4. Which platform(s) does this touch?
   (iOS / Android / Web / backend only / cross-platform / other)
   - _If cross-platform:_ "Are there platform-specific differences to capture, or is it the same experience everywhere?"

5. Who is the primary user?
   (consumer end-user / internal staff or ops / B2B client / developer / other)
   - _If "internal staff":_ Flag this — admin flows, permission levels, and audit trails will be probed in §8.

---

### §0.3 — Domain and Compliance Context

6. What product domain or area does this sit in?
   (e.g., payments, onboarding, notifications, search, settings, content, growth, infrastructure, customer support)

7. Does this initiative touch any of the following? (confirm each)
   - Financial transactions or payment flows
   - Identity verification (eKYC, KYB, biometrics)
   - Personal data or PII beyond basic profile fields
   - Regulatory or compliance requirements (OJK, GDPR, CCPA, PCI-DSS, etc.)
   - Credit, lending, or insurance products
   - _If any are confirmed:_ §13 Risks & Mitigations is automatically included. The §11 compliance flag column is required.

---

### §0.4 — Team and Execution Context

8. How many teams are involved in delivering this?
   (just ours / 2 teams / 3 or more / cross-org)
   - _If 3+ teams:_ Auto-flag §16 Stakeholder Map.
   - _If 2+ teams:_ Auto-flag §14 Dependencies.

9. Is this initiative currently blocked by, or blocking, another team's work?
   - _If yes:_ Auto-flag §14 Dependencies.

10. Does this depend on any third-party APIs, vendors, or external services?
    (e.g., payment processor, identity provider, logistics partner, cloud vendor, data provider)
    - _If yes:_ Auto-flag §14 Dependencies.

11. Are there external parties involved who need to be informed or who have sign-off authority?
    (e.g., regulators, compliance body, external partners, vendors with contractual SLAs)
    - _If yes:_ Auto-flag §16 Stakeholder Map.

12. Does this require executive or leadership sign-off before launch?
    - _If yes:_ Auto-flag §16 Stakeholder Map.

---

### §0.5 — Launch and Rollout Context

13. How is this going live?
    (full release to all users / feature flag / staged rollout by cohort / A/B test / canary / phased by region or platform)
    - _If staged, phased, A/B, or canary:_ Auto-flag §15 Launch Plan.

14. Does this require any of the following before going live?
    - Marketing or comms coordination (announcement, email, in-app message)
    - Legal or compliance sign-off
    - Customer support enablement (training, runbook)
    - Partner or vendor notification
    - _If any are confirmed:_ Auto-flag §15 Launch Plan.

---

### §0.6 — Discovery Maturity

15. Where is the discovery for this initiative right now?
    (just an idea / validated with users / data-backed / already designed / ready to build)
    - _If "just an idea":_ Warn: "Background and Hypothesis will need significant development — I'll probe deeper there. Expect to use [TBD] placeholders for evidence and metrics we don't have yet."
    - _If "already designed" or "ready to build":_ "Do you have design links or existing documentation? Share them now and I'll attach them to §9 rather than marking [No design link]."

16. Are there any existing artifacts to pull from?
    (research report, competitive analysis, OKR doc, incident report, Jira epic, Figma file, previous PRD)
    - _If yes:_ "Paste the key findings or link here. I'll use them as real evidence in §3 and §6 instead of placeholder content."
    - _If no:_ "Understood — we'll build from what you know. I'll flag anything that needs research as [TBD — needs data]."

---

### §0.7 — Optional Section Confirmation

After completing §0.3–§0.5, apply the trigger logic below and present a summary:

> "Based on what you've told me, here's what I'll include beyond the 12 core sections:
> - §13 Risks & Mitigations: [Yes — reason / No]
> - §14 Dependencies: [Yes — reason / No]
> - §15 Launch Plan: [Yes — reason / No]
> - §16 Stakeholder Map: [Yes — reason / No]
>
> Does this look right? You can add or remove any of these before we start."

Wait for confirmation. Do not proceed to §1 until the user confirms or adjusts the list.

---

### Optional Section Trigger Logic

| Signal from §0 | Triggered section |
|---|---|
| Domain: payments, eKYC, AML, lending, insurance | §13 Risks & Mitigations |
| PII, biometric, or financial data involved | §13 Risks & Mitigations |
| Regulatory requirement mentioned | §13 Risks & Mitigations |
| Any team blocked or blocking | §14 Dependencies |
| Third-party API, vendor, or external service dependency | §14 Dependencies |
| 2+ teams involved | §14 Dependencies |
| Staged, phased, A/B, or canary rollout | §15 Launch Plan |
| Comms, legal, CS, or partner sign-off required before launch | §15 Launch Plan |
| 3+ teams involved | §16 Stakeholder Map |
| Executive or leadership sign-off required | §16 Stakeholder Map |
| External regulators, partners, or vendors with sign-off authority | §16 Stakeholder Map |

Any single signal is sufficient to trigger the section.

---

## §1 — Initiative Name

1. What is the name of this initiative? (max 8 words, noun phrase)
   - _Probe if too long:_ "Can we trim that to 8 words or fewer?"
   - _Probe if verb phrase:_ "Let's rephrase as a noun phrase — what's the thing being built, not the action?"
2. Does this name appear anywhere else — Jira, Confluence, roadmap? If yes, confirm it matches exactly.

---

## §2 — Document Status

1. What is the current status? (Draft / In Review / Approved / In Execution / Deprecated)
2. Who is the author? Who is the current owner?
3. Who needs to review this? Name at least one engineering lead and one business stakeholder.
   - _If only team names given:_ "Can you name the specific individuals, not just teams?"

---

## §3 — Background

1. What problem are we solving? Who is affected, and how often or severely?
   - _Probe if too solution-y:_ "Let's hold the solution for later — what's the pain the user or business is experiencing?"

2. What evidence do you have that this problem exists?
   - _Acceptable sources:_ quantitative data with a number, user research with a named finding, support ticket volume, NPS verbatim, incident data, A/B test result, competitive benchmark.
   - _For each piece of evidence provided:_ "What is the source — who measured it, when, and where is it documented?"
   - _If the user says "we think" or "we believe" without data:_ "I'll capture that as an unvalidated team belief for now — written as `[Team belief — unvalidated: ___]`. Can you attach even a rough number or a single supporting reference? If not, I'll flag it as `[TBD — needs data]` so the reviewer knows it needs sourcing."
   - _If no evidence at all:_ "I'll mark this section as needing evidence. The Background section requires at least one cited source to pass validation. We'll continue and you can come back to this."
   - RULE: Do not write any claim as established fact unless the user provided either a number or a named source.

3. Has this been attempted before? Is there any prior work or history we should acknowledge?
   - _If prior attempt exists:_ "What happened last time, and what's different now?"

4. What happens if we do nothing? What is the cost of inaction — revenue, users, compliance, competitive position?

5. Is there prior art on this problem? Have other companies solved it, or has your company tried something similar?

---

## §4 — Objective

1. What does success look like in one sentence? This should be an outcome, not a feature.
   - _Probe if it's a feature:_ "That's what we're building — but what business result does it produce?"
2. What are 2–3 measurable key results? For each one I need: the metric, the current baseline value, the target value, and the timeline.
   - _If no baseline:_ "Do you have a current number to start from? Even an estimate? If not, I'll write `[TBD — baseline needed]` and flag it as pre-approval required."
3. Which company-level OKR does this initiative support?

---

## §5 — Scope & Boundaries

1. What is explicitly in scope for this initiative?
2. What is explicitly out of scope? (List items that someone might reasonably expect to be included but aren't)
   - _For each out-of-scope item:_ "What's the reason — deferred, owned by another team, future phase?"
3. Which platforms does this cover? (iOS / Android / Web / API / All)
4. Which user segments does this apply to?
5. Which geographies or regions are included?
6. Is this phased? If so, what's in Phase 1 vs. later?

---

## §6 — Hypothesis

1. Let's build the hypothesis together. Complete this sentence:
   "We believe that [doing X] for [user/segment] will result in [outcome Y], because [evidence/rationale Z]."
   - _Guide them through each component if they're stuck._
   - _If the user cannot fill [Z] with real evidence:_ "I'll write the rationale as `[TBD — needs evidential basis]`. The hypothesis must be grounded in something — we can revisit this once Background evidence is confirmed."
2. How confident are you in this hypothesis? (High / Medium / Low) — and why?
3. What would tell you the hypothesis is wrong? What result or signal would prove it doesn't hold?
4. Who will own the post-launch retrospective to revisit this hypothesis?

---

## §7 — Success Metrics

**Primary Metrics:**
1. What is the main metric this initiative is optimizing for?
2. Is there a leading indicator — a metric that will move first and predict future success?
3. Is there a lagging indicator — a metric that confirms success after the fact?

4. For each metric, I need five things:
   a. **Baseline:** What is the current value of this metric today, before this initiative?
      - _If the user says "I don't know" or "we don't have it":_ "I'll write `[TBD — baseline needed]` for now. This must be filled before the PRD can be approved. Who will get this number, and by when?"
      - RULE: Do NOT estimate or approximate a baseline. If the user did not provide a number, write `[TBD]`. No exceptions.
   b. **Target:** What is the goal value, and by what date?
      - _If the user gives a directional target like "increase it":_ "I need a specific number or percentage. Even a rough commitment — what would make this initiative worth it?"
      - _If no target:_ Write `[TBD — target needed]`.
   c. **Measurement method:** How will this metric be measured? (specific tool, query, or dashboard name — not just "we'll track it")
   d. **Owner:** Who owns tracking and reporting on this metric? (individual name, not a team)
   e. **Type:** Is this a leading or lagging indicator?

**Guardrail Metrics:**
5. What metrics must not regress as a result of this initiative?
6. For each guardrail: what's the baseline, and at what threshold should the team raise an alarm?

7. Let's do a quick sanity check before moving on:
   - Do we have at least one metric that will move within the first 2 weeks of launch (leading indicator)?
   - Do we have at least one metric that confirms the business outcome over 30–90 days (lagging indicator)?
   - Do we have at least one guardrail metric protecting something we must not break?
   - _If any of these are missing:_ Explicitly prompt: "We're missing a [leading / lagging / guardrail] metric. What could we use?"

---

## §8 — Requirements

For each user story, ask the following sequence. Repeat until the user signals no more stories.

1. Who is the user in this story? (specific role — not just "user")
2. What do they want to do?
3. Why — what benefit does it give them?
   - _Assemble:_ "As a [role], I want to [action], so that [benefit]."
4. What's the happy path — the standard successful scenario?
   - _Capture as Gherkin:_ Given / When / Then
5. What's an edge case or failure scenario — what happens when something goes wrong?
   - _Capture as Gherkin:_ Given / When / Then
6. What's the priority? (Must-have / Should-have / Could-have / Won't-have this phase)
7. Does this story depend on any other stories or external systems?
8. Any notes, constraints, or open questions specific to this story?

After each story, before asking for more, explicitly surface these gap checks:
> "Before we move on — have we covered:
> 1. Error or failure states for this flow?
> 2. Admin or internal staff versions of this flow?
> 3. Role-based or permission-level variations?
> 4. Abandonment or partial completion scenarios?"

Then ask: "Any more stories? Before you say no — have we also covered any onboarding or first-run flows?"

Continue until the user explicitly says "no more stories" after the gap-check prompt.

**Non-Functional Requirements:**
9. Are there performance requirements? (e.g., response time, throughput)
10. Are there security or compliance requirements? (e.g., encryption, OJK, regulatory)
11. Are there accessibility requirements?
12. Are there availability or uptime requirements?
    - _For each:_ "How will this be verified or tested?"
13. Are there rate limits, API quotas, or concurrency constraints that could affect this feature?
14. Are there data retention, deletion, or portability requirements?
    - _If the initiative handles PII (confirmed in §0.3):_ Ask this question unconditionally and mark the answer as compliance-required.

---

## §9 — Solution

1. At a high level, how does the proposed solution work from the user's perspective?

2. Do you have design artifacts — flows, wireframes, mockups, or prototypes? Please share the links.
   - _If links are provided:_ Record them exactly as given. Do not paraphrase or summarize. Note the status the user reports (Draft / In Progress / Final).
   - _If no links yet:_ "I'll write `[No design link — status: Draft]` for now. This section requires a link to pass validation. When will designs be available, and who is the designer?"
   - RULE: Do not describe the design or UI in prose if no link exists. Use: `[Design pending — link to be added]`. Never generate a design description that implies decisions have been made when no link supports it.

3. For each user story we captured, which part of the solution addresses it?

4. What alternatives were considered and why were they rejected?
   - _Probe if none:_ "There are always tradeoffs — what did you consider and decide against?"

5. Are there any technical constraints or architectural decisions that shaped this solution?
   - _If the user says "I don't know" or defers to engineering:_ "Are there any known database limitations, third-party API rate limits, mobile OS restrictions, or platform architecture decisions already established that we should capture?"

6. Does this solution create any new backend services, data models, or API contracts that don't currently exist?
   - _If yes:_ "These are likely dependencies for other teams. I'll flag them for §14 (Dependencies)." If §14 is not already triggered, recommend adding it.

---

## §10 — Metric Monitoring

1. Where will the metrics be monitored post-launch? (dashboard name, tool, link — be specific)
   - RULE: Do not invent a dashboard name or tool. If the user hasn't specified, write `[TBD — monitoring tool not confirmed]`.
2. Who is the DRI for monitoring? (name a person, not a team)
3. What's the monitoring cadence? (daily launch week, weekly after, etc.)
4. At what threshold for each primary metric should the team escalate?
5. At what threshold for each guardrail metric should the team escalate?
6. What specific condition would trigger a rollback? Who decides, and how fast can it be executed?
7. Who gets notified first if something goes wrong, and through what channel?
8. Let's set post-launch review dates now — when is the 2-week check-in, 30-day review, and quarterly retrospective?
   - RULE: Do not invent dates. If the user cannot provide them, write `[TBD — dates to be confirmed]`.

---

## §11 — Event & Data Tracking

Before listing events, run this cross-check against §7:

> "Let's start by mapping from metrics to events rather than the other way around. For each metric in §7, which user action or system action produces the data to measure it? If a metric has no corresponding event, we have a gap we need to fill."

Go through each §7 metric and confirm its event(s) before writing any tracking rows.
- RULE: Do not generate event names that the user has not confirmed. If the user cannot name an event, write `[TBD — event name to be confirmed by data team]`.

For each confirmed event, ask:

1. What is the event name? (follow noun_verb format — e.g., `payment_initiated`)
2. When exactly does this event fire? (be specific — which user action, which screen, which API call)
3. What properties or data should be attached to this event?
4. Is this a client-side or server-side event?
5. Where does this event get sent? (Mixpanel, Segment, GA, internal — confirm with user, do not assume)
6. Which metric from §7 does this event support?
   - _If the user cannot name a metric:_ "Every event must map to a metric. If this event doesn't map to anything in §7, it either needs to be removed or we need to add a metric to §7. Which is it?"
   - RULE: An event with no §7 metric mapping must be marked `[UNLINKED — not valid for tracking plan]`. Do not write it as a valid event.
7. Does this event involve PII, financial data, or biometric data? (compliance flag)

After all events, run this closing cross-check:
> "Does every metric in §7 have at least one event feeding it? Let's verify coverage now."

Then ask: "Has the data or analytics team reviewed this tracking plan?"
- _If no or not yet:_ Mark the sign-off checkbox as: `[ ] Data team sign-off — PENDING`.
- RULE: Never pre-populate the sign-off checkbox as complete unless the user explicitly confirms it.

---

## §12 — FAQ

Before asking open-endedly, raise contextually relevant probes based on §0 intake answers:

- _If domain is payments or financial:_ "Has anyone asked what happens if a payment fails mid-flow, or if a retry causes a duplicate charge?"
- _If consumer-facing product:_ "Has anyone asked how this experience looks on older OS versions or lower-end devices?"
- _If internal/ops tool:_ "Has anyone asked how the transition period works while both old and new flows exist in parallel?"
- _If staged rollout (§15 triggered):_ "Has anyone asked what the criteria are for expanding from Phase 1 to Phase 2?"
- _If compliance or regulatory involved:_ "Has there been a legal or compliance review? If not, should that be an open item with an owner?"
- _If 3+ teams involved:_ "Has anyone asked who has final decision-making authority when teams disagree?"

For each probe the user confirms as a real question:
- What was the question?
- What was the answer?
- Who answered it, and when?
- Is this Resolved or Open?

Then ask: "Are there any other questions that have come up from stakeholders or engineering?"

For any open (unresolved) items:
- "Who specifically owns resolving this? I need a person, not a team."
- "What is the deadline for resolution?"
- RULE: An open item with no individual owner is a warning. Push for a name before accepting the entry.
