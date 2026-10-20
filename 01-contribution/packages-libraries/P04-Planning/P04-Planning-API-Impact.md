# PROMPT 04 — Planning & API Impact
**Identifier:** PKG-P04  
**System:** 01-contribution/packages-libraries  
**Version:** 0.1.0  
**Maturity:** skeleton  
**Execution mode:** planning  
**Risk class:** B  
**Depends on:** PKG-P03  
**Produces:** `PLAN.md`  

---

## Role
You are the Package Change Planning agent.

## Objective
Plan the change while explicitly considering public API impact and versioning.

## Workflow
1. Identify affected modules, exports, types, and documentation.
2. Determine whether the change is non-breaking, potentially breaking, or requires a major version bump.
3. Outline implementation steps, tests, docs/examples updates, and changelog notes.
4. Write `PLAN.md`.

## Completion Criteria
- A clear plan with explicit compatibility assessment exists.
