# Usage Metering and Entitlements: count what you bill, enforce what you sold

**Identifier:** METER-01
**System:** 05-scenarios/usage-metering
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** audit-remediation
**Risk class:** A for analysis; B for code; **C** for changing what customers are charged
**Depends on:** none
**Produces:** `.metering/METERING_MODEL.md`, entitlement matrix, reconciliation report, backfill plan
**Inputs:** METERED_UNITS, PLAN_MODEL (optional: BILLING_PERIOD, APPROVER)
**Gallery:** You charge by usage, seat, or request — and the number that reaches the invoice has to be reproducible, explainable, and correct across plan changes, outages, and retries.

---

## 1. Role and mandate

You make the number on the invoice **defensible**.

Metering fails differently from every other system in this library: there is no error page. Requests fail to be counted, are counted twice after a retry, or are counted against the wrong account when a user changes plan mid-period. The first person to notice is a customer, in a finance thread, with a spreadsheet, and your answer has to be better than "the system says so".

The two mechanisms are usually conflated and must be separated:

- **Metering** records what happened: an immutable, idempotent stream of usage events.
- **Entitlements and enforcement** decide what may happen: quotas, limits, and what the product does when a limit is reached.

A system that enforces by decrementing a counter it also bills from has permanently entangled its accounting with its access control, and neither can be fixed independently afterwards.

## 2. Objective and scope

**Produce:** the billable unit definition with its exclusions, an idempotent event model, aggregation rules for a billing period, plan-change and proration rules, the entitlement matrix and its enforcement behaviour, a reconciliation method that compares metered usage to what the product actually served, and a backfill/correction procedure.

Out of scope: invoice rendering, tax, payment collection, and revenue recognition (`03-domains/payments/`), and infrastructure spend (`03-domains/cost-engineering/`).

## 3. Prerequisites and inputs

- `{{METERED_UNITS}}` — what is counted: requests, API calls, tokens, seats, storage GB-months, active users, compute seconds, documents processed. One per billing line, defined precisely.
- `{{PLAN_MODEL}}` — the plans and how they bound usage: included allowances, overage pricing, hard caps, tiered bands, or committed spend.
- `{{BILLING_PERIOD}}` — the period boundary and its timezone. Almost every dispute about a bill is a dispute about which period an event belonged to.
- `{{APPROVER}}` — required before any change that alters historical charges or credits a customer.

## 4. Workflow

1. **Define the billable unit unambiguously, including what does not count.** "An API request" is not a definition: is a failed request counted? a retried one? a cached one? a `HEAD`? one streaming response that lasts five minutes? A retried request that succeeds on the third attempt is one unit if you meter at the edge by idempotency key, and three if you count at the origin. Write the rule, decide where it is enforced, and make the metering point match the definition.

2. **Put metering at exactly one point per unit**, chosen for what it can see and cannot miss. Options: the edge (sees everything, may count retries), the application (sees intent, may miss async work), or the data store (sees the effect, cannot see attempts). One point, documented, with the known blind spot written next to it.

3. **Model the event as immutable and idempotent.** Each metered event carries: a deterministic key (tenant, unit, operation, idempotency token), a timestamp in UTC, a quantity, and the source. Ingestion must be idempotent on that key — a retried delivery must not double-bill. Never mutate an event; corrections are new events with a reason, because a billed quantity whose history can be edited cannot be audited.

4. **Decide what happens when the meter is unavailable.** This is the failure that reaches customers in both directions:
   - *fail open* — the request is served and not counted: you give away usage and the customer's bill is lower than reality;
   - *fail closed* — the request is refused because the counter is down: an outage caused by a billing subsystem.
   Record the choice per unit, the buffer (local queue, dead-letter, replay), and how the gap is reconciled afterwards. Silence is not an option: an unlogged drop is revenue loss nobody will ever find.

5. **Handle the period boundaries explicitly.** Events near midnight on the period boundary belong to exactly one period; late-arriving events belong to the period they occurred in, not the one they arrived in, unless you decide otherwise and say so. State the cut-off and the grace window (usually a few hours to days) after which late events are carried to the next period or credited. Use the account's billing timezone if the plan specifies one — otherwise use UTC and say it.

6. **Handle plan changes, upgrades, and cancellation.** Mid-period upgrade: prorate, or apply the new allowance only to the remainder, or start a new period? Downgrade with usage already above the new cap: does the overage apply, or is the cap applied at renewal? Trial to paid: does trial usage count against the first period? Each rule must be stated, implemented, and testable, because this is where disputes concentrate. Include seat-based models where adding a user mid-period has the same shape.

7. **Separate enforcement from accounting.** Entitlements read from the plan and the current usage; enforcement decides what the product does at a limit — throttle, return a specific error, queue, degrade, or allow overage and bill. That decision is a product decision and must be written per unit. **Enforcement must not decrement the billed quantity.** If the counter that gates access is also the counter you invoice from, an enforcement bug becomes a billing incident and a billing bug becomes an outage.

8. **Build the entitlement matrix**: plan × unit × included allowance × overage behaviour × hard limit × user-visible message. Then check the awkward combinations: two units on one plan, a tenant with multiple accounts, a grandfathered plan with a limit that no longer exists in the product, an enterprise contract with negotiated allowances that the code has never modelled.

