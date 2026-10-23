# Pull-request record

Required by the standing brief: every pull request gets a row, so the merge
history can be read without trusting anyone's memory. Numbers, states and
timestamps below were read from the API, not reconstructed.

## Open

| # | Title | Branch → base | Purpose | Status | Reviewer | Checks | Merge commit | Owner reviewed in person |
|---|-------|---------------|---------|--------|----------|--------|--------------|--------------------------|
| 35 | 2.28.6 — `06-interactive` completed: the router scored against the repository's own index | 2026-10-22 | `556ce7b` | Merged under the standing merge authority with the admin bypass the owner added to the ruleset. First system completed by execution rather than review: `WIZ-P01` 5/14 → 14/14 on a fixture derived from `TASKS.md`, `INT-P02` 0/5 → 5/5, `INT-P03` 1/8 → 8/8. CI run `39851067467` green |
| 34 | 2.28.5 — the repository is public; `INT-P01` run, failed 0/5, rebuilt to 5/5 | 2026-10-22 | `815f57c` | Merged under the standing merge authority **after the owner added Repository admin as a bypass actor** on the `Protect default branch` ruleset; the same PR was `BLOCKED` before that, because one approval was required and GitHub forbids self-approval. Three CI runs green (`39846014231`, `39846144167`, `39846320817`, `39846425944`) |
| 34 | 2.28.5 — the repository is public; `INT-P01` run, failed 0/5, rebuilt to 5/5 | `arena/7c0856d5-prompts` → `main` | Publication verified unauthenticated; first executed CI run in the repository's history; first `06-interactive` execution and its repair | **Open — blocked by the branch ruleset** | CI green (`39846320817`, `validate`, success) | 3 green runs | — | Not mergeable: the *Protect default branch* ruleset requires 1 approving review, GitHub refuses self-approval (`422`) and no bypass actor is configured, so `--admin` is refused too. Owner action: add *Repository admin* as a bypass actor, or set required approvals to 0 (`repository-configuration.md` §4a) |

## Closed without merging

| # | Title | Closed | Why |
|---|-------|--------|-----|
| 19 | 2.25.1 — `MLA-P03` tested against a committed leakage fixture, v1.1.0 | 2026-10-22 | Closed automatically when merging #18 deleted its base branch `arena/d7fd2ca8-prompts`; GitHub cannot reopen a PR whose base is gone. Reopened against `main` as #20, with the same commit rebased. Left closed with a comment linking forward |
| 13 | Gate runner: restore the catalog on failure, self-test the runner; code-review P01-P03 v1.1.0 | 2026-10-22 | Opened by the owner account, which makes the owner's review impossible: GitHub refuses a review request from the author (`422`) and disables *Approve* on your own pull request. Superseded by #14 from the same content on a fresh branch; nothing in it was reviewed or approved |

## Merged

Record-only pull requests — the ones whose entire content is this table — cannot record their own merge commit, because it does not exist when they are written. They are listed here instead: #25 (`720687c`, recording #24) and #27 (`ddc2920`, recording #26). The same applies to any later record-only PR, including the one that adds this note.

