# Workflow — Recover an Abandoned or Broken Project

**Identifier:** WF-RECOVER
**System:** 07-workflows
**Version:** 1.0.0
**Maturity:** draft
**Execution mode:** autonomous-completion
**Risk class:** B
**Depends on:** REC-P01 … REC-P07, optional AUDIT-P02/P05, QA-P04/P05
**Produces:** a preserved, understood, demonstrably working project — or an evidence-based recommendation to migrate instead

---

## When to use this

A repository exists, is supposed to work, and does not. You do not know how much is real. Previous work was interrupted — by a developer leaving, an agent hitting a limit, or a migration half-applied.

## Sequence

| # | Stage | Prompt | Gate |
|---|-------|--------|------|
| 1 | Containment | `02-engineering/project-recovery/P01-Containment/` | — |
| 2 | Intent reconstruction | `REC-P02` | — |
| 3 | Completeness audit | `REC-P03` | — |
| 4 | Environment truth | `REC-P04` | **GATE 1** |
| 5 | Recovery plan | `REC-P05` | **GATE 2 — mandatory approval** |
| 6 | Incremental recovery | `REC-P06` | — |
| 7 | Acceptance | `REC-P07` | **GATE 3 — merge decision** |
| 8 | (if needed) test safety net | `04-process/testing-qa/` QA-P04→P06 | — |
| 9 | (if needed) defect triage | `05-scenarios/debugging/` | — |

## Stage handoffs

1. **P01 → P02.** Handoff carries: HEAD SHA, safety branch/tag name, preserved uncommitted work location, risky conditions (in-progress merge, detached HEAD, committed secrets), environment capability.
   *Constraint established here:* no modification before preservation; no history rewriting; no deletion of unexplained code. This constraint persists through stage 9.

2. **P02 → P03.** Handoff carries: numbered requirements with provenance, the stopping-point analysis, branch inventory, contradictions table, open questions.
   *Decision point:* if the contradictions are irresolvable without the original author, the user must choose the intended behaviour. Record the choice.

3. **P03 → P04.** Handoff carries: status per requirement, placeholder inventory, wiring mismatches, the requirements blocking an end-to-end flow.

4. **P04 → GATE 1.** Handoff carries: the ladder level reached (`builds` / `starts` / `serves` / `completes flow`), first blocking errors in dependency order, seam failures, configuration drift, and proposals that were *not* applied.
   **GATE 1 — user decision:** is the target realistic? If the project cannot build because a required private dependency or service is unavailable, recovery stops here and the handoff becomes a decision document.

5. **P05 → GATE 2.** Handoff carries: the acceptance flow, critical path, increments with rollback points, stop line, `[DECISION]` items.
   **GATE 2 — mandatory approval.** Recovery changes are authorised by the plan, not by the workflow. Do not proceed on general enthusiasm.

6. **P06 → P07.** Handoff carries: commit range, per-increment verification evidence, observed-but-unfixed issues, pre-existing failure baseline.

7. **P07 → GATE 3.** Handoff carries: the grade (`acceptance-passed` / `partial` / `not-achieved`), the acceptance evidence, preservation verification, residual risk, and the handoff document for the next owner.
   **GATE 3 — merge decision.** Local commits exist; nothing is pushed or merged without explicit instruction.

## Failure routing

| Failure | Route |
|---------|-------|
| Cannot preserve state (no Git, read-only) | P01 fallback: filesystem snapshot; record reduced rollback; consider stopping |
| Intent irrecoverable, contradictions material | User decision at GATE 2; narrow the acceptance flow to what is unambiguous |
| Cannot build for environmental reasons | GATE 1 decision: obtain access, or accept static-only recovery with stated limits |
| Critical path implies a rewrite | Stop. Re-plan as a migration: `02-engineering/rewriting-migration/` |
| Third failed attempt on one increment | Stop at P06; escalate with evidence of each attempt |
| Acceptance fails on a hidden dependency | Return to P06 only with authorisation; otherwise record `partial` honestly |

## Completion criteria for the workflow

1. The project state at the start is recoverable (safety branch/tag verified to exist).
2. Every requirement is classified with evidence, and the classification is consistent between P03 and P07.
3. The acceptance flow was executed from a clean checkout, with recorded observations.
4. Any claim of "works" is supported by that execution, and anything not executed is labelled unverified.
5. A stranger can run the project using `HANDOFF.md` alone.
6. The outcome grade is honest, including when it is `partial` or `not-achieved`.

## Cost and time expectations

A typical interrupted project (5k–50k LOC, one blocked dependency, one half-built feature) takes roughly: 30–90 min for stages 1–3, 1–3 h for stage 4, 30 min for stage 5, 2–6 h for stage 6. A project with an unsound data model or auth design exceeds this and should be re-scoped as a migration after GATE 2.

## Anti-patterns

- Starting with "let me just fix the build" — destroys the ability to distinguish your changes from the original state.
- Deleting "dead" code found during P03 — some of it is the only implementation of a requirement.
- Treating a green build as acceptance.
- Expanding scope after GATE 2 because the code is finally understandable.
