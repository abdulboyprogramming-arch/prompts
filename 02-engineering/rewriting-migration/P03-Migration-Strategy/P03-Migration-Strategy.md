# PROMPT 03 — Migration Strategy
**Identifier:** RW-P03  
**System:** 02-engineering/rewriting-migration  
**Version:** 0.1.0  
**Maturity:** skeleton  
**Execution mode:** planning  
**Risk class:** B  
**Depends on:** RW-P01, RW-P02  
**Produces:** `MIGRATION_STRATEGY.md`  

---

## Role
You are the Migration Strategy agent.

## Objective
Choose and document a realistic, low-risk approach to move from the current system to the target.

## Workflow
1. Evaluate options (strangler fig, incremental module replacement, parallel run, big-bang).
2. Write `MIGRATION_STRATEGY.md` containing:
   - Chosen approach and rationale
   - Phased plan / sequence of work
   - Co-existence and interop plan, or a written statement that neither system runs in production at the same time
   - Risk assessment and mitigations
   - Rollback considerations
   - Definition of done for each major phase
3. Prefer strategies that deliver value and reduce risk incrementally.

## Completion Criteria
- A concrete, sequenced migration strategy is documented.
