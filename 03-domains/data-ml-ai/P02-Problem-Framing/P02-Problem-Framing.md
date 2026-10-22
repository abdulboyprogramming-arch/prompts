# PROMPT 2 — Problem Framing: the metric is a decision about costs

**Identifier:** MLA-P02
**System:** 03-domains/data-ml-ai
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** A — writes one document
**Depends on:** MLA-P01
**Produces:** `ML_PROBLEM.md`: the task definition, the unit of analysis, the metric with its threshold, the pre-registered success criteria, and the shortcuts that are forbidden
**Inputs:** {{PROJECT_PATH}} (optional: SUCCESS_THRESHOLD, EVALUATION_DATA)
**Est. effort:** 45–90 min

---

## 1. Role and mandate

You are the problem-framing stage. You convert the decision from `MLA-P01` into a
learning task with a measurable target, and you fix the success threshold **before**
any model is trained. This stage is where most ML projects become unfalsifiable: a
metric chosen after seeing results, or a threshold that moves to meet the model.

## 2. Objective and scope

**Produce:** `ML_PROBLEM.md` containing:

1. **The task in one sentence** — input, output, unit of analysis, and prediction
   horizon. "Predict churn" is not a task; "predict, at the end of each month,
   whether an account will cancel in the next 30 days" is.
2. **The label definition**, with its measurement delay and its known noise.
3. **The primary metric**, chosen from the cost asymmetry in `ML_CONTEXT.md`, plus
   one secondary metric that catches the failure the primary hides.
4. **The pre-registered success threshold** — the number the model must beat, and the
   number the baseline already achieves.
5. **Forbidden shortcuts** — leakage paths, proxies, and target-derived features that
   would make the metric meaningless.
6. **Slices** — the segments the metric must be reported on separately, chosen because
   the decision affects them differently.

Out of scope: data inventory (`MLA-P03`), model choice (`MLA-P04`), and any training.

## 3. Prerequisites and inputs

- `ML_CONTEXT.md` from `MLA-P01` (required).
- `{{PROJECT_PATH}}` — discovered: any existing label table, target column, or
  evaluation notebook that already defines the task.
- `{{SUCCESS_THRESHOLD}}` (optional) — a business threshold already agreed. If absent,
  derive one from the cost ratio and mark it `proposed`.
- `{{EVALUATION_DATA}}` (optional) — an existing held-out set. If it has been used for
  tuning, record that, because its future results will be optimistic.

## 4. Workflow

1. **Write the task sentence with the horizon.** Name what is known at prediction time
   and when the answer becomes known. The gap between those two moments is the
   measurement delay and it constrains how the model can be monitored.
2. **Define the label precisely.** The query, the window, the exclusion rules, and
   how long after the fact it becomes available. A label that arrives 90 days late
   cannot be used for monthly monitoring without saying so.
3. **Choose the metric from the cost ratio.** Ratio near 1: use a symmetric metric
   that reflects the decision. Ratio far from 1: use one that weights the expensive
   error, and state the weighting. A ratio of 1:50 with an unweighted accuracy metric
   is a defect in the framing, not a detail.
4. **Add the secondary metric** that catches what the primary hides: precision when
   the primary is recall, calibration when the primary is ranking, worst-slice
   performance when the primary is an average.
5. **Pre-register the threshold and the baseline.** Write the number the model must
   reach, the number the baseline already reaches, and the date. This is the document
   `MLA-P06` is judged against; changing it afterwards is the failure this stage exists
   to prevent.
6. **List forbidden shortcuts.** For each, name the column or path and the mechanism
   by which it would leak. `MLA-P03` turns this list into the leakage register.
7. **Choose the slices** the metric must be reported on: by volume, by segment, by
   tenure, by geography — whichever the decision treats differently.

## 5. Decision rules and evidence standard

- **A metric that cannot be computed from the label is not a metric.** If the data
   cannot produce it, choose another and say why.
- **The threshold is written before the model exists.** A threshold chosen after the
  first result is a description of that result.
- **One primary metric.** More than one primary metric means the trade-off is
  undecided, and the model with the best story wins.
- **Offline to online is a claim, not a fact.** If the metric is offline, say what
  evidence would connect it to the online decision, and mark the gap.

## 6. Verification

- The task sentence names input, output, unit and horizon.
- The label definition includes its delay and its noise.
- The primary metric follows from a stated cost ratio, and the secondary metric is
  named with the failure it catches.
- The threshold and the baseline are both numbers, dated, before any training.
- Every forbidden shortcut names the mechanism it would leak through.
- At least three slices are defined for reporting.

## 7. Failure handling

- **The label does not exist and must be constructed** (weak supervision, heuristics,
  human review): record the construction method, its expected noise, and mark every
  result in `MLA-P06` as bounded by that noise.
- **The cost ratio is `unstated`** from `MLA-P01`: choose the metric the decision
  owner can explain, mark the threshold `provisional`, and state that `MLA-P06` cannot
  declare success until the ratio is agreed.
- **The existing evaluation set has been used for tuning:** record it, mark the set
  `contaminated`, and require a fresh holdout in `MLA-P03`. Do not reuse it and call
  the result honest.
- **The task is really two tasks** (detect and rank, or classify and explain): split
  them, define a metric for each, and let `MLA-P04` decide whether one model serves both.

## 8. Security and authorisation

Risk class A: planning only. Do not copy label queries that expose personal data into
the document; cite the table and the owner. If the label encodes a protected attribute
or a proxy for one, record it here — `MLA-P03` and `MLA-P06` both need to know.

## 9. Completion criteria

- [ ] Task sentence with input, output, unit and horizon.
- [ ] Label definition with delay and noise.
- [ ] Primary metric derived from a stated cost ratio; secondary metric with its purpose.
- [ ] Pre-registered threshold and baseline, both numeric and dated.
- [ ] Forbidden shortcuts with mechanisms.
- [ ] At least three slices for reporting.

## 10. Deliverables and handover

`ML_PROBLEM.md`. `MLA-P03` needs from it: the label definition (to find leakage), the
forbidden shortcut list (to build the register), and the slices (to check coverage).
`MLA-P06` needs the pre-registered threshold, unchanged.
