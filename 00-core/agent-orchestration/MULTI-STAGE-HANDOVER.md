# Multi-Stage Handover Protocol

**Version:** 1.0.0  
**Type:** Core Orchestration Primitive  

---

## Purpose
Ensure long workflows remain coherent across stages and sessions.

## Required Handover Contents

Each completed stage should leave:

1. **Artifacts produced** — files, reports, plans, diffs
2. **Decisions made** — with brief rationale
3. **Open questions** — only if blocking
4. **Next stage recommendation** — exact next prompt/system ID
5. **Risks / residual uncertainty**

## Progress Ledger Pattern

Maintain a durable `PROGRESS.md` (or equivalent) with:

| Stage | Status | Key outputs | Notes |
|-------|--------|-------------|-------|
| ... | not started / in progress / done / blocked | ... | ... |

## Resume Rules
- On resume, read the ledger and latest artifacts before continuing.
- Do not redo completed stages unless new evidence invalidates them.
- If blocked, state the blocker and the smallest action needed from the user.
