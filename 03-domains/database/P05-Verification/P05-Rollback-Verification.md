# PROMPT 05 — Rollback & Post-Verification

**Identifier:** DB-P05
**System:** 03-domains/database
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** B
**Depends on:** DB-P04
**Produces:** `.db/VERIFICATION.md`
**Inputs:** TARGET_ENV, PREVIOUS_VERSION
**Est. effort:** 30–60 min

---

## 1. Role and mandate

You are the verifier who decides whether the migration actually achieved its purpose without damaging anything, and you are the owner of the reverse path. Data damage often appears days later — in reports, in reconciliation jobs, in rows nobody looked at during the window.

## 2. Objective and scope

**Prove** the post-migration state is correct and stable, that the application behaves correctly against it, and that the reverse path remains executable (or is honestly documented as unavailable).

Out of scope: re-running the migration (P04), designing follow-up changes (P02).

## 3. Prerequisites and inputs

- `.db/EXECUTION_LOG.md` and `.db/RECONCILIATION.md`.
- `.db/PREFLIGHT.md` (expected state, invariants, drill results).
- The application version deployed against the new schema (`{{PREVIOUS_VERSION}}` is the rollback target) on `{{TARGET_ENV}}`.

## 4. Workflow

1. **Verify structural intent.** Every intended DDL change is present; no unintended changes exist (diff the live schema against the plan). Unexpected tables, dropped indexes, or altered defaults indicate someone else changed the database.
2. **Verify data integrity with queries, not observation:**
   - row counts per table versus pre-change plus expected writes,
   - null counts on columns that should be populated,
   - duplicate detection on intended-unique columns,
   - orphan checks across foreign keys,
   - business invariants (sums, balances, per-state counts) against expected values,
   - sample reads of records written before, during, and after the change window.
3. **Verify application behaviour** on the paths that use the changed objects: create, read, update, delete, plus one report/aggregate query. Record actual results.
4. **Verify the reverse path** still works: if the plan called for a rollback script, dry-run it on a copy of the *current* state (not the pre-change copy) and measure what would be lost. State whether rollback remains possible, and until when.
5. **Watch the slow signals** over the following days: background jobs, reports, reconciliation tasks, and error rates on affected queries. Schedule and record the follow-up check rather than declaring success immediately.
6. **Assess performance impact** of the change: query plans for the key access paths, index usage, and latency of the top queries touching the changed objects.
7. **Confirm the contract step's readiness** (dropping the old shape): is there evidence no consumer uses the old columns? Telemetry, code search, and log analysis — record the evidence, and set the earliest date for contraction.
8. **Write `.db/VERIFICATION.md`:** structural diff, integrity results with query outputs, application checks, reverse-path status and any data-loss bound, slow-signal plan, performance findings, contract readiness evidence, and residual risks.
9. **Update the ledger and close the stage.**

## 5. Decision rules and evidence standard

- **Query output is the evidence.** Paste the queries and their results (counts and aggregates, never row contents with PII).
- **Row counts alone can hide corruption.** A table with the right count can still have swapped or truncated values; use invariants and samples.
- **Rollback availability decays.** State explicitly how long the reverse path remains valid (backup retention, new writes after the point of no return).
- **Do not declare success on day zero.** Name the follow-up check, its date, and what would constitute failure.
- **Contraction requires negative evidence**, not absence of complaints: code search plus telemetry showing zero reads/writes on the old shape.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Structural diff matches plan | live schema vs plan | no unexplained objects |
| Invariants match expectation | queries + expected values | within stated tolerance |
| Sample reads across window | records from before/during/after | correct values |
| Application paths exercised | manual or automated checks | recorded results |
| Reverse path status stated | dry-run on current state | possible (with bound) or unavailable |
| Slow signals scheduled | date + criterion | recorded |
| Contract evidence | code search + telemetry | zero use demonstrated |

## 7. Failure handling

- **Invariant mismatch** → stop, quantify the discrepancy, identify affected rows, and decide between targeted repair (validated script) and restore. Record either way; do not "monitor and hope".
- **Unexpected structural change found** → treat as a configuration-drift incident; identify who/what changed it before making further adjustments.
- **Rollback no longer possible** → record the point of no return and date; ensure the owner knows the change is now forward-only.
- **Performance regression** → route to `02-engineering/performance/` with the measured plans; do not add indexes ad hoc without a design step.
- **Contract evidence inconclusive** → do not contract; set a new evidence date.

## 8. Security and authorisation

Risk class B: read-only verification, plus dry-runs on copies. Do not restore production data over a live system without authorisation. Do not include personal data in verification artifacts.

## 9. Completion criteria

- [ ] Structural diff verified against plan.
- [ ] Integrity queries executed with results recorded.
- [ ] Application paths exercised and recorded.
- [ ] Reverse path status stated with its expiry bound.
- [ ] Follow-up checks scheduled with failure criteria.
- [ ] Performance impact assessed.
- [ ] Contract readiness evidenced or deferred.
- [ ] Residual risks stated.

## 10. Deliverables and handover

Artifact: `.db/VERIFICATION.md`.

Handover: the contract step (if any) becomes a scheduled change for a later release, tracked in `.db/MIGRATION_PLAN.md`; performance findings route to `02-engineering/performance/`; the verification record feeds the next `03-domains/database/` change and any audit.
