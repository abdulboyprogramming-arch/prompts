# Prompt Archive Taxonomy

**Version:** 2.0.0
**Status:** current. Changes require updating this file and `_meta/CATALOG.md`.

## Primary axes

Every prompt has a **stable identity** (its `Identifier`) and five attributes that locate it without relying on the folder name alone:

1. **Purpose / activity** — what the user is trying to accomplish.
2. **Technical domain** — the system or technology context.
3. **Execution mode** — diagnostic, planning, implementation, audit-remediation, autonomous-completion, research, continuous-improvement, orchestration, specialised.
4. **Risk class** — A read-only, B local mutation, C external side effect, D high-risk.
5. **Maturity** — skeleton, draft, operational, canonical.

Purpose and domain determine the folder; mode, risk, and maturity are declared in the file's metadata block and aggregated in the catalog. This keeps the directory tree navigable without creating a folder per combination.

## Top-level categories

| Code | Name | Contains | Maturity expectation |
|------|------|----------|----------------------|
| `00-core` | Core primitives | Safety, orchestration, base system prompt, prompt-engineering references | Operational (reference material) |
| `01-contribution` | Contribution | Adding value to existing projects: open source, packages, web, web3, language design | One operational system; others skeleton |
| `02-engineering` | Engineering | Audits, architecture, refactoring, migration, performance, security, project recovery, from-scratch | Mixed |
| `03-domains` | Domains | Deep technology systems: backend, frontend, devops, data/ML, games, AI/agentic | Mixed; backend/frontend/devops/data/games are skeleton |
| `04-process` | Process | Testing, code review, documentation, project management, research, observability, release engineering | Mixed |
| `05-scenarios` | Scenarios | Single-purpose prompts for common situations | Operational for debugging, incident, flaky tests; others draft/skeleton |
| `06-interactive` | Interactive | Intake prompts and wizards that collect context | Draft |
| `07-workflows` | Workflows | Composed multi-system sequences with gates and handoff contracts | Draft |
| `_meta` | Library standards | Authoring standard, rubric, templates, catalog, roadmap, review log | Operational |
| `archive` | Archive | Superseded source material (legacy .txt) | Retained, not maintained |
| `scripts` | Tooling | Validator and catalog generator | Operational |

## 01-contribution sub-taxonomy

- `open-source/general-agent` — the developed 16-stage autonomous contribution system.
- `packages-libraries` — API/compatibility-sensitive contribution.
- `web/general`, `web3/general` — framework-family contribution (skeleton).
- `language-design` — designing or extending a language (skeleton).

Rule: if the work is about *understanding or changing an existing system you own*, it belongs in `02-engineering`, not here. `01-contribution` is for contributing to someone else's project under their governance.

## 02-engineering sub-taxonomy

| Folder | Purpose | Maturity |
|--------|---------|----------|
| `codebase-audit` | Evidence-based audit: structure → architecture → quality → tests/deps → security/docs → findings → roadmap | Operational |
| `project-recovery` | Preserve, reconstruct, complete, and accept an inherited or interrupted project | Operational |
| `architecture-review` | Focused architectural evaluation and recommendations | Skeleton |
| `refactoring` | Safe incremental restructuring | Skeleton |
| `rewriting-migration` | Language/paradigm migration and rewrite planning | Skeleton |
| `feature-design-suggestion` | Designing new features for existing systems | Skeleton |
| `from-scratch` | Greenfield construction | Skeleton |
| `patterns-strategies-methods` | Inventing or improving patterns and methods | Skeleton |
| `performance` | Performance analysis and optimisation | Skeleton |
| `security-hardening` | Security assessment and hardening | Skeleton |

## 03-domains sub-taxonomy

`backend`, `frontend`, `devops-infra`, `data-ml-ai`, `games`, `ai-agentic` (operational). Domain systems hold technology-specific practice; cross-cutting activities stay in `02-engineering` or `04-process`.

Web3 contribution lives in `01-contribution/web3`; there is no `03-domains/web3` until a deep domain system exists. Do not create an empty folder in advance.

## 04-process sub-taxonomy

`testing-qa` (operational), `observability-reliability` (operational), `release-engineering` (operational), `code-review`, `documentation`, `project-management`, `research-and-development`, `systems-building-improvement` (skeletons).

## 05-scenarios

Single-file, high-utility prompts: debugging, incident response, flaky tests, legacy code, onboarding, performance investigation, PR authoring, quick fixes. Scenario prompts may be promoted into a system if they grow stage structure.

## 07-workflows

Composed sequences referencing systems across folders. Each workflow declares stages, gates, failure routing, and acceptance criteria, and uses `HANDOFF-CONTRACT.md`. Workflows do not duplicate prompt content.

## Naming conventions

- Folders: `kebab-case`; stage folders `P<NN>-Short-Name`.
- Prompt files: `P<NN>-Descriptive-Name.md`; standalone scenario prompts `UPPER-KEBAB-CASE.md`.
- Every multi-stage system has `README.md` with a stage table showing **actual maturity**.
- Identifiers: `<SYSTEM-PREFIX>-P<NN>`, globally unique, retired rather than reused.

## Evolution rules

1. Prefer deepening an existing system to creating a new one.
2. A new system must justify a gap that no existing system covers, and must ship at `operational` or be labelled `skeleton` from the start.
3. Never add a stage stub without adding it to the system README with maturity `skeleton`.
4. Promote maturity only with a review record in `_meta/review-log.md`.
5. When restructuring, update: system README, catalog, affected workflows, and this file — in the same change.
6. Retire, do not delete, material that carries historical intent; move it to `archive/` with a note.
