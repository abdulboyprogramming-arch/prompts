# Safe Refactoring System

**Status:** Operational (v1.0)  
**Entry Point:** [`P07-Orchestrator/P07-Safe-Refactoring-Orchestrator.md`](P07-Orchestrator/P07-Safe-Refactoring-Orchestrator.md)

A disciplined, multi-stage system for performing safe, incremental, high-quality refactorings on existing codebases.

## Stages

| ID | Prompt | Purpose |
|----|--------|---------|
| REF-P01 | Assessment & Goal Clarification | Understand current pain and desired outcome |
| REF-P02 | Refactoring Strategy | Choose approach, scope, and sequence |
| REF-P03 | Safety Net | Ensure tests and characterization coverage exist |
| REF-P04 | Execution | Perform the refactoring in small, verified steps |
| REF-P05 | Validation | Confirm behavior is preserved and quality improved |
| REF-P06 | Cleanup & Documentation | Final polish and knowledge capture |
| REF-P07 | Master Orchestrator | Coordinates the entire safe refactoring process |

## Core Principles

- Behavior preservation is non-negotiable.
- Prefer small, reversible steps with verification after each.
- Build or strengthen the safety net before changing structure.
- Make the code obviously better, not just different.
- Record decisions and trade-offs.
