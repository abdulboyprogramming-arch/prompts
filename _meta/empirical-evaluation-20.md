<!-- not-a-prompt -->

# Empirical Evaluation 20 — a prompt that decides what *not* to build, and the fixture that proved it wasn't one

**Date:** 2026-10-23
**Prompt:** `PORTFOLIO-01` (Feature Portfolio Decision) v0.1.0 → v1.0.0
**System:** `02-engineering/feature-portfolio` — new this cycle
**Evaluator:** the author of the prompt (conflict of interest recorded)
**Method:** desk runs against a committed fixture — eleven wants, two people, a repository whose
existing work is deliberately uneven — with the answers written into the fixture before the prompt was.

---

## 1. Why this prompt, and why now

Backlog #116: *nothing in the library decides between candidate features.*
`02-engineering/feature-design-suggestion` designs a feature once it has been chosen, and its seven
stages are still skeletons. `04-process/project-management/P02-Goals` writes goals and non-goals.
Between them is the step every product actually gets stuck on: a list arrives, everything is kept,
nothing is finished.

The prompt came from a real archived request — `archive/legacy-txt-files/feature-portfolio-decision.txt`,
formerly `process7(chat2).txt`, which asked for eleven capabilities, in one paragraph, with *"add as many
as possible"* as the only ordering principle. That request is the fixture's source material, which makes
this the rare case where the failure mode is documented by the person who lived it.

## 2. The fixture

`_meta/fixtures/portfolio-scenario/` — a Flask application called Reportwright (upload a CSV, get an
analysis, share it by token), plus the eleven wants. The tree is small enough to read and uneven on
purpose, because "does the model check the code before it ranks the list" is the whole question:

| Ground truth | How it is planted |
|---|---|
| The theme control is **half-wired** | `theme.css` defines the dark variables and `[data-theme]`; `settings.py` writes a `theme` cookie; **no template reads it** |
| Export is **half-built** | `export.py` serves CSV for the summary table only; PDF exists as a word in a comment |
| There are **no accounts** | no user, session, login or password code anywhere; reports are keyed by an unguessable token |
| The share link **already works** | `/r/<token>` in `app.py` |
| Accessibility **defects** | an input with only a placeholder, a table with no `scope` |
| Everything else is absent | no manifest, no service worker, no i18n, no notifications |

**The grading table was written before the run**, in `REQUEST.md`, and its "grading source" block is a
set of commands whose outputs are in the file — the third time this library has had to correct a fixture
against itself (routing, contribution, and now this one, where the first draft of the evidence block
claimed `settings.html` contained `data-theme`; `grep` says it does not).

## 3. Run 1 — v0.1.0: **0 of 8**

v0.1.0 is a competent-looking ranking prompt: group the list, score value against effort on a
three-point scale, rank, recommend three, sequence the rest, note risks. It is roughly what a careful
person writes on the first attempt. It produced a clean table of nine rows, three recommendations, and
a numbered sequence — and it is wrong in eight specific ways:

| # | Criterion | v0.1.0 | Why |
|---|---|---|---|
| 1 | Theme reported as half-built, missing step named | **FAIL** | recommended building "dark / light / system theme" from scratch; `theme.css` is never read |
| 2 | Export scoped as finishing an existing route | **FAIL** | "download the analysis" kept as new work; `export.py` never cited |
| 3 | Sign-in recorded as having nothing to hold, as an obligation | **FAIL** | ranked 7th of 9 with "the largest item"; nothing about what would be stored |
| 4 | Every candidate restated as a user problem | **FAIL** | all nine rows are the user's nouns, copied |
| 5 | Non-empty *Not now* with a reason per item | **FAIL** | a "sequence for the rest" — deferral, not decision |
| 6 | ≤3 *Now*, *Next* behind its dependency | **FAIL** | three *Now* items (pass) but a 4→9 sequence with no dependency, contradicting its own risk note that sign-in "should not block the others" |
| 7 | Accounts/analytics obligation: stored, where, how long, who reads, deletion | **FAIL** | none of the five |
| 8 | One slice end to end: change, test, rollback, user-visible sentence | **FAIL** | none |

