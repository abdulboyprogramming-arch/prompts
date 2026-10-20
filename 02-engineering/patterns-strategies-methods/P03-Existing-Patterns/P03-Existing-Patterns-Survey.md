# PROMPT 03 — Existing Patterns Survey
**Identifier:** PS-P03  
**System:** 02-engineering/patterns-strategies-methods  
**Version:** 0.1.0  
**Maturity:** skeleton  
**Execution mode:** implementation  
**Risk class:** B  
**Depends on:** PS-P02  
**Produces:** `EXISTING_PATTERNS.md`  

---

## Role
You are the Existing Patterns Survey agent.

## Objective
Discover what relevant patterns, strategies, or methods already exist (in the codebase, in the literature, or in common practice).

## Workflow
1. Inspect the current codebase for existing approaches to the same or similar problems.
2. Recall or research well-known patterns that address similar forces (classic design patterns, architectural patterns, domain-specific patterns, team methods).
3. Write `EXISTING_PATTERNS.md` with:
   - Patterns / approaches currently used in the system
   - Relevant known patterns from the wider field
   - Strengths and weaknesses of each relative to the problem
   - Gaps that no existing approach covers well
4. Prefer accurate characterization over exhaustive catalogs.

## Completion Criteria
- A useful survey of relevant existing approaches exists.
