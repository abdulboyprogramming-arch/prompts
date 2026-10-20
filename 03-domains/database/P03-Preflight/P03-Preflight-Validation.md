# PROMPT 03 — Pre-Flight Validation

**Identifier:** DB-P03
**System:** 03-domains/database
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** B
**Depends on:** DB-P02
**Produces:** `.db/PREFLIGHT.md`
**Inputs:** PREFLIGHT_ENV (optional: DATABASE_ACCESS)
**Est. effort:** 45–120 min

---

## 1. Role and mandate

You are the migration validator. Your job is to make the plan fail here rather than in production. You run the migration against a realistic copy, measure what it actually does, and confirm that the restore path works. A migration that has never been executed is a hypothesis.

## 2. Objective and scope

**Prove:** the statements execute cleanly, in the expected duration, with the expected locking, producing the expected data state — and that you can get back.

Out of scope: executing against the real environment (P04).

## 3. Prerequisites and inputs

- `.db/MIGRATION_PLAN.md` (statements, backfill design).
- A **staging copy** in `{{PREFLIGHT_ENV}}` with realistic data volume, reachable via `{{DATABASE_ACCESS}}`. Without volume, timing is meaningless and the drill proves nothing about duration.
- Permission to create and drop throwaway databases locally or in staging.

## 4. Workflow

1. **Build a representative copy.** Restore from a recent backup into staging, or generate a dataset whose row counts match production within an order of magnitude for every affected table. Record how the copy was produced and how it differs from production (this difference is a risk to state).
2. **Snapshot before.** Record row counts per affected table, constraint counts, index list, and a checksum or sampled hash of key business invariants (e.g. sum of balances, count of orders per state).
3. **Execute the full sequence** exactly as written — no improvisation, no skipped statements. Record per-statement wall-clock time and any error verbatim.
4. **Measure locking and blocking.** For each DDL statement, determine whether it takes an exclusive lock and for how long. Where the engine supports it, run under a concurrent write load and observe blocked queries; record the longest observed block. This is the number that decides whether the change needs a window.
5. **Run the backfill** with the designed batch size and throttle. Record: total duration, rows per second, time per batch, whether progress is resumable (kill it deliberately at ~50% and resume), and whether the completion query reports the true state.
6. **Validate data state after the run.** Compare row counts, constraint validation results, orphan checks, and business invariants against the pre-snapshot. Any unexpected difference is a stop-the-line finding.
7. **Run the rollback.** Execute the reverse path or restore from the pre-change snapshot. Confirm: how long it took, whether data written after the migration survives, and what would be lost in a real rollback. If rollback relies on a backup, perform an actual restore drill and record the duration.
8. **Test the compatibility claim.** Start the *currently deployed* application version against the migrated schema and run its smoke tests. If it fails, the expand phase is not safe and the plan returns to P02.
9. **Estimate production differences.** Volumes, replication lag, connection pool pressure, and concurrent traffic will differ. State the multiplier you expect and the margin.
10. **Write `.db/PREFLIGHT.md`:** copy provenance and deviations, per-statement timing, lock/block measurements, backfill throughput and resume evidence, post-state comparison, rollback drill results, old-code compatibility result, production projections, and the go/no-go recommendation with conditions.
11. **Update the ledger.**

## 5. Decision rules and evidence standard

- **Timing from a small dataset is fiction.** If only a small copy is available, state that duration is unknown and require either a larger copy or a maintenance window sized for the worst case.
- **A restore that has not been performed is not a rollback plan.** Perform it, record the duration, or classify the migration as forward-fix-only.
- **Death mid-backfill is the default assumption**, so resumability must be demonstrated, not designed.
- **Blocking measurement beats theory.** Documentation about lock modes is not a substitute for observing a blocked query.
- **Do not "fix" the plan silently.** If a statement fails or is slow, stop and return to P02 with the measurement.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Copy is representative | row-count comparison | within stated tolerance |
| Statements executed verbatim | command log | no edits |
| Lock behaviour measured | concurrent-load observation | longest block recorded |
| Backfill resumable | kill + resume | completes correctly |
| Post-state matches expectation | invariant comparison | no unexplained differences |
| Rollback or restore drill | executed | duration recorded |
| Old code runs on new schema | smoke tests | pass, or expand phase rejected |
| go/no-go stated | inspect | explicit with conditions |

## 7. Failure handling

- **No staging copy available** → do not proceed to execution; deliver the plan with `preflight not performed` as a blocking risk, and recommend the smallest viable drill (restore one table subset).
- **Migration exceeds the acceptable window** → return to P02 with the measurement; consider batching DDL, online schema change tools, or a maintenance window.
- **Backfill cannot be resumed** → redesign the batching key and progress tracking before any execution.
- **Old code breaks on new schema** → the expand phase is wrong; split it further.
- **Restore drill fails** → the migration is unsafe to run; escalate immediately. A backup you cannot restore is not a backup.

## 8. Security and authorisation

Risk class B: throwaway databases, local or staging only. Never run the drill against production or a shared staging database used by others without explicit authorisation. Never copy production data containing PII without the owner's approval; prefer anonymised or generated data at the same volume.

## 9. Completion criteria

- [ ] Representative copy built with provenance and deviations recorded.
- [ ] Pre-snapshot captured (counts, constraints, invariants).
- [ ] All statements executed verbatim with per-statement timing.
- [ ] Lock/block behaviour measured.
- [ ] Backfill throughput and resume demonstrated.
- [ ] Post-state compared; differences explained.
- [ ] Rollback or restore drill executed with duration.
- [ ] Old-code compatibility tested.
- [ ] Production projection and margin stated.
- [ ] Explicit go/no-go with conditions.

## 10. Deliverables and handover

Artifact: `.db/PREFLIGHT.md`.

P04 receives: validated statements, measured durations, lock windows, abort criteria derived from the measurements, and the rollback procedure that was actually performed.
