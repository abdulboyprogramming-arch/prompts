# Empirical Evaluation 03 — `CHAT-SELECT` Routing Run

**Date:** 2026-10-21
**Prompt under test:** `00-core/conversational/CHAT-SELECT.md` v1.0.0
**Evaluator:** the author of the prompt (conflict of interest stated below)
**Method:** six situations routed by hand against the real `TASKS.md`, then scored against the index's own assignment
**Result:** routing worked in four of six; the two failures found one defect in the prompt and one in the index

---

## Why this run is stronger than the first two

`DBG-01` and `CHAT-DEBUG` were tabletop runs against constructed fixtures: the evaluator had to judge whether the prompt's demands were reasonable, and the only ground truth was the fixture the evaluator wrote.

This run has **external ground truth**. `TASKS.md` is generated from the library, so "which task owns this prompt" is a fact in the repository, not an opinion. A routing card can therefore be checked: either it names a prompt that the index assigns to the task the situation belongs to, or it does not.

What that does **not** fix: the candidate routes were produced by the author following `CHAT-SELECT` as written, not by a live model in a live conversation. It is a tabletop with a scoring key, which is better than a tabletop without one and still weaker than two independent people running the same situations.

---

## Method

For each situation below, `CHAT-SELECT` as written was followed in mode B (no index pasted, route `inferred`), which is the harder and more common case. The questions asked are the ones the prompt permits: at most three, each discriminating. Then, in mode A, the route was checked against `TASKS.md` and the card's label was corrected from `inferred` to `observed` only when the index confirmed it.

One honesty note on sequence: the situations were written by the author, and the cross-check was run while writing up rather than days later. That is the same weakness as `CHAT-DEBUG`'s tabletop and it is stated rather than smoothed over — a route that survives a scoring key is better evidence than a route that survives a reread, and neither substitutes for two independent evaluators.

Scoring: **hit** = the named prompt is assigned by `TASKS.md` to the task the situation describes. **Miss** = a different task, or no prompt.

---

## The six situations, and what happened

### 1. "Our nightly export job stopped producing files three days ago; we noticed because a dashboard went flat."

| Step | Result |
|---|---|
| Question asked | "Did any deploy or config change land on the night it stopped?" — a discriminator, because a change points at a regression and no change points at a silent failure |
| Task chosen | *Something is broken right now* |
| Prompt named | `DBG-01` (reproduce locally, then bisect by time) |
| Falsifier written | "If the job's own log shows it ran and wrote nothing, this is `JOBS-01`, not a defect in the export code" |
| **Verdict** | **Hit on the task, miss on the prompt** — `TASKS.md` assigns `JOBS-01` to *I am running the work*, so the falsifier named a prompt the index files elsewhere |

This is the most useful case in the run: the routing was **right about the situation and wrong about the library's own shape**. A chat model in mode B would have produced exactly this, because "a job that stops running" is a job problem in the vocabulary of the index, while a user experiences it as breakage.

### 2. "I joined a team last week. The service is 40,000 lines, has no README, and I have to add a feature by Friday."

| Step | Result |
|---|---|
| Questions asked | One: "Do you need to understand the codebase, or only enough of it to land the feature?" |
| Task chosen | *I have to work in a codebase I have never seen* |
| Prompt named | `ONBOARD-01`, with `05-scenarios/quick-fixes/` named as the conditional alternative |
| Falsifier written | "If the feature touches a layer nobody documents, the route is `AUDIT-P01`, which inventories before the work starts" |
| **Verdict** | **Hit** — both prompts sit in the chosen task |

### 3. "We have to move fourteen services off one cloud account in six weeks."

| Step | Result |
|---|---|
| Questions asked | "Is a cutover date already committed to a customer?" |
| Task chosen | *I am shipping a release* |
| Prompt named | `HOSTMIG-01` |
| Falsifier written | "If any service holds customer data that cannot move, the route is `RESIDENCY-01` and the plan stops being a deployment problem" |
| **Verdict** | **Hit** — `HOSTMIG-01` is assigned to *I am shipping a release* |

### 4. "I pasted a function into ChatGPT, it said the code looked fine, and production throws a TypeError."

| Step | Result |
|---|---|
| Questions asked | "Can you paste the error text and the function with its imports?" — the paste protocol, not a routing question |
| Task chosen | *I only have a chat window* |
| Prompt named | `CHAT-DEBUG` |
| Falsifier written | "If the traceback's deepest frame is not in the code you pasted, the problem is in the caller and the route becomes `CHAT-MODE` with the file that calls it" |
| **Verdict** | **Hit** |

