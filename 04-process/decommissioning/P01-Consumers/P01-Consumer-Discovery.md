# PROMPT 01 — Consumer Discovery

**Identifier:** DEC-P01
**System:** 04-process/decommissioning
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A
**Depends on:** none (entry stage)
**Produces:** `.decommission/CONSUMER_MAP.md`, `.decommission/DECOMM_LEDGER.md`
**Inputs:** TARGET_SERVICE (optional: TARGET_AREA)
**Est. effort:** 30–90 min

---

## 1. Role and mandate

You are the engineer establishing whether anything still depends on the thing being retired. You do not accept "nothing uses it" as an answer: you produce positive evidence per consumer class, and you state exactly what your search could not see.

## 2. Objective and scope

**Answer:** who or what calls, reads, writes, or depends on this artefact, including the consumers that leave no trace in application logs?

Out of scope: the deprecation plan (P02), shutting anything down (P03).

## 3. Prerequisites and inputs

| Input | If missing |
|-------|------------|
| The artefact's identity: `{{TARGET_SERVICE}}` — service, endpoint, table, queue topic, bucket, flag, package; search scope `{{TARGET_AREA}}` | pin the exact scope with the owner |
| Access to telemetry: access logs, gateway metrics, APM traces, queue consumer groups | request access; without it, discovery is partial and must be labelled as such |
| Repository access for code search | ask for a list of consuming repositories |
| Contract/registry documentation (API catalogue, service map) | derive from search and label as derived |

## 4. Workflow

1. **Define the artefact precisely.** "The `/v1/reports` endpoint" not "reports". Record versions, aliases, hostnames, and legacy paths that route to the same thing — the forgotten alias is the classic miss.
2. **Enumerate consumer classes** and search each one separately:

   | Class | Evidence source | What it typically reveals |
   |-------|-----------------|---------------------------|
   | Internal services | gateway/APM traces, service map | synchronous callers |
   | Frontend clients | browser analytics, CDN logs, error reports | user traffic, old app versions still in the field |
   | Batch/scheduled jobs | cron inventory, scheduler config, job logs | monthly and quarterly consumers invisible in daily metrics |
   | External partners | API keys, contracts, support tickets | contractual obligations |
   | Data pipelines | warehouse ingestion jobs, export configs | readers that never appear in request logs |
   | Integrations/webhooks | outbound configuration, retry queues | consumers you push to rather than serve |
   | Analytics/reporting | BI dashboards, saved queries | human-facing dependence |
   | Documentation/examples | repository search | published guidance that promises the endpoint |

3. **Use time windows that match the slowest consumer.** Query telemetry over at least the longest known batch interval multiplied by a safety factor (a monthly job needs ≥13 months of evidence to be safe, a quarterly one ≥15). State the window used.
4. **Search code across all repositories**, not just this one: the endpoint path, the table name, the topic name, the package name, the config key. Include configuration files, infrastructure definitions, and SQL.
5. **Check for indirect dependence.** A table may be read by a nightly export; an event topic may be consumed by a service that only reports errors when the topic disappears.
6. **Distinguish verified absent from unobservable.** For each class, record one of: `consumer found (named)`, `no evidence in <source> over <window>`, or `cannot observe (reason)`.
7. **Instrument before concluding** where observation is weak: add a deprecation warning header on responses, log with a distinct marker, or enable request-level logging for a defined period. A two-week instrumented observation is stronger evidence than a year of sampled logs.
8. **Identify the decision owner** for each consumer class: who is allowed to break this dependency.
9. **Write `.decommission/CONSUMER_MAP.md`:** artefact definition, consumer table by class with evidence and window, instrumentation results, unobservable areas with reasons, migration difficulty per consumer (trivial/rework/blocked), and the owner per consumer.
10. **Initialise the ledger.**

## 5. Decision rules and evidence standard

- **No traffic ≠ no consumer.** Sampled logs, daily metrics, and short windows systematically miss batch and partner traffic.
- **Every "none found" needs the source and window recorded.** "Searched" is not evidence.
- **Unobservable is a finding, not a gap to gloss.** It changes P02 from "notice period" to "instrumentation period".
- **Prefer positive instrumentation** over passive metrics when the artefact is high-consequence.
- **Never contact consumers during discovery** without the owner's agreement; a warning to the wrong party can cause an unplanned migration or a contractual conversation.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Artefact scope pinned | inspect | versions, aliases, hosts listed |
| All consumer classes searched | inspect | one row per class |
| Window justified | inspect | ≥ slowest batch interval × 1 |
| Code search across repositories | commands recorded | patterns and repositories named |
| Indirect dependence checked | inspect | pipeline/integration classes addressed |
| Unobservable areas named | inspect | reason given |
| Instrumentation used where needed | config/log evidence | active or explicitly rejected |

## 7. Failure handling

- **No telemetry access** → discovery is static only; label it `unverified`, propose an instrumentation period, and do not approve (P02) on this basis.
- **Consumer behaviour unknown** (partner, third party) → treat as `blocked` until the contractual contact confirms.
- **Traffic exists but no owner can be identified** → search the request's auth identity, ticket history, and on-call records; if still unknown, escalate rather than removing.
- **Artefact is used by the same team that wants it gone** → trivial; record and proceed quickly (this is the common case and should not be over-engineered).
- **Discovery reveals the artefact is load-bearing for something undocumented** → stop; this is an architecture finding, and retiring it is now a project (`REC-P05`).

## 8. Security and authorisation

Risk class A: read-only. Do not query production data beyond metrics/logs needed for discovery. Do not contact consumers without approval. Handle consumer identities (partner names, keys) as confidential — record references, not secrets.

## 9. Completion criteria

- [ ] Artefact scope pinned including aliases and versions.
- [ ] Every consumer class searched with source and window recorded.
- [ ] Telemetry window covers the slowest known consumer.
- [ ] Code search performed across all identified repositories.
- [ ] Indirect dependence (pipelines, integrations, reporting) checked.
- [ ] Unobservable areas named with reasons.
- [ ] Instrumentation applied where evidence was weak.
- [ ] Owner identified per consumer class.
- [ ] Ledger initialised.

## 10. Deliverables and handover

Artifact: `.decommission/CONSUMER_MAP.md`.

P02 receives: the consumer list with migration difficulty, the unobservable areas (which determine the notice period and instrumentation plan), and the decision owners.
