# PROMPT 02 — Migration Design

**Identifier:** DB-P02
**System:** 03-domains/database
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** A
**Depends on:** DB-P01
**Produces:** `.db/MIGRATION_PLAN.md`
**Inputs:** MIGRATIONS_DIR (optional: CHANGE_WINDOW)
**Est. effort:** 45–90 min

---

## 1. Role and mandate

You are the migration architect. You design a sequence in which **old and new application code can both run against the evolving schema**, so that a deploy, a rollback, or an instance restart at any moment does not corrupt data. You do not execute anything.

## 2. Objective and scope

**Produce** a phased migration design (expand → migrate → contract) with compatibility analysis, backfill strategy, and explicit irreversibility decisions.

Out of scope: dry-running it (P03), executing it (P04), verifying afterwards (P05).

## 3. Prerequisites and inputs

- `.db/SCHEMA_TRUTH.md` (real schema, drift, volumes, irreversibility).
- The application change that motivates the migration, and the deployment strategy from `04-process/release-engineering/` if available.
- Constraints: acceptable downtime, maintenance window `{{CHANGE_WINDOW}}`, replication topology, ORM/query patterns, and the migrations directory `{{MIGRATIONS_DIR}}`.

## 4. Workflow

1. **State the target schema and the reason.** What must change and which application behaviour requires it. If the change exists only to tidy the schema, say so — cosmetic migrations carry real risk for no product value.
2. **Build the compatibility matrix.** For each phase: can the *currently deployed* code run against the *new* schema? Can the *new* code run against the *old* schema (needed for rollback)? Answer explicitly, per table/column. Any "no" forces an expand/contract phase.
3. **Design the phases:**

   | Phase | Contents | Deployed code compatible |
   |-------|----------|--------------------------|
   | 1 Expand | Add nullable columns/tables/indexes; no removals; dual-write if required | Old code unaffected |
   | 2 Migrate | Backfill in batches; dual-read or dual-write as needed | Old and new both work |
   | 3 Switch | Deploy code that reads/writes the new shape; keep old shape written if rollback must remain possible | New code primary |
   | 4 Contract | Remove old columns/constraints/indexes in a later release, only after telemetry shows no use | New code only |

4. **Design the backfill.** Batching key and size, idempotency, resumability, throttle, how progress is tracked, how concurrent writes during the backfill are handled (trigger, dual-write, or reconciliation pass), and the query used to measure completion.
5. **Choose index creation strategy per engine.** Note where creation takes a blocking lock and the non-blocking alternative (e.g. `CREATE INDEX CONCURRENTLY` on PostgreSQL, online DDL/algorithm=INPLACE on MySQL). State the engine assumption.
6. **Handle constraint introduction.** Adding NOT NULL, unique, or foreign keys requires: an audit query proving no violating rows, a plan for existing violations, and the validation method (`NOT VALID` + `VALIDATE CONSTRAINT` where supported). Never assume the data is clean.
7. **Handle type changes and renames.** Prefer add-new + backfill + switch + drop-old over in-place alteration. Renames break old code unless a view or compatibility layer exists.
8. **Define the destructive step explicitly.** Any `DROP`, `TRUNCATE`, or data-rewriting `UPDATE` gets: what is lost, whether it is recoverable, the restore procedure required, and a separate approval. If the answer is "not recoverable", say so in capitals in the plan and in the deployment record.
9. **Define abort points.** After which phase can the change stop safely? What is the state if the process dies mid-backfill? What does resuming require?
10. **Write `.db/MIGRATION_PLAN.md`:** target and rationale, compatibility matrix, phased steps with exact DDL/SQL, backfill design, constraint plan, index strategy, destructive-step register, abort/resume points, required approvals, and the rollback direction for each phase.
11. **Update the ledger.**

## 5. Decision rules and evidence standard

- **Never combine "add and use" in one irreversible step.** The test is whether deployed code would break during the window between the schema change and the code change.
- **Every DDL statement must appear verbatim in the plan**, not paraphrased. Reviewers approve statements, not intentions.
- **Backfills must be idempotent and resumable.** Assume the process will be killed at 60%.
- **Constraints are validated against data, not against wishes.** Include the audit query and its expected result.
- **If rollback requires restoring a backup, the migration is not "reversible"** — classify it as forward-fix-only and require explicit acceptance.
- **Prefer the smallest change that satisfies the requirement.** Dropping an unused column can wait.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Compatibility matrix complete | inspect per phase | old/new code answers for every affected object |
| DDL verbatim | inspect | copy-pasteable statements |
| Backfill resumable | inspect design | batching + progress + resume steps |
| Constraint audits present | inspect | query + expected zero rows |
| Destructive register complete | inspect | loss description + restore requirement |
| Abort points defined | inspect | state at each stop point |
| Rollback per phase | inspect | direction stated or forward-fix-only recorded |

## 7. Failure handling

- **Change cannot be made compatible** → the plan requires a maintenance window; state the downtime, the freeze mechanism, and the restore point. Escalate the decision to the owner.
- **Data already violates the intended constraint** → include a remediation step (clean, coalesce, quarantine) before validation, and record the business decision if rows must be deleted.
- **Unknown volumes** → design conservative batching and require measurement in P03 before execution.
- **Multiple services share the table** → the compatibility matrix must include every consumer; identify them or explicitly mark the gap as blocking.
- **Change is really a data model redesign** → stop and route to architecture review; a migration plan cannot fix a modelling error.

## 8. Security and authorisation

Risk class A. Design only. No DDL execution, no writes, no production access. The plan must state which statements are Category C/D when executed and who must approve them.

## 9. Completion criteria

- [ ] Target schema and rationale stated.
- [ ] Compatibility matrix complete for every phase.
- [ ] Phased steps with verbatim DDL.
- [ ] Backfill design: batching, idempotency, resume, measurement.
- [ ] Index and constraint strategies with engine-specific notes.
- [ ] Destructive-step register with recoverability.
- [ ] Abort and resume points defined.
- [ ] Rollback direction per phase; forward-fix-only cases labelled.
- [ ] Approvals identified.

## 10. Deliverables and handover

Artifact: `.db/MIGRATION_PLAN.md`.

P03 receives: the statements, the backfill design, and the volumes needed to prove duration, lock behaviour, and correctness on a realistic copy.
