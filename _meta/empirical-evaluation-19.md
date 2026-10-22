# Empirical Evaluation 19 — the last three skeletons in `06-interactive`, and a router that guessed

**Date:** 2026-10-22
**Prompts:** `WIZ-P01` (System Selector) v0.1.0 → v1.1.0; `INT-P02` (Contribution Intake) v0.1.0 → v1.1.0;
`INT-P03` (Greenfield Intake) v0.1.0 → v1.1.0
**System:** `06-interactive` — completed this cycle
**Evaluator:** the author of the prompts (conflict of interest recorded)
**Method:** desk runs against three committed fixtures whose answers the prompts did not write.

---

## 1. Why these three, and why now

`INT-P01` was rebuilt last cycle after a run in which it scored 0 of 5. The other three prompts in the
system were left as skeletons, and the system README said so explicitly: *"the fix was demonstrated on
one prompt and has to be repeated on the others before the system can be called operational."*

This cycle repeats it — and tests the one prompt in the library whose correctness can be graded against
**ground truth the repository generates for itself**. `WIZ-P01` routes requests; `TASKS.md` is the
generated index of 21 situations with a *Start here* line naming the destination for each. A router can
therefore be scored against the repository's own routing, not against its author's opinion.

## 2. `WIZ-P01` — the router, measured

### The fixture

[`_meta/fixtures/routing-scenario/REQUESTS.md`](fixtures/routing-scenario/REQUESTS.md): 14 requests
written as a requester would type them, each mapped to a `TASKS.md` section and to the destination that
section's *Start here* line names. Every destination path was verified to exist. The requests were
chosen to include six sections whose destination systems postdate the selector, three sections where
two destinations are legitimate and a condition decides, and one chat-only request.

**The fixture's own first draft was wrong twice** — it named `project-recovery` where the index says
`ONBOARD-01`, and `ai-output-verification` where the chat section names only `CHAT-*`. Both were caught
by checking against the index. That is the finding, not an anecdote: an author's memory of this
repository's routing is unreliable at 364 prompts, which is precisely why the selector must read.

### Run 1 — v0.1.0: 5 of 14

v0.1.0 asks for a one-sentence goal, classifies it into seven categories, asks two or three clarifying
questions, and recommends a system **with its path**. The seven categories are: contribute / understand
or audit / build from scratch / refactor or migrate / improve quality / handle a situational need /
design a feature or strategy.

| # | Request | Routed to | Verdict |
|---|---|---|---|
| 1 | service 500ing now | `05-scenarios/incident-response/` | pass |
| 2 | inherited a 200k-line repo | `02-engineering/codebase-audit/` | **fail** — index says `ONBOARD-01` |
| 3 | rename a config key across twelve services | `02-engineering/refactoring/` | pass |
| 4 | build a notification service from scratch | `02-engineering/from-scratch/` | pass |
| 5 | is this codebase healthy | `02-engineering/codebase-audit/` | pass |
| 6 | release checklist for Friday | no category exists → `05-scenarios/quick-fixes/` | **fail** |
| 7 | 400 tests I do not believe | `04-process/testing-qa/` | pass |
| 8 | a 300-line diff pasted into Slack | `04-process/code-review/` | **fail** — no repository access |
| 9 | taking over on-call next week | `04-process/handover/` | **fail** — rota at speed is `on-call-handover` |
| 10 | the AWS bill doubled | `02-engineering/performance/` | **fail** — the invoice is the symptom, not latency |
| 11 | legal deletion with proof | `02-engineering/security-hardening/` | **fail** |
| 12 | agent that can open PRs, guardrails first | `02-engineering/feature-design-suggestion/` | **fail** — that prompt is a skeleton |
| 13 | app stores in six weeks, auth flow | `02-engineering/from-scratch/` | **fail** — the stack decides the system |
| 14 | chat only, is this AI-written function safe | `05-scenarios/debugging/` | **fail** — capability not detected |

**5 of 14.** Three failure classes, none of them vocabulary:

1. **Three requests had no category at all** (6, 11, 12). A category list written before release
   engineering, privacy requests and AI-agentic systems existed cannot route to them.
2. **Three requests have two legitimate destinations separated by a condition** (8, 9, 10) and v0.1.0
   has no condition — it has a category.
3. **Four destinations postdate the prompt** (2, 11, 12, 13), so the named path is either wrong or
   points at a skeleton while an operational system exists elsewhere.

There is a fourth, structural defect that the score does not capture: v0.1.0's Role line reads *"You are
a guide to the Supercharged Prompt Archive"*. That name appears in exactly two files in this repository —
this prompt and `00-core/system-prompts/BASE-ENGINEERING-AGENT.md` — and in no README, index, or release.
The router is addressed at an ecosystem name the repository stopped using, which is a smaller version of
the same failure: it describes a library it cannot see.

### Run 2 — v1.1.0: 14 of 14

Five changes, each traceable to a failure class above:

