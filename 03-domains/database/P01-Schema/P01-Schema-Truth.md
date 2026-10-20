# PROMPT 01 — Schema Truth

**Identifier:** DB-P01
**System:** 03-domains/database
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A
**Depends on:** none (entry stage)
**Produces:** `.db/SCHEMA_TRUTH.md`, `.db/DB_LEDGER.md`
**Est. effort:** 30–60 min

---

## 1. Role and mandate

You are the database engineer establishing what the schema actually is before anyone changes it. Model definitions, migrations, and live databases drift apart; a change built on the wrong model of reality is how data gets lost. You do not design or execute anything here.

## 2. Objective and scope

**Answer:** what tables, columns, constraints, indexes, and relationships exist; how do code models, migration history, and declarations disagree; what are the volumes; and what is irreversible today?

Out of scope: designing the change (P02), running migrations (P04).

## 3. Prerequisites and inputs

| Input | Source | If missing |
|-------|--------|------------|
| Migration directory and ORM models | repository | locate by convention and state the assumption |
| Schema dump or read-only database access | repository or owner | analyse migrations statically and mark conclusions `unverified against live DB` |
| Row counts / volume estimates | owner or metrics | classify as unknown; this changes P03 planning |
| Environment topology (single DB, replicas, shards) | owner | assume single primary and record the assumption |

## 4. Workflow

1. **Inventory the artifacts:** migration files (tool, ordering, applied history table), ORM models, raw SQL, seed/fixture data, and any schema documentation.
2. **Establish the declared schema** from migrations applied in order. Identify the latest migration and whether the history is linear (no branches, no edits after apply, no duplicate timestamps).
3. **Compare with the code's model.** For every model/entity: does a matching table exist? Do column names, nullability, types, defaults, and relations match? List drifts with both references — this is the most valuable output of the stage.
4. **Compare with the live schema** where read-only access exists: columns, types, nullability, defaults, constraints, indexes, foreign keys, triggers, views, extensions. Record precisely how it was queried.
5. **Map data ownership and lifecycle:** which service writes each table, retention policy, soft-delete columns, audit tables, and tables that look abandoned. Unreferenced tables are candidates for P02 review, not deletion.
6. **Find irreversible or dangerous constructs:** columns with data that cannot be regenerated, unique constraints whose violation would fail a migration, foreign keys without `ON DELETE` policy, cascading deletes, triggers with side effects, and any migration that has already dropped something.
7. **Record volumes and growth** per table (exact counts where cheap, estimates otherwise) because they determine migration duration and lock risk in P03.
8. **Check the operational surface:** connection configuration, migration runner permissions (does it run as owner or superuser?), whether migrations run automatically on deploy, and whether the app can start against a schema one version behind.
9. **Write `.db/SCHEMA_TRUTH.md`:** artifact inventory, declared schema summary, drift tables (code↔migrations, migrations↔live), ownership and retention, irreversible constructs, volumes, runner mechanics, and unknown/unverified items.
10. **Initialise `.db/DB_LEDGER.md`.**

## 5. Decision rules and evidence standard

- **Live schema beats migrations; migrations beat models.** When they disagree, record all three and state which you trust and why.
- **Never infer a constraint from application validation.** Application-level checks are not database constraints, and a change that assumes they are will corrupt data.
- **Do not test by writing.** No DDL, no sample inserts, no `EXPLAIN ANALYZE` on production queries. Read-only inspection only.
- **Row counts must be measured or marked unknown**, never guessed.
- **Report drift without fixing it.** Schema drift is a finding for P02 to resolve deliberately.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Migration history linear | inspect ordering | no branches or duplicate timestamps |
| Drift claims cited | inspect | model path + migration/live evidence |
| Live schema method recorded | inspect | query or dump command stated |
| Volumes measured or unknown | inspect | no invented numbers |
| No writes performed | audit of commands | read-only only |
| Irreversible constructs listed | inspect | non-empty where applicable |

## 7. Failure handling

- **No live access** → static analysis only; label all live-schema conclusions `unverified` and list the exact read-only queries the owner should run.
- **Migration history inconsistent** (edited files, missing entries, out-of-order) → stop and record it as a blocking finding; designing a new migration on a corrupted history multiplies risk.
- **Multiple databases/services** → produce the truth per database and note cross-database consistency assumptions.
- **Unknown volumes** → state that durations and lock risk cannot be estimated, and require measurement in P03 before execution.
- **Schema managed outside migrations** (manual DDL, platform-managed) → record the mechanism and treat drift as expected; the change procedure must match reality.

## 8. Security and authorisation

Risk class A. Use read-only credentials. Do not export table contents, do not sample PII, and do not print connection strings. If a secret appears in configuration, record its location only.

## 9. Completion criteria

- [ ] Migration and model inventory complete.
- [ ] Declared schema established; history linearity checked.
- [ ] Code↔schema drift documented with references.
- [ ] Live schema compared or explicitly marked unverified.
- [ ] Ownership, retention, and abandoned tables noted.
- [ ] Irreversible constructs listed.
- [ ] Volumes measured or marked unknown.
- [ ] Runner mechanics and startup compatibility recorded.
- [ ] Ledger initialised.

## 10. Deliverables and handover

Artifact: `.db/SCHEMA_TRUTH.md`.

P02 receives: the true schema, drift list, irreversible constructs, volumes, and runner mechanics — all of which constrain the migration design.
