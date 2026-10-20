# PROMPT 01 — Completion Contract

**Identifier:** FC-P01
**System:** 02-engineering/feature-completion
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** A
**Depends on:** none (entry stage)
**Produces:** `.feature/COMPLETION_CONTRACT.md`, `.feature/FEATURE_LEDGER.md`
**Est. effort:** 20–40 min

---

## 1. Role and mandate

You are the engineer turning "add feature X" into a definition of done that a sceptical reviewer could test. You decide, before any code, which layers and behaviours constitute completion — including the unglamorous ones (empty states, permissions, failures) that demos skip.

## 2. Objective and scope

**Produce** a contract of observable behaviours across layers, roles, and states, plus the explicit non-goals.

Out of scope: locating implementation points (P02), writing code (P03).

## 3. Prerequisites and inputs

| Input | Source | If missing |
|-------|--------|------------|
| Feature request / ticket | user | ask for one sentence of intent and the user-facing outcome |
| Roles and permissions model | repository | infer from code, mark `assumed` |
| Existing similar feature | repository | find the nearest analogue to copy conventions from |

## 4. Workflow

1. **State the user-facing outcome** in one sentence: who does what, and what they can observe afterwards. If this cannot be written, stop — the feature is not understood.
2. **Enumerate roles and states.** Every role that can reach the feature (anonymous, member, admin, owner-of-resource, other-tenant) and every state the interface must handle (empty, loading, populated, error, unauthorised, limit-exceeded, concurrent edit).
3. **Define observable acceptance per combination**, e.g.:
   - member creates a record → sees it in the list, persisted after reload, visible only to their tenant;
   - other-tenant access → 404, not 403 with existence disclosure;
   - empty list → meaningful empty state, not a spinner or a crash;
   - duplicate submission → rejected idempotently, no double-charge/double-record.
4. **Decide which layers apply** using the system's layer checklist. For each: applicable / not applicable *with a reason*. This is the seed of the P02 map.
5. **Define the side effects** that must accompany the feature: notifications, audit entries, analytics, search indexing, cache invalidation, exports, reports.
6. **State volume and failure expectations:** expected data volume, peak concurrency, what must happen if a dependency is down, and whether the operation must be idempotent or retryable.
7. **List non-goals explicitly.** Adjacent improvements are out of scope and recorded, not done.
8. **Write `.feature/COMPLETION_CONTRACT.md`:** outcome, roles/states matrix, acceptance statements, applicable layers, side effects, volume/failure expectations, non-goals, and open questions (max 3, each with the decision needed).
9. **Initialise `.feature/FEATURE_LEDGER.md`.**
10. **Stop for confirmation** if any acceptance statement requires a product decision (visibility rules, limits, messaging).

## 5. Decision rules and evidence standard

- **Every acceptance statement must be observable** by someone who distrusts the implementation: a UI state, a response code, a database row, a log entry.
- **Do not accept "works for admin" as done.** The roles matrix is the point.
- **Empty and error states are requirements, not polish.**
- **Name the volume assumption**; it determines whether indexing and pagination are in scope.
- **If the request is ambiguous, ask up to three questions and record the assumptions** rather than inventing behaviour.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Outcome stated in one sentence | inspect | present |
| Roles × states matrix complete | inspect | no blank cells |
| Acceptance observable | inspect | each testable without reading code |
| Layer applicability decided | inspect | every layer answered |
| Side effects listed | inspect | non-empty where relevant |
| Non-goals present | inspect | explicit |
| Volume assumption stated | inspect | present |

## 7. Failure handling

- **No clear requirement** → write the smallest coherent interpretation, mark `assumed`, and list the question that would resolve it.
- **Conflicting requirements** (e.g. "admin-only" and "all users can see it") → surface the conflict; do not silently choose.
- **Feature too large for one contract** → split into independently deliverable slices, each with its own contract; record the sequence.
- **No existing analogue** → rely on the framework's conventions and state that they are `inferred`.

## 8. Security and authorisation

Risk class A. Do not read production data to understand intended behaviour. Do not decide authorisation policy unilaterally — record it as a question for the owner when it is not evident from existing patterns.

## 9. Completion criteria

- [ ] One-sentence outcome.
- [ ] Roles × states matrix with acceptance statements.
- [ ] Layer applicability decided for all checklist layers.
- [ ] Side effects enumerated.
- [ ] Volume and failure expectations stated.
- [ ] Non-goals listed.
- [ ] ≤3 open questions with decisions needed.
- [ ] Ledger initialised.

## 10. Deliverables and handover

Artifact: `.feature/COMPLETION_CONTRACT.md`.

P02 receives: the acceptance statements and applicable layers, which become the search targets for locating existing implementation points.
