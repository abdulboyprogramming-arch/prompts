# PROMPT 01 — Background Jobs That Stop Doing Damage

**Identifier:** JOBS-01
**System:** 05-scenarios/background-jobs
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** B (inspects queues and writes fixes; re-running jobs against production data is C)
**Depends on:** none
**Produces:** `.jobs/DIAGNOSIS.md`, a job safety checklist, idempotency and overlap fixes
**Gallery:** Diagnose why background work duplicates, drops, loops, or fails silently — and make every job safe to re-run.
**Inputs:** TARGET_SERVICE, JOB_SCOPE (optional: SCHEDULER, QUEUE_BACKEND, INCIDENT_REF, TARGET_ENV)
**Est. effort:** 1–4 h

---

## 1. Role and mandate

You diagnose why background work is duplicating, dropping, looping, or silently failing — and you make it safe to re-run.

Background jobs are where correctness goes to hide. They run without a user watching, they retry by default, they overlap when a previous run is slow, and their failures appear as "the report is wrong three days later" rather than an exception.

The defining property: **every job will eventually run twice, run late, or run while the previous copy is still running.** A job that is not idempotent is a job that corrupts data on its first retry.

## 2. Objective and scope

**Produce:** a per-job safety assessment (idempotent? overlapping? bounded? observable?), the specific defects behind the observed symptoms, and fixes that make retries safe.

Out of scope: queue infrastructure sizing, and rewriting the scheduler.

## 3. Prerequisites and inputs

- `{{TARGET_SERVICE}}` and `{{JOB_SCOPE}}` — the jobs in question (payments, emails, syncs, exports, cleanups).
- `{{SCHEDULER}}` — cron, Kubernetes CronJob, cloud scheduler, or an in-app scheduler; each has different overlap semantics.
- `{{QUEUE_BACKEND}}` — Redis/SQS/RabbitMQ/DB-backed; determines visibility timeouts and redelivery behaviour.
- `{{INCIDENT_REF}}` — if a specific incident triggered this; `{{TARGET_ENV}}`.

## 4. Workflow

1. **Build the job table** before diagnosing: name, trigger (schedule or event), expected duration, expected frequency, what it touches, whether it can run concurrently with itself, and what happens if it fails halfway. Most diagnoses are already visible in this table.

2. **Test idempotency first, for every job.** Ask: if this runs twice with the same input, what happens? Duplicate emails, double charges, duplicated rows, counters incremented twice, or a no-op. If the answer is not "no-op", that is the first finding — and the fix is usually a natural key, a unique constraint, or an idempotency key, not application-level checking.

3. **Check overlap and drift**: does the scheduler start a new run while the previous is running? Cron at `0 * * * *` with a 70-minute runtime overlaps every hour. Is there a lock, and does it expire correctly if the worker dies mid-run? A stale lock blocks all future runs; a missing lock doubles the work.

4. **Check the retry semantics end to end**: automatic retries (count, backoff, jitter), the visibility timeout versus actual runtime (a timeout shorter than the runtime guarantees duplicate delivery), poison-message handling (does it retry forever?), and the dead-letter queue — does anything monitor it, or is it a graveyard?

5. **Check the clock**: jobs scheduled in local time break at DST transitions (a 02:30 job runs twice, or not at all). Storage of "next run" in local time, comparisons between UTC and local timestamps, and month-end arithmetic are the usual defects. Schedule in UTC and store instants, not wall-clock strings.

6. **Check partial failure**: a job that processes 10,000 records and dies at 6,000 — does the retry start from the beginning (duplicating 6,000), or resume from a cursor? Is the cursor persisted before or after the work? "Before" loses work; "after" duplicates it.

7. **Check observability**: can you tell whether last night's run happened, how long it took, and how many records it processed? A job with no success metric is a job whose failure is discovered by a customer.

8. **Check backpressure and fan-out**: a nightly job that enqueues one message per user can flood the queue at 02:00; a job that fans out without a concurrency cap starves the interactive path.

9. **Fix in order of data safety**: idempotency (unique constraint or key) → overlap lock → retry/timeout alignment → cursor-based resume → observability → scheduling in UTC.

