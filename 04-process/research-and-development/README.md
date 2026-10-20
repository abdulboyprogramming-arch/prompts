# Research & Development Process System

**Status:** Skeleton — 8 stage outlines (skeleton 8). The stages name a sensible sequence but lack the evidence rules, verification, and failure handling that this library requires of `operational`. Treat the system as a plan, not a procedure; see [`_meta/ROADMAP-AND-BACKLOG.md`](../../_meta/ROADMAP-AND-BACKLOG.md).
**Entry Point:** [`P08-Orchestrator/P08-Research-Development-Orchestrator.md`](P08-Orchestrator/P08-Research-Development-Orchestrator.md)

A multi-stage system for running focused technical R&D: turning uncertainty into evidence-backed decisions.

Use this when you need to:
- Evaluate a new technology, architecture, or approach
- Reduce uncertainty before a major build commitment
- Compare alternatives with experiments rather than opinions
- Produce a clear go / no-go / iterate recommendation

## Stages

| ID | Prompt | Purpose |
|----|--------|---------|
| RD-P01 | Research Question | Define the decision and success criteria |
| RD-P02 | Background Survey | Gather relevant prior art and constraints |
| RD-P03 | Hypotheses | State testable hypotheses and alternatives |
| RD-P04 | Method Design | Design experiments / spikes / measurements |
| RD-P05 | Experimentation | Run the investigation and collect evidence |
| RD-P06 | Analysis | Interpret results against criteria |
| RD-P07 | Decision & Next Steps | Recommend action and residual risks |
| RD-P08 | Master Orchestrator | Coordinates the full R&D process |

## Principles

- Start from a decision that matters.
- Prefer small, discriminating experiments over vague exploration.
- Separate facts, inferences, and opinions.
- Optimize for decision quality, not research theater.
- Time-box spikes and record what was *not* learned.
