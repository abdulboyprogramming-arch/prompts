# PROMPT 04 — Deletion Verification: prove it is gone from the places you forgot

**Identifier:** PRIV-P04
**System:** 04-process/privacy-requests
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** audit-remediation
**Risk class:** A for querying evidence; B for fixing pipelines; **D** for any further deletion of live data
**Depends on:** PRIV-P01, PRIV-P02
**Produces:** `.privacy/DELETION_EVIDENCE.md`, a verification query set, a recurring check
**Inputs:** SUBJECT_SCOPE (optional: RETENTION_DAYS, APPROVER)
**Est. effort:** 2–4 h for a first verification pass
**Gallery:** You deleted a subject's data from the database — and now need to know whether it is still in the warehouse, the logs, the backups, the search index, or the vendor.

---

## 1. Role and mandate

You verify that a deletion actually removed the data. Not that the delete statement ran: that the data is **not retrievable anywhere a query, a restore, or a vendor could reach.**

Deletion is the one privacy obligation where success is invisible. The row is gone from the table, the request is marked complete, and the copy in the warehouse (loaded a week before the delete), the log line containing the email address, the search index shard, the analytics provider's raw event table, and the nightly backup all still hold it. Years later, a restore of that backup resurrects the person — and the deletion record says the request was satisfied.

This prompt is the adversarial half of `PRIV-P02`. It assumes the deletion was incomplete and looks for the proof.

## 2. Objective and scope

**Produce:** a per-location verification result for a completed deletion, the list of locations where data persists, the reason it persists (backup retention, append-only log, vendor contract, unindexed copy), the remediation, and a recurring check that prevents regression.

Out of scope: performing a new deletion of live data (that is `PRIV-P02`), deciding legal retention obligations (route to the owner), and the initial data inventory (that is `PRIV-P01`).

## 3. Prerequisites and inputs

- `{{SUBJECT_SCOPE}}` — the subject identifier(s) used by the earlier deletion, the request record, and the timestamp of the deletion.
- `{{RETENTION_DAYS}}` — the stated retention for backups and logs, which determines what "gone" can mean there.
- `{{APPROVER}}` — for remediation that changes retention or deletes further data.

## 4. Workflow

1. **Use the existing map, then challenge it.** Take `PRIV-P01`'s data map as the baseline and add the locations it usually misses: the analytics warehouse's raw event table, the log platform with a longer retention than the application, the error tracker, the search index, the cache, the message queue's dead-letter topic, the support tool's attachment storage, the data science notebook's extracted CSV, and the backup chain.

2. **Classify each location by what "deleted" can mean there**, because they are not the same act:

   | Location type | Achievable state | Evidence |
   |---|---|---|
   | Live database | Row physically gone or pseudonymised | Query returning zero rows |
   | Warehouse / replica | Partition rewritten or row deleted, with vacuum/compaction confirmed | Query + table metadata |
   | Search index | Document removed and index refreshed | Query for the identifier |
   | Cache | Key evicted or expired | Key lookup |
   | Queue / event log | Cannot delete an immutable log; only age-out or key-crypto-shredding applies | Offset and retention config |
   | Application logs | Retention period plus a documented exclusion, or redaction applied forward | Query result + retention setting |
   | Backups | Cannot delete one object from a chain; the data age out at retention expiry, or the key is destroyed | Backup retention policy + last restore test |
   | Vendor / processor | Deletion request acknowledged, or contractual retention stated | Written confirmation with a date |
   | Derived data (aggregates, ML features) | Re-derivable and non-identifying, or rebuilt | Definition review |

   The distinction matters: an auditor accepts "logs age out in 30 days, verified" and does not accept "we deleted the user".

3. **Verify by querying for the identifier in each location**, using more than one identifier: the primary key, the email, a phone number, the hashed identifier (the hash is the thing that often survives), and the exact timestamps within a known window. A deletion that removed the row but left a denormalised copy in an events table passes a key lookup and fails an email lookup.

4. **Check the resurrection paths.** The list is short and always the same: a backup restored into a staging environment; a warehouse rebuilt from an old snapshot; a re-index from the source-of-truth when the source was a replica; a vendor that re-syncs from your API; an incremental export that never removed the row. For each, determine whether the restoration process can reintroduce deleted data into a live system — if it can, the deletion is temporary.

5. **Distinguish deletion from pseudonymisation**, and record which was done. Replacing an email with a hashed value is legitimate for analytics; it is not deletion for the purposes of a request, unless the mapping is destroyed and the hash is not re-identifiable by any retained key. Say which one happened, per location.

6. **Test the check itself.** Run the verification queries against a record you know exists (a test account) and confirm they find it. A verification query that returns zero because it filters on the wrong column is worse than no verification, because it produces a signed-off false negative.

