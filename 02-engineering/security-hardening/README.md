# Security Hardening

**Maturity: operational (v1.1.0).** Seven stages: authorisation → threat model → control review → triaged findings → plan → implementation and verification → orchestration.

**Entry point:** [`P07-Orchestrator/P07-Security-Hardening-Orchestrator.md`](P07-Orchestrator/P07-Security-Hardening-Orchestrator.md)
**Execution mode:** audit-remediation
**Risk class:** A for assessment stages, B for implementation — no production probing, no exploitation, no destructive testing

## What this system is

A review-and-fix system for the security of a codebase you own or are authorised to assess. It produces confirmed findings with code-level evidence, then fixes the ones you authorise, then verifies the fixes did not weaken anything else.

**It is not a penetration test**, a compliance attestation, or a vulnerability research programme. If you need active exploitation or adversary simulation, this system stops at P04 and hands over.

## The authorisation rule

Security work is the one area where "helpful" can be harmful. Therefore:

- P01 establishes **written authorisation, scope, and rules of engagement** before any assessment.
- Only read-only analysis and local, non-destructive checks are permitted.
- No payloads, no live probing of production, no credential attacks, no third-party systems.
- Findings are disclosed responsibly: enough to fix, not enough to weaponise (`00-core/safety-and-security/SECRETS-AND-SENSITIVE-DATA.md`).

If authorisation is absent, the system stops and says so. Absence of findings is never evidence of safety.

## Stages

| ID | Stage | Produces | Risk |
|----|-------|----------|------|
| SEC-P01 | [Authorisation, scope & rules of engagement](P01-Context/P01-Context-Scope.md) | `.security/SEC_SCOPE.md` | A |
| SEC-P02 | [Assets & threat model](P02-Threat-Model/P02-Threat-Model.md) | `.security/THREAT_MODEL.md` | A |
| SEC-P03 | [Control review](P03-Surface-Analysis/P03-Surface-Analysis.md) | `.security/CONTROL_REVIEW.md` | A |
| SEC-P04 | [Findings & triage](P04-Findings/P04-Findings-Prioritization.md) | `.security/FINDINGS.md` | A |
| SEC-P05 | [Hardening plan](P05-Hardening-Plan/P05-Hardening-Plan.md) | `.security/HARDENING_PLAN.md` | A |
| SEC-P06 | [Implementation & verification](P06-Implementation-Validation/P06-Implementation-Validation.md) | changes, `.security/VERIFICATION.md` | B |
| SEC-P07 | [Orchestrator](P07-Orchestrator/P07-Security-Hardening-Orchestrator.md) | all of the above | A/B |

## Shared contracts

**Finding states.** Every observation is exactly one of:

- `confirmed` — the code path is identified and the control is absent or wrong at that point.
- `suspected` — configuration- or environment-dependent; needs runtime confirmation you are not authorised to perform.
- `question` — requires an owner decision (intended behaviour, compensating control).

Only `confirmed` findings may be rated S1/S2.

**Severity.** Reuse the audit model: S1 data loss/breach/unauthorised access in normal operation; S2 likely exploitable or fails a required control; S3 real but constrained; S4 hygiene. Severity is adjusted by **reachability** (is the path exercised?) and **exposure** (internal or internet-facing), and the adjustment is recorded.

**Evidence.** Every finding cites `file:line` and shows *why* the control fails. No payload, no working exploit, no reproduction that could be copied into an attack without additional work.

## Boundaries

- Whole-codebase quality and architecture: `02-engineering/codebase-audit/` (this system consumes its P06 output when available).
- LLM-specific attack surface (prompt injection, tool abuse): `03-domains/ai-agentic/` AI-P04.
- Deployment-time controls (TLS, network policy, secret injection): `03-domains/devops-infra/`.
- Incident in progress: `05-scenarios/incident-response/`. Do not run a review during an outage.
- Dependency CVEs: gather in audit P05 or this system's P03 supply-chain section; do not duplicate both.
- Credentials published in client artifacts (browser bundles, app binaries, `EXPO_PUBLIC_*`/`NEXT_PUBLIC_*` inlining): `05-scenarios/client-secrets/` — a different failure from a leaked server credential, because there is no rotation that un-publishes it.
- Build and release integrity (lockfiles, install scripts, provenance, digest pinning): `05-scenarios/supply-chain/`.
- Evidence obligations for a named standard: `04-process/standards-conformance/`.

## What this system will not do

- Prove absence of vulnerabilities.
- Attest compliance or produce audit evidence for a third party without a separate, scoped engagement.
- Test third-party services, even ones the application calls.
- Fix a finding by disabling a feature or weakening a check to make a test pass.
