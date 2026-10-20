# Performance Analysis & Optimization System

**Status:** Skeleton — 7 stage outlines (skeleton 7). The stages name a sensible sequence but lack the evidence rules, verification, and failure handling that this library requires of `operational`. Treat the system as a plan, not a procedure; see [`_meta/ROADMAP-AND-BACKLOG.md`](../../_meta/ROADMAP-AND-BACKLOG.md).
**Entry Point:** [`P07-Orchestrator/P07-Performance-Orchestrator.md`](P07-Orchestrator/P07-Performance-Orchestrator.md)

A disciplined multi-stage system for measuring, analyzing, and improving software performance in a focused, evidence-based way.

## Stages

| ID | Prompt | Purpose |
|----|--------|---------|
| PERF-P01 | Context & Goals | Define performance objectives and constraints |
| PERF-P02 | Measurement Setup | Establish baselines and reliable measurement methods |
| PERF-P03 | Analysis | Understand current performance characteristics |
| PERF-P04 | Bottleneck Identification | Locate the real limiting factors |
| PERF-P05 | Optimization Design | Design targeted, high-leverage improvements |
| PERF-P06 | Implementation & Validation | Apply changes and prove improvement |
| PERF-P07 | Master Orchestrator | Coordinates the full performance work |

## Principles

- Measure before and after. Avoid optimizing based on intuition alone.
- Focus on the highest-impact bottlenecks first.
- Preserve correctness and maintainability.
- Prefer simple, proven techniques over premature or exotic optimizations.
- Make trade-offs (complexity, readability, resource usage) explicit.
