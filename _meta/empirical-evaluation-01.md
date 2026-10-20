# Empirical Evaluation 01 — `DBG-01` Systematic Debugging

**Date:** 2026-10-20
**Prompt under test:** `05-scenarios/debugging/SYSTEMATIC-DEBUGGING.md` v1.1.0
**Evaluator:** the author of the prompt (bias noted below)
**Result:** protocol completed successfully; three real prompt weaknesses found and fixed in v1.2.0

---

## Why this exists

Every prompt in this library was labelled `operational` on the basis of structural review: metadata, sections, verification tables, internal consistency. None had been executed against a real defect. The coverage matrix records that as the largest credibility gap, and this is the first attempt to close it.

**What this evaluation can and cannot show:** one run against one small synthetic defect demonstrates that the protocol is usable end to end and that following it produces a verified fix. It does not demonstrate effectiveness against large codebases, non-deterministic defects, or unfamiliar stacks, and the evaluator wrote the prompt — a conflict of interest that a second evaluator would remove.

---

## Method

1. Built a fixture project (`/tmp/fx01`, not committed) with a **deliberately hidden defect** and a **passing test suite**.
2. Wrote a defect report in the form a user would give, without naming the cause.
3. Followed the prompt's workflow steps in order, without consulting the fixture's source in advance.
4. Recorded which steps did useful work, which required judgment the prompt did not supply, and where the prompt was silent.
5. Changed the prompt where the run exposed a gap; re-ran the fixture to confirm the changes do not break the protocol.

## Fixture

A small CSV importer for supplier price lists: validate required fields, deduplicate within a batch, convert price to `Decimal`. Two passing tests covering the happy path and invalid-row skipping.

The defect: the dedupe set was a **mutable default argument** (`def import_rows(rows, seen=set())`), created once at import time, so dedupe state leaked between batches in a long-lived process. The second import of the same file silently skipped every valid row, reporting them as duplicates.

This shape was chosen because it has the properties that make real bugs hard: the suite is green, the cause is invisible at the call site, the symptom is data loss rather than an exception, and the naive fix ("clear the set") addresses the symptom.

## What actually happened

| Prompt step | What it contributed | Time |
|-------------|--------------------|------|
| 1. Defect statement | Forced the report into "when X, observed Y instead of Z" — made "second import drops rows" precise | 1 min |
| 2. Reproduce | Two sequential calls reproduced it immediately: 2 imported / 0 imported | 2 min |
| 3. Minimise | Reduced to one SKU, two calls — the "second call" pattern became obvious | 1 min |
| 4. Localise | **Prompt was weakest here.** Elimination advice covered inputs, layers, and dependencies; the decisive move was changing the *call sequence*, which the step did not suggest | 3 min |
| 5–6. Hypotheses + instrumentation | Confirmed the default object was identical across calls and already contained the first batch's SKUs — evidence, not code reading | 3 min |
| 7. Cause, not symptom | Reached the actual invariant: "a default argument is evaluated once; per-call state must not live there" | 2 min |
| 8. Minimal fix | `seen=None` + fresh set per call, with a comment stating why | 1 min |
| 9. Verify both directions | Reproduction passed; existing suite still passed; **reverting the fix made the regression test fail again** | 3 min |
| 10. Regression test | Fails on the pre-fix commit, passes after | 2 min |
| 11. Record | Cause summary suitable for a commit message | 1 min |

Total: roughly 19 minutes of work, all steps executable as written, no step that produced nothing.

## Weaknesses found, and what changed

### 1. "Green suite" was not treated as evidence to investigate (fixed)

The protocol required the suite to stay green after the fix, but said nothing about the suite being green **while the defect existed**. In this fixture the tests passed because they called the operation once — the tests encoded the assumption that caused the bug to be invisible.

**Change:** step 2 now requires recording the suite's state while the defect is present, and interpreting a green suite as "the tests assert the buggy behaviour".

### 2. The decisive localisation axis was missing (fixed)

The elimination advice listed inputs, layers, and stubs. State-leak defects are found by varying the **invocation context** — call count, ordering, threads, process reuse, restart. I found it by instinct, not by following the prompt.

**Change:** step 4 now requires varying invocation context explicitly, and step 5 adds an ordered hypothesis-class list led by shared mutable state, noting that a defect appearing only on the second invocation is almost always that.

### 3. No requirement to explain why the tests missed it (fixed)

Step 10 added a regression test but never asked *why the existing suite was blind*. Without that, the same class of defect remains undetected elsewhere — the fix treats one instance.

**Change:** new step 11 requires naming the assumption the suite made; a verification row and a completion criterion were added.

## What the prompt did well

- Step 1's insistence on a one-sentence defect statement prevented an unfocused read of the code.
- Step 6 ("instrument, don't guess") was the step that converted a plausible hypothesis into proof; reading the source would have shown the same signature without demonstrating the leak was real across calls.
- Step 9's revert requirement is the single most valuable check: it distinguishes a cause from a coincidence, and it is the check most humans skip.
- The completion criteria were specific enough that "done" was unambiguous.

## What remains unproven

- One defect, one language, one evaluator, ~20 minutes. This is a smoke test, not a validation study.
- Non-deterministic, cross-service, and performance defects were not exercised.
- Whether a model following the prompt *without* the evaluator's prior knowledge would find the same axis is untested — the evaluator knew the fixture's construction. A stronger design would have a second party author the fixture.
- No comparison against an unprompted baseline, so no claim is made that the prompt is better than competent debugging without it.

## Consequences for the library

- `DBG-01` → v1.2.0, with three concrete changes traceable to this run.
- Roadmap item "empirical test harness" stays P0: one evaluation is not a harness. The next step is a fixture set with a repeatable scoring sheet, and ideally fixtures written by someone other than the prompt's author.
- No other prompt's `operational` label is affected by this evaluation. They remain structural reviews.

## Reproducing this evaluation

The fixture is not committed (it is a throwaway). To reproduce: create a module with a mutable default argument that accumulates state across calls, a test suite that calls the function once, and a defect report describing "the second import drops rows". Run the protocol; the decisive step should be step 4's invocation-context variation.
