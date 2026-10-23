# Feature Design & Suggestion System

**Status:** Skeleton — 7 stage outlines (skeleton 7). The stages name a sensible sequence but lack the evidence rules, verification, and failure handling that this library requires of `operational`. Treat the system as a plan, not a procedure; see [`_meta/ROADMAP-AND-BACKLOG.md`](../../_meta/ROADMAP-AND-BACKLOG.md).
**Entry Point:** [`P07-Orchestrator/P07-Feature-Design-Orchestrator.md`](P07-Orchestrator/P07-Feature-Design-Orchestrator.md)

A structured system for turning vague feature ideas or user needs into clear, well-reasoned, implementable feature proposals.

**Before this system, decide whether the feature should exist.** These stages design a feature once it has been
chosen. When the input is a *list* of wanted capabilities and capacity for two of them, the step that is missing
is [`02-engineering/feature-portfolio/`](../feature-portfolio/FEATURE-PORTFOLIO.md) (`PORTFOLIO-01`): it checks the
repository for half-built versions, restates each candidate as a user problem, and returns one item with a
reason — which is the input `FD-P01` wants.

## Stages

| ID | Prompt | Purpose |
|----|--------|---------|
| FD-P01 | Context Gathering | Understand the product, users, and current system |
| FD-P02 | Problem Framing | Clearly define the problem worth solving |
| FD-P03 | Ideation | Generate and explore possible approaches |
| FD-P04 | Design | Shape the preferred solution |
| FD-P05 | Trade-offs & Risks | Explicitly evaluate alternatives and downsides |
| FD-P06 | Specification | Produce a concrete, reviewable feature spec |
| FD-P07 | Master Orchestrator | Coordinates the design process |

## Principles

- Start from user/problem value, not from cool technology.
- Make trade-offs visible.
- Prefer designs that fit the existing architecture unless a deliberate change is justified.
- Output should be usable by implementers and decision-makers.
