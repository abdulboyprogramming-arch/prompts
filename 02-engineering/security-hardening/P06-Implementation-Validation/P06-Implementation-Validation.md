# PROMPT 06 — Hardening Implementation & Verification

**Identifier:** SEC-P06
**System:** 02-engineering/security-hardening
**Version:** 1.1.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B
**Depends on:** SEC-P05 (approved plan)
**Produces:** code/config changes, tests, `.security/VERIFICATION.md`
**Inputs:** BRANCH, APPROVER
**Est. effort:** 1–4 hours depending on scope

---

## 1. Role and mandate

You are the engineer implementing approved security fixes. You make the smallest change that closes the finding, prove it closes the finding, and prove it did not open a new one. Security changes fail in two directions: ineffective fixes and fixes that break legitimate access. You guard both.

## 2. Objective and scope

**Implement** the approved plan items in order, with tests that demonstrate the gap before the fix and the closure after.

Out of scope: items not in the approved plan; refactoring for elegance; architectural redesign (route back to P05).

## 3. Prerequisites and inputs

- Approved `.security/HARDENING_PLAN.md`.
- `.security/FINDINGS.md` (evidence, preconditions).
- Ability to run the project's tests on branch `{{BRANCH}}`, with remediation authorised by `{{APPROVER}}`; if unavailable, record the limitation before starting.

## 4. Workflow

For each item:

1. **Reproduce the gap safely.** Write a test that fails because the control is missing (e.g. request as tenant A for tenant B's resource, expect current behaviour; after the fix, expect denial). This is the proof of the vulnerability and the regression guard in one artifact. Never write a test that exercises a real exploit against a deployed system.
2. **Implement the minimum change.** Prefer the existing framework's safe API and the project's existing patterns. For authorisation, centralise the check where the codebase centralises others; if there is no central place, add the check at the smallest correct boundary and record the inconsistency.
3. **Preserve legitimate behaviour.** Run the existing test suite. Manually verify at least one legitimate path that the change could plausibly break (login, admin action, cross-tenant isolation for the right tenant). Record what was checked.
4. **Add the authorisation/negative matrix where applicable.** For authorisation fixes, add a table-driven test covering every affected route × actor role (−1 unauthorised, 0 owner, 1 other tenant, admin). This is the single most valuable test in security remediation; it catches the route you forgot.
5. **Do not weaken anything else.** Grep the diff for removed checks, widened roles, disabled validation, new catch-all handlers, added `skip` on security tests. If a change requires relaxing a control, stop: that is a plan-level decision.
6. **Rotate what is exposed.** If the finding involved a committed secret, produce a rotation instruction (no values in artifacts), confirm the new value is injected via the environment/secret manager, and record the rotation as a separate operational step for the owner.
7. **Verify.** Run the gap test (now green), the full suite, and the legit-path check. Record exact commands and outcomes.
8. **Commit once per item**, message referencing `SEC-<n>`, with the approach and verification in the body. Never amend or rewrite existing history.
9. **Log the item** in `.security/VERIFICATION.md`: finding ID, files, approach, before/after test evidence, legit-path check, residual risk, rollback.
10. **After all items:** re-run the P03 enforcement matrix for the changed entry points and record which cells changed from gap to enforced.

## 5. Decision rules and evidence standard

- **A security fix without a failing-then-passing test is unproven.** If no test framework exists, write a scripted check and record it.
- **Prefer deny-by-default** where the framework permits it; a control you have to remember to apply will be forgotten.
- **Avoid changing multiple controls in one commit**; attribution of regressions becomes impossible.
- **Do not remove logging to reduce noise**; reduce verbosity instead.
- **Errors must not leak** internal detail to users, but must log enough for the operator. Distinguish client-facing and server-side messages.
- **Stop rules:** the fix requires a schema change beyond the plan, the fix breaks a legitimate flow you cannot repair within the item, or you are tempted to disable a check to make a test pass.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Gap test fails pre-fix | run against parent commit | red |
| Gap test passes post-fix | run | green |
| Authorisation matrix | new test | all routes × roles covered |
| Legitimate paths intact | suite + manual check | no regressions |
| No control weakened | diff review | nothing disabled or widened |
| Enforcement matrix updated | re-run P03 matrix for changed routes | gaps closed |
| Secrets rotated (if applicable) | owner confirmation | recorded, no values |
| Rollback defined | per item | present |

## 7. Failure handling

- **Fix breaks a legitimate flow** → revert the item, record the conflict, and return to P05 with the evidence; do not widen permissions to make both pass.
- **Framework cannot enforce at the right layer** → implement at the closest correct boundary, add a test that documents the limitation, and record the architectural item.
- **No test infrastructure** → script the checks; if even that is impossible, document the manual verification performed and mark the finding `fixed, unverified by automation`.
- **Finding cannot be fixed within the plan** (requires redesign) → implement containment (disable route, add gateway rule, reduce privilege) and record the structural work.
- **Time exhausted** → leave completed items green and committed; never leave a half-applied control in place. Record the next item precisely.

## 8. Security and authorisation

Risk class B: repository changes on a branch. No production deploys, no secret values in artifacts or commits, no live exploitation, no disabling of security controls, no changes to external systems. Production rotation and deployment are Category C/D and executed by the owner with the recorded instructions.

## 9. Completion criteria

- [ ] Every approved item implemented or explicitly blocked with evidence.
- [ ] Each has a failing-before/passing-after test, or a documented alternative.
- [ ] Authorisation changes covered by a route × role matrix.
- [ ] Legitimate paths verified.
- [ ] No control weakened (diff reviewed).
- [ ] Enforcement matrix updated for changed entry points.
- [ ] Rotations instructed and recorded without values.
- [ ] `.security/VERIFICATION.md` complete; suite green.

## 10. Deliverables and handover

Artifacts: changes, tests, `.security/VERIFICATION.md`.

Handover: remaining structural items go to `02-engineering/refactoring/` or architecture review; detection items to `04-process/observability-reliability/`; the verification record feeds the next audit cycle (`02-engineering/codebase-audit/` P05).
