# Data-Loss Recovery

**Identifier:** DATALOSS-01
**System:** 05-scenarios/data-loss
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** specialised
**Risk class:** D — any action here can convert a recoverable loss into a permanent one
**Gallery:** Contain the damage, then recover data from a backup, log replay, or an upstream source — and say precisely what is still gone.
**Depends on:** none; runs before root-cause analysis
**Produces:** `.dataloss/RECOVERY_LOG.md`, restored data, a quantified loss statement
**Inputs:** TARGET_ENV, DATA_LOSS_WINDOW, APPROVER (optional: BACKUP_INVENTORY)
**Est. effort:** 1–8 hours, in stages

---

## 1. Role and mandate

You are the recovery lead. Data has been lost or corrupted and the clock matters, but the first instinct — "restore the backup" — is how a partial loss becomes a total one. Your job is to stop further damage, establish exactly what was lost, and choose a recovery route that is verified before it is applied.

**You are not debugging yet.** Cause comes after containment. If you start reading code while writes continue, the loss grows.

## 2. Objective and scope

**Sequence:**

1. Stop the damage.
2. Preserve what remains.
3. Establish the loss precisely.
4. Choose and verify a recovery route.
5. Recover in a way that can be abandoned.
6. Quantify what is permanently gone.
7. Hand the cause to incident/debugging.

Out of scope: root-cause analysis, prevention implementation (both follow), and legal advice on notification obligations (flag them, do not decide them).

## 3. Prerequisites and inputs

| Input | Why it matters | If missing |
|-------|----------------|------------|
| Access to freeze writes on `{{TARGET_ENV}}` (revoke credentials, disable the job, put the service in read-only), authorised by `{{APPROVER}}` | The only step that is time-critical | Escalate immediately; without it you are recovering into a moving target |
| Backup/snapshot inventory `{{BACKUP_INVENTORY}}` with timestamps and retention | Determines the recoverable point | Ask the platform owner; do not assume "we have backups" |
| Knowledge of the loss window `{{DATA_LOSS_WINDOW}}` | Bounds the damage | Narrow it with logs, request traces, and the last known-good observation |
| Write-ahead/binlog/change-stream availability | Allows replay between restore point and incident | Record as unavailable; it changes the strategy |

## 4. Workflow

### Stage 1 — Freeze (first 15 minutes)

1. **Stop the writes.** In escalating order of bluntness: disable the offending feature flag or job; revoke the credential the writer uses; switch the endpoint to read-only; pause the consumer/queue; scale the worker to zero. Record exactly what you changed and when.
2. **Do not delete anything.** No cleanup, no "removing the bad rows", no truncating the partial table. The corrupted data may be the evidence that lets you reconstruct the correct state.
3. **Stop the retry.** Many losses are amplified by a retry loop, a backfill that keeps running, or a queue that re-delivers the same destructive message. Check for scheduled jobs and cron entries that will fire again.
4. **Preserve logs and state before they rotate.** Copy the relevant application logs, database logs, and audit entries, and snapshot the current database state (or at least the affected tables) even if it is corrupt — a copy of the damage is valuable.
5. **Declare the incident and name one owner.** Two people issuing recovery commands against the same system is a second incident. In the same message, state what you have frozen.

### Stage 2 — Establish the loss

6. **Characterise the loss type**, because each has a different recovery route:

   | Type | Distinguishing evidence | Primary route |
   |------|------------------------|---------------|
   | Deletion (rows/objects) | Rows absent where they existed; `DELETE` in logs | PITR + replay, or restore-verify-merge |
   | Overwrite/truncation | Columns blank or reset; bulk `UPDATE` | PITR to a side instance, diff, merge |
   | Corruption (logical bug) | Wrong values written over time, no single event | Reconstruct from source of truth or derived recomputation |
   | Schema/migration damage | Loss coincides with a deployment; `DB-P04` context | Reverse the migration, restore affected tables |
   | Storage/hardware failure | I/O errors, missing files, replica gone | Failover to replica, restore from backup |
   | Malicious/ransomware | Encrypted or mass-deleted data, unusual access | Isolate, preserve evidence, **do not pay, do not restore over live**, involve security |

