# Package & Library Contribution System

**Status:** two skeleton outlines (`PKG-P01`, `PKG-P08`), six operational stages. The developed stages are organised around the public surface: discovery searches downstream consumer code for workarounds and pins, selection prices the surface cost, planning fixes the allowed delta and the release choreography, implementation exports nothing the plan did not price, validation diffs the published artefact, and communication is written as a release note first. `P01` and `P08` name a defensible sequence and nothing more; see [`_meta/ROADMAP-AND-BACKLOG.md`](../../_meta/ROADMAP-AND-BACKLOG.md).
**Entry Point:** [`P08-Orchestrator/P08-Package-Contribution-Orchestrator.md`](P08-Orchestrator/P08-Package-Contribution-Orchestrator.md)

A multi-stage system for making high-quality contributions to software packages and libraries (language packages, SDKs, shared libraries, CLI tools distributed as packages).

## Stages

| ID | Prompt | Purpose |
|----|--------|---------|
| PKG-P01 | Context & Package Understanding | Understand purpose, API surface, and norms |
| PKG-P02 | [Discovery & Opportunity Identification](P02-Discovery/P02-Discovery-Opportunity-Identification.md) — **operational** | Consumer-evidence table: workarounds, pins, duplicate reports |
| PKG-P03 | [Opportunity Selection & Framing](P03-Selection/P03-Opportunity-Selection-Framing.md) — **operational** | Surface cost ledger, semver expectation, support burden |
| PKG-P04 | [Planning & API Impact](P04-Planning/P04-Planning-API-Impact.md) — **operational** | Allowed surface delta, deprecation sequence, release choreography |
| PKG-P05 | [Implementation](P05-Implementation/P05-Implementation.md) — **operational** | Surface delta as a guard, entry-point tests, packaging checked |
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
