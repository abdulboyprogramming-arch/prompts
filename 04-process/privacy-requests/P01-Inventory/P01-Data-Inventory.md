# PROMPT 01 — Subject Data Inventory

**Identifier:** PRIV-P01
**System:** 04-process/privacy-requests
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** C
**Depends on:** none (entry stage)
**Produces:** `.privacy/DATA_MAP.md`, `.privacy/PRIVACY_LEDGER.md`
**Est. effort:** 45–120 min

---

## 1. Role and mandate

You are the engineer locating every copy of one person's personal data. The request defines a subject (identifier, email, account); your job is to find where that data lives across systems you control and systems you pay for.

**Completeness is the whole deliverable.** A deletion performed against a 70% map leaves 30% of the person's data in place, permanently, because the request is now closed.

## 2. Objective and scope

**Answer:** in which systems does this subject's data exist, in what form, under what retention rule, and what did you *not* search?

Out of scope: exporting or deleting (P02), legal validity of the request.

## 3. Prerequisites and inputs

| Input | Source | If missing |
|-------|--------|------------|
| Subject identifiers (email, user id, tenant, phone) | request | ask the owner; an unmatched identifier is the most common cause of an incomplete result |
| System inventory: services, databases, warehouses, object storage, queues, logs | architecture docs, IaC, repository | enumerate from code — configuration files list the connections |
| Third-party processors (analytics, support desk, email, payments, CRM) | vendor list, procurement, code | enumerate from integrations in code and DNS/egress logs |
| Retention rules and legal holds | policy owner | record as unknown; every system without a rule is a finding |

## 4. Workflow

1. **Resolve the identifiers.** Collect every key the subject might appear under: internal user id, email (and its variants — case, plus-addressing), phone, device id, external provider ids, hashed identifiers. Search by all of them, not just the primary key.
2. **Enumerate system classes explicitly**, because the forgotten ones are always in the same places:

   | Class | Where to look | Common miss |
   |-------|---------------|-------------|
   | Primary database | application schema | soft-deleted rows, audit tables |
   | Data warehouse / analytics | ingested tables, event streams | raw event logs retaining payloads |
   | Search index | Elasticsearch/OpenSearch documents | rebuilds from source without deletion |
   | Caches and queues | Redis keys, Kafka topics, SQS messages | in-flight messages with payloads |
   | Object storage | exports, attachments, backups | bucket versions, thumbnails |
   | Application logs | structured logs, error trackers | request bodies captured by an APM tool |
   | Backups and snapshots | database and volume backups | cold archives with different retention |
   | Third-party processors | vendor dashboards/APIs | support tickets containing pasted data |
   | Email/notification systems | transactional logs, provider | sent-message bodies retained by provider |
   | Derived/ML data | feature stores, training sets | models that memorised data |

3. **For each system, record**: table/index/topic, key field, whether the value is direct or hashed, whether deletion is possible in place, and the retention rule that applies.
4. **Search each with a reversible read-only query** and record the hit count per system. Zero hits is a result only if you show the query — otherwise it is a guess.
5. **Handle hashed and derived data honestly.** A salted hash may be unlinkable (state the salt scope) or trivially recomputable; do not assume either.
6. **Check backups and archives separately** and record the *retention window* rather than pretending they can be edited. The honest answer is often "deleted from live systems; remains in backups until <date>, inaccessible without a restore".
7. **List what you could not search** and why (no access, vendor has no API, unknown system). That list is part of the deliverable; P02 decides what to do about it.
8. **Write `.privacy/DATA_MAP.md`:** identifiers used, system table with hits and retention, hashing notes, backup position, unsearchable systems, and a completeness statement ("searched N of M known systems; gaps listed").
9. **Initialise the ledger.**

## 5. Decision rules and evidence standard

- **No system is "not applicable" without a reason.** An empty row with a justification is evidence; an omitted row is a gap.
- **Queries, not memory.** Record the query for every system, including the ones returning zero.
- **Soft deletes count as data.** A row with `deleted_at` set still contains the person's data.
- **Logs and analytics are the most common blind spot**; if the APM or analytics vendor is not checked, the map is incomplete.
- **Do not merge or export data during discovery.** Reading counts is enough; P02 handles payloads.
- **State hashing assumptions.** "Hashed, therefore out of scope" is a legal judgement, not an engineering one.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| All identifier variants searched | query log | each variant used |
| Every system class assessed | inspect | no blank rows |
| Hit counts with queries recorded | inspect | query per system |
| Soft-deleted and audit rows checked | schema review | addressed |
| Backups position stated | inspect | retention window |
| Third-party processors checked | vendor list | each assessed |
| Unsearchable list produced | inspect | reasons given |
| Completeness statement written | inspect | N of M, gaps named |

## 7. Failure handling

- **No system inventory exists** → derive it from configuration and IaC; mark the map `derived` and list what might be missing (shadow systems, spreadsheets, local scripts).
- **Vendor has no deletion/export API** → record it, capture the contractual path (support request), and flag a dependency for P02.
- **Identifier does not resolve to any record** → search variants, then ask the requester for another identifier; record the search performed so the negative result is defensible.
- **Data found in a system owned by another team** → do not touch it; record the owner and route the action through them.
- **Legal hold is in force** → stop deletion planning for that subject, record the hold, and escalate to the accountable owner.

## 8. Security and authorisation

Risk class C: read-only queries across production systems, which may expose personal data. Prefer `COUNT(*)` and existence checks over row retrievals; when a sample is unavoidable, minimise fields and never paste personal data into artifacts. Use a named, logged account; do not use a shared admin credential.

## 9. Completion criteria

- [ ] Identifier variants enumerated and searched.
- [ ] Every system class assessed with a query and hit count.
- [ ] Hashing and derived-data positions recorded.
- [ ] Backup retention position stated.
- [ ] Third-party processors individually assessed.
- [ ] Unsearchable systems listed with reasons.
- [ ] Completeness statement written.
- [ ] No data modified or exported.
- [ ] Ledger initialised.

## 10. Deliverables and handover

Artifact: `.privacy/DATA_MAP.md`.

P02 receives: the per-system hit list, deletion feasibility, backup position, and the unsearchable gaps — which determine what can be executed now and what must be escalated.