7. **Bound the window.** Identify the last known-good observation (a report that reconciled, a screenshot, a row with a plausible timestamp) and the first known-bad one. The gap is the exposure window.
8. **Scope the blast radius:** which tables/objects, which tenants or customers, which time ranges, which downstream systems received the bad data (caches, search indexes, exports, warehouses, emails already sent). Downstream copies are the most commonly forgotten part of the loss.
9. **Quantify** with queries, not impressions: rows affected, distinct users, business value at risk, and whether anything left the system (sent notifications, files downloaded).

### Stage 3 — Choose the route

10. **Enumerate the routes before choosing:**

    | Route | When it works | What it costs |
    |-------|---------------|---------------|
    | **PITR to a side instance, then merge** | You have PITR and a bounded window | Time; needs a careful diff/merge procedure |
    | **Restore backup to side instance, then merge** | Snapshot exists and the gap is small | Data after the snapshot is lost unless replayable |
    | **Replay from logs/change stream** | Binlog, CDC, or event stream covers the window | Complex; replay must be idempotent |
    | **Reconstruct from an upstream source of truth** | The data was derived from another system (ERP, provider API, user re-entry) | Time, and only for derivable data |
    | **Forward-fix** | The damage is well understood and bounded; restoring would lose more | Requires a validated correction script |
    | **Accept the loss** | Recovery costs more than the value, or makes things worse | Explicit, documented, communicated |

11. **Never restore over the live system as the first attempt.** Restore to a separate instance or database, verify the restored state, and merge deliberately. An in-place restore destroys the current state, including any data written after the backup.
12. **Verify the backup before relying on it.** Does it restore at all? Does it contain the expected tables and row counts? Is it the version you think it is? A restore drill in `DB-P03` is exactly this check, performed before you needed it.
13. **Prefer the route that is reversible.** If two routes are viable, choose the one that leaves the current data intact until the replacement is proven.
14. **Write the recovery plan** with explicit steps, checkpoints, and a decision point where you can still abandon it.

### Stage 4 — Recover

15. **Restore to the side instance** and verify: schema matches, row counts plausible, spot-check records against known-good values, constraints hold.
16. **Diff restored against current** for the affected objects. Produce: rows to reinsert, rows to overwrite, rows written during the incident that must be preserved. Do not merge blindly — the restored state is "the past", and the current state contains legitimate new writes.
17. **Apply the merge in a transaction or in idempotent batches**, with counts logged per batch, on a copy first if the volume is large.
18. **Reconcile**: the invariants from `DB-P05` (counts, sums, orphans, samples across the window). Record numbers.
19. **Handle downstream copies**: invalidate caches, rebuild search indexes, re-derive warehouse tables, and identify already-sent notifications or exports that cannot be recalled — those are permanent consequences, not recoverable data.
20. **Verify the application** against restored data on the critical paths, and only then re-enable writes. Re-enabling is itself a change: confirm the cause is contained, or you will resume the loss.

### Stage 5 — Quantify and hand over

21. **Write the loss statement** in plain language: what was lost permanently, what was recovered, what was reconstructed, what is uncertain, and who is affected. This statement is what the owner communicates and what auditors will read.
22. **Do not overstate recovery.** "Recovered 4,812 of 5,000 records; 188 could not be reconstructed because they were created between the snapshot and the incident and no source exists" is the standard. "Data restored" is not acceptable.
23. **Flag obligations without deciding them:** customer notification, regulatory reporting, contractual breach notification, and privacy implications. Name the decision owner.
24. **Hand over to root cause:** `05-scenarios/incident-response/` for the operational postmortem, `05-scenarios/debugging/` for a logic defect, `04-process/dependency-management` or `DB-P04` if a change caused it.
25. **Convert the lesson into a control:** a restore drill, a backup retention change, a constraint that would have prevented the damage, or a guard on the destructive operation. Record it with an owner and a date.

