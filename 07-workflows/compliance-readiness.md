# Workflow — Compliance Readiness

**Identifier:** WF-COMPLY
**System:** 07-workflows
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** orchestration
**Risk class:** A for assessment stages; B for remediation of documentation and configuration; **C** where a control change touches production, and **C** for anything sent to a customer or auditor
**Gallery:** A security questionnaire, an audit window, or a customer contract names a standard you must evidence — sequence the whole response instead of improvising it.
**Depends on:** `04-process/governance-compliance/`, `04-process/standards-conformance/`, `04-process/licence-compliance/`, `05-scenarios/supply-chain/`, `05-scenarios/data-residency/`, `02-engineering/security-hardening/`, `04-process/privacy-requests/`
**Depends on (inputs):** `04-process/governance-compliance/`, `04-process/standards-conformance/`, `04-process/licence-compliance/`, `05-scenarios/supply-chain/`, `05-scenarios/data-residency/`, `02-engineering/security-hardening/`, `04-process/privacy-requests/`
**Produces:** a compliance evidence pack, a gap plan with owners, and a readiness position you can defend
**Inputs:** STANDARD, SYSTEM_SCOPE (optional: APPROVER, TIME_BUDGET)

---

## 1a. When to use this

One of these has just arrived:

- a customer security questionnaire with a deadline;
- an audit window with a defined scope;
- a procurement requirement naming SOC 2, ISO 27001, PCI DSS, HIPAA, a data-processing addendum, or an internal standard;
- a renewal of something you previously claimed and have not maintained.

Do not use it to "become compliant" in the abstract. Compliance work without a named standard, scope, and evidence consumer becomes a documentation project that satisfies nobody.

## 3. Entry conditions

| Condition | Required |
|---|---|
| The standard is named **with a version**: `{{STANDARD}}` | yes — a family name is not a standard |
| The scope is named: `{{SYSTEM_SCOPE}}` — system, environment, time period | yes |
| The evidence consumer is named: auditor, customer, internal owner | yes |
| A person owns the claim | yes — `{{APPROVER}}` in each stage |
| The deadline is known: `{{TIME_BUDGET}}` | yes — it decides depth |

Missing any of these means the first action is to obtain it, not to start assessing.

## 1. The sequence

| # | Step | Prompt | Output | Gate |
|---|------|--------|--------|------|
| 1 | Fix scope and standard | `04-process/standards-conformance/` step 1 | scope statement | **GATE 1** scope accepted by the claim owner |
| 2 | Requirement matrix | `STD-01` | `.standards/CONFORMANCE_MATRIX.md` | — |
| 3 | Organisation-level controls | `04-process/governance-compliance/` `GOV-P01`, `GOV-P02` | `.governance/CONTROL_MAP.md`, `EVIDENCE.md` | — |
| 4 | Technical gaps | `02-engineering/security-hardening/` `SEC-P01..P05` | threat model, enforcement matrix, plan | **GATE 2** remediation authorised |
| 5 | Remediation | `SEC-P06`, `STD-01` step 9 | changes with re-verification | — |
| 6 | Software obligations | `04-process/licence-compliance/`, `05-scenarios/supply-chain/` | licence report, notices, provenance | — |
| 7 | Data location obligations | `05-scenarios/data-residency/`, `04-process/privacy-requests/` | data map, transfer register, deletion evidence | — |
| 8 | Operational evidence | `05-scenarios/operational-readiness/`, `05-scenarios/disaster-recovery/` | drill records, runbooks, alert inventory | — |
| 9 | Readiness decision | `GOV-P03`, `STD-01` step 10 | `.governance/READINESS.md`, `.standards/GAP_PLAN.md` | **GATE 3** position approved for external use |
| 10 | Evidence pack and response | this workflow | indexed evidence pack | **GATE 4** sent |

## Decision rules that matter

1. **Scope before evidence.** Gathering artifacts before the boundary is fixed produces a pack of documents that answer different questions.
2. **Evidence capture before remediation.** Where the practice exists but leaves no record, capturing the record is days of work and closes the finding; engineering a new control is weeks. Do the cheap one first and buy time.
3. **Technical before procedural.** A policy claiming a control that the pipeline does not implement is a finding with a lawyer attached. Fix the machine-checkable controls first.
4. **Licence and data-location work runs in parallel with technical work**, not after — they have different owners and often longer lead times.
5. **Never send anything externally from a stage still marked `unknown`** unless the unknown is disclosed. An auditor forgives "not yet evidenced"; they do not forgive a false statement.

## 2. What the evidence pack contains

| Section | Source | Minimum |
|---|---|---|
| Scope and period | step 1 | system, environment, dates, entities |
| Control matrix | `STD-01` | requirement, practice, evidence, status |
| Technical evidence | repository, CI, IaC | branch protection export, pipeline config, scan results with dates |
| Access evidence | identity provider | role assignments, review records with dates |
| Change evidence | version control | sample of merged changes with approvals |
| Incident evidence | incident records | list with dates and resolutions |
| Continuity evidence | `DR-01` | drill log with measured RTO/RPO |
| Software obligations | `LIC-01`, `SUPPLY-01` | licence report, notices, SBOM/signature status |
| Data obligations | `RESIDENCY-01`, `PRIV-*` | data map, transfer register, deletion records |
| Open gaps | `GAP_PLAN.md` | owner and date for everything not yet met |

Every item carries a date and a location. An evidence pack without dates is a brochure.

## Failure handling and routing

| Situation | Response |
|---|---|
| The standard's text is unavailable | stop; assess against internal policy and label the output a self-assessment |
| A required control cannot exist in the current architecture | scope gap: name the architectural prerequisite, do not write a compensating narrative |
| The deadline is shorter than the remediation | submit with disclosed gaps and a dated plan; a request for extension is better than a false statement |
| A previous claim turns out to be unevidenced | disclose it to the claim owner immediately; it changes the whole response |
| Remediation breaks a working control | revert, then re-plan — never trade a live control for a document |
| Responsibility for a control sits outside engineering | record the owner, request the artifact in writing, and mark it `unknown` until received |

## Completion criteria for the workflow

- [ ] Every applicable requirement has a status and, where compliant, dated evidence.
- [ ] Every gap has an owner, a date, and a disclosure decision.
- [ ] The evidence pack is indexed, dated, access-controlled, and reproducible from the sources it cites.
- [ ] The readiness position is stated in one sentence that a non-engineer can act on.
- [ ] The maintenance model is written: which rows re-check automatically, which recur on a schedule, and who runs them.

## Handover

`04-process/governance-compliance/` continues to own the organisation-level programme after the response. `04-process/standards-conformance/` maintains the matrix between cycles. The next cycle starts from `STD-01` step 5, not from scratch — that is the difference between a certification and a habit.
