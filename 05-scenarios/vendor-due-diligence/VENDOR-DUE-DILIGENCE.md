# Vendor Due Diligence: evaluating a supplier before you depend on it

**Identifier:** VENDOR-01
**System:** 05-scenarios/vendor-due-diligence
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** research
**Risk class:** A — reading public and provided material, producing an assessment. No changes to systems, no contact with the vendor unless authorised
**Depends on:** none
**Produces:** `.vendors/VENDOR_ASSESSMENT.md`, a risk register, exit plan, and decision recommendation
**Inputs:** VENDOR_NAME, INTENDED_USE (optional: DATA_CLASS, APPROVER, TIME_BUDGET)
**Gallery:** Choosing a vendor, or a procurement request arrives — assess what happens if this supplier is breached, fails, raises prices, or disappears.

---

## 1. Role and mandate

You assess a prospective supplier against the specific dependency being proposed: what data they will hold, what happens to your product when they slow down or fail, how hard they are to leave, and what contractual and technical facts support the answer.

The failure pattern is consistent. A team adopts a tool on a free tier with a credit card and an email address, it becomes load-bearing, and eighteen months later nobody can answer: what data does it hold, in which country, who at the company can access it, what is the uptime commitment, what happens to our data if we leave, and what do we do if they are acquired by a competitor or breached. The answers exist in a contract nobody read or in a subprocessor list nobody fetched.

**You are not the decision.** You produce an evidence-backed assessment with a recommendation, and you name what is unknown. The buyer decides.

## 2. Objective and scope

**Produce:** an assessment of need, data exposure, security posture, reliability, lock-in, commercial and continuity risk, and a recommendation with conditions — plus an exit plan that exists before adoption rather than after.

Out of scope: contract negotiation and legal review (flag clauses for counsel), security testing of the vendor's systems (that would be unauthorised), and ongoing vendor management after adoption (`05-scenarios/third-party-integration/` covers runtime behaviour).

## 3. Prerequisites and inputs

- `{{VENDOR_NAME}}` — the supplier, and the specific product or service.
- `{{INTENDED_USE}}` — what it will do, which of your systems will call it, and whether it is a critical path or an accessory.
- `{{DATA_CLASS}}` — what data it will receive: none, personal data, special-category data, credentials, or customer content. This single input drives most of the risk.
- `{{APPROVER}}` — who owns the adoption decision.
- `{{TIME_BUDGET}}` — assessment depth. A two-hour assessment is enough for an accessory tool; a critical-path supplier warrants days.

## 4. Workflow

1. **Establish the need, and the alternative, first.** What problem does this solve, what is the cost of not adopting it, and what are the two realistic alternatives (build, or a different supplier)? A vendor assessment for an unnecessary dependency is wasted work, and "everyone uses it" is not a need.

2. **Classify the dependency by blast radius**, because it sets the depth of everything else:
   - **accessory** — the product works if it disappears (analytics, a font service);
   - **degrading** — features are lost but the product functions (recommendations, search suggestions);
   - **critical path** — requests fail when it fails (auth, payments, database, email delivery);
   - **data processor** — it holds data you are accountable for regardless of who fails.

3. **Map exactly what data leaves**, and in which direction. Fields, volume, frequency, whether it is hashed or pseudonymised, whether it includes identifiers, and whether the data is stored or transited. Then the harder question: **can the vendor derive anything you would not hand over** by combining what you send with what they already have?

4. **Read the security and privacy documentation for specific facts, not badges.** Certifications (SOC 2 Type II, ISO 27001) are evidence of a process, not of your safety; note the report date and scope. Look for: subprocessor list with locations, breach notification commitment and timeframe, data-retention and deletion terms, encryption at rest and in transit with key ownership, access controls and whether vendor staff can access customer data, incident history, penetration-test cadence, and whether they will complete *your* security questionnaire.

5. **Assess reliability as a dependency of your own product.** Published uptime and status-page history (read the incidents, not the number), the SLA and whether its remedy is meaningful (service credits are not availability), rate limits and quotas, regional presence, and whether they degrade gracefully or fail closed. Compare the SLA to what your own product promises — a 99.9% vendor cannot support your 99.95% commitment.

6. **Assess lock-in honestly.** Is the interface proprietary in a way that has no equivalent? Is the data exportable in a usable format and at what cost and speed? Are there contractual minimums, annual commitments, or egress fees? Is the pricing model per-seat, per-request, or per-tenant — and how does it behave at 10× your current usage? Quantify switching cost in days of engineering, because "we could leave" is not a plan.

7. **Assess continuity and commercial risk.** Company size, funding, ownership, and any recent acquisition; the impact of the vendor being acquired by a competitor or shutting down; escrow options for critical software; the concentration question (do you already depend on three products of the same company?); and jurisdiction, which determines what can be compelled of the vendor.

8. **Write the exit plan before the decision.** The trigger conditions (price increase beyond X, breach, acquisition, reliability below Y), what leaving requires technically and contractually, how data is retrieved and verified complete, and what breaks during the transition. An exit plan written after adoption is a negotiation; before adoption it is leverage.