**The diagnosis is not "the output was thin".** The output was plausible, well-formatted, and would pass
a human skim. The defect is structural: **v0.1.0 ranks the list it was handed.** It treats the candidate
names as facts about the product, so "add dark mode" and "add export" are both new work — when the
repository already contains 80% of one and 50% of the other. A prompt that never opens the repository
cannot know that, and no amount of better scoring fixes it.

There is a second defect, which matters more for a decision document: **v0.1.0 has no place to put a
"no".** Value/effort ranking always produces an order, and an order always has room for every row. The
list arrived with eleven items and left with eleven items.

## 4. Run 2 — v1.0.0: **8 of 8**

The rewrite changes what the prompt is *for*:

1. **Step 1 is a code check with citations.** Each candidate is looked up in the tree before it is
   scored, and "already exists" must name a file. This alone converts two candidates from builds into
   completions: theme (read the cookie in the base template — one day) and export (per-column CSV, then
   PDF).
2. **Step 2 restates each candidate as a user problem**, keeping the user's noun beside it. "PWA"
   becomes *a returning user on a phone cannot get back to a report without the link* — which, once
   written, argues itself into *Not now* because there are no returning users yet.
3. **Step 4 makes *Not now* mandatory and gives it a closed list of reasons.** Four of eleven items
   landed there, each with a reason from the list, not a vibe.
4. **Step 5 gives accounts, personal data and payments their own paragraph** — stored, where, how long,
   who reads, deletion path — and forbids folding them into a batch of improvements.
5. **Step 7 requires one slice to be finished**: change, failing-first test, rollback, and the sentence
   a user would notice.

Run 2's portfolio put **theme, export and accessibility** in *Now* — three items for two people in six
weeks — and four in *Not now*, including sign-in, on the grounds that the product has no per-user state
for accounts to hold. It also found something the criteria did not require: the share link already
exists (`/r/<token>`), so that candidate is a "show it and let it be revoked" item, not a build.

| # | Criterion | v1.0.0 |
|---|---|---|
| 1 | Theme half-built, missing step named | PASS — "80% built, 0% working; no template reads the cookie" |
| 2 | Export scoped as a completion | PASS — names the route, the summary-only limit, the missing PDF |
| 3 | Sign-in: nothing to hold, and an obligation | PASS — *Not now*, with the five-part paragraph |
| 4 | Candidates restated as problems | PASS — nine of nine |
| 5 | *Not now* non-empty, reasoned | PASS — four items |
| 6 | ≤3 *Now*, *Next* with dependencies | PASS — three; each *Next* row names what it waits for |
| 7 | Data obligation complete | PASS — stored, where, retention, readers, deletion |
| 8 | One slice end to end | PASS — theme: change, three tests, revert-only rollback, user sentence |

## 5. What this evaluation does not show

- **Desk runs by one executor.** The author wrote the prompt, wrote the fixture, ran it, and scored it.
  The ground truth is checked by command against the files, but the score is a judgement about whether
  an output meets a criterion the same author wrote.
- **The fixture was designed to be findable.** A real repository has twenty half-features, not two, and
  finding the relevant ones is harder than `grep data-theme`.
- **Stakeholder conflict is untested.** The *Not now* list is the part that has to survive an argument
  with the person who asked for the feature. The prompt gives the argument its materials
  (problem statement, cost, obligation); it cannot win the argument.
- **No downstream composition.** Nothing here shows that `FD-P01` produces a better design because it
  starts from a problem statement rather than a noun. The library still has no composition harness.
- **One prompt, one run.** This is the 38th recorded execution and the 38th by the author. The ratio in
  `_meta/evidence-levels.md` moves from 37 of 285 to 38 of 286 — still 13 %, still zero independent.

## 6. Status

| Prompt | Before | After |
|---|---|---|
| `PORTFOLIO-01` | did not exist (backlog #116) | **v1.0.0, operational, `TESTED — PASS`** (8 of 8) |

Backlog #116 is closed by this run. The library's second named gap, #115 (a mechanical Markdown
formatting pass), is still open and still unbuilt — deliberately: one validated prompt is worth more than
two drafted ones, and the same fixture discipline is what it will take.
