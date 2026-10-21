# PROMPT 03 — Safety Net

**Identifier:** REF-P03
**System:** 02-engineering/refactoring
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B
**Depends on:** REF-P02
**Produces:** `SAFETY_NET.md`, tests and characterisation artifacts
**Inputs:** REPO_PATH (optional: PRODUCTION_DATA_SOURCE)
**Est. effort:** 1–4 hours

---

## 1. Role and mandate

You are the engineer building the net that catches mistakes during structural change. Refactoring is the one activity where you deliberately move code without changing behaviour, so your only defence is a test suite that actually detects when behaviour changes. Most suites do not: they cover the happy path of the parts someone cared about when they were written.

## 2. Objective and scope

**Produce** a safety net sufficient for the slices in the strategy: characterisation tests of current behaviour (including the odd parts), contract tests at seams, and a demonstrated ability to detect breakage in the area being changed.

Out of scope: restructuring the code (P04), improving the tests' style, fixing bugs the tests reveal.

## 3. Prerequisites and inputs

- `REFACTOR_STRATEGY.md` (slices, seams, verification per slice).
- A runnable environment for `{{REPO_PATH}}`; the current test suite and how long it takes.
- Access to historical inputs/outputs if the system has them (`{{PRODUCTION_DATA_SOURCE}}`: logs, fixtures, sample data) — the best characterisation data is real.

## 4. Workflow

1. **Establish the baseline.** Run the suite, record pass/fail counts and duration, and — critically — note which parts of the target area are *uncovered*. Coverage measured on the area, not on the repository: repository-wide percentages hide the fact that the code being moved has none.
2. **Write characterisation tests**, not wishful tests. A characterisation test asserts what the code *does now*, including behaviour that looks wrong. If current behaviour is a bug, record it as a bug and assert the current behaviour anyway — the refactoring must not fix it accidentally.
3. **Cover the awkward inputs**, because that is where equivalence breaks: empty collections, null/missing fields, duplicate keys, unicode and locale, time zones and DST, boundary values, very large inputs, error paths, and concurrent access where relevant.
4. **Build golden-master / approval tests** for output-heavy areas: capture current outputs for a representative input corpus, store them, and diff after each slice. This is the cheapest way to prove equivalence across a large surface.
5. **Add contract tests at the seams** identified in P02: the exact input/output shapes that callers depend on, including error contracts. These survive the refactoring and protect consumers.
6. **Prove the net catches breakage — this is the step that is skipped.** For each important test, break the behaviour deliberately in a scratch copy (return a wrong value, drop a field, change an error code) and confirm the test fails. A test that passes against broken code is decoration. Restore and confirm with `git diff`.
7. **Add the behavioural observation you cannot unit-test**: metrics, structured logs, or a shadow comparison that will show whether the new path behaves like the old one after deployment (feeds P05).
8. **Record wall-clock time and flakiness.** A slow or flaky net will be disabled during the refactoring — the moment it is most needed. Quarantine or speed up before proceeding, and switch to `05-scenarios/flaky-tests/` when the flake rate exceeds one in twenty runs.
9. **Write `SAFETY_NET.md`:** baseline results, coverage of the area, tests added by category, mutation results per important test, golden-master corpus and how to regenerate it, runtime behaviour observations, known gaps, and a go/no-go for P04.

## 5. Decision rules and evidence standard

- **Characterise what exists; do not improve it.** Changing behaviour while creating the net destroys its value as a baseline.
- **A net that has not been mutation-tested is an assumption.** Demonstrate failure.
- **Coverage of the area is the metric**, not global coverage.
- **If the net cannot be built in reasonable time, the refactoring is not ready.** Say so; proceeding without a net converts a refactoring into an unverified rewrite.
- **Speed matters.** A suite that takes 40 minutes will be skipped under deadline pressure; optimise the inner loop (subset runner, parallelisation, fixtures) before starting.
- **Test data must not include production personal data.** Use synthetic or redacted corpora.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Baseline recorded | run suite | counts and duration |
| Area coverage known | coverage tool scoped to area | number recorded, gaps listed |
| Characterisation covers awkward inputs | inspect | checklist addressed |
| Golden-master corpus exists | regenerate and compare | identical output |
| Contract tests at seams | inspect | shapes and errors covered |
| Mutation probe on key tests | deliberately break | test fails, then restored |
| Suite speed acceptable | timed run | fits the change loop |
| No production personal data | inspect fixtures | synthetic or redacted |

## 7. Failure handling

- **No test framework or tests at all** → build the smallest harness that can execute the code path (script + assertions), and rely on golden-master tests; record the elevated risk and recommend a narrower first slice.
- **Behaviour is non-deterministic** (time, randomness, ordering) → inject the clock/randomness or capture a fixed seed; if impossible, record the limitation and verify with statistical comparison in P05.
- **Area requires external services** → use recorded fixtures or a contract-level fake; document exactly what is real and what is simulated.
- **Mutation probe passes** (tests do not catch the break) → the net is insufficient; extend it before proceeding. This is a stop condition, not a warning.
- **The net reveals existing bugs** → record them in the ledger, keep the characterisation assertion, and route to debugging after the refactoring; do not fix inside the net.

## 8. Security and authorisation

Risk class B: tests and fixtures in the repository. Never copy production data containing personal data into fixtures. Do not add tests that perform real external side effects (sending email, charging cards) — use fakes or sandbox credentials, and record the choice.

## 9. Completion criteria

- [ ] Baseline suite results and duration recorded.
- [ ] Area coverage measured with gaps listed.
- [ ] Characterisation tests written, including awkward inputs.
- [ ] Golden-master corpus captured where output-heavy.
- [ ] Contract tests at every seam.
- [ ] Mutation probes executed for important tests, with results.
- [ ] Post-deploy observation mechanism defined.
- [ ] Suite fast enough to be run constantly.
- [ ] Explicit go/no-go for execution.

## 10. Deliverables and handover

Artifacts: `SAFETY_NET.md`, the tests, the golden corpus.

P04 receives: a net that has been demonstrated to catch breakage, the exact commands to run it, and the list of behaviours it does not cover (which P04 must handle manually).
