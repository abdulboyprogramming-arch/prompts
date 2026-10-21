# Package & Library Contribution System

**Status:** six skeleton outlines, two operational stages (`PKG-P03`, `PKG-P06`). Selection prices a change before it exists: a surface cost ledger for every candidate, the semver expectation with the symbol that drives it, and the support burden the maintainer takes on. Validation carries the evidence rules this domain needs — published-artifact diff, clean-environment install per runtime, and a semver verdict with its reason. The rest name a defensible sequence and nothing more; see [`_meta/ROADMAP-AND-BACKLOG.md`](../../_meta/ROADMAP-AND-BACKLOG.md).
**Entry Point:** [`P08-Orchestrator/P08-Package-Contribution-Orchestrator.md`](P08-Orchestrator/P08-Package-Contribution-Orchestrator.md)

A multi-stage system for making high-quality contributions to software packages and libraries (language packages, SDKs, shared libraries, CLI tools distributed as packages).

## Stages

| ID | Prompt | Purpose |
|----|--------|---------|
| PKG-P01 | Context & Package Understanding | Understand purpose, API surface, and norms |
| PKG-P02 | Discovery & Opportunity Identification | Find valuable contribution opportunities |
| PKG-P03 | [Opportunity Selection & Framing](P03-Selection/P03-Opportunity-Selection-Framing.md) — **operational** | Surface cost ledger, semver expectation, support burden |
| PKG-P04 | Planning & API Impact | Plan the change with compatibility in mind |
| PKG-P05 | Implementation | Execute following project conventions |
| PKG-P06 | [Validation & Compatibility](P06-Validation/P06-Validation-Compatibility.md) — **operational** | Published-artifact diff, clean-install smoke tests, semver verdict |
| PKG-P07 | PR & Communication | Prepare a professional pull request |
| PKG-P08 | Master Orchestrator | Coordinates the full contribution flow |

## Package-Specific Considerations

- Public API surface and backward compatibility
- Semantic versioning expectations
- Documentation and examples as first-class artifacts
- Cross-platform / multi-runtime concerns
- Changelog and release notes discipline
- Consumer impact of breaking changes
