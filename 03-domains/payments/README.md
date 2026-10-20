# Payments & Money Correctness

**Maturity: operational (v1.0.0).** Three stages for code that moves money, where a bug is not a bad user experience but a financial loss, a reconciliation break, or a regulatory finding.

**Entry point:** [`P01-Model/P01-Money-Model-Invariants.md`](P01-Model/P01-Money-Model-Invariants.md)
**Execution mode:** specialised
**Risk class:** A for analysis, **C** for changes to payment flows, **D** for any operation that moves real funds

## Why this system exists

Money code fails differently from other code:

- **It fails silently and asymmetrically.** A retry that double-charges is discovered by the customer, not by monitoring. A refund that never lands is discovered weeks later by finance.
- **It cannot be fixed by a deploy.** Code can be rolled back; a captured payment cannot.
- **The edge cases are the business.** Currency exponents, rounding allocation, partial refunds, chargebacks, currency conversion, and time zones around settlement are not corner cases — they are the product.
- **The provider is a second source of truth**, and the two truths diverge unless something reconciles them.

## Stages

| ID | Stage | Purpose | Produces |
|----|-------|---------|----------|
| PAY-P01 | [Money model & invariants](P01-Model/P01-Money-Model-Invariants.md) | Representation, rounding, states, and the invariants that must always hold | `.payments/MONEY_MODEL.md` |
| PAY-P02 | [Idempotency & unknown outcomes](P02-Idempotency/P02-Idempotency-Failure.md) | Retries, webhooks, timeouts, and the hardest case: you do not know whether it happened | `.payments/FLOW_ANALYSIS.md` |
| PAY-P03 | [Reconciliation & change safety](P03-Reconciliation/P03-Reconciliation-Change-Safety.md) | Prove the books balance, and review money changes without gambling | `.payments/RECONCILIATION.md` |

## The five rules

1. **Store money as integer minor units** with an explicit currency, or as a decimal type with a documented scale. Never as floating point.
2. **Every money-moving operation is idempotent**, keyed by something the caller controls.
3. **An unknown outcome is a state**, not an exception. Design for "we do not know" before you need it.
4. **The provider's ledger and yours must agree**, and something must check daily.
5. **No money-touching change ships without a recorded invariant check and a rollback that does not depend on reversing a captured payment.**

## Boundaries

- Schema changes for money tables: `03-domains/database/` (this system supplies the invariants it must preserve).
- Incident response for a live money bug: `05-scenarios/incident-response/`.
- Fraud and abuse: `02-engineering/security-hardening/`.
- Financial reporting, tax, and accounting policy: the finance owner, not engineering.

## What this system will not do

- Decide tax treatment, revenue recognition, or regulatory obligations.
- Replace a payments provider's SDK guarantees with assumptions.
- Guarantee correctness. It makes invariants explicit, testable, and reconciled.
