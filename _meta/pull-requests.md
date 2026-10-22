# Pull-request record

Required by the standing brief: every pull request gets a row, so the merge
history can be read without trusting anyone's memory. Numbers, states and
timestamps below were read from the API, not reconstructed.

## Open

| # | Title | Branch → base | Purpose | Status | Reviewer | Checks | Merge commit | Owner reviewed in person |
|---|-------|---------------|---------|--------|----------|--------|--------------|--------------------------|
| 13 | Gate runner: restore the catalog on failure, self-test the runner; code-review P01-P03 v1.1.0 | `arena/5b041870-prompts` → `main` | Fix the gate runner leaving `_meta/CATALOG.md` rewritten when it failed; add the runner's missing self-test; guard the published executed-prompt ratio against drift; CR-P02/P03 v1.1.0 | **open**, not merged | review requested from `abdulboyprogramming-arch` — refused by the API (`422 Review cannot be requested from pull request author`) because the PR author is that same account; assigned instead, label `needs-review` | no CI: runs `39781017511` and `39781373937` on this branch both concluded `failure` with **0 steps** — Actions is blocked by account billing (see `publication-decision.md` §5). Local `check_all.py`: 16/16 | — | **no** — awaiting the owner |

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

## Standing rules

- No pull request is merged before the owner has reviewed it. The one exception,
  PR #12, was authorised in advance and in words.
- No review is ever written, approved or dismissed in the owner's name by an
  agent. The 422 above is the API enforcing the same rule that the brief states:
  an agent running as the owner cannot review the owner's pull request.
- A check that did not run is recorded as not run. CI has never executed a step
  on this repository.
