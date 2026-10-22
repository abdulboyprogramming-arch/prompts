# Backend Domain System

**Status:** Operational — 8 developed stages (`BE-P01` … `BE-P08`) plus one standalone companion prompt, `API-VER-01` (`P09-API-Versioning`). Each stage states its inputs, decision rules, verification, failure handling and handover. None of these eight has been executed against a real service yet: they are developed to the standard, not empirically tested — see [`_meta/evidence.json`](../../_meta/evidence.json) for the prompts that have run.
**Entry Point:** [`P08-Orchestrator/P08-Backend-Orchestrator.md`](P08-Orchestrator/P08-Backend-Orchestrator.md)

A multi-stage system for designing and building backend services, APIs, and server-side features with attention to contracts, data, reliability, and operability.

## Stages

| ID | Prompt | Purpose |
|----|--------|---------|
| BE-P01 | Context & Constraints | Understand service role, consumers, and constraints |
| BE-P02 | API / Interface Design | Define contracts, endpoints, events, or interfaces |
| BE-P03 | Architecture | Structure modules, boundaries, and integrations |
| BE-P04 | Data & Persistence | Model data, migrations, and consistency needs |
| BE-P05 | Implementation | Build handlers, domain logic, and integrations |
| BE-P06 | Reliability & Operability | Errors, retries, observability, security basics |
| BE-P07 | Validation | Tests, contract checks, and readiness review |
| BE-P08 | Master Orchestrator | Coordinates the full backend process, with a gate between stages |

`P09-API-Versioning/` holds `API-VER-01`, a standalone prompt for consumer-contract
versioning. It is not part of the `BE-P01` … `BE-P08` sequence; use it when an existing
API must change without breaking its callers.

## What each stage gates on

The orchestrator refuses to advance on prose. `BE-P01` produces a consumer table with
timeouts; `BE-P02` an error taxonomy every handler must implement verbatim; `BE-P03` a
transaction boundary per operation; `BE-P04` a migration with a tested reverse; `BE-P05`
a handler and a request test per operation; `BE-P06` a timeout per outbound call with
the budget arithmetic; `BE-P07` an evidence table with artifacts and a residual-risk
list. Any gate that fails stops the run at the owning stage.

## Principles

- Design contracts before deep implementation.
- Make failure modes explicit.
- Prefer clear domain boundaries over layered ceremony without purpose.
- Treat observability and operability as part of done.
- Keep migrations and compatibility intentional.
