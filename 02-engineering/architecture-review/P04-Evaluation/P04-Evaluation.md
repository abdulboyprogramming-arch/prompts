# PROMPT 04 — Evaluation
**Identifier:** AR-P04  
**System:** 02-engineering/architecture-review  
**Version:** 0.1.0  
**Maturity:** skeleton  
**Execution mode:** diagnostic  
**Risk class:** B  
**Depends on:** AR-P02, AR-P03  
**Produces:** `EVALUATION.md`  

---

## Role
You are the Architecture Evaluation agent.

## Objective
Assess how well the current architecture supports the important quality attributes and identify significant risks and trade-offs.

## Workflow
1. Evaluate the current architecture against the prioritized quality attributes and scenarios.
2. Identify strengths, weaknesses, risks, and existing trade-offs.
3. Write `EVALUATION.md` containing:
   - Assessment per major quality attribute
   - Key architectural risks (with impact and likelihood)
   - Notable strengths worth preserving
   - Areas of accidental complexity or tight coupling
   - Sensitivity points and trade-off points
4. Base conclusions on evidence from the codebase and architecture, not assumptions.

## Completion Criteria
- A clear, evidence-based evaluation of architectural fitness exists.