| Fixes | Change |
|---|---|
| all | **§4.1: read `TASKS.md` before classifying.** The index is the map; the router's memory is not |
| 8, 9, 10 | **§4.2 and a condition table**: capability first, then five named two-destination sections with the condition that decides |
| 6, 11, 12 | **§4.4: verify the path exists** — a destination that cannot be opened is not a destination |
| 13 | **§5 "Do not start here"**: name the plausible-but-wrong destination and why |
| 2, 12 | **§7: do not invent a system; do not route to a skeleton while an operational system covers it** |

Verified on the same fourteen: every destination matches the index, every path resolves, capability is
stated for the two chat requests, and the five two-destination sections carry their condition rather
than an "either".

## 3. `INT-P02` — contribution intake, against five planted traps

Fixture: [`_meta/fixtures/contribution-scenario/UPSTREAM.md`](fixtures/contribution-scenario/UPSTREAM.md),
a synthetic upstream (`acme/ledgerkit`, GPL-3.0) with the rules written out and five traps planted — no
`accepted` issue, a refused runtime dependency, a sign-off the contributor may not be entitled to give,
an `npm test` that is actually `make check`, and a copyleft licence.

| Trap | v0.1.0 | v1.1.0 |
|---|---|---|
| 1 · no `accepted` issue | missed — the prompt has no step that reads the upstream's PR policy | found — §4.1 reads `CONTRIBUTING.md` first; §4.3 checks the task against what the project solicits |
| 2 · adding a runtime dependency | missed | found — recorded as the project's explicit refusal, with the plugins repository named as the destination |
| 3 · employer sign-off | missed — "GitHub username or preferred identity (if relevant)" invites the wrong answer | found — §4.5 treats sign-off authority as a legal question, and "unknown" is an accepted answer |
| 4 · `npm test` | accepted the user's command as context | found — the test command is sourced from `CONTRIBUTING.md`; §5's fact table has no unsourced row |
| 5 · GPL-3.0 | not considered | found — licence position recorded as unknown for the contributor's case, to be confirmed with their employer |

**v0.1.0 scored 0 of 5; v1.1.0 scored 5 of 5.** The structural reason is the same one that broke
`INT-P01`: v0.1.0 collects the contributor's *intent* and never reads the upstream's *rules*, so every
question it asks can be answered wrongly by the person asking it.

## 4. `INT-P03` — greenfield intake, against a proposal in search of a problem

Fixture: [`_meta/fixtures/greenfield-scenario/REQUEST.md`](fixtures/greenfield-scenario/REQUEST.md) — an
"internal event platform" request that opens with Kafka, contains one genuine fixed constraint (a 30-day
deletion rule with audit trail), three preferences presented in the same tone, no deadline, a scope for
"every team" and a team of 1.5 people.

| # | Requirement | v0.1.0 | v1.1.0 |
|---|---|---|---|
| 1 | problem separated from the Kafka proposal | **fail** — §1 "Project identity" records the proposal as the purpose | pass |
| 2 | "every team" challenged as scope | **fail** | pass — first user and first outcome named, platform demoted to a non-goal |
| 3 | fixed constraint vs preferences | **fail** — one flat list | pass — §4 classifies and sources each |
| 4 | deletion rule as architecture-shaping | **fail** | pass |
| 5 | a non-goal, with where the request goes | **fail** | pass — the analytics stream processor, routed to `03-domains/data-engineering/` |
| 6 | a failure mode | **fail** | pass — an unowned platform in a two-person team |
| 7 | no invented deadline | pass — it did not invent one | pass |
| 8 | no stage count from urgency | **fail** — "start coding next week" becomes the plan | pass — lifecycle sets the stages |

**v0.1.0: 1 of 8. v1.1.0: 8 of 8.** The single pass at v0.1.0 is the absence of a mistake rather than a
decision; the prompt never had a place to put a deadline, so it never invented one.

## 5. What this cycle does not show

- **Desk runs by one executor.** Every score is the author following the procedure as written. For
  `WIZ-P01` the ground truth is generated by the repository, which is stronger than for the other two;
  for `INT-P02`/`INT-P03` the fixture's grading criteria were also written by the author, so they test
  whether the prompt can find what the fixture planted, not whether it asks the right questions in life.
- **Routing accuracy is not usefulness.** 14 of 14 on a fixture built from the index means the router
  reads the index. It does not mean a user with a confused request gets a good afternoon.
- **No composition test.** Nothing here shows that a brief produced by `INT-P02` improves what
  `01-contribution/` produces. The library still has no end-to-end composition harness.
- **`INT-P01` was not re-run.** Its last result stands (`empirical-evaluation-18.md`).

## 6. Status

| Prompt | Before | After |
|---|---|---|
| `WIZ-P01` | v0.1.0, skeleton, `TESTED — FAIL` (5 of 14) | **v1.1.0, operational, `TESTED — PASS`** (14 of 14) |
| `INT-P02` | v0.1.0, skeleton, `TESTED — FAIL` (0 of 5) | **v1.1.0, operational, `TESTED — PASS`** (5 of 5) |
| `INT-P03` | v0.1.0, skeleton, `TESTED — FAIL` (1 of 8) | **v1.1.0, operational, `TESTED — PASS`** (8 of 8) |

`06-interactive` is now four operational prompts and no skeletons — the smallest system in the library
and the first one completed by execution rather than by review.