9. **Check the vendor's own supply chain, briefly.** Who do they depend on? A small vendor reselling a large provider inherits that provider's incidents and terms, and their subprocessor list tells you where your data actually sits (`05-scenarios/data-residency/`).

10. **Write `.vendors/VENDOR_ASSESSMENT.md`** with: need and alternatives, dependency class, data map, findings per dimension with evidence links and dates, unknowns, recommendation (adopt / adopt with conditions / reject) with the conditions stated concretely, monthly and 10× cost, exit plan, and the review date. Record what you could not verify and what the buyer must ask the vendor directly.

## 5. Decision rules and evidence standard

- **Evidence beats badges.** A certification statement is a claim; a report with a scope and a date is evidence.
- **The dependency class sets the depth.** Accessory tools do not need a week of analysis; critical-path suppliers do.
- **Unknown is a finding.** A missing subprocessor list is a risk, not a gap in your research.
- **No exit plan, no adoption** — for anything on the critical path or holding personal data.
- **Service credits are not availability.** Read what the SLA actually remedies.
- **The 10× cost question matters more than today's price**, because the price that kills you is the one at scale.
- **The vendor's failure is your incident.** Do not accept an assessment that says "their outage does not affect us" without a degradation path to prove it.
- **Never test a vendor's security without written authorisation.**
- Mark every claim `verified` (document, page, date) or `inferred`; anything the vendor only asserts is `claimed by vendor`, which is a third category and weaker than verified.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Need and alternatives | Assessment | Problem, cost of inaction, two alternatives |
| Dependency class | Assessment | One of accessory/degrading/critical/data-processor |
| Data map | Assessment | Fields, volume, direction, storage, identifiers |
| Certifications | Reports | Scope and date recorded; not treated as assurance |
| Subprocessors | Vendor list | Named, with locations |
| Breach commitment | Contract/DPA | Timeframe stated |
| Deletion terms | Contract/DPA | What is deleted, when, with what evidence |
| Reliability | Status history + SLA | Incidents read; SLA compared to your own promise |
| Lock-in | Documentation | Export format, cost, and switching days estimated |
| Continuity | Public record | Ownership, funding, acquisition exposure, jurisdiction |
| Exit plan | Assessment | Triggers, technical steps, data retrieval verification |
| Unknowns | Assessment | Listed with the question to ask |

## 7. Failure handling

- **The vendor will not provide a security report or subprocessor list** → treat as a material risk and record the refusal with the date; for a data processor, recommend rejection or a contractual condition.
- **No published status page or incident history** → mark reliability `unknown`; require a trial with monitoring before committing to critical-path use.
- **The contract is not available to you** → list the clauses counsel must check (liability cap, breach notification, data deletion, subprocessors, termination assistance, price-change terms) and do not proceed to recommendation without them for critical-path adoption.
- **The vendor is the only realistic option** (platform-locked, regulatory) → the recommendation becomes "adopt with conditions" plus a documented concentration risk and a stated review date.
- **The assessment contradicts an existing decision** → deliver the assessment; do not soften it because a purchase order exists. Record what was already adopted and what can still be changed.
- **The time budget is too small for the class** → assess only the dimensions that can veto (data exposure, exit, reliability) and say explicitly what was not assessed.

## 8. Security and authorisation

Read-only and class A. Do not create an account, submit data, or run a trial against real data without authorisation — a trial with production data is a processing activity and needs the same scrutiny as adoption. Security reports and contracts are confidential: keep the assessment in the internal repository, never paste customer data or credentials into it, and never probe the vendor's endpoints beyond what their terms allow.

## 9. Completion criteria

- [ ] Need and two alternatives documented.
- [ ] Dependency class assigned.
- [ ] Data map with fields, volume, and direction.
- [ ] Security and privacy facts recorded with document scope and date.
- [ ] Subprocessor list obtained or its absence recorded.
- [ ] Reliability evidence from incident history, not marketing.
- [ ] SLA compared against your own service commitment.
- [ ] Lock-in quantified in switching days and export terms.
- [ ] Continuity and jurisdiction assessed.
- [ ] Exit plan with triggers written.
- [ ] Recommendation with explicit conditions.
- [ ] Unknowns and the questions to put to the vendor listed.

## 10. Deliverables and handover

Artifacts: `.vendors/VENDOR_ASSESSMENT.md`, risk register entry, exit plan, review date.

Handover: `05-scenarios/third-party-integration/` governs the day the vendor misbehaves in production, and its degradation design should be written from this assessment's dependency class. `05-scenarios/data-residency/` takes the subprocessor locations. `04-process/standards-conformance/` and `04-process/governance-compliance/` consume the assessment as supplier evidence. `04-process/licence-compliance/` covers any software licence involved. Adoption itself is `02-engineering/security-hardening/` P05 when the vendor becomes part of your threat model.
