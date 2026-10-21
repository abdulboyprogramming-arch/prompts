# PROMPT 01 — Money Model & Invariants

**Identifier:** PAY-P01
**System:** 03-domains/payments
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A
**Depends on:** none (entry stage)
**Produces:** `.payments/MONEY_MODEL.md`, `.payments/PAYMENT_LEDGER.md`
**Inputs:** REPO_PATH, SUPPORTED_CURRENCIES (optional: PROVIDER_NAME)
**Est. effort:** 30–60 min

---

## 1. Role and mandate

You are the engineer establishing how money is represented and what must always be true in this system. Most money defects are not logic errors; they are representation errors (floats, implicit currencies, truncated roundings) and missing invariants (nothing checks that the sum of the parts equals the whole).

You do not change code here. You produce the model and the invariants that every later change must preserve.

## 2. Objective and scope

**Answer:** how is money stored, computed, and rounded; what states can a payment take; and which invariants must hold across every operation?

Out of scope: idempotency and failure handling (P02), reconciliation (P03).

## 3. Prerequisites and inputs

| Input | Source | If missing |
|-------|--------|------------|
| Schema for money-bearing tables | migrations, ORM models | derive from code and mark `derived` |
| Provider integration code for `{{PROVIDER_NAME}}` and its API version, in `{{REPO_PATH}}` | repository | note the provider and version, since semantics differ |
| Supported currencies and their exponents: `{{SUPPORTED_CURRENCIES}}` | product/owner | list what the code handles and flag the rest |
| Refund, dispute, and partial-capture rules | product/finance owner | record as open questions; do not invent policy |

## 4. Workflow

1. **Inventory every place money appears**: columns, fields, API payloads, event schemas, report queries, exports, and configuration (prices, fees, tax rates). Include the ones that look like integers but are actually money.
2. **Establish the representation per location** and flag every violation:

   | Representation | Verdict |
   |---------------|---------|
   | Integer minor units + explicit currency | Correct; state the exponent per currency |
   | Decimal with fixed scale | Acceptable if scale is documented and consistent |
   | Float/double | Defect — record every instance and the amounts it can corrupt |
   | String | Acceptable only at boundaries; must be parsed exactly once |
   | Integer with implicit currency | Fragile — flag missing currency dimension |

3. **Check currency handling**: is a currency code stored beside every amount, or inferred from context? Are non-2-exponent currencies (JPY 0, KWD 3) handled? Is conversion performed at a stored rate with a recorded timestamp, or recomputed later from a moving rate?
4. **Document the rounding rule and its allocation.** When an amount must be split (tax, fees, instalments, partial refunds), the parts must sum exactly to the whole. State the allocation method (largest remainder, first-item, or explicit fixed order) and whether remainder cents are assigned deterministically.
5. **Map the state machine**: authorised → captured → settled → refunded/partially refunded → disputed → reversed, plus failed/voided and any provider-specific states. For each transition, record what triggers it, what is idempotent, and which states are terminal. Mark any transition that can happen out of order (e.g. a settlement webhook arriving before the capture response).
6. **Write the invariants** as checks that can be run as SQL or tests, for example:
   - the sum of ledger entries for a payment equals its current state amount;
   - captured + refunded ≤ authorised, per currency;
   - no payment is in a terminal state with an open authorisation;
   - refunds never exceed the captured amount net of prior refunds;
   - every payment has exactly one currency and all its entries share it;
   - the count of successful provider captures equals the count of local captured records (checked in P03).
7. **Test the model against the awkward cases**: zero-amount authorisations, 1-cent totals with a 3-way split, JPY, currencies with different exponents in one account, refunds after a partial capture, and timestamps across DST and day boundaries for settlement.
8. **Record open policy questions** rather than deciding them: who may issue a manual refund, what happens on a duplicate webhook, whether authorisations expire.
9. **Write `.payments/MONEY_MODEL.md`:** representation inventory with violations, currency rules, rounding and allocation, state machine with transitions, the invariant list (each written as a checkable statement), awkward-case results, and open questions.
10. **Initialise `.payments/PAYMENT_LEDGER.md`.**

## 5. Decision rules and evidence standard

- **Floating point for money is always a defect**, not a style preference — record it with the affected fields and the maximum error it implies.
- **An amount without a currency is ambiguous data**, even if the product is single-currency today.
- **Every invariant must be expressible as a query or an assertion**, otherwise it is a hope.
- **Do not invent business policy** (fees, refund windows). Record the question and its owner.
- **State machine gaps are findings**: an unreachable terminal state, a transition with no idempotency, or a state that can be entered from two directions.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| All money locations inventoried | schema + API review | columns, payloads, events, reports |
| Representation classified | inspect | every violation flagged |
| Currency dimension checked | schema review | present per amount, or flagged |
| Rounding/allocation rule stated | inspect | parts sum exactly |
| State machine complete | diagram + code cross-check | transitions match code |
| Invariants checkable | sample query per invariant | runs or can be written |
| Awkward cases exercised | calculations shown | results recorded |

## 7. Failure handling

- **Floats found in the data path** → quantify the risk and stop: any change built on a float pipeline must first fix representation, which is `03-domains/database/` work with a migration plan.
- **Currency not stored** → mark the multi-currency capability `unsupported` and record what would be required; do not assume the default.
- **State machine disagrees with provider semantics** → record both and treat the provider as authoritative for captured funds; the mismatch becomes a P02 concern.
- **No ledger, only a mutable balance column** → record it: a mutable balance cannot be audited or reconciled. Recommend an append-only ledger as a design change with its own plan.
- **Policy unknown** (refund authority, expiry) → list as an open question with the owner; later stages must not assume an answer.

## 8. Security and authorisation

Risk class A: read-only. Do not query production payment records beyond schema and aggregate checks; card data (PAN, CVV) must never be read, logged, or included in an artifact. Use aggregated counts and synthetic examples in the model document.

## 9. Completion criteria

- [ ] Every money-bearing location inventoried.
- [ ] Representation classified with violations listed.
- [ ] Currency handling assessed per amount.
- [ ] Rounding and allocation rules documented.
- [ ] State machine mapped with triggers and terminal states.
- [ ] Invariants written as checkable statements.
- [ ] Awkward cases tested with calculations.
- [ ] Open policy questions recorded with owners.

## 10. Deliverables and handover

Artifact: `.payments/MONEY_MODEL.md`.

P02 receives: the state machine, the invariants, and the representation risks — which determine where idempotency and unknown-outcome handling are needed.