10. **Write `.jobs/DIAGNOSIS.md`** with the job table, the defects and their evidence, the fixes applied, the definition of "safe to re-run", and the runbook for a stuck or duplicated job.

## 5. Decision rules and evidence standard

- **Assume every job runs twice**; design for the second run.
- **A unique constraint is stronger than a check-then-insert**, which races.
- **Visibility timeout must exceed the 99th-percentile runtime**, or you have designed duplicate delivery.
- **Locks need expiry and ownership**, or a crashed worker stops the schedule.
- **UTC for scheduling, instants for storage**, always.
- **A job with no success signal is unmonitored**, regardless of its logs.
- **Re-running a job in production is a data change**, not a diagnostic step.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Job table complete | Inventory | Trigger, duration, frequency, concurrency, failure behaviour |
| Idempotency tested | Run twice on a copy | Second run is a no-op |
| Duplicate guard | Schema | Unique constraint or idempotency key present |
| Overlap behaviour | Scheduler config | Lock with expiry, or single-flight |
| Timeout alignment | Config vs p99 | Visibility timeout > p99 runtime |
| Poison handling | Queue config | Retry cap and DLQ, with a monitor |
| Clock handling | Code review | UTC scheduling, instants stored |
| Partial-failure resume | Test | Cursor persisted, no loss or duplication |
| Success observable | Metric | Last-run time, duration, record count |
| Backpressure | Load check | Concurrency cap and queue depth alert |
| Runbook | Document | Steps for stuck, duplicated, and backlogged jobs |

## 7. Failure handling

- **Duplicates already happened in production** → quantify and reconcile before changing code: which records, which customers, what was double-sent or double-charged (`03-domains/payments/` for money, `05-scenarios/data-loss/` for deletions).
- **The job is too slow to finish within its interval** → split by partition or increase the interval; do not increase the timeout alone, or the overlap returns.
- **A stale lock blocks the schedule** → add expiry and ownership; provide a documented (gated) way to clear it.
- **The DLQ is full of old messages** → assess whether replay is safe *before* replaying; a month-old payment event replayed blindly is worse than dropping it.
- **The queue is backed up** → scale consumers temporarily, but first check whether the consumers are failing (a retry storm looks like throughput).
- **The job is a cron expression nobody understands** → document it in words with the next five run times, and test the DST boundary explicitly.
- **The scheduler is the database** (a table of due jobs) → watch for two workers polling the same row; use `SELECT … FOR UPDATE SKIP LOCKED` or an equivalent claim.

## 8. Security and authorisation

Risk class B: reads queue and scheduler state, writes code and configuration. Re-running jobs against production data is class C and requires explicit authorisation with a stated window. Jobs that send email, move money, or delete records are irreversible in effect even if the code is reversible — gate those behind an approval step and never test them by triggering the real job. Logs from job runs may contain personal data; redact before attaching to a report.

## 9. Completion criteria

- [ ] Job table complete for every job in scope.
- [ ] Idempotency tested by running each job twice on a copy.
- [ ] Duplicate guards in place (constraint or key).
- [ ] Overlap handled with an expiring lock or single-flight scheduling.
- [ ] Retry, timeout, and visibility settings aligned.
- [ ] Poison messages capped, dead-lettered, and monitored.
- [ ] Scheduling in UTC; DST boundary tested.
- [ ] Partial-failure resume behaviour verified.
- [ ] Success metric visible (last run, duration, count).
- [ ] Concurrency caps and backlog alert configured.
- [ ] Runbook written for stuck, duplicated, and backlogged states.

## 10. Deliverables and handover

Artifacts: `.jobs/DIAGNOSIS.md`, job safety checklist, fixes, runbook.

Handover: `04-process/observability-reliability/` P03 adds the last-run and backlog alerts this diagnosis produced; `03-domains/payments/` reconciles any duplicated financial effects; `05-scenarios/data-loss/` handles accidental deletions from a bad re-run; `03-domains/database/` adds the unique constraints as schema changes with their own migration.
