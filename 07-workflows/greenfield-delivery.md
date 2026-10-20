# Workflow — Greenfield Delivery

**Identifier:** WF-GREENFIELD
**System:** 07-workflows
**Version:** 1.0.0
**Maturity:** draft
**Execution mode:** autonomous-completion
**Risk class:** B
**Depends on:** `02-engineering/from-scratch/`, `02-engineering/feature-design-suggestion/`, `04-process/testing-qa/`, `04-process/release-engineering/`
**Produces:** a running, tested, documented, deployable initial version

---

## When to use this

You are starting from nothing (or near nothing) and need to reach a state where the software does something real, safely, and can be handed to others.

## Sequence

| # | Stage | Prompt | Gate |
|---|-------|--------|------|
| 1 | Problem and scope | `02-engineering/feature-design-suggestion/P02-Problem-Framing/` or `from-scratch/P01-Vision/` | — |
| 2 | Architecture and stack | `from-scratch/P02-Architecture/`, `P03-Stack-Decision/` | **GATE 1** |
| 3 | Scaffold | `from-scratch/P04-Scaffold/` | — |
| 4 | Vertical slice | implement one end-to-end path (your own prompt or `from-scratch/P05`) | **GATE 2** |
| 5 | Test strategy for the slice | `04-process/testing-qa/` QA-P04→P06 (targeted) | — |
| 6 | Expand breadth | feature design → implementation, one feature at a time | — |
| 7 | Harden | `02-engineering/security-hardening/` (scoped), `04-process/observability-reliability/` | — |
| 8 | Document and release | `from-scratch/P07-Docs-Polish/`, `04-process/release-engineering/` | **GATE 3** |

## Stage handoffs

1. **Scope.** One paragraph problem statement, target user, three to five success behaviours, explicit non-goals. Constraint in force from here: build for the stated scope only.
2. **Architecture — GATE 1.** Stack decision with rejected alternatives and reasons; data model; deployment assumption. Human approval, because reversing a stack later is expensive.
3. **Scaffold.** Repository conventions, build/test/lint commands that actually run, CI skeleton. Verification: a trivial test passes in CI.
4. **Vertical slice — GATE 2.** One complete user-visible path through every layer (UI → API → logic → persistence), with at least one test. This proves the architecture before breadth is added. If the slice fights the architecture, fix the architecture now, not later.
5. **Slice tests.** Cover the slice's success path and one failure path. This becomes the regression baseline.
6. **Breadth.** Each feature: problem → design → implementation → tests → review. No feature is "done" without a test and a working manual path.
7. **Hardening.** Threat model for the real surface, secrets handling, error tracking, structured logs, health check. Scope security to what exists; do not build a compliance programme for a prototype.
8. **Release — GATE 3.** Version, changelog, run instructions that a stranger can follow, deployment procedure, rollback plan.

## Gates

- **GATE 1 — stack and architecture.** Human decision. Cheapest to change now, most expensive later.
- **GATE 2 — architecture proven by slice.** Agent stops and reports: does the slice work, what did it reveal, what would change in the architecture?
- **GATE 3 — release readiness.** Human decision to publish/deploy (Category C).

## Failure routing

| Failure | Route |
|---------|-------|
| Scope keeps growing | Return to stage 1 with the non-goals list; split into v1 and later |
| Stack does not support a required behaviour | GATE 1 re-decision before more code is written |
| Vertical slice reveals architectural mismatch | Fix architecture while code volume is small; record the decision |
| Tests cannot be written cheaply | Suspect design coupling; refactor the seam now, not after breadth |
| Deadline pressure | Cut scope, not verification — ship fewer features that work |

## Completion criteria for the workflow

1. The stated success behaviours work end to end, demonstrated by a recorded run.
2. Build, test, and lint run locally and in CI, with commands documented.
3. A new contributor can set up and run the project from the docs alone.
4. Secrets are not in the repository; configuration is documented by key name.
5. A rollback path exists for the first deployment.
6. Non-goals and deferred work are written down.

## Anti-patterns

- Building breadth before a vertical slice proves the architecture.
- Deferring tests "until the design settles" — the design settles by testing it.
- Writing a deployment pipeline before there is anything worth deploying.
- Scaffolding with dependencies chosen before the problem is understood.
