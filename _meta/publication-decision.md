# Publication Decision — 2.22.0, 2026-10-22

**Question:** can this repository be published publicly *now*, honestly, without waiting for full validation?

**Answer: yes** for publication as an experimental, actively-developed library, with one honesty fix applied in this pass (the CI claim) and no repository-side blocker remaining. **No** for any claim that the prompts are validated, proven, or production-ready — 26 of 273 have been executed, all by the author, none by a second person.

---

## 1. Publication and full validation are different requirements

| | **Publication** asks | **Full validation** asks |
|---|---|---|
| Test | Can a stranger read this, use it, and understand exactly how far it has been proven? | Does each procedure work when someone else runs it? |
| Evidence needed | licence, no secrets, usage instructions, accurate status, policies, checks that pass | independent runs, per-prompt evidence, end-to-end systems |
| Current state | **met** (§2) | 26 of 273 executed (9.5%); 0 independent runs |

Conflating them is what turns readiness into an endless cycle: full validation of 228 procedures needs months and other people, while publication needs a truthful snapshot. The library's own rule applies — label the claim and ship the evidence.

## 2. MUST FIX BEFORE PUBLICATION

**None open.** Each requirement, with the check that produced the evidence:

| Requirement | Evidence | Status |
|---|---|---|
| Open-source licence | `LICENSE` = MIT; `LICENSE-CONTENT` = CC BY 4.0 full text; both linked from the README | met |
| No exposed secrets or unauthorised material | `grep` over the tree and over all 19 commits for `ghp_`, `github_pat_`, `AKIA`, private-key headers → **0 hits**; no personal data, no absolute paths | met |
| Installation and usage instructions | README "Start here" routing table, maturity legend, structure, composition; `QUICKSTART.md` for six situations | met |
| Accurate project status | counts and maturity are gate-checked against the tree; execution ratio generated from `_meta/evidence.json`; limitations stated in README and `release-readiness.md` | met |
| Contribution and conduct policies | `CONTRIBUTING.md`, `.github/CODE_OF_CONDUCT.md`, `.github/SECURITY.md` exist **and** are linked (validator `check_community`) | met |
| Required validation checks | 16 gates pass locally; 106 self-test cases pass; composition 0 errors | met |

**One accuracy defect was found and fixed in this pass**, which is why this list is not "we assumed": the README asserted that CI fails when a generated file is stale, and `PROJECT-STATUS.md` described the workflow as running. Neither is true on this account (§5). Both now state the billing block and the local equivalent.

**Owner-only actions to publish** (not defects): set the repository description and topics, upload the 1280×640 social preview, then change visibility. Commands are in [`repository-configuration.md`](repository-configuration.md) §2–§5.

## 3. SHOULD FIX BEFORE MERGING

| # | Item | Evidence | Severity | Why before merge |
|---|---|---|---|---|
| 1 | **CI executes nothing.** Three consecutive runs of `validate` on PR #12: conclusion `failure`, **0 steps**, 3–4 s, no output text. The job dies before the first step. | `gh run list`, `gh api .../jobs`, `gh api .../check-runs` | **High** for trust, **none** for code | Merging to `main` puts a red check on the default branch, which is the first thing a visitor sees, and removes the only automated guard on future pushes | 
| 2 | **No branch protection, so nothing enforces the gate** | `_meta/repository-configuration.md` §3 | Medium | Once public, an unreviewed push can regress the tree; protection needs the check to exist first, which is item 1 |
| 3 | **`REQ-CHANGE-01` decision vocabulary is ambiguous** — two identical inputs produced `ACCEPTED WITH CONDITION` and `DEFERRED` | `empirical-evaluation-11.md` §4 | Low | The prompt is **not in the library** (it was never added), so nothing published depends on it. It is listed here only because the merge commit description mentions it |

**Smallest concrete action for item 1:** restore Actions billing on the account, or make the workflow honest in the meantime by restricting it to `workflow_dispatch` and stating in the README that verification is local. Both are owner decisions; the second is a two-line edit and would take the red badge off the branch.

## 4. CAN BE COMPLETED AFTER PUBLICATION

