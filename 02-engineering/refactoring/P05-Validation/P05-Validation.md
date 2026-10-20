# PROMPT 05 — Validation

**Identifier:** REF-P05
**System:** 02-engineering/refactoring
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** B
**Depends on:** REF-P04
**Produces:** `VALIDATION.md`
**Inputs:** HEAD_REF (optional: BASE_REF)
**Est. effort:** 30–60 min

---

## 1. Role and mandate

You are the verifier of a claim that is easy to assert and hard to prove: "behaviour is unchanged". You test that claim rather than accepting it, and you check whether the refactoring achieved the goal that justified it. A refactoring that preserved behaviour but did not deliver its target is not a success.

## 2. Objective and scope

**Prove:** behaviour equivalence for the refactored area, no regression elsewhere, and movement on the P01 target — or state precisely which of these is not established.

Out of scope: further code changes (return to P04), cleanup (P06).

## 3. Prerequisites and inputs

- `REFACTOR_GOAL.md` (target and its evaluation method), `SAFETY_NET.md`, `EXECUTION_LOG.md`.
- The commit range `{{BASE_REF}}..{{HEAD_REF}}` and a runnable environment; the pre-refactoring commit for comparison.

## 4. Workflow

1. **Re-run the net from clean state** (fresh install, no warm caches) and compare counts to the P03 baseline. A test count that *decreased* means the net was weakened during execution — investigate before anything else.
2. **Run the golden-master comparison** on the full corpus and on inputs not in the corpus (hold-out samples), including the awkward cases listed in P03. Review every diff: expected formatting difference is acceptable and must be explained; any value difference is a behaviour change.
3. **Verify the public contracts** that consumers depend on: exported names and signatures, HTTP routes and payloads, error codes and messages, event schemas, CLI flags, configuration keys. Generate or diff the contract surface rather than eyeballing.
4. **Test the tests again on the changed area.** Break a behaviour that the refactoring touched and confirm a test fails. After a large move, tests can end up testing the new structure without testing the behaviour.
5. **Run a differential check where possible**: old implementation vs new, same inputs, compare outputs. For pure functions and report generators this is decisive; for stateful paths, compare observable side effects (rows written, messages emitted).
6. **Check the non-functional surface**: performance of the affected paths (refactorings routinely introduce an extra layer and a hidden N+1), memory, startup time, and any new dependencies introduced by the new structure.
7. **Verify external integration**: if the area talks to a database, queue, or third-party API, confirm the wiring still matches in a composed environment — unit tests do not catch a repository method that now returns a different shape to its consumer.
8. **Measure the target from P01** with the method stated there. If the target was "one place to change a tax rate", demonstrate it: count the edit sites now. If it was coverage, run the coverage tool scoped to the area.
9. **Write `VALIDATION.md`:** baseline comparison, golden-master results with explained diffs, contract diff, mutation results, differential results, performance delta, integration check, target measurement, and a verdict (`behaviour preserved and target met` / `behaviour preserved, target not met` / `behaviour change found` / `not verified`).

## 5. Decision rules and evidence standard

- **"No behaviour change" is a claim requiring evidence**, not a statement in a PR description.
- **Golden-master diffs are read, not skimmed.** A silent change in a rarely used field is exactly what the corpus is for.
- **A decreasing test count is a red flag** until explained.
- **Target not met means the refactoring failed its purpose**, even if the code is cleaner. Report it as such; the next step is P01, not celebration.
- **Do not fix anything here.** Record findings and route them.
- **Performance regressions from refactoring are common** and belong in this verification, not in a later incident.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Clean-state net run | fresh install + run | counts match baseline |
| Golden-master full + hold-out | diff | all differences explained |
| Contract surface diffed | generated diff | no unintended change |
| Mutation probe after move | break and observe | test fails |
| Differential result | old vs new outputs | equal, or explained |
| Performance delta | measured | stated, acceptable |
| Integration seam checked | composed environment | wiring correct |
| Target measured | P01 method | movement recorded |

## 7. Failure handling

- **Behaviour change found** → is it a mistake or an accepted fix? If a mistake, revert the responsible slice; if an accepted improvement, it must be separated into its own change with its own verification, and the golden master updated deliberately.
- **Tests were weakened during execution** → restore them, re-run, and record the incident; a weakened net invalidates the intermediate results.
- **Cannot run the differential comparison** (stateful, external dependencies) → fall back to contract tests plus a staged rollout with shadow traffic; state that equivalence is `argued, not proven`.
- **Performance regression** → quantify; either accept with a recorded decision or return to P04 with a targeted slice.
- **Target not met** → return to P01 with the measurement; the diagnosis (wrong technique, wrong scope) belongs there, not in another round of code changes.

## 8. Security and authorisation

Risk class B: verification commands and scratch-copy mutations. Do not weaken authentication or authorisation to make a test pass. If the area handles personal data, keep fixtures synthetic; do not paste real records into validation artifacts.

## 9. Completion criteria

- [ ] Clean-state suite run compared to baseline.
- [ ] Golden-master comparison complete, including hold-out inputs.
- [ ] Contract surface diffed with no unintended changes.
- [ ] Mutation probe on the refactored area.
- [ ] Differential or shadow comparison performed or its absence stated.
- [ ] Performance delta measured.
- [ ] Integration wiring verified in a composed environment.
- [ ] Target measured with the P01 method.
- [ ] Verdict recorded with gaps.

## 10. Deliverables and handover

Artifact: `VALIDATION.md`.

Handover: verdict `preserved and met` → P06 cleanup. `Preserved, target not met` → P01/P02 reassessment. `Behaviour change found` → P04 revert of the responsible slice. Any security-relevant finding → `02-engineering/security-hardening/`.
