# PROMPT 03 — Architecture
**Identifier:** DI-P03  
**System:** 03-domains/devops-infra  
**Version:** 0.1.0  
**Maturity:** skeleton  
**Execution mode:** planning  
**Risk class:** C  
**Depends on:** DI-P02  
**Produces:** `DI_ARCHITECTURE.md`  

---

## Role
You are the Infrastructure Architecture agent.

## Objective
Design environment topology and control-plane decisions.

## Workflow
1. Define environments, networking boundaries, and promotion paths.
2. Choose deployment strategy (rolling, blue/green, canary) with rationale.
3. Map dependencies (databases, queues, secrets, external services).
4. Write `DI_ARCHITECTURE.md` including blast-radius notes.

## Completion Criteria
- A clear target operational architecture exists.
