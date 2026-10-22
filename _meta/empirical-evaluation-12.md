# Empirical evaluation 12 — `code-review` stages 1–3 against this repository's own tooling

**Prompts:** `CR-P01` (`04-process/code-review/P01-Context/P01-Context-Goals.md`), `CR-P02` (`P02-Change-Understanding`), `CR-P03` (`P03-Review/P03-Structured-Review.md`) — all v1.0.0
**Date:** 2026-10-22 · **Method:** real execution, agent-performed and agent-graded, by the author.
**Target:** the tooling diff `v2.21.1..main` — 12 files, **+1,794 / −80**, plus `.github/` workflows. Chosen because it is a real, recent, self-contained change to the repository's own validation code, which is the highest-consequence code in a repository that claims machine-checked honesty.

---

## 1. `CR-P01` — context and goals

| Field | Value |
|---|---|
| Intent | stated, from commit messages and the changelog: replace three drifting gate lists with one runner, add composition checking, add self-tests |
| Scope | 12 files in `scripts/` + `.github/`; 8 new, 4 modified; Python only; no generated or vendored files in the subset |
| Change type | **Infrastructure** — with a security-relevant edge, because the code under review is the gate that everything else passes through |
| Risk surface named before reading | 1) the runner is the only path to "validated", so a defect in it silently weakens every other check; 2) the new gates write to the tree; 3) a gate may pass without testing anything |
| Hypotheses to test in P03 | a) the single runner has no test of its own; b) a gate that rewrites a file may leave the tree modified; c) a self-test may pass trivially |
| Depth decision | full read of `check_all.py` and of the new functions in `validate_library.py`; **sampled** read of the 515-line `generate_task_index.py` and of the 247-line `test_contract.py`; stated as a sampling rather than a full review |
| Explicitly not covered | performance of the gate list, the prose changes in the 199 modified Markdown files, and whether each generated file's *content* is right (only whether it is current) |

**Verification table:** all eight checks pass — ref range exact, intent stated with its source, scope metrics computed with `git diff --stat`, type classified, three risk areas named before the diff was read, hypotheses testable, depth justified by risk, exclusions stated.

## 2. `CR-P02` — change understanding

Read the diff by module rather than line by line. What the change actually does:

- `check_all.py` (new, 136 lines) — one ordered gate list, a `--fix` mode that regenerates in dependency order, and a catalog-currency check that works by rewriting the file and comparing.
- `check_prompt_contract.py` (new, 351 lines) — dependency resolution, artifact ownership, cycles, and the flow metric.
- `validate_library.py` (+214) — `check_community`, `check_documented_counts`, `check_stated_totals`, `check_readme_counts`.
- Four new/extended test files, and the deletion of the superseded second workflow.

Discrepancies noticed at this stage, carried to P03 as hypotheses: the runner is the only script without a test; the runner writes to the tree; nothing verifies that a self-test case can fail.

## 3. `CR-P03` — findings

Each finding was **verified before it was recorded**, which is the stage's central rule. The deciding command is quoted.

| # | Sev | Finding | Consequence | Evidence |
|---|---|---|---|---|
| 1 | **High** | `catalog_is_current()` returned early when the validator exited non-zero, *after* the rewrite had already been written. | On any run where validation fails, the gate leaves `_meta/CATALOG.md` modified in the working tree — built from the tree that just failed validation. A contributor sees a dirty tree, and CI's "tree must be unchanged" step fails for the wrong reason, masking the real error. | Reproduced: a temp broken prompt made the validator exit 1 while writing the catalog; `git status` showed `M _meta/CATALOG.md` with +7 lines from the bad input. |
| 2 | **Medium** | `check_all.py` had no test, while every script it runs does. | The runner is the single definition of "validated"; a defect in it is a defect in every claim the repository makes, and nothing would notice. | `ls scripts/test_*.py` listed five suites, none for the runner. |
| 3 | **Low** | The same function restored a *missing* catalog by writing `""`. | Left an empty generated file where none had existed, which reads downstream as a real but empty catalog. | Read of the restore branch: `open(path, "w").write(before)` with `before = ""`. |
| 4 | **Low** | The module docstring said "nine checks"; the list held thirteen gates plus the catalog check. | A stale count in the file whose purpose is to end stale lists. | `grep -c` of the `GATES` entries against the prose. |

**A hypothesis that did not survive:** "a self-test may pass trivially." `test_contract.py` contains a case built specifically to be able to fail (an unknown dependency, detected by token shape rather than by resolving identifiers); it was checked in `empirical-evaluation-09` and re-read here. No finding recorded.

## 4. Fixes applied

