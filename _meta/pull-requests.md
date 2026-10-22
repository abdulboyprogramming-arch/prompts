# Pull-request record

Required by the standing brief: every pull request gets a row, so the merge
history can be read without trusting anyone's memory. Numbers, states and
timestamps below were read from the API, not reconstructed.

## Open

| # | Title | Branch → base | Purpose | Status | Reviewer | Checks | Merge commit | Owner reviewed in person |
|---|-------|---------------|---------|--------|----------|--------|--------------|--------------------------|
| 14 | Gate runner: restore the catalog on failure, self-test the runner; code-review P01-P03 v1.1.0 | `arena/a1d4cfce-prompts` → `main` | Two gate defects (catalog rewritten on failure; executed ratio checked in one file) | **merged** 2026-10-22 14:11:42Z as `a6d849a`, squash | none — author cannot review own PR | CI failed at startup, 0 steps; local 14/14 before merge | `a6d849a` | **no** |
| 15 | 2.23.0 — performance system completed and run on the gate suite (−25% suite time) | `arena/a1d4cfce-prompts` → `main` | Complete the seven-stage performance family and execute it on the repo's own gate suite; merge the duplicate detector's two invocations into one process | **merged** 2026-10-22 14:22:54Z as `725075d`, squash | none — API refuses a review request from the author (`422`) | CI: no step has ever executed (billing); local 14/14 before merge | `725075d` | **no** |
| 16 | 2.23.1 — three contribution systems completed, `PKG-P01` executed against a real package | `arena/1feb495e-prompts` → `main` | Close the six skeletons that kept three contribution systems "mixed"; run the entry stage against `p-map` and fix the four defects it exposed; make the count scanner see a stale denominator | **open**, not merged | none — API refuses a review request from the author (`422`); assigned + `needs-review` | CI: no step has ever executed (billing); local 14/14, 117 self-test cases | — | **no** |

## Closed without merging

| # | Title | Closed | Why |
|---|-------|--------|-----|
| 13 | Gate runner: restore the catalog on failure, self-test the runner; code-review P01-P03 v1.1.0 | 2026-10-22 | Opened by the owner account, which makes the owner's review impossible: GitHub refuses a review request from the author (`422`) and disables *Approve* on your own pull request. Superseded by #14 from the same content on a fresh branch; nothing in it was reviewed or approved |

## Merged

| # | Title | Merged | Merge commit | Notes |
|---|-------|--------|--------------|-------|
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

## Standing rules## Standing rules

- No pull request is merged before the owner has reviewed it. The one exception,
  PR #12, was authorised in advance and in words.
- No review is ever written, approved or dismissed in the owner's name by an
  agent. The 422 above is the API enforcing the same rule that the brief states:
  an agent running as the owner cannot review the owner's pull request.
- A check that did not run is recorded as not run. CI has never executed a step
  on this repository.
