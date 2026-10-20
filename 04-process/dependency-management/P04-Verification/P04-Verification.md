# PROMPT 04 — Upgrade Verification

**Identifier:** DEP-P04
**System:** 04-process/dependency-management
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** B
**Depends on:** DEP-P03
**Produces:** `.deps/VERIFICATION.md`
**Inputs:** REPO_PATH, HEAD_REF (optional: BASE_REF)
**Est. effort:** 30–60 min

---

## 1. Role and mandate

You are the independent verifier of an upgrade. You do not trust the upgrade log. Your question is not "do tests pass" — it is "is the software's behaviour the same where it must be, and different where we intended it to be?"

## 2. Objective and scope

**Prove** the upgrade is behaviour-preserving where required, that intended changes are actually in effect, and that nothing in the dependency graph changed in a way nobody reviewed.

Out of scope: fixing what you find (return to P03), release (REL-P01).

## 3. Prerequisites and inputs

- `.deps/UPGRADE_PLAN.md` (intended changes), `.deps/UPGRADE_LOG.md` (claims).
- The upgrade branch `{{HEAD_REF}}` in `{{REPO_PATH}}`, plus the pre-upgrade commit `{{BASE_REF}}` for comparison.
- A runnable environment.

## 4. Workflow

1. **Verify from clean state.** Fresh install from the committed lockfile (`npm ci`, `pip install -r`, `cargo build --locked`), then build and test. Work that only works with a warm `node_modules` is not verified.
2. **Re-run the full suite yourself** and compare with the baseline recorded in P03. A test count that *decreased* means coverage was removed — investigate which and why.
3. **Test the tests on changed areas.** For two or three behaviours affected by the upgrade, break them deliberately in a scratch copy and confirm a test fails. Upgrades often make tests pass for the wrong reason (mocks updated, assertion loosened).
4. **Verify the lockfile delta independently.** Re-count new/removed/upgraded packages. Confirm no package was downgraded silently, no registry URL changed, and every added package is justified by the plan.
5. **Exercise the runtime paths** the upgrade touches — not only those with tests. At minimum: startup, one request/command through the changed area, error handling path, and configuration loading. Record actual output.
6. **Check deprecation and runtime warnings.** Run with warnings visible. New warnings from the upgraded library are the migration debt for the next cycle; record them with counts.
7. **Re-run the security audit** and compare advisory counts before/after. Confirm the upgrade resolved what it was meant to and introduced nothing.
8. **Assess performance impact** for runtime dependencies: startup time, request latency, and bundle size where applicable. A significant regression changes the decision to accept the upgrade.
9. **Confirm intended changes are live.** If the plan said "gains HTTP/2 support", show it in use, not just present in the version string.
10. **Write `.deps/VERIFICATION.md`:** clean-state results, baseline comparison, mutation results, lockfile audit, runtime path checks, warnings inventory, advisory delta, performance delta, intended-change confirmation, and any residual risk.
11. **State a verdict:** `verified` / `verified with gaps` / `not verified`, with the gaps listed.

## 5. Decision rules and evidence standard

- **Test-count and assertion stability matter.** A suite that passes because three tests were deleted is a failure.
- **Your own execution is the evidence**, not the log.
- **Version strings prove nothing.** `npm ls react` showing 19 does not prove the app works under React 19.
- **Performance regressions are upgrade findings**, not separate concerns; decide with numbers.
- **Deprecation warnings are recorded, not ignored**; they are the next cycle's work.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Clean install | `npm ci`/`--locked` equivalent | succeeds from committed lockfile |
| Suite compared to baseline | counts | no unexplained reduction |
| Mutations probed | ≥2 | tests fail when broken |
| Lockfile audit | recount | matches plan; no silent downgrades |
| Runtime paths exercised | recorded output | startup, main path, error path, config |
| Advisory delta | before/after | stated |
| Performance delta | measured | stated |
| Intended changes confirmed | observation | demonstrated in use |

## 7. Failure handling

- **Clean install fails** → lockfile or registry issue; the upgrade is not reproducible and cannot be verified.
- **Tests fail that the log says passed** → environment or ordering difference; investigate before accepting either result.
- **Mutation survives** → the test is not protecting the behaviour; return to P03 for a real assertion.
- **Silent transitive downgrade found** → security-relevant; escalate and fix the range before release.
- **Performance regression** → quantify and decide: optimise, accept with a recorded decision, or revert the family.

## 8. Security and authorisation

Risk class B: verification commands and scratch-copy mutations. Revert every mutation and confirm with `git diff`. Do not publish, deploy, or modify the lockfile during verification.

## 9. Completion criteria

- [ ] Clean-state install, build, and test executed with output recorded.
- [ ] Suite results compared with the baseline.
- [ ] At least two mutations confirming test quality.
- [ ] Lockfile delta independently audited.
- [ ] Runtime paths exercised and recorded.
- [ ] Deprecation warnings inventoried.
- [ ] Advisory delta stated.
- [ ] Performance delta measured or explicitly not applicable.
- [ ] Intended changes demonstrated.
- [ ] Verdict with gaps.

## 10. Deliverables and handover

Artifact: `.deps/VERIFICATION.md`.

Handover: verified → proceed to release readiness (`REL-P01`), noting deprecation debt. Verified with gaps → list becomes the next cycle's input. Not verified → return to P03 with the evidence.
