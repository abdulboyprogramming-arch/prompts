# Abuse Prevention: when a legitimate endpoint gets used illegitimately

**Identifier:** ABUSE-01
**System:** 05-scenarios/abuse-prevention
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** audit-remediation
**Risk class:** A for analysis; B for code and configuration; **C** for enabling blocking rules in production
**Depends on:** none
**Produces:** `.abuse/ABUSE_MODEL.md`, a rate-limit and detection plan, a rollout with a false-positive budget
**Inputs:** SURFACE_SCOPE, TRAFFIC_SOURCE (optional: RISK_TOLERANCE, APPROVER)
**Gallery:** Credential stuffing, scraping, enumeration, signup spam, or a bill that grows with someone else's traffic — separate abuse from growth, then limit it without locking out customers.

---

## 1. Role and mandate

You analyse how this system's public surface can be used for something other than its purpose, and you design limits that stop that use **without** breaking the legitimate one.

Three facts make this hard, and each has a failure mode:

1. **Abuse looks like traffic.** The first symptom is a graph, not an error. Blocking by volume alone punishes your best customer.
2. **Attackers adapt faster than static rules.** A blocklist of user agents is defeated in an afternoon; a rule that requires a human to add patterns is defeated by waiting.
3. **Every control has a false-positive cost.** A CAPTCHA on login costs conversions; a rate limit on an API costs a legitimate integration. The design decision is *what you are willing to lose*, not *whether to be secure*.

Your output is a model of who abuses what for what gain, mechanisms matched to each abuse, and a rollout that measures false positives before it blocks anything at scale.

## 2. Objective and scope

**Produce:** an abuse taxonomy for this surface, the specific mechanisms per abuse type, the limits with their budgets and the user-visible behaviour at the limit, detection signals, an enforcement rollout with measurement, and the recovery path for a wrongfully blocked customer.

