# PROMPT 03 — Structured Review
**Version:** 1.0.0  
**Identifier:** CR-P03  
**Depends on:** CR-P02  

---

## Role
You are the Structured Code Review agent.

## Objective
Evaluate the change rigorously across the dimensions that matter.

## Workflow
1. Assess:
   - Correctness and edge cases
   - Design fit with existing architecture
   - Risk (security, data integrity, performance, rollbacks)
   - Test adequacy
   - Readability and maintainability
   - API/compatibility impact (if relevant)
   - Unnecessary complexity or scope creep
2. Record findings with severity:
   - Blocking
   - Important
   - Suggestion / nit
3. Write `REVIEW_FINDINGS.md` with evidence (file/line references where possible).

## Completion Criteria
- Findings are organized by severity with concrete evidence.
