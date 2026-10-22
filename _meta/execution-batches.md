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

**Kind C is the one that counts and the only one that cannot be manufactured here.** Everything below is A and B, run by the author, and recorded as such. The few prompts that have been executed are data points, not a tested library; this file makes the remaining work queueable rather than vague.

---

## 2. The batches

Batches are ordered by *what a run costs to set up*, not by folder. Each batch below was measured from the tree: the counts are prompts, then how many of those are `operational`.

| Batch | What it is | Prompts / operational | Target | Run status |
|---|---|---:|---|---|
| **B0** | The eight identified prompts in `00-core/` — six conversational (`CHAT-MODE`, `CHAT-DEBUG`, `CHAT-DESIGN`, `CHAT-HANDOFF`, `CHAT-REVIEW`, `CHAT-SELECT`) plus `GEN-P01` and `GEN-P02` under `prompt-engineering/` | 8 / 8 | a paste, a pasted file, a decision about which prompt to use, or a prompt to forge and test | **8 of 8 executed** (2026-10-22). See §5 — the earlier version of this table said 8 conversational prompts and named `CHAT-ASK`, which does not exist |
| **B1** | Codebase work: `02-engineering/` | 82 / 38 | this repository for roughly a third of them — the audit, review, and repair prompts, whose subject is a source tree; an application fixture for the rest, which expect routes, schema, or services this repository does not have | 0 recorded |
| **B2** | Process work: `04-process/` | 92 / 68 | this repository's own history and releases, or a purpose-built fixture when the prompt needs an operation in progress | **5 of 68 recorded** — all five `git-operations` stages: P01–P02 as a unit in `empirical-evaluation-10.md`, P03–P05 in `-11.md` |
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

## 5. B0 in detail — complete, and a membership correction

**This section was wrong when it was written, and the error is worth keeping.** It said B0 held eight *conversational* prompts, listed `CHAT-ASK` as unrun, and concluded that four runs would finish the batch. Verification against the tree on 2026-10-22 found six conversational prompts — `CHAT-ASK` has never existed — and a B0 total of eight only if `GEN-P01` and `GEN-P02` are included, which is what the validator's count of `00-core/` (8 identified prompts) always said. The plan had invented a prompt to reach a number it already had.

| Prompt | Version after this pass | Run | Record |
|---|---|---|---|
| `CHAT-MODE` | 1.1.0 | adapted `GIT-P03` for a chat window; 4 of 4 prerequisite rows mapped | `empirical-evaluation-05.md` |
| `CHAT-DEBUG` | 1.1.0 | recorded 2026-10-20 | `-02.md` |
| `CHAT-SELECT` | 1.1.0 | recorded 2026-10-21 | `-03.md` |
| `CHAT-REVIEW` | 1.1.0 | reviewed this repository's own composition gate; found two metric defects | `-04.md` |
| `CHAT-DESIGN` | 1.1.0 | ADR on splitting the composition gate from the validator | `-06.md` |
| `CHAT-HANDOFF` | 1.1.0 | 48-line packet, then a five-question reconstruction with 5/5 answerable | `-07.md` |
| `GEN-P01` | 1.1.0 | forged `REQ-CHANGE-01` for a named coverage gap; self-scored 83/100 | `-08.md` |
| `GEN-P02` | 1.1.0 | ran `REQ-CHANGE-01` against a real git fixture, three cases, shell assertions | `-09.md` |

**What B0 completion does and does not mean.** All eight have been executed and all eight changed as a result: 6 of 8 gained a v1.1.0, and both prompt-engineering prompts did. That is the batch's real output — not coverage, but defects. **None of the eight has been run by anyone other than the author**, and two of the eight (`CHAT-MODE`, `CHAT-HANDOFF`) were graded on artifacts the same agent wrote and then read back. The batch is complete in the column that counts executions and empty in the column that would make it evidence a stranger can rely on.

The next executable task in this batch is a re-run by a second person, and there is no way to manufacture that here.

## 6. Honest status

- **24 of 228 operational prompts executed (10.2%).** Stated in [`evidence-levels.md`](evidence-levels.md), generated from the registry, and checked in CI so it cannot drift.
- **0 runs by a second person**, which is the only kind that tests usefulness.
- **Batch 0 complete (8 of 8); batch 2 at 5 of 68**, all five `git-operations` stages. The two `git-operations` runs are the first execution of two stages of one system as a unit, which is a weaker test than the system run criterion 11 asks for and is recorded as partial.
- **B2 is the cheapest ten runs** and the target already exists in this checkout.
- **B7 (131 skeletons) is not a testing backlog.** It is a writing backlog; testing an outline measures the outline.
- **This file is a plan, not evidence.** Nothing in it raises the ratio. The runs it describes are the thing that would.
