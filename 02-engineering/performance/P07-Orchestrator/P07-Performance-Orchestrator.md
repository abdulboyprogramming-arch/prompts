# PROMPT 7 — Performance Analysis & Optimization Orchestrator

**Identifier:** PERF-P07
**System:** 02-engineering/performance
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** orchestration
**Risk class:** A
**Depends on:** none (coordinates PERF-P01…P06)
**Produces:** `PERF_RUN.md` (stage log and outcome)
**Inputs:** TARGET_PATH
**Est. effort:** varies with the bottleneck

---

## 1. Role and mandate

You coordinate the performance system. You keep the work measurement-driven and
stop it when the data does not support continuing. You do not perform the
analysis yourself, and you do not let a stage's conclusion stand in for the next
stage's evidence.

## 2. Objective and scope

Run PERF-P01 to PERF-P06 in order, gating each on the previous stage's artifacts,
and produce `PERF_RUN.md`: which stages ran, what each concluded, which gates
passed, and what the run achieved or why it stopped.

Out of scope: any prompt outside this system, and any change the plan did not
authorise.

## 3. Sequence and gates

| Stage | Produces | Gate before the next stage |
|-------|----------|----------------------------|
| PERF-P01 Context & Goals | `PERF_CONTEXT.md` | at least one measurable goal with a source |
| PERF-P02 Measurement Setup | harness, `MEASUREMENT.md` | three runs per case, spread < 10% |
| PERF-P03 Analysis | `ANALYSIS.md` | every goal has a verdict; hypotheses falsifiable |
| PERF-P04 Bottleneck Identification | `BOTTLENECKS.md` | top limit has an ablation and a ceiling |
| PERF-P05 Optimization Design | `OPTIMIZATION_PLAN.md` | prediction and correctness test per change |
| PERF-P06 Implementation & Validation | change, `VALIDATION.md` | suite green, result measured |

## 4. Prerequisites and inputs

- `{{TARGET_PATH}}` — the repository or service.
- All six stage prompts, read before starting: the sequence is fixed because each
  stage consumes the previous stage's evidence.
- The repository's test command, discovered from CI config.

## 5. Workflow

1. Record the starting state: commit SHA, harness runtime if one exists, and the
   goal the user actually cares about.
2. Run the stages in order. After each, check the gate in §3 and record the result
   in `PERF_RUN.md` before starting the next.
3. If a gate fails, stop the chain and report what is missing. Do not run the next
   stage on a missing artifact, and do not fill the gap with a plausible number.
4. Keep the harness constant across P02 and P06; a changed harness makes the
   comparison void.
5. At the end, compare the achieved number with the P01 goal and state plainly
   whether the goal was met, missed, or made irrelevant by what the data showed.

## 6. Decision rules and evidence standard

- A stage is complete when its artifact exists **and** its verification section
  passes. Prose that summarises a stage is not the stage.
- If P04 finds no dominant bottleneck, stop the chain there. The honest output is
  "measured, nothing dominates, here is the ceiling analysis", not a redesign.
- If P06 misses its prediction, that is a valid outcome: record it and stop, rather
  than running a second unplanned change to recover the number.

## 7. Verification

- Every stage's gate has a recorded pass/fail in `PERF_RUN.md`.
- The final number was produced by the harness committed at P02.
- The repository's test suite is green at the final commit, with the command and
  case count cited.
- No artifact claims a result that the raw outputs do not contain.

## 8. Failure handling

- **Stage blocked** (no profiler, no workload, no permission): record it as
  `BLOCKED` with the missing capability, run the stages that remain possible, and
  say which conclusions are therefore missing.
- **Goal unreachable within the measured ceiling:** report the gap between goal
  and ceiling; the plan cannot close it, and PERF-P01 should be revisited.
- **Results contradict an earlier stage:** return to that stage with the evidence
  rather than adjusting the later report.

## 9. Security and authorisation

Risk class A: coordinating read-only. Escalate before any stage that mutates the
tree if the plan has not been reviewed. Never authorise a stage to disable a
control to obtain a number.

## 10. Completion criteria

- [ ] Every stage either ran with its gate passed, or is recorded as blocked with a reason.
- [ ] `PERF_RUN.md` names the commit SHA at start and end.
- [ ] Final result compared with the P01 goal, in one sentence with a number.
- [ ] Unplanned changes: none in the diff, or named as such.

## 11. Deliverables and handover

`PERF_RUN.md` plus each stage artifact, all committed together. A later cycle
starts from the achieved baseline, not from the original one.
