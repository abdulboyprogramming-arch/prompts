# Workflows — Composing the Library

**Maturity:** draft for the contract; each workflow below carries its own maturity.

Individual prompts solve tasks. Real engineering is a sequence of tasks with handoffs, decision gates, and a definition of done that spans them. This folder contains **composed workflows**: which system to run, in what order, what each stage must hand over, where a human decision is mandatory, and what to do when a stage fails.

A workflow is not a new prompt to paste. It is an operating procedure for a session or a team, referencing the prompts that do the work.

## Available workflows

| Workflow | Use when | Entry system | Maturity |
|----------|----------|--------------|----------|
| [Recover an abandoned or broken project](recover-abandoned-project.md) | Inherited code, interrupted agent, "it half-works" | `02-engineering/project-recovery/` | draft |
| [Audit → remediate](audit-to-remediation.md) | You have (or suspect) serious findings and need them fixed safely | `02-engineering/codebase-audit/` | draft |
| [Production incident](production-incident.md) | Something is broken in production right now | `05-scenarios/incident-response/` | draft |
| [Greenfield delivery](greenfield-delivery.md) | A new project that must reach a working, shippable state | `02-engineering/from-scratch/` | draft |
| [Continuous improvement](continuous-improvement.md) | A healthy project that should keep getting better | `05-scenarios/README.md` + baselines | draft |
| [Independent verification](independent-verification.md) | An agent or engineer says the work is complete; you need to know if that is true | any completed change set | operational |

## The handoff contract

Every stage in every workflow produces a handoff block conforming to [`HANDOFF-CONTRACT.md`](HANDOFF-CONTRACT.md). This is what makes composition possible: the next stage reads the handoff, not the entire conversation.

If a stage cannot fill the contract honestly, it is not finished.

## Rules for composing

1. **One owner per artifact.** Two stages must not both write `FINDINGS.md`. If a later stage disagrees, it writes a new artifact and records the disagreement.
2. **Gates are real.** A `[GATE]` marker means stop and get a human decision. Do not infer approval from silence or from earlier general authorisation.
3. **Failure routes upward, not sideways.** When a stage is blocked, return to the plan that authorised it (or the user); do not improvise a different task.
4. **Constraints propagate.** A safety constraint established in stage 1 (risk class, no-push, no-deletion) remains in force until a human lifts it. Later prompts cannot grant themselves more authority.
5. **No stage grades its own work.** Verification stages must independently re-execute, not read the log.
6. **Sequence ≠ automation.** Running five prompts in a row is not orchestration. If you automate a chain, each stage must still be able to fail and stop.
7. **Partial completion is a valid outcome** — record it in the handoff and stop cleanly.

## Choosing between workflows

- **Something is on fire** → production incident. Do not start with an audit.
- **You do not know what you have** → recover-abandoned-project (P01–P03 gives the inventory) or codebase-audit if it works but may be unsound.
- **You know what is wrong and it is serious** → audit → remediate.
- **Nothing is wrong but velocity is dropping** → continuous improvement.
- **Nothing exists yet** → greenfield delivery.

## Anti-patterns

- Running a full audit to answer a question a single scenario prompt would answer.
- Using the recovery workflow on a project whose design cannot support the goal — recognise that early and switch to migration planning.
- Treating a workflow's stage list as a checklist to tick without executing verification.
- Composing stages from different systems without reconciling artifact names (e.g. `FINDINGS.md` vs `GAPS.md`).