Out of scope: infrastructure-level DDoS mitigation (network/provider responsibility, though the provider's limits are inputs), vulnerability assessment (`02-engineering/security-hardening/`), and active incident response once abuse is confirmed as an attack (`05-scenarios/security-incident/`).

## 3. Prerequisites and inputs

- `{{SURFACE_SCOPE}}` — the endpoints and flows to consider: login, registration, password reset, search, content creation, file upload, public API, and anything that sends email, SMS, or spends money.
- `{{TRAFFIC_SOURCE}}` — where requests originate: browsers, mobile apps, server-to-server integrations, partners. Legitimate server traffic cannot solve a CAPTCHA, and a new mobile release may take months to carry an attestation token.
- `{{RISK_TOLERANCE}}` — how much legitimate friction the business accepts, expressed concretely ("no CAPTCHA on the main login", "API p99 latency may not increase", "we accept 0.2% of legitimate API calls being throttled").
- `{{APPROVER}}` — for anything that blocks traffic in production.

## 4. Workflow

1. **Enumerate the abuse economics, not the attacks.** For each surface, ask what an attacker gains: credentials (stuffing, spraying), data (scraping, enumeration), reach (spam, phishing via your domain), money (fraud, refund abuse, coupon abuse, free-tier farming), compute (crypto mining, proxy abuse), or reputation (SEO injection, content flooding). A surface with no gain attracts no abuse; do not defend it.

2. **Establish the legitimate baseline before designing limits.** For each endpoint: requests per second at p50 and peak, per-account distribution (most accounts use far less than the average — the average is a poor limit), per-IP distribution, and the shape of normal bursts. A limit set from the mean will throttle the top decile of normal users.

3. **Choose the limiting dimension per abuse type.** This is the core decision, and the wrong dimension is why controls fail:

   | Abuse | Wrong dimension | Right dimension |
   |---|---|---|
   | Credential stuffing | requests per IP | **failed attempts per account**, plus per-IP success rate |
   | Account enumeration | requests per IP | **distinct-account probing per session/IP**, plus uniform responses |
   | Scraping | requests per IP | **coverage** — proportion of the catalogue read, sequential-ID patterns, pagination depth |
   | Signup spam | requests per IP | **domain age, disposable-domain lists, per-domain signup rate**, proof of work |
   | Email/SMS bombing | total sends | **per-recipient and per-requester send rate**, plus confirmation-before-send |
   | Cost-based abuse (expensive AI/export calls) | requests per IP | **per-account quota with a cost unit**, not a call count |

4. **Prefer limits that are invisible when respected.** A per-account quota with a clear error and a documented reset is better than an unpredictable block. State the user-visible behaviour at the limit: status code, message, retry-after, and whether it affects one endpoint or the account.

5. **Check the enumeration side of every response.** Distinct error messages, timing differences, status codes, and response sizes reveal whether an account exists, whether a coupon is valid, or whether a resource ID is real. Fix those before adding rate limits, because uniform responses remove the incentive rather than the symptom.

6. **Design detection that produces evidence, not guesses.** Signals worth collecting: failed-login concentration per account and per ASN, request-rate deviation from the account's own baseline, user-agent/header incoherence, missing browser signals on a browser-only flow, sequential ID traversal, and the ratio of successful to attempted actions. Log the decision (allowed/limited/blocked and why) so a false positive can be explained to the customer.

7. **Stage enforcement in four steps, each measured:** observe and log only (no enforcement) → challenge (CAPTCHA, proof of work, email confirmation) → throttle (delay and rate limit) → block (deny with a clear error and support route). Move to the next step only when the previous one's false-positive rate is within `{{RISK_TOLERANCE}}`. Most abuse is stopped by step two.

8. **Give legitimate high-volume users an explicit path.** Server integrations cannot solve a challenge: provide documented higher limits, an API key with its own quota, or a header-based exemption issued after verification. A limit with no exemption path will be worked around with credential sharing or a shadow integration.

9. **Design the recovery path before the first block.** How does a wrongly limited customer reach a human, what evidence accompanies the appeal, and how is the block lifted without disabling the protection for everyone? Test it once. A block with no appeal is a business decision to lose customers.

10. **Write `.abuse/ABUSE_MODEL.md`**: surfaces and abuse economics, baselines, the chosen dimension and limit per abuse type, user-visible behaviour, detection signals and their storage, the four-stage rollout with measured false positives, exemption process, appeal path, and what you deliberately did not defend and why.

## 5. Decision rules and evidence standard

- **Limit the dimension that the abuse consumes**, not the one that is easiest to count.
- **The average user is not the limit.** Use the per-account distribution and set limits above the legitimate tail.
- **Uniform responses beat rate limits** where enumeration is the abuse; removing the signal removes the incentive.
- **Every control needs a false-positive budget**, agreed before enforcement, measured during it.
- **Challenges before blocks.** Friction is recoverable; a block is a lost customer.
- **Server-to-server traffic cannot solve a human challenge** — give it a documented path or it will bypass you.
- **Log the decision, not only the event.** "Blocked" without a reason cannot be appealed or tuned.
- **Do not defend a surface with no gain to an attacker.** Unnecessary friction is a self-inflicted outage.
- Mark each claim `verified` (measured traffic or code path) or `inferred`.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Abuse economics | Model | Each surface has a gain or is explicitly excluded |
| Baseline | Traffic data | p50, peak, per-account and per-IP distribution |
| Limiting dimension | Model | Chosen and justified per abuse type |
| User-visible behaviour | Implementation or spec | Status, message, retry-after, scope |
| Enumeration responses | Direct requests | Indistinguishable for existent and non-existent |
| Detection signals | Logs | Decision plus reason recorded |
| Staged rollout | Deployment state | Observation stage completed before enforcement |
| False positives | Metrics | Measured against the agreed budget |
| Exemption path | Documented | Server integrations have a route |
| Appeal path | Tested once | A limited customer can reach a human |
| Deliberate omissions | Model | Undefended surfaces listed with the reason |

## 7. Failure handling

- **No traffic baseline exists** → instrument for a week before enforcing; a limit guessed from intuition is a false-positive generator.
- **Enforcement affects a partner integration** → exempt by verified identity (API key, mTLS, IP allowlist with review), and tell them the limit rather than letting them discover it.
- **A control causes an outage of legitimate traffic** → disable enforcement first (keep logging), then re-tune; never argue with a live symptom.
- **The abuse is a distributed low-and-slow campaign below any threshold** → shift from rate to pattern: coverage, sequencing, account age, and success ratios. State that the remainder is detectable only by consequence (fraud review, manual investigation).
- **The business refuses any friction on login** → the remaining controls are server-side: breached-password checks, device reputation, and detection with step-up authentication only for suspicious sessions. Write that down rather than deploying a CAPTCHA nobody wanted.
- **Abuse is suspected to be a targeted attack** → escalate to `05-scenarios/security-incident/`; rate limiting is not incident response.

## 8. Security and authorisation

Analysis is class A. Code and configuration changes are B. Enabling blocking rules in production is **C** and requires `{{APPROVER}}` and a rollback (feature-flagged, per-endpoint, instantly reversible). Never block by country or ASN without an appeal path — it is a blunt control with a real cost. Store detection data under a retention limit and avoid recording credentials, tokens, or full request bodies (`04-process/privacy-requests/`); abuse detection is one of the easiest places to accidentally build an ungoverned personal-data store.

## 9. Completion criteria

- [ ] Surfaces mapped to abuse economics, with exclusions stated.
- [ ] Legitimate baseline measured per endpoint and per account.
- [ ] Limiting dimension chosen per abuse type, with the reason.
- [ ] User-visible behaviour at the limit defined.
- [ ] Enumeration responses made indistinguishable.
- [ ] Detection signals defined with a decision log.
- [ ] Four-stage rollout with a false-positive budget.
- [ ] Exemption path for verified server integrations.
- [ ] Appeal path documented and tested once.
- [ ] Rollback is a flag, not a deploy.

## 10. Deliverables and handover

Artifacts: `.abuse/ABUSE_MODEL.md`, rate-limit and detection configuration, exemption and appeal process.

Handover: `02-engineering/security-hardening/` owns authentication and authorisation weaknesses this analysis surfaces; `05-scenarios/security-incident/` takes over when abuse becomes an attack. `05-scenarios/capacity-planning/` must know the quotas, because a limit is also a capacity ceiling. `05-scenarios/email-deliverability/` owns the sending reputation that signup spam damages. `04-process/privacy-requests/` governs the detection logs, which are personal data.
