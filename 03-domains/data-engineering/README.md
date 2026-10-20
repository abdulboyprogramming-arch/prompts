# Data Engineering

**Maturity: operational (v1.0.0).** Two stages for pipelines whose failures are silent.

**Entry point:** [`P01-Pipelines/P01-Pipeline-Reliability.md`](P01-Pipelines/P01-Pipeline-Reliability.md)
**Execution mode:** audit-remediation
**Per stage:** audit-remediation (P01, class B), implementation (P02, class C)
**Identifiers:** `DE-P01..P02`

## Why this system exists

`03-domains/data-ml-ai/` treats data as a stage on the way to a model. That framing hides the discipline that runs the warehouse: ingestion contracts, freshness, idempotent loads, backfills, and reconciliation. When a pipeline breaks it does not throw — it writes an empty partition and every dashboard keeps rendering.

The coverage matrix has carried "data engineering: **Missing** — `data-ml-ai` conflates pipelines with modelling" since 2.9.0. This system is the correction, and `data-ml-ai` now points here for everything upstream of feature engineering.

## Stages

| ID | Stage | Purpose | Produces |
|----|-------|---------|----------|
| DE-P01 | [Pipeline reliability](P01-Pipelines/P01-Pipeline-Reliability.md) | Inventory, seven failure modes, data tests, freshness/volume contracts, tested alerts | `.data/PIPELINE_AUDIT.md` |
| DE-P02 | [Backfill & reconciliation](P02-Backfills/P02-Backfill-Reconciliation.md) | Full-scale dry run, atomic per-partition writes, value-level reconciliation, consumer notification | `.backfill/BACKFILL_PLAN.md`, `RECONCILIATION.md` |

## The rules

1. **Success is not data** — assert on the output, never on the task status.
2. **Every load is idempotent**; retries are guaranteed.
3. **Volume anomalies are failures** — a 90% drop is not a quiet day.
4. **Contracts beat tribal knowledge**: cadence, bounds, lateness, written and tested.
5. **A backfill is a migration with consumers**, not a re-run.
6. **Snapshot before you write.**
7. **Reconcile values, not counts.**
8. **Derived data is in scope** — a fixed base table under a stale aggregate is not fixed.

## Proportionality

| Situation | Run |
|-----------|-----|
| A dashboard is wrong or empty | DE-P01 (tests and freshness first) |
| Adding a new source | DE-P01 inventory + contract |
| Historical data is wrong | DE-P02 |
| After any backfill | DE-P01 adds the test that would have caught it |
| Model accuracy dropped | `03-domains/data-ml-ai/`, but check DE-P01 contracts first |

## Boundaries

- Modelling, features, evaluation: `03-domains/data-ml-ai/`.
- Schema migrations and correction scripts in an operational database: `03-domains/database/`.
- Warehouse cost: `03-domains/cost-engineering/`.
- Deletion and retention obligations: `04-process/privacy-requests/`.

## What this system will not do

- Make a bad source trustworthy — it makes the badness visible on arrival.
- Replace a data quality platform; it specifies what to assert and why, which is the part tools do not supply.
- Own BI semantics — metric definitions belong to the business owner, and the pipeline only proves they are computed as stated.
