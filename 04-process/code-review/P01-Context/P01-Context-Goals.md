# PROMPT 01 — Context & Goals

**Identifier:** CR-P01
**System:** 04-process/code-review
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A
**Depends on:** none (entry stage)
**Produces:** `REVIEW_CONTEXT.md`, `REVIEW_LEDGER.md`
**Inputs:** BASE_REF, HEAD_REF (optional: PR_DESCRIPTION, AUTHOR_INTENT)
**Est. effort:** 10–20 min

---

## 1. Role and mandate

You are setting up a review that will actually be useful. Most reviews fail before the first comment: the reviewer does not know what the change is meant to do, what constraints apply, or what the author already knows is incomplete. So the review becomes a style inspection of a diff viewed out of context.

You do not review code in this stage. You establish what a correct review would have to determine.

## 2. Objective and scope

**Answer:** what is this change trying to achieve, what does it touch, what risk does it carry, and what must this review establish to be worth the author's time?

Out of scope: reading the diff in detail (P02), findings (P03).

## 3. Prerequisites and inputs

| Input | Source | If missing |
|-------|--------|------------|
| `BASE_REF`, `HEAD_REF` | user | ask; a review of "the branch" is ambiguous |
| The stated intent (PR description, ticket, commit messages) | user `PR_DESCRIPTION` | derive from commits and mark `inferred` |
| The project's conventions (style guide, architecture rules, test policy) | repository | state which conventions you will apply |
| `AUTHOR_INTENT` — what they already know is unfinished | author | assume nothing is declared; `{{AUTHOR_INTENT}}` stays unspecified and P02 looks for the gaps |

## 4. Workflow

1. **State the change's intent in one sentence**, taken from `{{PR_DESCRIPTION}}` or the commit range `{{BASE_REF}}..{{HEAD_REF}}`. If the commits contradict the description, record both — that mismatch is itself a finding for P03.
2. **Establish scope**: files changed, lines added/removed, languages touched, and whether the diff includes generated or vendored files (which must be reviewed differently or excluded with a reason).
3. **Classify the change type**, because it determines what to look for:

   | Type | The review must establish |
   |------|--------------------------|
   | Feature | Behaviour matches intent, edge cases, authorisation, tests |
   | Bug fix | The fix addresses the cause, a regression test exists, nothing else changed |
   | Refactor | Behaviour preserved, slices mechanical, old path removed |
   | Dependency bump | Lockfile delta, breaking changes, verification evidence |
   | Infrastructure / config | Blast radius, rollback, secrets, environment parity |
   | Data / migration | Reversibility, compatibility, reconciliation (`DB-*` applies) |
   | Documentation | Accuracy against the code as it now is |
   | Security-relevant | Threat surface, authorisation, input handling, disclosure |

4. **Identify the risk surface** and name the two or three areas that deserve the most attention: authentication, payment logic, data deletion, concurrency, migration, public API shape, or a new dependency.
5. **Find what the change does *not* include but probably should**: tests for the new path, documentation, migration, config for a new key, authorisation for a new endpoint. Do not confirm these as findings yet; list them as hypotheses for P03.
6. **Note the review standard to apply**: repository conventions, the project's own patterns, and the relevant library system (`REF-*`, `PAY-*`, `DB-*`, `SEC-*`) if the change falls in a domain with specific rules.
7. **Decide the review depth** proportional to risk: a full read of a 40-line fix in auth; a sampled read of a 4,000-line generated-lockfile bump.
8. **Write `REVIEW_CONTEXT.md`:** intent (stated vs inferred), scope metrics, change type, risk surface, hypotheses to test, conventions to apply, depth decision, and what this review explicitly will not cover (e.g. performance benchmarking).
9. **Initialise `REVIEW_LEDGER.md`** for findings.

## 5. Decision rules and evidence standard

- **A review without a stated intent is a style check.** If intent is missing, ask once; if it stays missing, review against the commits and say so.
- **Scope determines depth.** Reviewing 4,000 lines line-by-line produces rubber-stamping, not rigour.
- **Generated and vendored files are excluded explicitly**, not silently skipped.
- **Name the risk surface before reading the diff**, or the diff's shape will dictate what you notice.
- **Do not pre-judge.** Hypotheses are hypotheses until P03 confirms them.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Ref range recorded | `git log` | exact refs |
| Intent stated with source | inspect | stated / inferred / unknown |
| Scope metrics computed | `git diff --stat` | files, lines, languages |
| Change type classified | inspect | one of the taxonomy rows |
| Risk surface named | inspect | 2–3 specific areas |
| Hypotheses listed | inspect | testable in P03 |
| Depth decision justified | inspect | proportional to risk |
| Exclusions stated | inspect | generated, vendored, out-of-scope |

## 7. Failure handling

- **No PR description and unclear commits** → review the diff as "unknown intent" and make intent reconstruction the first finding: an unreviewable change is a process problem worth reporting.
- **Diff is enormous** (thousands of lines, mixed concerns) → say so and propose splitting; review the highest-risk subset and record the sampling. A single review of a 5,000-line change is not a control.
- **Generated files dominate the diff** → identify the generator and review the *input* to it instead; state that.
- **The change touches several domains** (code + migration + infra) → route each part to its system (`DB-*`, `REL-*`) and review them separately; one review cannot validate all three.
- **You lack access to the linked ticket** → record it; intent is `inferred` and the review's conclusions are conditional.

## 8. Security and authorisation

Risk class A: read-only. Do not modify the branch, push fixups, or comment on the PR in this stage. If the diff contains secrets or credentials, record the location only — never the value — and treat it as a blocking finding for P03.

## 9. Completion criteria

- [ ] Exact ref range recorded.
- [ ] Intent stated with its source.
- [ ] Scope metrics and file classification.
- [ ] Change type classified.
- [ ] Risk surface named.
- [ ] Hypotheses for P03 listed.
- [ ] Review depth decided and justified.
- [ ] Exclusions stated.
- [ ] Ledger initialised.

## 10. Deliverables and handover

Artifact: `REVIEW_CONTEXT.md`.

P02 receives: the ref range, the intent, the risk surface, and the hypotheses — which determine what to read closely and what to skim.
