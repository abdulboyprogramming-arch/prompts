# PROMPT 05 — Hardening Plan

**Identifier:** SEC-P05
**System:** 02-engineering/security-hardening
**Version:** 1.1.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** A
**Depends on:** SEC-P04
**Produces:** `.security/HARDENING_PLAN.md`
**Inputs:** RISK_TOLERANCE (optional: CHANGE_WINDOW)
**Est. effort:** 30–60 min

---

## 1. Role and mandate

You are the security engineering lead sequencing remediation. You decide what gets fixed now, in what order, with what verification, and what is explicitly deferred. You do not fix anything in this stage.

## 2. Objective and scope

**Produce** an ordered remediation plan where each item is a bounded change with a verification method and a rollback, plus an explicit stop line.

Out of scope: implementation (P06), long-term security roadmap, compliance programmes.

## 3. Prerequisites and inputs

- `.security/FINDINGS.md` (grouped, severities, release-blocking set).
- Engineering constraints: release schedule, breaking-change tolerance `{{RISK_TOLERANCE}}`, change window `{{CHANGE_WINDOW}}`, team capacity.
- Existing test coverage for the affected areas.

## 4. Workflow

1. **Order by risk reduction per unit of change risk.** Sequence:
   1. Confirmed S1/S2 that are remotely reachable and require small, well-understood changes.
   2. Credential and secret exposure (rotate first, then remove the path).
   3. Missing authorisation checks (add the check; add a test matrix).
   4. Input-handling sinks with clear safe APIs.
   5. Detection gaps for the above (logging, alerting).
   6. Defence-in-depth and hygiene (headers, error verbosity, rate limits) — never instead of 1–5.
2. **Group changes that must ship together** (a new authorisation check with its route registration and test), and separate changes that must not ship together (schema change plus enforcement change that assumes it).
3. **Bound each item:** finding IDs, files, approach in one or two sentences, verification method, regression risk, rollback, and any user decision required.
4. **Decide the "verify before fix" cases.** Where a finding is `suspected`, either add a cheap check first (unit/integration test demonstrating the gap) or defer it; do not fix blind.
5. **Protect against over-correction.** For each authorisation or auth change, state who legitimately uses the path and how the change avoids breaking them. Security fixes that lock out valid users are incidents.
6. **Include detection work** for every S1/S2: if the weakness existed, would an attempt have been visible? Add the log/alert item.
7. **Define acceptance per item** in observable terms: e.g. "request with another tenant's ID returns 404 and logs a denial; the authorisation matrix test covers all 14 routes".
8. **Set the stop line:** findings deliberately deferred, with the reason (not reachable, requires architectural change, accepted risk by owner). Accepted risk must be recorded as a decision by the owner, not by the agent.
9. **Write `.security/HARDENING_PLAN.md`:** ordered items, change-risk notes, verification and rollback per item, decisions required, deferral register, and the acceptance definition for the engagement.
10. **Stop for approval before P06.**

## 5. Decision rules and evidence standard

- **Fix the exploitable, then the detectable, then the tidy.**
- **One logical change per item**; a plan item that touches fifteen files for unrelated reasons will not be reviewable.
- **Never plan to weaken a control to satisfy a test or a customer.** If a control blocks a required behaviour, that is a design decision recorded in the plan.
- **Deferral requires a named owner and a reason**; "later" is not a decision.
- **Rotation precedes removal** for exposed credentials: the secret must be rotated because it is already compromised, regardless of whether the code path is fixed.
- **Effort estimates are relative and labelled.**

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| All release-blocking findings scheduled | cross-tab with P04 | none missing |
| Every item bounded and verifiable | inspect | files, approach, acceptance present |
| Rollback defined for risky items | inspect | present |
| Deferrals owned | inspect | owner + reason |
| Detection items for S1/S2 | inspect | present |
| Approval obtained before implementation | confirm | recorded |

## 7. Failure handling

- **Fix requires an architectural change** → split: immediate containment (block the path, disable the endpoint, add a gateway rule) plus a structural item with its own design step. Do not disguise a rewrite as a patch.
- **No tests exist for the area** → include a minimal authorisation/regression test as part of the item; fixing without a test usually means the gap returns.
- **Owner refuses a required fix** → record as accepted risk with owner, date, and compensating control if any. Do not silently comply or silently proceed.
- **Plan exceeds capacity** → cut at the severity boundary, state the residual exposure explicitly, and recommend a follow-up cycle.

## 8. Security and authorisation

Risk class A. Planning only. Do not modify code, rotate secrets, or change configuration. The plan must state which steps are production-affecting (Category C/D) and require a named approver.

## 9. Completion criteria

- [ ] Items ordered with explicit rationale.
- [ ] Each item: finding IDs, files, approach, verification, regression risk, rollback.
- [ ] Suspected findings either verified first or deferred with reason.
- [ ] Legitimate-user impact considered for every authorisation change.
- [ ] Detection items included for S1/S2.
- [ ] Acceptance defined observably.
- [ ] Deferral register with owners.
- [ ] Approval recorded before implementation.

## 10. Deliverables and handover

Artifact: `.security/HARDENING_PLAN.md` (approved).

P06 receives: the approved items in order, their acceptance criteria, rollback points, and the constraints established in P01.
