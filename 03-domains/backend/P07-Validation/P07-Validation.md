# PROMPT 7 — Validation: evidence that the contract holds, not a green build

**Identifier:** BE-P07
**System:** 03-domains/backend
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** C — runs tests and load against a controlled environment; writes only the report
**Depends on:** BE-P06
**Produces:** `BE_VALIDATION.md`: every check with its command, its actual result, its evidence, and the residual risk that remains after it
**Inputs:** {{PROJECT_PATH}} (optional: CI_COMMAND, ENVIRONMENT})
**Est. effort:** 1–3 h

---

## 1. Role and mandate

You decide whether this service is fit to deploy, and you produce evidence rather than
opinion. A green unit suite proves the logic compiles and the happy paths run; it does
not prove that the migration rolls back, that the caller's timeout is met under load, or
that a dependency failing gives the caller the promised error.

You run checks. You do not fix code (`BE-P05`) or tune runtime behaviour (`BE-P06`) —
you send findings back with the reproduction.

## 2. Objective and scope

**Produce:** `BE_VALIDATION.md` with:

1. **Evidence table.** Check, command, environment, result, artifact path. Nothing marked
   passed without an artifact that shows it.
2. **Contract conformance.** Every operation from `BE_API_DESIGN.md` exercised against
   its documented success and each documented error.
3. **Migration safety.** Forward, backward, and the data invariants after each.
4. **Failure behaviour.** Each row of `BE_RELIABILITY.md`'s failure table, exercised by fault
   injection, or marked `not injectable` with the reason.
5. **Load and limits.** Latency against the caller budget, behaviour at the rate limit
   and at the connection pool ceiling.
6. **Security checks.** Authorisation per operation, tenant isolation, input limits,
   secret leakage in logs.
7. **Residual risk.** What remains unverified, with the reason and the impact.

Out of scope: the fix. A failing check goes back to the stage that owns it.

## 3. Prerequisites and inputs

- `{{PROJECT_PATH}}` — the implementation and its tests.
- `{{CI_COMMAND}}` (optional) — the project's suite command. If absent, discover it from
  the repository's workflow or task runner; if there is none, say so and run the tests
  the way their runner is documented.
- `{{ENVIRONMENT}}` (optional) — where the checks run. Local, ephemeral container, or a
  staging environment. Production is not an option for load tests.

## 4. Workflow

1. **Establish the baseline first.** Run the suite on the base commit and record the
   result. Without it, every later failure is ambiguous: pre-existing or introduced.
2. **Walk the contract, not the code.** One row per operation, one per documented error
   code. A code in the taxonomy with no test is an untested promise.
3. **Test the migrations for real.** Apply forward on a restored copy, check the
   invariants, apply the reverse, check them again, compare row counts. A migration whose
   down path was never run is a hope.
4. **Inject the failures.** Kill the dependency, delay it past its timeout, return 500,
   return a malformed body, deliver the same message twice. Each must produce the
   behaviour `BE_RELIABILITY.md` claims. Where injection is impossible, write
   `not injectable in this environment` and treat the claim as unverified.
5. **Load to the promised numbers.** At the caller's budget, at the rate limit, and at
   twice the expected peak. Record p50, p95, p99 and the error rate. If the harness is
   synthetic, say so; a benchmark against a mock is not a latency proof.
6. **Check the security surface.** For each operation: unauthenticated, wrong tenant,
   insufficient scope, oversized body, and a log inspection for tokens and personal data.
7. **Re-run the suite after any fix lands**, and keep both results. Replace nothing.
8. **Write the residual risk.** The honest list — untested failure modes, environment
   differences, single-machine measurements — with impact and what would close it.

## 5. Decision rules and evidence standard

- **A check without an artifact is a claim, not evidence.** Paste the command and its
  tail, or link the file.
- **The word "passing" is reserved for checks that ran.** A skipped test is `not run`,
  a blocked environment is `blocked`, and neither counts toward readiness.
- **Load numbers are only meaningful with the environment.** One machine, a local
  network and a mock dependency is a regression signal, not a capacity proof.
- **A duplicate delivered twice is the default condition of every queue.** If dedupe is
  claimed and untested, it is unverified.
- **Never weaken a check to reach green.** If an assertion is wrong, write the finding
  and let its owner change the specification deliberately.
- **Residual risk is required, not optional.** A report with no residual risk has either
  tested everything (rare) or stopped looking.

## 6. Verification

- The baseline result on the base commit is recorded.
- Every operation and every documented error code has a check with its artifact.
- Migrations ran forward and back with invariant checks and row counts.
- Each failure-table row is either exercised or marked `not injectable`, with reason.
- Latency is reported at p50/p95/p99 against the caller budget, with the harness named.
- Authorisation, tenant isolation and log redaction are checked per operation.
- The suite was re-run after fixes, and both results are present.
- Residual risk lists every unverified claim with its impact.

## 7. Failure handling

- **The test environment cannot host real dependencies** (no containers, no network):
  mark integration and fault-injection checks `blocked`, list exactly which failure
  modes are therefore unverified, and do not report the service as validated. Say what
  would unblock it.
- **The suite is too slow to run.** Record the time, run the full suite once for the
  release, and mark the subset used for iteration. Do not silently narrow coverage.
- **A check fails intermittently.** Do not retry until green. Record both outcomes, treat
  it as a flake with a defect ticket, and note that a flaky check is not evidence either
  way.
- **A migration cannot be reversed** (by design, lossy): require the tested restore and
  record the restore's evidence as the reverse path. Mark the step irreversible.
- **The contract and the code disagree** during conformance testing: that is a finding
  against `BE-P05`, with the operation, the expected code and the observed one. Do not
  adjust the contract to match the code without the design owner's decision.

## 8. Security and authorisation

Risk class C. Run destructive checks only against an environment designated for them —
never production, never a shared staging database that another team depends on. Test
credentials are scoped, short-lived fakes. Load tests name their target host in the
report so nobody repeats one against the wrong environment. If a check finds a live
secret in a log or a repository file, report its location and type only; do not paste it.

## 9. Completion criteria

- [ ] Baseline recorded.
- [ ] Every operation and documented error code checked, with artifacts.
- [ ] Migration forward, backward, invariants and counts.
- [ ] Failure table exercised or marked not injectable with reason.
- [ ] Latency against the caller budget, harness and environment named.
- [ ] Security checks per operation, including log redaction.
- [ ] Suite re-run after fixes, both results kept.
- [ ] Residual risk with impact and the check that would close it.

## 10. Deliverables and handover

`BE_VALIDATION.md` and the artifacts it cites. A deploy decision follows from it: ship,
ship with named risk, or do not ship — with the reason. Anything marked `blocked` or
`not injectable` is inherited by the release record, and by the on-call runbook, as a
thing to watch rather than a thing that was solved.
