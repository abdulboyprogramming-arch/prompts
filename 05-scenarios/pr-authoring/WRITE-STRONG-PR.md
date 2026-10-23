# Write a Strong Pull Request — a description a reviewer can approve or reject in twenty minutes

**Identifier:** PR-01
**System:** 05-scenarios/pr-authoring
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A — read-only; the only write is the description itself
**Depends on:** none. Feeds `04-process/code-review/` (the reviewer's side of the same change), `04-process/git-operations/` (splitting or reverting), and `04-process/release-engineering/` when the PR is the release
**Produces:** `PR.md` — a title, a body, and a six-line reviewer brief
**Inputs:** COMMIT_RANGE or DIFF_PATH, BASE_BRANCH (optional: AUTHOR_NOTES, ISSUE_REF, REPO_PATH, TIME_BUDGET)
**Est. effort:** 20–40 min for a change under 50 files; longer when the diff mixes concerns that should have been separate PRs

---

## 1. Role and mandate

You are the author of a change, writing the description for someone who has twenty minutes and did not
watch you make it. Your job is not to summarise the diff — they can read it. Your job is to make the
review **cheap and honest**: what this changes, where to look first, what you checked, what you did not,
and how to undo it.

**The rule that governs everything below: the diff is the fact and your notes are the claim.** Your memory
of what you did is a summary written after the fact, and summaries are systematically optimistic — they
omit the file you forgot was in the change, the generated artefact you committed by hand, and the thing you
meant to test and didn't. Where the notes and the diff disagree, the diff wins, and the disagreement is a
finding you disclose rather than quietly correct.

**The second rule: a description that cannot be wrong is worthless.** "Updated the prompt and regenerated
indexes" cannot be wrong and cannot be reviewed. "Ran the new version against the same fixture and it
scored 9 of 9 — the old scored 0 of 9, and here is the file with both outputs" can be checked, and could
have been false.

## 2. Objective and scope

**In scope:** producing the description for a change that already exists.

**Out of scope:** making the change, deciding whether it should merge, rewriting history, and adding
evidence that does not exist. If the diff has a defect, you report it in the description or fix it before
writing — you do not describe it as though it were fine.

**When not to use this prompt:** when the change is still in progress (write it at the end); when you are
the reviewer (use `04-process/code-review/`); when the change is a release with its own notes
(`04-process/release-engineering/`).

## 3. Prerequisites and inputs

| Input | Required | What it is | If missing |
|---|---|---|---|
| `{{COMMIT_RANGE}}` or `{{DIFF_PATH}}` | yes | the change under review, e.g. `origin/main...HEAD` or a `.patch` file | stop; a description without the diff is a guess |
| `{{BASE_BRANCH}}` | yes | what the change lands on | infer, and say you inferred it |
| `{{AUTHOR_NOTES}}` | optional | your own notes, unedited | reconstruct from the diff and disclose that you had no notes |
| `{{ISSUE_REF}}` | optional | the ticket this closes | omit the link; do not invent one |
| `{{REPO_PATH}}` | optional | to read the PR template and commit conventions | use the conventions visible in the commit range |
| `{{TIME_BUDGET}}` | optional | how long the reviewer has | default: 20 minutes |

## 4. Workflow

### Step 1 — Triage the diff by class, before writing a word

List every changed file and put it in exactly one class. This is the step that decides whether the
reviewer spends their time on the right eight files.

```
git diff --stat {{BASE}}...{{HEAD}}
git diff --name-status {{BASE}}...{{HEAD}}      # added / modified / deleted / renamed / binary
```

| Class | Test | What the reviewer does with it |
|---|---|---|
| **Behaviour** | changing it changes what the software does | read it, in full |
| **Evidence** | fixtures, tests, recorded outputs, sample data | read the assertions, skim the data |
| **Derived** | produced by a script in the repo | confirm it was regenerated, do not read line by line |
| **Record** | changelog, review log, ledgers, status prose | skim for honesty, not for correctness |

For every **derived** file, name the command and the source of truth that produces it
(`python3 scripts/check_all.py --fix`, `generate_task_index.py`, `evidence_report.py --write`). If you
cannot name the generator, it is not derived — it is hand-written, and it belongs in Behaviour or Record.

### Step 2 — State one product claim

One sentence: **what changes for the person who uses this repository, or the software it modifies.** Not
"updates the prompt"; "the prompt now runs the start procedure instead of quoting it, so a takeover cannot
pass while the app has never been started."

Then the smallest piece of the diff that makes the claim checkable — a file and a line, a command and its
output, a before/after pair. A claim with nothing behind it is deleted, not softened.

### Step 3 — Reconcile the notes against the diff

Walk the author's notes and mark each item: **confirmed** (the diff shows it), **absent** (the notes claim
it, the diff does not contain it), or **unmentioned** (the diff does it, the notes forget). Absent and
unmentioned items go in the description: the first as "not in this change", the second as "also in this
change, which the notes missed". A reviewer who finds an unmentioned change stops trusting the rest of the
description.

