# Rewriting & Language Migration System

**Status:** Skeleton — 8 stage outlines (skeleton 8). The stages name a sensible sequence but lack the evidence rules, verification, and failure handling that this library requires of `operational`. Treat the system as a plan, not a procedure; see [`_meta/ROADMAP-AND-BACKLOG.md`](../../_meta/ROADMAP-AND-BACKLOG.md).
**Entry Point:** [`P08-Orchestrator/P08-Rewriting-Migration-Orchestrator.md`](P08-Orchestrator/P08-Rewriting-Migration-Orchestrator.md)

A disciplined multi-stage system for safely rewriting systems or migrating them to a new language, framework, or major paradigm.

## Stages

| ID | Prompt | Purpose |
|----|--------|---------|
| RW-P01 | Assessment & Goals | Understand why rewrite/migrate and what success looks like |
| RW-P02 | Target Design | Define the desired end-state architecture and technology |
| RW-P03 | Migration Strategy | Choose approach (strangler, big-bang, incremental modules, etc.) |
| RW-P04 | Safety Net | Characterization tests and behavioral locks |
| RW-P05 | Incremental Migration | Execute the migration in verified steps |
| RW-P06 | Validation | Prove behavioral equivalence and quality |
| RW-P07 | Cleanup & Cutover | Remove old code, finalize docs, complete transition |
| RW-P08 | Master Orchestrator | Coordinates the entire process |

## Core Principles

- Prefer incremental, reversible progress over risky big-bang rewrites when possible.
- Lock behavior with tests before changing implementation.
- Make the target design explicitly better, not just different.
- Track parity and risk throughout.
- Document decisions and remaining gaps.
