# Privacy Requests

**Maturity: operational (v1.0.0).** Three stages for handling access, export, and deletion requests for personal data — the engineering obligations behind GDPR/CCPA-style rights.

**Entry point:** [`P01-Inventory/P01-Data-Inventory.md`](P01-Inventory/P01-Data-Inventory.md)
**Execution mode:** specialised
**Risk class:** C for discovery and export, **D** for deletion

## Why this system exists

A person asks for their data, or asks for it to be deleted. The request has a legal deadline, and the engineering reality is that nobody knows where their data lives: the primary database, a warehouse copy, log files, backups, a support tool, an analytics provider, a queue that has not drained, and a search index.

The failure modes are predictable and expensive:

- The deletion removes rows from the primary database and leaves the warehouse, the backups, and the vendor copy untouched.
- An export contains another person's data because the query joined on the wrong key.
- Data is deleted that a legal hold or a financial retention obligation required, creating a compliance problem while solving another.
- The request is completed, but nothing records what was done, so the next request repeats the discovery from scratch.

## Stages

| ID | Stage | Purpose | Produces |
|----|-------|---------|----------|
| PRIV-P01 | [Data inventory](P01-Inventory/P01-Data-Inventory.md) | Where does this person's data exist — every system, including the ones nobody thinks of | `.privacy/DATA_MAP.md` |
| PRIV-P02 | [Execution](P02-Execution/P02-Request-Execution.md) | Export or delete with verification, scoping, and a record | `.privacy/REQUEST_LOG.md` |
| PRIV-P03 | [Retention & recurrence](P03-Retention/P03-Retention-Systematise.md) | Retention schedules, and making the next request cheap | `.privacy/RETENTION.md` |

## Rules

1. **Discover before acting.** A deletion executed against an incomplete map is a partial deletion that you will have to repeat, with the deadline already burned.
2. **Verify identity and authority** before exporting or deleting anything.
3. **Deletion is verified, not assumed.** Prove the data is gone from each system, or record precisely where it persists and why.
4. **Never delete data under legal hold, financial retention, or an active investigation** — flag and escalate instead.
5. **Every request leaves a record** that satisfies an auditor and does not itself contain the personal data.

## Boundaries

- Data-loss incidents (accidental deletion): `05-scenarios/data-loss/`.
- Security incidents involving personal data: `05-scenarios/security-incident/`.
- General schema and migration work: `03-domains/database/`.
- Legal interpretation, notification obligations, and whether a request is valid: the accountable owner and legal counsel. This system organises engineering work; it does not decide law.

## What this system will not do

- Decide whether a request is legally valid, or which exemption applies.
- Guarantee completeness of the data map — it makes the search systematic and records its limits.
- Retain the personal data in its own artifacts; the record is about the data, not of it.
