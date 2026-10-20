# Deep Codebase Audit & Analysis System

**Status:** Operational (v1.0)  
**Entry Point:** [`P09-Orchestrator/P09-Deep-Codebase-Audit-Orchestrator.md`](P09-Orchestrator/P09-Deep-Codebase-Audit-Orchestrator.md)

A complete, multi-stage professional system for performing deep, evidence-based audits of existing codebases.

## Stages

| ID | Prompt | Purpose |
|----|--------|---------|
| AUDIT-P01 | Environment & Context Bootstrap | Scope, tools, initial artifacts |
| AUDIT-P02 | Structural Mapping | Directory map, entry points, roots |
| AUDIT-P03 | Architectural Analysis | Subsystems, dependencies, risks |
| AUDIT-P04 | Code Quality & Maintainability | Smells, complexity, consistency |
| AUDIT-P05 | Tests & Dependencies Health | Test maturity, dependency posture |
| AUDIT-P06 | Security Surface & Documentation | Trust boundaries, docs quality |
| AUDIT-P07 | Findings Synthesis & Prioritization | Consolidated, prioritized findings |
| AUDIT-P08 | Improvement Roadmap & Final Report | Actionable roadmap + professional report |
| AUDIT-P09 | Master Orchestrator | Coordinates the entire audit |

## How to Use

Give your coding agent the **Master Orchestrator** prompt together with the target repository (and any specific audit goals or constraints).

The agent will produce a full set of durable artifacts under `.codebase-audit/` and a final professional report.

## Design Principles

- Evidence over assertion
- Progressive deepening
- Clear separation of facts, inferences, and recommendations
- Actionable output (prioritized findings + roadmap)
- Responsible handling of security-related observations
