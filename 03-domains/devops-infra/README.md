# DevOps & Infrastructure Domain System

**Status:** Operational — 8 developed stages (`DI-P01` … `DI-P08`). Each stage states its inputs, decision rules, verification, failure handling and handover. None of these eight has been executed against a real estate yet: they are developed to the standard, not empirically tested — see [`_meta/evidence.json`](../../_meta/evidence.json) for the prompts that have run.
**Entry Point:** [`P08-Orchestrator/P08-DevOps-Infra-Orchestrator.md`](P08-Orchestrator/P08-DevOps-Infra-Orchestrator.md)

A multi-stage system for designing, implementing, and improving infrastructure, CI/CD, and operational platforms.

Use for:
- CI/CD pipeline design or improvement
- Infrastructure as Code (Terraform, Pulumi, CloudFormation)
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

## What each stage gates on

`DI-P01` establishes what exists, who owns it and what a bad apply can destroy, including
which resources are shared between environments. `DI-P02` writes targets that a step can
fail on — four delivery metrics with formulas, SLIs with their exclusions named, and an
error-budget policy with a trigger. `DI-P03` decides environment isolation and the promotion
path, and fills a blast-radius table with reversibility per change type. `DI-P04` designs
the two artefacts that make applies safe: locked remote state with versioning, and a plan
gate that fails on a destroy of an irreversible resource. `DI-P05` applies one change at a
time, records the plan and the approver, and verifies with an assertion. `DI-P06`
instruments the platform itself — pipeline staleness, drift, lock age, expiry, quota and
backup age — because those failures have no customer-facing symptom until they do.
`DI-P07` proves the machinery: a failing fixture per gate, a restore drill with row counts,
and a timed rollback.

Three related prompts are cited rather than duplicated: [`IAC-01`](../../05-scenarios/infrastructure-as-code/INFRA-AS-CODE.md)
for drift and adoption across an estate this system did not build, [`OBS-P01`–`OBS-P05`](../../04-process/observability-reliability/README.md)
for service-level signal and alert design, and [`OPS-01`](../../05-scenarios/operational-readiness/OPERATIONAL-READINESS.md)
for the readiness review of a whole service.

## Principles

- Prefer incremental, reversible changes.
- Make blast radius explicit.
- Codify infrastructure and delivery paths.
- Treat observability and rollback as first-class.
- Never weaken security or access controls for convenience.
