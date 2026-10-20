# 03-Domains

Deep, technology-specific prompt systems. Cross-cutting activities (audits, refactoring, recovery, from-scratch construction) live in `02-engineering/`.

## Systems

| Path | Description | Stages | Maturity |
|------|-------------|-------:|----------|
| [`ai-agentic/`](ai-agentic/README.md) | LLM features and agents: risk, architecture, evaluation, guardrails, production operations | 5 | **operational** |
| [`database/`](database/README.md) | Schema truth, migration design, pre-flight drills, safe execution, rollback and integrity verification | 5 | **operational** |
| [`cost-engineering/`](cost-engineering/README.md) | Cost attribution, waste diagnosis, safe optimisation, guardrails and unit economics | 4 | **operational** |
| [`payments/`](payments/README.md) | Money representation and invariants, idempotency and unknown outcomes, reconciliation | 3 | **operational** |
| [`backend/`](backend/README.md) | Service implementation, API design, data, reliability | 8 | skeleton |
| [`frontend/`](frontend/README.md) | UI architecture, state, accessibility, polish | 8 | skeleton |
| [`devops-infra/`](devops-infra/README.md) | Infrastructure, IaC, pipelines, observability setup | 8 | skeleton |
| [`data-ml-ai/`](data-ml-ai/README.md) | Data pipelines, ML problem framing, evaluation, deployment | 8 | skeleton |
| [`games/`](games/README.md) | Game design, architecture, vertical slice, playtest | 8 | skeleton |

## Why only one domain system is developed

The previous state of this repository consisted of plausible stage outlines for five domains, each about 5 KB in total. Depth requires domain judgement — the specific traps, verification methods, and trade-offs an experienced practitioner would recognise — and that is slow to write well. `ai-agentic/` was developed first because the failure modes there are least covered by general engineering intuition (non-determinism, prompt injection, fluent-but-wrong output).

The promotion order for the remaining domains is in [`_meta/ROADMAP-AND-BACKLOG.md`](../_meta/ROADMAP-AND-BACKLOG.md): backend first, then frontend, then data/ML. Coverage status per scenario is tracked in [`_meta/coverage-matrix.md`](../_meta/coverage-matrix.md).

## What these skeletons are good for today

- Structuring a human-led design session (the stage sequence is sound).
- Ensuring a review covers the areas that domain tends to skip (e.g. frontend skeleton's accessibility stage, backend's idempotency stage).
- As a checklist before using a deeper system from another folder.

They are not safe for unsupervised agent execution: they lack verification, evidence rules, and failure handling, and the validator marks them accordingly.

## Missing domains

Mobile (native and cross-platform), embedded/firmware, desktop and CLI tooling, and data engineering have **no system at all**. These are real gaps, not omissions by accident; creating a folder with three-line prompts would make the library look more complete and be less useful. See the backlog.

## Boundaries

- Contributing to someone else's web/web3/package project → `01-contribution/`.
- Auditing or recovering your own system → `02-engineering/`.
- Release, observability, and testing practice → `04-process/`.
