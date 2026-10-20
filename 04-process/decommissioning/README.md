# Decommissioning

**Maturity: operational (v1.0.0).** Four stages for retiring a service, endpoint, feature, or data store without breaking a consumer you forgot about.

**Entry point:** [`P01-Consumers/P01-Consumer-Discovery.md`](P01-Consumers/P01-Consumer-Discovery.md)
**Execution mode:** specialised
**Risk class:** C — deletion is irreversible and often discovers its dependents only after the fact

## Why this system exists

Every library covers building and almost none cover removal. Decommissioning fails in ways that are entirely predictable:

- A consumer nobody knew about starts failing at 3 a.m. on the day the endpoint is removed.
- "No traffic in the logs" is taken as proof of no use, but the log sampling missed a monthly batch job.
- The service is deleted; its database, object storage, and DNS records are not, and the data sits unowned for years.
- Data is deleted to satisfy a retention policy, destroying records that another system still needed.
- The migration completes but the old code path, feature flag, and deployment pipeline remain forever.

None of these are exotic. This system makes each one an explicit decision with evidence.

## Stages

| ID | Stage | Purpose | Produces |
|----|-------|---------|----------|
| DEC-P01 | [Consumer discovery](P01-Consumers/P01-Consumer-Discovery.md) | Find every consumer with positive evidence and instrument what telemetry cannot see | `.decommission/CONSUMER_MAP.md` |
| DEC-P02 | [Deprecation plan](P02-Deprecation/P02-Deprecation-Plan.md) | Notice, migration path per consumer, timeline, and fallback | `.decommission/DEPRECATION_PLAN.md` |
| DEC-P03 | [Shutdown execution](P03-Shutdown/P03-Shutdown-Execution.md) | Staged traffic removal, verification at each stage, reversal window | `.decommission/SHUTDOWN_LOG.md` |
| DEC-P04 | [Data and asset retirement](P04-Retirement/P04-Data-Asset-Retirement.md) | Retention, archival, legal holds, teardown of infrastructure and identities | `.decommission/RETIREMENT_RECORD.md` |

## Rules

1. **Absence of traffic is not absence of consumers.** Instrument before concluding.
2. **Deprecation requires a migration path for every consumer**, or an explicit decision to break it.
3. **Removal is staged with reversal points**; nothing is switched off and deleted in one step.
4. **Data outlives code.** Decide retention, archival, and ownership before deleting anything.
5. **The paperwork is part of the deliverable**: contracts, runbooks, dashboards, DNS, and references in other repositories all have to go.

## Boundaries

- Understanding what the system does before retiring it: `02-engineering/codebase-audit/`.
- Releasing the replacement: `04-process/release-engineering/`.
- Deleting database objects safely: `03-domains/database/` (with its own destructive register).
- Handling personal data in archives: `02-engineering/security-hardening/`.

## What this system will not do

- Decide your legal retention obligations. It surfaces them as decisions with an owner.
- Remove the last copy of data without an explicit, recorded decision by the owner.
- Guarantee that no consumer exists — only that the search was systematic and its limits are stated.
