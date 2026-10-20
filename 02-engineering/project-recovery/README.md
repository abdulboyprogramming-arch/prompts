# Project Recovery & Completion

**Maturity: operational (v1.0.0).** Seven stages, each with workflow, evidence rules, verification, failure handling, and completion criteria.

**Entry point:** [`P07-Acceptance/P07-Acceptance-Handoff.md`](P07-Acceptance/P07-Acceptance-Handoff.md) is the final gate; start with [`P01-Containment/P01-Containment-State-Preservation.md`](P01-Containment/P01-Containment-State-Preservation.md) or run the sequence through the README.
**Execution mode:** autonomous-completion
**Risk class:** B — local edits in a dedicated branch; no push, deploy, or destructive Git operations without explicit authorisation

## When to use this

You have a repository that is *supposed to work* and does not, or is supposed to be finished and is not:

- A previous developer or AI agent abandoned it mid-feature.
- The last session ended with uncommitted work, a half-applied migration, or a broken build.
- The frontend exists, the backend exists, and they do not talk to each other.
- Authentication is 70% wired; payments are 50%; the README claims both are done.
- You inherited it and cannot tell what is real, what is stubbed, and what is dead.

This system separates three things that are usually conflated: **preserving what exists**, **establishing what is true**, and **making it work end to end**. It refuses to let an agent "clean up" a repository before it has preserved it.

## What makes recovery different from building

| New project | Recovery |
|-------------|----------|
| Requirements are chosen | Requirements must be *recovered* from code, commits, and artifacts — and may be contradictory |
| You can delete and restart freely | Deletion may destroy the only record of intent |
| "Done" is defined up front | "Done" must be reconstructed and then agreed |
| Tests are added as you go | Existing tests may be broken, disabled, or lying |
| One coherent author | Multiple authors and agents, with divergent conventions |

Consequences baked into this system: containment before modification; reconstruction before planning; acceptance before claims of completion; and an explicit prohibition on declaring success without an end-to-end run.

## Stages

| ID | Stage | Purpose | Produces |
|----|-------|---------|----------|
| REC-P01 | [Containment & state preservation](P01-Containment/P01-Containment-State-Preservation.md) | Make the current state recoverable before touching it | `RECOVERY_STATE.md`, safety branch/tag, inventory of uncommitted work |
| REC-P02 | [Reconstruction](P02-Reconstruction/P02-Intent-Reconstruction.md) | Recover what the project was meant to be and where work stopped | `INTENT.md`, stopping-point analysis |
| REC-P03 | [Completeness audit](P03-Completeness/P03-Completeness-Audit.md) | Separate implemented, stubbed, broken, and dead | `COMPLETENESS.md` |
| REC-P04 | [Environment & integration truth](P04-Integration/P04-Integration-Environment-Truth.md) | Establish whether it builds, starts, and connects | `INTEGRATION.md` |
| REC-P05 | [Recovery plan](P05-Plan/P05-Recovery-Plan.md) | Sequence the critical path to a working system | `RECOVERY_PLAN.md` |
| REC-P06 | [Incremental recovery](P06-Execution/P06-Incremental-Recovery.md) | Execute in verified increments, preserving existing work | code changes, `RECOVERY_LOG.md` |
| REC-P07 | [Acceptance & handoff](P07-Acceptance/P07-Acceptance-Handoff.md) | Prove it works end to end; report honestly | `ACCEPTANCE.md`, `HANDOFF.md` |

## The three prohibitions

These are the failure modes this system exists to prevent. They are absolute.

1. **No modification before preservation.** P01 must complete — branch, commit or stash of unrelated work, recorded SHAs — before any file edit. An agent that "just fixes the build" first has already made recovery harder.
2. **No deletion of unexplained code.** Code that looks wrong may be the only implementation of a required behaviour, or evidence of an unfinished decision. Mark it; do not remove it in P01–P05. Deletion only happens in P06, for code proven dead, with a recorded reason.
3. **No completion claim without an end-to-end run.** "The code is now complete" is not a deliverable. P07 requires a reproducible path from start to the user-visible outcome, executed and recorded.

## Guardrails for autonomous agents

- Work on a dedicated branch (`recovery/<date>` or the user's convention), never on the default branch.
- One logical change per commit; commit only when a verification step passes.
- Never `git reset --hard`, `git clean -fd`, force-push, rewrite history, or delete branches. If history repair seems necessary, stop and ask.
- If uncommitted work exists, preserve it exactly: commit it on a clearly labelled branch or record a patch file, *then* proceed.
- If the project requires external services you cannot reach, degrade to static recovery and state what could not be verified.

## How it typically unfolds

1. **P01–P02** (30–90 min): you learn what you have and where it stopped. Many "broken" projects are 80% complete with a blocked dependency, not 20% complete.
2. **P03–P04** (1–3 hours): the honest inventory. Expect the README to be wrong in specific, documentable ways.
3. **P05**: a plan with a *critical path* — not a wishlist. Usually 3–8 items to reach a demonstrable end-to-end flow.
4. **P06**: execute the critical path; stop before the polish.
5. **P07**: prove it, then hand over with a precise list of what remains.

If the budget ends earlier, the artifacts still leave the project better understood and safely preserved than it was.

## Related

- Broad assessment before deciding to recover vs rewrite: `02-engineering/codebase-audit/`
- Full rewrite decision: `02-engineering/rewriting-migration/`
- Test safety net before touching code: `04-process/testing-qa/`
- Multi-stage composition including this system: `07-workflows/recover-abandoned-project.md`
