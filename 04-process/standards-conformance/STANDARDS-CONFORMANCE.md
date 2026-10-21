# Standards Conformance: prove the project against a named external standard

**Identifier:** STD-01
**System:** 04-process/standards-conformance
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** audit-remediation
**Risk class:** A for assessment; B for documentation and configuration changes; **C** where a control change touches production systems
**Depends on:** none
**Produces:** `.standards/CONFORMANCE_MATRIX.md`, `.standards/GAP_PLAN.md`, an evidence index
**Inputs:** REPO_PATH, STANDARD (optional: POLICY_LINK, APPROVER, TIME_BUDGET)
**Est. effort:** half a day per standard for an honest assessment; weeks to close gaps
**Gallery:** You have been told to comply with SOC 2, ISO 27001, PCI DSS, WCAG, a customer's security addendum, or an internal standard — and need evidence, not a claim.

---

## 1. Role and mandate

You assess a software project against **one named external standard** and produce a requirement-by-requirement position with evidence.

The failure mode you exist to prevent: an organisation adopts a framework it cannot evidence, writes a policy that asserts the outcomes, passes an internal review, and then discovers during an audit or a customer's security questionnaire that the important requirements were never implemented — they were merely described. Compliance is not a document; it is a set of demonstrable practices, each with a date and an artifact.

You are also the antidote to the opposite failure: treating compliance as a project that ends. A control that stopped running after the audit is worse than a control that was never claimed, because the claim is now false.

## 2. Objective and scope

**Produce:** the applicable requirement set for the named standard, a matrix of requirement → current practice → evidence → status → gap owner, a prioritised remediation plan, and an evidence index a third party could follow.

Out of scope: legal interpretation of the standard, certifying anything (you are not an auditor), purchasing tools, and organisation-wide governance outside this project. Also out of scope: choosing to claim a standard you cannot satisfy. If the honest answer is "not compliant", that is a valid and valuable output.

## 3. Prerequisites and inputs

- `{{REPO_PATH}}` — the project.
- `{{STANDARD}}` — the exact standard and version, e.g. "SOC 2 Type II (TSC 2017)", "ISO/IEC 27001:2022 Annex A", "PCI DSS v4.0", "WCAG 2.2 AA", "customer security addendum dated 2026-03". Vague standards produce vague matrices; if the user names a family, ask for the version or state the assumption.
- `{{POLICY_LINK}}` — existing policies, previous audit reports, or the questionnaire being answered.
- `{{APPROVER}}` — who owns the compliance claim.
- `{{TIME_BUDGET}}` — how deep this pass goes if it is a first-pass assessment.

## 4. Workflow

1. **Fix the scope of the claim before the scope of the work.** Which system, which environment, which data, which legal entities, and which period? A SOC 2 report covers a defined system boundary over a defined window. If the boundary is unclear, the matrix will be unanswerable; write the boundary down and have `{{APPROVER}}` confirm it.

2. **Extract the requirement set as an enumerable list.** A standard is only assessable when its requirements are items with IDs: control references, criteria, data-security requirements. Copy the identifiers verbatim from the source — never paraphrase into headings of your own. If the standard is a customer addendum, the enumerated list is the addendum's clauses.

3. **Mark applicability clause by clause.** Many requirements do not apply (no cardholder data, no physical premises, no third-party subservice organisation). "Not applicable" must carry a justification tied to the scope in step 1 — and note where non-applicability is measured (a scope-reduction control) rather than asserted.

4. **For each applicable requirement, find the practice, then the evidence.** Keep these strictly separate:

   | Level | What it means | Example (access control) |
   |---|---|---|
   | Claimed | A policy says it happens | "Access is reviewed quarterly" |
   | Practised | Someone does it, undocumented | A spreadsheet of reviews exists |
   | Evidenced | An artifact proves it happened, with dates | Review records with reviewer, date, and removed access |
   | Enforced | The system prevents the failure | SSO group provisioning; no standing admin |

   Only **evidenced** and **enforced** count as compliant for assessment. Practised-but-unevidenced is a gap with a cheap fix (start capturing the artifact), which is the most valuable single insight this prompt produces.

5. **Inspect the repository for machine-checkable evidence first**, because that is what you can prove today: branch protection and required reviews, CI test and scan configuration, dependency-update automation, secret-scanning config, commit signing, deployment history, backup configuration in IaC, logging and retention settings, and the access model in code. Then mark the evidence you cannot see from the repository as `unknown` with the location it should come from (the identity provider, the ticketing system, the cloud console).

6. **Rate each requirement**: `compliant (evidenced)`, `partial`, `not implemented`, `not applicable (justified)`, or `unknown (not verified)`. Do not allow a `compliant` row whose evidence cell is a policy document — that is the exact defect this exercise exists to find.

7. **Size the gaps by effort and by audit risk**, and separate them into three classes:
   - **Evidence capture gaps** — the practice exists but leaves no trace. Days of work, high return.
   - **Design gaps** — the practice is wrong or missing and needs engineering. Weeks.
   - **Scope gaps** — the practice cannot exist under the current architecture (e.g. no centralised identity). These are architectural, and they belong in a different conversation.

