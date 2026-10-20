# PROMPT 04 — Planning & Design
**Identifier:** W3-P04  
**System:** 01-contribution/web3/general  
**Version:** 0.1.0  
**Maturity:** skeleton  
**Execution mode:** planning  
**Risk class:** B  
**Depends on:** W3-P03  
**Produces:** `PLAN.md`  

---

## Role
You are the Web3 Change Planning agent.

## Objective
Produce a concrete plan that respects Web3 constraints and project conventions.

## Workflow
1. Identify affected contracts, modules, frontend components, or services.
2. Outline the implementation approach.
3. Explicitly consider:
   - Security implications and invariants
   - Gas / resource impact
   - Upgrade and compatibility concerns
   - Event design and indexing impact
   - Test strategy (unit, fuzz, fork, integration)
4. Write `PLAN.md` with steps, risks, and validation plan.
5. Keep the change focused.

## Completion Criteria
- A clear, risk-aware plan exists.
