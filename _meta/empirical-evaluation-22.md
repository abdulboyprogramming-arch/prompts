<!-- not-a-prompt -->

# Empirical Evaluation 22 — the PR description that cannot be wrong

**Date:** 2026-10-23
**Prompt:** `PR-01` (Write a Strong Pull Request) v0.1.0 → v1.0.0
**System:** `05-scenarios/pr-authoring` — promoted from skeleton this cycle
**Evaluator:** the author of the prompt (conflict of interest recorded)
**Method:** both versions run against the same real diff — commit `3abe628`, PR #45: 30 files, +825/−85.

---

## 1. Why this prompt, and why this input

`PR-01` was 57 lines: *summarise, structure, title, follow the template, be nice to the reviewer*. Written
against a real change, it produces exactly what a competent engineer would produce without it. The question
is whether that is enough — and this repository is a good place to ask, because its own pull request
template already ends with a section called **"Honest limits"**. The template knows descriptions lie by
omission. The skeleton did not.

The test input is the change that promoted `ONBOARD-01` (evaluation 21): a prompt rewritten, an eleven-file
fixture added, five indexes regenerated, a changelog entry, and a counts ripple. Thirty files, of which
**eleven are fixture source and five are derived**. A reviewer who reads them in file order spends their
twenty minutes badly. That is the whole job of the description, and it is invisible from the diff.

## 2. Grading table, written before either run

Nine requirements, one point each, no partial credit; a requirement counts only if a reviewer who did not
do the work could act on it without opening the diff. Full table in
`_meta/fixtures/pr-scenario/REQUEST.md`.

## 3. Run 1 — v0.1.0: **5 of 9**

| # | Requirement | v0.1.0 | Why |
|---|---|---|---|
| 1 | Product claim in the opening paragraph | **PASS** | "the rewrite turns the prompt from a description of a codebase into an evidence-based procedure ending in a takeover verdict" |
| 2 | Review order with a skip list | **FAIL** | no order at all. The eleven fixture files and the five derived files are offered to the reviewer as equals |
| 3 | Derived vs hand-written, with sources | **FAIL** | one bullet lists five index files as "regenerated" and never says which script produces which — so the reviewer cannot tell whether they were regenerated or hand-edited |
| 4 | What the change does not prove | **FAIL** | one sentence: the fixture is small. Nothing about the manufactured environment, the author-run conflict, or the parts never exercised |
| 5 | Reproduction | **PASS** | `check_all.py`, the fixture's `grep` commands, and the path to rerun the prompt |
| 6 | Rollback including consequences | **FAIL** | "git revert of the merge commit" — which leaves a tag, a release, five derived files and four prose counts describing a prompt that no longer exists |
| 7 | Counts ripple named | **PASS** | 74 → 73 skeletons, 287 operational, 39 of 287 (13.6%) |
| 8 | Title | **PASS** | `feat(onboarding): promote ONBOARD-01 from skeleton to a tested takeover procedure` |
| 9 | Template completed truthfully | **PASS** | type ticked, bar items true, Honest limits present and specific |

**What the 5 of 9 means.** The skeleton is not bad. It produces a description that an experienced engineer
would sign. It fails at exactly the three places where a description earns its keep: it does not tell the
reviewer **where to look**, it does not distinguish **what was regenerated from what was written**, and it
does not say **what it cannot prove**. Those are the three things the diff cannot tell you.

## 4. Run 2 — v1.0.0: **9 of 9**

The rewrite is nine steps, and three of them are the difference:

1. **Step 1 triages every file into four classes** — Behaviour, Evidence, Derived, Record — and requires
   each derived file to name its generator. The reviewer is told to spot-check five files, not read them.
2. **Step 6 makes "what this does not prove" a four-row table** — Scale, Environment, Independence,
   Doubt — with a floor of three categories and at least one unflattering. "Has been reviewed" is banned
   by name.
3. **Step 8 is "reject your own PR first"** — a self-review against the diff for stray files, secrets,
   unsupported claims, unregenerated derived files and leftover placeholders, with the rule that a finding
   is either fixed or stated with a reason.

The other six steps close smaller holes: the diff is the fact and the notes are the claim (so an item in
the notes that the diff does not contain is reported, not silently dropped); a product claim must come with
the smallest checkable thing behind it; rollback distinguishes reverting the commit from retracting a tag,
a release, or a published document; and the reviewer brief is capped at six lines because it is a routing
decision, not a summary.

Run 2 on the same diff scored 9 of 9 and produced the body this cycle's own pull request uses — the
prompt's output is shipped as the PR that ships the prompt.

## 5. What this evaluation does not show

- **It was graded by the author** against requirements written by the author. The fixture was written
  before the runs, which prevents post-hoc tuning, but it does not make the 9 of 9 independent.
- **"Twenty minutes" is asserted.** Nothing here measures review time or review quality with a second
  person. That would need a reviewer, and this repository has one contributor.
- **One diff shape.** A 30-file mixed-concern PR. A one-line bugfix and a 400-file refactor are untested;
  the "recommend a split" branch of §7 was never taken.
- **The template fallback is untested.** Every run had a repository template to fill.
- **The description's honesty depends on the reader.** Step 6 can be satisfied with true but useless
  limits ("works on my machine"). The prompt raises the floor; it cannot make an author candid.

## 6. Status

| Prompt | Before | After |
|---|---|---|
| `PR-01` | v0.1.0, skeleton, 57 lines, `NOT TESTED` | **v1.0.0, operational, `TESTED — PASS`** (5 of 9 → 9 of 9) |

The library's skeleton count falls from 73 to 72. Three single `05-scenarios` skeletons remain:
`LEGACY-01`, `PERF-01`, `QUICK-01`.
