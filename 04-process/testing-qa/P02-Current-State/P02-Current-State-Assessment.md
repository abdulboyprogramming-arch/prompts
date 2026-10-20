# PROMPT 02 — Current Test State Assessment

**Identifier:** QA-P02
**System:** 04-process/testing-qa
**Version:** 1.1.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** B
**Depends on:** QA-P01
**Produces:** `.qa/CURRENT_STATE.md`
**Inputs:** REPO_PATH, BASE_REF
**Est. effort:** 30–60 min

---

## 1. Role and mandate

You are the test suite auditor. You measure what exists, how it behaves when run, and what it actually protects — with the risk map from P01 as the lens. You do not write or fix tests here.

## 2. Objective and scope

**Answer:** what tests exist, do they pass, are they trustworthy, how fast are they, and which R1 behaviours are unprotected?

Out of scope: deciding what to do about it (P03/P04), modifying tests (P05).

## 3. Prerequisites and inputs

- `.qa/QA_CONTEXT.md` (risk map, constraints).
- `{{REPO_PATH}}` at a known commit `{{BASE_REF}}`; run commands only if non-destructive.

## 4. Workflow

1. **Inventory.** Count tests by level (unit/integration/e2e/contract/manual) and by area. Identify frameworks, config files, fixtures, factories, and helpers. Note test-to-source ratio and any test directories excluded from CI.
2. **Run the suite.** Record: command, wall-clock duration, passed/failed/skipped counts, failure names (not full logs), and whether failures are pre-existing on the target commit. If it cannot run, record the precise blocking reason.
3. **Map R1 behaviours to tests.** For each R1 behaviour from P01, find the test(s) that would fail if the behaviour broke. Classify: `covered` (a specific test fails when broken), `incidental` (some test touches it but would not fail), `uncovered`. Cite test file:line.
4. **Probe test quality on a sample.** For five tests spanning levels, ask: would this fail if the implementation were subtly wrong? Look for assertion-free tests, over-mocking, snapshot-only assertions, and tests that assert mocks rather than behaviour.
5. **Measure reliability signals.** Re-run the suite twice if cheap and compare results. Search for sleeps, retries, `skip`/`xit`, `|| true`, ordering dependencies, shared global state, time-dependent assertions, and network calls in unit tests.
6. **Measure feedback latency.** Time to run unit tests, integration tests, and the full PR pipeline. Compare against the P01 constraint.
7. **Check enforcement.** Does CI run the tests on PRs? Are failures blocking? Which branch protections exist? Are some suites manual-only?
8. **Record coverage reality.** If instrumentation exists, report numbers per critical module — never repo-wide only. If not, say `no instrumentation` and do not estimate.
9. **Write `.qa/CURRENT_STATE.md`:** inventory table, suite run results, R1 coverage map, quality-sample findings, reliability signals, latency vs target, CI enforcement, coverage reality, and coverage limits of this assessment.
10. **Update the ledger.**

## 5. Decision rules and evidence standard

- **`covered` requires a demonstration.** Either the test names the behaviour and asserts it, or you ran a deliberate mutation to confirm red. Otherwise it is `incidental`.
- **A passing suite that skips R1 paths is not "healthy"** — say so explicitly, with the uncovered list.
- **Do not count assertion-free or skipped tests as coverage.**
- **Timing numbers must be measured**, not estimated from file counts.
- Pre-existing failures are recorded as the baseline, not hidden; a suite that is already red cannot detect regressions and that is an R1-level process finding in P03.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Suite run reproducible | record command and counts | re-run matches (or divergence is reported) |
| R1 map complete | compare with P01 risk map | every R1 behaviour classified |
| `covered` claims justified | inspect citation or mutation note | test would fail if behaviour broke |
| Latency measured | timing recorded with method | not estimated |
| CI enforcement verified | workflow files cited | explicit |
| Coverage numbers sourced | tool output present or `unknown` | no invented figures |

## 7. Failure handling

- **Suite cannot run** (missing services, secrets, native toolchain) → record the blocker, run the subset that does run, and mark the assessment partial. This blocker is itself a finding.
- **Suite hangs** → set a timeout, report the hang, and identify which test/test group hangs using `--fail-fast` or per-file runs.
- **Thousands of tests** → inventory counts by area, run a representative subset plus all R1-related tests, and state the sampling.
- **No tests at all** → report `no automated tests`, map all R1 behaviours to `uncovered`, and proceed directly to P03/P04.

## 8. Security and authorisation

Risk class B, artifacts only. Do not run tests that hit production, send email/SMS, charge cards, or mutate shared data. If tests require credentials, do not supply them; record the requirement and run without.

## 9. Completion criteria

- [ ] Inventory by level and area with counts.
- [ ] Suite executed with command, duration, and counts recorded (or blocker stated).
- [ ] Every R1 behaviour classified covered/incidental/uncovered with evidence.
- [ ] Five-test quality sample assessed.
- [ ] Reliability signals documented.
- [ ] Feedback latency measured against the P01 target.
- [ ] CI enforcement verified from config.
- [ ] Coverage reality stated honestly.

## 10. Deliverables and handover

Artifact: `.qa/CURRENT_STATE.md`.

P03 receives: the R1 coverage map, reliability signals, latency data, and the sampled quality findings.
