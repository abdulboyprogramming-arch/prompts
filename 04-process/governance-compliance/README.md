# Enterprise Readiness & Governance

**Maturity: operational (v1.0.0).** Three stages for proving that engineering practice matches what the organisation claims about it.

**Entry point:** [`P01-Control-Map/P01-Control-Map.md`](P01-Control-Map/P01-Control-Map.md)
**Execution mode:** audit-remediation
**Risk class:** A for assessment; B for remediation; C for changes to production access controls

## Why this system exists

Enterprise buyers, auditors, and regulators do not ask whether your code is good. They ask whether you can **demonstrate** that it is produced under controls: that changes are reviewed, that access is limited, that incidents are recorded, that data is retained and deleted as promised.

Most engineering organisations can describe these practices and cannot evidence them. The gap appears at the worst moment — during a security questionnaire, an audit, or an incident investigation — and it is expensive because evidence cannot be manufactured retroactively.

This system does not implement a compliance framework. It connects what already exists in the repository and the pipeline to the controls being claimed, and it names the controls that have no evidence.

## Stages

| ID | Stage | Purpose | Produces |
|----|-------|---------|----------|
| GOV-P01 | [Control map](P01-Control-Map/P01-Control-Map.md) | Map claimed obligations to actual engineering practice and locate evidence | `.governance/CONTROL_MAP.md` |
| GOV-P02 | [Evidence & control testing](P02-Evidence/P02-Evidence-Testing.md) | Prove controls operate, not just that they are documented | `.governance/EVIDENCE.md` |
| GOV-P03 | [Gap remediation & readiness](P03-Readiness/P03-Readiness-Decision.md) | Close or formally accept gaps; state readiness honestly | `.governance/READINESS.md` |

## The distinction that matters

| Claim | Evidence that supports it | Evidence that does not |
|-------|---------------------------|------------------------|
| "All changes are reviewed" | Branch protection settings + a sample of merged PRs showing approvals before merge | A policy document saying reviews are required |
| "Access is least-privilege" | Current role assignments for production, with justification per human and per service account | An onboarding checklist |
| "Vulnerabilities are remediated on a schedule" | Advisories with open/close dates and the measured time-to-fix | A scanner being installed |
| "Data is deleted on request" | A completed deletion record with verification | A documented process |
| "Incidents are recorded" | Incident records with timelines for the last N events | A template |

**A control that is not evidenced is not a control** — it is an intention. Say so, in writing, in the readiness decision.

## Boundaries

- Technical security remediation: `02-engineering/security-hardening/`.
- Incident handling: `05-scenarios/security-incident/` and `05-scenarios/incident-response/`.
- Release controls: `04-process/release-engineering/`.
- Dependency and supply-chain integrity: `04-process/dependency-management/` P05.
- **Legal interpretation and audit attestation**: out of scope. This system surfaces facts and gaps for the accountable owner; it does not certify anything.

## What this system will not do

- Produce a certificate, an attestation, or a legal opinion.
- Invent controls the organisation does not actually operate.
- Retroactively create evidence. Missing historical evidence is a permanent finding for that period.
