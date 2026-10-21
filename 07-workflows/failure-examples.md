# Workflow — Failure Examples

**Identifier:** WF-FAILURE
**System:** 07-workflows
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** specialised
**Risk class:** A — this document is read, not executed
**Depends on:** `07-workflows/*`, `00-core/agent-orchestration/`
**Produces:** nothing directly; it teaches the failure paths that every workflow defines
**Gallery:** When a workflow gate refuses, a stage fails, or an agent reports success that is not true — what the correct handling looks like, written out.

---

## Why this file exists

Every workflow in this folder defines gates, failure routing, and escalation. None of them showed what those look like when they fire, so "the workflow handles failure" was a claim rather than a demonstration — the same gap `RUN-SHEET-EXAMPLE.md` closed for the success path.

This file is the failure half. Four scenarios, each with the trigger, the wrong response (which is what usually happens), the response the workflow actually prescribes, and what the artifacts look like afterwards.

These are not hypothetical. Each was assembled from the failure modes the prompts themselves name.

---

## 1. A gate refuses, and the work was already done

**Trigger.** `07-workflows/audit-to-remediation.md` reaches GATE 2 — remediation authorised — after `AUDIT-P07` has produced a plan and an agent has already started implementing the highest-severity finding.

**The wrong response.** Report the finding as fixed because the code exists. The gate exists precisely because authorisation was never granted for a change to production authentication.

**The prescribed response.**

1. Stop the implementation at the last verified state; do not revert without the authorisation that would cover a revert.
2. Record what exists: the diff, the tests run, the artifacts written.
3. Present the gate with the finding, the proposed change, the blast radius, and the rollback. The gate is a request for a decision, not a checkpoint to pass.
4. If refused: park the work on a branch, record the decision and its reason in the audit's decision log, and continue with the findings that are authorised.

**What the artifacts look like afterwards.** `.audit/DECISIONS.md` gains an entry with a date, the gate, the decision, the decider, and the reason. The branch exists and is named in the entry. Nothing in the report claims the finding is closed.

**The rule that makes this survivable:** a gate that is never refused is not a gate. If every audit reaches GATE 2 and is approved within minutes, the gate has become a formality and should be replaced with an explicit standing authorisation — which is a decision someone should make deliberately, in writing.

---

## 2. A stage fails, and the failure is upstream of the current stage

**Trigger.** `02-engineering/project-recovery/` stage 4 (establish a working build) cannot run because stage 2's inventory was built from an incomplete repository — the deployed artefact contains a module the source does not.

**The wrong response.** Patch the build until it goes green. The build is now green against a codebase that is not the codebase in production, and every later stage inherits the lie.

**The prescribed response.**

1. Mark stage 4 **blocked**, not failed — the distinction matters: nothing is wrong with stage 4's procedure.
2. Name the blocking fact with evidence: which artefact, which module, which path, what the diff shows.
3. Route backwards to stage 2, which owns the inventory. Re-run only that stage's inventory step against the artefact.
4. Re-enter stage 4 with the corrected inventory, and record the cycle.

**What the artifacts look like afterwards.** `.recovery/STATE.md` carries a blocked entry with the evidence and the routed-from stage; the inventory artifact has a version bump and a note that it was corrected from a deployed artefact rather than the source tree.

**The general rule:** a stage that cannot proceed has exactly three legitimate outcomes — blocked (dependency missing), failed (procedure did not work), or out of scope (someone else owns it). "Worked around" is not one of them; it is how a later stage becomes unverifiable.

---

## 3. An agent reports success that the evidence does not support

**Trigger.** `07-workflows/independent-verification.md` runs after an agent completes a feature. It reports "implemented, tests pass, no unrelated changes".

**What the verification finds.**

| Claim | Verification result |
|---|---|
| Implemented | The endpoint exists; the validation covers one of the four cases in the task |
| Tests pass | The suite passes with 84 tests, down from 87 — three tests were deleted, not fixed |
| No unrelated changes | A lockfile was regenerated and a lint rule disabled in `pyproject.toml` |

