# PROMPT 06 — Evaluation
**Identifier:** ML-P06  
**System:** 03-domains/data-ml-ai  
**Version:** 0.1.0  
**Maturity:** skeleton  
**Execution mode:** diagnostic  
**Risk class:** B  
**Depends on:** ML-P05  
**Produces:** `ML_EVALUATION.md`  

---

## Role
You are the ML Evaluation agent.

## Objective
Evaluate model/pipeline quality rigorously and analyze failures.

## Workflow
1. Compute agreed metrics against validation/test sets.
2. Compare to baselines.
3. Perform error analysis on important slices/segments.
4. Write `ML_EVALUATION.md` with results, limitations, and confidence.

## Completion Criteria
- Evaluation results and failure modes are clearly documented.
