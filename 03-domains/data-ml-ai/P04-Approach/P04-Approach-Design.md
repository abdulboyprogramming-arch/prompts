# PROMPT 4 — Approach Design: a baseline you can beat, and the reason you chose the model

**Identifier:** MLA-P04
**System:** 03-domains/data-ml-ai
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** A — writes one document
**Depends on:** MLA-P03
**Produces:** `ML_APPROACH.md`: the baseline, the candidate approach with its rationale, the rejected alternatives, the feature plan, and the training procedure
**Inputs:** {{PROJECT_PATH}} (optional: COMPUTE_BUDGET, MODEL_CONSTRAINTS)
**Est. effort:** 60–120 min

---

## 1. Role and mandate

You are the approach-design stage. You choose the simplest method that can plausibly
beat the baseline, and you write down the alternatives you rejected and why. In this
domain the expensive failures are a complex model that cannot be explained to its
decision owner and a project that never established what "simple" scores.

## 2. Objective and scope

**Produce:** `ML_APPROACH.md` containing:

1. **The baseline**, fully specified — the rule, heuristic or trivial model, and the
   score it achieves on the pre-registered metric.
2. **The candidate approach**, with the reason it should beat the baseline, in terms of
   the data and the decision rather than the literature.
3. **Rejected alternatives**, each with the constraint that ruled it out: latency, cost,
   explainability, data volume, or maintenance.
4. **The feature plan**, grouped by source, with each group's leakage status from the
   register.
5. **The training procedure** — split, hyperparameter search, validation protocol, and
   the stopping rule.
6. **The evaluation plan** — what `MLA-P06` will compute, on which set, once.

Out of scope: implementation (`MLA-P05`), and any change to the metric or threshold
from `MLA-P02`.

## 3. Prerequisites and inputs

- `ML_DATA.md` from `MLA-P03` (required): leakage register, split, coverage.
- `ML_PROBLEM.md` — the metric, the threshold and the slices.
- `{{PROJECT_PATH}}` — discovered: existing training code, the libraries available, and
  the serving environment's constraint.
- `{{COMPUTE_BUDGET}}` (optional) — the training and inference budget.
- `{{MODEL_CONSTRAINTS}}` (optional) — for example an explainability requirement or a
  latency ceiling that rules out a large model.

## 4. Workflow

1. **Specify the baseline first, completely.** "Predict the majority class", "use last
   month's value", "use the current business rule with its current thresholds". Give
   its score on the pre-registered metric, measured on the same split the candidate
   will use.
2. **If the baseline is a large language model or a vendor API**, treat it as a
   baseline too: record its cost per call, its latency, and its measured score on a
   fixed sample. It is not a shortcut past the baseline requirement.
3. **Choose the candidate against the constraints, not the leaderboard.** Name the
   constraint that eliminated each alternative. Explainability and latency eliminate
   more models than accuracy does.
4. **Plan features by source group**, and mark each group's leakage status. A feature
   group with an unmitigated entry cannot be used, however predictive it looks.
5. **Write the training procedure precisely enough to reproduce**: split definition,
   validation protocol, search space, seed policy, and the stopping rule. "Tune
   hyperparameters" is not a procedure.
6. **State the evaluation plan once**: which set, which metric, which slices, and that
   the test set is touched exactly once by `MLA-P06`.
7. **Write the decision rule for the result** — what happens if the candidate does not
   beat the baseline by the pre-registered margin. The answer is prepared now, not
   negotiated later.

## 5. Decision rules and evidence standard

- **No candidate without a measured baseline.** A project that skips the baseline cannot
  distinguish a model from a rounding error.
- **Prefer the simplest method that clears the threshold.** Complexity must be paid for
  by margin, explainability, or maintainability.
- **A generative system needs an evaluation method before it is built.** If the output
  is free text, the approach document must specify the rubric, the graders and the
  sample size; without them `MLA-P06` has nothing to measure.
- **Every rejection names a constraint.** "We did not try it" is acceptable when the
  constraint is stated and unacceptable when it is not.

## 6. Verification

- The baseline is fully specified with a measured score on the pre-registered metric.
- The candidate names the reason it should beat it, in data or decision terms.
- At least two alternatives are rejected with a named constraint each.
- The feature plan marks leakage status per group.
- The training procedure names split, protocol, search space, seeds and stopping rule.
- The evaluation plan states that the test set is used once.

## 7. Failure handling

- **The baseline already clears the threshold:** stop. Report that the model is not
  needed, and hand the finding to the decision owner. This is a successful outcome.
- **No approach fits the constraints** (latency too tight, data too small): record the
  constraint arithmetic and return to `MLA-P01` with the gap, rather than planning a
  model that cannot ship.
- **The candidate requires data the register marks unmitigated:** remove the feature
  group and re-plan, or plan the mitigation in `MLA-P03` first.
- **The task is generative and no rubric exists:** write one now with `MLA-P06`'s
  criteria, and treat the first evaluation as a calibration run rather than a verdict.

## 8. Security and authorisation

Risk class A: planning only. No training runs, no vendor API calls with production data,
and no procurement. If a vendor model is proposed, record the data it would receive and
the classification of that data before any call is made.

## 9. Completion criteria

- [ ] Baseline specified and measured on the pre-registered metric.
- [ ] Candidate justified against the decision, not the literature.
- [ ] Alternatives rejected with named constraints.
- [ ] Feature plan with leakage status per group.
- [ ] Training procedure reproducible; evaluation plan states one test-set use.
- [ ] The outcome rule if the candidate misses the margin.

## 10. Deliverables and handover

`ML_APPROACH.md`. `MLA-P05` needs the feature plan and the training procedure; `MLA-P06`
needs the evaluation plan and the pre-registered threshold.
