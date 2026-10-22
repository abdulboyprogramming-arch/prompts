# PROMPT 7 — Deployment & Monitoring: design the wrong answer before shipping the right one

**Identifier:** MLA-P07
**System:** 03-domains/data-ml-ai
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** C — changes what production does with predictions
**Depends on:** MLA-P06
**Produces:** `ML_DEPLOYMENT.md`: the serving path, the fallback behaviour, the monitoring plan, the rollback trigger, and the launch checklist
**Inputs:** {{PROJECT_PATH}}, TARGET_ENV (optional: LATENCY_BUDGET, RETRAIN_CADENCE, ONCALL_OWNER)
**Est. effort:** 1–3 days

---

## 1. Role and mandate

You are the deployment stage. A model in production is a system that is wrong some of
the time, at machine speed, with a confidence score attached. Your job is to decide what
happens on the wrong answer before the first right one is served.

## 2. Objective and scope

**Produce:** `ML_DEPLOYMENT.md` containing:

1. **The serving path** — batch, online, embedded or human-in-the-loop, with the latency
   and cost per prediction measured, not estimated.
2. **The fallback behaviour** — what the product does when the model is unavailable,
   uncertain, or out of distribution.
3. **The monitoring plan** — input drift, output distribution, the quality metric where a
   delayed label allows it, and the decision-level impact.
4. **The rollback trigger**, as a number, with who can pull it.
5. **The launch checklist** — what must be true before switching traffic on, and what
   stays true after.

Out of scope: retraining policy beyond its cadence, and any change to the model.

## 3. Prerequisites and inputs

- `ML_EVALUATION.md` from `MLA-P06` (required): verdict, slices, error modes.
- The artefact and its register row from `MLA-P05`.
- `{{PROJECT_PATH}}` — discovered: the serving code, the deployment configuration, and
  the existing feature-flag or traffic-switch mechanism.
- `{{TARGET_ENV}}` (optional) — where it runs. If the repository has one environment,
  say so and note the absence of staging.
- `{{LATENCY_BUDGET}}` (optional) — from `MLA-P01`; the model must fit inside it with
  the feature fetch included.
- `{{RETRAIN_CADENCE}}` (optional) — how often the model can be rebuilt; a cadence the
  team cannot meet is a plan to serve a stale model.
- `{{ONCALL_OWNER}}` (optional) — who is paged when the metrics move.

## 4. Workflow

1. **Measure the serving path end to end**, including feature fetch. A model that
   infers in 20 ms and waits 300 ms for its features has a 320 ms latency, and the
   budget in `MLA-P01` was about the total.
2. **Define the fallback for each failure**: model timeout, feature missing, score
   outside the trained range, and the whole service down. Each needs a defined product
   behaviour, not an exception trace.
3. **Set the confidence threshold from the cost asymmetry**, not from the default 0.5.
   Record the abstention rate it produces, because that is the human workload it creates.
4. **Choose the monitoring signals that move first.** Input drift and score distribution
   move before the label-based metric, which arrives late. Monitor all three and say
   which is the early warning.
5. **Write the rollback trigger as a number**: "if the decision-level metric drops below
   X over Y requests, roll back". Also record who can trigger it and how, because a
   trigger nobody can pull is documentation.
6. **Run the shadow or canary step.** Score live traffic without acting on it, or serve a
   small fraction, and compare the distribution to the evaluation set. Record what you
   saw.
7. **Write the launch checklist** with the pre-conditions and the post-conditions, and
   the date each was observed.

## 5. Decision rules and evidence standard

- **No deployment without a fallback.** A model with no defined failure behaviour is an
  outage waiting for its first out-of-distribution input.
- **A delayed label limits the metric you can monitor.** If labels arrive in 30 days,
  the first real quality signal is 30 days away; plan an interim proxy and say it is a
  proxy.
- **The threshold is a product decision.** Set it with the decision owner, record the
  abstention rate, and revisit it when the workload is measured.
- **Shadow before canary, canary before full.** Each step produces evidence; skipping
  one means the next step carries its risk.

## 6. Verification

- Latency measured end to end including features, against the budget from `MLA-P01`.
- A defined fallback exists for each failure mode listed.
- The confidence threshold is justified and its abstention rate recorded.
- Monitoring covers input drift, score distribution and the delayed quality metric.
- The rollback trigger is numeric, with a named owner and a tested procedure.
- Shadow or canary results are recorded before full traffic.

## 7. Failure handling

- **Latency exceeds the budget** because of feature fetch: fix the feature path or reduce
  the model, and re-measure. Do not raise the budget without the calling system's owner.
- **No labels will arrive** (no feedback loop): record that quality cannot be monitored
  directly, and monitor proxies with an explicit statement that they are proxies.
- **The serving environment has no staging:** use shadow mode as the substitute, record
  the absence, and keep the canary small.
- **A rollback is triggered during launch:** roll back first, diagnose second, and record
  the observation that triggered it in `ML_EVALUATION.md` for the next cycle.

## 8. Security and authorisation

Risk class C: changes production behaviour. No model becomes authoritative without the
fallback and the rollback in place. Do not log raw inputs in production without a stated
retention and a data classification; do not ship a model whose training data the serving
environment is not permitted to derive from.

## 9. Completion criteria

- [ ] Serving path measured end to end against the latency budget.
- [ ] Fallback defined for each failure mode.
- [ ] Threshold justified with its abstention rate.
- [ ] Monitoring for drift, score distribution and delayed quality.
- [ ] Numeric rollback trigger with a named owner and a tested procedure.
- [ ] Shadow or canary evidence recorded.

## 10. Deliverables and handover

`ML_DEPLOYMENT.md` and the serving configuration. The next cycle starts from the
monitoring signals: a drift alert or a quality drop is the input to `MLA-P03` and
`MLA-P05`, not a reason to retrain blindly.

## 11. Regression protection

Before each new artefact, re-run the evaluation on the fixed holdout and compare with the
serving model on the same set. A candidate that is better on average but worse on the
worst slice is a regression for the users in that slice.

## 12. Rollback

Serving points at a versioned artefact, so rollback is repointing, not retraining. Test
the repoint once before launch: an untested rollback is a plan, not a control.