| # | Title | Merged | Merge commit | Notes |
|---|-------|--------|--------------|-------|
| 47 | 2.31.0 — `PR-01`: a description a reviewer can act on in twenty minutes | 2026-10-23 | `f4bbc0a` | Merged under the standing merge authority. v0.1.0 scored 5 of 9 on the real 30-file diff of `3abe628`; v1.0.0 scores 9 of 9 with a four-class file triage, a what-this-does-not-prove table and a self-review pass. Evidence 40/288 (13.9%). CI run `39909927605` green. Tag `v2.31.0` on this commit. The evidence gate was also exempted from scanning fixtures, because it failed on a recorded run output that quoted a then-true ratio |
| 45 | 2.30.0 — `ONBOARD-01`: a takeover prompt that executes instead of describing | 2026-10-23 | `3abe628` | Merged under the standing merge authority. Run as written (0 of 9) then rebuilt (9 of 9) against a committed six-file fixture with an undocumented environment, a schema that disagrees with its models, a Dockerfile that cannot start, no tests, personal data with no deletion path and a hardcoded payment-key placeholder. Evidence 39/287 (13.6%). CI run `39907125285` green. Tag `v2.30.0` on this commit. PR #44 was record-only and, per the rule above, is not listed |
| 43 | 2.29.0 — `PORTFOLIO-01`: the prompt that decides between candidate features | 2026-10-23 | `dee7c5b` | Merged under the standing merge authority. Closes backlog #116. Built, run (0 of 8), rewritten and re-run (8 of 8) against a new fixture whose theme control is a cookie nothing reads. Evidence 38/286 (13.3%). CI run `39906410962` green. Tag `v2.29.0` on this commit |
| 41 | 2.28.9 — archive fragments replaced in place; one stale branch removed | 2026-10-23 | `6a589f8` | Merged under the standing merge authority. Four `.txt` files that were never prompts replaced and renamed; `rewritten/` deleted and its cost recorded in the archive README. `arena/5b041870-prompts` deleted after checking it held 0 files `main` lacks (PR #13 closed, pre-rewrite lineage); `main` is now the only branch. CI run `39905266097` green. Tag `v2.28.9` on this commit |
| 39 | 2.28.8 — correct seven stale statements about CI, merges and maturity | 2026-10-23 | `7363e5f` | Merged under the standing merge authority. README said the Actions workflow does not run; run `39903440904` executed steps 1–5 and passed. Also corrected: skeleton count 131→74, "three runs"→37, PROJECT-STATUS "five external blockers"→two owner-only, release-readiness "branch protection blocks all merges"→cleared, 23 releases→26, publication-checklist §5.1 and bottom line. Decision record left as written with a dated banner. CI run `39904132836` green. Tag `v2.28.8` on this commit |
| 37 | 2.28.7 — audit the legacy `.txt` requests; rewrite the four short ones | 2026-10-23 | `4dde0f3` | Merged under the standing merge authority with the admin bypass. First full read of the twelve archived files (18,835 lines): three unsuperseded constitutions, an instruction that cannot terminate, scope with no stop condition, four rules the library now forbids, and a self-contradiction about "production-ready". Four short requests rewritten in `archive/legacy-txt-files/rewritten/` (since removed); originals byte-identical; counts unchanged (491 files, 364 prompts, validator 0/0). CI run `39903310147` green. Tag `v2.28.7` on this commit |
| 36 | 2.28.6 — record the merge commit for #35 and the `v2.28.6` release | 2026-10-22 | `b5a0114` | Record-only. CI run `39851235499` green |
| 32 | 2.28.4 — publication readiness re-measured: content ready, visibility still owner-only | 2026-10-22 | `e5bfa0c` | Merged under the standing merge authority. Re-ran all 23 publication gate rows, corrected ten drifted figures, re-assessed six coverage rows, fixed a misleading prose-lint summary and one leaked sandbox path, and re-scanned history under an unshallowed clone (61 commits, 22 tags, 0 hits). Release `v2.28.4` created at the merge commit |
| 31 | docs(release): publish the twelve missing releases; fix two stale figures | 2026-10-22 | `25b14dc` | Merged under the standing merge authority. Created `v2.22.0`–`v2.28.3` after the tag list stopped seven versions behind, and corrected a file total (462 → 485) and an execution ratio (1.8% → 11.7%) in the readiness page |
| 29 | 2.28.3 — testing-QA stage 7: the orchestrator run, and a ledger three releases stale | 2026-10-22 | `f363f90` | Merged under the standing merge authority. The orchestrator run recorded two partial checks rather than green: the mandatory P01 checkpoint cannot be held by a solo author, and 3 of 12 fixtures are guards with no red state. The `validate` check run again reported `failure` with `steps: 0` — Actions billing, not a test result |
| 26 | 2.28.2 — testing-QA stages 3–6: placeholder and empty-section rules made blocking | 2026-10-22 | `1b843a5` | Merged under the standing merge authority. The `validate` check run reports `failure` with **`steps: 0`** — the runner never started a step because Actions billing is not enabled, so it is not a test result and nothing in the repository was gated by it; the local suite was green (0 errors / 0 warnings, 44/44, all gates passed) before merging, and that is the only enforcement evidence that exists |
| 24 | 2.28.1 — testing-QA stages 1–2 run against this repository; risk-class-A rule made blocking | 2026-10-22 | `ce2ec6d` | Merged under the standing merge authority; the run found a gate that could not fail and made it blocking |
| 23 | 2.28.0 — devops-infra family completed (`DI-P01`…`DI-P08`) | 2026-10-22 | `b1cbc9a` | Merged under the standing merge authority; locked state with a recovery procedure and a four-condition plan gate |
| 22 | 2.27.0 — frontend family completed (`FE-P01`…`FE-P08`) | 2026-10-22 | `64cdd05` | Merged under the standing "merge all" authorisation; state matrix with no blank cells, one owner per piece of state |
| 21 | 2.26.0 — backend family completed; prose counts now gated | 2026-10-22 | `a159e24` | Merged under the standing "merge all" authorisation; validator rule added after `PROJECT-STATUS.md` was found three releases stale |
| 20 | 2.25.1 — `MLA-P03` tested against a committed leakage fixture, v1.1.0 | 2026-10-22 15:08:05Z | `a497cec` | Independent of #18 after merge; a stage run against four planted defects found one |
| 18 | 2.25.0 — data / ML / AI family completed (`MLA-P01`…`MLA-P08`) | 2026-10-22 15:07:27Z | `0376e12` | Stacked #19 had to be re-opened as #20 after `--delete-branch` removed its base |
| 17 | 2.24.0 — game-development family completed (`GD-P01`…`GD-P08`) | 2026-10-22 14:51:48Z | `a54a896` | Merged by the agent under an explicit grant for this PR |
| 16 | 2.23.1 — three contribution systems completed; `PKG-P01` executed on a real package | 2026-10-22 14:28:25Z | `a82731a` | — |
| 15 | 2.23.0 — performance system completed and run on the gate suite (−25% suite time) | 2026-10-22 14:22:54Z | `725075d` | — |
| 14 | Gate runner: restore the catalog on failure, self-test the runner; code-review P01-P03 v1.1.0 | 2026-10-22 14:11:42Z | `a6d849a` | — |
| 12 | 2.22.0 — git-operations completed, security-control fix retested, publication decision (hold) | 2026-10-22 09:24:28Z | recorded as `1dc6f25`; the history rewrite that followed changed it to `3a62a6b` | merged under the owner's explicit final authorization |
| 11 | 2.21.1 — run CHAT-DEBUG, fix the defects it found | 2026-10-21 14:45:29Z | — | pre-record |
| 10 | v2.21.0 — Conversational mode: the library in a chat window | 2026-10-21 14:42:23Z | — | pre-record |
| 9 | v2.20.0 — A starting point for people, and lint for the prose | 2026-10-21 14:31:28Z | — | pre-record |
| 8 | v2.19.0 — The estate, and the library measuring itself | 2026-10-21 14:15:22Z | — | pre-record |
| 7 | v2.18.0 — Compliance, automation, and verification of AI output | 2026-10-21 14:04:55Z | — | pre-record |
| 6 | v2.17.0 — Complete the coverage map | 2026-10-20 15:11:31Z | — | pre-record |
| 5 | 2.16.0 — tenant isolation, secret rotation, background jobs, email deliverability, a11y, data engineering | 2026-10-20 14:59:36Z | — | pre-record |
| 4 | 2.15.0 — prompt forge, prompt regression, web3/mobile/embedded domains, games save+netcode, RAG + agent permissions | 2026-10-20 14:48:20Z | — | pre-record |
| 3 | 2.14.0 — deployment targets, host migration, dev environments, agent context, on-call handover | 2026-10-20 14:32:04Z | — | pre-record |
| 2 | fix: exact MIT licence text so GitHub detects SPDX MIT (v2.13.1) | 2026-10-20 14:10:05Z | — | pre-record |
| 1 | Enforce library standards, rewrite core systems, add missing prompt families | 2026-10-20 14:07:26Z | — | pre-record |

"pre-record" means the row was added after the fact from the API's merge
timestamp; the branch names and review states of those pull requests are not
recorded here because this file did not exist while they were open. Inventing
them now would be worse than the gap.

## One account, and what it costs

The repository has one identity: `abdulboyprogramming-arch`, displayed as
Abdulrahman Adeeyo. Every commit on `main` and on this branch carries it as
author and committer.

On 2026-10-22 a second account, `Abdul-Programing` (id `259543701`, already a
collaborator with write access), was tried as the contributor so that the owner
could review and approve a pull request the owner had not opened. That required
GitHub device authorisation in the owner's browser; three attempts authenticated
the owner's own account instead, and the owner then instructed that the split be
dropped. No commit in the repository now carries that account, and the two-account
re-authoring was reversed by rewriting the branch before it was pushed anywhere
that matters.

The cost is stated rather than hidden: **a pull request opened by the owner
cannot be approved by the owner.** GitHub returns `422 Review cannot be requested
from pull request author` and offers no *Approve* on your own pull request. So
PR #14 can carry a comment review and an explicit merge instruction, and it does
not carry an independent approval, because none was possible on this repository
with one account.

## Standing rules

- No pull request is merged before the owner has reviewed it. The one exception,
  PR #12, was authorised in advance and in words.
- No review is ever written, approved or dismissed in the owner's name by an
  agent. The 422 above is the API enforcing the same rule that the brief states:
  an agent running as the owner cannot review the owner's pull request.
- A check that did not run is recorded as not run. *Corrected 2026-10-23 (2.28.8): this
  rule read "CI has never executed a step on this repository", which was true until the
  repository was published on 2026-10-22. Run `39846014231` was the first to execute every
  step; every run since has.*