## 5. Decision rules and evidence standard

- **Containment before diagnosis.** Always. Diagnosis while writes continue is how the second incident happens.
- **A backup is unproven until restored.** Verify on a side instance before planning around it.
- **Never restore over live as step one.** The current state is data too.
- **Restored ≠ correct.** The restored point is earlier than the incident; merging is required unless you accept the gap.
- **Loss must be quantified in records and users**, not described as "some data".
- **No destructive cleanup of the evidence** until the postmortem and any legal hold are resolved.
- **Do not re-enable writes until the cause is contained**, even if users are waiting: say what is blocked and why.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Writes frozen | observe: no new writes in the affected path | confirmed |
| Evidence preserved | logs/tables copied | copies exist with timestamps |
| Window bounded | last good / first bad | both identified |
| Blast radius includes downstream | inventory check | caches, indexes, exports listed |
| Backup verified by restore | side-instance restore | row counts and samples correct |
| Merge preserves new writes | diff review | post-incident legitimate rows retained |
| Reconciliation quantified | invariants | numbers recorded |
| Loss statement precise | read as an auditor | recovered vs lost vs uncertain |
| Obligations flagged | inspect | named with decision owner |
| Prevention has an owner | inspect | control + date |

## 7. Failure handling

- **Cannot freeze writes** → escalate to whoever controls access immediately; recover on the assumption the state will change and keep re-diffing.
- **No usable backup** → the routes are reconstruction and acceptance only; say so plainly, and start from upstream sources and downstream copies (warehouses, exports, third parties).
- **Backup restores but is older than expected** → the gap is larger; quantify it and consider log replay before accepting.
- **Restore is larger than the free space / takes longer than the outage allows** → restore only the affected tables to the side instance, or restore in stages.
- **Merging causes conflicts** (same row changed both before and after) → resolve per row with the business owner; do not let a script pick a winner silently.
- **Data left the system** (email, export, webhook) → it is unrecoverable; record it and route to notification decisions.
- **The cause is unknown and writes must resume** → resume with the destructive path disabled and a monitoring guard, not on hope.

## 8. Security and authorisation

Risk class D. Every recovery action that modifies data requires a named approver. Never restore production data into an environment with weaker access controls. Treat the incident as a potential security event until disproven: if the loss was not caused by an obvious mistake, preserve evidence and involve `05-scenarios/security-incident/`. Do not include personal data in recovery artifacts beyond what the procedure requires.

## 9. Completion criteria

- [ ] Writes frozen; retries and scheduled jobs stopped.
- [ ] Evidence preserved before rotation.
- [ ] Loss type characterised and window bounded.
- [ ] Blast radius including downstream copies identified.
- [ ] Routes enumerated; chosen route justified, with its irreversibility stated.
- [ ] Backup verified by an actual restore to a side instance.
- [ ] Merge applied with counts, preserving post-incident legitimate writes.
- [ ] Invariants reconciled with numbers.
- [ ] Application verified; writes re-enabled only after containment.
- [ ] Loss statement precise (recovered / lost / uncertain / affected).
- [ ] Notification obligations flagged with an owner.
- [ ] Prevention control recorded with owner and date.

## 10. Deliverables and handover

Artifacts: `.dataloss/RECOVERY_LOG.md` (every action with a timestamp and result), the loss statement, and reconciliation numbers.

Handover: `05-scenarios/incident-response/` for the postmortem timeline; `05-scenarios/debugging/` if a logic defect caused it; `03-domains/database/DB-P03` for the restore drill that should have caught this; the prevention control into `_meta`-style tracking or the team's issue tracker, with a date.
