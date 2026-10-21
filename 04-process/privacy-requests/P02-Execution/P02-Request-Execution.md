# PROMPT 02 — Request Execution

**Identifier:** PRIV-P02
**System:** 04-process/privacy-requests
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** specialised
**Risk class:** D
**Depends on:** PRIV-P01
**Produces:** `.privacy/REQUEST_LOG.md`, verified deletion or scoped export
**Inputs:** SUBJECT_IDENTIFIERS, VERIFICATION_METHOD, REQUEST_ID
**Est. effort:** 30–120 min

---

## 1. Role and mandate

You execute an access or deletion request. Deletion is irreversible, so you work from the inventory, verify identity and authority, execute system by system, and prove the result. You do not improvise scope: if the map says a system holds the data, it is handled or explicitly escalated.

## 2. Objective and scope

**Execute:** export the subject's data, or delete it, with per-system verification and a complete record.

Out of scope: deciding whether the request is legally valid (owner/legal), inventing systems not on the map (return to P01).

## 3. Prerequisites and inputs

| Input | Required | If missing |
|-------|----------|------------|
| `.privacy/DATA_MAP.md` with a completeness statement | yes | return to P01; executing on an incomplete map creates permanent partial deletion |
| Identity verification of the requester `{{SUBJECT_IDENTIFIERS}}` via `{{VERIFICATION_METHOD}}` | yes | stop; deleting or exporting on an unverified request is itself a breach |
| Legal hold check for request `{{REQUEST_ID}}` | yes | stop and escalate |
| Deletion authority for each system (owner, runbook, API) | per system | mark that system `blocked`; do not improvise |

## 4. Workflow

### For an access/export request

1. **Scope the export** to the subject's data only. Use the identifier list from P01; never query by a field that could match multiple people (name, partial email).
2. **Test the query on a staging copy first**, and count rows. If the count is implausibly high, the key is wrong — stop.
3. **Assemble in the least-exposing format**: machine-readable (JSON/CSV), transmitted over an authenticated channel, encrypted at rest, with a stated expiry for the transfer link.
4. **Redact third-party data** (other users in the same records, internal notes about other people, fraud signals you are legally allowed to withhold — flag, do not decide).
5. **Record the export** (what, where, key used, row counts, recipient, expiry) without storing the payload in the repository.

### For a deletion request

6. **Confirm the legal position**: no active hold, no contractual retention covering the data, no open investigation. If any is unclear, stop and escalate — an unrecoverable deletion under a hold is a serious incident.
7. **Order the deletions to avoid leaving orphans and to keep the system consistent**: derived systems first (search index, caches, exports, thumbnails), then event streams and queues, then primary records, then audit/analytics copies, then vendor systems.
8. **Prefer the application's own deletion path** (a service endpoint or documented runbook) over raw SQL: it handles cascades, soft-delete semantics, and downstream events. Raw SQL is a fallback with a recorded reason.
9. **Execute one system at a time**, recording the exact statement/endpoint, key used, and rows affected. If rows affected is zero where the map predicted hits, investigate before proceeding.
10. **Verify each system afterwards with a fresh read-only query**, not by trusting the response code. Record the post-deletion count.
11. **Handle backups explicitly.** You usually cannot delete individual records from backups. Record: the retention window, the date after which the data ages out, and the compensating control (restores are restricted and re-deletion is part of the restore procedure).
12. **Handle caches and replicas**: invalidate cache keys, confirm replicas have applied the deletion (replication lag), and rebuild search indexes from source rather than patching documents.
13. **Record residual copies with an owner and a date** — vendor holding the request, archive not yet expired, legal-hold copy that must be preserved but access-restricted.

## 5. Decision rules and evidence standard

- **Identity before action.** An export or deletion performed on an unverified request is a data breach with paperwork.
- **Never delete beyond the scope of the request.** Wider deletions (by name, by tenant) require their own authorisation.
- **A zero-row result contradicts the map** — stop and investigate rather than declaring success.
- **Backups are described, not pretended.** "Deleted from backups" is almost always false.
- **Keep the record, not the data.** Log counts and locations; never store the extracted personal data in the repository.
- **Escalate, don't improvise**, when a system has no deletion path or a hold is suspected.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Identity verified | evidence recorded | method and result |
| Legal hold checked | record | cleared before deletion |
| Export scoped to one subject | row-count review | plausible, single-subject |
| Deletions verified per system | fresh query | zero rows, or residual documented |
| Rows-affected matches the map | comparison | consistent or explained |
| Derived systems handled | index/cache checks | rebuilt or invalidated |
| Backups position recorded | retention policy | window and age-out date |
| Vendor requests tracked | ticket references | status and owner |
| Log complete | inspect | per-system evidence |

## 7. Failure handling

- **A system has no deletion capability** → record `blocked`, quantify the residual, and escalate to the owner; do not close the request as complete.
- **Deletion breaks application behaviour** (foreign key, missing lookup) → stop and restore from the transaction; route the schema issue to `03-domains/database/`; a deletion that requires a schema change is planned, not improvised.
- **The subject appears in a shared record** (e.g. a chat thread with others) → redact rather than delete, record the approach, and flag for the legal owner.
- **Data is found outside the map** during execution → add it to the map, handle it, and record that the inventory was incomplete; repeat the search for the missed class.
- **Replication lag delays the deletion** → wait and re-verify; do not report completion on the primary alone.
- **A hold is discovered mid-execution** → stop immediately, record what was already deleted, and escalate; do not attempt to restore without the owner's approval.

## 8. Security and authorisation

Risk class D. Deletion requires a named approver and an authenticated, logged session with the minimum privilege that can perform it. Export transfers must be encrypted, access-controlled, and expiring. Never send personal data over email or chat; never commit it to the repository; never keep it longer than the delivery window requires.

## 9. Completion criteria

- [ ] Identity and authority verified and recorded.
- [ ] Legal hold clearance recorded.
- [ ] Export scoped, tested, redacted, and delivered securely (or deletion executed in dependency order).
- [ ] Every mapped system either executed and verified, or marked blocked with an owner.
- [ ] Derived systems (index, cache, queue) handled and verified.
- [ ] Backup position and age-out date recorded.
- [ ] Residual copies listed with owners and dates.
- [ ] Request log complete, containing no personal data.

## 10. Deliverables and handover

Artifacts: `.privacy/REQUEST_LOG.md`, verified state per system.

P03 receives: what had to be done manually, which systems were blocked, and where deletion depended on a mechanism that should be automatic — the input for retention rules and a self-service path.
