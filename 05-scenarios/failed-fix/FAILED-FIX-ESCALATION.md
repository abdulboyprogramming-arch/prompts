# Failed Fix Escalation

**Identifier:** FIXFAIL-01
**System:** 05-scenarios/failed-fix
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** B
**Depends on:** none
**Produces:** `.failed-fix/ATTEMPT_LEDGER.md`, a decision: revert, re-scope, or escalate
**Inputs:** ORIGINAL_SYMPTOM, REPO_PATH (optional: ATTEMPT_LIST)
**Est. effort:** 20–45 min

---

## 1. Role and mandate

You are the engineer called in after one or more fix attempts have failed. Your job is to break the failure loop, not to add a fourth patch. Repeated failed fixes are almost never caused by insufficient effort; they are caused by a wrong model of the defect, a wrong reproduction, or a fix applied at the wrong layer.

## 2. When to use this

- Two or more attempts at the same defect have not worked.
- The fix works locally but not in CI / staging / production.
- Each fix reveals a new symptom in the same area.
- An agent has been "almost done" for a while and keeps changing the same files.
- Someone is proposing a rewrite to solve a bug.

**Do not use this** for a first attempt, or for a defect that is simply not yet understood — use `05-scenarios/debugging/` for that.

## 3. Objective and scope

**Produce:** an accurate record of what was tried and what it proved, an explicit statement of the current model of the defect and why it is probably wrong, and a decision — revert, change layer, narrow the reproduction, or escalate.

Out of scope: writing more speculative patches.

## 4. Prerequisites and inputs

| Input | Source | If missing |
|-------|--------|------------|
| List of attempts `{{ATTEMPT_LIST}}` (what changed, what happened) | git log, agent history, author | reconstruct from the diff history |
| The current state of the code in `{{REPO_PATH}}` | working tree | check whether failed attempts are still applied |
| The original symptom `{{ORIGINAL_SYMPTOM}}` and reproduction | issue/logs | re-establish before anything else |

## 5. Workflow

1. **Establish the current state first.** Is the tree clean, or are two failed attempts still sitting in the working copy? Record every uncommitted change and decide nothing until the baseline is known. Failed attempts left in place are the most common cause of "it is even more broken now".
2. **Build the attempt ledger** — one row per attempt:

   ```markdown
   | # | Hypothesis it tested | Change made | Predicted effect | Observed effect | Verdict |
   |---|----------------------|-------------|------------------|-----------------|---------|
   | 1 | ... | file:line | ... | ... | falsified / inconclusive / untested |
   ```

   The value of this table is diagnostic: repeated attempts usually test the *same* hypothesis in different costumes, or were never tested against a real reproduction.
3. **Classify why attempts failed:**
   - **Wrong model** — the assumed mechanism is not the real one (most common).
   - **Wrong reproduction** — the local repro does not match the failing environment.
   - **Wrong layer** — fixing the symptom's location instead of the cause's location (e.g. masking in the UI what is corrupt in the data).
   - **Untested assumption** — the fix was assumed to work without running the failing case.
   - **Incomplete fix** — addressed one code path of several.
   - **Regression** — the fix broke something else, and the new symptom was chased instead.
4. **State the current model explicitly** and attack it: what would have to be true for this defect to occur? What evidence exists *against* that? If the evidence against is strong, the model is wrong and more patching is waste.
5. **Reset the evidence base.** Re-read the original error/log; re-run the reproduction from a clean checkout; check whether the reproduction still reproduces at all (the environment may have changed). Confirm the failing path is the path being fixed — trace it rather than assuming.
6. **Change the variable class.** If attempts have been at the code level, move to data, configuration, environment, or dependency versions. If attempts have been local, get the artefact from the failing environment (logs, trace, core dump, network capture).
7. **Decide, and record the decision:**
   - **Revert** — the failed attempts add risk without value. Record the revert commit.
   - **Re-scope** — the defect requires a design change; stop patching and write the design note.
   - **Narrow** — write a smaller, deterministic reproduction that isolates the failing layer; hand it to systematic debugging.
   - **Escalate** — missing access, missing knowledge, or a third-party defect. Name exactly what is needed and from whom.
8. **Write the handoff:** the ledger, the current model with its weaknesses, the reproduction status, what was tried and what it proved, and the single next experiment (with the observation that would settle it).
9. **Set the stop rule for the next session:** if the next experiment also fails, the next step is escalation, not another patch. Write this down.

## 6. Decision rules and evidence standard

- **No new speculative patch in this workflow.** Its output is a decision, not a fix.
- **An attempt without a prediction taught nothing.** Record it as `inconclusive` rather than counting it as evidence.
- **Two attempts at the same layer with the same model = stop.** Effort is not a variable.
- **Failed attempts must not remain applied** unless deliberately kept as an experiment; if kept, record why.
- **The bug may not be where the stack trace points.** Proxies, queues, retries, caches, and serialisation change the answer; verify the layer, do not assume it.
- **Reverting is a legitimate, often correct outcome.** A clean baseline plus a precise reproduction is progress.

## 7. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Baseline state known | `git status`, diff review | recorded |
| Every attempt in the ledger | inspect | hypothesis, change, result |
| Failure classification justified | inspect | evidence per classification |
| Reproduction re-run | execute | result recorded (or reason it cannot run) |
| Model stated with counter-evidence | inspect | weaknesses listed |
| Decision recorded | inspect | one of revert/re-scope/narrow/escalate |
| Next experiment specified | inspect | singular, falsifiable |

## 8. Security and authorisation

Risk class B: you may revert failed attempts on a branch and create artifacts under `.failed-fix/`. Do not revert another person's committed work without recording it and, where the repository is shared, without agreement. Do not experiment against production.

## 9. Completion criteria

- [ ] Current tree state recorded; stray attempts identified.
- [ ] Attempt ledger complete with hypotheses and verdicts.
- [ ] Failure classification assigned with evidence.
- [ ] Current model stated, with the evidence against it.
- [ ] Reproduction re-run and confirmed (or its status recorded).
- [ ] Decision made and recorded.
- [ ] Single next experiment defined with its settling observation.
- [ ] Stop rule written for the following session.

## 10. Deliverables and handover

Artifacts: `.failed-fix/ATTEMPT_LEDGER.md`, decision record, handoff note.

Handover: `narrow` → `05-scenarios/debugging/SYSTEMATIC-DEBUGGING.md`; `re-scope` → `02-engineering/refactoring/` or architecture review; `escalate` → the named owner with the specific ask; `revert` → proceed to a fresh, evidence-based attempt with the ledger attached so the same hypothesis is not retried.
