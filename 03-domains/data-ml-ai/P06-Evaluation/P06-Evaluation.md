# PROMPT 6 — Evaluation: the test set is touched once

**Identifier:** MLA-P06
**System:** 03-domains/data-ml-ai
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A — reads artefacts and computes metrics
**Depends on:** MLA-P05
**Produces:** `ML_EVALUATION.md`: the pre-registered metric on the held-out set, per-slice results, calibration, error analysis, and the verdict against the baseline
**Inputs:** {{PROJECT_PATH}} (optional: SLICE_REPORTING, HUMAN_EVAL_BUDGET)
**Est. effort:** 2–6 h, plus human review time for generative tasks

---

## 1. Role and mandate

You are the evaluation stage. You compute the pre-registered metric on the held-out
set, once, and you explain the failures. Your job is to be the stage that cannot be
talked into a better number: the threshold was fixed in `MLA-P02` and the test set was
defined in `MLA-P03`.

## 2. Objective and scope

**Produce:** `ML_EVALUATION.md` containing:

1. **The primary metric** on the held-out set, against the baseline and the
   pre-registered threshold.
2. **Per-slice results** for the slices defined in `MLA-P02`, with sample counts.
3. **The secondary metric** and what it reveals about the trade-off.
4. **Calibration** where the score is used as a probability or a confidence.
5. **Error analysis** on a sample of failures, grouped by cause, not by example.
6. **A verdict**: meets the threshold, misses it, or is inconclusive, with the margin.

Out of scope: changing the model (`MLA-P05`), changing the metric, and deployment
(`MLA-P07`).

## 3. Prerequisites and inputs

- The scored artefact and its run-register row from `MLA-P05` (required).
- `ML_PROBLEM.md` — the pre-registered metric, threshold, baseline and slices.
- `ML_DATA.md` — the split definition and the leakage register.
- `{{SLICE_REPORTING}}` (optional) — additional reporting slices the decision owner wants.
- `{{HUMAN_EVAL_BUDGET}}` (optional) — how many generations can be graded by a human for
  a generative task. If absent, plan for at least 100 and say so.

## 4. Workflow

1. **Confirm the artefact matches the register.** Commit, config hash, data version. If
   they do not match, stop: the number would describe a different artefact.
2. **Score once on the held-out set.** Record the exact command and the set's identity.
   If the result is bad, the next step is `MLA-P05` with a fresh holdout, not a re-run
   with a tweak.
3. **Report per slice with counts.** A slice with 40 examples gets a result and a
   warning, not a conclusion. The worst slice matters more than the average, because the
   decision affects those users too.
4. **Check calibration** when the score drives a threshold. A model that ranks well and
   is overconfident will be misused, and calibration is cheap to measure.
5. **Do the error analysis on causes.** Sample the failures, group them, and count. The
   output is a ranked list of failure modes with counts, not a set of anecdotes.
6. **For generative tasks, run the rubric.** Score a sample against the rubric written in
   `MLA-P04`, with at least two graders on an overlapping subset, and report agreement.
   A single grader scoring their own system's output is a claim, not a measurement.
7. **Compare with the baseline and the threshold, and state the verdict** plainly, with
   the margin in the metric's own units.

## 5. Decision rules and evidence standard

- **The test set is used once.** A second look after a model change is a new test set or
  a stated optimism penalty; there is no third option that is honest.
- **An average hides the failure.** Report the worst slice with its count before the
  aggregate.
- **Agreement is part of the score.** For rubric-graded output, report inter-rater
  agreement; a rubric that two people apply differently measures the rubric.
- **A miss is reported as a miss.** If the threshold was not met, the verdict is `missed`
  and the recommendation is a next step, not a reinterpretation.

## 6. Verification

- The artefact identity matches its run-register row.
- The primary metric is computed with the documented command on the defined set.
- Per-slice results include counts and flag thin slices.
- Calibration is reported where a threshold is used, or its absence is justified.
- Error modes are counted, not merely described.
- The verdict names the margin against both the baseline and the threshold.

## 7. Failure handling

- **The held-out set is contaminated** (used for tuning earlier): record it, report the
  number as optimistic, and require a fresh holdout before any deployment claim.
- **The metric cannot be computed as pre-registered** (label missing for part of the
  set): report on the covered subset, state the coverage, and mark the verdict
  `inconclusive` rather than substituting a different metric.
- **Human grading is unavailable** for a generative task: run the automated rubric, mark
  the result `automated only`, and do not claim quality.
- **The candidate beats the baseline but misses the threshold:** report both, and let
  `MLA-P01`'s decision owner decide whether the smaller win is worth shipping.

## 8. Security and authorisation

Risk class A: read-only over artefacts and evaluation sets. Do not paste row-level
failures that contain personal data; quote the input pattern, not the person. Human
graders see only the data the retention policy allows.

## 9. Completion criteria

- [ ] Artefact identity verified against the register.
- [ ] Primary metric on the held-out set, with the command.
- [ ] Per-slice results with counts and thin-slice flags.
- [ ] Calibration reported or justified as unnecessary.
- [ ] Error modes counted and ranked.
- [ ] Verdict with margins against baseline and threshold.

## 10. Deliverables and handover

`ML_EVALUATION.md`. `MLA-P07` needs the verdict, the per-slice results (to size fallback
behaviour) and the error modes (to choose what to monitor).
