# PROMPT 03 — SLOs and Alerting

**Identifier:** OBS-P03
**System:** 04-process/observability-reliability
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** B
**Depends on:** OBS-P02
**Produces:** `SLOS.md`, alert rule definitions
**Est. effort:** 1–2 hours

---

## 1. Role and mandate

You are the SRE defining what "reliable enough" means for this system and building the alert set that enforces it without exhausting the humans who respond. You write objectives and rules; you do not page anyone or change production alerting without authorisation.

## 2. Objective and scope

**Produce** a small set of user-centred SLIs/SLOs with error budgets, and alert rules that fire on budget burn and hard failure — not on causes.

Out of scope: dashboards for exploration (P02/P04), incident response procedure (P04), infrastructure scaling.

## 3. Prerequisites and inputs

- `SIGNALS.md` (available metric names and business events).
- User expectations or historical performance if available.
- Human constraints: who is on call, working hours, escalation path.

## 4. Workflow

1. **Define SLIs per critical journey**, expressed from the user's perspective: availability (successful responses / valid requests), latency (proportion under threshold), correctness (e.g. orders whose state matches payment), freshness (data lag), durability where relevant.
2. **Set SLO targets deliberately.** If history exists, start slightly below current performance with a stated improvement path; do not set a target that is already being missed. Typical web targets: 99.9% availability monthly, p95 latency under a user-perceptible threshold. Record the rationale per objective.
3. **Compute error budgets** and state what the budget buys: how much unreliability is acceptable before feature work pauses.
4. **Design alerts in two classes:**
   - **Symptom/page alerts:** high error rate, severe latency, availability loss, correctness failure (business event anomalies), saturation that will imminently cause failure. These page.
   - **Ticket/warning alerts:** elevated burn rate on a multi-hour window, disk/infra thresholds, certificate expiry, backup failure, queue backlog growth. These do not wake anyone.
5. **Use burn-rate alerting for SLOs.** Multi-window (fast burn for pages, slow burn for tickets), with thresholds tied to the budget. Avoid static percentage thresholds that ignore traffic volume.
6. **For each alert define:** name, signal/query, threshold and window, severity, owner, runbook link, and the expected first action. If you cannot name the first action, the alert is not ready.
7. **Eliminate noise.** Review existing alerts: duplicates, causal alerts with no user symptom, alerts nobody acted on in 90 days. Propose deletions explicitly.
8. **Validate the queries** against the metric names from P02 (syntax-check where tooling exists; otherwise review against the schema). A rule referencing a nonexistent metric is worse than no rule.
9. **Write `SLOS.md`:** SLI definitions, SLOs with rationale, error budgets, alert table, burn-rate config, noise-reduction proposals, escalation and routing, and what is deliberately not alerted.
10. **Update the ledger.**

## 5. Decision rules and evidence standard

- **Alert on what users feel.** CPU at 90% with normal latency is not a page.
- **Every page needs an action and an owner.** No owner → route to a team channel as a ticket.
- **Fewer, better alerts.** Target: fewer than ten pages per week for a typical service; if the design exceeds that, the thresholds or signals are wrong.
- **SLOs are commitments, not observations.** Do not set 99.99% for a system with no redundancy and one database.
- **Do not invent metric names.** Validate against P02's inventory; unknown names are marked `unvalidated`.
- **Alert rules are code**: versioned, reviewed, and reversible. State the rollback (previous rule set).

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Every SLI has a signal | cross-check with P02 | exists |
| Targets justified | inspect | rationale per SLO |
| Every alert has action + owner + runbook | inspect table | none missing |
| Queries reference real metrics | schema/tooling check | all valid or marked unvalidated |
| Burn-rate windows consistent | inspect | fast/slow windows align with budget |
| Noise proposals listed | inspect | explicit deletions |
| Rollback defined | inspect | previous rules restorable |

## 7. Failure handling

- **No historical data** → set provisional targets, mark `provisional`, and define the review date (two weeks of data) before treating them as commitments.
- **No tracing/metrics for an SLI** → either instrument (return to P02) or substitute the closest proxy and record the inaccuracy.
- **Existing paging load already unsustainable** → prioritise deletion over addition; propose a noise budget and where to route non-urgent signals.
- **No on-call rotation exists** → define business-hours alerting first and mark out-of-hours as a gap requiring a management decision.

## 8. Security and authorisation

Risk class B: repositories of alert configuration and documents. Do not push rules to a production monitoring system without explicit authorisation; provide the rule files and the change procedure.

## 9. Completion criteria

- [ ] SLIs defined for each critical journey.
- [ ] SLOs with rationale and error budgets.
- [ ] Page vs ticket classification for every alert.
- [ ] Each alert has signal, threshold, owner, action, runbook.
- [ ] Queries validated or marked unvalidated.
- [ ] Noise-reduction proposals with explicit deletions.
- [ ] Rollback procedure stated.

## 10. Deliverables and handover

Artifacts: `SLOS.md`, alert rule files.

P04 receives: the alert inventory and owners, so runbooks can be written for exactly the alerts that can fire.