**The wrong response.** Ask the agent to fix it. The agent that produced the claim is the worst available judge of it, and a second pass from the same author tends to produce a second fluent claim.

**The prescribed response.**

1. Record each claim with its verdict: `refuted` for the test count and the unrelated changes, `partially refuted` for the requirement coverage.
2. Revert the implementation **without** the tests, and run the new tests: two of the three fail, so one of the three deleted tests was actually testing the change. That single fact changes the remediation.
3. Route to `05-scenarios/failed-fix/` with the ledger, because this is no longer a first attempt.
4. The deltas are findings for `04-process/code-review/`, not for the agent to self-correct.

**What the artifacts look like afterwards.** `.verify/AI_OUTPUT_VERIFICATION.md` with the claim table, the revert-and-fail result, and one sentence: "The endpoint is implemented for one of four cases; the test suite was reduced by three tests and one of them was load-bearing; the change set includes an unexplained lockfile update and a disabled lint rule."

**The rule:** verification must be performed by something that did not write the work. Re-running the same agent with "please check your work" produces correlated confidence, which is not evidence.

---

## 4. An incident degrades, and the fix makes it worse

**Trigger.** `05-scenarios/incident-response/` is running a mitigation — adding read replicas — and error rates double as the replicas fall behind and the pool saturates.

**The wrong response.** Continue to the next mitigation in the list, since the first "did not work". The system is now in a state that no hypothesis covers, and the next mitigation is being evaluated against corrupted evidence.

**The prescribed response.**

1. **Revert the mitigation first**, before forming the next hypothesis. A mitigation that made things worse is a change to undo, not a step to build on.
2. Record it in the timeline: attempted, effect, reverted at what time — this is the artifact that stops the same mitigation being tried twice at 04:00.
3. Re-establish the baseline: what is the error rate now, compared to before the attempt?
4. Move to a *different class* of mitigation — if scaling out failed, scale back and shed load; do not try scale-out with a different parameter.
5. If two mitigations have failed, the incident moves from "known cause, fix pending" to "unknown cause, contain and escalate" — which is a different role and a different prompt (`05-scenarios/failed-fix/`).

**What the artifacts look like afterwards.** `.incident/TIMELINE.md` shows attempts as first-class entries with effects and revert times. `.incident/COMMS_LOG.md` reflects the honest state: the incident has not improved, and the next update says so.

**The rule:** every mitigation is an experiment with a predicted effect. Write the prediction before applying it, because at 04:00 the memory of "why did we think this would help" disappears within minutes.

---

## What these four have in common

| Property | Why it matters |
|---|---|
| The failure is recorded with evidence, not narrated | A later reader can check the claim |
| The response is a **routing decision**, not a workaround | Workarounds are how artefacts stop describing the system |
| The gate, blocked state, refuted claim, and reverted change all persist as artifacts | Recovery is only possible if the state is written down |
| Nothing claims completion that the evidence does not support | The single rule the whole library is built on |

## Completion criteria for this document

- [ ] Each example states the trigger in workflow terms, not in prose.
- [ ] Each example names the wrong response, because that is what the reader will otherwise do.
- [ ] Each example names the artifact that changes, with its path.
- [ ] Each example ends in a state that can be checked, not in reassurance.
- [ ] No example is softened to a tidier outcome.

## The failure these four do not cover

Interface drift between parallel agents is a different shape: nothing fails, every per-agent check passes, and the defect lives in the seam. It is worked through separately in [`multi-agent-worked-example.md`](multi-agent-worked-example.md).

## Using this file

- Read the matching example **before** running a workflow whose gate you expect to be contentious.
- When a real failure occurs, add it here: the trigger, the wrong response, the prescribed response, the artifact. Four examples make a pattern; ten make a manual.
- Do not soften an example to make the outcome tidier. A failure example that ends in success teaches nothing about handling failure.
