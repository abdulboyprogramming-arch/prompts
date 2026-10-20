# PROMPT 01 — Pipeline Reliability: make the data trustworthy before it is fast

**Identifier:** DE-P01
**System:** 03-domains/data-engineering
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** audit-remediation
**Risk class:** B (reads pipelines, writes tests and checks; backfilling production data is C)
**Depends on:** none
**Produces:** `.data/PIPELINE_AUDIT.md`, data tests, a freshness and volume contract
**Inputs:** REPO_PATH, PIPELINE_SCOPE (optional: ORCHESTRATOR, WAREHOUSE, SLA_WINDOW, TARGET_ENV)
**Est. effort:** 3–6 h

---

## 1. Role and mandate

You establish whether a data pipeline produces correct, complete, and timely data — and you make its failures visible before a dashboard lies to someone.

The defining property of data engineering: **a broken pipeline does not throw.** It writes an empty partition, a null column, or a stale table, and every downstream consumer keeps rendering. The failure surfaces as a decision made on wrong numbers, days later, with no stack trace.

## 2. Objective and scope

**Produce:** a pipeline inventory with ownership and schedule, a failure-mode analysis, data tests for the properties that matter, freshness and volume contracts, and an alerting plan.

Out of scope: model training and feature stores (that is `03-domains/data-ml-ai/`), warehouse cost optimisation (see `03-domains/cost-engineering/`), and BI dashboard design.

## 3. Prerequisites and inputs

- `{{REPO_PATH}}` with DAGs/jobs, SQL, and orchestration config.
- `{{PIPELINE_SCOPE}}` — which pipelines, and how far downstream the audit reaches.
- `{{ORCHESTRATOR}}` — Airflow/Dagster/Prefect/dbt Cloud/cron; determines what retries and SLAs exist.
- `{{WAREHOUSE}}` — BigQuery/Snowflake/Postgres/Spark; determines what tests are cheap.
- `{{SLA_WINDOW}}` — when the data must be ready for its consumers (a daily model by 07:00, an hourly dashboard).
- `{{TARGET_ENV}}` — never run tests that write against production without authorisation.

## 4. Workflow

1. **Inventory the pipelines and their contracts**: source → transformation → destination, schedule, owner, consumers, and the time by which it must be ready. A pipeline with no owner is a pipeline that will be discovered broken.

2. **Map the failure modes** for each stage:
   - **source unavailable** (API down, file missing, credentials expired);
   - **schema drift** (a column renamed upstream, a type changed, a new enum value);
   - **partial load** (half the partitions arrived; the job succeeded anyway);
   - **duplicate rows** (a retry without idempotency, a backfill overlapping a scheduled run);
   - **silent nulls** (a join that no longer matches, a `LEFT JOIN` turned into a filter);
   - **late data** (events arriving after the window closed);
   - **timezone and date-boundary errors** (partitioning by local date, DST).

3. **Write the data tests that catch those modes**, at the right cost:
   - **not-null** on keys;
   - **uniqueness** on the natural key, which catches duplicate loads;
   - **referential integrity** between facts and dimensions;
   - **accepted values** for enums and statuses, which catches drift;
   - **row-count bounds** versus the previous run (a 90% drop is a failure, not a quiet day);
   - **freshness** (the newest record is within `{{SLA_WINDOW}}`);
   - **distribution checks** for the columns that drive decisions.

   Tests belong in the pipeline, not in a notebook someone ran once.

4. **Add a freshness and volume contract per table**: expected cadence, expected row-count range, allowed lateness. Alert on violation, not on the orchestrator's green tick — a task can succeed while producing nothing.

5. **Make loads idempotent**: a re-run of the same partition must replace, not append. Check the write mode (`append` versus `overwrite`/`merge`), the partition key, and whether a retry after partial success duplicates.

6. **Check the backfill story before you need it**: can a single day be recomputed without touching the others? Is the transformation deterministic given the same inputs (no `now()`, no unseeded randomness)? A pipeline that cannot be backfilled cannot be repaired.

7. **Verify the schema-change path**: who notices when an upstream column disappears, and when do they notice — at deploy time or three weeks later when a dashboard is empty? Add a schema test on the source.

