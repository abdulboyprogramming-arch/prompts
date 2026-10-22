<!-- not-a-prompt -->
# QA Context — the prompt library's own quality contract

**Produced by:** `QA-P01` v1.1.0 (`.qa/` artifact)
**Target:** this repository at `b1cbc9a` (main, 2.28.0)
**Date:** 2026-10-22
**Evaluator:** the author of the prompts. This is an author-run evaluation, not an independent one.

---

## 1. What this software is

A library of 364 Markdown prompt procedures for software engineering, plus 15 Python
gates that validate the library's own claims: that every count matches the tree, that
every link resolves, that no prompt claims a maturity its body does not support, that
generated indexes are current, and that no prompt overstates what has been tested.

Its users are engineers who copy a prompt into an agent, and agents that read the files
directly. They depend on two things and only two: **the prompts describe the outcome they
actually produce**, and **the numbers in the README are true**. A library that overstates
is worse than a smaller honest one, because the reader cannot tell which claims to
discount.

## 2. Risk map

Behaviours, not modules. Risk is assigned by consequence.

| # | Behaviour | Risk | Consequence if wrong |
|---|-----------|------|----------------------|
| B1 | A prompt's stated maturity matches what the file contains (no skeleton labelled operational) | **R1** | A reader trusts an outline as a procedure and runs it on a live system |
| B2 | Every count a reader sees (prompts, files, operational, executed) matches the tree | **R1** | The library's central claim is that it does not overstate; a stale count is exactly that overstatement |
| B3 | Every prompt link and cross-reference resolves | **R2** | A reader follows a dead end; recoverable, visible |
| B4 | A prompt's declared dependency graph composes — artefact names flow downstream | **R2** | A stage is run without its input and produces a plausible artifact with no basis |
| B5 | The evidence registry is the single source of the "executed" number | **R1** | Double-counting or hand-maintained ratios inflate the only trust metric in the library |
| B6 | A destructive instruction is never labelled low-risk (risk-class A prompts must not contain `apply`, `deploy`, `drop`) | **R1** | An agent is told a consequential action is read-only and performs it unsupervised |
| B7 | Generated files (catalog, gallery, task index, conformance report, evidence page) are current | **R2** | Two files disagree about the library; the reader trusts the stale one |
| B8 | A prompt declares the inputs it actually uses (placeholders match the `Inputs:` field) | **R3** | Minor friction; the agent asks for a value it was not told it needed |
| B9 | Prose passes the lint rules (no unactionable instructions, no empty intensifiers) | **R3** | Style, not correctness |
| B10 | Duplicate prompt identifiers are detected | **R2** | Two files answer to one id, and links become ambiguous |

**At least three R1 candidates exist**, as the stage requires: B1, B2, B5, B6.

## 3. What has already gone wrong

There is no issue tracker history to read. The repository keeps its own incident register
in [`_meta/review-log.md`](../_meta/review-log.md) — every defect found during authoring is
recorded there with its fix. The most consequential, all real and all recorded:

| Defect | Where recorded | Consequence |
|--------|----------------|-------------|
| `PROJECT-STATUS.md` claimed 213 operational prompts and two executed while the tree held 265 and 26 | `CHANGELOG.md` 2.26.0, review log | The headline claim was wrong by three releases |
| The prose count rule read `N operational` and missed `N prompts carry that label`, one line below it | `CHANGELOG.md` 2.28.0 | The same drift recurred a third time |
| `--delete-branch` on a merged PR deleted a stacked PR's base and silently closed it | PR #19 | A completed change had to be re-opened and re-reviewed |
| A `commit-msg` hook re-added an agent trailer to a commit authored as the owner | 2.27.0 review entry | An attribution defect that had to be caught by grep before pushing |
| A fixture script hard-coded `data/accounts.csv`, so it failed from its own directory | 2.25.1 | A committed fixture was not reproducible as documented |
| The executed-prompt ratio was checked in one document while readers saw it in five | `a6d849a` (PR #14) | The number the reader sees could drift from the registry |

The pattern is consistent and it is the finding: **every recorded defect is a claim that
drifted from reality, and every one was caught by a human or an agent reading, not by a
test.** The suite that exists tests the validator's rules; almost nothing tests that the
documents a reader actually reads are true.

## 4. Constraints

| Constraint | Value | Source |
|------------|-------|--------|
| PR feedback target | 10 minutes | assumed — no CI runs, so no measured baseline exists |
| CI | **does not run**: Actions jobs fail at startup with zero steps | `gh api .../actions/runs/*/jobs` → `steps: 0` on every run since 2.22.0 |
| Local suite runtime | 15 gates, measured in `PERF-P02`'s evaluation at a 3.40 s median | `_meta/empirical-evaluation-13.md` |
| Environments | local only; no cloud account, no database, no browser | this sandbox |
| Team | one author plus agent sessions | repository history |
| Test framework | plain Python scripts, hand-rolled case lists, no pytest | `scripts/test_*.py` |

The CI constraint dominates: **nothing in this repository has ever been blocked by a
remote check.** Every gate is a local command a person has to remember to run. That makes
B2 and B7 (truth of generated numbers) dependent on discipline rather than enforcement,
which is why they are the two that have failed repeatedly.

## 5. Success measures for this engagement

Observable by a third party, without asking the author:

1. **Every R1 behaviour has a test that fails when the behaviour breaks** — demonstrated by
   a deliberate mutation, with the red result recorded.
2. **The reader-facing documents are checked, not just the generated ones** — the counts a
   reader sees in README, QUICKSTART and PROJECT-STATUS are compared to the tree on every
   gate run, with a fixture proving the check fails when they are wrong.
3. **The suite runs under 10 minutes on a cold checkout** and its result is reproducible
   across two runs.
4. **No R1 behaviour remains `uncovered` without a recorded, owned debt item.**

## 6. Non-goals

- A coverage percentage target. Coverage is diagnostic here as everywhere.
- Running the CI workflow. It cannot execute; fixing billing is an owner action and
  outside this engagement.
- Testing the *content* of prompts for usefulness. That needs a second reader and is the
  documented gap in `_meta/evidence-levels.md`; this engagement measures the library's
  claim-checking machinery, not whether the prompts are good advice.
- Rewriting the validator into a framework. Plain scripts with printable cases work and
  are readable by the people who maintain them.
