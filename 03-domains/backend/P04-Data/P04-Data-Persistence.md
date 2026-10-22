# PROMPT 4 — Data & Persistence: the migration that runs while the old code is still serving

**Identifier:** BE-P04
**System:** 03-domains/backend
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B — writes migration and schema files; reversible only if planned
**Depends on:** BE-P03
**Produces:** `BE_DATA.md`: the model, the migration plan in expand/contract form, index justification, consistency and retention rules, and the rollback for each step
**Inputs:** {{PROJECT_PATH}} (optional: DATA_CLASSIFICATION, RETENTION_POLICY)
**Est. effort:** 1–3 h

---

## 1. Role and mandate

You change stored data without taking the service down and without making rollback
impossible. A schema change is not a file; it is a sequence of states that old code, new
code, and the migration process all have to survive at the same time.

You implement the schema and the migration. You do not write feature logic (`BE-P05`)
and you do not choose the storage engine without the constraints in `BE_ARCHITECTURE.md`
(`BE-P03`), whose transaction boundaries this stage may not widen.

## 2. Objective and scope

**Produce:** `BE_DATA.md` containing:

1. **Model.** Entities, keys, relationships, and the invariants the database itself
   enforces rather than trusting application code to.
2. **Migration plan.** Every change as expand → backfill → switch → contract, with the
   code version that must be deployed at each step.
3. **Reverse path.** For each step, the statement or deploy that undoes it, and whether
   the undo loses data.
4. **Indexes.** Each one named with the query it serves, and the write cost it adds.
5. **Consistency.** Which reads must see their own writes, which may be stale, and how
   the isolation level supports that.
6. **Retention and deletion.** What is kept, for how long, on what authority, and how a
   deletion request is satisfied across backups.
7. **Volume and growth.** Current row counts, growth rate, and the size at which the
   current access pattern stops working.

Out of scope: endpoint shapes (`BE-P02`), module boundaries (`BE-P03`), runtime retry
behaviour (`BE-P06`).

## 3. Prerequisites and inputs

- `{{PROJECT_PATH}}` — where migrations, models and queries live. **Discovered here:**
  the migration tool in use, the existing migration history, and the current schema.
- `{{DATA_CLASSIFICATION}}` (optional) — from `BE_CONTEXT.md`. If absent, read it from
  that artifact; a schema change creating a new personal-data column without a stated
  classification is incomplete.
- `{{RETENTION_POLICY}}` (optional) — the organisation's rule. If absent, record the
  requirement as `unstated` and raise it as an open question rather than inventing one.

## 4. Workflow

1. **Write the invariants first.** Which facts must be true of the data at all times —
   an invoice total equals its lines, a subscription has at most one active period. Then
   decide which are enforced by constraints and which by code, and say why for each.
   Anything left to code is a place a bug can write bad rows.
2. **Enumerate the migration as states, not statements.** For each change: what the old
   code does when the new column exists but is null, what the new code does when it is
   absent, and what happens if the deploy rolls back mid-way.
3. **Use expand/contract for every column change.** Add nullable, backfill in batches,
   dual-write, then enforce. Never add a `NOT NULL` column with no default to a live
   table, and never rename in one step.
4. **Size the backfill before running it.** Row count, batch size, time per batch,
   lock behaviour, and what else slows down while it runs. If the estimate exceeds the
   maintenance window, say so and split the work.
5. **Justify each index with a query.** Name the query from `BE-P02` or `BE-P03` it
   serves and the write amplification it costs. An index with no query is a tax.
6. **Set the retention rule per table**, with its authority: legal, contractual,
   product, or none. For a new personal-data column, state the deletion path including
   backups.
7. **Check consistency against the caller's expectation** from `BE-P01`. A caller that
   reads its own write within the same request needs read-your-writes, and a replica read
   will break it.
8. **Test the migration on a copy** before proposing it: forward, then back, on restored
   data, with the row count before and after recorded.

## 5. Decision rules and evidence standard

- **Destructive steps are separate deploys.** Dropping a column, dropping a table and
  rewriting data are their own change, after the code that reads them is gone.
- **A migration without a reverse is a one-way door.** If it cannot be reversed without
  loss, it needs a backup taken immediately before, the restore tested, and that fact
  recorded in the plan.
- **Batch large updates.** An unbounded `UPDATE` on a production table takes locks and
  rewrites the table; the batch size is a number, not "small".
- **Constraints belong in the database when they are invariants.** Uniqueness, foreign
  keys, and non-null are invariants; "the API validates it" is not a constraint.
- **Soft delete is a decision with a cost.** It preserves data nobody queries and breaks
  every uniqueness constraint. Choose it only with the reason and the purge job.
- **Money is integer minor units; time is UTC stored with its timezone type.** Both are
  already decided in `BE-P02`; the schema must not contradict it.

## 6. Verification

- Every invariant is listed and assigned to a database constraint or to code with reason.
- Each change is a sequence of states, each with the deploy that accompanies it.
- Each step has a reverse, and any lossy reverse is flagged with its backup.
- Backfill has row count, batch size, estimated duration and lock behaviour.
- Every index names a query and states its write cost.
- Retention is stated per table with its authority; deletion covers backups.
- The migration has been run forward and back on a restored copy, with counts recorded.
- Read-your-writes requirements are checked against the chosen consistency model.

## 7. Failure handling

- **The backfill will not finish inside the window.** Split by key range across several
  deploys, keep the column nullable longer, and dual-write meanwhile. Record the extra
  deploys.
- **The database cannot enforce the invariant** (cross-shard, or a legacy engine without
  checks): move the check to a single writer or a periodic verifier, and record the
  window in which bad rows can exist.
- **There is no migration framework.** Do not invent a bespoke one mid-task. Write an
  idempotent script with a recorded applied-version table, and flag adopting a standard
  tool as a follow-up.
- **A restore has never been tested.** Say so, and require one before any lossy step.
  The plan may proceed only with the risk written down and accepted by the owner.
- **Data classification is unknown for a new column.** Stop and ask; do not add a column
  whose retention nobody has decided. This is the one place in the system where
  "we can fix it later" is usually false.

## 8. Security and authorisation

Risk class B. Do not run migrations against production from this prompt, and do not
copy production data into a development environment to test — restore an anonymised or
synthetic copy. Migration scripts must not contain credentials; connection details come
from the environment. Any column holding personal or sensitive data is named as such in
the model, not discovered later during an audit.

## 9. Completion criteria

- [ ] Model with keys, relationships and invariants, each assigned to a mechanism.
- [ ] Migration as expand → backfill → switch → contract, with the deploy per step.
- [ ] Reverse path per step, with lossy reverses backed by a tested restore.
- [ ] Backfill estimate with batches, duration and lock behaviour.
- [ ] Every index justified by a query and its write cost.
- [ ] Retention per table with authority, and deletion including backups.
- [ ] Forward and back run on a copy, with row counts recorded.

## 10. Deliverables and handover

`BE_DATA.md`, the migration files, and the model. `BE-P05` needs the model and the
enforced invariants so handlers do not duplicate or contradict them. `BE-P06` needs the
lock behaviour and the failure modes of the backfill. `BE-P07` needs the forward and
back migration tests, and the row counts, as regression evidence.
