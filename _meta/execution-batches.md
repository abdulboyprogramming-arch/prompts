# Execution Batches — how to run the prompts end to end, and what eight of them proved

**Purpose:** part 5 of the 2026-10-22 brief was *"begin end-to-end testing of each individual prompt, in batches if possible — self-verifying alignment and functionality for anything I can actually run, including agentic-style prompts if feasible."*

This file is the plan and the ledger. It says which prompts can be executed **without a second person**, in what order, what a pass means, and what has already been run. It exists so that the ratio in [`evidence-levels.md`](evidence-levels.md) stops being a number nobody acts on.

---

## 1. Why 228 prompts cannot be tested the same way

A prompt is a procedure for a situation. Whether it works is a fact about a run, and most of these situations need conditions this repository cannot create: a production incident, a cryptographically signed release, a second engineer who has never seen the prompt, a team that disagrees.

Three kinds of test are available, and only the first can be done alone:

| Kind | What it proves | Cost | Applies to |
|---|---|---|---|
| **A — Executable against this repository** | The procedure completes on real input, its verification table can be filled in, and its artifacts come out usable | one sitting each | prompts whose target is a source tree, a diff, a plan, or a chat paste |
| **B — Adversarial fixture** | The prompt's failure handling fires on the input it was written for | a constructed fixture | anything with a decision rule or a refusal |
| **C — Independent run** | The prompt works for a reader who is not its author | a second person | everything; this is the only kind that tests *usefulness* |

**Kind C is the one that counts and the only one that cannot be manufactured here.** Everything below is A and B, run by the author, and recorded as such. A library where 4 of 228 prompts have been executed is a library with 4 data points, not a tested library; this file makes the remaining work queueable rather than vague.

---

## 2. The batches

Batches are ordered by *what a run costs to set up*, not by folder. Each batch below was measured from the tree: the counts are prompts, then how many of those are `operational`.

| Batch | What it is | Prompts / operational | Target | Run status |
|---|---|---:|---|---|
| **B0** | Conversational prompts: `00-core/conversational/` | 8 / 8 | a paste, a pasted file, or a decision about which prompt to use | **4 of 8 recorded** — `CHAT-DEBUG`, `CHAT-SELECT`, `CHAT-REVIEW`, plus `CHAT-MODE`'s capability delta used implicitly by all three. `CHAT-ASK`, `CHAT-DESIGN`, `CHAT-HANDOFF`, and `CHAT-MODE` standalone remain |
| **B1** | Codebase work: `02-engineering/` | 82 / 38 | this repository for roughly a third of them — the audit, review, and repair prompts, whose subject is a source tree; an application fixture for the rest, which expect routes, schema, or services this repository does not have | 0 recorded |
| **B2** | Process work: `04-process/` | 92 / 68 | this repository's own history and releases — a real diff, a real `CHANGELOG.md`, a real tag | 0 recorded. Needs a deliberately messy branch, or a historic one restored from `git log` |
| **B3** | Incident and scenario rehearsal: `05-scenarios/` | 42 / 37 | a labelled staging directory and a declared fake incident, never the real repository | **1 recorded** — `DBG-01` |
| **B4** | Contribution systems: `01-contribution/` | 48 / 34 | a *different* repository — a library, a web app, or a protocol, since the prompts are about contributing to someone else's | 0 recorded. The target is the cost here: each system needs a plausible upstream repository |
| **B5** | Domain work: `03-domains/` | 75 / 35 | synthetic fixtures, one per domain | 0 recorded. The most expensive per prompt and the least valuable to run by the author, because the domain content is what a domain reader would test |
| **B6** | Orchestrations and interactive skeletons: `07-workflows/` and `06-interactive/` | 17 / 8 | an agent run with the prompt as its system message; a produced packet read cold by a second instance | 0 recorded. `07-workflows/` holds 5 drafts; `06-interactive/` is 4 skeletons and is not runnable |
| **B7** | The 131 skeletons | 131 / 0 | — | **not runnable by definition.** A skeleton is an outline; running it would test the outline's plausibility, not the procedure |

**B2 is where the next ten runs should come from.** Code review, git operations, and release engineering all take this repository as their target, which already has commits to compare, a changelog to edit, tags to inspect, and a test suite to gate on. A failure there is a defect in the prompt rather than in a fixture the author also wrote — which is the difference between B1 and B4.

**B2 is where the next ten runs should come from.** It is the only batch where the target, the tests, the artifact destinations, and the acceptance criteria all already exist, and where a failure would be a defect in the prompt rather than in the fixture.

