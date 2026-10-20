# PROMPT 02 — Flag Design and Safe Defaults

**Identifier:** FF-P02
**System:** 04-process/feature-flags
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** B
**Depends on:** FF-P01 (for the existing set); none when designing a flag from scratch
**Produces:** `.flags/FLAG_DESIGN.md`
**Inputs:** TARGET_SERVICE, CHANGE_WINDOW (optional: RISK_TOLERANCE, APPROVER)
**Est. effort:** 30–60 min

---

## 1. Role and mandate

You decide whether a flag should exist at all, what type it is, what its default must be, and how it will die. Most flag debt is created at design time by flags that were never given an owner, an expiry, or a reason.

Your bias: **the fewest switches that let the change ship safely.** A flag is a cost paid on every future read of that code.

## 2. Objective and scope

**Produce:** a design record per flag: purpose and type, name, read sites, default and failure behaviour, targeting, owner, expiry or review date, test plan for both states, and removal criteria.

Out of scope: implementing the flag plumbing for an existing codebase is part of the change itself; staged exposure is P03; removal is P05.

## 3. Prerequisites and inputs

- The change being made and the risk it carries — from `.flags/FLAG_INVENTORY.md`, the plan, or the request.
- `{{TARGET_SERVICE}}` and the window `{{CHANGE_WINDOW}}` in which behaviour may change.
- `{{RISK_TOLERANCE}}` if the team's appetite for partial exposure is known; `{{APPROVER}}` for any flag that will gate a class C/D action.

## 4. Workflow

1. **Justify the flag or remove it.** Four legitimate reasons: ship dark without exposing incomplete behaviour; decouple deploy from release; provide a kill-switch for a risk you cannot fully mitigate; run a controlled experiment. "It might be useful later" is not one. If the change is reversible in minutes and low-risk, a flag is extra surface — say so.

2. **Choose the type explicitly** (release, operational/kill-switch, permission, experiment, migration) and derive the consequences: expected lifetime, who may flip it, whether targeting is allowed, whether it must be auditable. A permission check implemented as a flag is a security defect: entitlements belong in the authorisation system with review and audit, not in a console toggled by support.

3. **Name for removal.** `release_<feature>_<date>` or the ticket identifier, not `new_flow`. The name should tell a future engineer what it is and when it should be gone. Reject names that describe the implementation (`use_v2`) when they can describe the behaviour.

4. **Set the default as a safety property.** Ask: what happens if the flag service is unreachable, the config is missing, or evaluation errors? State the answer per state:
   - Default **off** for incomplete or risky behaviour (fail closed).
   - Default **on** only for a kill-switch whose purpose is to keep the system working when the provider is down.
   - Never a default that silently enables a data-destructive or money-moving path.

5. **Design the read sites.** One evaluation per request, at the outermost sensible point, with the result passed down — not re-evaluated inside loops or deep call stacks, and not read in a way that makes the two paths interleave within one operation. State where the flag is read and what the value is bound to (tenant, user, request).

6. **Declare the targeting and its authority.** Static config, cohort/percentage, tenant list, or per-user. Percentage rollouts need a stable bucketing key (user or tenant id), not a random per-request draw, or a user's experience will flip between requests. Say who may change targeting and whether changes are audited.

7. **Write the both-states test plan.** Which tests run with the flag on, which with it off, and which assert that the flag *itself* works (the default, the fallback, the bucketing stability). If only the "on" state is tested, the off state is unverified code that will be relied on as a rollback.

8. **Set the expiry or review date and the owner, at creation.** Release: a date. Experiment: the analysis end date. Operational: an annual exercise date, with the operator named. Migration: the cutover date. Without this, the flag becomes permanent by inertia.

9. **Record removal criteria** that P05 can execute mechanically: which state becomes the code, what evidence is required (traffic share, elapsed time, no targeting in use), and what must be deleted (branch, config, tests, docs).

10. **Write `.flags/FLAG_DESIGN.md`:** one section per flag with the above, the rejected candidates with the reason, and the aggregate effect on the inventory (how many flags this adds and when each leaves).

## 5. Decision rules and evidence standard

- **No flag without an owner and an expiry.** A flag with neither is a permanent fork of behaviour with nobody accountable.
- **Default safe beats default convenient.** The unreachable case decides the default, not the happy path.
- **A kill-switch is a control, so it needs an operator and an exercise.** Name both, and add the exercise to the design.
- **Never gate authorisation with a flag.** Entitlements belong in the policy layer; flags have no equivalent review or audit.
- **Percentage rollouts require stable bucketing**, or the rollout measures noise.
- **Both states must be testable and tested**, including the default path.
- **Prefer a config value to a flag** when the decision is per-environment and permanent (timeouts, pool sizes). Flags are for behaviour that will change again.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Each flag justified | read-through | one of the four reasons, stated |
| Type matches purpose | inspect | permission gates routed out of the flag system |
| Default is safe | failure-case walkthrough | unreachable provider behaviour stated |
| Bucketing stable | design inspection | key is user/tenant, not random |
| Read sites bounded | code sketch | one evaluation, passed down |
| Both states tested | plan | on, off, and flag-mechanics tests |
| Owner and expiry set | table | no blanks |
| Removal criteria executable | review | mechanical, evidence-based |

## 7. Failure handling

- **The team wants a permanent flag for a feature that will always be on** → that is configuration or a release flag with a removal date; say which, and refuse the ambiguity.
- **The change cannot be made safe with a flag** (data migration, schema change, money movement) → route to `03-domains/database/` or `03-domains/payments/`; a flag does not make an unsafe migration safe.
- **Provider cannot guarantee evaluation availability** → design the default as the operating mode, and state the latency/consistency assumptions.
- **Multiple teams own the flag's consumers** → the flag needs a single owner with authority over all read sites, or it will be removed by whoever finishes first. Name the conflict.
- **The design adds more than three flags to one change** → the change is too large to reason about; propose splitting rather than building a matrix.

## 8. Security and authorisation

Risk class B: designing flags changes production behaviour indirectly. Do not put secrets, customer identifiers, or entitlement lists in flag names, targeting rules, or artifacts. Flags that gate security-relevant behaviour must be marked as such and require `APPROVER` before P03. Never design a flag whose "off" state disables logging, auditing, or authorisation checks.

## 9. Completion criteria

- [ ] Every flag justified against the four legitimate reasons; rejections recorded.
- [ ] Type assigned, with entitlement-like gates routed elsewhere.
- [ ] Names encode purpose and removal.
- [ ] Default and unreachable-provider behaviour stated per flag.
- [ ] Read sites and binding declared.
- [ ] Targeting authority and bucketing rule stated.
- [ ] Both-states and flag-mechanics tests planned.
- [ ] Owner, expiry/review date, and removal criteria recorded.

## 10. Deliverables and handover

Artifact: `.flags/FLAG_DESIGN.md`.

P03 receives: the flag set with defaults, targeting rules, and the metrics gates must be defined against. P05 receives: the removal criteria, written before the flag existed, which is the only time they are written honestly.
