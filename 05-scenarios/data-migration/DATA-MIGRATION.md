# Data Migration: move the records, not just the schema

**Identifier:** DATA-MIG-01
**System:** 05-scenarios/data-migration
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** specialised
**Risk class:** C for a copy-and-verify rehearsal; **D** for any write to the source or the cutover of live traffic
**Depends on:** none
**Produces:** `.migration/DATA_MIGRATION_PLAN.md`, `.migration/RECONCILIATION.md`, a rehearsal log
**Inputs:** SOURCE_SYSTEM, TARGET_SYSTEM (optional: FREEZE_WINDOW, APPROVER, TIME_BUDGET)
**Gallery:** Records must move between systems — a new CRM, a rebuilt service, a warehouse, a vendor change — and the plan must survive partial failure without losing or duplicating a row.

---

## 1. Role and mandate

You plan and rehearse the movement of **records** from one system to another.

This is not schema migration (`03-domains/database/` P01–P05 change the shape of a table in place), and it is not host migration (`05-scenarios/platform-migration/` moves a running service). This is moving data whose meaning changes on the way: a user in one schema is an account plus a membership plus a profile in another; a status enum has different values; timestamps have different precision; a denormalised field becomes a join; and three fields in the source have no destination at all.

The failure that matters is not "the job errored". It is **the job succeeded and the data is wrong** — silently truncated strings, lost timezone offsets, duplicated rows from a rerun, orphaned children because parents arrived in a different batch, and a reconciliation step that compared row counts and declared victory.

## 2. Objective and scope

**Produce:** a field-level mapping with transforms and loss decisions, an ordered load plan that tolerates partial failure, a reconciliation method that compares *values* rather than counts, a rehearsal with recorded results, a cutover and rollback procedure, and a post-cutover verification.

