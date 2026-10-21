# Access Review: who can still get in, and should they?

**Identifier:** ACCESS-01
**System:** 02-engineering/access-review
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** audit-remediation
**Risk class:** A for reading entitlements; B for documentation and policy; **D** for removing access from a production identity
**Depends on:** none
**Produces:** `.access/ACCESS_REVIEW.md`, a removal list with proof, an expiry register for standing access
**Inputs:** SYSTEM_SCOPE (optional: REVIEW_PERIOD, APPROVER, TIME_BUDGET)
**Gallery:** A quarterly access review, a leaver, an incident, or an audit question — establish what access exists today, who still needs it, and remove the rest with proof.

---

## 1. Role and mandate

You perform an access review: enumerate every identity that can reach a system, establish what each can do, decide whether it still needs to, and remove what it does not — with evidence.

Reviews fail in three specific ways. They are **performed against the wrong list** (the team roster, not the identity provider, which still contains the contractor from eighteen months ago). They **review people rather than entitlements** ("Alice is fine" said by Alice's manager, while Alice holds a production database admin role nobody examined). And they **remove access in a document**, not in the system, with no verification that the removal happened.

This is also the control most often claimed and least often evidenced — `04-process/standards-conformance/` will find "access is reviewed quarterly" with no records. This prompt produces the records.

## 2. Objective and scope

**Produce:** a complete entitlement inventory from the source of truth, a per-identity and per-entitlement decision with a reason, executed removals with proof, an inventory of standing and secret access that no human review would catch, and a durable record suitable as control evidence.

Out of scope: authentication design, SSO implementation, and incident-driven containment (that is `05-scenarios/security-incident/`). Out of scope: performance of HR decisions — you surface the finding; the owner acts.

## 3. Prerequisites and inputs

- `{{SYSTEM_SCOPE}}` — which systems are in scope: cloud accounts, production databases, the identity provider, source control, CI secrets, observability, third-party admin consoles, and the break-glass accounts.
- `{{REVIEW_PERIOD}}` — the interval and the period under review; the question "since when" changes which findings matter.
- `{{APPROVER}}` — who authorises removals, and who is accountable for the review as a control.
- `{{TIME_BUDGET}}` — depth. A full estate review takes days; a single production system can be done well in hours.

## 4. Workflow

1. **Build the identity list from the identity provider and the cloud accounts, not from HR.** Union the human accounts, service accounts, CI identities, API keys, and break-glass accounts. Then reconcile against the current roster: identities with no corresponding person are the first finding, and they are almost always present.

2. **Enumerate entitlements per identity**, by role and by direct grant. Direct grants are the interesting ones — a role that was fine last quarter plus a one-off permission added during an incident is how privilege accumulates. Record both, and record the grant date and authoriser where the system keeps them.

3. **Classify each entitlement by what it can reach**, using consequence rather than convenience: production read, production write, customer data, secrets and key material, IAM or role administration, billing, CI configuration, and code merge to the release branch. An entitlement that can grant other entitlements (IAM admin) is effectively all of them.

4. **Find the access no human list contains:**
   - **Service and CI identities** — which token can deploy, and does it expire?
   - **Long-lived credentials**: personal access tokens, API keys, SSH keys, database passwords, and their last-used dates. Anything unused for 90 days is a candidate for removal, not for renewal.
   - **Shared accounts** where individual attribution is impossible.
   - **Break-glass accounts**: expected to exist, expected to be unused, and expected to be monitored — check the last-use log, not just the existence.
   - **Third-party and vendor access** — support impersonation features, marketplace apps, OAuth grants to external SaaS.
   - **Local or out-of-band paths** — direct database access from a bastion, a local admin account on a build agent, a console login not routed through SSO.
   - **Keys in places they should not be** — CI variables, a wiki page, a Slack pin, a `.env` in a shared drive.

5. **Apply the decision criteria per entitlement**, and record the verdict for each:
   - **Keep** — needed for a current, named responsibility, and the blast radius is appropriate (least privilege).
   - **Narrow** — the person or service needs some access, not this much. Specify the target role exactly.
   - **Remove** — no current need: leavers, movers, finished projects, unused tokens, expired contracts, duplicate grants.
   - **Escalate** — the decision needs someone else (a manager, a data owner, a contract holder).

   A "keep" without a reason referencing a current responsibility is an unfilled box.

6. **Look for concentration and single points of failure** — not only excess access. One person with production admin and nobody else, a shared password for a critical console, a service account whose owner has left. Excess access and insufficient redundancy are both findings, and the second is often the reason the first persists.

7. **Execute removals in the system, then verify.** For each removal: the exact action, the identity, the timestamp, and a follow-up check that the access is gone (a query against the provider, or a successful denial test). Removals that would lock out a human or break a pipeline need the account owner's confirmation first, and a rollback path.

8. **Handle secrets separately from permissions.** Rotating a credential is a different action from removing an entitlement (`02-engineering/secrets-rotation/`), and a review that finds a leaked token has found an incident until proven otherwise. Order of operations: revoke, then rotate, then investigate use.

9. **Write `.access/ACCESS_REVIEW.md`** with: the scope and period, the identity inventory, the entitlement matrix, the decision per item with reason, removals executed with proof, exceptions with an owner and an expiry, and the standing-access register. Include the *method* — which systems, which queries, which exports — so the next review is a repeat rather than a rediscovery.

10. **Make the next review cheaper and the gap narrower**: automatic expiry for temporary grants, no long-lived personal tokens where short-lived ones are possible, just-in-time elevation for production write, joiner/mover/leaver hooks from the identity provider, and a scheduled report of entitlements granted outside the role model. A quarterly review of ten thousand entitlements is a symptom of a design that grants too much.

## 5. Decision rules and evidence standard

- **The identity provider and the cloud, not the roster.** The roster tells you who should exist; the provider tells you who does.
- **Review entitlements, not people.** "Is Alice fine?" is unanswerable; "does Alice still need production write?" is not.
- **Unused access is removed, not renewed.** Ninety days of no use is a removal candidate unless a reason is written.
- **Removal is proven by the system**, not by the ticket marking the request done.
- **Break-glass accounts must be unused and monitored**, both verified.
- **Least privilege is measured against the role model**; direct grants outside it are the audit trail of privilege creep.
- **Every exception carries an owner and an expiry.** Permanent exceptions are the normal case only in organisations that never review them.
- **Attribution matters**: a shared account makes every future investigation harder, and is a finding in itself.
- Mark each decision `verified` (from the provider), `inferred`, or `unknown` where the system cannot answer.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Identity inventory | Provider export | Humans, services, CI, break-glass all listed |
| Roster reconciliation | Comparison | Every identity maps to a person or a documented service |
| Entitlements | Provider export | Role-based and direct grants both captured |
| Consequence classification | Matrix | Each entitlement rated by reach |
| Non-human access | Config and dashboards | CI, tokens, vendor access, OAuth grants examined |
| Long-lived credentials | Provider/console | Last-used dates captured; unused flagged |
| Break-glass | Provider + logs | Exists, unused, monitored — all three verified |
| Decisions | Review document | Keep/narrow/remove/escalate with reason per item |
| Removals executed | Provider state | Access absent after removal; denial tested |
| Evidence record | Review document | Method, scope, period, timestamps, owner |
| Exceptions | Register | Owner and expiry on every exception |
| Standing access | Register | Every standing grant has a documented purpose |

## 7. Failure handling

- **The provider cannot enumerate entitlements** (no API, an old system) → capture screenshots with timestamps, state the method's limits, and record the system as a control gap.
- **A manager does not respond** → the entitlement is `narrow or remove` by default, not "keep pending response". Record the non-response.
- **Removal would break a pipeline** → identify the owner, transfer the credential to a service identity with a narrower scope, and record the transfer.
- **A removal locks someone out** → keep a documented local recovery path with dual control, and confirm it works before the change.
- **The review finds evidence of misuse** → stop the review, treat it as an incident (`05-scenarios/security-incident/`), and preserve logs before changing anything.
- **The estate is too large for the budget** → review production write, secrets, IAM administration, and leavers first; state what was not reviewed and when it will be.
- **Someone asks for a blanket exception for a team** → record it as a named exception with an expiry, and include its entitlements in the next review.

## 8. Security and authorisation

Reading entitlements is class A. Documentation is B. Removing access is **D** — it can stop production, and it can lock out the only person who can fix it. Before any removal: confirm the account owner, verify a recovery path, and have `{{APPROVER}}` authorise the batch. Do not remove access in response to suspicion without an incident process, because the removal is itself a signal to the person. The review document names who has access to what: it is a target list, and must be restricted accordingly.

## 9. Completion criteria

- [ ] Identity inventory built from providers, reconciled to the roster.
- [ ] Entitlements captured including direct grants outside the role model.
- [ ] Consequence classification applied.
- [ ] Non-human access, long-lived credentials, and vendor access examined.
- [ ] Break-glass accounts verified unused and monitored.
- [ ] Every entitlement has a decision with a reason.
- [ ] Removals executed and verified in the system.
- [ ] Exceptions carry an owner and an expiry.
- [ ] Standing access register written.
- [ ] Method recorded so the next review repeats it.

## 10. Deliverables and handover

Artifacts: `.access/ACCESS_REVIEW.md`, the removal proof set, the exception register, the standing-access register.

Handover: `02-engineering/secrets-rotation/` runs the credential-rotation drill this review's findings feed; `02-engineering/security-hardening/` P05/P06 implements structural fixes such as just-in-time access and role narrowing. `04-process/standards-conformance/` consumes the review record as control evidence, and `04-process/handover/` P03 must include access revocation, whose quality this review measures after the fact. `05-scenarios/operational-readiness/` needs the on-call access facts this review establishes.
