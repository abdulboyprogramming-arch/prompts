# PR scenario fixture — a real 30-file change

**Purpose:** the test input for `PR-01` (`05-scenarios/pr-authoring/WRITE-STRONG-PR.md`). Written before
either prompt version was run, so the grading table could not be tuned to a result.

**Status of the change:** real. `DIFF.patch` is the verbatim diff of commit `3abe628`
(PR #45, 30 files, +825/−85) in this repository. It is a genuinely awkward change for a reviewer: a
prompt rewrite, a new eleven-file fixture, six regenerated indexes, a changelog entry, and a counts
ripple from 74 to 73 skeletons.

**The task given to the prompt:** produce the pull-request description for this change, for a reviewer who
has 20 minutes and did not follow the work.

## Inputs given to the prompt

| Input | Where |
|---|---|
| Diff | `DIFF.patch` in this folder |
| Author's own notes, unedited | `NOTES.md` in this folder |
| Repository conventions | `.github/pull_request_template.md` at the repo root |
| Base / head | `333509e` → `3abe628` on `main` |
| Gate output | `python3 scripts/check_all.py` → all gates passed |

## The nine requirements, and how each is checked

Each line names the objective check. "The reviewer can…" means a person who did not do the work.

| # | Requirement | Check |
|---|---|---|
| 1 | The opening paragraph says what the change **does for the user of the library**, in one read, not a file inventory | First paragraph names the prompt and the behaviour change; does not begin with "this PR updates…" |
| 2 | **Review order** — which files to read first and why, given that 11 of the 30 are fixture noise | A named sequence with a reason per step, covering the prompt file and excluding at least the generated indexes |
| 3 | **Derived vs hand-written** — which files are regenerated and must not be reviewed line by line | Names `TASKS.md`, `GALLERY.md`, `_meta/CATALOG.md`, `_meta/conformance-report.md`, `_meta/evidence-levels.md` as generated; names the source of truth for each |
| 4 | **What the change does not prove** — stated as a limit, not a disclaimer | At least: six-file fixture ≠ large repository; author-run; no independent run; the "cut order" path unexercised |
| 5 | **Reproduction** — the commands a reviewer runs to see the evidence themselves | `check_all.py`, plus the command that reruns the prompt against the fixture, plus where the two outputs live |
| 6 | **Rollback** — exact, including consequences beyond `git revert` | Names the tag/release implication and the fact that reverting the prompt alone leaves the fixture orphaned |
| 7 | **The counts ripple**, named so a reviewer can check honesty | States 74 → 73 skeletons, 287 operational, 39 evidence records (13.6%), and why those numbers moved |
| 8 | Title: imperative and specific, matching repo convention | Not "Update prompt"; names the prompt and the change |
| 9 | The repository's own PR template completed truthfully, including its **Honest limits** section | Type box ticked; "the library's own bar" items true; Honest limits non-empty and specific |

**Scoring:** 1 point per requirement, no partial credit. A requirement is met only if a reviewer who did
not do the work could act on it without opening the diff.

## What this fixture cannot test

- Whether the description *helped* — that needs a real second reviewer, and this repository has one
  contributor. The grading is against the written requirements, not against review outcomes.
- Large-diff behaviour beyond 30 files / 1255 diff lines.
