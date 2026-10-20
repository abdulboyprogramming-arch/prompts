# PROMPT 04 — End-to-End Acceptance

**Identifier:** FC-P04
**System:** 02-engineering/feature-completion
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** B
**Depends on:** FC-P03
**Produces:** `.feature/ACCEPTANCE.md`, verdict
**Inputs:** TARGET_ENV (optional: TEST_ACCOUNTS)
**Est. effort:** 30–45 min

---

## 1. Role and mandate

You are the acceptance reviewer who did not write this feature. You execute the contract's acceptance statements for every role and every state, from a clean state, and you grade the result honestly. The feature is done when the evidence says so, not when the implementation log says so.

## 2. Objective and scope

**Prove** each acceptance statement from `.feature/COMPLETION_CONTRACT.md`, including the negative and edge cases, and identify what remains unverified.

Out of scope: fixing what you find (return to P03), release decisions (REL-P01).

## 3. Prerequisites and inputs

- `.feature/COMPLETION_CONTRACT.md`, `.feature/LAYER_MAP.md`, `.feature/IMPLEMENTATION_LOG.md`.
- A clean environment `{{TARGET_ENV}}` with the feature branch applied; test accounts for each role (`{{TEST_ACCOUNTS}}`).

## 4. Workflow

1. **Set up from clean state.** Fresh install, build, migrate, seed. Record commands. If setup requires manual steps not in the docs, that is itself a documentation finding.
2. **Create the evidence accounts.** One per role in the contract (anonymous, member, other tenant, admin). Do not test authorisation using the admin's session for other roles.
3. **Walk the acceptance matrix**, cell by cell. For each: perform the action, record the observed result verbatim (response code, UI text, database row, log line, job execution). Mark `pass`, `fail`, or `unverified` with the reason.
4. **Hunt the classic omissions explicitly**, even if not in the contract:
   - direct URL/endpoint access by a lower-privileged role (bypassing the UI),
   - object-level access with another tenant's identifier,
   - double submission / retry (idempotency),
   - the record after a restart (persistence),
   - the empty and error states,
   - the side effects actually firing (notification, audit entry, job).
5. **Check the volume case** if the contract declared one: seed realistic volume and confirm the list/query remains acceptable, and that pagination or limits behave.
6. **Verify failure behaviour:** stop a dependency (or simulate its timeout) and confirm the feature degrades as specified rather than hanging or corrupting data.
7. **Inspect the diff for undeclared changes.** Anything outside the feature's layers is reported.
8. **Grade:** `accepted` (all contract statements pass, negative cases pass, no undeclared changes), `accepted with gaps` (specific statements unverified or failing cosmetically), or `not accepted` (a blocking statement fails). Never round up.
9. **Write `.feature/ACCEPTANCE.md`:** environment, matrix results, omission hunt results, volume and failure results, diff audit, grade with justification, and the gaps list.

## 5. Decision rules and evidence standard

- **Observed, not inferred.** Every pass cites a recorded observation.
- **Test as the role, not about the role.** Authorisation claims require an actual request with that role's credentials.
- **A UI that hides a control is not authorisation.** Direct access is mandatory.
- **`unverified` is an honest outcome**; `pass` without evidence is not.
- **Cosmetic failures do not block acceptance**, but they are recorded and assigned.
- **Do not fix anything during acceptance.** A verification that edits code becomes a self-assessment.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Clean setup | recorded commands | succeeds from repository state |
| Every matrix cell resolved | inspect | pass/fail/unverified, none blank |
| Negative cases executed | per role | denials observed |
| Side effects observed | logs/rows/jobs | fired |
| Volume case tested | seeded data | acceptable performance |
| Failure behaviour tested | dependency disabled | degrades as specified |
| Diff audited | file list | no undeclared changes |
| Grade justified | read as sceptic | matches evidence |

## 7. Failure handling

- **Cannot create role accounts** → mark those cells `unverified` and state the security implication explicitly; do not accept the feature on the admin's word.
- **Environment cannot run the feature** → static acceptance only for that layer; grade cannot exceed `accepted with gaps`.
- **Blocking statement fails** → `not accepted`; provide the reproduction to P03.
- **Undeclared changes found** → report with file list; acceptance is conditional on their justification.
- **Side effect fires twice** → record as a blocking failure (idempotency), not a cosmetic issue.

## 8. Security and authorisation

Risk class B: local/test environments and read-only production observation only if authorised. Do not probe production for authorisation bypasses. Do not include personal data or secrets in the acceptance artifact.

## 9. Completion criteria

- [ ] Clean-state setup recorded.
- [ ] Every acceptance matrix cell resolved with evidence.
- [ ] Omission hunt completed (direct access, object-level, double submit, restart, empty/error, side effects).
- [ ] Volume case tested or explicitly not applicable.
- [ ] Failure behaviour verified.
- [ ] Diff audited for undeclared changes.
- [ ] Grade assigned with justification.
- [ ] Gaps listed with owners or next steps.

## 10. Deliverables and handover

Artifact: `.feature/ACCEPTANCE.md`.

Handover: accepted → ready for release readiness (`REL-P01`). Accepted with gaps → the gap list becomes the next task; it may merge if gaps are cosmetic and recorded. Not accepted → return to P03 with the reproduction. For high-stakes features, pair with `07-workflows/independent-verification.md`.