### Step 4 — Give a review order that fits the budget

A numbered path through the Behaviour files, most consequential first, with a reason per step and an
explicit list of what to skip. Cheapest sufficient review, not most thorough review:

```
1. <file> — <why first: it decides whether the rest is safe>
2. <file> — <why next>
3. …
Skip: <derived files> (regenerated; spot-check one), <fixture data> unless you want to verify a trap
```

### Step 5 — Write the reproduction block

The commands that let the reviewer regenerate your evidence, in order, with the output you expect. For a
change with tests, that is the test command; for a prompt change, the command that reruns the prompt
against the same fixture, and the path where both outputs live. **If you cannot write this block, the
change has no evidence and the description says so.**

### Step 6 — Write "what this does not prove"

Not a disclaimer — a list. Four categories, at least three filled, and at least one that is unflattering:

| Category | The question to answer |
|---|---|
| **Scale** | what is the size of the thing tested, and what size is untested? |
| **Environment** | what was real, and what was manufactured to make the run possible? |
| **Independence** | who ran it, and were they the author? |
| **Doubt** | what are you least sure about in this change? |

"Untested on Windows" is a real limit. "Has been reviewed" is not a limit; it is a claim, and a weak one.

### Step 7 — Risk, blast radius, and exact rollback

Blast radius follows the classes from Step 1: Behaviour files fail loudly or quietly, Derived files drift
silently (a stale generated file is a lie the gate may not catch), Record files are prose that will be
believed. Then the rollback, which is more than `git revert`:

- the merge commit to revert, and whether the change is a single commit or a range;
- derived files that must be regenerated **after** the revert, and the command;
- anything published that a revert does not retract — tags, releases, deployed artifacts, published
  documentation, and who needs to be told;
- data or migrations that a revert does not undo at all, if any.

### Step 8 — Reject your own PR first

Before writing the body, try to refuse the change. Read the diff for:

- files that do not belong (editor config, local scratch, secrets, `.env`, large binaries);
- credentials or personal data in fixtures, examples, logs or screenshots;
- claims in the description with no command behind them;
- derived files committed without being regenerated (open one and check a value you know changed);
- leftover placeholders, `TODO`, debug prints, commented-out code that is not deliberate;
- a mixed-concern diff that should be two PRs.

Anything you find, you **fix it, or state it in the description with the reason it is acceptable**. This is
the step that makes the rest of the description trustworthy.

### Step 9 — Title, then the template

Title: imperative, specific, and naming the thing, not the verb — "ONBOARD-01: executes the start
procedure instead of quoting it", not "Update prompt". Follow the repository's commit convention if the
title becomes the commit subject.

If the repository has a pull-request template, **fill it** rather than replacing it, and leave none of its
sections empty. Its checklist items are claims: tick one only if you can point at the command that proves
it.

### Step 10 — Cut it in half

Read the draft as the reviewer. Delete everything that does not change what they do in the next twenty
minutes: restated diffs, adjectives, thanks, and any sentence that survives being false.

## 5. Output

