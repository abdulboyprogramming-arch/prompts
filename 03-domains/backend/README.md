# Backend Domain System

**Status:** Operational (v1.0)  
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
| BE-P08 | Master Orchestrator | Coordinates the full backend process |

## Principles

- Design contracts before deep implementation.
- Make failure modes explicit.
- Prefer clear domain boundaries over layered ceremony without purpose.
- Treat observability and operability as part of done.
- Keep migrations and compatibility intentional.