Out of scope: schema design for the target (that is the target system's own design work), application code changes beyond what the migration requires, and decommissioning the source (`04-process/decommissioning/`).

## 3. Prerequisites and inputs

- `{{SOURCE_SYSTEM}}` — where the records are, how they can be read (export, replica, API), and whether a consistent snapshot is possible while it is live.
- `{{TARGET_SYSTEM}}` — the destination schema, its constraints, its generated values, and who owns it.
- `{{FREEZE_WINDOW}}` — how long writes can be stopped, if at all. Zero means you need change capture or a dual-write period, which changes the whole design.
- `{{APPROVER}}` — required for the rehearsal against real data and for cutover.
- `{{TIME_BUDGET}}` — how long the planning and rehearsal pass may take. It decides whether you map every entity or start with the highest-risk three, and the plan must say which was chosen.

## 4. Workflow

1. **Inventory the data before mapping it.** Every table/collection/entity, its row count, its growth rate, its size on disk, its largest row, and its foreign-key graph. Find the entities nobody mentions: audit logs, soft-deleted rows, drafts, attachments, join tables, and the settings blob with JSON inside it. A migration that forgets soft-deleted rows loses the ability to restore a user's deleted record.

2. **Map field by field, in a written table**, with five columns: source field, target field, transform, loss, and verification. Every transform is code, not prose. Under **loss**, record explicitly: dropped fields, truncated lengths, reduced precision, collapsed enum values, timezone normalisation, and merged duplicates. Loss is legitimate; undocumented loss is a defect discovered by a customer.

3. **Decide identity before you copy anything.** How is a source record identified in the target? Preserve the source ID (best for reconciliation and support), mint a new one with a mapping table, or derive a deterministic key. Then decide how reruns behave: the load must **upsert on that identity**, never append. This single decision prevents the duplicate-rows failure that survives every count-based check.

4. **Resolve the graph order and the orphan problem.** Parents before children, and either foreign keys deferred or constraints validated after the full load. If the target enforces foreign keys strictly, load in dependency order per batch; if a row's parent is missing, the row must go to a reject file, not be silently skipped.

5. **Design for partial failure from the first line.** The load is resumable: a checkpoint per entity and per batch, an idempotent upsert, and a reject file with the reason. The question to answer before writing code: *if this dies at 60%, what exactly is the state, and how does the next run continue without duplicating the 60%?*

6. **Reconcile on values, not counts.** Counts match when both sides are equally wrong — a truncated string and a dropped timezone offset both preserve the count. Reconcile with:
   - counts per entity, including deleted and filtered rows;
   - a checksum or hash per row over the mapped fields, compared source-to-target;
   - aggregates that would move if a numeric field were altered (sum of amounts, min/max timestamps, distinct enum distributions);
   - a sampled row-by-row diff of at least 100 rows, including the largest, the oldest, the newest, and any row containing nulls;
   - referential integrity queries (no orphans in either direction);
   - and a record of every mismatch with the row's identifier.

7. **Handle the fields that cannot round-trip.** Long text truncated by a target column limit, enums with no equivalent, arrays flattened, money with different precision or currency handling, and timestamps without timezone information (see `02-engineering/time-correctness/`). For each: transform, widen the target, keep the original in a side table, or accept the loss — recorded, with the number of affected rows.

8. **Rehearse against a copy of real data, twice.** The first run finds the bugs; the second proves idempotency and measures the actual duration. Record the duration per entity and the wall-clock time, because that number decides whether the freeze window is viable. Verify the rehearsal with the step-6 method and record the mismatches.

9. **Write the cutover as a sequence with a decision point at each step:** freeze writes (or start change capture) → final delta load → reconcile → switch reads → verify → switch writes → monitor → unfreeze. For each step: the command, the expected result, the abort criterion, and the reverse action. Note the exact point after which rollback stops being possible — usually the first write to the target that the source cannot accept back.

10. **Plan the after-period**: dual-read comparison for a defined window, a reconciliation report on a schedule, a fixed date for freezing the source read-only, and a date for retiring it. Write `.migration/DATA_MIGRATION_PLAN.md` and `.migration/RECONCILIATION.md`, and store the rehearsal log with its numbers.

## 5. Decision rules and evidence standard

- **Upsert on a stable identity.** Append-only loads duplicate on every rerun.
- **Counts are not reconciliation.** Compare values with hashes and aggregates.
- **Every loss is recorded with an affected-row count**, before it happens.
- **Rehearse twice, against real data, and measure the duration.** A migration timed on 1% of the data will not fit the window.
- **Rejects are data, not noise.** Every rejected row has a reason and an owner who resolves it.
- **Foreign keys are validated after the load**, or the order is proven correct — never assumed.
- **A migration is not finished at cutover.** It is finished when dual-read comparison matches for the agreed period.
- **Rollback has an expiry.** Name the moment it stops being possible.
- Mark every reconciliation figure `verified` (query and result) or `inferred`.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Entity inventory | Queries against source | Counts and sizes recorded, including deleted rows |
| Field mapping | Mapping table | Every source field mapped or explicitly dropped |
| Loss register | Mapping table | Each loss has a transform decision and a row count |
| Identity decision | Plan | Stable key, upsert semantics stated |
| Graph order | Load plan | Parents first or constraints deferred |
| Partial failure | Injected mid-run failure | Resume works with no duplicates |
| Rejects | Reject file | Every rejected row has a reason and an owner |
| Reconciliation | Hash/aggregate diff | Zero unexplained mismatches, or each one listed |
| Sample diff | Row-level comparison | ≥100 rows including extremes and nulls |
| Referential integrity | Queries | No orphans in either direction |
| Duration | Rehearsal | Measured against the freeze window |
| Idempotency | Second rehearsal run | Same target state, no duplicates |
| Rollback | Procedure | Steps, expiry point, and reverse actions stated |
| Post-cutover | Dual-read report | Matches for the agreed window |

## 7. Failure handling

- **No consistent snapshot is possible** → use change capture or a dual-write period; record the inconsistency risk and reconcile deltas explicitly.
- **The source cannot be read without affecting production** → read from a replica or a backup, and check replication lag at the moment of the snapshot.
- **The target rejects rows for constraint violations** → reject file plus a resolution owner; do not disable constraints to make the load pass.
- **The rehearsal exceeds the freeze window** → reduce scope (migrate historical data separately), parallelise per entity, or convert to an incremental migration — do not shorten the verification.
- **Reconciliation finds mismatches after cutover** → keep the source writable, fix forward with a targeted re-migration of affected records, and delay retiring the source.
- **Business rules differ between systems** (a status that does not exist in the target) → this is a product decision, not a transform; record the options and route it.
- **A vendor is involved and cannot provide an export with stable IDs** → treat identity as the first blocker and resolve it before anything else.

## 8. Security and authorisation

Rehearsal against a copy is class C. Writing to the source, cutting over live traffic, or deleting data is class **D** and requires `{{APPROVER}}` plus a proven restore path (`05-scenarios/disaster-recovery/`). A migration copy of production data is a second uncontrolled copy of personal data: minimise it, restrict access, and destroy it after verification with evidence (`04-process/privacy-requests/`). Exports that leave the environment follow the same rules as any bulk transfer, including residency (`05-scenarios/data-residency/`).

## 9. Completion criteria

- [ ] Every entity inventoried, including soft-deleted and auxiliary data.
- [ ] Field-by-field mapping with transforms and a loss register.
- [ ] Identity and upsert semantics decided.
- [ ] Graph order resolved or constraints deferred.
- [ ] Resumable load with checkpoints and reject files.
- [ ] Value-level reconciliation method defined and executed in rehearsal.
- [ ] Two rehearsals completed; idempotency demonstrated; duration measured.
- [ ] Cutover sequence with abort criteria and reverse actions.
- [ ] Rollback expiry point identified.
- [ ] Post-cutover dual-read window agreed and scheduled.
- [ ] Source retirement date set.

## 10. Deliverables and handover

Artifacts: `.migration/DATA_MIGRATION_PLAN.md`, `.migration/RECONCILIATION.md`, rehearsal log, reject file with owners, cutover runbook.

Handover: `03-domains/database/` owns schema change inside one system; `05-scenarios/platform-migration/` moves a service without changing its data model; `04-process/decommissioning/` retires the source afterwards. `04-process/privacy-requests/` must know about the copy, and `05-scenarios/disaster-recovery/` must be updated to include the new system in its asset inventory — a migration that adds a system without adding it to the recovery plan creates an unrecoverable tier.
