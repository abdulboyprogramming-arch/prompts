# Language Design & Invention System

**Status:** Skeleton — 8 stage outlines (skeleton 8). The stages name a sensible sequence but lack the evidence rules, verification, and failure handling that this library requires of `operational`. Treat the system as a plan, not a procedure; see [`_meta/ROADMAP-AND-BACKLOG.md`](../../_meta/ROADMAP-AND-BACKLOG.md).
**Entry Point:** [`P08-Orchestrator/P08-Language-Design-Orchestrator.md`](P08-Orchestrator/P08-Language-Design-Orchestrator.md)

A multi-stage system for designing new programming languages, DSLs, or major language extensions — and for contributing thoughtfully to existing language projects.

## Stages

| ID | Prompt | Purpose |
|----|--------|---------|
| LD-P01 | Vision & Motivation | Clarify why a new language or extension is needed |
| LD-P02 | Requirements & Constraints | Define goals, non-goals, and hard constraints |
| LD-P03 | Language Design | Shape syntax, semantics, and core model |
| LD-P04 | Specification | Produce a clear language/spec description |
| LD-P05 | Implementation Plan | Plan compiler/runtime/tooling approach |
| LD-P06 | Prototype | Build a minimal viable implementation slice |
| LD-P07 | Evaluation | Assess design quality, trade-offs, and next steps |
| LD-P08 | Master Orchestrator | Coordinates the full language design process |

## Principles

- Start from a real problem and target users, not from novelty for its own sake.
- Make trade-offs explicit (expressiveness vs simplicity, safety vs flexibility, etc.).
- Prefer a sharp MVP language/feature set over an unbounded design.
- Separate design decisions from implementation accidents.
- Document rationale so future contributors can evolve the language intentionally.
