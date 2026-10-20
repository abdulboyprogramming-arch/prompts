# Dependency & Toolchain Management

**Maturity: operational (v1.0.0).** Five stages for the change that most often breaks working software: upgrading what it is built on.

**Entry point:** [`P01-Inventory/P01-Dependency-Inventory-Risk.md`](P01-Inventory/P01-Dependency-Inventory-Risk.md)
**Execution mode:** audit-remediation
**Risk class:** B — manifest, lockfile, and code changes; publishing or deploying is Category C

## Why this system exists

Dependency work is the highest-frequency, lowest-glamour source of regressions. It fails in predictable ways:

- An upgrade is applied as a version bump without reading the breaking changes.
- Transitive dependencies are upgraded implicitly by a lockfile refresh and are never reviewed.
- A major framework upgrade is attempted across the whole codebase in one commit, so nothing can be attributed or rolled back.
- A dependency is abandoned but kept forever because replacing it is "too big".
- A minor version silently changes behaviour despite the semver promise.

The coverage matrix recorded this as **missing** until v1.0.0 of this system. It is now a first-class procedure.

## Stages

| ID | Stage | Purpose | Produces |
|----|-------|---------|----------|
| DEP-P01 | [Inventory & risk](P01-Inventory/P01-Dependency-Inventory-Risk.md) | Know what you depend on, direct and transitive, and what is risky | `.deps/DEPENDENCY_MAP.md` |
| DEP-P02 | [Upgrade planning & breaking-change assessment](P02-Planning/P02-Upgrade-Planning.md) | Read the actual migration guide; plan the sequence and blast radius | `.deps/UPGRADE_PLAN.md` |
| DEP-P03 | [Execution](P03-Execution/P03-Upgrade-Execution.md) | One family at a time, lockfile discipline, codemods where approved | commits, `.deps/UPGRADE_LOG.md` |
| DEP-P04 | [Verification](P04-Verification/P04-Verification.md) | Prove behaviour is unchanged where it must be, and improved where intended | `.deps/VERIFICATION.md` |
| DEP-P05 | [Policy & maintenance](P05-Policy/P05-Policy-Maintenance.md) | Pinning, cadence, abandoned-dependency criteria, supply-chain integrity | `.deps/POLICY.md` |

## Rules

1. **Semver is a promise, not a guarantee.** Read release notes for every minor and patch upgrade that touches runtime behaviour.
2. **Never upgrade and refactor in the same change.** Two variables make verification meaningless.
3. **Transitive changes are changes.** If the lockfile moved, someone must read why.
4. **One dependency family per commit**, so a regression can be attributed and reverted precisely.
5. **The lockfile is the artefact under test.** A manifest change without a committed lockfile update is an unreviewed resolution.
6. **Abandonment is a decision with a date**, not a permanent state of unease.
7. **Security upgrades are not deferred for convenience**, but they still follow the verification path — faster, not skipped.

## Boundaries

- Vulnerability scanning and reporting: `02-engineering/security-hardening/` P03/P04 (this system consumes the output).
- Build/toolchain failures unrelated to versioning: `05-scenarios/debugging/`.
- Release sequencing for the upgraded application: `04-process/release-engineering/`.
- Reproducible pipeline and caching: `03-domains/devops-infra/`.

## What this system will not do

- Guarantee an upgrade is safe. It makes the risk visible and the verification real.
- Chase latest versions. Newest is not a goal; supported, maintained, and secure is.
- Upgrade across major versions automatically without a plan.