1. `catalog_is_current()` now snapshots, runs inside `try`, and restores **unconditionally in `finally`**, comparing contents only when the exit code is 0. A catalog that did not exist is removed rather than blanked.
2. New `scripts/test_check_all.py` — 10 cases: the three restore paths (fail / identical / stale), the missing-file case, every gate naming a script that exists, and no duplicated gate names. Wired into the gate list as `gate-list self-tests`, first, so a broken runner is reported before anything it runs.
3. Docstring count removed rather than corrected — a count in prose is a claim that drifts, which is the lesson the repository keeps relearning.
4. Two stale documents corrected: `_meta/publication-decision.md` and `_meta/release-readiness.md` still described PR #12 as open and unmerged.

## 5. Retest

- `python3 scripts/test_check_all.py` → **10/10**.
- The original defect was re-created (temp broken prompt), the full gate list was run, and `_meta/CATALOG.md` was **unchanged** afterwards — the failure reproduces, the corruption does not.
- Full suite after the fix: **15/15 gates pass**, self-tests 23/23, 19/19, 13/13, 12/12, 17/17, 10/10.

## 6. Findings about the prompts

| # | Sev | Finding |
|---|---|---|
| 1 | **Medium** | `CR-P03` says "run the failing case, trace the branch, or cite both lines that contradict" — three verification methods, none of them a way to **record** the demonstration. The review is asked to verify but not to preserve the command that verified, so a later reader has a claim and no reproduction. This run added the commands by hand. |
| 2 | **Low** | `CR-P01` requires naming the risk surface before reading the diff, and offers no way to keep that ordering checkable. Nothing in the artifacts shows the ordering happened; a reviewer who read the diff first can write the same file. |
| 3 | **Low** | `CR-P02` produces `CHANGE_SUMMARY.md` with no rule for **sampling**: the depth decision lives in P01, and P02 has no place to record which modules were read in full and which were skimmed. This run kept that in its own notes. |

## 7. Changes made to the prompts

- `CR-P03` v1.1.0: every finding must carry the **command or trace that demonstrated it**, in the findings table, not only the claim that it was verified. Its verification table gains a row: *each finding names its demonstration*.
- `CR-P02` v1.1.0: carries the sampling record — modules read in full, modules sampled, modules not read — so the depth decision made in P01 is auditable in the artifact that used it.

`CR-P01` left unchanged: the ordering requirement is real, and the fix for finding 2 would be a timestamp that the artifacts do not have a reliable way to carry. Recorded rather than papered over.

## 8. Limitations

- The review was performed by an agent that had **written** the code under review earlier the same day, and graded itself. That is the weakest possible evaluator for this target, and it is disclosed rather than mitigated.
- Three of six stages ran. `CR-P04` (feedback), `CR-P05` (follow-up) and `CR-P06` (orchestrator) were not executed, so this is not an end-to-end system run.
- 500 of the 1,794 lines were sampled, not read. A full read would likely find more.
- The target is the only kind of code this reviewer is currently able to review without inventing a fixture.

## 9. Follow-on, same day: the ratio was published fourteen times

Registering the three reviews above moved the executed count from 14 to 17, and
the gate run passed. It passed because `evidence_report.py --check` compares one
generated file and nothing else. Fourteen hand-written copies of the old ratio
were still in the tree — in `README.md`, `QUICKSTART.md`, `PROJECT-STATUS.md`,
`_meta/execution-batches.md`, `_meta/publication-checklist.md`,
`_meta/publication-decision.md`, `_meta/release-readiness.md` and
`_meta/repository-configuration.md` — including three different numbers for the
same figure (9, 11 and 14 of 228) in documents published as current.

This is the same defect class the review was about: a number that is checked in
one place and restated in others. The fix follows the same principle, check the
thing a reader actually reads:

- `published_claims()` in `evidence_report.py --check` now scans every Markdown
  page for `N of <operational total>` and fails when the count disagrees with the
  registry. Dated records (`_meta/empirical-evaluation-*.md`, `CHANGELOG.md`,
  `_meta/review-log.md`) are exempt, because they state what was true when they
  were written. A zeroth count is exempt because it is only ever the
  independent-run figure, which shares the denominator and counts something else.
- All fourteen copies were corrected by hand, along with the percentages beside
  them (6.1% → 7.5%, 4.8% → 7.5%, 3.9% → 7.5%).
- `scripts/test_evidence_report.py` covers the scan: 12 cases, including the
  exemptions and the file-and-line in the message. It is one of the sixteen gates.

Two further stale figures surfaced in the same pass and are recorded rather than
quietly fixed: `_meta/release-readiness.md` said "five suites, 84 cases" (six and
94 at the time of the check, seven and 106 after the additions here), and
`_meta/publication-checklist.md` said 471 tracked files / 4.2 MB / 112 KB largest
(513 tracked files, 3.6 MB, 120 KB, measured with `git ls-files` and `du`).

The scan does not cover every number in the repository, only this ratio over
every page. Totals of files and prompts are still checked in four documents only,
by the validator's `DOC_TOTAL_FILES` list, and everything else is prose. That gap
is now named in `release-readiness.md` row 8 rather than left implied.
