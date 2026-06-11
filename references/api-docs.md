# API & Vendor Documentation Registry

A curated list of official documentation URLs for vendors commonly named in PRDs.

**Purpose:** when the user names a third-party vendor in §0.4 but does *not* give a docs
link, suggest the official URL below and ask the user to confirm before fetching. This is a
convenience only — it does **not** authorize autonomous search. The skill stays fetch-only:
it `WebFetch`es a URL the user has confirmed (from this list or one they provide), never a
URL it discovered by searching.

**What to extract** when reading vendor docs (feeds §8 NFRs, §9 Technical Constraints, §14
Dependencies): rate limits, quotas, authentication model, SLAs / uptime commitments, pricing
tiers, data residency / region options, webhook and idempotency behaviour.

**Guardrails:**
- Never invent a rate limit, quota, or SLA. If the fetched page does not state it, write
  `[TBD — confirm with vendor docs]`.
- Cite every extracted fact: `[source: <url>, retrieved: YYYY-MM-DD]`.
- Show the user the exact extracted value before writing it (verify-before-write rule).
- `last_reviewed` reflects when this list was last checked; URLs may move — fall back to
  asking the user for the current link.

**last_reviewed:** 2026-06-11

| Vendor | Category | Official Docs URL |
|---|---|---|
| Stripe | Payments | https://docs.stripe.com/ |
| Adyen | Payments | https://docs.adyen.com/ |
| PayPal / Braintree | Payments | https://developer.paypal.com/api/rest/ |
| Midtrans | Payments (ID) | https://docs.midtrans.com/ |
| Xendit | Payments (SEA) | https://developer.xendit.co/ |
| Plaid | Banking / data aggregation | https://plaid.com/docs/ |
| Twilio | Messaging / SMS / voice | https://www.twilio.com/docs |
| SendGrid | Email | https://www.twilio.com/docs/sendgrid |
| Onfido | Identity / eKYC | https://documentation.onfido.com/ |
| Jumio | Identity / eKYC | https://docs.jumio.com/ |
| Persona | Identity / eKYC | https://docs.withpersona.com/ |
| VIDA | Identity / eKYC / digital signature (ID) | https://docs.vida.id/ |
| Verihubs | Identity / eKYC / liveness / OCR (ID) | https://docs.verihubs.com/ |
| Auth0 | Authentication | https://auth0.com/docs |
| Okta | Authentication / SSO | https://developer.okta.com/docs/ |
| AWS | Cloud infrastructure | https://docs.aws.amazon.com/ |
| Google Cloud | Cloud infrastructure | https://cloud.google.com/docs |
| Microsoft Azure | Cloud infrastructure | https://learn.microsoft.com/azure/ |
| Firebase | Backend / mobile | https://firebase.google.com/docs |
| Mixpanel | Analytics | https://docs.mixpanel.com/ |
| Segment | Analytics / CDP | https://segment.com/docs/ |
| Amplitude | Analytics | https://amplitude.com/docs |
| Google Analytics (GA4) | Analytics | https://developers.google.com/analytics |

**Vendors with gated docs** — these publish no public API documentation, so they have no row
above. Treat them like any auth-walled source: ask the user (or the vendor) for access and
paste the relevant excerpt.

- **Privy** (privy.id — the Indonesian digital-identity / digital-signature provider; not to
  be confused with privy.io, a US web3 auth company). API docs are provided on request.
- **ASLI RI** (asliri.id — Indonesian biometric verification / eKYC). Docs via sales contact.

> To extend this list, add a row with the vendor's **official** documentation domain. Do not
> add unofficial mirrors, blog posts, or aggregator pages.