---

## 3. What a run has to leave behind

A run counts only if it leaves a record that someone else can check. The bar is deliberately low and non-negotiable:

1. **The prompt, version, date, and evaluator**, including whether the evaluator wrote the prompt.
2. **The target**, specific enough to be reconstructed: a commit, a file, a fixture, or a paste kept in the record.
3. **What was produced** — the artifact the prompt says it produces, quoted or linked, not summarised as "it worked".
4. **The verification table, filled in.** Every prompt has one; a run that cannot fill a row records why, and that row is a finding.
5. **Findings**, classified: prompt defect (and the fix), target defect, or unusable instruction.
6. **What the run does not show**, in one sentence, always.

`_meta/empirical-evaluation-0*.md` are the four models of this, and `_meta/evidence.json` is the registry that `scripts/evidence_report.py` validates. Adding a run is: write the record, add the entry, run `python3 scripts/evidence_report.py --write`. The generated page states the ratio, so the claim cannot drift from the registry.

---

## 4. What eight prompts have produced so far

Four runs, eight prompts exercised (some inside other runs), across 228 operational prompts:

| Prompt | Kind | What it produced | Prompt defect found |
|---|---|---|---|
| `DBG-01` | A | Three weaknesses in a debugging protocol, against a fixture with a hidden mutable default | yes, fixed in v1.2.0 |
| `CHAT-DEBUG` | B | Three defects: no instruction to find other holders of a resource, a ledger that cannot record findings outside the paste, no rule for contradictions between the user's account and the evidence | yes, fixed in v1.1.0 |
| `CHAT-SELECT` | B | 4 of 6 routings correct against `TASKS.md` as ground truth, plus one defect in the index itself | yes, two, fixed |
| `CHAT-REVIEW` | A | Two defects in the repository's own composition metric, which had overstated the integration claim by twelve points | yes, three, fixed in v1.1.0 |

**The pattern is the result.** Four runs, four prompts changed. Every single execution produced at least one real defect in the prompt that the structural review had passed — which is the argument for executing more of them, stated as evidence rather than as an opinion.

**The pattern has a limit that must be stated too.** All four were run by the prompt's author, three were tabletop or designed by the same person, and none was run by a reader who had to understand the prompt from the text alone. The defects found this way are the ones an author can find by trying harder. The ones that matter — instructions a reader misreads, prerequisites a reader does not have, artifacts a reader cannot produce — need kind C, and no amount of author labour substitutes for it.

---

## 5. B0 in detail, because it can be finished

The eight conversational prompts share one target: a chat window with a paste. Six of the eight can be run in a single sitting each, and three already have.

| Prompt | State | What remains |
|---|---|---|
| `CHAT-MODE` | used implicitly by three runs, never run standalone | one run where the capability delta is stated for a task whose answer depends on it |
| `CHAT-DEBUG` | executed, v1.1.0 | re-run after the v1.1.0 changes to confirm the three fixes did not add a fourth problem |
| `CHAT-SELECT` | executed, v1.1.0 | re-run against the current `TASKS.md`, which changed after the run |
| `CHAT-REVIEW` | executed, v1.1.0 | re-run on a file the author did not write — the obvious first candidate is a third-party script in the same language |
| `CHAT-DESIGN` | never run | a design discussion with a stated deadline and two candidate approaches |
| `CHAT-ASK` | never run | a question whose answer requires two clarifying turns, one of which the user does not want to give |
| `CHAT-HANDOFF` | never run, new in 2.22.0 | a packet produced at the end of a long session, then read cold by a second model instance with no other context |
| `CHAT-SELECT` and `CHAT-REVIEW` | — | the only pair that can be run back to back on one artifact: choose the prompt, then run the one chosen |

Finishing B0 is four runs. It would move the ratio to 8 of 228 and, more usefully, give the first evidence about prompts read cold, since `CHAT-HANDOFF` is designed to be consumed by something that was not present when it was written.

---

## 6. Honest status

- **4 of 228 operational prompts executed (1.8%).** Stated in [`evidence-levels.md`](evidence-levels.md), generated from the registry, and checked in CI so it cannot drift.
- **0 runs by a second person**, which is the only kind that tests usefulness.
- **B2 is the cheapest ten runs** and the target already exists in this checkout.
- **B7 (131 skeletons) is not a testing backlog.** It is a writing backlog; testing an outline measures the outline.
- **This file is a plan, not evidence.** Nothing in it raises the ratio. The runs it describes are the thing that would.
