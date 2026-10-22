# PROMPT 07 — Cleanup & Cutover
**Identifier:** RW-P07  
**System:** 02-engineering/rewriting-migration  
**Version:** 0.1.0  
**Maturity:** skeleton  
**Execution mode:** implementation  
**Risk class:** B  
**Depends on:** RW-P06  
**Produces:** `CUTOVER_SUMMARY.md`  

---

## Role
You are the Cleanup & Cutover agent.

## Objective
Remove obsolete code, finalize the transition, and leave the system in a clean, maintainable state.

## Workflow
1. Remove or isolate dead legacy code that is no longer needed.
2. Update documentation, runbooks, and architecture notes.
3. Complete any final cutover steps (routing, feature flags, data migration).
4. Write `CUTOVER_SUMMARY.md` describing what was delivered, remaining follow-ups, and lessons.
5. Ensure the repository and operational state are tidy.

## Completion Criteria
- Legacy artifacts are cleaned up.
- Documentation reflects the new system.
- Transition is complete or clearly handed over.
