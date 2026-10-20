# Code Review Process System

**Status:** Operational (v1.0)  
**Entry Point:** [`P06-Orchestrator/P06-Code-Review-Orchestrator.md`](P06-Orchestrator/P06-Code-Review-Orchestrator.md)

A focused multi-stage system for performing high-quality, constructive code reviews.

## Stages

| ID | Prompt | Purpose |
|----|--------|---------|
| CR-P01 | Context & Goals | Understand the change purpose and review expectations |
| CR-P02 | Change Understanding | Build an accurate mental model of the diff |
| CR-P03 | Structured Review | Evaluate correctness, design, risk, and maintainability |
| CR-P04 | Feedback Crafting | Produce clear, actionable, respectful feedback |
| CR-P05 | Follow-up Support | Help resolve discussion and verify updates |
| CR-P06 | Master Orchestrator | Coordinates the review process |

## Principles

- Prioritize correctness and risk over style nits.
- Be specific and actionable.
- Distinguish blocking issues from suggestions.
- Assume positive intent.
- Prefer questions when intent is unclear.
- Help the author improve the change and the codebase.