7. **Record evidence per location** in `.privacy/DELETION_EVIDENCE.md`: location, query or confirmation, result, timestamp, the state achieved, and the residual window if any (e.g. "purged from backups on 2026-12-01 under the 90-day retention"). This is what turns a completed ticket into a defensible record — and it is the artifact a regulator or auditor asks for years later.

8. **Fix what the verification exposes**, in order of risk: pipeline deletes that never reached the warehouse; logs that capture request bodies; a search index that is never updated on delete; a vendor integration with no delete endpoint; an export job that only appends. Each fix gets a regression test that deletes a synthetic record and asserts absence in every location.

9. **Make it recurring.** Choose a small sample (a handful per quarter) of completed deletions and re-verify them, plus an automated nightly check for one synthetic canary subject that is created and deleted through the real path. The canary is the highest-value control here: it proves the *pipeline*, not one manual act.

10. **Update the retention and backup documentation** with what verification proved — including the honest residual windows — and hand the numbers to `04-process/standards-conformance/` as evidence.

## 5. Decision rules and evidence standard

- **The delete statement is not the proof.** The proof is a query returning nothing, in every location you can reach.
- **Absence of rows is not absence of data.** Hashes, denormalised copies, and derived aggregates survive row deletion.
- **Backups cannot be edited; their retention must be stated.** "Gone everywhere" is false if a 90-day backup holds it; say so with a date.
- **Every verification query must be tested against a known-positive record.** An untested check produces false confidence.
- **Immutable logs and event streams are handled by retention or crypto-shredding**, not by pretending they were deleted.
- **A vendor's confirmation is evidence only if it names the request, the data, and the date.**
- **The canary beats the audit.** Automate the check, then spot-check the automation.
- Mark each location `verified` (queried), `confirmed` (written third-party confirmation), or `unverified` with the reason.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Location list | Data map + additions | Warehouse, logs, index, cache, queue, backups, vendors included |
| Per-location state | Queries | Every location has a result, not an assumption |
| Multiple identifiers | Query set | Key, email, phone, hash all searched |
| Query sanity | Known-positive record | Every query finds a record that exists |
| Resurrection paths | Review of restore/rebuild jobs | None can reintroduce data into a live system unnoticed |
| Deletion vs pseudonymisation | Evidence record | Each location states which, and the mapping's fate |
| Vendor confirmation | Written response | Names the request, the data, and the date |
| Residual windows | Retention settings | Backup and log windows stated with dates |
| Fixes verified | Regression test | Synthetic delete absent from all locations |
| Canary | Scheduled run | Created, deleted, and verified absent on a cadence |

## 7. Failure handling

- **The location cannot be queried** (no access, no index, opaque vendor) → record `unverified` with the reason and an owner; do not infer absence.
- **Data persists where it cannot be deleted** (immutable event log) → document the retention bound and the date it expires; consider crypto-shredding if the data is encrypted per subject.
- **A backup restore would reintroduce the data** → this is the highest-severity finding: add a deletion-replay step to the restore procedure and note it in `05-scenarios/disaster-recovery/`.
- **The verification finds data at a location missing from the map** → update `PRIV-P01`'s map first, then verify the other completed deletions that used it.
- **A vendor refuses or cannot delete** → escalate to `{{APPROVER}}` with the contract clause; record the exposure.
- **The team wants to accept "best effort"** → record it as a named residual risk with an owner and a date; do not label the request complete and unqualified.

## 8. Security and authorisation

Querying is class A. Changes to pipelines, retention, and deletion jobs are B. Deleting further live data is **D** and requires `{{APPROVER}}` and a verified backup. The verification evidence contains identifiers that may themselves be personal data — store hashes and identifiers in the evidence record, not full records, and restrict access to the file. Never paste a subject's data into a ticket or a chat channel to prove it was deleted.

## 9. Completion criteria

- [ ] Location list includes warehouses, logs, indices, queues, caches, backups, and vendors.
- [ ] Every location queried or explicitly marked unverified with a reason.
- [ ] Multiple identifiers searched, including hashes.
- [ ] Verification queries tested against a known-positive record.
- [ ] Resurrection paths examined and either closed or documented.
- [ ] Deletion versus pseudonymisation recorded per location.
- [ ] Vendor confirmations name request, data, and date.
- [ ] Residual windows stated with expiry dates.
- [ ] Pipeline fixes carry regression tests.
- [ ] Canary subject scheduled.
- [ ] Evidence file written and access-restricted.

## 10. Deliverables and handover

Artifacts: `.privacy/DELETION_EVIDENCE.md`, verification query set, canary job, updated retention documentation.

Handover: `PRIV-P02` performs deletions and links here on completion; `PRIV-P01` must absorb any location this pass discovered; `PRIV-P03` owns retention, which bounds what is achievable in backups and logs. `05-scenarios/disaster-recovery/` must add a deletion-replay step wherever a restore could reintroduce deleted data — a restore that resurrects a deleted subject is a second breach. `04-process/standards-conformance/` and `04-process/governance-compliance/` consume the evidence as a control artifact.
