# PROMPT 03 — Reconciliation & Change Safety

**Identifier:** PAY-P03
**System:** 03-domains/payments
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** specialised
**Risk class:** C
**Depends on:** PAY-P02
**Produces:** `.payments/RECONCILIATION.md`
**Est. effort:** 45–90 min

---

## 1. Role and mandate

You are the engineer who proves the books balance, and who reviews money-touching changes before they ship. Without reconciliation, the first person to notice a money bug is a customer or an accountant — usually a month later, when the trail is cold.

## 2. Objective and scope

**Produce:** a working reconciliation between your records and the provider's, a drift classification with owners, and a change-safety checklist for every future money change.

Out of scope: accounting policy, tax, and revenue recognition; incident handling for an active money bug (`05-scenarios/incident-response/`).

## 3. Prerequisites and inputs

- `.payments/MONEY_MODEL.md` (invariants), `.payments/FLOW_ANALYSIS.md` (unknown outcomes, stuck states).
- Provider settlement reports or ledger API, with API access and the right scopes.
- Access to your own ledger/payment tables, read-only.

## 4. Workflow

1. **Choose the comparison basis.** Provider settlement/payout reports are the closest thing to truth for captured funds; the provider ledger API is better for per-transaction detail. State which you used and why; they disagree in ways that matter (fees, timing, currency conversion).
2. **Reconcile per transaction, then in aggregate.** Per-transaction comparison finds missing, duplicated, and amount-mismatched records. Aggregate comparison (daily totals per currency) catches what the per-transaction keys miss.
3. **Classify every difference** into a taxonomy — do not stop at "there are 14 mismatches":
   - **timing** (captured today, settled tomorrow) — expected, quantify the window;
   - **missing locally** (provider has it, we do not) — lost webhook or crash gap;
   - **missing at provider** (we recorded it, provider does not) — phantom success, the worst class;
   - **amount mismatch** — rounding, currency conversion, fee handling, partial capture;
   - **duplicate** — double charge or double application;
   - **state mismatch** — refunded locally but not at provider, or the reverse.
4. **Quantify each class** in count and money, per currency, and name the owner for fixing it.
5. **Repair deliberately, and only after classification.** Duplicates require a refund to the customer; missing-locally requires importing the provider record, not re-charging. Never "fix" reconciliation by re-running a charge.
6. **Automate it.** A reconciliation that requires a person to remember is not a control. Specify: frequency (daily at minimum), window (yesterday plus a rolling 7 days to catch late settlements), alert thresholds per class, and where the report is stored.
7. **Reconcile fees and currency explicitly.** Provider fees, currency conversion spreads, and rounding at conversion are the most common source of "small" persistent differences; if they are unexplained, the reconciliation is not complete.
8. **Define the money-change safety checklist** — applied to every future change to payment code:
   - invariant checks still pass, and a test exists for each invariant touched;
   - idempotency key unchanged, or the change documented as a new key namespace;
   - provider API semantics verified against the version in use;
   - failure paths exercised in sandbox (timeout, duplicate webhook, concurrency);
   - rounding and allocation unchanged, or a before/after calculation on real-shaped data;
   - reconciliation impact assessed (will this create a new difference class?);
   - rollback plan that does not require reversing a captured payment;
   - a named reviewer who has read the money model.
9. **Write `.payments/RECONCILIATION.md`:** basis, method, per-class findings with money amounts, repairs, automation design (frequency, window, alerts, storage), fee/currency treatment, and the change-safety checklist.

## 5. Decision rules and evidence standard

- **The provider is authoritative for captured funds; you are authoritative for intent.** A difference is not "the provider's bug" until proven.
- **Never repair by re-charging.** Import, refund, or adjust — each is a different operation with different customer impact.
- **Unexplained small differences are not noise.** They usually accumulate, and they hide the one that matters.
- **Reconciliation must be automated and alerted**, or it will not run during the month it is most needed.
- **A money change without the checklist is a gamble.** No exceptions for "small" changes — rounding bugs are small changes.
- **Quantify in money, per currency.** A count of mismatches hides whether the problem is 3 cents or 3,000 dollars.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Basis stated | inspect | settlement or ledger, with reason |
| Per-transaction and aggregate compared | report | both present |
| Every difference classified | inspect | taxonomy applied |
| Differences quantified per currency | report | counts and amounts |
| No repair by re-charge | repair log | imports/refunds only |
| Reconciliation automated | job config | schedule, window, alerts |
| Fees and FX explained | report | residual stated |
| Checklist defined and usable | inspect | eight items, actionable |

## 7. Failure handling

- **No provider settlement access** → reconcile against the provider API for the same period and state that settlement-level fees are unverified; escalate access as a P1 gap.
- **Large volumes** (millions of transactions) → reconcile by day and by hash of amount+status, and sample per-transaction detail; state the sampling.
- **A difference cannot be classified** → quarantine it with the amount, the transaction ids, and the date; do not close the period as balanced.
- **Duplicate charges confirmed** → this is a customer-impacting incident: route to incident response for refunds and communication, and record the root cause for P02.
- **Reconciliation reveals a systemic gap** (webhooks lost for a period) → the repair is a backfill plan validated on a copy (`03-domains/database/` rules apply), not a loop over production.

## 8. Security and authorisation

Risk class C: read-only provider and database access with the minimum scope. Refunds and adjustments are Category D and require named approval — this prompt specifies them, it does not execute them. Never include card data, full customer records, or provider secrets in the report; use transaction ids and amounts.

## 9. Completion criteria

- [ ] Comparison basis chosen and justified.
- [ ] Per-transaction and aggregate reconciliation performed.
- [ ] All differences classified and quantified per currency.
- [ ] Repairs specified (never by re-charge) with owners.
- [ ] Automation defined: frequency, window, thresholds, storage.
- [ ] Fees and FX treatment explained or flagged.
- [ ] Money-change safety checklist adopted.
- [ ] Period closed as balanced or explicitly unbalanced with reasons.

## 10. Deliverables and handover

Artifact: `.payments/RECONCILIATION.md`.

Handover: duplicate-charge findings → incident response with amounts and affected customers; lost-webhook gaps → P02 for idempotency fixes; invariant violations → P01 model review; the checklist into code review for money paths; the reconciliation job into `04-process/observability-reliability/` so its failure alerts.
