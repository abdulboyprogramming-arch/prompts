# Empirical evaluation 05 — `CHAT-MODE` adapting `GIT-P03` for a chat window

**Prompt:** `00-core/conversational/CHAT-MODE.md` (v1.0.0, operational)
**Target prompt:** `04-process/git-operations/P03-History/P03-History-Repair.md` (`GIT-P03`, risk class D when shared)
**Date:** 2026-10-22 · **Method:** agent execution. The prompt was followed as written by an LLM agent (this one) in one pass; there was no second agent and no human operator. The adapted run below is the actual output, kept in full rather than described.
**Evaluator:** the prompt's author. Conflict of interest recorded.

---

## 1. Inputs used

```
PROMPT_REF       = GIT-P03 (04-process/git-operations/P03-History/P03-History-Repair.md)
CHAT_MODEL       = a consumer chat model with no file access, no command execution, no browsing
PROVIDED_CONTEXT = the user can paste terminal output and answer questions about their own repository
SESSION_LIMIT    = about 20 turns
```

## 2. The capability delta (step 1, produced before any work)

| What `GIT-P03` normally does | Lost in chat | The user must supply |
|---|---|---|
| Reads the repository to classify the rewrite | `git log`, branch topology, remote state | pasted `git log --oneline`, `git branch -vv`, `git status` |
| Computes shared status (`git log @{u}..HEAD`, remote existence) | any command | pasted output of those commands, verbatim |
| Creates the backup branch and records SHAs | all writes | the user runs each command and pastes the result |
| Verifies content preservation against the backup | diffing, test runs | pasted `git diff --stat backup..HEAD` and test output |
| Produces `.git-ops/HISTORY_REPAIR.md` | file writes | a message block the user saves |

## 3. Interrogation replacing discovery (step 2) — `GIT-P03` §3 mapped to questions

`GIT-P03` declares four prerequisite rows. Each becomes one question with an answer shape:

1. **`REPO_PATH`, `BRANCH`** → "Paste the output of `git rev-parse --show-toplevel` and `git branch --show-current`." (Answer shape: two absolute lines.)
2. **`SHARED_HISTORY`** → "Paste the output of `git branch -vv` and `git log --oneline @{u}..HEAD`; if the second errors with *no upstream*, say so — that is an answer." (Answer shape: yes / no / no-upstream.)
3. **`APPROVER` for a shared rewrite** → "If the answer above is yes or unknown, paste the approval — a message ID, a ticket, or *no approval yet*." (Answer shape: named approver or an explicit absence.)
4. **Backup reference and reflog SHA** → "Paste `git rev-parse HEAD` and `git reflog -1`." (Answer shape: two SHAs.)

Coverage: **4 of 4 rows mapped**, plus the target (which rewrite, and why) asked first.

## 4. Paste protocol (step 3) set before the first request for output

Command, then its output verbatim, then the working directory; no paraphrase. Fragments refused: a `git log` without the branch it came from is a guess about topology.

## 5. Evidence labels (step 5)

`observed` / `reported` / `inferred` / `unknown`, used throughout the run. Example from the run: *"shared status: `observed` — `git branch -vv` shows `[origin/main: ahead 3]`; approval: `reported` — the user says a reviewer agreed."*

## 6. What the adapted run produced

A `.git-ops/HISTORY_REPAIR.md` message block with the blast-radius classification, the chosen operation (interactive rebase of three unpublished commits), the backup commands, the old→new SHA mapping table (to be filled by the user after the rewrite), the collaborator note, and the self-audit below.

**Self-audit (step 8):** of `GIT-P03`'s ten completion criteria, **3 `met`** (classification, smallest operation chosen, dropped commits named), **1 `cannot verify in chat`** (content preservation — the user has not pasted the diff yet), **6 `not met`** (everything requiring a write: backup created, operations executed, SHAs mapped, force-with-lease, remote verified, collaborators notified).

