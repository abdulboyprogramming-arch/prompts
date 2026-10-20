# Release Engineering

**Maturity: operational (v1.0.0).** Four stages covering readiness, communication, deployment strategy, and post-release verification.

**Entry point:** [`P01-Readiness/P01-Release-Readiness.md`](P01-Readiness/P01-Release-Readiness.md)
**Execution mode:** audit-remediation
**Risk class:** B — version files, changelogs, release configuration, and checklists; publishing and deploying are Category C and require explicit authorisation

## Why this system exists

Most bad releases are not caused by bad code. They are caused by a missing verification step, an undeclared breaking change, a migration that ran before the code that needed it, or a rollback nobody tested. This system turns releasing into a repeatable procedure with evidence at each gate.

## Stages

| ID | Stage | Produces |
|----|-------|----------|
| REL-P01 | [Release readiness](P01-Readiness/P01-Release-Readiness.md) | `RELEASE_READINESS.md`, go/no-go verdict |
| REL-P02 | [Versioning, changelog & release notes](P02-Versioning/P02-Versioning-Changelog.md) | version bump, `CHANGELOG.md` entry, release notes |
| REL-P03 | [Deployment strategy, migrations & rollback](P03-Deployment/P03-Deployment-Rollback.md) | `DEPLOYMENT_PLAN.md` |
| REL-P04 | [Post-release verification](P04-Verification/P04-Post-Release-Verification.md) | `POST_RELEASE.md` |

## Principles

1. **A release is a decision, not a build artifact.** Something is released when readiness evidence exists, the change is communicated, and the deployment is reversible.
2. **Every change is classified by compatibility.** Before the version is chosen, determine whether the change is breaking for any supported consumer: API shape, schema, config keys, CLI flags, error semantics, on-disk formats.
3. **Migrations are two-phase.** Expand (add, backward compatible) → deploy code that uses the new shape → contract (remove old) in a later release. A single release must never require new and old code to disagree about schema.
4. **Rollback must be executable, not conceptual.** A rollback that depends on a database downgrade you have never run is not a rollback.
5. **Feature flags decouple deploy from release.** Ship dark, enable deliberately, and record the flag owner and expiry.
6. **The changelog is for the consumer, not the committer.** It states what changed in behaviour, what breaks, and what to do about it.

## Boundaries

- CI/CD pipeline construction: `03-domains/devops-infra/`.
- Incident response when a release goes wrong: `05-scenarios/incident-response/` and `07-workflows/production-incident.md`.
- Post-release reliability review: `04-process/observability-reliability/` OBS-P05.
- Package publishing specifics (registry metadata, deprecation): `01-contribution/packages-libraries/`.
