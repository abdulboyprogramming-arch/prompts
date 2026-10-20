# PROMPT 03 — Progressive Rollout

**Identifier:** FF-P03
**System:** 04-process/feature-flags
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** C
**Depends on:** FF-P02 (design and defaults)
**Produces:** `.flags/ROLLOUT_LOG.md`
**Inputs:** TARGET_ENV, TARGET_SERVICE (optional: APPROVER, CHANGE_WINDOW)
**Est. effort:** 1–3 h planning; elapsed time set by the stages

---

## 1. Role and mandate

You move a flagged change from invisible to fully exposed, one bounded step at a time, with a pre-declared way to stop. The value of progressive delivery is not the percentage ladder — it is the **decision to abort that was made before you were invested in the outcome**.

You do not improvise thresholds after seeing the graph. You do not skip a stage because the first one "looked fine".

## 2. Objective and scope

**Produce:** an executed or planned stage sequence with, per stage: exposure, cohort, duration, guardrail thresholds, the evidence to collect, the decision rule, and the recorded decision.

Out of scope: designing the flag (P02), responding to an incident where the flag is the control (P04), removing the flag (P05).

## 3. Prerequisites and inputs

- `.flags/FLAG_DESIGN.md` (defaults, targeting, both-states tests) and a passing both-states test run.
- `{{TARGET_ENV}}` and `{{TARGET_SERVICE}}` with dashboards for the guardrail metrics; `{{CHANGE_WINDOW}}` for when exposure changes are permitted; `{{APPROVER}}` for stopping or continuing past a red gate if your policy requires it.
- A baseline: the metric values for the *current* behaviour over a comparable period, recorded before the first stage.

## 4. Workflow

1. **Define the guardrail metrics and the success metric before any exposure.** Guardrails are the things that must not get worse: error rate, latency p95/p99, saturation, queue depth, payment success, support contacts, crash rate. Success is what the change is for. For each: the metric definition, the baseline value and its normal variance, the threshold that stops the rollout, and the observation interval that makes it meaningful (an error budget measured over ten minutes on a low-traffic service is noise).

2. **Choose the cohort ladder, not a percentage ladder.** Internal users → a low-risk tenant or region → a percentage of the remainder → everyone. Cohort first because a tenancy bug in 5% of random traffic is unanalysable, while a tenancy bug in one test tenant is a phone call.

3. **Set durations to the traffic, not to convenience.** A stage must last long enough to collect the sample the threshold needs. Compute the required sample: for a 1% error-rate change on a service doing 100 requests/hour, the stage is days, not an hour. Write the calculation down; it is the most common dishonest part of a rollout.

4. **Pre-declare the decision rule per stage:** continue, pause, roll back, or stop-and-escalate, with the numeric condition for each. "We will watch the dashboards" is not a rule.

5. **State the abort mechanics before starting:** who can flip the flag, how quickly it takes effect, whether in-flight work is affected, and what data the change has already written that a flip will not undo. A rollout that creates records the old code cannot read is not reversible by a flag.

6. **Execute one stage at a time.** Record: timestamp, exposure change, the person/agent who made it, the metric snapshot at the start, and the observation window. Wait the declared duration. Do not stack stages to save time.

7. **At each gate, compare against the threshold and record the decision with its evidence.** A "continue" is a decision that needs the numbers written down, not an absence of alarm.

8. **Watch for the class of failure that a flag cannot fix.** Errors may be identical in both states while the *data* diverges (new writes incompatible with old readers), or the failure may only appear on the reverse path (turning it off after the new path wrote state). Add an explicit check for writes and schema/format compatibility, and a test of the planned reversal on a non-production environment before the first production stage.

9. **Close the rollout:** exposure at 100%, duration held long enough to satisfy the removal criteria in P02, the observation recorded, and the flag's removal scheduled. A rollout that ends at 100% with the flag still in the code is only half done.

10. **Write `.flags/ROLLOUT_LOG.md`:** metric definitions and baselines, the stage table with thresholds and actuals, decisions and their evidence, anomalies seen and dismissed (with reason), and the handover to P05.

## 5. Decision rules and evidence standard

- **Thresholds before data.** A threshold chosen after seeing the graph is not a control.
- **One variable at a time.** If another change ships during a stage, the stage's evidence is confounded — record it and either extend or restart.
- **A guardrail breach stops the rollout by default**, up to the last known-good exposure. Continuing past a breach requires a stated reason, the approver, and a documented risk acceptance.
- **Small sample is not "no signal".** State the confidence you actually have; do not convert an underpowered stage into a pass.
- **Reversal must be tested, not assumed**, including the effect on data already written.
- **The kill-switch is part of the design**, and its exercise is part of the rollout (do it on the first stage, not during an incident).

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Baselines recorded first | artifact timestamps | baseline predates stage 1 |
| Thresholds pre-declared | inspect | numeric, per guardrail |
| Sample-size reasoning | computation shown | stage duration justified |
| Decisions evidenced | per-stage record | numbers, not adjectives |
| Reversal tested | non-production run or drill | result recorded |
| Data compatibility checked | write-path analysis | old readers unaffected, or flagged |
| Confounders noted | log | concurrent changes listed |
| Removal scheduled | link to P05 criteria | date and owner |

## 7. Failure handling

- **A guardrail breaches** → hold at the last known-good exposure, record the breach, diagnose with `05-scenarios/debugging/`, and do not resume until the cause is understood or the risk is accepted in writing.
- **The flag's off-path does not restore behaviour** (partial exposure leaves inconsistent state) → stop the ladder, document the non-reversibility, and treat the change as a migration rather than a feature: route to the relevant domain system.
- **Traffic is too low to measure** → the honest options are a longer stage, a cohort-based exposure with direct verification, or an explicit decision to accept unmeasured risk. Say which you chose.
- **Another deploy lands mid-stage** → record it as a confounder; if it touches the same code path, restart the stage.
- **Provider evaluation is inconsistent** (users flipping between states) → stop; fix bucketing before continuing. Inconsistent exposure invalidates everything measured so far.
- **Pressure to skip stages for a deadline** → record who accepted the residual risk; an unmeasured 100% rollout is a deploy, and should be labelled as one.

## 8. Security and authorisation

Risk class C: this stage changes production behaviour and exposure. Exposure changes require the authority named in P02, and any stage touching money, personal data, or a class C/D action requires `APPROVER`. Do not widen exposure to satisfy a deadline, do not grant targeting overrides by hand outside the recorded ladder, and never expose a change that disables a security control to a general cohort before security review.

## 9. Completion criteria

- [ ] Guardrails and success metric defined with baselines and sample reasoning.
- [ ] Cohort ladder and durations chosen and justified.
- [ ] Numeric decision rule per stage, declared before execution.
- [ ] Abort mechanics and data-write consequences stated.
- [ ] Reversal exercised before production exposure.
- [ ] Each stage recorded with snapshot, window, and decision.
- [ ] Confounders and anomalies recorded.
- [ ] Removal date and owner handed to P05.

## 10. Deliverables and handover

Artifact: `.flags/ROLLOUT_LOG.md`.

P05 receives: exposure history, the evidence that the winning state is stable, and the removal criteria — which are now executable because the flag has been at 100% for a measured period. P04 may receive the same log if the flag must be used as a control.
