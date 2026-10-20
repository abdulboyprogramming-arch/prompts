# 03-Domains

Deep, technology-specific prompt systems. Cross-cutting activities (audits, refactoring, recovery, from-scratch construction) live in `02-engineering/`.

## Systems

| Path | Description | Stages | Maturity |
|------|-------------|-------:|----------|
| [`ai-agentic/`](ai-agentic/README.md) | LLM features and agents: risk, architecture, evaluation, guardrails, production operations, grounded retrieval, agent permissions | 7 | **operational** |
| [`database/`](database/README.md) | Schema truth, migration design, pre-flight drills, safe execution, rollback and integrity verification | 5 | **operational** |
| [`cost-engineering/`](cost-engineering/README.md) | Cost attribution, waste diagnosis, safe optimisation, guardrails and unit economics | 4 | **operational** |
| [`payments/`](payments/README.md) | Money representation and invariants, idempotency and unknown outcomes, reconciliation | 3 | **operational** |
| [`web3/`](web3/README.md) | Contract threat model, key custody, upgrade and storage migration, exploit response | 4 | **operational** |
| [`mobile/`](mobile/README.md) | Store release and phased rollout, crash triage, client-version compatibility | 3 | **operational** |
| [`embedded-iot/`](embedded-iot/README.md) | Firmware OTA with rollback, fleet health and remote recovery | 2 | **operational** |
| [`backend/`](backend/README.md) | Service implementation, API design, data, reliability | 8 | skeleton |
| [`frontend/`](frontend/README.md) | UI architecture, state, accessibility, polish | 8 | skeleton |
| [`devops-infra/`](devops-infra/README.md) | Infrastructure, IaC, pipelines, observability setup | 8 | skeleton |
| [`data-engineering/`](data-engineering/README.md) | Pipeline reliability, data tests and contracts, backfill and reconciliation | 2 | **operational** |
| [`data-ml-ai/`](data-ml-ai/README.md) | ML problem framing, features, evaluation, deployment (pipelines moved to `data-engineering/`) | 8 | skeleton |
| [`games/`](games/README.md) | Game design, architecture, vertical slice, playtest; save migration and netcode | 10 | mixed (2 operational, 8 skeleton) |

## Developed domains and why these first

Six domains are operational: `ai-agentic`, `database`, `cost-engineering`, `payments`, `web3`, `mobile`, `embedded-iot` (seven counting `games`'s two operational stages). They were promoted in order of **consequence of failure**, not popularity:

- `ai-agentic` — failure is fluent and silent; general engineering intuition does not cover non-determinism or untrusted prose input.
- `web3` — failure is irreversible and adversarial; a key or storage-layout mistake is a permanent loss.
- `mobile` — the client cannot be rolled back and a third party gates the release.
- `embedded-iot` — recovery requires physical access; a bad image is a ladder and a technician.
- `games` — saves and netcode are where players lose progress and trust.
- `data-engineering` — a broken pipeline does not throw; it writes an empty partition and the dashboard keeps rendering.

`backend`, `frontend`, `devops-infra`, and `data-ml-ai` remain skeletons: their sequences are sound, but writing them to the operational bar (evidence rules, verification, failure handling) is still outstanding. Coverage per scenario is tracked in [`_meta/coverage-matrix.md`](../_meta/coverage-matrix.md).

## What these skeletons are good for today

- Structuring a human-led design session (the stage sequence is sound).
- Ensuring a review covers the areas that domain tends to skip (e.g. frontend skeleton's accessibility stage, backend's idempotency stage).
- As a checklist before using a deeper system from another folder.

They are not safe for unsupervised agent execution: they lack verification, evidence rules, and failure handling, and the validator marks them accordingly.

## Still missing

Desktop and CLI tooling and hardware/EDA work have **no system at all**. Mobile and embedded/firmware were closed in 2.15.0; these three remain real gaps rather than omissions by accident, and are recorded in the backlog. Creating a folder with three-line prompts would make the library look more complete and be less useful.

## Boundaries

- Contributing to someone else's web/web3/package project → `01-contribution/`.
- Auditing or recovering your own system → `02-engineering/`.
- Release, observability, and testing practice → `04-process/`.
