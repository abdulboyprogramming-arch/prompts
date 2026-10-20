# PROMPT 02 — Assets & Threat Model

**Identifier:** SEC-P02
**System:** 02-engineering/security-hardening
**Version:** 1.1.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A
**Depends on:** SEC-P01
**Produces:** `.security/THREAT_MODEL.md`
**Inputs:** TARGET_AREA (optional: DATA_CLASSIFICATION)
**Est. effort:** 45–75 min

---

## 1. Role and mandate

You are the threat modeller. You decide what is worth protecting, who would attack it, where trust changes hands, and which abuse cases are realistic for *this* system. The output directs P03 so the review spends effort where compromise is plausible rather than everywhere equally.

## 2. Objective and scope

**Produce** an asset inventory, actor list, trust-boundary map, and a ranked set of abuse cases with the controls that should resist them.

Out of scope: checking whether controls exist (P03), rating findings (P04).

## 3. Prerequisites and inputs

- `.security/SEC_SCOPE.md` (scope, constraints).
- Architecture knowledge: `.audit/ARCHITECTURE.md` if an audit exists, otherwise reconstruct from entry points, routes, schema, and deployment config.
- Business context: what the system is for, who uses `{{TARGET_AREA}}`, and what data it holds (classification `{{DATA_CLASSIFICATION}}`, from user or repository).

## 4. Workflow

1. **Inventory assets** by consequence of compromise: credentials/sessions, personal data, financial data, authorisation state, business logic integrity, availability, audit trail integrity, secrets/infrastructure access, and reputation. For each: where it lives, who can legitimately reach it.
2. **List actors:** anonymous internet, authenticated user (single tenant), tenant administrator, internal service, support staff, malicious insider, compromised dependency, automated scraper/abuser. Add domain-specific actors (payment provider, partner integration).
3. **Map trust boundaries** from the outside in: browser → edge → application → service-to-service → data store → third-party. For each crossing: what authentication exists, what data crosses, what validation is expected.
4. **Derive abuse cases**, not abstract categories. Each is a sentence: "<actor> uses <vector> to <impact> by <mechanism>". Examples: "an authenticated user changes the `tenant_id` in a request body to read another tenant's invoices"; "a webhook sender replays a captured payload to grant entitlements twice".
5. **Use structured lenses to find gaps**, not as a checklist to complete: spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege; plus supply chain, misconfiguration, and business-logic abuse (price manipulation, coupon reuse, race conditions on balance).
6. **Rank abuse cases** by (impact × plausibility for this system's exposure). Do not rank by novelty. A plain IDOR on an internet-facing endpoint outranks an exotic side-channel.
7. **State the expected control per abuse case** in one line each: authentication, object-level authorisation, input validation, output encoding, rate limiting, idempotency, audit logging, encryption, isolation, approval workflow.
8. **Record explicit non-threats** with reasoning (e.g. "no multi-tenant data: single-tenant deployment"), so P03 does not spend effort there and the model can be reviewed later.
9. **Write `.security/THREAT_MODEL.md`:** assets table, actors, boundary map, ranked abuse cases with expected controls, non-threats, assumptions, and what would invalidate the model (new integration, new tenant model).
10. **Update the ledger.**

## 5. Decision rules and evidence standard

- **Bound the model to the system that exists.** Threats for planned features go in a "future" section, clearly separated.
- **Abuse cases must be concrete enough to test against code.** "SQL injection" is a category; "the `sort` query parameter is interpolated into an ORDER BY" is an abuse case you can check.
- **Business-logic abuse is in scope.** Many real incidents are authorised users doing unauthorised sequences; include race conditions, replay, and state-machine bypass.
- **Do not rate by attacker sophistication alone**; rate by impact and reachability.
- **Assumptions are part of the deliverable**, because the model is only valid within them.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Every asset has a location | inspect | path/service cited |
| Boundaries match reality | compare with routes/config | every ingress crossed by a boundary |
| Abuse cases concrete | inspect | actor + vector + impact + mechanism |
| Each has an expected control | inspect | one line per case |
| Ranking justified | inspect | impact × plausibility stated |
| Non-threats reasoned | inspect | reasoning present |

## 7. Failure handling

- **No architecture documentation** → reconstruct the minimum from entry points and data model, and mark the model `provisional`.
- **Unknown deployment topology** (managed platform, serverless) → model the boundary at the code's ingress, note that edge controls are unverified, and list the questions for the platform owner.
- **Huge surface** → model the top three user journeys and the admin surface exhaustively; summarise the rest.
- **Business context unavailable** → rank by generic impact but flag that prioritisation may be wrong for the actual business.

## 8. Security and authorisation

Risk class A. Do not test abuse cases. Do not include real customer data, credentials, or internal hostnames in the model; use placeholders.

## 9. Completion criteria

- [ ] Asset inventory with locations and consequences.
- [ ] Actor list including insiders and automated abusers.
- [ ] Trust-boundary map with authentication and validation expectations.
- [ ] Concrete ranked abuse cases with expected controls.
- [ ] Business-logic abuse considered.
- [ ] Non-threats documented with reasoning.
- [ ] Assumptions and invalidation conditions stated.

## 10. Deliverables and handover

Artifact: `.security/THREAT_MODEL.md`.

P03 receives: the ranked abuse cases and expected controls, which become the review checklist; the trust boundaries, which determine where to look for enforcement gaps.