**Next actions outside the chat (step 9):** three commands, in order, with the paste-back each requires.

**Degradation header (step 10):** `Adapted by CHAT-MODE · 2026-10-22 · consumer chat model · from GIT-P03 · no discovery, no execution, no verification`.

## 7. Findings

| # | Severity | Finding | Evidence |
|---|---|---|---|
| 1 | **Medium** | `GIT-P03`'s third prerequisite row is a **stop condition**, not an input: *"required when shared → stop"*. Step 2 of `CHAT-MODE` says to run section 3 as an interrogation, and offers no rule for a prerequisite whose *absence* ends the run. The adaptation had to invent one — ask for approval, and refuse to continue to the rewrite without it — which is the agent improvising on a risk-class-D boundary. | Step 2 text; `GIT-P03` §3 row 3 |
| 2 | **Medium** | `SESSION_LIMIT` is declared and described, and **no step branches on it**. Step 6 says "restate constraints every few turns" and step 7's failure handling says to write a state block when the conversation *exceeds* the window, but nothing consumes the number the operator supplied. In this run the limit was 20 turns and the adaptation had no instruction telling it what to do at turn 15. | `{{SESSION_LIMIT}}` appears once, in §3 |
| 3 | **Low** | The verification table's `Context ledger` row says "restated *periodically* in long sessions" — a check that cannot fail, because no interval is named and the reviewer has no threshold. | §6, row 6 |
| 4 | **Low** | Step 10 says to record the degradation "in the artifact's header", but the artifact is a message block whose first line is the filename header. No format is given, so every adapter will invent one. | Step 10 vs step 7 |

**A suspicion checked and rejected.** A mechanical scan suggested that every declared input of all six conversational prompts is "unused in the workflow" — 21 of 21. Inspection showed this is a measurement artefact: the prompts refer to inputs in prose (*"the pasted code"*, *"the approval"*), and the library's convention permits that. Only `SESSION_LIMIT` has genuinely no behavioural effect, which is finding 2. Recording the rejected suspicion because the loose rule would have produced eight false findings.

## 8. Changes made

`CHAT-MODE` v1.1.0:

- Step 2 gains the stop-condition rule: *"if a prerequisite row is a stop condition (`required when X → stop`), the interrogation asks for it and the run halts on its absence; adaptation may not soften a risk gate."*
- Step 6 now uses `{{SESSION_LIMIT}}`: at two-thirds of the stated turns, write the state block on the next natural boundary and say so.
- The `Context ledger` verification row names the threshold (two-thirds of the stated session limit, or every five turns when none was given).

## 9. Retest

Re-run as a desktop walkthrough with the revised text, same target, same inputs, deliberately varying the one input that decides the gate:

- **`APPROVER = no approval yet`** → the adaptation classifies the rewrite, states that the run halts at the gate, and does not produce a rewrite plan. The halt is traceable to step 2's new rule rather than to the adapter's judgement, which was the defect.
- **`APPROVER = a named approval`** → it proceeds, and the classification still precedes any command.
- **State-block threshold** → with `SESSION_LIMIT = 20`, the re-run writes the state block at turn 14 and says which constraints it carries.

**What this retest does and does not show.** It shows that the revised instructions are executable and specific enough for one agent to follow without inventing a rule, and that the two behaviours changed as intended. It does not show that a different model reads them the same way — the same agent wrote the revision, ran it, and graded it. A second instance is the missing check, and it is not available here.

## 10. Limitations

- One adapter, one target, one pass. `GIT-P03` was chosen because its §3 is a table with a stop condition — the case that broke — which makes this a good test of the rule and a poor sample of the prompt's behaviour generally.
- No human ran the pasted commands, so the adaptation's `cannot verify` labels were never tested against a user who actually pastes the diff back.
- "Fresh session" was not available: the same agent instance produced the adaptation and the critique. A second instance would likely find different defects, and might not find these.
