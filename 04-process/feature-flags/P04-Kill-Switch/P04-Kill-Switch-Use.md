# PROMPT 04 — Kill-Switch Use Under Pressure

**Identifier:** FF-P04
**System:** 04-process/feature-flags
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** specialised
**Risk class:** C
**Depends on:** FF-P01 (a kill-switch exists and is audited)
**Produces:** `.flags/SWITCH_LOG.md`
**Inputs:** TARGET_SERVICE, INCIDENT_ID (optional: APPROVER, TARGET_ENV)
**Est. effort:** 5–30 min per decision, in real time

---

## 1. Role and mandate

You are using a flag as an incident control. The decision to flip is a production change made under time pressure with incomplete information — exactly the conditions that produce the worst changes.

Your discipline: **state what you expect the flip to fix, flip once, verify the expected effect, and record what it did not fix.** A kill-switch that "seems to have helped" while the error rate stays flat has told you the cause is elsewhere, and that is the most valuable information in the incident.

## 2. Objective and scope

**Produce:** a recorded switch decision — observed symptom, hypothesis, expected effect, the flip, the measured result, and the residual state (including data written before the flip) — or a reasoned decision *not* to flip.

Out of scope: the wider incident command (`05-scenarios/incident-response/`), root-cause analysis of a defect (`05-scenarios/debugging/`), designing flags (P02).

## 3. Prerequisites and inputs

- A known flag identifier from `.flags/FLAG_INVENTORY.md`, with its type and the owner/operator recorded there. If the flag is unaudited, audit its behaviour before relying on it as a control.
- `{{TARGET_SERVICE}}` and `{{INCIDENT_ID}}` for the record; `{{TARGET_ENV}}` if there is more than one; `{{APPROVER}}` where policy requires one for production changes.
- Current dashboards for the symptom metric — you cannot evaluate the effect of a flip without a before-and-after reading at a known timestamp.

## 4. Workflow

1. **State the symptom as a number and a timestamp.** "p99 latency 4.2 s since 14:05, 12% error rate on the checkout API" — not "checkout is broken". This becomes the comparison baseline.

2. **State the hypothesis the flip tests.** Which code path is responsible, and why the off state removes it. If you cannot say which path the flag controls, you are flipping a coin in production.

3. **Predict the effect before flipping.** Expected movement in the metric, the time to take effect (cache TTL, connection draining, in-flight requests), and what would *not* change. Write the prediction down; it is what makes the outcome interpretable.

4. **Choose the narrowest switch that removes the harm.** Prefer the flag for the failing feature over a global flag that stops all traffic; prefer cohort-scoped over global when the harm is cohort-specific. Record the exposure scope you are disabling.

5. **Check the reversibility and the data consequences before the flip.** What has the new path already written? Will the old code read those records, schemas, or messages? A kill-switch usually stops *new* work; it does not undo completed work. If disabling creates orphaned or unreadable data, say so before acting and involve the data owner.

6. **Flip once, note the exact time, and watch the declared interval.** Do not flip back and forth: each flip resets the observation and makes causality unknowable. If the change is not visible within the expected time, check propagation before concluding the hypothesis failed.

7. **Evaluate against the prediction, not against relief.** Record the metric at the comparison time. Three outcomes, each with a different next step:
   - **Effect as predicted** → hold, and record the residual work: the fix, the data already written, the flag state, and who will restore it.
   - **No effect** → the hypothesis is wrong; the flag stays off only if it is harmless, and the investigation moves to the next candidate. Say clearly that the cause is still unknown.
   - **Worse** → revert the flip immediately if reverting is safer, then escalate; record why the flag's off state was harmful (an untested path is now proven untested).

8. **Record the state you are leaving behind** for the incident commander and the next responder: flags in non-default state, exposure removed, work in flight, data affected, and who will restore the flag. A flag left flipped by an incident becomes invisible debt the moment the incident closes.

9. **Write `.flags/SWITCH_LOG.md`:** symptom, hypothesis, prediction, flip (flag, scope, time, operator), result with numbers, residual data state, flag state on exit, and the follow-ups (fix, restore, P05 removal if the off state becomes permanent).

## 5. Decision rules and evidence standard

- **One flip, one observation.** Repeat flips destroy the ability to attribute the change.
- **Prediction before action.** An unstated prediction makes the outcome a story rather than evidence.
- **Prefer the narrowest control** that removes the harm; a global flag is a blunt instrument that hides the cause.
- **A kill-switch does not undo data.** Check the write path; disabling a producer does not purge what it produced.
- **Never flip an untested off-path during an incident** without saying that you are now running code no test has executed — and prefer a non-flag mitigation if the off-path is unverified.
- **The record matters as much as the recovery**: the next responder needs to know the flag state, not just that the incident "resolved".

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Symptom quantified | metric + timestamp | baseline recorded before flip |
| Hypothesis names the path | read-through | specific code path |
| Prediction recorded | log entry predating the flip | expected effect stated |
| Narrowest scope used | scope comparison | no broader than the harm |
| Data consequences checked | write-path review | stated before acting |
| Effect measured | post-flip metric | numbers, same comparison basis |
| Exit state recorded | log | flags, data, owner for restoration |
| Follow-ups assigned | inspect | owner and date per item |

## 7. Failure handling

- **Flag provider is unreachable** (the case a kill-switch defaults on for) → use the documented fallback: config override, deployment rollback, or traffic-level mitigation. State that you cannot use the switch.
- **The off-path fails when used** → stop relying on it, note the failure as a finding for P01/P05, and use the deployment rollback path instead.
- **Policy requires an approver and none is reachable** → for a class C/D harm, act to stop the harm if that authority is pre-delegated for incidents; otherwise escalate and document the delay and its cost. Never improvise authority.
- **The flip helps but the cause remains unknown** → hold the mitigated state and hand the diagnosis to `05-scenarios/debugging/` with the flag state recorded; do not "leave it off and move on" without an owner.
- **Multiple flags suspected** → flip one, observe, then the next. Sequential changes are diagnosable; simultaneous ones are not.

## 8. Security and authorisation

Risk class C: this changes production behaviour. Follow the incident's authority model — the incident commander or the pre-delegated on-call operator flips; the agent proposes and records unless the operator role has been explicitly delegated. Never disable a security control (authentication, rate limiting, audit logging, WAF rule) as a mitigation; that converts an availability problem into a security event. Do not paste customer identifiers or credentials into the switch log.

## 9. Completion criteria

- [ ] Symptom quantified with a baseline timestamp.
- [ ] Hypothesis names the code path.
- [ ] Predicted effect written before the flip.
- [ ] Narrowest effective scope chosen.
- [ ] Data-write consequences checked and stated.
- [ ] Single flip executed and effect measured.
- [ ] Outcome classified: as predicted / no effect / worse, with the next step.
- [ ] Exit state recorded: flags, exposure, data, restoration owner.

## 10. Deliverables and handover

Artifact: `.flags/SWITCH_LOG.md`.

Handover: the incident commander receives the residual state and the restoration owner; `05-scenarios/debugging/` receives the unexplained cause; P05 receives any flag whose off state is now permanent (a feature that should not return is a removal, not a rollout).
