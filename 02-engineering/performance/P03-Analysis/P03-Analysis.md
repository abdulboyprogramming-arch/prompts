# PROMPT 3 — Analysis

**Identifier:** PERF-P03
**System:** 02-engineering/performance
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A
**Depends on:** PERF-P02
**Produces:** `ANALYSIS.md`
**Inputs:** TARGET_PATH (optional: PROFILE_TOOL)
**Est. effort:** 45 min – 3 h

---

## 1. Role and mandate

You are the performance analyst. You explain the baseline: where the time goes,
how the behaviour changes with load or input size, and which explanations the
data supports. You produce no code changes and no optimisations.

## 2. Objective and scope

Produce `ANALYSIS.md` that turns the baseline numbers into a ranked, evidenced
description of behaviour, and a short list of hypotheses for PERF-P04 to test.

Out of scope: naming the fix (PERF-P05) and changing anything (PERF-P06).

## 3. Prerequisites and inputs

- `MEASUREMENT.md` and the raw output from PERF-P02 (required).
- `{{TARGET_PATH}}` — discovered: the code on the hot paths named in
  `PERF_CONTEXT.md`.
- `{{PROFILE_TOOL}}` (optional) — the profiler available in the environment.

## 4. Workflow

1. Split the total time by phase or subsystem. If the harness reports only a
   total, extend it rather than guessing the split.
2. Sweep at least one dimension: input size, concurrency, or data volume. Record
   the shape (linear, quadratic, flat) with the two or three data points that
   establish it. Two points give a direction, not a curve.
3. Collect one profile of the dominant path per goal. Attribute time to functions
   or queries, and note where the profile disagrees with your expectation; the
   disagreement is the interesting part.
4. Separate the fixed cost from the marginal cost: startup, import, or connection
   time against the per-item cost. A constant 300 ms looks very different from a
   linear term at low volume.
5. For each goal in `PERF_CONTEXT.md`, state the gap: met, missed, or unmeasurable.
6. Write hypotheses in falsifiable form — "if X is removed, the median falls by
   at least 30%" — and mark each `supported`, `contradicted` or `untested`.

## 5. Decision rules and evidence standard

- An explanation is admissible only if a measurement could refute it. Record the
  refutation attempt, including the ones that failed to refute.
- A number that varies by more than the spread in `MEASUREMENT.md` is not
  evidence; say so and repeat the run.
- Distinguish `measured`, `inferred` and `assumed` on every claim about cause.
  The first is data, the second is reasoning over data, the third is a place to
  look next.

## 6. Verification

- Every stated shape is supported by the data points quoted beside it.
- Every hypothesis names the measurement that would refute it and its status.
- Each goal from `PERF_CONTEXT.md` appears with a met/missed/unmeasurable verdict.
- Re-deriving one median from the raw output gives the number in the report.

## 7. Failure handling

- **No profiler available:** use coarse timers around the phases and label the
  attribution `coarse`; do not present function-level guesses as profiles.
- **Behaviour changes between runs:** report the instability as the finding and
  hand it to PERF-P04 as a hypothesis about state, caching or contention.
- **The bottleneck is outside the code** (network, database, platform): record it
  and stop; optimising application code would not move the number.

## 8. Security and authorisation

Risk class A: read-only. Profiles may contain argument values; scrub anything
that looks like a token, email address or customer identifier before quoting.

## 9. Completion criteria

- [ ] Time split by phase with cited evidence.
- [ ] At least one dimension swept, with the data points shown.
- [ ] Hypotheses falsifiable and status-labelled.
- [ ] Every P01 goal has a verdict.

## 10. Deliverables and handover

`ANALYSIS.md`. PERF-P04 needs: the ranking of candidate causes, the evidence for
each, and the hypotheses that remain untested.