| # | Item | Evidence | Reason it can wait |
|---|---|---|---|
| 1 | Execute the remaining operational prompts | 26 of 273 (9.5%); batch 0 complete (8 of 8), batch 2 at 2+3 of 68 | Publication claims an audit, not a validation; the ratio is published and generated |
| 2 | **Any run by someone other than the author** | 0 of 241 | The only thing that would justify a stronger claim; cannot be manufactured here, and its absence is stated in README, `release-readiness.md` and `evidence-levels.md` |
| 3 | One continuous end-to-end system run | `git-operations` stages 1–5 executed, but across two sittings (`-10.md`, `-11.md`) | The letter is satisfied; the spirit is a second incident from one record |
| 4 | `REQ-CHANGE-01` vocabulary fix and ship decision | `-11.md` §4 | Not part of the published library |
| 5 | Completing batch 2 (66 prompts) and the 131 skeletons | `execution-batches.md` | A writing and execution backlog, not a publication gate |
| 6 | Making every skeleton's `Depends on:` name a real artifact | 82 links name nothing, all in skeletons | Already published as a measured number with a per-system list |

## 5. The Actions billing blocker, verified

- **What is blocked:** the workflow job. `gh run list` shows `failure` in 3–4 s; `gh api .../jobs` returns a job with an empty `steps` array and no log; `gh api repos/…/actions/permissions` is refused to the integration (403).
- **The cause, in GitHub's own words (2026-10-22, run `39763331642`):** the check-run annotation reads *"The job was not started because recent account payments have failed or your spending limit needs to be increased."* That is a billing state on the account, not a defect in the workflow: the same run also carries a runner-image notice, so the workflow was parsed and a runner was selected. Only the owner can clear it, in **Settings → Billing & plans**.
- **What it affects:** a **correctness** check (the 15-gate run on every push and PR) and, indirectly, any GitHub-native security feature that depends on Actions, such as CodeQL. It does not affect secret scanning alerts on the repository itself.
- **Safe alternative, and its limits:** `python3 scripts/check_all.py --verbose` runs the identical gate list locally; the 2026-10-22 baseline is captured verbatim in `_meta/baseline/2026-10-22-baseline.txt`, and every commit on this branch was gated with it before push. This **verifies the same checks** but does not provide the thing CI actually provides: an independent guard that cannot be skipped by the person pushing. Naming it as a replacement would be a false claim; it is a substitute for the *checks*, not for the *enforcement*.

## 6. What the published status must say

Already in the README and checked in this pass:

- 364 prompts: **228 operational, 5 draft, 131 skeleton** — with `operational` defined as structurally reviewed, not proven.
- **26 of 273 executed (9.5%)**, all by the author, none independently.
- Composition measured, not assumed: 92 of 239 stage links (38%) do not cite the upstream filename.
- CI does not run; the local gate does.

## 7. One-line decision

> **Publish as an experimental, actively-developed library whose structure is machine-checked and whose procedures are largely unproven.** Every claim above is reproducible from this checkout; none of it requires the reader to trust the author.

## 8. Landing page: which state a visitor sees

Verified 2026-10-22 against the API, and it changes the order of operations:

| | Default branch `main` | Unmerged PR branch |
|---|---|---|
| Commit | `060ffe5` — v2.21.1 | `ab695a1` — 2.22.0 work |
| Prompt files | 431 | 364 |
| README says | "124 of 364 prompts are skeleton" | 124 of 364, 235 operational, 17 executed |
| Workflows | `validate-library.yml` only, no composition gate | `validate.yml` calling `check_all.py` |
| Diff vs the other | 213 files, +7,696 / −976 | — |

Every ref becomes readable when a repository goes public, so the PR branch and PR #12 are visible too. **But a visitor lands on `main`,** so publishing now puts v2.21.1 at the front door with counts the branch has since corrected and a workflow that lacks the gate this work is about.

Two honest routes, and the choice belongs to the owner:

1. **Merge PR #12 first, then publish.** The front door is the verified state. Requires the merge authorisation that is on hold.
2. **Publish now, merge later.** Acceptable, and the repository is not dishonest — v2.21.1 was its own accurate release — but the first impression is a weaker, older tree, and the improvement arrives after launch.

**PR #12 merged on 2026-10-22** (squash, `1dc6f25`, branch deleted). It was later shown that every commit in the
repository carried an `arena-agent` co-author trailer; history was rewritten the same day and `main` now reads
`3a62a6b`. See the review log.
