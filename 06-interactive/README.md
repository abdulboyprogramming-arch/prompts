# 06-Interactive — Context Collection & Wizards

Prompts that gather the information a deeper system needs, so that work does not begin on assumptions. They ask a small number of high-leverage questions and produce a structured brief the next prompt can consume.

**Maturity: one `operational`, three `skeleton` (v2.28.5).** `PROJECT-INTAKE.md` was run against a frozen request in 2.28.5, failed every graded criterion, and was rebuilt around repository discovery, contradictions and sourced facts (`_meta/empirical-evaluation-18.md`). The other three remain skeletons: a useful question set with no verification, evidence rules or failure handling. Use those three interactively with a human.

## Contents

| Prompt | Purpose | Produces |
|--------|---------|----------|
| [`context-collectors/PROJECT-INTAKE.md`](context-collectors/PROJECT-INTAKE.md) | Establish the project, repository, stack, and constraints — discovered first, then asked — `operational` | `PROJECT_BRIEF.md` |
| [`context-collectors/CONTRIBUTION-INTAKE.md`](context-collectors/CONTRIBUTION-INTAKE.md) | Establish target repository, contributor identity, and authorisation | `CONTRIBUTION_BRIEF.md` |
| [`context-collectors/GREENFIELD-INTAKE.md`](context-collectors/GREENFIELD-INTAKE.md) | Establish the problem, users, and non-goals for a new project | `GREENFIELD_BRIEF.md` |
| [`multi-step-wizards/SYSTEM-SELECTOR.md`](multi-step-wizards/SYSTEM-SELECTOR.md) | Route the user to the right system/workflow | recommendation |

## Design principles

- **Ask only what the repository cannot answer.** Stack, conventions, test command, and structure are discovered, not requested.
- **Batch questions.** One message with five questions beats five round trips.
- **Offer defaults.** If the user is unsure, propose a defensible default and mark it as an assumption.
- **Separate facts, assumptions, and open questions** in the output; downstream prompts rely on that distinction.
- **Never ask for secrets.** If a credential is required, ask the user to place it in their environment and confirm availability.
- **Produce something reusable:** the brief is an artifact, not a conversation summary.

## When not to use these

If the request is already specific ("this test is flaky", "the audit found these five issues"), go directly to the relevant prompt. Intake exists to remove ambiguity, not to add ceremony.

## Known gaps before promotion to `draft`/`operational`

1. ~~No validation that the produced brief is internally consistent.~~ **Closed for `INT-P01` in 2.28.5** — §6 verification, seven checks.
2. ~~No handling of contradictory answers.~~ **Closed for `INT-P01` in 2.28.5** — contradictions are a first-class section of the brief.
3. `SYSTEM-SELECTOR` does not yet cover the systems added in 2.0.0 (project-recovery, observability, release, AI/agentic, workflows). **Open.**
4. ~~No record of which assumptions the user confirmed.~~ **Closed for `INT-P01` in 2.28.5** — each assumption carries its confirmer and a falsifier.

The same three repairs are **not** applied to `INT-P02`, `INT-P03` or `WIZ-P01`, which remain skeletons. The fix was demonstrated on one prompt and has to be repeated on the others before the system can be called operational.

Tracked in [`_meta/ROADMAP-AND-BACKLOG.md`](../_meta/ROADMAP-AND-BACKLOG.md).
