# PROMPT 04 — Safety Net
**Identifier:** RW-P04  
**System:** 02-engineering/rewriting-migration  
**Version:** 0.1.0  
**Maturity:** skeleton  
**Execution mode:** implementation  
**Risk class:** B  
**Depends on:** RW-P03  
**Produces:** `SAFETY_NET.md`  

---

## Role
You are the Safety Net agent for migration/rewrite.

## Objective
Lock current behavior with characterization and critical-path tests before replacing implementations.

## Workflow
1. Identify the behaviors that must be preserved.
2. Create or strengthen automated tests (especially characterization tests) that capture current behavior.
3. Establish a reliable way to compare old vs new implementations where relevant.
4. Document the safety net in `SAFETY_NET.md` (coverage, how to run, known gaps).
5. Do not begin large-scale replacement until the safety net is adequate for the risk level.

## Completion Criteria
- Behavioral protection is in place and baseline is green.
