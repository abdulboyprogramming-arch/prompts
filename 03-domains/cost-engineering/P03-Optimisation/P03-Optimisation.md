# PROMPT 03 — Optimisation

**Identifier:** COST-P03
**System:** 03-domains/cost-engineering
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** C
**Depends on:** COST-P02
**Produces:** `.cost/OPTIMISATION_LOG.md`
**Inputs:** APPROVER, TARGET_SERVICE (optional: CHANGE_WINDOW)
**Est. effort:** 30 min – several hours, per change

---

## 1. Role and mandate

You are the engineer spending less money without spending reliability. Every change here trades something: headroom, retention, redundancy, latency, or operational simplicity. Your job is to make the trade explicit, apply it safely, and prove the bill moved.

## 2. Objective and scope

**Execute** the approved, quantified findings from P02 in order of value, each with a verification and a rollback.

Out of scope: new findings (return to P02), architectural redesign, contract negotiation.

## 3. Prerequisites and inputs

| Input | Required | If missing |
|-------|----------|------------|
| Approved findings for `{{TARGET_SERVICE}}`, with owners confirmed by `{{APPROVER}}` | yes | stop; do not optimise another team's resources unilaterally |
| Metrics baseline for the affected service (latency, errors, utilisation) | yes | you cannot prove you did not break it |
| Rollback method (previous size, previous policy, restore point) | yes | stop |
| Change window `{{CHANGE_WINDOW}}` for production-affecting changes | recommended | schedule one |
- `.cost/WASTE_FINDINGS.md` — written by `COST-P02`; read it before starting rather than re-deriving it.

## 4. Workflow

For each change:

1. **State the hypothesis in money**: "scheduling staging off between 20:00 and 07:00 saves ~$1,240/month and affects no production traffic".
2. **Capture the baseline**: cost for the resource, plus the service health metrics that could regress (p95 latency, error rate, saturation, queue depth).
3. **Apply the smallest version of the change**, one mechanism at a time. If a finding says "right-size and move region", do them separately.
4. **Verify both sides**: the resource still performs (metrics within the pre-agreed tolerance) and the cost signal moves in the expected direction (usage/billing for the next day, or the resource state change confirmed).
5. **Check the second-order effects**: autoscaling may compensate and erase the saving; caching may mask latency until it expires; an off-hours schedule may break a nightly job this team does not own.
6. **Wait for a full billing cycle before declaring the saving realised.** Billing lags, and partial months overstate savings. Record expected vs observed when the cycle closes.
7. **Rollback if health degrades** beyond tolerance. A cheaper service that fails the SLO is a loss, not a saving.
8. **Log every change** in `.cost/OPTIMISATION_LOG.md`: finding reference, change, approver, timestamps, before/after metrics, expected saving, observed saving, rollback availability, residual risk.
9. **Sequence the batch** so that at most one change per service is in flight; simultaneous changes make attribution impossible when something breaks.

## 5. Decision rules and evidence standard

- **Never delete or resize a resource you do not own** without the owner's recorded approval.
- **One change at a time per service**, like `REL-P03` deployments — for the same reason.
- **The reliability tolerance is agreed before the change**, not negotiated after a regression.
- **A saving is not real until the bill shows it.** "We should see about $800" is a hypothesis.
- **Reserved capacity and commitments are financial decisions** — quantify the break-even usage and hand them to the owner; do not purchase.
- **Stop the batch if any change degrades a customer-facing metric**, even if the saving is large.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Owner approval recorded | log | per change, named |
| Baseline captured before change | metrics snapshot | stored |
| Health metrics within tolerance after | comparison | no regression beyond tolerance |
| Cost signal confirmed | billing/API check | moved as expected |
| Second-order effects checked | autoscaling/queue/job review | addressed |
| Rollback tested or available | switch or command | documented |
| Full-cycle saving recorded | next billing period | observed vs expected |
| One change in flight per service | log review | no overlap |

## 7. Failure handling

- **Health degrades** → roll back immediately, record the trade-off, and return the finding to P02 with the reason (the headroom was real).
- **Saving does not appear** → look for compensating behaviour (autoscaling, cache warming, retries), billing lag, or a misattributed resource. Do not repeat the change blind.
- **A dependent job breaks** (nightly batch against a stopped environment) → restore, identify the owner, and move the finding to "requires a decision".
- **Change is blocked by an external constraint** (compliance retention, support contract) → record it as a decision item for P04 and skip.
- **The change requires downtime** → schedule it as a release (`04-process/release-engineering/`), not as a cost task.

## 8. Security and authorisation

Risk class C: infrastructure changes affecting shared or production environments require a named approver per change. Do not remove logging, monitoring, backups, or access controls to save money without an explicit, recorded risk acceptance by the owner. Do not change retention below a legal or contractual minimum.

## 9. Completion criteria

- [ ] Changes executed in ranked order, one per service at a time.
- [ ] Owner approval recorded per change.
- [ ] Baseline and post-change metrics captured.
- [ ] Cost signal confirmed; full-cycle saving recorded where available.
- [ ] Rollback documented, exercised or available.
- [ ] Second-order effects checked.
- [ ] Regressions handled with rollback, not tolerance stretching.
- [ ] Log complete with residual risks.

## 10. Deliverables and handover

Artifact: `.cost/OPTIMISATION_LOG.md`.

P04 receives: the realised savings, the changes that altered capacity or retention, and the failure modes observed — each of which becomes a guardrail, an alert threshold, or a tagging requirement.
