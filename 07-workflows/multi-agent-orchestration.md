# Workflow — Multi-Agent Orchestration

**Identifier:** WF-MULTIAGENT
**System:** 07-workflows
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** orchestration
**Risk class:** B (C when agents reach shared or production environments)
**Depends on:** the systems each agent runs
**Produces:** `ORCHESTRATION_PLAN.md`, `RUN_LOG.md`, a merged result with per-task verification
**Est. effort:** planning 20–40 min; run varies

---

## 1. Role and mandate

You are the orchestrator. Several agents (or several sessions of one agent) will work on parts of the same problem. Your job is to decompose work so that pieces cannot silently conflict, to give each agent a contract it can be verified against, and to integrate results with the same scepticism you would apply to a stranger's pull request.

**Parallelism is a cost, not a free win.** Coordination overhead, duplicated exploration, contradictory edits, and confident-but-wrong completions all increase with the number of agents. Use multiple agents when the work is genuinely separable or when you need independent verification — not to go faster on tightly coupled code.

## 2. Objective and scope

**Produce** a decomposition with non-overlapping boundaries, per-agent contracts, a shared state protocol, and an integration-and-verification path.

Out of scope: doing the work in one agent (often better), and acting as a substitute for human approval gates.

## 3. Prerequisites and inputs

| Input | If missing |
|-------|------------|
| A goal decomposed into tasks with clear interfaces | do not fan out; you will produce conflicts |
| A single source of truth for shared state (branch, files, plan document) | establish one before starting |
| Verification method per task | the task is not ready to delegate |
| Authority boundaries: what each agent may do (write files, run tests, open PRs, deploy) | assume the minimum and state it |

## 4. Workflow

### Phase 1 — Decide whether to parallelise at all

1. **Check separability.** Parallel agents work when tasks touch disjoint files or disjoint concerns, and their interfaces are defined up front. Classic safe splits: independent research questions, independent test suites, independent modules behind a stated interface, independent review perspectives.
2. **Check the coordination cost.** If the tasks need the same files, the same design decisions, or iterative feedback from each other, a single agent with a sequence will be faster and more coherent. Record the decision to stay sequential — it is a valid outcome of this workflow.
3. **Identify the conflicts you expect**: shared configuration files, shared dependency manifests, shared schema/migrations, shared test fixtures. Each needs an owner.

### Phase 2 — Decompose with contracts

4. **Write one task contract per agent:**

   | Field | Content |
   |-------|---------|
   | Objective | One sentence, verifiable |
   | Owned paths | Files/modules it may modify — nothing else |
   | Forbidden paths | Shared config, manifests, migrations, other agents' areas |
   | Interfaces | Exact signatures/schema it may rely on and must not change |
   | Inputs | Files to read, decisions already made |
   | Deliverable | Artifact + where it goes |
   | Verification | The command/behaviour that proves it worked |
   | Stop conditions | When to stop and report rather than improvise |

5. **Freeze the interfaces first.** Schema, API shapes, function signatures, and event formats are decided once by the orchestrator (or one agent) *before* parallel work. Two agents inventing the same interface produce a merge conflict at the design level, which is the expensive kind.
6. **Assign ownership of the shared files.** Exactly one agent owns dependency manifests, lockfiles, CI config, and migrations for the duration; others request changes. This single rule prevents most multi-agent breakage.
7. **Give each agent the verification command**, so it can prove its own work without asking you. An agent that cannot verify itself returns "done" on faith.

### Phase 3 — Run with a shared state protocol

8. **Establish the state artefacts:**
   - the plan (tasks, owners, status) — one file, orchestrator-owned;
   - a decision log (any interface change, any deviation) — append-only;
   - per-task output locations, so results do not overwrite each other.
9. **Require status reports in a fixed form**: done + evidence, blocked + what is needed, deviated + why. Free-form reports are where "confidently wrong" hides.
10. **Do not let agents negotiate interfaces directly.** Route interface changes through the orchestrator and the decision log; pairwise negotiation among three agents produces an inconsistent design nobody chose.
11. **Check in at boundaries, not continuously.** Verify each completed task against its contract before dependent work starts. A task that fails verification should not unblock its dependents.
12. **Watch for the three pathologies:**
    - **drift** — an agent implementing something adjacent because it seemed necessary (contract violation);
    - **duplication** — two agents solving the same sub-problem differently;
    - **silent assumption** — an agent filling a gap in its contract and not reporting it.

