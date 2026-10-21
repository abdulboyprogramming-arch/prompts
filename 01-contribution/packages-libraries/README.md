# Package & Library Contribution System

**Status:** four skeleton outlines, four operational stages (`PKG-P02`, `PKG-P03`, `PKG-P06`, `PKG-P07`). Discovery searches downstream consumer code for workarounds and pins, because a library's evidence lives outside its repository. Selection prices a change before it exists: a surface cost ledger, the semver expectation with the symbol that drives it, and the support burden the maintainer takes on. Validation carries the published-artifact diff, the clean-environment install per runtime, and the semver verdict. Communication is written as a release note first, because the changelog entry is the acceptance test for the description. The rest name a defensible sequence and nothing more; see [`_meta/ROADMAP-AND-BACKLOG.md`](../../_meta/ROADMAP-AND-BACKLOG.md).
**Entry Point:** [`P08-Orchestrator/P08-Package-Contribution-Orchestrator.md`](P08-Orchestrator/P08-Package-Contribution-Orchestrator.md)

A multi-stage system for making high-quality contributions to software packages and libraries (language packages, SDKs, shared libraries, CLI tools distributed as packages).

## Stages

| ID | Prompt | Purpose |
|----|--------|---------|
| PKG-P01 | Context & Package Understanding | Understand purpose, API surface, and norms |
| PKG-P02 | [Discovery & Opportunity Identification](P02-Discovery/P02-Discovery-Opportunity-Identification.md) — **operational** | Consumer-evidence table: workarounds, pins, duplicate reports |
| PKG-P03 | [Opportunity Selection & Framing](P03-Selection/P03-Opportunity-Selection-Framing.md) — **operational** | Surface cost ledger, semver expectation, support burden |
| PKG-P04 | Planning & API Impact | Plan the change with compatibility in mind |
| PKG-P05 | Implementation | Execute following project conventions |
| PKG-P06 | [Validation & Compatibility](P06-Validation/P06-Validation-Compatibility.md) — **operational** | Published-artifact diff, clean-install smoke tests, semver verdict |
| PKG-P07 | [PR & Communication](P07-PR/P07-PR-Communication.md) — **operational** | Verdict first, draft changelog, migration snippet, release timing |
| PKG-P08 | Master Orchestrator | Coordinates the full contribution flow |

## Package-Specific Considerations

- Public API surface and backward compatibility
- Semantic versioning expectations
- Documentation and examples as first-class artifacts
- Cross-platform / multi-runtime concerns
- Changelog and release notes discipline
- Consumer impact of breaking changes
