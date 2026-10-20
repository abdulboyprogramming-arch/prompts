# DevOps & Infrastructure Domain System

**Status:** Skeleton — 8 stage outlines (skeleton 8). The stages name a sensible sequence but lack the evidence rules, verification, and failure handling that this library requires of `operational`. Treat the system as a plan, not a procedure; see [`_meta/ROADMAP-AND-BACKLOG.md`](../../_meta/ROADMAP-AND-BACKLOG.md).
**Entry Point:** [`P08-Orchestrator/P08-DevOps-Infra-Orchestrator.md`](P08-Orchestrator/P08-DevOps-Infra-Orchestrator.md)

A multi-stage system for designing, implementing, and improving infrastructure, CI/CD, and operational platforms.

Use for:
- CI/CD pipeline design or improvement
- Infrastructure as Code (Terraform, Pulumi, CloudFormation, etc.)
- Environment topology and deployment strategy
- Observability, reliability, and operational guardrails
- Platform/engineering-enablement infrastructure work

## Stages

| ID | Prompt | Purpose |
|----|--------|---------|
| DI-P01 | Context & Constraints | Understand systems, environments, and operational constraints |
| DI-P02 | Requirements & SLOs | Define reliability, delivery, and security requirements |
| DI-P03 | Architecture | Design topology, environments, and control planes |
| DI-P04 | IaC & Pipelines | Design infrastructure-as-code and delivery pipelines |
| DI-P05 | Implementation | Apply infra/pipeline changes safely |
| DI-P06 | Observability & Ops | Logging, metrics, alerts, runbooks |
| DI-P07 | Validation | Verify safety, rollback, and operational readiness |
| DI-P08 | Master Orchestrator | Coordinates the full DevOps/infra process |

## Principles

- Prefer incremental, reversible changes.
- Make blast radius explicit.
- Codify infrastructure and delivery paths.
- Treat observability and rollback as first-class.
- Never weaken security or access controls for convenience.
