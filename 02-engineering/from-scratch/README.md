# From-Scratch Project System

**Status:** Skeleton — 8 stage outlines (skeleton 8). The stages name a sensible sequence but lack the evidence rules, verification, and failure handling that this library requires of `operational`. Treat the system as a plan, not a procedure; see [`_meta/ROADMAP-AND-BACKLOG.md`](../../_meta/ROADMAP-AND-BACKLOG.md).
**Entry Point:** [`P08-Orchestrator/P08-From-Scratch-Project-Orchestrator.md`](P08-Orchestrator/P08-From-Scratch-Project-Orchestrator.md)

A complete multi-stage system for designing and building high-quality software projects from zero.

## Stages

| ID | Prompt | Purpose |
|----|--------|---------|
| FS-P01 | Vision & Requirements Clarification | Goals, users, constraints, success criteria |
| FS-P02 | High-Level Architecture | System shape, major components, data flow |
| FS-P03 | Stack & Tooling Decision | Language, frameworks, infrastructure choices with rationale |
| FS-P04 | Project Scaffolding | Repository structure, tooling, CI skeleton, initial config |
| FS-P05 | Core Implementation | Implement the essential vertical slices |
| FS-P06 | Testing & Quality | Tests, linting, type safety, basic CI |
| FS-P07 | Documentation & Polish | README, usage, architecture notes, final cleanup |
| FS-P08 | Master Orchestrator | Coordinates the entire creation process |

## Design Principles

- Start from clear intent, not from technology.
- Make deliberate, documented stack decisions.
- Prefer boring, proven technology unless the problem demands otherwise.
- Deliver a working, well-structured, documented foundation rather than a half-finished feature explosion.
- Keep the system adaptable to web apps, CLIs, libraries, services, and internal tools.
