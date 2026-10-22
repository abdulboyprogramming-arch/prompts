<!-- not-a-prompt -->

# Validation record — QA-P06

**Cycle:** 2.28.2
**Prompt:** `04-process/testing-qa/P06-Validation/P06-Validation-Measurement.md`
**Subject:** the validator changes and 12 fixtures recorded in `.qa/IMPLEMENTATION_LOG.md`
**Environment:** local sandbox, Python 3, a checkout of this repository
**Status of this document:** every number below came from a command run in this cycle. No result is
simulated or carried over from an earlier cycle.

## 1. What "validated" means here

Three questions, answered separately because they fail separately:

1. **Does the change work on the corpus?** — the gate passes and the corpus produces no new findings.
2. **Does the change stay working?** — the same commands, repeated, give identical results.
3. **Does the test suite notice if the change is undone?** — mutations of the validator are killed
   by the fixtures.

A green run alone answers only the first.

## 2. Repeatability — three consecutive runs

Each row is one full pass of all three commands, run back to back.

| Run | `validate_library.py` | `test_validator.py` | `check_all.py` |
|-----|----------------------|---------------------|----------------|
| 1 | 0 errors, 0 warnings (0.25 s) | 44/44 (0.10 s) | All gates passed (3.04 s) |
| 2 | 0 errors, 0 warnings (0.25 s) | 44/44 (0.11 s) | All gates passed (2.95 s) |
| 3 | 0 errors, 0 warnings (0.25 s) | 44/44 (0.11 s) | All gates passed (3.09 s) |

Identical results, exit code 0 every time, `check_all.py` inside the `TEST_STRATEGY.md` target of
under 5 seconds (worst observed 3.09 s). No flakiness to report, and no retry was needed — nothing
was re-run to turn a red result green.

## 3. Mutation testing — does the suite have teeth?

Five mutations were applied to a copy of `scripts/validate_library.py` in `/tmp`, one per isolated
copy of the tree, and `scripts/test_validator.py` was run in each copy. The real working tree was
never mutated; the copy was rebuilt from the unmodified file for every mutation.

| Mutation | What it simulates | Result | Cases that failed |
|----------|-------------------|--------|-------------------|
| M1 | Reverting marker detection to the 2.28.1 literal-token scan (warnings only) | **killed** — 41/44 | the three marker cases |
| M2 | Keeping detection but demoting findings to warnings | **killed** — 41/44 | the three marker cases |
| M3 | Demoting an empty required section back to a warning | **killed** — 43/44 | empty required section |
| M4 | Deleting the duplicate-identifier rule | **killed** — 43/44 | duplicate identifier |
| M5 | Turning a broken relative link into a warning | **killed** — 43/44 | broken relative link |

**5 of 5 mutations killed, 0 survived**, against the strategy's target of 0 surviving.

Process note, kept because it affects how much the numbers are worth: the first mutation run used a
single shared copy directory, and mutations M2 and M3 appeared to produce each other's failures. The
harness was rebuilt to copy the tree per mutation, and the table above is from that isolated run.
The first run's numbers were discarded rather than explained away.

## 4. Gap coverage

| Gap | Rule now blocking? | Fixture | Mutation evidence |
|-----|--------------------|---------|-------------------|
| G-01 plain `TODO:`/`FIXME:` invisible | yes | 3 positive marker cases | M1, M2 |
| G-02 placeholder hits only warned | yes | same cases, which assert *no warning* as well as *an error* | M1, M2 |
| G-03 empty required section passed | yes | "empty required section" | M3 |
| G-04 body-size overclaim unfixtured | already blocking | "body shorter than the minimum" | — (rule untouched) |
| G-05 duplicate identifier unfixtured | already blocking | "duplicate identifier" | M4 |
| G-06 broken relative link unfixtured | already blocking | "broken relative link" | M5 |
| G-07 input/placeholder agreement unfixtured | already blocking | undeclared placeholder (error) + declared-but-unused (warning) | — (rule untouched) |

Two negative controls keep the marker rule honest: a prose mention ("a component file with a TODO
is not an interface") and a mid-line mention ("Search for TODO comments in the diff") must produce
neither an error nor a warning. Both pass, which is what makes the zero-hit corpus scan meaningful
rather than a sign the rule matches nothing.

## 5. Limits of this validation

- **Everything here is author-run.** One execution environment, one operator, no independent
  reproduction. The evidence count in `_meta/evidence.json` records it as such.
- **The fixtures are synthetic trees.** They prove the rules fire on constructed inputs and that
  undo-ing them fails; they do not prove a real prompt library contains no such defect. The corpus
  scan covers the corpus, not the fixtures.
- **Not covered:** the README/PROJECT-STATUS count checks against a synthetic tree, behaviour on a
  malformed prompt that trips several rules at once, and any Windows line-ending path.
- **No CI corroboration exists to appeal to.** No workflow step has ever executed in this
  repository, so this record is the enforcement evidence — not a local shadow of a remote check.

## 6. Verdict

The strategy's targets were met: 4 of 4 R1 behaviours fixtured, 7 of 7 gaps closed by test or rule,
`check_all.py` under its time target, 12 new cases (target ≥ 12), 0 of 5 mutations surviving.
The claim this supports is narrow and should be quoted narrowly: **the validator's placeholder,
empty-section, overclaim, duplicate-identifier, broken-link and input rules are pinned by fixtures
and fail the local gate when broken.** It does not support "the library is validated".
