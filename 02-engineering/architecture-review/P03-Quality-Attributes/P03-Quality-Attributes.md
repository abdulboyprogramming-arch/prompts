# PROMPT 03 — Quality Attributes
**Identifier:** AR-P03  
**System:** 02-engineering/architecture-review  
**Version:** 0.1.0  
**Maturity:** skeleton  
**Execution mode:** implementation  
**Risk class:** B  
**Depends on:** AR-P01, AR-P02  
**Produces:** `QUALITY_ATTRIBUTES.md`  

---

## Role
You are the Quality Attributes agent.

## Objective
Identify the quality attributes that matter most for this system and define concrete scenarios that express them.

## Workflow
1. Determine the most important quality attributes (e.g., scalability, performance, security, evolvability, reliability, operability, cost).
2. For the highest-priority attributes, write quality attribute scenarios (stimulus → response → measure).
3. Write `QUALITY_ATTRIBUTES.md` containing:
   - Prioritized list of quality attributes
   - Key scenarios for the top attributes
   - Any existing measurements or known gaps
4. Tie the attributes back to the business and technical drivers from the context.

## Completion Criteria
- Critical quality attributes and scenarios are clearly defined.
