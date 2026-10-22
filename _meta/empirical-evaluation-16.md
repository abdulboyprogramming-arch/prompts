# Empirical Evaluation 16 — the library's own test state, and the check that could not fail

**Date:** 2026-10-22
**Prompts:** `QA-P01` v1.1.0 (Testing Context & Quality Goals) and `QA-P02` v1.1.0 (Current
Test State Assessment)
**Evaluator:** the author of the prompts. Author-run, conflict of interest recorded.
**Target:** this repository at `b1cbc9a` (main, 2.28.0)
**Result:** **TESTED — PASS** for both stages, after one R1 defect was found and fixed in
the library's own validator.

---

## 1. Why these two, and why together

The library's binding limit is not coverage — 281 of 364 prompts are operational — but
**evidence**: every one of the 26 recorded runs is author-run, and the executed ratio sits
at 9.3 %. Of the batches in `_meta/execution-batches.md`, B2 (`04-process/`) is the only
one where the target, the tests, the artefacts and the acceptance criteria already exist,
because the target is this repository itself.

`QA-P01` → `QA-P02` was chosen over the other B2 stages for three reasons: it is a
**two-stage composition**, so the handoff gets tested rather than assumed; its output is a
set of factual claims about the tree, every one of which can be checked objectively; and
its subject is the library's own quality claim, which is the claim most worth attacking.

## 2. What was run

| Stage | Input | Output |
|---|---|---|
| `QA-P01` | this repository, no stated trigger, no stated time budget | [`.qa/QA_CONTEXT.md`](../.qa/QA_CONTEXT.md), [`.qa/QA_LEDGER.md`](../.qa/QA_LEDGER.md) |
| `QA-P02` | `QA_CONTEXT.md` risk map | [`.qa/CURRENT_STATE.md`](../.qa/CURRENT_STATE.md) |

The trigger was **assumed**, per the stage's own fallback rule: the highest-consequence,
highest-churn area from the repository's recorded history. The history itself came from
`_meta/review-log.md` and `CHANGELOG.md` rather than `git log`, because this checkout is
shallow (2 commits) — recorded as a limitation of the run, not of the prompt.

## 3. What the run produced, checked against the tree

Every number in `.qa/CURRENT_STATE.md` was verified after the fact:

| Claim in the artefact | Verified |
|---|---|
| 7 test files, 119 cases | `python3 scripts/test_*.py` → 10 + 19 + 17 + 17 + 12 + 17 + 27 = 119 |
| `check_all.py` takes 3.04 s | measured; re-run 3.07 s / 3.11 s |
| 15 gates, 0 errors, 0 warnings on the real tree | measured |
| 476 files, 364 prompts | validator output at run time |
| test-to-source ratio 0.38 | 1,217 test lines / 3,215 tooling lines |
| no `sleep`, no network, no `skip`/`xfail` in tests | `grep` over `scripts/test_*.py` |
| CI has never executed a step | `gh api .../actions/runs/*/jobs` → `steps: 0` |

The `covered` classifications were not decided by reading the code. Each was demonstrated
by a **mutation** in a throwaway copy (`/tmp/qa-mut`): a skeleton relabelled operational,
a count changed, a broken link added, an undeclared placeholder added, an identifier
duplicated. Five fired as errors, exactly as the artefact claims.

## 4. The defect

**B6 — a risk-class-A prompt must not invite a destructive action.**

The validator has carried this rule since the risk classes were introduced. On a
purpose-made mutation — appending *"The agent will deploy the change to production after
review."* to a prompt that declares `Risk class: A` — it produced:

```
WARNING  ...: risk class A but text mentions 'deploy the'; confirm the action is gated or raise the class
```

and `scripts/validate_library.py` exited **0**. `scripts/check_all.py` — the single gate
every contributor and the CI workflow run — printed **"All gates passed"**.

A risk-class-A prompt tells an agent the work is read-only. A prompt that says that and
then invites a deploy has given the agent a licence to act on a system it was told it
could not touch, and the library's own gate said nothing. By the standard the library
applies to tests — *"a test that cannot fail is not a test"* (`04-process/testing-qa/README.md`,
test-value rule 4) — a check that cannot fail a build is not a control.

**Why the test suite did not catch it:** there was no fixture for the rule at all. The
rule was added and verified by hand at the time, which is evidence that it worked once.

## 5. The fix

`v1.1.0` → behaviour unchanged, enforcement changed:

- the logic moved into `check_risk_class(doc)` so it can be called directly;
- it appends to `errors` instead of `warnings`;
- the message states the three ways out: gate the action in the sentence, raise the class,
  or state the read-only boundary explicitly;
- five fixtures in `scripts/test_validator.py` pin it — error on an unnegated destructive
  verb, no error under class B, no error when the sentence forbids the action, no error
  with no verb present, and one that asserts the message tells the author how to resolve it.

The negation escape is deliberately permissive (`do not`, `never`, `must not`, `avoid`,
`without`, `not` in the preceding clause) because a strict version would block legitimate
prose such as "the pipeline must not deploy on Fridays". That trade-off is recorded rather
than hidden: the rule catches the contradiction, not every phrasing of it.

## 6. Retest

| Check | Before | After |
|---|---|---|
| Mutation: class-A prompt + unnegated deploy | `WARNING`, validator exit 0, `check_all` pass | `ERROR`, validator exit 1, `check_all` exit 1 |
| Real tree, 476→479 files | 0 errors, 0 warnings | 0 errors, 0 warnings |
| Validator self-tests | 27/27 | **32/32** |
| Full gate suite | 15/15, 3.04 s | 15/15, 3.07 s |

Both stages therefore end **TESTED — PASS**: the procedures ran on a real target, their
verification tables were filled in, their artefacts are checkable, and the one defect the
run surfaced is fixed and retested.

## 7. A second finding, about the target rather than the prompt

Running `QA-P01` inside this repository **fails five gates**: two file-total claims and two
artefacts the validator does not recognise as documents. The validator's message names the
escape hatch, and both were resolved (`<!-- not-a-prompt -->`, totals 476 → 479).

This is correct behaviour, but it means the QA system cannot be run against a repository
that validates itself without editing it. For any other user of the library it is a
non-issue; for this repository it is a standing friction worth knowing before the next
engagement, and it is why the `.qa/` artefacts are committed with the marker rather than
left as untracked files.

## 8. What this run does not show

- **It is author-run.** The person who wrote `QA-P01`/`QA-P02` designed the mutations and
  judged the classifications. It demonstrates the procedures complete and their output is
  checkable; it does not demonstrate that an outside reader would reach the same
  conclusions. The library's independence gap is unchanged.
- **It tests the library's claim-checking machinery, not the prompts' usefulness.** Whether
  `QA-P02` produces a *useful* test-state assessment for a product team, as opposed to a
  correct one for this repository, is not measured here.
- **Two stages of seven.** `QA-P03` … `QA-P06` were not run; the ledger records them as
  `not started`, and the deliberate stop after `P02` is written into the ledger per the
  stage's own instruction to stop before inventory.
- **No end-to-end level exists to test.** Nothing in the suite applies a prompt to a real
  project; that remains the documented gap in `_meta/evidence-levels.md`.
- **CI is still unverified as a control.** The fix makes the gate fail locally. Whether the
  workflow would surface it remotely is unknown, because no workflow step has ever executed.
