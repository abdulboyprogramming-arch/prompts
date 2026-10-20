# PROMPT 03 — Gap Remediation & Readiness Decision

**Identifier:** GOV-P03
**System:** 04-process/governance-compliance
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** A
**Depends on:** GOV-P02
**Produces:** `.governance/READINESS.md`
**Inputs:** AUDIT_DATE, APPROVER
**Est. effort:** 30–60 min

---

## 1. Role and mandate

You are advising the accountable owner. Your output is a decision, not a recommendation to "improve security": which controls are evidenced, which gaps are being remediated and by when, which risks are accepted and by whom, and what cannot be claimed today.

**You do not certify readiness.** You make it impossible to be vague about it.

## 2. Objective and scope

**Produce:** a remediation plan ordered by consequence, a risk-acceptance register with named owners, and a readiness statement per claim that an auditor or customer question can be answered against.

Out of scope: performing the remediation (route to the owning system), legal attestation, contractual negotiation.

## 3. Prerequisites and inputs

- `.governance/CONTROL_MAP.md` (what is claimed and what exists).
- `.governance/EVIDENCE.md` (what operated, with exception rates).
- The deadline driving this work (`{{AUDIT_DATE}}`), and the accountable owner's identity (`{{APPROVER}}`).

## 4. Workflow

1. **Classify each gap by consequence, not by framework clause:**
   - **Misrepresentation risk** — a claim is made that evidence contradicts (highest: this is a contractual and reputational exposure, not a technical one).
   - **Control absent on a critical path** — no approval on production changes, no restore test, unowned production credentials.
   - **Control operating with exceptions** — quantify the rate; decide whether it is acceptable.
   - **Observability gap** — the control may operate but cannot be evidenced; remediation is instrumentation.
   - **Documentation gap** — the control operates, the description is stale.
2. **Remediate by consequence**: fix misrepresentation first (stop claiming, or make it true), then critical absences, then exceptions, then observability, then documentation.
3. **For each gap choose one of four responses, in writing:**
   - **Fix** — with an owner, a date, and the evidence that will prove it afterwards;
   - **Instrument** — the control is believed to operate but cannot be shown; add logging/records, then test;
   - **Accept** — with a named risk owner, a rationale, a compensating control, and a review date;
   - **Stop claiming** — remove the claim from policy, questionnaires, and marketing until it is true.
4. **Prefer "fix" over "accept" on controls where the absence is itself the risk** (unowned production credentials, no restore test, direct pushes to production). Acceptance of those needs an executive owner, not an engineering one.
5. **Estimate remediation effort honestly** and sequence against the deadline: what must be true by the audit date, what can follow, and what will not be ready (state it before someone else discovers it).
6. **Define the evidence that will prove each fix** — the artefact, the period, and who will retrieve it. A fix without a defined evidence trail will be re-found as a gap next cycle.
7. **Write the readiness statement per claim**, in the exact words a questionnaire would use, with one of: `evidenced for period X`, `operating with exceptions (rate, trend)`, `remediating by <date>`, `not claimed`. This is the document's most useful output.
8. **Record the residual risk position**: what the organisation is knowingly exposed to, who owns it, and when it is reviewed.
9. **Write `.governance/READINESS.md`:** gaps by consequence class, the four-way response per gap with owners and dates, the sequencing against the deadline, evidence definitions, per-claim readiness statements, residual risk register, and the list of what this assessment did not cover.
10. **Update the ledger and schedule the re-test** (P02) for each fix, because a fix that is not re-evidenced is a claim.

## 5. Decision rules and evidence standard

- **Never round up.** "Substantially compliant" is not a status; use the four per-claim statements.
- **Acceptance requires a named human owner and a date.** An accepted risk without an owner is an unowned risk.
- **Misrepresentation is fixed first**, even when the technical control takes months: correcting the claim is immediate and removes the exposure.
- **Do not promise a date you cannot evidence.** A missed remediation date is worse than an honest later one.
- **Compensating controls must be real and tested**, not plausible.
- **State what the assessment did not cover** — a readiness document that implies total coverage is itself a misrepresentation.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Gaps classified by consequence | inspect | class per gap |
| Every gap has one of four responses | inspect | none unaddressed |
| Fixes have owner, date, evidence definition | inspect | all three |
| Acceptances have named risk owner + review date | inspect | present |
| Sequencing against deadline explicit | inspect | what will not be ready stated |
| Per-claim readiness statements precise | read as a customer | unambiguous |
| Coverage limits stated | inspect | present |
| Re-test scheduled | inspect | date per fix |

## 7. Failure handling

- **Deadline is impossible** → say so immediately with the specific claims that cannot be supported; propose scope reduction or a corrected statement. Silence here converts an engineering problem into a contractual one.
- **Owner refuses to accept a risk** → record the gap as `unresolved` with the refusal; escalate to the accountable executive. Do not absorb the risk into engineering by default.
- **Evidence cannot be produced for a past period** → the gap for that period is permanent; record it and ensure the mechanism produces evidence going forward.
- **A gap is in a third party** (vendor, cloud provider) → record the dependency, request their attestation, and note the reliance in the readiness statement.
- **Remediation requires a change to production access** → route through `02-engineering/security-hardening/` and treat it as Category C with its own approval.

## 8. Security and authorisation

Risk class A: planning. Do not implement access changes here. Do not commit the readiness document containing security findings to a public repository — keep it in the controlled location used for `.governance/`, and record that decision.

## 9. Completion criteria

- [ ] Gaps classified by consequence.
- [ ] Four-way response recorded per gap.
- [ ] Fixes have owner, date, and evidence definition.
- [ ] Acceptances have a named owner, compensating control, and review date.
- [ ] Sequencing against the deadline, including what will not be ready.
- [ ] Per-claim readiness statements written in questionnaire language.
- [ ] Residual risk register complete.
- [ ] Coverage limits stated.
- [ ] Re-test scheduled per fix.

## 10. Deliverables and handover

Artifact: `.governance/READINESS.md`.

Handover: technical fixes → `02-engineering/security-hardening/`, `04-process/dependency-management/` P05, `03-domains/database/` P03; access changes → `security-hardening` with Category C gating; instrumentation → `04-process/observability-reliability/`; the readiness statements → the owner responding to the audit or questionnaire, with the evidence index attached.