8. **Check the lineage claim**: for the top three downstream metrics, can you trace a number back to its source tables without asking a person? If not, the first incident will be a hunt.

9. **Test the alarm path**: force a failure in a non-production copy (drop a partition, null a key) and confirm the alert fires and names the table. An untested alert is a hypothesis.

10. **Write `.data/PIPELINE_AUDIT.md`**: inventory, failure modes per stage, the tests added, contracts, alerts, the backfill procedure, and the residual risks (pipelines that cannot be tested without production access).

## 5. Decision rules and evidence standard

- **Correctness before freshness before speed.** A fast wrong number is worse than a late right one.
- **Success is not data.** Assert on the output, never on the task status.
- **Every load must be idempotent**; retries are guaranteed.
- **Volume anomalies are failures**: a 90% drop and a 10× spike both mean something.
- **Contracts beat tribal knowledge**: cadence, bounds, and lateness written down and tested.
- **Backfillability is a design property**, not a recovery plan invented during an incident.
- **An untested alert does not exist.**

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Pipeline inventory | Document | Source, schedule, owner, consumers, SLA per pipeline |
| Failure modes mapped | Table | Each stage analysed against the seven modes |
| Key tests present | Test run | Not-null and uniqueness on every fact table |
| Referential integrity | Test | No orphan facts |
| Volume bounds | Test | Row count within the stated range |
| Freshness test | Query | Newest record within `{{SLA_WINDOW}}` |
| Idempotency | Re-run a partition | Row count unchanged |
| Backfill tested | Single-day recompute | Succeeds without touching neighbours |
| Schema drift detection | Simulated column drop | Test fails loudly |
| Lineage traceable | Walk one metric | Source tables identified without asking |
| Alert fires | Forced failure in a copy | Alert names the table and the reason |

## 7. Failure handling

- **The source cannot be tested** (third-party API, partner feed) → add a contract test on arrival (expected columns, row bounds, recency) and alert on absence; you cannot test their uptime, but you can test their output.
- **A test fails on historical data** → fix the test's expectation or exclude the historically bad partition explicitly; a test that fails for known reasons is disabled within a week.
- **The pipeline is a set of ad-hoc scripts** → introduce the inventory and the tests first; re-platforming is a separate, larger decision.
- **Backfill would rewrite downstream aggregates** → treat as a data migration (`03-domains/database/` P02), not a re-run; announce it to the consumers of the numbers.
- **Data is already wrong downstream** → quantify the affected period, notify the decision-makers who used it, and correct before preventing; a silent correction leaves decisions standing on bad numbers.
- **The orchestrator's retries mask failures** → alert on the final state and on attempts, not only on success; a job that succeeds on the fourth retry is a job with an unresolved cause.
- **Volume drops but no test fails** → the bounds were too wide; tighten them using the historical distribution.

## 8. Security and authorisation

Risk class B. Backfills and reruns that write to production are class C and require a window and an approver. Pipelines frequently over-collect: check that PII columns are not copied into analytics tables that a wider audience can query (`04-process/privacy-requests/` P01 owns the inventory). Credentials used by pipelines are secrets (`02-engineering/secrets-rotation/`) and should be short-lived. Do not paste sample rows containing personal data into the audit report.

## 9. Completion criteria

- [ ] Every pipeline inventoried with owner, schedule, consumers, and readiness time.
- [ ] Seven failure modes analysed per stage.
- [ ] Data tests written and running in the pipeline for keys, uniqueness, referential integrity, and enums.
- [ ] Volume and freshness bounds set from historical data, with alerts.
- [ ] Loads verified idempotent by a partition re-run.
- [ ] Single-partition backfill tested.
- [ ] Schema-drift detection tested by simulation.
- [ ] Lineage walkable for the top three metrics.
- [ ] Alerts fired in a forced-failure test.
- [ ] Residual risks recorded.

## 10. Deliverables and handover

Artifacts: `.data/PIPELINE_AUDIT.md`, test suite, contracts, alert rules.

Handover: `03-domains/data-ml-ai/` consumes these tables and inherits the contracts; `04-process/observability-reliability/` P03 takes the freshness and volume alerts into the on-call rotation; `04-process/privacy-requests/` P01 needs the column inventory for deletion requests; `03-domains/database/` owns any correction that rewrites history.
