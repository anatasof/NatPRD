# Interview Questions by Section

These are the questions Claude asks the user during Mode 1 (Generate).
Ask them conversationally — one at a time, not as a dump.
Validate each answer before moving to the next section.

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
2. What evidence do you have that this problem exists? (data, research, tickets, NPS, incidents)
   - _If no evidence:_ "We'll need to cite something here — even rough numbers. What can we reference?"
3. Has this been attempted before? Is there any prior work or history we should acknowledge?
4. What happens if we do nothing? What is the cost of inaction — revenue, users, compliance, competitive position?

---

## §4 — Objective

1. What does success look like in one sentence? This should be an outcome, not a feature.
   - _Probe if it's a feature:_ "That's what we're building — but what business result does it produce?"
2. What are 2–3 measurable key results? For each one I need: the metric, the current baseline value, the target value, and the timeline.
   - _If no baseline:_ "Do you have a current number to start from? Even an estimate?"
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
2. How confident are you in this hypothesis? (High / Medium / Low) — and why?
3. What would tell you the hypothesis is wrong? What result or signal would prove it doesn't hold?
4. Who will own the post-launch retrospective to revisit this hypothesis?

---

## §7 — Success Metrics

**Primary Metrics:**
1. What is the main metric this initiative is optimizing for?
2. Is there a leading indicator — a metric that will move first and predict future success?
3. Is there a lagging indicator — a metric that confirms success after the fact?
4. For each metric: what's the baseline? What's the target? How will it be measured? By when? Who owns it?

**Guardrail Metrics:**
5. What metrics must not regress as a result of this initiative?
6. For each guardrail: what's the baseline, and at what threshold should we raise an alarm?

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

After each story: "Any more user stories for this initiative?"

**Non-Functional Requirements:**
9. Are there performance requirements? (e.g., response time, throughput)
10. Are there security or compliance requirements? (e.g., encryption, OJK, regulatory)
11. Are there accessibility requirements?
12. Are there availability or uptime requirements?
   - _For each:_ "How will this be verified or tested?"

---

## §9 — Solution

1. At a high level, how does the proposed solution work from the user's perspective?
2. Do you have design artifacts — flows, wireframes, mockups? Please share the links.
   - _If no links yet:_ "What's the current design status? We'll mark it as Draft."
3. For each user story we captured, which part of the solution addresses it?
4. What alternatives were considered and why were they rejected?
   - _Probe if none:_ "There are always tradeoffs — what did you consider and decide against?"
5. Are there any technical constraints or architectural decisions that shaped this solution?

---

## §10 — Metric Monitoring

1. Where will the metrics be monitored post-launch? (dashboard, tool, link)
2. Who is the DRI for monitoring? (name a person, not a team)
3. What's the monitoring cadence? (daily launch week, weekly after, etc.)
4. At what threshold for each primary metric should the team escalate?
5. At what threshold for each guardrail metric should the team escalate?
6. What specific condition would trigger a rollback? Who decides, and how fast can it be executed?
7. Who gets notified first if something goes wrong, and through what channel?
8. Let's set post-launch review dates now — when is the 2-week check-in, 30-day review, and quarterly retrospective?

---

## §11 — Event & Data Tracking

For each event, ask:

1. What is the event name? (follow noun_verb format — e.g., `payment_initiated`)
2. When exactly does this event fire? (be specific — which user action, which screen)
3. What properties/data should be attached to this event?
4. Is this a client-side or server-side event?
5. Where does this event get sent? (Mixpanel, Segment, GA, internal)
6. Which metric from Section 7 does this event support?
7. Does this event involve PII, financial data, or biometric data? (compliance flag)

After all events: "Has the data or analytics team reviewed this tracking plan?"

---

## §12 — FAQ

1. Are there any questions that have already come up from stakeholders or engineering that we should document?
2. For each: what was the question, what was the answer, who answered it, and when?
3. Are there any open questions that don't have answers yet? Who owns resolving each one?

---

## Optional Section Screening Questions

Ask these during intake (Step 1) to determine which optional sections to include:

- "Does this initiative touch payments, financial transactions, compliance requirements, regulated data (eKYC, AML, PII), or multi-team execution?" → Include §13 Risks & Mitigations
- "Is this initiative blocked by another team, or does it depend on a third-party system, API, or vendor?" → Include §14 Dependencies
- "Does this feature require a coordinated rollout, staged release, marketing communications, or a compliance gate before going live?" → Include §15 Launch Plan
- "Does this initiative involve more than 3 teams, require executive sign-off, or involve external parties like vendors, regulators, or partners?" → Include §16 Stakeholder Map
