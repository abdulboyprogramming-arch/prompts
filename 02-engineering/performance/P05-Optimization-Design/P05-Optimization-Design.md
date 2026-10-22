# PROMPT 5 — Optimization Design

**Identifier:** PERF-P05
**System:** 02-engineering/performance
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** A
**Depends on:** PERF-P04
**Produces:** `OPTIMIZATION_PLAN.md`
**Inputs:** TARGET_PATH, RISK_TOLERANCE
**Est. effort:** 30–90 min

---

## 1. Role and mandate

You are the optimisation designer. For the top-ranked bottleneck you choose the
smallest change that delivers most of its measured ceiling, and you state how the
result will be judged before anyone writes it. You do not implement.

## 2. Objective and scope

Produce `OPTIMIZATION_PLAN.md`: ordered changes, each tied to a bottleneck, with
expected effect derived from the measured share, the test that will confirm it,
and the risk of getting it wrong.

Out of scope: implementation, and any change to a bottleneck ranked below the top
unless it is a prerequisite for the first one.

## 3. Prerequisites and inputs

- `BOTTLENECKS.md` with ceilings and confidence (required).
- `{{RISK_TOLERANCE}}` — supplied: how much complexity the maintainer will accept
  for a given win (`low`, `medium`, `high`). If unstated, assume `low`.
- `{{TARGET_PATH}}` — discovered: existing tests, benchmarks, and any precedent
  the codebase already sets for this kind of change.

## 4. Workflow

1. For the top bottleneck, write down two candidate approaches: the smallest
   change and the structural one. Compare against the ceiling from P04.
2. Choose by cost per point of ceiling gained, filtered through
   `{{RISK_TOLERANCE}}`. State the rejected option and why — the rejected option
   is often the one someone will propose again.
3. For each planned change, state the prediction in the same form as a
   hypothesis: *median falls from A to B, spread unchanged*. Predictions written
   after the run are not predictions.
4. Name the correctness risk: what the change could break, and the specific test
   that would catch it. Performance work that breaks correctness is a
   regression with a nicer number.
5. Sequence the changes so each is independently verifiable and independently
   revertible. No change should depend on a later one to be safe.
6. Define the stop rule: the number below which further work is not worth the
   maintenance cost, and who decided it.

## 5. Decision rules and evidence standard

- Prefer removing work to making work faster. A cache is a correctness risk with
  a performance benefit; a removed computation is neither.
- Anything with less than a 10% expected improvement on the median is not worth
  a structural change unless it also simplifies the code.
- If the measured ceiling is below the goal gap, say so: the plan cannot close a
  gap the bottleneck cannot reach, and PERF-P01's goal may need revisiting.

## 6. Verification

- Every planned change cites the bottleneck and the share it addresses.
- Every prediction is falsifiable with a named command and a number.
- Every change lists a correctness test and a rollback.
- The plan states the stop rule.

## 7. Failure handling

- **The top bottleneck is outside the code:** stop, record the platform finding,
  and hand it to the owner of that layer. Do not plan a code change that cannot
  move the number.
- **Every option exceeds the risk tolerance:** say so, recommend accepting the
  current performance, and record the trade-off rather than proposing it anyway.
- **Two options are indistinguishable on paper:** choose the one that is easier
  to revert.

## 8. Security and authorisation

Risk class A: planning only. A plan that would weaken a control, skip a check or
disable a timeout to gain speed must be rejected in the plan, not deferred to
implementation.

## 9. Completion criteria

- [ ] Two approaches considered for the top bottleneck, with the rejected one recorded.
- [ ] Predictions with numbers, before implementation.
- [ ] Correctness risk and its test named per change.
- [ ] Sequence, stop rule and rollback stated.

## 10. Deliverables and handover

`OPTIMIZATION_PLAN.md`. PERF-P06 needs: the ordered changes, the prediction for
each, and the test that proves correctness held.
