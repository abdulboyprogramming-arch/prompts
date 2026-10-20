# Code Review

**Maturity: operational (v1.0.0).** Six stages that turn a diff into a decision: understand the intent, understand the change, find what matters, say it usefully, verify the fixes, and close the loop.

**Entry point:** [`P01-Context/P01-Context-Goals.md`](P01-Context/P01-Context-Goals.md) — or the [orchestrator](P06-Orchestrator/P06-Code-Review-Orchestrator.md) if you review frequently.
**Execution mode:** diagnostic
**Per stage:** diagnostic (P01–P03), implementation (P04), specialised (P05), orchestration (P06)
**Risk class:** A — a review reads and comments; it does not modify or merge

## Why this system exists

Code review is the highest-frequency engineering activity that is almost never designed. The failure modes are consistent and expensive:

- **Rubber-stamping**: approvals without evidence, especially on large diffs where reading is impossible.
- **Style-first reviewing**: forty nits and a missed authorisation bypass, which trains authors to skim reviews.
- **Unstated intent**: the reviewer does not know what the change is for, so they cannot tell a bug from a decision.
- **Feedback that fails**: the same finding delivered as an accusation produces an argument instead of a fix.
- **Unclosed loops**: findings discussed, half-fixed, one "noted for later" that nobody tracks.

This system makes the review proportionate to risk, evidence-based, and closed.

## Stages

| ID | Stage | Purpose | Produces |
|----|-------|---------|----------|
| CR-P01 | [Context & goals](P01-Context/P01-Context-Goals.md) | Intent, scope, change type, risk surface, review depth | `REVIEW_CONTEXT.md` |
| CR-P02 | [Change understanding](P02-Change-Understanding/P02-Change-Understanding.md) | Three-pass read, deletions first, intent reconciliation, one traced path | `CHANGE_SUMMARY.md` |
| CR-P03 | [Structured review](P03-Review/P03-Structured-Review.md) | Findings with consequences, severity vocabulary, tests probed | `REVIEW_FINDINGS.md` |
| CR-P04 | [Feedback](P04-Feedback/P04-Feedback-Crafting.md) | Observation → consequence → request, marked nits vs blockers | `REVIEW_FEEDBACK.md`, comments |
| CR-P05 | [Follow-up](P05-Follow-up/P05-Follow-up-Support.md) | Re-verify fixes, track deferrals, close every finding | `FOLLOW_UP.md` |
| CR-P06 | [Orchestrator](P06-Orchestrator/P06-Code-Review-Orchestrator.md) | Triage, gates, domain routing, proportional depth | `REVIEW_RUN.md` |

## The review rules

1. **Know the intent before judging the code.** No description means the intent is reconstructed and labelled as inferred.
2. **Deletions and renames get read first.** That is where regressions hide.
3. **Every finding states a consequence.** No consequence, no finding — it is a nit, and it is labelled.
4. **Blockers are reserved for harm**: data loss, security, broken behaviour, unverifiable claims.
5. **The reviewer does not fix the author's branch.** Reviewing and authoring are different controls.
6. **Fixes are re-verified, not accepted.** "Fixed" is a claim.
7. **Every finding ends in a state** — fixed, disputed, deferred with an owner, or withdrawn.

## Proportionality

| Change | Review depth |
|--------|--------------|
| Docs, typo, comment | Structural check; no full review |
| Localised code with tests | All five stages |
| Auth, payments, data deletion, migration, public API | All stages **plus** the domain system (`SEC-*`, `PAY-*`, `DB-*`) |
| Thousands of lines / mixed concerns | Return for splitting; review the risk surface and disclose what is unreviewed |

## Boundaries

- Verifying an agent's *claims* of completion (not reviewing code quality): `07-workflows/independent-verification.md`.
- Security assessment: `02-engineering/security-hardening/`.
- Merge conflicts during the change: `04-process/git-operations/` P02.
- Release decision after merge: `04-process/release-engineering/` P01.

## What this system will not do

- Approve in the reviewer's name. The decision is stated; a human owner still provides platform approvals.
- Substitute for domain verification: a payments change needs `PAY-*`, a migration needs `DB-*`.
- Guarantee the change is good. It guarantees the review's evidence is visible and its gaps are disclosed.
