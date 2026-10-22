# PROMPT 01 — Cost Visibility & Attribution

**Identifier:** COST-P01
**System:** 03-domains/cost-engineering
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A
**Depends on:** none (entry stage)
**Produces:** `.cost/COST_MAP.md`, `.cost/COST_LEDGER.md`
**Inputs:** CLOUD_ACCOUNT, BILLING_EXPORT_PATH
**Est. effort:** 30–60 min

---

## 1. Role and mandate

You are the engineer making spend legible. Until cost is attributed to a service, team, and environment, every optimisation conversation is anecdote. You do not optimise anything here; you establish what the bill actually consists of and which part cannot be explained.

## 2. Objective and scope

**Answer:** what did we spend, on what, attributed to whom, and what fraction is unattributable?

Out of scope: changing resources, choosing savings (P02).

## 3. Prerequisites and inputs

| Input | Source | If missing |
|-------|--------|------------|
| Billing export for `{{CLOUD_ACCOUNT}}` at resource granularity (daily, line-item), at `{{BILLING_EXPORT_PATH}}` | cloud console/billing API | request it; invoice-level totals cannot support diagnosis |
| Tag/label conventions | infrastructure-as-code, docs | infer from resource names and state that it is inferred |
| Service catalogue or repository list | repository/org | derive from infrastructure definitions |
| Traffic/usage data (requests, storage volumes, data transfer) | metrics | unit economics cannot be computed; record as a gap |

## 4. Workflow

1. **Establish the period and the total.** Use complete billing months; state the currency and whether tax/credits/support are included. A total that mixes committed-use discounts with list prices is not comparable month to month.
2. **Break down by the dimensions that drive decisions**: service (compute, storage, network, managed services), environment (prod/staging/dev), team or product, and cost type (fixed vs variable, recurring vs one-off).
3. **Attribute, and measure the unattributed remainder.** Tag-based attribution is usually partial; classify the rest by naming convention, IaC ownership, or known topology. Report the percentage that is genuinely unattributable — that number is the headline finding, because it is what prevents accountability.
4. **Find the top ten line items.** Cost is almost always concentrated: a handful of resources usually account for the majority. List them with service, environment, owner (or unknown), and monthly amount.
5. **Identify the largest *variable* costs and their drivers** — data transfer, request counts, storage growth, log ingestion, database read units. Fixed costs can be right-sized; variable costs are controlled by engineering behaviour.
6. **Compare to a baseline**: last month, same month last year (seasonality), and plan/budget if one exists. A rising trend that tracks traffic is healthy; one that tracks user count growing 5% while cost grows 60% is the finding.
7. **Check the boring but large items explicitly**: log/metric retention, snapshot and image accumulation, idle non-production environments, unattached volumes and elastic IPs, egress between regions or to the internet, and licensing per-seat for tools nobody uses.
8. **State the limits**: what the billing export does not cover (support plans, marketplace subscriptions, SaaS billed separately), and which numbers are estimates.
9. **Write `.cost/COST_MAP.md`:** period and total, breakdown by dimension, attribution percentage, top ten items, variable cost drivers, trend comparison, unattributed inventory, and coverage limits.
10. **Initialise `.cost/COST_LEDGER.md`.**

## 5. Decision rules and evidence standard

- **Numbers must come from billing data**, never from pricing-page arithmetic on guessed usage. If you estimate, label it `estimated` and show the inputs.
- **Report unattributed spend as a first-class figure**, not a footnote.
- **Monthly normalisation**: convert annual commitments and one-off charges to a monthly equivalent, stated.
- **Do not treat "dev" as free by definition** — non-production frequently accounts for a third of spend through forgotten environments.
- **Currency, tax, and discount treatment must be stated** or the numbers are not comparable.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Total reconciles to the invoice | sum components | within stated tolerance |
| Period and inclusions stated | inspect | complete months, credits noted |
| Attribution percentage computed | tagged vs total | number recorded |
| Top ten enumerated | billing export | amounts and owners |
| Variable drivers identified | usage data | cost per unit stated |
| Trend compared | prior periods | explained or flagged |
| Coverage limits listed | inspect | non-billing spend named |

## 7. Failure handling

- **No resource-level billing export** → work from the invoice's service breakdown, mark attribution as unavailable, and make "enable billing export with tags" the first recommendation.
- **Tags absent or inconsistent** → attribute by naming convention and IaC resource addresses, quantify the unattributable remainder, and recommend a tagging standard (P04).
- **Multiple accounts/providers** → produce one map per account and a combined total with the split stated; cross-account transfer costs are a common hidden item.
- **Figures look implausible** (a service costing more than its usage implies) → chase the mechanism: orphaned resources, duplicate environments, misconfigured replication, or a runaway job. This is often the largest single finding.
- **Only a partial period is available** → annualise with an explicit method, and mark it.

## 8. Security and authorisation

Risk class A: read-only billing and usage data. Billing exports can contain account identifiers and resource names — treat them as confidential, do not commit raw exports, and redact account IDs in artifacts.

## 9. Completion criteria

- [ ] Period, currency, and inclusions stated.
- [ ] Total reconciles to the invoice.
- [ ] Breakdown by service, environment, owner, and cost type.
- [ ] Attribution percentage and unattributed inventory.
- [ ] Top ten line items with amounts.
- [ ] Variable cost drivers with per-unit costs.
- [ ] Trend compared against prior periods.
- [ ] Coverage limits recorded.
- [ ] Ledger initialised.

## 10. Deliverables and handover

Artifact: `.cost/COST_MAP.md`.

P02 receives: the top items, the variable drivers, the unattributed remainder, and the trend anomalies — which determine where diagnosis effort goes first.
