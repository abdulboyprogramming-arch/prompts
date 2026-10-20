# PROMPT 02 — Backfill and Reconciliation

**Identifier:** DE-P02
**System:** 03-domains/data-engineering
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** C — rewrites historical data that downstream decisions already used
**Depends on:** DE-P01 (tests and contracts exist)
**Produces:** `.backfill/BACKFILL_PLAN.md`, `.backfill/RECONCILIATION.md`
**Inputs:** TARGET_TABLE, DATE_RANGE (optional: DOWNSTREAM_CONSUMERS, APPROVER, WAREHOUSE)
**Est. effort:** 2–5 h plus runtime

---

## 1. Role and mandate

You correct historical data without corrupting the present or silently invalidating decisions that were made on the old numbers.

A backfill is not a re-run. It rewrites inputs that have already produced reports, forecasts, invoices, or model training sets. The technical work is usually easy; the hard part is knowing **what changed, who consumed the old values, and how the correction is communicated**.

## 2. Objective and scope

**Produce:** a scoped backfill plan with a dry run, a reconciliation report proving the new data is correct, a list of affected downstream artefacts, and a rollback position.

Out of scope: changing the transformation logic itself (that is a code change, reviewed separately), and re-training models (owned by `03-domains/data-ml-ai/`).

## 3. Prerequisites and inputs

- `{{TARGET_TABLE}}` and `{{DATE_RANGE}}` — explicit dates and timezone; "last month" is not a range.
- `{{DOWNSTREAM_CONSUMERS}}` — dashboards, reports, exports, models, invoices, and partner feeds that read this table.
- `{{WAREHOUSE}}` — determines partitioning, cost, and whether the write is atomic.
- `{{APPROVER}}` — required: this changes historical facts.

## 4. Workflow

1. **State the defect precisely**: which rows are wrong, why, and from when. A backfill without a defined correctness condition cannot be verified — it becomes "run it and see".

2. **Establish the blast radius before writing anything**: which partitions, how many rows, which downstream tables are derived, which reports were produced in the affected period, and whether any external party received the old numbers (invoices and partner feeds are the ones that cannot be un-sent).

3. **Take a snapshot of the affected partition(s)** — a table copy or an export to cold storage. This is the rollback position and the comparison baseline; without it, "did the backfill help?" has no answer.

4. **Dry-run on a copy at full scale.** Not a 1,000-row sample: the failure modes (skew, partition limits, a join that explodes on a specific date) only appear at volume. Record runtime, bytes scanned, and cost.

5. **Make the write atomic per partition.** A backfill that half-completes leaves a mix of old and new logic that no query can distinguish. Prefer `MERGE`/`INSERT OVERWRITE` per partition, commit per partition, and record which partitions are done.

6. **Reconcile, don't just compare counts.** For each affected period, compare: row counts, sum of the key measures, distinct entity counts, and a sample of specific records traced end to end. A row-count match with different values is the failure this step exists to catch.

7. **Check the derived layer explicitly**: aggregates, materialised views, incremental models, and exports that were built from the old data. A correct base table with a stale aggregate is the most common post-backfill incident.

8. **Handle the "already consumed" reality**: identify reports and decisions that used the old numbers, quantify the change (e.g. "the September revenue figure moves by 0.4%"), and notify the owners. A silent correction is how trust in the data team is lost.

9. **Define the completion and abort conditions before starting**: how many partitions must match, what error rate aborts the run, who watches it, and how to stop it mid-flight.

10. **Write both artifacts**: `BACKFILL_PLAN.md` (defect, scope, snapshot, dry-run results, execution order, abort conditions, communication list) and `RECONCILIATION.md` (per-period comparison, derived-layer verification, deltas, sign-off).

## 5. Decision rules and evidence standard

- **A backfill is a data migration with consumers**, not a job re-run.
- **Snapshot before you write.** No snapshot, no approval.
- **Dry-run at full scale or do not claim the runtime.**
- **Atomic per partition**; a half-applied backfill is indistinguishable from a bug.
- **Reconcile values, not just counts.**
- **Derived data is in scope** — a fixed base table under a stale aggregate is not fixed.
- **Communication is part of the migration**: affected reports named, deltas quantified.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Defect defined | Plan | Correctness condition stated and testable |
| Blast radius mapped | Lineage + consumer list | Downstream tables and reports enumerated |
| Snapshot taken | Storage check | Affected partitions copied and restorable |
| Dry run at scale | Copy run | Runtime, bytes, cost recorded |
| Atomic writes | Execution log | Each partition committed whole |
| Reconciliation | Comparison table | Counts, sums, distincts, and traced records match |
| Derived layer rebuilt | Check each downstream | Aggregates match the new base |
| External consumers handled | Comms record | Invoices/feeds identified, decision recorded |
| Deltas quantified | Report | Percentage or absolute change per affected metric |
| Abort conditions | Plan | Numeric, with a named watcher |
| Rollback tested | Restore from snapshot | Restores the pre-backfill state |

## 7. Failure handling

- **The backfill is bigger than the window** → chunk by partition with a checkpoint, and state which partitions are complete; resumability is part of the plan.
- **Reconciliation shows a mismatch** → stop; compare the new transformation against the old on a single known-correct date to find whether the defect is in the fix or the test.
- **A downstream aggregate is stale** → rebuild it *after* the base is signed off, and verify the derived numbers independently.
- **An invoice or external feed used the old data** → this is a business decision, not a technical one: surface it to the owner with the delta and do not issue corrections unilaterally.
- **The snapshot cannot be restored within the platform's retention** → say so before starting; an unrestorable snapshot is a false sense of safety.
- **The backfill reveals a live bug still writing bad data** → fix the writer first, or the backfill will be undone by tonight's run.
- **Cost exceeds the estimate mid-run** → abort is a valid outcome; report what completed and resume later, per partition.

## 8. Security and authorisation

Risk class C: rewrites historical data. Requires `{{APPROVER}}`, a recorded window, and a snapshot. Backfills that touch tables containing personal data are also privacy-relevant: a "corrected" row may reintroduce data that was deleted under a subject request (`04-process/privacy-requests/` P02). Never copy production data into a personal environment for the dry run; use a warehouse copy with the same access controls.

## 9. Completion criteria

- [ ] Defect and correctness condition stated.
- [ ] Blast radius mapped including derived tables and reports.
- [ ] Snapshot taken and restore verified.
- [ ] Full-scale dry run with runtime and cost recorded.
- [ ] Per-partition atomic writes with a completion record.
- [ ] Reconciliation on counts, sums, distincts, and traced records.
- [ ] Derived layer rebuilt and verified.
- [ ] External consumers identified and the decision recorded.
- [ ] Deltas quantified for affected metrics.
- [ ] Abort conditions and watcher named.
- [ ] `BACKFILL_PLAN.md` and `RECONCILIATION.md` written.

## 10. Deliverables and handover

Artifacts: `.backfill/BACKFILL_PLAN.md`, `.backfill/RECONCILIATION.md`, snapshot reference.

Handover: the data owners of every affected dashboard receive the delta; `03-domains/data-ml-ai/` evaluates whether a trained model must be retrained on corrected data; `04-process/observability-reliability/` P05 records the incident if the defect produced customer-visible numbers; DE-P01 adds the test that would have caught the original defect, because a backfill without a new test is a repeat appointment.
