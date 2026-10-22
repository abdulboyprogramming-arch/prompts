# Empirical Evaluation 17 — the validator that knew but could not refuse

**Date:** 2026-10-22
**Prompts:** `QA-P03` v1.1.0 (Gap Analysis), `QA-P04` v1.1.0 (Strategy), `QA-P05` v1.1.0
(Implementation), `QA-P06` v1.1.0 (Validation)
**Evaluator:** the author of the prompts. Author-run, conflict of interest recorded.
**Target:** this repository at `720687c` (main, 2.28.1), plus throwaway trees under `/tmp`
**Result:** **TESTED — PASS** for all four stages, after three R1 defects were found and one
proposed design was refuted by measurement before it was written.

---

## 1. Why these four, and why together

`empirical-evaluation-16.md` stopped deliberately after `QA-P02`, because that stage's own
instruction is to stop before inventorying gaps. `QA-P03` → `QA-P06` is the rest of the system and
is the first place in the library where four stages compose into a single deliverable: a gap list
that becomes a strategy, that becomes code, that becomes a validation record.

It also targets the thing the previous run exposed. `QA-P02` found one gate that could not fail.
The question worth asking next is not *"is there another one?"* — it is *"why was there one at
all?"* `QA-P03` is the stage that answers that, and it did:

> the validator had the knowledge but not the authority.

Four checks knew about unfinished prompts, empty sections, duplicate identifiers and dead links.
Three recorded what they found as warnings. Four had no fixture, so nothing would have noticed if
they had been deleted. The library's own test-value rule — *"a test that cannot fail is not a
test"* — applied to its own validator.

## 2. What was run

| Stage | Input | Output |
|---|---|---|
| `QA-P03` | this repository at `720687c` | [`.qa/GAPS.md`](../.qa/GAPS.md) — 7 gaps, four at R1, each probe-confirmed |
| `QA-P04` | that gap list | [`.qa/TEST_STRATEGY.md`](../.qa/TEST_STRATEGY.md) — levels, order, non-goals, numeric targets |
| `QA-P05` | that strategy | [`.qa/IMPLEMENTATION_LOG.md`](../.qa/IMPLEMENTATION_LOG.md) — two rule changes, twelve fixtures |
| `QA-P06` | that change | [`.qa/VALIDATION.md`](../.qa/VALIDATION.md) — 3× repeat, 5 mutations, verdict |

The handoff was tested rather than assumed: each stage's output is a file the next stage reads, and
each output is checkable against the tree. `GAPS.md` cites `file:line` for every claim; the
strategy's targets are numbers that either get met or do not.

## 3. The three R1 defects

Each was demonstrated by probe, not by reading the code: a prompt was written into a temporary
tree, `validate_library.check()` was called, and the messages were inspected.

**G-01 — the commonest placeholder form was invisible.** The check matched the literals `"[TODO"`,
`TBD`, `lorem ipsum` and `<insert`. `TODO: finish this` and `FIXME: later` produced nothing at all,
because they contain neither a bracket nor a bare `TBD`.

**G-02 — every hit was a warning.** Even when the check fired, the build passed: `check_all.py`
printed "All gates passed" over a prompt containing `[TODO]`.

**G-03 — an empty required section satisfied the required-section rule.** `## 6. Verification` with
nothing after it matched the heading check, so a prompt with no verification procedure passed the
rule that exists to require one. Only a warning was emitted.

## 4. The design that measurement refuted

`TEST_STRATEGY.md` §6 originally proposed a word-boundary scan for `TODO`, which is the obvious
implementation. Before writing it, it was run against the live corpus: **seven operational prompts
legitimately discuss `TODO` as a concept** (a component file with a TODO is not an interface; search
for TODO comments in the diff). A word-boundary scan would have failed the build on correct
prompts.

The shipped rule keys on the marker form instead — a token opening a line, optionally bulleted,
either bracketed (`[TODO]`, `[TODO: finish]`) or followed by a colon or dash (`TODO:`). Re-measured
across all 365 prompt-shaped documents: **0 hits**.

That section of `TEST_STRATEGY.md` was corrected rather than left as a plan the implementation
quietly ignored, and the correction is visible in the file.

## 5. What the fixtures caught that the fix did not

The first version of the new regex required punctuation after a bracketed token. That silently
dropped `[TODO] finish the handover` — a form the *old* code did catch. The fixture written from
the gap list failed on its first run, the regex gained a bracket branch, and the case passed.

This is the run's most useful single observation: the fixtures were written before the
implementation was trusted, and they found a regression in the new code within minutes.

## 6. Retest

| Check | Before (`720687c`) | After |
|---|---|---|
| Unbracketed `TODO:` in a prompt | silent | error with `file:line` |
| `[TODO]`, `[TODO: finish]`, `FIXME:`, bulleted `TBD` | warning | error |
| Empty required section | warning | error for non-skeleton prompts; warning elsewhere |
| Validator self-tests | 32/32 | **44/44** (+12) |
| Mutations of the five pinned rules | 0 of 5 attempted | **5 of 5 killed, 0 survived** |
| `check_all.py` | All gates passed (3.07 s) | All gates passed (2.95–3.09 s over three runs) |
| Real tree | 0 errors, 0 warnings | 0 errors, 0 warnings (484 files) |

The repeats were identical, so nothing was re-run to make a red result green.

## 7. What this run does not show

- **It is author-run.** The person who wrote the four stages also wrote the gaps, the fixes and the
  mutations. The gap list is checkable and the mutation numbers are reproducible, but the judgement
  about which behaviours matter is not independent. The library's independence gap is unchanged at
  0 %.
- **It tests the validator, not the prompts' usefulness.** That the rules fire says nothing about
  whether a verification section, once required, contains a *good* verification.
- **The fixtures are synthetic.** They prove a rule fires on a constructed prompt; the corpus scan
  proves the corpus is clean today. Neither proves a future prompt will be well written.
- **No CI enforcement.** No workflow step has ever executed in this repository (`steps: 0`,
  billing). The local gate is the only gate, before and after this run.
- **`P07` (Orchestrator) was not run.** The system's composition test stops at four of seven
  stages; the ledger records `P07` as not started.
