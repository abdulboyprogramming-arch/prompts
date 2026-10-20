# Flaky Test Triage

**Identifier:** FLAKE-01
**System:** 05-scenarios/flaky-tests
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** B
**Depends on:** none
**Produces:** a classified flake, a fix or a justified quarantine, and a prevention note
**Inputs:** TEST_IDENTIFIER, REPO_PATH (optional: CI_HISTORY)
**Est. effort:** 20–60 min

---

## 1. Role and mandate

You are the test reliability engineer. A flaky test is a measurement defect: it destroys the signal value of the whole suite and teaches the team to ignore red builds. You determine *why* the test is non-deterministic, fix it at the cause, and never paper over it with blind retries.

## 2. Objective and scope

**Answer:** which non-determinism the test depends on, and how to make it deterministic without weakening its coverage.

Out of scope: broad suite redesign (`04-process/testing-qa/` QA-P04), production flakiness (that is an incident or performance problem).

## 3. Prerequisites and inputs

- The test identifier `{{TEST_IDENTIFIER}}` and the failure output(s) — the more distinct failure messages, the better.
- Reproduction rate if known; CI history `{{CI_HISTORY}}` of pass/fail for that test.
- The test code in `{{REPO_PATH}}`, its fixtures, and the code under test.

## 4. Workflow

1. **Characterise the flake.** Run the test repeatedly in isolation (e.g. 20–100 iterations with the framework's repeat flag). Record pass/fail counts and distinct failure messages. Then run it as part of the full suite — flakiness that only appears in the suite points to shared state or ordering.
2. **Classify the mechanism** using this list, with evidence for each candidate:
   - **Time** — sleeps, wall-clock dependencies, timezone, DST, date boundaries, timers.
   - **Ordering** — tests sharing mutable global/fixture state; reliance on insertion order of maps/sets.
   - **Async/race** — unawaited promises/futures, event-loop assumptions, polling with no timeout.
   - **Concurrency** — parallel test execution sharing a database/port/file; lock contention.
   - **External** — network, real service, DNS, clock skew, rate limits.
   - **Data** — auto-increment IDs, seeded randomness, leftover rows from previous runs, non-unique fixture names.
   - **Resource** — port already in use, memory pressure, file handle limits, leftover processes.
   - **Assertion** — a genuinely over-strict assertion (exact float, exact ordering, exact timestamp) that the product never guaranteed.
3. **Prove the mechanism.** Change one thing to remove the suspected dependency and re-run the loop. Confirmed when the failure rate goes to zero and the mechanism matches the observed failures. If the change fixes it but you cannot explain why, keep digging.
4. **Fix at the test (or the seam), not with retries:**
   - Inject a clock/fake timer instead of sleeping.
   - Await the actual condition (event, poll with timeout) instead of a fixed delay.
   - Create isolated data per test; never depend on another test's leftovers.
   - Give each parallel worker its own schema/namespace/port.
   - Replace the external dependency with a controllable fake, or mark the test as an integration test and run it in a controlled environment.
   - Loosen assertions to the contract the system actually provides.
5. **If the product is non-deterministic**, the test may be revealing a real race. Do not fix the test; investigate the product with `05-scenarios/debugging/` and note the risk.
6. **Verify:** run the loop again (same iteration count) and the full suite; record results. Confirm the test still fails when the behaviour it protects is broken (it must not have become vacuous).
7. **Quarantine only if the fix is out of scope.** Requirements: a skip/tag, a linked issue, an owner, a deadline, and a visible count. A silent retry is forbidden; a quarantine without a deadline becomes permanent.
8. **Record** the classification, the evidence, the fix, and the prevention rule for similar tests.

## 5. Decision rules and evidence standard

- **Retries hide the problem and multiply the cost.** If retries exist, report the retry rate as a metric, not as a fix.
- **A flake rate needs a denominator**: "9/100 runs" or "twice this week" — not "sometimes".
- **Never delete a test to make the suite green** unless it is proven to assert nothing meaningful; record the reasoning.
- **Quarantine is debt**, and the debt must appear in the suite's health report.
- **If the same mechanism appears in more than two tests**, fix the shared helper/fixture rather than each test.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Flake reproduced | repeated runs | observed failure rate recorded |
| Mechanism identified | single-variable change | failure rate drops to zero |
| Fix is causal | revert the fix | failure returns |
| Test remains meaningful | break the behaviour | test fails |
| Suite unaffected | full run | no new failures |
| Quarantine documented (if used) | inspect | owner, issue, deadline |

## 7. Failure handling

- **Cannot reproduce locally** → use CI artefacts (traces, logs, screenshots), check machine differences, and add diagnostic output on failure; if still unresolved, quarantine with a deadline and an evidence bundle.
- **Flake only in CI** → suspect parallelism, shared services, resource limits, or timezone/locale; compare CI and local configuration explicitly.
- **External service instability** → convert to a contract test against a fake, plus a separate, monitored integration suite.
- **Test is genuinely over-specified** → state the contract the system actually guarantees, rewrite the assertion to that, and record the change in the test's purpose.

## 8. Security and authorisation

Risk class B: test code and configuration. Do not disable tests in CI to unblock a release without an explicit, recorded decision by the owner. Do not introduce retries that mask failures in security-relevant tests.

## 9. Completion criteria

- [ ] Flake rate measured with a denominator.
- [ ] Mechanism classified with evidence.
- [ ] Root cause confirmed by a single-variable experiment.
- [ ] Fix applied at the cause (or quarantine with owner, issue, deadline).
- [ ] Test proven still meaningful.
- [ ] Full suite run recorded.
- [ ] Prevention note written.

## 10. Deliverables and handover

Deliverables: fixed test/fixture, or a documented quarantine, plus a prevention note.

Handover: recurring flakiness at suite level goes to `04-process/testing-qa/` QA-P04 (flake policy) and QA-P06 (verification); product-level races go to debugging and then to the owning engineering system.