```
PR.md
├── TITLE              one line, imperative, names the thing
├── BODY               the template filled, or these sections in order:
│                       What this changes · Why · Review order · Reproduction
│                       What this does not prove · Risk and rollback · Evidence
└── REVIEWER BRIEF     ≤ 6 lines: the three files to open, the one thing to check, the one thing to ignore
```

`REVIEWER BRIEF` is what the author says when asked "quick, what should I look at?" — it is not a summary
of the body, it is a routing decision.

## 6. Verification

Run before publishing. Each line is checkable by someone else.

| # | Check | How |
|---|---|---|
| V1 | Every changed file is classified | the Step 1 table covers the `--name-status` output with no gaps |
| V2 | Each derived file names its generator | a reader could regenerate it from the description alone |
| V3 | The product claim is checkable | it points at a file, a command, or a before/after |
| V4 | Notes reconciled | every note is confirmed, absent, or unmentioned — explicitly |
| V5 | Review order fits the stated budget | the Behaviour files in the order are the ones that decide the outcome |
| V6 | Reproduction block runs | you ran it, and the output matches what you wrote |
| V7 | `What this does not prove` has ≥ 3 categories, ≥ 1 unflattering | count them |
| V8 | Rollback names derived-file regeneration and any published artefact | the tag/release/artifact question is answered, even if the answer is "none" |
| V9 | Self-review found something, or you can say why not | the Step 8 list was actually run |
| V10 | Template sections all filled | no empty heading survives |

## 7. Failure handling

| Situation | Do this |
|---|---|
| No notes and no ticket | reconstruct from the diff, and say the motivation is inferred. Do not invent one |
| Diff over ~1000 lines | write the review order for the smallest coherent subset and say the rest is a skim; recommend splitting if the classes are independent |
| Derived file committed without regeneration | state it, regenerate it if you can, and note that the gate did not catch it — that is a finding about the tooling |
| The diff contains a secret | do not reproduce the value anywhere, including the description; name the file and line and say what must be rotated |
| The diff is binary, a rename, or a vendored dump | give the reviewer the summary and the command to inspect it; do not paste it |
| You find a defect you cannot fix | the PR is not ready; describe the defect and mark the PR as blocked rather than describing the change as complete |
| The change should be two PRs | say so, and name the split; shipping a mixed-concern PR with a good description is still a mixed-concern PR |

## 8. Security and authorisation

Read-only. The description is published: it must not contain credentials, tokens, personal data,
customer names, internal hostnames, or anything from a private channel that the repository's audience
cannot see. Screenshots are part of the description — treat browser chrome, tabs, and notification popups
as content.

## 9. Completion criteria

- [ ] every changed file classified, with derived files mapped to a generator
- [ ] one checkable product claim
- [ ] review order with a skip list, fitted to the reviewer's budget
- [ ] reproduction block that was actually run
- [ ] `What this does not prove` with ≥ 3 categories, ≥ 1 unflattering
- [ ] rollback including derived files and published artefacts
- [ ] self-review pass done, findings stated
- [ ] template filled, none of it empty
- [ ] reviewer brief of ≤ 6 lines

## 10. Handoff

The description is the input to `04-process/code-review/` — the reviewer's prompt reads exactly this
document and asks whether the claims hold. When a PR is reverted, `04-process/git-operations/` owns the
history and `04-process/release-engineering/` owns any tag or release that a revert does not retract.

## 11. Testing and known limitations

Run at v1.0.0 against `_meta/fixtures/pr-scenario/` — the real 30-file diff of commit `3abe628` — where
it scores 9 of 9 against requirements written before either version ran; v0.1.0 scored 5 of 9 on the
same input. Record: `_meta/empirical-evaluation-22.md`.

Known limitations:

- **No independent review.** Graded by the author against written requirements, not by a reviewer
  approving the result. Nothing here shows the description made a real review faster.
- **One diff shape.** A 30-file PR that mixes a rewrite, a fixture and regenerated indexes. A
  single-file bugfix and a 400-file refactor are untested.
- **The template requirement is repository-specific.** A repository with no template gets the fallback
  section order in §5, which was never exercised against a real reviewer.
- **The twenty-minute budget is asserted, not measured.**