### 5. "A 300-million-row table needs a new column and a backfill. A plain `ALTER TABLE` locks writes for six minutes."

| Step | Result |
|---|---|
| Questions asked | "Can the backfill run while the old code is still writing rows?" |
| Task chosen | *I need to move or delete data* |
| Prompt named | `DB-P02` (migration design) |
| Falsifier written | "If reads must keep working on the old shape during the backfill, the plan is `DB-P02` then `DB-P03` preflight — not a one-shot migration" |
| **Verdict** | **Hit**, and the falsifier is the reason: the first instinct was `DB-P01` (schema truth), which the index also assigns to the same task but which does not design a migration |

### 6. "Our enterprise customer's security team sent a 60-page questionnaire and wants evidence for SOC 2 by Friday."

| Step | Result |
|---|---|
| Questions asked | "Is the ask evidence of controls you run, or a map of which controls you would need?" |
| Task chosen | *I need to answer someone outside engineering* |
| Prompt named | `GOV-P01` (control map) |
| Falsifier written | "If the questionnaire names SOC 2 controls specifically and the work is mapping them, `STD-01` is the route; `GOV-P01` is for controls you already operate" |
| **Verdict** | **Miss** — `GOV-P01` and `STD-01` are both in the task, so the task was right, but the card named the wrong one first for the situation described |

The miss is real and it is the kind a chat model will make: **two prompts in one task answer nearly the same sentence**, and the difference ("controls you operate" versus "a standard you must map to") lives in the prompt bodies, which mode B cannot read.

---

## Defects found and fixed

| # | Defect | Fix in `CHAT-SELECT` v1.1.0 |
|---|---|---|
| 1 | Nothing said what to do when the situation's symptom and the index's task disagree — case 1 routed to the right task for the user and the wrong one for the library | New rule: **route by the sentence the user wrote, then name the index's task for the same prompt**. If they differ, say both, and say which one to run first |
| 2 | Nothing warned that two prompts in one task can answer nearly the same sentence (case 6) | New rule: when two prompts in the chosen task both fit, the falsifier must separate *them*, not just the task |

Defect 2 is the more interesting one. The prompt already required a falsifier, and every card in this run had one — but four of the six falsifiers separated **tasks**, which was not the risk. The risk was within a task.

## Defect found in the index, not the prompt

Case 1 exposed a filing error rather than a routing error: `JOBS-01` (background jobs) sat only under *I am running the work*, although a job that fires twice or never is the most common form of "something is broken right now". The home was added to that task, and `TASKS.md` regenerated. The index's coverage check could not have caught this — every prompt had a home — which is why a routing run is a different instrument from a coverage check.

## What the run cost

Six situations, at most one discriminating question each, and one cross-check per card against the generated index. The work is small — under an hour — and the yield came from the scoring key, not from re-reading the prompt: both prompt defects and the index defect are invisible to a careful read of `CHAT-SELECT`, which reads as complete until a card is scored against something outside itself.

## Files changed because of this run

| File | Change |
|---|---|
| `00-core/conversational/CHAT-SELECT.md` | v1.1.0: classify the sentence rather than the noun, with the symptom/heading disagreement stated in the card; the falsifier must separate two prompts within a task; new verification row and completion criteria; two new failure-handling cases |
| `scripts/generate_task_index.py` | `05-scenarios/background-jobs` added as a second home of *Something is broken right now*; the start-here note now names `JOBS-01` for scheduled work that stops without an exception; a comment records that overlapping homes are deliberate and must be true of both descriptions |
| `TASKS.md` | regenerated — `JOBS-01` now appears under both tasks |
| `scripts/test_task_index.py` | two cases pinning multi-home routing (17/17) |
| `05-scenarios/background-jobs/BACKGROUND-JOBS.md` | an explicit `Gallery` line, because both index rows were rendering the clipped fragment "A per-job safety assessment (idempotent?" |

## What this does not prove

- **That a model follows the questions.** The questions here were chosen by the author, who knew the answer each situation needed.
- **That mode B routes well in unfamiliar territory.** All six situations were written by someone who knows the library's vocabulary, even though none of them uses it.
- **That six situations make a benchmark.** They are a smoke test of the mechanism. `GEN-P02` defines what a real one would need.
