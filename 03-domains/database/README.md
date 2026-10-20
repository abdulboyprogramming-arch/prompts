# Database Engineering: Schema, Migration & Data Integrity

**Maturity: operational (v1.0.0).** Five stages for changes that can destroy data irreversibly.

**Entry point:** [`P01-Schema/P01-Schema-Truth.md`](P01-Schema/P01-Schema-Truth.md)
**Execution mode:** audit-remediation
**Risk class:** A for analysis, **B** for migration code, **C/D** for any execution against a shared or production database

## Why this system exists

Database changes are the only routine engineering change that can destroy value the code cannot recreate. Yet in this library — and in most teams — they were covered by a paragraph inside release planning ("use expand/contract"). This system makes schema change a first-class procedure:

- What the schema actually is (not what the ORM models claim).
- Whether a migration is compatible with the code currently deployed.
- Whether it has been *proved* on a realistic copy before it touches real data.
- How data written during the change is reconciled.
- How the change is undone if it fails, including when the answer is "it cannot be".

## The four rules this system enforces

1. **Application and schema changes are never coupled in one irreversible step.** Expand → deploy → backfill → verify → contract.
2. **A migration that has not run against a realistic copy is unproven**, regardless of how simple it looks.
3. **Every destructive operation requires a tested restore path** — not a backup that exists, but a restore that has been performed.
4. **Data integrity is verified by queries, not by "the app works".** Row counts, constraints, nullability, orphan checks, and business invariants are checked after the change.

## Stages

| ID | Stage | Purpose | Produces |
|----|-------|---------|----------|
| DB-P01 | [Schema truth](P01-Schema/P01-Schema-Truth.md) | Establish the real schema, drift, constraints, volumes, ownership | `.db/SCHEMA_TRUTH.md` |
| DB-P02 | [Migration design](P02-Design/P02-Migration-Design.md) | Design expand/contract steps and compatibility with running code | `.db/MIGRATION_PLAN.md` |
| DB-P03 | [Pre-flight validation](P03-Preflight/P03-Preflight-Validation.md) | Dry-run, locks, duration, backfill sizing, restore drill | `.db/PREFLIGHT.md` |
| DB-P04 | [Execution & reconciliation](P04-Execution/P04-Execution-Reconciliation.md) | Staged execution, monitoring, abort criteria, data reconciliation | `.db/EXECUTION_LOG.md` |
| DB-P05 | [Rollback & post-verification](P05-Verification/P05-Rollback-Verification.md) | Reverse path, restore drill, post-change integrity verification | `.db/VERIFICATION.md` |

## What "safe" means here

| Situation | Required before execution |
|-----------|---------------------------|
| Add nullable column / new table | Review + dry run |
| Add index | Review of lock behaviour + concurrent creation method |
| Backfill | Batched plan, throttle, idempotency, measured on a copy |
| Add NOT NULL / constraint | Data audit proving no violating rows + validation path |
| Rename / drop column or table | Expand/contract across releases; never in one step with code |
| Change type / precision | Compatibility analysis, copy-based validation, rollback plan |
| Data correction | Written statement of intended state, reversible script, reconciliation query |

## Boundaries

- Deployment sequencing and rollback at release level: `04-process/release-engineering/` (this system supplies the migration facts).
- Query/index performance: `02-engineering/performance/`.
- Backup infrastructure and restore tooling: `03-domains/devops-infra/` (this system requires evidence that restore works).
- ORM/data-access code quality: `02-engineering/codebase-audit/` P04.

## What this system will not do

- Run migrations against production. Execution is Category C/D and belongs to an authorised operator.
- Design your domain model. It audits and plans changes to an existing one.
- Guarantee zero downtime. It quantifies downtime and lock risk so you can decide.

## Known limitations

- Examples are engine-neutral (PostgreSQL/MySQL/SQLite differences are noted where they change the procedure).
- No automated drift detection tooling ships with this system; P01 describes the commands to run.
