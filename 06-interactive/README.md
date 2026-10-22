# 06-Interactive — Context Collection & Wizards

Prompts that gather the information a deeper system needs, so that work does not begin on assumptions. They ask a small number of high-leverage questions and produce a structured brief the next prompt can consume.

**Maturity: all four prompts are `operational` (v2.28.6).** Each was run against a committed fixture before it was trusted, and every one failed first: `PROJECT-INTAKE` scored 0 of 5 (`empirical-evaluation-18.md`), `CONTRIBUTION-INTAKE` 0 of 5, `GREENFIELD-INTAKE` 1 of 8 and `SYSTEM-SELECTOR` 5 of 14 (`-19.md`). The repairs came from the failures — read the repository before asking the user, treat the user's statements as claims to check, and route from the generated index rather than from memory.

## Contents

| Prompt | Purpose | Produces |
|--------|---------|----------|
| [`context-collectors/PROJECT-INTAKE.md`](context-collectors/PROJECT-INTAKE.md) | Establish the project, repository, stack, and constraints — discovered first, then asked — `operational` | `PROJECT_BRIEF.md` |
| [`context-collectors/CONTRIBUTION-INTAKE.md`](context-collectors/CONTRIBUTION-INTAKE.md) | Read the upstream's rules and permissions before any code is written — `operational` | `CONTRIBUTION_BRIEF.md` |
| [`context-collectors/GREENFIELD-INTAKE.md`](context-collectors/GREENFIELD-INTAKE.md) | Separate the problem from the proposal, fix the constraints, write the non-goals — `operational` | `GREENFIELD_BRIEF.md` |
| [`multi-step-wizards/SYSTEM-SELECTOR.md`](multi-step-wizards/SYSTEM-SELECTOR.md) | Route to a destination that exists, using `TASKS.md` rather than memory — `operational` | routing card |

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
3. ~~`SYSTEM-SELECTOR` does not yet cover the systems added in 2.0.0~~ **Closed in 2.28.6** — it now routes from the 21-section `TASKS.md` index, and a 14-request fixture scores it against that index rather than against memory (5 of 14 → 14 of 14).
4. ~~No record of which assumptions the user confirmed.~~ **Closed for `INT-P01` in 2.28.5** — each assumption carries its confirmer and a falsifier.

All four gaps are now closed, and each was closed by a run that failed first. The system has no skeletons left.

**What is still not tested:** that these briefs improve the work of the systems that consume them. The library has no end-to-end composition harness, and every result above is author-run.

Tracked in [`_meta/ROADMAP-AND-BACKLOG.md`](../_meta/ROADMAP-AND-BACKLOG.md).
