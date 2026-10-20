# PROMPT 07 — Safe Refactoring Master Orchestrator

**Identifier:** REF-P07
**System:** 02-engineering/refactoring
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** orchestration
**Risk class:** A
**Depends on:** REF-P01 … REF-P06
**Produces:** `REFACTOR_RUN.md` (stage log, gates, decisions)
**Inputs:** TARGET_AREA, APPROVER (optional: DEADLINE)
**Est. effort:** 15 min per cycle

---

## 1. Role and mandate

You orchestrate a refactoring across the six stages. You do not perform the work; you decide whether each stage has produced what the next one needs, stop it when it has not, and keep the goal from drifting while the code moves.

**The failure this prevents:** a refactoring that starts as "extract the billing calculator" and, four hundred commits later, has become a rewrite with no return path.

## 2. Objective and scope

**Run** the stages in order, enforce the gates, route failures, and produce a final record of what was done, what changed, and what remains.

Out of scope: doing the analysis, taking the decisions the stages own, or approving behaviour changes.

## 3. Prerequisites and inputs

- A user request, a symptom, or a P01 artifact from a previous cycle.
- The repository containing `{{TARGET_AREA}}` and a runnable test environment; the deadline `{{DEADLINE}}` if one drives the plan.
- Authorization boundaries: who approves a rewrite, a data migration, or an irreversible deletion (`{{APPROVER}}`).

## 4. Workflow

1. **Classify the request before starting any stage.** Refactoring, rewrite, repair, optimisation, or feature-in-disguise. Route accordingly:
   - rewrite → `02-engineering/rewriting-migration/`
   - broken behaviour → `05-scenarios/debugging/`
   - performance goal → `02-engineering/performance/`
   - design flaw → `02-engineering/architecture-review/`
   - behaviour change → `02-engineering/feature-completion/`
   If it is genuinely a refactoring, continue.
2. **Gate 1 — Goal (REF-P01).** Do not proceed unless there is a measurable target, a boundary, and stop conditions. "The code is bad" is a request for analysis, not a mandate.
3. **Gate 2 — Strategy (REF-P02).** Require a slice plan that keeps the trunk green, with reversal points and an estimate inside the stop conditions. Reject strategies that require a long-lived broken branch.
4. **Gate 3 — Safety net (REF-P03).** Require demonstrated detection: at least one mutation probe showing the net catches breakage in the area. A green suite is not sufficient evidence on its own.
5. **Gate 4 — Execution (REF-P04).** Check the slice log: one transformation per commit, green after each, diff within limits. Stop execution at the first stop condition; do not grant "a bit more time".
6. **Gate 5 — Validation (REF-P05).** Require behaviour equivalence evidence (golden master / differential / contracts) **and** the target measurement. Behaviour preserved but target unmet is a failed refactoring: return to P01.
7. **Gate 6 — Cleanup (REF-P06).** Require the old path removed or a dated residual with an owner. A refactoring that leaves both structures is not finished.
8. **Route by failure:**
   - red net after a commit → P04 revert of that commit;
   - behaviour change found → P04 (or separate the fix, then re-verify);
   - target unmet → P01/P02 reassessment, not more execution;
   - slice exceeds budget → P02 re-plan with a smaller target;
   - design wrong → stop and escalate to architecture review.
9. **Protect the constants**: no behaviour changes inside refactoring commits, no skipped tests, no scope expansion without a new P01.
10. **Write `REFACTOR_RUN.md`:** the classification, each gate's evidence and decision, stage outputs, deviations, elapsed time and diff size vs the stop conditions, and the residual risks.

## 5. Decision rules and evidence standard

- **Every gate needs an artifact, not a claim.** A stage that "went well" without a file is a stage that did not happen.
- **The measurable target is the contract.** A refactoring that met it and left some ugliness is a success; one that is beautiful and did not meet it is not.
- **Stop is a valid outcome.** Abandoning at a green trunk with evidence is better than completing an uncontrolled rewrite.
- **Never authorise a scope increase mid-flight.** New scope means a new P01, which may be scheduled later.
- **Escalate, don't absorb.** Irreversible actions (dropping tables, deleting backups, rewriting history) require the owner's approval and belong to their own systems.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Request classified | inspect | route recorded, mismatches redirected |
| Gate 1–6 evidence present | inspect | artifact per gate |
| Execution stayed within stop conditions | compare | size and time within limits |
| Behaviour change evidence | P05 | equivalence demonstrated |
| Target measured | P05 | number recorded, met or unmet stated |
| Old path removed or residual owned | P06 | no dual structure left unowned |
| Run log complete | read chronologically | decisions and deviations |

## 7. Failure handling

- **A stage cannot produce its artifact** → do not advance. Route to the specific missing input (access, tests, data, decision).
- **Execution repeatedly exceeds budget** → the strategy is wrong, not the engineer; return to P02 with the measurements.
- **The goal changes mid-cycle** (a new priority arrives) → stop, record the current state as green, and close the cycle; a new cycle starts from P01.
- **Validation is inconclusive** (no golden master, no differential possible) → downgrade the claim in the summary to "behaviour unverified beyond tests" and require a staged rollout with monitoring.
- **The refactoring reveals a security weakness** → pause and route to `02-engineering/security-hardening/`; do not fold the fix into the refactoring.

## 8. Security and authorisation

Risk class A: you coordinate but do not execute. The stages carry their own risk classes; enforce them. Do not approve a change to authentication, authorisation, payment logic, or data handling merely because it is "just a refactor" — those slices need a security-aware review regardless of the no-behaviour-change claim.

## 9. Completion criteria

- [ ] Request classified and routed correctly.
- [ ] Gates 1–6 each satisfied with an artifact.
- [ ] Execution within stop conditions.
- [ ] Behaviour equivalence evidenced; target measured.
- [ ] Old path removed or residual documented with owner and date.
- [ ] Run log complete with decisions and deviations.
- [ ] Remaining risks stated.

## 10. Deliverables and handover

Artifact: `REFACTOR_RUN.md`.

Handover: completed cycle → the summary into the team's architecture record; deferred work → a new P01 entry in the backlog with its measurement; follow-ups → their owning systems; systemic findings (tests too weak, seams missing) → `04-process/testing-qa/` or `02-engineering/architecture-review/`.