### Phase 4 — Integrate and verify

13. **Integrate in dependency order**, verifying after each merge rather than at the end. A failure after three merges is three times harder to attribute.
14. **Treat each agent's completion claim as a claim.** Run `07-workflows/independent-verification.md` on the integrated result — ideally by an agent that did not write it. At minimum: re-run every verification command yourself.
15. **Audit for cross-agent interference**: files changed by an agent outside its owned paths, duplicated helpers, inconsistent error handling, two migration files with the same timestamp, a lockfile regenerated by two agents.
16. **Run the end-to-end check that no individual agent could run** — the integration journey (`WF-INTEGRATE`). This is precisely the class of defect that parallel work creates.
17. **Record the run log**: tasks, agents, durations, deviations, failed verifications, rework, and what the decomposition got wrong. The log is how the next orchestration is decomposed better.

## 5. Decision rules and evidence standard

- **No parallel work without frozen interfaces.** This is the single highest-leverage rule in the workflow.
- **One owner per shared file.** Contention on manifests and migrations is the most common failure.
- **Verification is per task and per integration.** Agent self-reports are inputs, not evidence.
- **Agents do not expand their own scope.** A discovered necessity is reported, not implemented.
- **Prefer fewer agents.** Three agents on one module is usually worse than one agent and a reviewer.
- **Human gates are not delegated.** Irreversible actions (`SEC-P01` gates, Category C/D) still require the human approval defined elsewhere.
- **If two agents disagree on a fact, resolve it with evidence**, not by majority or recency.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Parallelisation justified | inspect | separability + cost recorded |
| Interfaces frozen before start | inspect | schema/signatures committed |
| Every task has a contract | inspect | all fields present |
| Shared files have one owner | inspect | named |
| Status reports in fixed form | inspect | evidence attached |
| Each task verified before dependents | run log | verification recorded |
| Cross-agent interference audited | diff review | no out-of-scope changes |
| Independent verification performed | report | verdict recorded |
| End-to-end journey run | observed | passes or gaps listed |

## 7. Failure handling

- **Merge conflicts in shared files** → the ownership rule was violated; resolve with the owner, and reassign ownership before continuing.
- **Two agents produced incompatible designs** → stop dependent work, decide in the decision log, and have one agent rework rather than both patching.
- **An agent is blocked on a missing interface** → unblock by deciding the interface centrally; do not let it invent one silently.
- **An agent reports done with no evidence** → treat as not done; run the verification yourself.
- **Integration fails with no single culprit** → bisect by reverting agent contributions one at a time, keeping a record of which revert changed the symptom.
- **Orchestration overhead exceeds the work** → collapse to a single agent, record the lesson, and keep the contracts as the task description.

## 8. Security and authorisation

Risk class B, C if agents reach shared environments. Grant each agent the minimum permissions for its task: no production credentials, no deploy rights, no access to other tasks' secrets. Isolate workspaces (separate branches or worktrees) so one agent cannot overwrite another's uncommitted work. Review every agent's diff before it reaches a protected branch — an agent with push access is an unreviewed committer.

## 9. Completion criteria

- [ ] Decision to parallelise (or not) recorded with reasoning.
- [ ] Interfaces frozen and committed before parallel work.
- [ ] Task contracts complete, with owned and forbidden paths.
- [ ] Shared files assigned to a single owner.
- [ ] State artefacts established (plan, decision log, outputs).
- [ ] Status reports in the fixed form with evidence.
- [ ] Each task verified before dependents began.
- [ ] Integration verified incrementally; interference audited.
- [ ] Independent verification of the merged result.
- [ ] End-to-end journey run; run log written.

## 10. Deliverables and handover

Artifacts: `ORCHESTRATION_PLAN.md` (contracts, ownership, interfaces), `RUN_LOG.md` (deviations, verification results, rework).

Handover: verified integration → `04-process/release-engineering/` P01; systemic lessons about decomposition → `_meta`-equivalent process docs or the team's retro; per-task defects → the owning system; anything the orchestration could not verify → stated explicitly rather than assumed.
