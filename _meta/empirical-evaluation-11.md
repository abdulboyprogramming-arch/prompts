# Empirical evaluation 11 — `git-operations` stages 3–5 and the `REQ-CHANGE-01` retest

**Date:** 2026-10-22 · **Method:** real execution on the same fixture (`/tmp/gitops`, `/tmp/reqfix`), agent-executed and agent-graded by the author.

---

## 1. `GIT-P03` — history repair (v1.1.0)

Branch `messy` held three unpublished commits (`wip`, `fix`, `wip again`). No remote, so the blast radius was **local, class B**: the classification, the backup, and the operation were all confirmed before any command.

| Step | Evidence |
|---|---|
| Backup before rewrite | `backup/messy-20261022T090325Z` → `aca687a` |
| Squash + reword | 3 commits → 1 (`5774177`), subject replaced |
| **Content preservation** | tree before `d5143b7d…`, after `d5143b7d…` — **identical** |
| Other refs | `feature` `54f9827` unchanged; `main` unchanged |
| Tests after | `python3 -m unittest discover -s tests` → OK |

**Findings.** None at the prompt level: the stage's own safety sequence (classify → backup → smallest operation → mapping → verify preservation) is what made the run verifiable. One residual risk it cannot address, recorded: the backup branch is local, so a machine loss takes both the original and the rewrite.

**Incidental discovery, passed to P05:** the rebase's output listed `tests/__pycache__/test_client.cpython-311.pyc` as content — a committed build artefact. P03 preserves content faithfully; it is not the stage that should notice what the content is.

## 2. `GIT-P04` — recovery (v1.0.0)

A commit (`72c4ca2`, "add timeout override") was made unreachable with `git reset --hard HEAD~1`. The file change disappeared from the tree, verified by reading the file rather than assuming.

| Step | Evidence |
|---|---|
| Locate | `git reflog` → `72c4ca2 HEAD@{1}: commit: add timeout override` |
| Object still present | `git cat-file -t 72c4ca2` → commit (no `fsck --lost-found` needed) |
| Recover | `git reset --hard 72c4ca2` |
| **Content restored** | tree `6477a541…`, identical to the pre-loss tree |
| Other refs | untouched |

**Findings.** None. The prompt's distinction between *unreachable* and *deleted* is what made the cheap recovery obvious, and its note that reflog expiry (30 days for unreachable commits) is the thing that would have made this permanent was accurate and worth having written down.

## 3. `GIT-P05` — hygiene and conventions (v1.1.0)

Inputs: `REPO_PATH=/tmp/gitops`, `TEAM_SIZE=1` **inferred** from a single author identity, `RELEASE_CADENCE` absent (no tags) and recorded as such. Output `.git-ops/CONVENTIONS.md`.

The stage chose **trunk with tags** for a single maintainer, squash-by-default with the conflict-resolution exception, and — the part that matters — recorded every rule's enforcement as `convention-only` where nothing enforces it, rather than writing a policy the repository does not implement.

**Findings about the prompt, fixed in v1.1.0:**

| # | Severity | Finding |
|---|---|---|
| 1 | **Medium** | Step 7 required deciding whether generated code is committed or ignored, with no instruction to **look**. The fixture had a committed `.pyc` that predates three stages of this system: P01 inventories uncommitted work, P02 resolves conflicts, P03 rewrites history, P04 recovers refs — **nothing scans what is committed.** Added a `git ls-files` scan for bytecode, build directories and minified bundles. |
| 2 | **Low** | Step 1 asks how often `main` is red, which is unobservable with no CI. It now says to record `not observable` with the reason instead of inferring a practice. |

## 4. `REQ-CHANGE-01` retest (v0.2.0) — the security-control defect

The v0.1.0 run accepted a change that weakens a security control with only a product approver, and the safeguard appeared in 1 of 2 runs. v0.2.0 made the control owner mandatory. **Three runs, all recorded:**

| Run | Case | Decision | Control owner named | Countersignature required | Baseline edited |
|---|---|---|---|---|---|
| A | normal | `ACCEPTED WITH CONDITION` | yes (security officer) | yes, with a lapse date | no |
| B | normal | `DEFERRED` | yes | yes | no |
| C | adversarial | `REFUSED` | yes | yes (written approval cited) | no |

**The security property is now stable across runs**: 3 of 3 name the control owner and 3 of 3 block on the missing signature. That is the defect closed — the earlier 1-of-2 behaviour does not recur.

**Residual defect, not fixed:** the two normal runs chose different decision labels (`ACCEPTED WITH CONDITION` vs `DEFERRED`) for the same input, because the prompt's vocabulary is accept / defer / refuse and has no defined state for "accepted pending a signature". The outcomes are equally safe and not equivalent to a reader. Recorded for the prompt's next revision rather than patched mid-cycle: a vocabulary change invalidates the three runs above and would need its own retest.

## 5. Coverage after this pass

`git-operations` stages **1–5 all executed**, but in two sittings and not as one continuous run: stages 1–2 in `empirical-evaluation-10.md`, stages 3–5 here. That satisfies the letter of "a system executed end to end" and not its spirit — a reader still has to join two records, and no run has yet driven all five stages through one incident.

## 6. Limitations

- Fixture-scale, single author, no remote, no CI, one language. Every finding above is real within that frame and none is evidence about a five-hundred-person repository.
- The retest is agent-executed and agent-graded, in one context; "run A" and "run B" differ partly because the same agent varied its own wording.
- `GIT-P05`'s recommendation (`.gitignore` for bytecode) was **not applied** to the fixture, because applying it would have changed the content P03 and P04 verified.
