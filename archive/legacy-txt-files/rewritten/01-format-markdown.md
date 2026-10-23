<!-- not-a-prompt -->

# Rewrite 01 — "properly format and organize the .md files"

**Source:** [`../Format dot md file.txt`](../Format%20dot%20md%20file.txt) — 1 sentence, 133 bytes, no trailing newline
**Status:** archive rewrite. The original is preserved byte-for-byte and is still the historical record; this file is the clear statement of what that sentence was asking for.
**Closest library prompt:** `04-process/documentation/P07-Review/P07-Review-Validation.md` (`DOC-P07`) for the publication check, plus `scripts/validate_library.py` for links and structure. Neither is a formatting pass — see §5.

---

## 1. The original, verbatim

> i need you to properly format and organize the content of all .md file in this project monorepo so it can be clean and well presented

## 2. What it was trying to say

*"The Markdown in this repository is inconsistent — headings at the wrong depth, tables that do not
render, links that point nowhere, mixed list markers, stray whitespace. Go through the files and make
the presentation consistent, without changing what any of them actually says."*

## 3. Why the original fails as a prompt

| Defect | What actually happens when an agent receives it |
|---|---|
| **"properly format"** names no standard | the model invents one, and invents a different one next run. Nothing can be checked afterwards |
| **"all .md file"** is unbounded | in a 400-file repository this becomes a mass rewrite, and a mass rewrite cannot be reviewed |
| **no non-goal on prose** | "so it can be clean and well presented" invites re-wording. A formatting pass that rewrites sentences destroys the review, because every line is now changed |
| **no verification** | "clean and well presented" cannot pass or fail, so the run ends with a claim rather than a result |
| **no batching** | one bad pass over the whole tree, and no clean commit to return to |
| **no scope for what to leave alone** | generated files, licence text, and vendored docs get reformatted, and their meaning or legal effect can change |

## 4. The rewritten prompt

> **Role.** You are reformatting the Markdown in this repository. You are not editing it. Every change
> you make must be one that a reviewer can justify as *presentation only* — if a change could alter what
> a sentence means, you do not make it.
>
> **Inputs.** `{{REPO_PATH}}`, and `{{FILE_GLOB}}` if the pass is limited to part of the tree. If
> `{{FILE_GLOB}}` is absent, use every tracked `.md` file **except** the exclusions in *Do not touch*.
>
> **Do not touch.** `LICENSE`, `LICENSE-*`, `archive/`, any generated file (one carrying a
> `do not edit by hand` line), any file whose content is quoted from a third party, and any file that
> fails to parse as Markdown before you start — report those instead.
>
> **Step 1 — measure before changing.** For each file record: heading depths used and whether they
> skip a level; fenced code blocks and whether they are balanced; tables whose column count differs
> between header and separator; relative links and whether the target resolves; list markers in use;
> trailing whitespace; blank-line runs over two. Write the counts to `FORMAT_BASELINE.md`. **Do not
> change a file in this step.**
>
> **Step 2 — propose the rule set.** State the six or seven rules you will apply, in one line each, for
> example: *"headings start at H1 and never skip a level"*, *"one list marker style per file: `-`"*,
> *"no trailing whitespace; exactly one blank line between blocks"*, *"every relative link resolves or is
> reported"*. Get agreement on these before editing, because they are the whole of the change.
>
> **Step 3 — apply in batches of ten files.** After each batch: `git diff --stat`, then read the diff.
> A batch that changes more than presentation — a reworded sentence, a moved paragraph, a deleted
> "redundant" clause — is reverted with `git checkout -- <files>` and redone. Commit each batch
> separately with the rule set in the message, so any batch can be reverted alone.
>
> **Step 4 — verify with the repository's own checks, not your judgement.** Run the link and structure
> checks the repository already has (here: `python3 scripts/validate_library.py`); run a Markdown
> renderer over a sample of ten files and confirm the headings and tables appear as intended. Report
> before/after counts from `FORMAT_BASELINE.md`.
>
> **Step 5 — report.** Files touched, rules applied, files skipped and why, links still broken (with
> the reason each is not fixable by formatting), and the diff size. **A file you formatted and a file
> you fixed are different claims** — say which each one was.
>
> **Stop conditions.** A file that would need re-wording to be consistent → leave it, list it, do not
> re-word. A link whose target is missing → report it; do not invent a file to point at. More than
> forty files in scope → do the first forty, report, and wait; a 400-file diff is not a formatting
> pass, it is a rewrite nobody can review.
>
> **Done when:** every in-scope file follows the agreed rule set, the repository's own checks pass, the
> diff contains no changed prose, and the report accounts for every file that was in scope.

### What changed, phrase by phrase

| Original | Rewritten as | Why |
|---|---|---|
| "properly format" | six named, checkable rules agreed before editing | "properly" is not a standard; a named rule set can be reviewed and re-run |
| "all .md file" | every tracked `.md`, with an explicit exclusion list | the exclusions are where a careless pass does damage |
| "organize the content" | **removed** — content organisation is `DOC-P05` (a plan) and `DOC-P06` (writing), not a formatting pass | two different jobs in one sentence is how the wrong one gets done |
| "clean and well presented" | before/after counts from `FORMAT_BASELINE.md`, plus a rendered sample | an adjective cannot pass or fail; a count can |
| *(absent)* | batches of ten, one commit each, revertible | makes the work reviewable and the mistakes cheap |
| *(absent)* | "a file you formatted and a file you fixed are different claims" | the honest-reporting rule this repository applies everywhere |

## 5. Does the library cover this now?

**Partly, and the gap is worth naming.** `DOC-P07` reviews and publishes documentation products; the
validator checks links, headings and required sections. Neither is a mechanical formatting pass over an
existing tree, and neither has a "presentation only, no prose changes" rule — which is the rule that
makes such a pass safe.

Whether that is a library gap or deliberate restraint is recorded in
[`../../../_meta/ROADMAP-AND-BACKLOG.md`](../../../_meta/ROADMAP-AND-BACKLOG.md); this file does not
create a new prompt, because the honest first step is one run of the prompt above, not a new system.
