# Package & Library Contribution System

**Status:** Skeleton — 8 stage outlines (skeleton 8). The stages name a sensible sequence but lack the evidence rules, verification, and failure handling that this library requires of `operational`. Treat the system as a plan, not a procedure; see [`_meta/ROADMAP-AND-BACKLOG.md`](../../_meta/ROADMAP-AND-BACKLOG.md).
**Entry Point:** [`P08-Orchestrator/P08-Package-Contribution-Orchestrator.md`](P08-Orchestrator/P08-Package-Contribution-Orchestrator.md)

A multi-stage system for making high-quality contributions to software packages and libraries (language packages, SDKs, shared libraries, CLI tools distributed as packages, etc.).

## Stages

| ID | Prompt | Purpose |
|----|--------|---------|
| PKG-P01 | Context & Package Understanding | Understand purpose, API surface, and norms |
| PKG-P02 | Discovery & Opportunity Identification | Find valuable contribution opportunities |
| PKG-P03 | Opportunity Selection & Framing | Choose and clearly frame the work |
| PKG-P04 | Planning & API Impact | Plan the change with compatibility in mind |
| PKG-P05 | Implementation | Execute following project conventions |
| PKG-P06 | Validation & Compatibility | Tests, versioning, and compatibility checks |
| PKG-P07 | PR & Communication | Prepare a professional pull request |
| PKG-P08 | Master Orchestrator | Coordinates the full contribution flow |

## Package-Specific Considerations

- Public API surface and backward compatibility
- Semantic versioning expectations
- Documentation and examples as first-class artifacts
- Cross-platform / multi-runtime concerns
- Changelog and release notes discipline
- Consumer impact of breaking changes
