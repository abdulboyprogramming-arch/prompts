# 02-Engineering

Engineering activities that apply across technologies: understanding a system, changing it safely, and recovering it when someone else left it half-finished.

## Systems

| Folder | Purpose | Stages | Maturity |
|--------|---------|-------:|----------|
| [`codebase-audit/`](codebase-audit/README.md) | Evidence-based audit → validated findings → roadmap and report | 9 | **operational** |
| [`project-recovery/`](project-recovery/README.md) | Preserve, reconstruct, complete, and accept an inherited or interrupted project | 7 | **operational** |
| [`architecture-review/`](architecture-review/README.md) | Architectural evaluation and recommendations | 7 | skeleton |
| [`refactoring/`](refactoring/README.md) | Safe incremental restructuring | 7 | skeleton |
| [`rewriting-migration/`](rewriting-migration/README.md) | Language/paradigm migration and rewrite planning | 8 | skeleton |
| [`feature-design-suggestion/`](feature-design-suggestion/README.md) | Designing features for existing systems | 7 | skeleton |
| [`from-scratch/`](from-scratch/README.md) | Greenfield construction | 8 | skeleton |
| [`patterns-strategies-methods/`](patterns-strategies-methods/README.md) | Inventing or improving patterns and methods | 7 | skeleton |
| [`performance/`](performance/README.md) | Performance analysis and optimisation | 7 | skeleton |
| [`security-hardening/`](security-hardening/README.md) | Authorised review, triaged findings, proven remediation | 7 | **operational** |

## What "skeleton" means here

A skeleton system has a sound stage sequence and named artifacts, but each stage is a 20–40 line outline: no evidence standard, no verification that can fail, no failure handling. Use it to structure a human-led session. Do not hand it to an agent and expect disciplined autonomy.

## Choosing between the operational systems

- **"What is wrong with this codebase, and in what order do we fix it?"** → `codebase-audit/`. Read-only, produces findings and a roadmap.
- **"This project is supposed to work and does not."** → `project-recovery/`. Preserves state first, then reconstructs intent, then completes the critical path and proves it.
- **Both.** When you do not know whether the project is unsound or merely unfinished, run recovery P01–P03 first: it is cheaper and answers "what exists". Run the audit afterwards if quality or security is in question. Composition: `07-workflows/recover-abandoned-project.md`.

## Cross-cutting rules

- Audits diagnose; recovery completes; neither is a licence to refactor broadly.
- Every system that writes files declares risk class `B` and confines artifacts to a dot-directory (`.audit/`, `.recovery/`).
- Security findings follow responsible disclosure: enough detail to fix, no weaponised payloads.

## Planned

New systems with no home yet (database engineering, dependency management, mobile, embedded) are tracked in [`_meta/ROADMAP-AND-BACKLOG.md`](../_meta/ROADMAP-AND-BACKLOG.md). Do not create empty folders for them in advance.
