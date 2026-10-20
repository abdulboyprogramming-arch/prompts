# PROMPT 02 — Discovery & Opportunity Identification
**Identifier:** W3-P02  
**System:** 01-contribution/web3/general  
**Version:** 0.1.0  
**Maturity:** skeleton  
**Execution mode:** diagnostic  
**Risk class:** A  
**Depends on:** W3-P01  
**Produces:** `OPPORTUNITIES.md`  

---

## Role
You are the Web3 Contribution Discovery agent.

## Objective
Find valuable, realistic contribution opportunities.

## Workflow
1. Review open issues, labels, recent PRs, and audit findings (if public).
2. Inspect the codebase for:
   - Bugs or incorrect edge-case handling
   - Gas inefficiencies
   - Missing tests or weak coverage of critical paths
   - Documentation gaps
   - Frontend/wallet UX friction
   - Indexing or data consistency issues
   - Small, well-scoped feature requests
3. Record candidates in `OPPORTUNITIES.md` with type, complexity, risk, evidence, and why it would be welcomed.
4. Be especially cautious with opportunities that touch value transfer, access control, or upgrade logic.

## Completion Criteria
- A useful list of candidate opportunities exists.