9. **Reconcile metered usage against reality, monthly and automatically.** For each unit: compare metered quantity to an independent source — gateway logs, storage measurements, database row counts, provider-side metrics — and report the delta with a tolerance. A meter nobody reconciles drifts, and drift is either revenue loss or overbilling. Store the reconciliation output with the invoice.

10. **Plan the corrections.** Underbilling found during reconciliation: credit or invoice forward, with the customer informed. Overbilling: credit, with the reason. A dispute from a customer: reconstruct the exact events for their account and period, show the count, and compare against the independent source. That reconstruction must be possible from stored events alone — if it needs a developer to query production, you cannot answer disputes at scale.

11. **Test the meter like money**, because it is. Required tests: duplicate delivery does not double-count; an event with a clock skew lands in the correct period; a tenant switching plans mid-period produces the specified split; a late event is handled per the stated rule; enforcement at the cap does not alter the billed quantity; a fail-open gap is detectable in reconciliation. Write `.metering/METERING_MODEL.md` with the unit definitions, event schema, blind spots, boundary and plan-change rules, entitlement matrix, reconciliation method, and correction procedure.

## 5. Decision rules and evidence standard

- **The billable unit is a contract**, not a log line. Define exclusions first.
- **Meter at one point and name its blind spot.**
- **Events are immutable and idempotent.** Corrections are new events with reasons.
- **Enforcement must not decrement the billed counter.** Accounting and access control are separate systems that share data, not state.
- **Fail-open and fail-closed are both decisions; unlogged drops are a defect.**
- **The period boundary is where disputes live.** State the timezone, the cut-off, and the late-event rule.
- **If you cannot reconstruct the exact billed events for one account and one period, you cannot answer a dispute.**
- **A meter that is never reconciled is a meter that drifts.** Reconcile against an independent source.
- Mark each claim `verified` (query, log, or test) or `inferred`.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Unit defined with exclusions | Model | Included and excluded cases enumerated |
| Single metering point | Architecture | One point per unit; blind spot documented |
| Event schema | Stored events | Key, timestamp, quantity, source, tenant |
| Idempotent ingestion | Duplicate delivery test | No double count |
| Meter-unavailable behaviour | Code path | Fail-open/closed chosen and logged |
| Period boundary | Boundary test | Events land in exactly one period |
| Late events | Injected late event | Handled per the stated rule |
| Plan change | Test | Proration or allowance rule matches the spec |
| Entitlement matrix | Table | Every plan × unit combination has enforcement behaviour |
| Enforcement isolation | Code review | Billed quantity unaffected by enforcement |
| Reconciliation | Monthly report | Delta within tolerance, with the independent source named |
| Dispute reconstruction | Manual run | One account-period rebuilt from stored events |
| Failure-path tests | Suite | All seven listed cases pass |

## 7. Failure handling

- **Metering was added later and history is incomplete** → define a start date, backfill from the best available source, and label backfilled quantities; never present a reconstruction as a measurement.
- **Two units disagree** (seats billed, requests metered, and the customer expects one) → this is a product contract question; record the discrepancy and route it rather than picking a number.
- **An outage caused a gap** → reconcile, credit or invoice forward with notification, and record the gap in the model. Do not silently absorb it; the next one will be larger.
- **A customer disputes a bill** → reconstruct from events, compare to the independent source, answer with the numbers. If the two disagree, the independent source wins until proven otherwise.
- **Enforcement is bypassed by a legacy endpoint** → treat as a product gap with a revenue estimate, not a code bug to hotfix quietly.
- **The team wants to change a historical bill** → that is a credit, not an edit. Route to `{{APPROVER}}`.

## 8. Security and authorisation

Analysis is class A. Metering code is B. Anything that changes what a customer is charged — rates, allowances, credits, backfills that alter invoices — is **C** and requires `{{APPROVER}}`, a written rationale, and a way to reverse it. Metering events are commercially sensitive and often contain identifiers: restrict access, retain per policy (`04-process/privacy-requests/`), and never log full request payloads to count a unit.

## 9. Completion criteria

- [ ] Billable unit defined with explicit exclusions.
- [ ] One metering point per unit, blind spot documented.
- [ ] Event schema immutable, keyed, idempotent.
- [ ] Meter-unavailable behaviour chosen and logged.
- [ ] Period boundary, timezone, cut-off, and late-event rule stated.
- [ ] Plan change, upgrade, downgrade, trial, and cancellation rules written.
- [ ] Entitlement matrix complete, including grandfathered plans.
- [ ] Enforcement separated from accounting, verified in code.
- [ ] Reconciliation against an independent source, monthly, stored with the invoice.
- [ ] Dispute reconstruction demonstrated for one account-period.
- [ ] Seven failure-path tests passing.

## 10. Deliverables and handover

Artifacts: `.metering/METERING_MODEL.md`, entitlement matrix, reconciliation report template, test suite.

Handover: `03-domains/payments/` owns money movement, idempotency against the provider, and reconciliation of charges once the quantity is agreed — this prompt produces the quantity, not the transaction. `05-scenarios/capacity-planning/` shares the quota data from the other direction (internal limits versus customer entitlements). `05-scenarios/abuse-prevention/` sets the limits that protect the service; entitlements set the ones that protect the contract, and they must not contradict each other. `04-process/governance-compliance/` needs the reconciliation evidence for revenue controls.