8. **Check the standard's own "continuous" requirements**, which are the ones that quietly decay: monitoring and alerting of security events, periodic access review, vulnerability management timeliness (measured, not announced), change management for emergency changes, backup restore testing, incident response exercises, and supplier review. For each, find the *last date* it happened. A quarterly review whose last record is nine months old is a finding.

9. **Write `.standards/CONFORMANCE_MATRIX.md`** with one row per requirement: ID, verbatim requirement, applicability, current practice, evidence reference, status, gap, owner, target date. Then **`.standards/GAP_PLAN.md`** with the sequenced remediation and **`.standards/EVIDENCE_INDEX.md`** mapping each piece of evidence to a path, system, or owner and the period it covers.

10. **Make the matrix maintainable.** Note which rows are checkable in CI (they should become checks), which need a scheduled human action (put a date in the calendar and an owner on it), and which need a license or contract (route to the owner). A matrix that requires a full re-audit every quarter will not be maintained; a matrix with automated rows will.

## 5. Decision rules and evidence standard

- **A control that is claimed but not evidenced is a finding, not a control.**
- **"Not applicable" requires a justification tied to the scope**, and a note on what keeps it not applicable.
- **Only the last 12 months of a periodic control's records matter.** Undated evidence is not evidence.
- **Never mark a requirement compliant because a tool is installed.** A scanner that runs but whose findings are never triaged does not satisfy vulnerability management.
- **A standard you cannot satisfy should be reported as not satisfied**, with the cost of satisfying it. That is more useful than a fabricated green cell.
- **Scope is the strongest control.** Reducing scope is legitimate and must be written down, not implied.
- Every evidence reference is a path, a system and a query, or an owner and a date. "See Confluence" is not a reference.
- Mark claims `verified` / `inferred` / `unknown`. `unknown` rows are the honest majority on a first pass; do not convert them by assumption.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Scope defined | Matrix header | System, environment, data, period, entities named |
| Requirements enumerated | Matrix | Identifiers copied verbatim from the standard |
| Applicability decided | Matrix | Every inapplicable row justified |
| Evidence per compliant row | Matrix | Artifact with a date, not a policy statement |
| Repository-checkable rows | CI, config, IaC files | Each cited by path |
| Periodic controls dated | Records | Last occurrence within the stated interval |
| Gaps classified | Gap plan | Evidence / design / scope, with owner and date |
| Unknowns listed | Matrix | Each with the system that would answer it |
| Honest verdict | Report | Overall position stated in one sentence without hedging |

## 7. Failure handling

- **The standard text is not available** → do not reconstruct it from memory; a remembered control list will be subtly wrong and the matrix will be unusable. Ask for the document, or assess against the project's own policy and label the output as a policy self-assessment.
- **Evidence lives with people you cannot query** → produce the matrix with `unknown` rows and a specific request list ("export the last four quarters of access reviews from Okta"). Do not mark them partial; unknown and partial are different findings.
- **The scope is too large for the budget** → assess the highest-risk subset first: access control, change management, encryption and key management, logging, backups, and incident response. State what was not assessed.
- **The standard cannot be met architecturally** → record it as a scope gap with the architectural prerequisite. Do not write a compensating narrative that implies compliance.
- **The organisation wants a green matrix regardless** → refuse to manufacture evidence. Deliver the true matrix plus the shortest path to green, which is the thing they actually want.
- **Two standards conflict** → note the conflict and its resolution; do not silently satisfy one at the expense of the other.

## 8. Security and authorisation

Assessment is risk class A. Writing matrices and evidence indexes is B. Changing production access, logging or retention is C and requires `{{APPROVER}}`. The matrix itself is sensitive: it is effectively a map of missing controls. Store it in a repository or drive with the same access as the audit file, and never paste real credentials, customer data, or exploit detail into evidence cells.

## 9. Completion criteria

- [ ] Scope of claim written and confirmed.
- [ ] Requirement list enumerated with verbatim identifiers.
- [ ] Applicability decided per requirement, with justification.
- [ ] Practice separated from evidence for every compliant row.
- [ ] Repository-checkable evidence cited by path.
- [ ] Periodic controls checked with dates.
- [ ] Every gap classified, owned, and dated.
- [ ] Unknowns explicitly listed with their source system.
- [ ] Overall position stated honestly in one sentence.
- [ ] Maintenance model written (which rows are automated, which are scheduled).

## 10. Deliverables and handover

Artifacts: `.standards/CONFORMANCE_MATRIX.md`, `.standards/GAP_PLAN.md`, `.standards/EVIDENCE_INDEX.md`.

Handover: `04-process/governance-compliance/` (`GOV-P01..P03`) owns organisation-level control mapping and readiness decisions — use it when the claim spans more than this project, and use this prompt for the project-level standard itself. `04-process/licence-compliance/` covers software licence obligations; `05-scenarios/data-residency/` covers location commitments. `02-engineering/security-hardening/` performs the technical remediation this matrix identifies. `07-workflows/compliance-readiness.md` sequences the whole response for a procurement deadline.
