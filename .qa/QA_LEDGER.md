<!-- not-a-prompt -->

# QA Ledger

**Engagement:** the prompt library's own quality contract
**Target:** `720687c` (main, 2.28.1) for stages P01–P02; `ab1528b` (main, 2.28.2) for P03–P06; verified again at `ab1528b` for P07
**Started:** 2026-10-22
**Closed:** 2026-10-22 — all seven stages run

| Stage | Artifact | Status | Notes |
|-------|----------|--------|-------|
| QA-P01 | `.qa/QA_CONTEXT.md` | `complete` | 10 behaviours mapped; 4 at R1 |
| QA-P02 | `.qa/CURRENT_STATE.md` | `complete` | suite measured; one R1 defect found (risk-class-A warning) and fixed in 2.28.1 |
| QA-P03 | `.qa/GAPS.md` | `complete` | 7 gaps, 4 at R1, each probe-confirmed |
| QA-P04 | `.qa/TEST_STRATEGY.md` | `complete` | order, non-goals, numeric targets; the proposed word-boundary scan was refuted by measurement before coding |
| QA-P05 | `scripts/validate_library.py`, `scripts/test_validator.py`, `.qa/IMPLEMENTATION_LOG.md` | `complete` | two rules made blocking; 12 fixtures, 32 → 44 cases |
| QA-P06 | `.qa/VALIDATION.md` | `complete` | 3× repeat identical; 5 mutations, 5 killed, 0 survived |
| QA-P07 | this file, §Close-out | `complete (composition run)` | seven checks verified below; one deviation and two unobservable items recorded |

## P07 — verification against the orchestrator's own table

| # | Check (from `QA-P07` §6) | Method used | Result |
|---|--------------------------|-------------|--------|
| 1 | Artifacts complete | `ls .qa/` | **pass** — all seven present: context, ledger, current state, gaps, strategy, implementation log, validation |
| 2 | R1 risk map agreed at P01 | inspect `QA_CONTEXT.md` | **partial** — the map was produced and used; the mandatory human checkpoint was *not* held, because author and approver are the same person. Recorded as a deviation, not a pass |
| 3 | Every new test has red→green evidence | trace each of the 12 fixtures to a mutation or a pre-fix probe | **partial** — 6 have a mutation that kills them, 3 have a pre-fix probe that was silent or warned, 3 are guards/pins with no prior red state (see §Red→green) |
| 4 | Mutations reverted | `git status`, `git diff` in the working tree | **pass** — tree clean; every mutation ran in a separate `/tmp` copy, never in this checkout |
| 5 | Suite deterministic | three consecutive runs of `check_all.py` and the validator self-tests | **pass** — 44/44 and "All gates passed" on all three; 2.89 s / 2.92 s / 2.93 s |
| 6 | CI enforcement | workflow file + latest run's jobs | **not observable** — run `39836004571` failed with **`steps: 0`**: the runner never started a step (Actions billing). No remote check has ever executed here |
| 7 | Targets verdicts measured | compare `TEST_STRATEGY.md` §7 with artifacts | **pass** — 4/4 R1 behaviours fixtured, 7/7 gaps closed, `check_all` under 5 s, 12 new cases (target ≥ 12, met exactly: 32 → 44), 0/5 mutations surviving |
| 8 | Ledger current | this file | **pass after this edit** — it previously still said P02 in progress and P03–P06 not started, which was three releases stale |
| 9 | Working tree contains only test/CI and `.qa/` changes | `gh api commits/1b843a5` file list | **pass for production code** — the merge touched `scripts/validate_library.py` and `scripts/test_validator.py`, no CI config and no production code. It also touched twelve documentation and record files, which this orchestrator's wording does not anticipate; that is a documentation of the rule's narrowness, not a violation |

### Red→green evidence per fixture

| Fixture | Red evidence |
|---------|--------------|
| marker at the start of a line | mutation M1/M2 → fails; pre-fix behaviour was silent |
| bulleted marker | mutation M1/M2 → fails |
| bracketed `[TODO]` form | mutation M1 → fails; pre-fix behaviour was a warning |
| empty required section | mutation M3 → fails; pre-fix behaviour was a warning |
| duplicate identifier | mutation M4 → fails |
| broken relative link | mutation M5 → fails |
| undeclared placeholder | no mutation; pre-fix probe confirmed the rule already fired, so this pins existing behaviour |
| body-size overclaim | no mutation; pre-fix probe confirmed it fired |
| empty non-required section | guard — pins that the new blocking rule does not over-reach |
| prose mention of TODO | guard — was never red; exists so the marker rule cannot be "fixed" by widening it |
| mid-line mention of TODO | guard, same reasoning |
| declared-but-unused input | guard — pins the warning side of the input rule |

Three of twelve are therefore regression pins and guards rather than demonstrated red→green
transitions. That is the honest count; claiming twelve would be claiming evidence that does not exist.

## Close-out summary (P07 §10, 250-word limit)

Seven stages ran against this repository. Four R1 defects were found and fixed: two placeholder forms were invisible, every placeholder hit only warned, and an empty required section satisfied the rule meant to require it. Four more rules worked but had no fixture.

The proposed fix was refuted by measurement before it was written — a word-boundary `TODO` scan matched seven legitimate prompts — and replaced by a marker-form rule that finds 0 hits across 485 documents. The fixtures then caught a defect in the new regex on their first run.

Suite duration did not regress: 3.04 s before, 2.89–2.93 s after. Validation is deterministic across three runs and 5 of 5 mutations were killed.

Residual risk: all runs are author-run; the fixtures prove rules fire, not that a required verification section contains a good verification; three fixtures are guards with no red state; the mandatory P01 checkpoint could not be held because author and approver are the same person.

Flake status: none observed; nothing was re-run to make a red result green.

CI remains unobserved — no workflow step has ever executed here (`steps: 0`).

Next three items: (1) `QA-P07` run by a second person, which is the only thing that would make the checkpoint real; (2) fixtures for the three guard cases that currently have no failing state; (3) the same treatment for the contract and overlap validators, which have the same class of "fires but nothing enforces it" risk that was found here.
