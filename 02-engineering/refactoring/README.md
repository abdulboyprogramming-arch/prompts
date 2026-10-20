# Safe Refactoring

**Maturity: operational (v1.0.0).** Seven stages for changing structure without changing behaviour — and for proving both halves of that claim.

**Entry point:** [`P01-Assessment/P01-Assessment-Goal-Clarification.md`](P01-Assessment/P01-Assessment-Goal-Clarification.md)
**Execution mode:** diagnostic
**Per stage:** diagnostic (P01, P05), planning (P02, P07), implementation (P03, P04, P06)
**Risk class:** A–B (P01/P02/P07 read-only and planning; P03–P06 change the repository)

## Why this system exists

Refactoring is the most frequently performed risky change in software and the least verified. The failure pattern is consistent:

- It starts because code "feels bad", with no measurable goal, so nobody can say whether it worked.
- It drifts: a rename becomes an extraction, becomes a rewrite, becomes an abandoned branch.
- It proceeds without tests, on the argument that tests will be added afterwards.
- Behaviour changes are smuggled in as "obvious fixes", making the diff unreviewable.
- It ends with both the old and the new structure present, and a feature flag that nobody dares remove.

This system imposes the discipline that makes refactoring safe: a measurable target, slices that keep the trunk green, a net proven to catch breakage, mechanical execution, equivalence evidence, and removal of what was replaced.

## Stages

| ID | Stage | Purpose | Produces |
|----|-------|---------|----------|
| REF-P01 | [Assessment & goal](P01-Assessment/P01-Assessment-Goal-Clarification.md) | Turn a complaint into a measurable target — or decline the work | `REFACTOR_GOAL.md` |
| REF-P02 | [Strategy](P02-Strategy/P02-Refactoring-Strategy.md) | Choose the technique, slice it, find the seams, define reversal | `REFACTOR_STRATEGY.md` |
| REF-P03 | [Safety net](P03-Safety-Net/P03-Safety-Net.md) | Characterisation and contract tests, **mutation-proven** to catch breakage | `SAFETY_NET.md` |
| REF-P04 | [Execution](P04-Execution/P04-Execution.md) | One mechanical transformation per commit, green after each | commits, `EXECUTION_LOG.md` |
| REF-P05 | [Validation](P05-Validation/P05-Validation.md) | Prove equivalence *and* measure whether the target moved | `VALIDATION.md` |
| REF-P06 | [Cleanup](P06-Cleanup/P06-Cleanup-Documentation.md) | Remove the old path, dead code, and stale documentation | `REFACTOR_SUMMARY.md` |
| REF-P07 | [Orchestrator](P07-Orchestrator/P07-Safe-Refactoring-Orchestrator.md) | Gates, failure routing, and stopping scope drift | `REFACTOR_RUN.md` |

## The five rules

1. **No measurable target, no refactoring.** "Cleaner" is not a target; "one place to change the tax rule instead of four" is.
2. **Behaviour change is never part of a refactoring commit.** It gets its own change and its own verification.
3. **The net must be shown to catch breakage** before execution starts.
4. **Every slice keeps the trunk working**, and every slice has a reversal point.
5. **A refactoring that leaves the old path in place is unfinished.**

## Choosing a technique

| Situation | Technique |
|-----------|-----------|
| A feature is coming that the structure fights | Preparatory refactoring — make the change easy, then make the easy change |
| The change is too large for one branch | Branch by abstraction, behind a seam and a flag |
| Replacing a subsystem that serves traffic | Strangler, with routing control |
| Correctness is critical and outputs comparable | Parallel run, comparing old and new |
| Only option is a long-lived branch | Treat as a rewrite: `02-engineering/rewriting-migration/` |

## Boundaries

- Replacing the implementation (behaviour may change): `02-engineering/rewriting-migration/`.
- The code is broken, not ugly: `05-scenarios/debugging/`.
- The goal is a performance number: `02-engineering/performance/`.
- The boundaries themselves are wrong: `02-engineering/architecture-review/`.
- Schema or data restructuring: `03-domains/database/`.
- Verifying someone else's refactoring claim: `07-workflows/independent-verification.md`.

## What this system will not do

- Guarantee the design improves. It guarantees that behaviour is preserved and the stated target is measured.
- Make a rewrite safe by relabelling it. Requests are classified in P01 and routed.
- Replace code review. It produces evidence a reviewer can check quickly.
