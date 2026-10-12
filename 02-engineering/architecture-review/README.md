# Architecture Review System

**Status:** Operational (v1.0)  
**Entry Point:** [`P07-Orchestrator/P07-Architecture-Review-Orchestrator.md`](P07-Orchestrator/P07-Architecture-Review-Orchestrator.md)

A focused, professional multi-stage system for evaluating the architecture of an existing system and producing clear, prioritized recommendations.

This is lighter and more decision-oriented than the full Deep Codebase Audit. It concentrates on structural fitness, quality attributes, risks, and actionable architectural guidance.

## Stages

| ID | Prompt | Purpose |
|----|--------|---------|
| AR-P01 | Context & Goals | Understand purpose, constraints, and review objectives |
| AR-P02 | Current Architecture | Capture the as-is architecture accurately |
| AR-P03 | Quality Attributes | Identify critical quality attributes and scenarios |
| AR-P04 | Evaluation | Assess fitness, risks, and trade-offs |
| AR-P05 | Recommendations | Produce concrete architectural recommendations |
| AR-P06 | Roadmap | Prioritize and sequence the recommendations |
| AR-P07 | Master Orchestrator | Coordinates the review |

## Principles

- Focus on architecture (structure, boundaries, quality attributes, risks) rather than line-by-line code quality.
- Make trade-offs explicit.
- Prefer recommendations that are incremental and justified.
- Output should be useful to both technical leads and decision-makers.
