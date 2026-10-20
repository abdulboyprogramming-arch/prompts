# Catalog

<!-- GENERATED FILE — do not edit by hand. Run: python3 scripts/validate_library.py --catalog -->

Every prompt in the library, grouped by system, with its declared maturity,
execution mode, and risk class. `skeleton` rows are structural outlines and
are not ready to run. See `_meta/prompt-authoring-standard.md`.

**Totals:** 325 prompts — 0 canonical, 171 operational, 5 draft, 149 skeleton.

## `00-core`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `GEN-P01` | PROMPT 01 — The Prompt Forge: build a runnable prompt from a | operational | specialised | A | [PROMPT-FORGE.md](../00-core/prompt-engineering/PROMPT-FORGE.md) |
| `GEN-P02` | PROMPT 02 — Prompt Regression: prove a prompt change is an i | operational | continuous-improvement | A | [PROMPT-REGRESSION.md](../00-core/prompt-engineering/PROMPT-REGRESSION.md) |

## `01-contribution/language-design`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `LD-P01` | PROMPT 01 — Vision & Motivation | skeleton | planning | B | [P01-Vision-Motivation.md](../01-contribution/language-design/P01-Vision/P01-Vision-Motivation.md) |
| `LD-P02` | PROMPT 02 — Requirements & Constraints | skeleton | planning | B | [P02-Requirements-Constraints.md](../01-contribution/language-design/P02-Requirements/P02-Requirements-Constraints.md) |
| `LD-P03` | PROMPT 03 — Language Design | skeleton | planning | B | [P03-Language-Design.md](../01-contribution/language-design/P03-Design/P03-Language-Design.md) |
| `LD-P04` | PROMPT 04 — Specification | skeleton | planning | B | [P04-Specification.md](../01-contribution/language-design/P04-Specification/P04-Specification.md) |
| `LD-P05` | PROMPT 05 — Implementation Plan | skeleton | planning | B | [P05-Implementation-Plan.md](../01-contribution/language-design/P05-Implementation-Plan/P05-Implementation-Plan.md) |
| `LD-P06` | PROMPT 06 — Prototype | skeleton | research | A | [P06-Prototype.md](../01-contribution/language-design/P06-Prototype/P06-Prototype.md) |
| `LD-P07` | PROMPT 07 — Evaluation | skeleton | diagnostic | B | [P07-Evaluation.md](../01-contribution/language-design/P07-Evaluation/P07-Evaluation.md) |
| `LD-P08` | PROMPT 08 — Language Design Master Orchestrator | skeleton | orchestration | A | [P08-Language-Design-Orchestrator.md](../01-contribution/language-design/P08-Orchestrator/P08-Language-Design-Orchestrator.md) |

## `01-contribution/open-source/general-agent`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `P01` | PROMPT 01 — System Architecture, Requirements & Execution Bl | operational | planning | C | [P01-System-Architecture-Requirements-Execution-Blueprint.md](../01-contribution/open-source/general-agent/P01-System-Architecture/P01-System-Architecture-Requirements-Execution-Blueprint.md) |
| `P02` | PROMPT 02 — Environment & Identity Bootstrap | operational | implementation | B | [P02-Environment-Identity-Bootstrap.md](../01-contribution/open-source/general-agent/P02-Environment-Bootstrap/P02-Environment-Identity-Bootstrap.md) |
| `P03` | PROMPT 03 — Repository Discovery & Initial Reconnaissance | operational | diagnostic | C | [P03-Repository-Discovery-Initial-Reconnaissance.md](../01-contribution/open-source/general-agent/P03-Repo-Discovery/P03-Repository-Discovery-Initial-Reconnaissance.md) |
| `P04` | PROMPT 04 — Deep Architectural Intelligence | operational | implementation | C | [P04-Deep-Architectural-Intelligence.md](../01-contribution/open-source/general-agent/P04-Architectural-Intelligence/P04-Deep-Architectural-Intelligence.md) |
| `P05` | PROMPT 05 — File, Module, Dependency & Component Understandi | operational | implementation | B | [P05-File-Module-Dependency-Component-Understanding.md](../01-contribution/open-source/general-agent/P05-File-Module-Understanding/P05-File-Module-Dependency-Component-Understanding.md) |
| `P06` | PROMPT 06 — Git History, Branches, Releases & Development Co | operational | implementation | C | [P06-Git-History-Branches-Releases-Development-Conventions.md](../01-contribution/open-source/general-agent/P06-Git-History-Conventions/P06-Git-History-Branches-Releases-Development-Conventions.md) |
| `P07` | PROMPT 07 — GitHub Issues, Discussions, PRs & Documented Con | operational | diagnostic | C | [P07-GitHub-Issues-Discussions-PRs-Contribution-Discovery.md](../01-contribution/open-source/general-agent/P07-GitHub-Opportunities/P07-GitHub-Issues-Discussions-PRs-Contribution-Discovery.md) |
| `P08` | PROMPT 08 — Independent Defect Discovery & Technical Opportu | operational | diagnostic | A | [P08-Independent-Defect-Discovery-Technical-Opportunity-Analysis.md](../01-contribution/open-source/general-agent/P08-Independent-Discovery/P08-Independent-Defect-Discovery-Technical-Opportunity-Analysis.md) |
| `P09` | PROMPT 09 — Opportunity Verification, Prioritization & Task  | operational | planning | A | [P09-Opportunity-Verification-Prioritization-Task-Selection.md](../01-contribution/open-source/general-agent/P09-Opportunity-Selection/P09-Opportunity-Verification-Prioritization-Task-Selection.md) |
| `P10` | PROMPT 10 — Implementation Planning & Change Isolation | operational | planning | B | [P10-Implementation-Planning-Change-Isolation.md](../01-contribution/open-source/general-agent/P10-Implementation-Planning/P10-Implementation-Planning-Change-Isolation.md) |
| `P11` | PROMPT 11 — Engineering Execution & Code Modification | operational | implementation | B | [P11-Engineering-Execution-Code-Modification.md](../01-contribution/open-source/general-agent/P11-Engineering-Execution/P11-Engineering-Execution-Code-Modification.md) |
| `P12` | PROMPT 12 — Testing, Security, Regression Analysis & Quality | operational | diagnostic | A | [P12-Testing-Security-Regression-Quality-Assurance.md](../01-contribution/open-source/general-agent/P12-QA-Validation/P12-Testing-Security-Regression-Quality-Assurance.md) |
| `P13` | PROMPT 13 — Git Operations, Atomic Commits & Authorized Remo | operational | implementation | C | [P13-Git-Operations-Commits-Authorized-Remote-Publication.md](../01-contribution/open-source/general-agent/P13-Git-Publication/P13-Git-Operations-Commits-Authorized-Remote-Publication.md) |
| `P14` | PROMPT 14 — Issues, Pull Requests, Review Responses & Mainta | operational | diagnostic | C | [P14-Issues-Pull-Requests-Review-Responses-Maintainer-Communication.md](../01-contribution/open-source/general-agent/P14-PR-Communication/P14-Issues-Pull-Requests-Review-Responses-Maintainer-Communication.md) |
| `P15` | PROMPT 15 — Continuous Contribution Management, Monitoring & | operational | implementation | B | [P15-Continuous-Contribution-Management-Recovery.md](../01-contribution/open-source/general-agent/P15-Continuous-Management/P15-Continuous-Contribution-Management-Recovery.md) |
| `P16` | PROMPT 16 — Final Autonomous Contribution Orchestrator | operational | orchestration | C | [P16-Final-Autonomous-Contribution-Orchestrator.md](../01-contribution/open-source/general-agent/P16-Master-Orchestrator/P16-Final-Autonomous-Contribution-Orchestrator.md) |

## `01-contribution/packages-libraries`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `PKG-P01` | PROMPT 01 — Context & Package Understanding | skeleton | implementation | B | [P01-Context-Package-Understanding.md](../01-contribution/packages-libraries/P01-Context/P01-Context-Package-Understanding.md) |
| `PKG-P02` | PROMPT 02 — Discovery & Opportunity Identification | skeleton | diagnostic | A | [P02-Discovery-Opportunity-Identification.md](../01-contribution/packages-libraries/P02-Discovery/P02-Discovery-Opportunity-Identification.md) |
| `PKG-P03` | PROMPT 03 — Opportunity Selection & Framing | skeleton | planning | B | [P03-Opportunity-Selection-Framing.md](../01-contribution/packages-libraries/P03-Selection/P03-Opportunity-Selection-Framing.md) |
| `PKG-P04` | PROMPT 04 — Planning & API Impact | skeleton | planning | B | [P04-Planning-API-Impact.md](../01-contribution/packages-libraries/P04-Planning/P04-Planning-API-Impact.md) |
| `PKG-P05` | PROMPT 05 — Implementation | skeleton | implementation | B | [P05-Implementation.md](../01-contribution/packages-libraries/P05-Implementation/P05-Implementation.md) |
| `PKG-P06` | PROMPT 06 — Validation & Compatibility | skeleton | diagnostic | C | [P06-Validation-Compatibility.md](../01-contribution/packages-libraries/P06-Validation/P06-Validation-Compatibility.md) |
| `PKG-P07` | PROMPT 07 — PR & Communication | skeleton | implementation | B | [P07-PR-Communication.md](../01-contribution/packages-libraries/P07-PR/P07-PR-Communication.md) |
| `PKG-P08` | PROMPT 08 — Package & Library Contribution Master Orchestrat | skeleton | orchestration | A | [P08-Package-Contribution-Orchestrator.md](../01-contribution/packages-libraries/P08-Orchestrator/P08-Package-Contribution-Orchestrator.md) |

## `01-contribution/web/general`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `WEB-P01` | PROMPT 01 — Context & Project Understanding | skeleton | implementation | B | [P01-Context-Project-Understanding.md](../01-contribution/web/general/P01-Context/P01-Context-Project-Understanding.md) |
| `WEB-P02` | PROMPT 02 — Discovery & Opportunity Identification | skeleton | diagnostic | A | [P02-Discovery-Opportunity-Identification.md](../01-contribution/web/general/P02-Discovery/P02-Discovery-Opportunity-Identification.md) |
| `WEB-P03` | PROMPT 03 — Opportunity Selection & Framing | skeleton | planning | B | [P03-Opportunity-Selection-Framing.md](../01-contribution/web/general/P03-Opportunity/P03-Opportunity-Selection-Framing.md) |
| `WEB-P04` | PROMPT 04 — Planning & Design | skeleton | planning | B | [P04-Planning-Design.md](../01-contribution/web/general/P04-Planning/P04-Planning-Design.md) |
| `WEB-P05` | PROMPT 05 — Implementation | skeleton | implementation | B | [P05-Implementation.md](../01-contribution/web/general/P05-Implementation/P05-Implementation.md) |
| `WEB-P06` | PROMPT 06 — Validation & Quality | skeleton | diagnostic | B | [P06-Validation-Quality.md](../01-contribution/web/general/P06-Validation/P06-Validation-Quality.md) |
| `WEB-P07` | PROMPT 07 — PR & Communication | skeleton | implementation | B | [P07-PR-Communication.md](../01-contribution/web/general/P07-PR-Communication/P07-PR-Communication.md) |
| `WEB-P08` | PROMPT 08 — Web Contribution Master Orchestrator | skeleton | orchestration | A | [P08-Web-Contribution-Orchestrator.md](../01-contribution/web/general/P08-Orchestrator/P08-Web-Contribution-Orchestrator.md) |

## `01-contribution/web3/general`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `W3-P01` | PROMPT 01 — Context & Project Understanding | skeleton | implementation | B | [P01-Context-Project-Understanding.md](../01-contribution/web3/general/P01-Context/P01-Context-Project-Understanding.md) |
| `W3-P02` | PROMPT 02 — Discovery & Opportunity Identification | skeleton | diagnostic | A | [P02-Discovery-Opportunity-Identification.md](../01-contribution/web3/general/P02-Discovery/P02-Discovery-Opportunity-Identification.md) |
| `W3-P03` | PROMPT 03 — Opportunity Selection & Framing | skeleton | planning | B | [P03-Opportunity-Selection-Framing.md](../01-contribution/web3/general/P03-Selection/P03-Opportunity-Selection-Framing.md) |
| `W3-P04` | PROMPT 04 — Planning & Design | skeleton | planning | B | [P04-Planning-Design.md](../01-contribution/web3/general/P04-Planning/P04-Planning-Design.md) |
| `W3-P05` | PROMPT 05 — Implementation | skeleton | implementation | B | [P05-Implementation.md](../01-contribution/web3/general/P05-Implementation/P05-Implementation.md) |
| `W3-P06` | PROMPT 06 — Validation & Security Checks | skeleton | diagnostic | B | [P06-Validation-Security.md](../01-contribution/web3/general/P06-Validation/P06-Validation-Security.md) |
| `W3-P07` | PROMPT 07 — PR & Communication | skeleton | implementation | B | [P07-PR-Communication.md](../01-contribution/web3/general/P07-PR/P07-PR-Communication.md) |
| `W3-P08` | PROMPT 08 — Web3 Contribution Master Orchestrator | skeleton | orchestration | A | [P08-Web3-Contribution-Orchestrator.md](../01-contribution/web3/general/P08-Orchestrator/P08-Web3-Contribution-Orchestrator.md) |

## `02-engineering`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `SEC-ROT-01` | PROMPT 01 — Secret Rotation: drill it before you need it | operational | implementation | C | [SECRETS-ROTATION.md](../02-engineering/secrets-rotation/SECRETS-ROTATION.md) |
| `TENANCY-01` | PROMPT 01 — Tenant Isolation Audit | operational | diagnostic | A | [TENANCY-AUDIT.md](../02-engineering/tenancy-audit/TENANCY-AUDIT.md) |

## `02-engineering/architecture-review`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `AR-P01` | PROMPT 01 — Context & Goals | skeleton | planning | B | [P01-Context-Goals.md](../02-engineering/architecture-review/P01-Context/P01-Context-Goals.md) |
| `AR-P02` | PROMPT 02 — Current Architecture | skeleton | planning | C | [P02-Current-Architecture.md](../02-engineering/architecture-review/P02-Current-Architecture/P02-Current-Architecture.md) |
| `AR-P03` | PROMPT 03 — Quality Attributes | skeleton | implementation | B | [P03-Quality-Attributes.md](../02-engineering/architecture-review/P03-Quality-Attributes/P03-Quality-Attributes.md) |
| `AR-P04` | PROMPT 04 — Evaluation | skeleton | diagnostic | B | [P04-Evaluation.md](../02-engineering/architecture-review/P04-Evaluation/P04-Evaluation.md) |
| `AR-P05` | PROMPT 05 — Recommendations | skeleton | implementation | B | [P05-Recommendations.md](../02-engineering/architecture-review/P05-Recommendations/P05-Recommendations.md) |
| `AR-P06` | PROMPT 06 — Roadmap | skeleton | planning | B | [P06-Roadmap.md](../02-engineering/architecture-review/P06-Roadmap/P06-Roadmap.md) |
| `AR-P07` | PROMPT 07 — Architecture Review Master Orchestrator | skeleton | orchestration | A | [P07-Architecture-Review-Orchestrator.md](../02-engineering/architecture-review/P07-Orchestrator/P07-Architecture-Review-Orchestrator.md) |

## `02-engineering/codebase-audit`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `AUDIT-P01` | PROMPT 01 — Scope, Environment & Audit Contract | operational | diagnostic | B | [P01-Audit-Environment-Bootstrap.md](../02-engineering/codebase-audit/P01-Bootstrap/P01-Audit-Environment-Bootstrap.md) |
| `AUDIT-P02` | PROMPT 02 — Structural Mapping | operational | diagnostic | B | [P02-Structural-Mapping.md](../02-engineering/codebase-audit/P02-Structure/P02-Structural-Mapping.md) |
| `AUDIT-P03` | PROMPT 03 — Architecture Recovery | operational | diagnostic | B | [P03-Architectural-Analysis.md](../02-engineering/codebase-audit/P03-Architecture/P03-Architectural-Analysis.md) |
| `AUDIT-P04` | PROMPT 04 — Code Quality & Maintainability | operational | diagnostic | B | [P04-Code-Quality-Maintainability.md](../02-engineering/codebase-audit/P04-Quality/P04-Code-Quality-Maintainability.md) |
| `AUDIT-P05` | PROMPT 05 — Tests, Dependencies & Build Health | operational | diagnostic | B | [P05-Tests-Dependencies-Health.md](../02-engineering/codebase-audit/P05-Tests-Deps/P05-Tests-Dependencies-Health.md) |
| `AUDIT-P06` | PROMPT 06 — Security Surface & Documentation | operational | diagnostic | A | [P06-Security-Surface-Documentation.md](../02-engineering/codebase-audit/P06-Security-Docs/P06-Security-Surface-Documentation.md) |
| `AUDIT-P07` | PROMPT 07 — Findings Synthesis & Prioritisation | operational | diagnostic | B | [P07-Findings-Synthesis-Prioritization.md](../02-engineering/codebase-audit/P07-Findings/P07-Findings-Synthesis-Prioritization.md) |
| `AUDIT-P08` | PROMPT 08 — Improvement Roadmap & Final Report | operational | planning | B | [P08-Improvement-Roadmap-Report.md](../02-engineering/codebase-audit/P08-Roadmap/P08-Improvement-Roadmap-Report.md) |
| `AUDIT-P09` | PROMPT 09 — Deep Codebase Audit Master Orchestrator | operational | orchestration | B | [P09-Deep-Codebase-Audit-Orchestrator.md](../02-engineering/codebase-audit/P09-Orchestrator/P09-Deep-Codebase-Audit-Orchestrator.md) |

## `02-engineering/feature-completion`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `FC-P01` | PROMPT 01 — Completion Contract | operational | planning | A | [P01-Completion-Contract.md](../02-engineering/feature-completion/P01-Contract/P01-Completion-Contract.md) |
| `FC-P02` | PROMPT 02 — Layer Inventory & Gap Map | operational | diagnostic | A | [P02-Layer-Gap-Map.md](../02-engineering/feature-completion/P02-Layer-Map/P02-Layer-Gap-Map.md) |
| `FC-P03` | PROMPT 03 — Layer Implementation | operational | implementation | B | [P03-Layer-Implementation.md](../02-engineering/feature-completion/P03-Implementation/P03-Layer-Implementation.md) |
| `FC-P04` | PROMPT 04 — End-to-End Acceptance | operational | diagnostic | B | [P04-End-to-End-Acceptance.md](../02-engineering/feature-completion/P04-Acceptance/P04-End-to-End-Acceptance.md) |

## `02-engineering/feature-design-suggestion`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `FD-P01` | PROMPT 01 — Context Gathering | skeleton | implementation | B | [P01-Context-Gathering.md](../02-engineering/feature-design-suggestion/P01-Context/P01-Context-Gathering.md) |
| `FD-P02` | PROMPT 02 — Problem Framing | skeleton | planning | B | [P02-Problem-Framing.md](../02-engineering/feature-design-suggestion/P02-Problem-Framing/P02-Problem-Framing.md) |
| `FD-P03` | PROMPT 03 — Ideation | skeleton | planning | B | [P03-Ideation.md](../02-engineering/feature-design-suggestion/P03-Ideation/P03-Ideation.md) |
| `FD-P04` | PROMPT 04 — Design | skeleton | planning | A | [P04-Design.md](../02-engineering/feature-design-suggestion/P04-Design/P04-Design.md) |
| `FD-P05` | PROMPT 05 — Trade-offs & Risks | skeleton | planning | B | [P05-Tradeoffs-Risks.md](../02-engineering/feature-design-suggestion/P05-Tradeoffs/P05-Tradeoffs-Risks.md) |
| `FD-P06` | PROMPT 06 — Specification | skeleton | planning | B | [P06-Specification.md](../02-engineering/feature-design-suggestion/P06-Specification/P06-Specification.md) |
| `FD-P07` | PROMPT 07 — Feature Design Master Orchestrator | skeleton | orchestration | A | [P07-Feature-Design-Orchestrator.md](../02-engineering/feature-design-suggestion/P07-Orchestrator/P07-Feature-Design-Orchestrator.md) |

## `02-engineering/from-scratch`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `FS-P01` | PROMPT 01 — Vision & Requirements Clarification | skeleton | planning | B | [P01-Vision-Requirements-Clarification.md](../02-engineering/from-scratch/P01-Vision/P01-Vision-Requirements-Clarification.md) |
| `FS-P02` | PROMPT 02 — High-Level Architecture | skeleton | planning | A | [P02-High-Level-Architecture.md](../02-engineering/from-scratch/P02-Architecture/P02-High-Level-Architecture.md) |
| `FS-P03` | PROMPT 03 — Stack & Tooling Decision | skeleton | implementation | C | [P03-Stack-Tooling-Decision.md](../02-engineering/from-scratch/P03-Stack-Decision/P03-Stack-Tooling-Decision.md) |
| `FS-P04` | PROMPT 04 — Project Scaffolding | skeleton | implementation | B | [P04-Project-Scaffolding.md](../02-engineering/from-scratch/P04-Scaffold/P04-Project-Scaffolding.md) |
| `FS-P05` | PROMPT 05 — Core Implementation | skeleton | implementation | B | [P05-Core-Implementation.md](../02-engineering/from-scratch/P05-Core-Implementation/P05-Core-Implementation.md) |
| `FS-P06` | PROMPT 06 — Testing & Quality | skeleton | implementation | B | [P06-Testing-Quality.md](../02-engineering/from-scratch/P06-Testing-Quality/P06-Testing-Quality.md) |
| `FS-P07` | PROMPT 07 — Documentation & Polish | skeleton | implementation | B | [P07-Documentation-Polish.md](../02-engineering/from-scratch/P07-Docs-Polish/P07-Documentation-Polish.md) |
| `FS-P08` | PROMPT 08 — From-Scratch Project Master Orchestrator | skeleton | orchestration | A | [P08-From-Scratch-Project-Orchestrator.md](../02-engineering/from-scratch/P08-Orchestrator/P08-From-Scratch-Project-Orchestrator.md) |

## `02-engineering/patterns-strategies-methods`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `PS-P01` | PROMPT 01 — Context & Goals | skeleton | planning | B | [P01-Context-Goals.md](../02-engineering/patterns-strategies-methods/P01-Context/P01-Context-Goals.md) |
| `PS-P02` | PROMPT 02 — Problem Analysis | skeleton | diagnostic | B | [P02-Problem-Analysis.md](../02-engineering/patterns-strategies-methods/P02-Problem-Analysis/P02-Problem-Analysis.md) |
| `PS-P03` | PROMPT 03 — Existing Patterns Survey | skeleton | implementation | B | [P03-Existing-Patterns-Survey.md](../02-engineering/patterns-strategies-methods/P03-Existing-Patterns/P03-Existing-Patterns-Survey.md) |
| `PS-P04` | PROMPT 04 — Ideation & Adaptation | skeleton | planning | B | [P04-Ideation-Adaptation.md](../02-engineering/patterns-strategies-methods/P04-Ideation/P04-Ideation-Adaptation.md) |
| `PS-P05` | PROMPT 05 — Evaluation | skeleton | diagnostic | B | [P05-Evaluation.md](../02-engineering/patterns-strategies-methods/P05-Evaluation/P05-Evaluation.md) |
| `PS-P06` | PROMPT 06 — Specification & Guidance | skeleton | planning | B | [P06-Specification-Guidance.md](../02-engineering/patterns-strategies-methods/P06-Specification/P06-Specification-Guidance.md) |
| `PS-P07` | PROMPT 07 — Patterns, Strategies & Methods Master Orchestrat | skeleton | orchestration | A | [P07-Patterns-Strategies-Orchestrator.md](../02-engineering/patterns-strategies-methods/P07-Orchestrator/P07-Patterns-Strategies-Orchestrator.md) |

## `02-engineering/performance`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `PERF-P01` | PROMPT 01 — Context & Goals | skeleton | planning | B | [P01-Context-Goals.md](../02-engineering/performance/P01-Context/P01-Context-Goals.md) |
| `PERF-P02` | PROMPT 02 — Measurement Setup | skeleton | implementation | B | [P02-Measurement-Setup.md](../02-engineering/performance/P02-Measurement/P02-Measurement-Setup.md) |
| `PERF-P03` | PROMPT 03 — Analysis | skeleton | diagnostic | B | [P03-Analysis.md](../02-engineering/performance/P03-Analysis/P03-Analysis.md) |
| `PERF-P04` | PROMPT 04 — Bottleneck Identification | skeleton | implementation | B | [P04-Bottleneck-Identification.md](../02-engineering/performance/P04-Bottleneck-Identification/P04-Bottleneck-Identification.md) |
| `PERF-P05` | PROMPT 05 — Optimization Design | skeleton | planning | B | [P05-Optimization-Design.md](../02-engineering/performance/P05-Optimization-Design/P05-Optimization-Design.md) |
| `PERF-P06` | PROMPT 06 — Implementation & Validation | skeleton | implementation | B | [P06-Implementation-Validation.md](../02-engineering/performance/P06-Implementation-Validation/P06-Implementation-Validation.md) |
| `PERF-P07` | PROMPT 07 — Performance Analysis & Optimization Master Orche | skeleton | orchestration | A | [P07-Performance-Orchestrator.md](../02-engineering/performance/P07-Orchestrator/P07-Performance-Orchestrator.md) |

## `02-engineering/project-recovery`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `REC-P01` | PROMPT 01 — Containment & State Preservation | operational | specialised | B | [P01-Containment-State-Preservation.md](../02-engineering/project-recovery/P01-Containment/P01-Containment-State-Preservation.md) |
| `REC-P02` | PROMPT 02 — Intent Reconstruction & Stopping Point | operational | diagnostic | A | [P02-Intent-Reconstruction.md](../02-engineering/project-recovery/P02-Reconstruction/P02-Intent-Reconstruction.md) |
| `REC-P03` | PROMPT 03 — Completeness Audit | operational | diagnostic | A | [P03-Completeness-Audit.md](../02-engineering/project-recovery/P03-Completeness/P03-Completeness-Audit.md) |
| `REC-P04` | PROMPT 04 — Environment & Integration Truth | operational | diagnostic | B | [P04-Integration-Environment-Truth.md](../02-engineering/project-recovery/P04-Integration/P04-Integration-Environment-Truth.md) |
| `REC-P05` | PROMPT 05 — Recovery Plan | operational | planning | A | [P05-Recovery-Plan.md](../02-engineering/project-recovery/P05-Plan/P05-Recovery-Plan.md) |
| `REC-P06` | PROMPT 06 — Incremental Recovery Execution | operational | implementation | B | [P06-Incremental-Recovery.md](../02-engineering/project-recovery/P06-Execution/P06-Incremental-Recovery.md) |
| `REC-P07` | PROMPT 07 — Acceptance, Honest Reporting & Handoff | operational | audit-remediation | B | [P07-Acceptance-Handoff.md](../02-engineering/project-recovery/P07-Acceptance/P07-Acceptance-Handoff.md) |

## `02-engineering/refactoring`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `REF-P01` | PROMPT 01 — Assessment & Goal Clarification | operational | diagnostic | A | [P01-Assessment-Goal-Clarification.md](../02-engineering/refactoring/P01-Assessment/P01-Assessment-Goal-Clarification.md) |
| `REF-P02` | PROMPT 02 — Refactoring Strategy | operational | planning | A | [P02-Refactoring-Strategy.md](../02-engineering/refactoring/P02-Strategy/P02-Refactoring-Strategy.md) |
| `REF-P03` | PROMPT 03 — Safety Net | operational | implementation | B | [P03-Safety-Net.md](../02-engineering/refactoring/P03-Safety-Net/P03-Safety-Net.md) |
| `REF-P04` | PROMPT 04 — Execution | operational | implementation | B | [P04-Execution.md](../02-engineering/refactoring/P04-Execution/P04-Execution.md) |
| `REF-P05` | PROMPT 05 — Validation | operational | diagnostic | B | [P05-Validation.md](../02-engineering/refactoring/P05-Validation/P05-Validation.md) |
| `REF-P06` | PROMPT 06 — Cleanup & Documentation | operational | implementation | B | [P06-Cleanup-Documentation.md](../02-engineering/refactoring/P06-Cleanup/P06-Cleanup-Documentation.md) |
| `REF-P07` | PROMPT 07 — Safe Refactoring Master Orchestrator | operational | orchestration | A | [P07-Safe-Refactoring-Orchestrator.md](../02-engineering/refactoring/P07-Orchestrator/P07-Safe-Refactoring-Orchestrator.md) |

## `02-engineering/rewriting-migration`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `RW-P01` | PROMPT 01 — Assessment & Goals | skeleton | diagnostic | B | [P01-Assessment-Goals.md](../02-engineering/rewriting-migration/P01-Assessment/P01-Assessment-Goals.md) |
| `RW-P02` | PROMPT 02 — Target Design | skeleton | planning | B | [P02-Target-Design.md](../02-engineering/rewriting-migration/P02-Target-Design/P02-Target-Design.md) |
| `RW-P03` | PROMPT 03 — Migration Strategy | skeleton | planning | B | [P03-Migration-Strategy.md](../02-engineering/rewriting-migration/P03-Migration-Strategy/P03-Migration-Strategy.md) |
| `RW-P04` | PROMPT 04 — Safety Net | skeleton | implementation | B | [P04-Safety-Net.md](../02-engineering/rewriting-migration/P04-Safety-Net/P04-Safety-Net.md) |
| `RW-P05` | PROMPT 05 — Incremental Migration | skeleton | implementation | B | [P05-Incremental-Migration.md](../02-engineering/rewriting-migration/P05-Incremental-Migration/P05-Incremental-Migration.md) |
| `RW-P06` | PROMPT 06 — Validation | skeleton | diagnostic | B | [P06-Validation.md](../02-engineering/rewriting-migration/P06-Validation/P06-Validation.md) |
| `RW-P07` | PROMPT 07 — Cleanup & Cutover | skeleton | implementation | B | [P07-Cleanup-Cutover.md](../02-engineering/rewriting-migration/P07-Cleanup/P07-Cleanup-Cutover.md) |
| `RW-P08` | PROMPT 08 — Rewriting & Migration Master Orchestrator | skeleton | orchestration | A | [P08-Rewriting-Migration-Orchestrator.md](../02-engineering/rewriting-migration/P08-Orchestrator/P08-Rewriting-Migration-Orchestrator.md) |

## `02-engineering/security-hardening`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `SEC-P01` | PROMPT 01 — Authorisation, Scope & Rules of Engagement | operational | planning | A | [P01-Context-Scope.md](../02-engineering/security-hardening/P01-Context/P01-Context-Scope.md) |
| `SEC-P02` | PROMPT 02 — Assets & Threat Model | operational | diagnostic | A | [P02-Threat-Model.md](../02-engineering/security-hardening/P02-Threat-Model/P02-Threat-Model.md) |
| `SEC-P03` | PROMPT 03 — Control Review (Attack Surface Analysis) | operational | diagnostic | A | [P03-Surface-Analysis.md](../02-engineering/security-hardening/P03-Surface-Analysis/P03-Surface-Analysis.md) |
| `SEC-P04` | PROMPT 04 — Findings & Triage | operational | diagnostic | A | [P04-Findings-Prioritization.md](../02-engineering/security-hardening/P04-Findings/P04-Findings-Prioritization.md) |
| `SEC-P05` | PROMPT 05 — Hardening Plan | operational | planning | A | [P05-Hardening-Plan.md](../02-engineering/security-hardening/P05-Hardening-Plan/P05-Hardening-Plan.md) |
| `SEC-P06` | PROMPT 06 — Hardening Implementation & Verification | operational | implementation | B | [P06-Implementation-Validation.md](../02-engineering/security-hardening/P06-Implementation-Validation/P06-Implementation-Validation.md) |
| `SEC-P07` | PROMPT 07 — Security Hardening Orchestrator | operational | orchestration | A | [P07-Security-Hardening-Orchestrator.md](../02-engineering/security-hardening/P07-Orchestrator/P07-Security-Hardening-Orchestrator.md) |

## `03-domains/ai-agentic`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `AI-P01` | PROMPT 01 — AI Context, Use Case & Risk | operational | planning | A | [P01-Context-Risk.md](../03-domains/ai-agentic/P01-Context/P01-Context-Risk.md) |
| `AI-P02` | PROMPT 02 — AI Application Architecture | operational | planning | A | [P02-Architecture.md](../03-domains/ai-agentic/P02-Architecture/P02-Architecture.md) |
| `AI-P03` | PROMPT 03 — Evaluation-Driven Development | operational | implementation | B | [P03-Evaluation.md](../03-domains/ai-agentic/P03-Evaluation/P03-Evaluation.md) |
| `AI-P04` | PROMPT 04 — Safety, Guardrails & Prompt-Injection Defence | operational | implementation | B | [P04-Safety-Guardrails.md](../03-domains/ai-agentic/P04-Safety/P04-Safety-Guardrails.md) |
| `AI-P05` | PROMPT 05 — AI Production Operations | operational | implementation | B | [P05-Production-Operations.md](../03-domains/ai-agentic/P05-Production/P05-Production-Operations.md) |
| `AI-P06` | PROMPT 06 — Grounded Retrieval: does the system answer from  | operational | audit-remediation | B | [P06-Grounded-Retrieval.md](../03-domains/ai-agentic/P06-Retrieval/P06-Grounded-Retrieval.md) |
| `AI-P07` | PROMPT 07 — Agent Permissions and Tool Supply Chain | operational | audit-remediation | B | [P07-Agent-Permissions.md](../03-domains/ai-agentic/P07-Permissions/P07-Agent-Permissions.md) |

## `03-domains/backend`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `BE-P01` | PROMPT 01 — Context & Constraints | skeleton | implementation | B | [P01-Context-Constraints.md](../03-domains/backend/P01-Context/P01-Context-Constraints.md) |
| `BE-P02` | PROMPT 02 — API / Interface Design | skeleton | planning | B | [P02-API-Interface-Design.md](../03-domains/backend/P02-API-Design/P02-API-Interface-Design.md) |
| `BE-P03` | PROMPT 03 — Architecture | skeleton | planning | B | [P03-Backend-Architecture.md](../03-domains/backend/P03-Architecture/P03-Backend-Architecture.md) |
| `BE-P04` | PROMPT 04 — Data & Persistence | skeleton | implementation | B | [P04-Data-Persistence.md](../03-domains/backend/P04-Data/P04-Data-Persistence.md) |
| `BE-P05` | PROMPT 05 — Implementation | skeleton | implementation | B | [P05-Implementation.md](../03-domains/backend/P05-Implementation/P05-Implementation.md) |
| `BE-P06` | PROMPT 06 — Reliability & Operability | skeleton | implementation | B | [P06-Reliability-Operability.md](../03-domains/backend/P06-Reliability/P06-Reliability-Operability.md) |
| `BE-P07` | PROMPT 07 — Validation | skeleton | diagnostic | C | [P07-Validation.md](../03-domains/backend/P07-Validation/P07-Validation.md) |
| `BE-P08` | PROMPT 08 — Backend Master Orchestrator | skeleton | orchestration | A | [P08-Backend-Orchestrator.md](../03-domains/backend/P08-Orchestrator/P08-Backend-Orchestrator.md) |

## `03-domains/cost-engineering`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `COST-P01` | PROMPT 01 — Cost Visibility & Attribution | operational | diagnostic | A | [P01-Cost-Visibility.md](../03-domains/cost-engineering/P01-Visibility/P01-Cost-Visibility.md) |
| `COST-P02` | PROMPT 02 — Waste Diagnosis | operational | diagnostic | A | [P02-Waste-Diagnosis.md](../03-domains/cost-engineering/P02-Diagnosis/P02-Waste-Diagnosis.md) |
| `COST-P03` | PROMPT 03 — Optimisation | operational | implementation | C | [P03-Optimisation.md](../03-domains/cost-engineering/P03-Optimisation/P03-Optimisation.md) |
| `COST-P04` | PROMPT 04 — Guardrails & Unit Economics | operational | planning | B | [P04-Guardrails-Unit-Economics.md](../03-domains/cost-engineering/P04-Guardrails/P04-Guardrails-Unit-Economics.md) |

## `03-domains/data-engineering`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `DE-P01` | PROMPT 01 — Pipeline Reliability: make the data trustworthy  | operational | audit-remediation | B | [P01-Pipeline-Reliability.md](../03-domains/data-engineering/P01-Pipelines/P01-Pipeline-Reliability.md) |
| `DE-P02` | PROMPT 02 — Backfill and Reconciliation | operational | implementation | C | [P02-Backfill-Reconciliation.md](../03-domains/data-engineering/P02-Backfills/P02-Backfill-Reconciliation.md) |

## `03-domains/data-ml-ai`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `ML-P01` | PROMPT 01 — Context & Constraints | skeleton | implementation | B | [P01-Context-Constraints.md](../03-domains/data-ml-ai/P01-Context/P01-Context-Constraints.md) |
| `ML-P02` | PROMPT 02 — Problem Framing | skeleton | planning | B | [P02-Problem-Framing.md](../03-domains/data-ml-ai/P02-Problem-Framing/P02-Problem-Framing.md) |
| `ML-P03` | PROMPT 03 — Data Assessment | skeleton | diagnostic | B | [P03-Data-Assessment.md](../03-domains/data-ml-ai/P03-Data/P03-Data-Assessment.md) |
| `ML-P04` | PROMPT 04 — Approach Design | skeleton | planning | B | [P04-Approach-Design.md](../03-domains/data-ml-ai/P04-Approach/P04-Approach-Design.md) |
| `ML-P05` | PROMPT 05 — Implementation | skeleton | implementation | B | [P05-Implementation.md](../03-domains/data-ml-ai/P05-Implementation/P05-Implementation.md) |
| `ML-P06` | PROMPT 06 — Evaluation | skeleton | diagnostic | B | [P06-Evaluation.md](../03-domains/data-ml-ai/P06-Evaluation/P06-Evaluation.md) |
| `ML-P07` | PROMPT 07 — Deployment & Monitoring | skeleton | implementation | C | [P07-Deployment-Monitoring.md](../03-domains/data-ml-ai/P07-Deployment-Monitoring/P07-Deployment-Monitoring.md) |
| `ML-P08` | PROMPT 08 — Data / ML / AI Master Orchestrator | skeleton | orchestration | C | [P08-Data-ML-AI-Orchestrator.md](../03-domains/data-ml-ai/P08-Orchestrator/P08-Data-ML-AI-Orchestrator.md) |

## `03-domains/database`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `DB-P01` | PROMPT 01 — Schema Truth | operational | diagnostic | A | [P01-Schema-Truth.md](../03-domains/database/P01-Schema/P01-Schema-Truth.md) |
| `DB-P02` | PROMPT 02 — Migration Design | operational | planning | A | [P02-Migration-Design.md](../03-domains/database/P02-Design/P02-Migration-Design.md) |
| `DB-P03` | PROMPT 03 — Pre-Flight Validation | operational | diagnostic | B | [P03-Preflight-Validation.md](../03-domains/database/P03-Preflight/P03-Preflight-Validation.md) |
| `DB-P04` | PROMPT 04 — Execution & Reconciliation | operational | specialised | C | [P04-Execution-Reconciliation.md](../03-domains/database/P04-Execution/P04-Execution-Reconciliation.md) |
| `DB-P05` | PROMPT 05 — Rollback & Post-Verification | operational | diagnostic | B | [P05-Rollback-Verification.md](../03-domains/database/P05-Verification/P05-Rollback-Verification.md) |

## `03-domains/devops-infra`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `DI-P01` | PROMPT 01 — Context & Constraints | skeleton | implementation | B | [P01-Context-Constraints.md](../03-domains/devops-infra/P01-Context/P01-Context-Constraints.md) |
| `DI-P02` | PROMPT 02 — Requirements & SLOs | skeleton | planning | C | [P02-Requirements-SLOs.md](../03-domains/devops-infra/P02-Requirements/P02-Requirements-SLOs.md) |
| `DI-P03` | PROMPT 03 — Architecture | skeleton | planning | C | [P03-Infra-Architecture.md](../03-domains/devops-infra/P03-Architecture/P03-Infra-Architecture.md) |
| `DI-P04` | PROMPT 04 — IaC & Pipelines | skeleton | implementation | C | [P04-IaC-Pipelines.md](../03-domains/devops-infra/P04-IaC-Pipelines/P04-IaC-Pipelines.md) |
| `DI-P05` | PROMPT 05 — Implementation | skeleton | implementation | B | [P05-Implementation.md](../03-domains/devops-infra/P05-Implementation/P05-Implementation.md) |
| `DI-P06` | PROMPT 06 — Observability & Ops | skeleton | implementation | B | [P06-Observability-Ops.md](../03-domains/devops-infra/P06-Observability/P06-Observability-Ops.md) |
| `DI-P07` | PROMPT 07 — Validation | skeleton | diagnostic | B | [P07-Validation.md](../03-domains/devops-infra/P07-Validation/P07-Validation.md) |
| `DI-P08` | PROMPT 08 — DevOps & Infrastructure Master Orchestrator | skeleton | orchestration | A | [P08-DevOps-Infra-Orchestrator.md](../03-domains/devops-infra/P08-Orchestrator/P08-DevOps-Infra-Orchestrator.md) |

## `03-domains/embedded-iot`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `IOT-P01` | PROMPT 01 — Firmware OTA with Rollback | operational | implementation | D | [P01-Firmware-OTA.md](../03-domains/embedded-iot/P01-OTA/P01-Firmware-OTA.md) |
| `IOT-P02` | PROMPT 02 — Fleet Health and Remote Recovery | operational | diagnostic | B | [P02-Fleet-Health.md](../03-domains/embedded-iot/P02-Fleet/P02-Fleet-Health.md) |

## `03-domains/frontend`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `FE-P01` | PROMPT 01 — Context & Stack | skeleton | implementation | C | [P01-Context-Stack.md](../03-domains/frontend/P01-Context/P01-Context-Stack.md) |
| `FE-P02` | PROMPT 02 — UX & Interaction Goals | skeleton | planning | B | [P02-UX-Interaction-Goals.md](../03-domains/frontend/P02-UX-Goals/P02-UX-Interaction-Goals.md) |
| `FE-P03` | PROMPT 03 — Frontend Architecture | skeleton | planning | B | [P03-Frontend-Architecture.md](../03-domains/frontend/P03-Architecture/P03-Frontend-Architecture.md) |
| `FE-P04` | PROMPT 04 — Implementation | skeleton | implementation | B | [P04-Implementation.md](../03-domains/frontend/P04-Implementation/P04-Implementation.md) |
| `FE-P05` | PROMPT 05 — State & Data | skeleton | implementation | B | [P05-State-Data.md](../03-domains/frontend/P05-State-Data/P05-State-Data.md) |
| `FE-P06` | PROMPT 06 — Quality & Accessibility | skeleton | implementation | B | [P06-Quality-Accessibility.md](../03-domains/frontend/P06-Quality/P06-Quality-Accessibility.md) |
| `FE-P07` | PROMPT 07 — Polish & Handoff | skeleton | implementation | B | [P07-Polish-Handoff.md](../03-domains/frontend/P07-Polish/P07-Polish-Handoff.md) |
| `FE-P08` | PROMPT 08 — Frontend Master Orchestrator | skeleton | orchestration | A | [P08-Frontend-Orchestrator.md](../03-domains/frontend/P08-Orchestrator/P08-Frontend-Orchestrator.md) |

## `03-domains/games`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `GD-P01` | PROMPT 01 — Vision & Player Fantasy | skeleton | planning | B | [P01-Vision-Player-Fantasy.md](../03-domains/games/P01-Vision/P01-Vision-Player-Fantasy.md) |
| `GD-P02` | PROMPT 02 — Game Design | skeleton | planning | B | [P02-Game-Design.md](../03-domains/games/P02-Design/P02-Game-Design.md) |
| `GD-P03` | PROMPT 03 — Technical Architecture | skeleton | planning | B | [P03-Technical-Architecture.md](../03-domains/games/P03-Architecture/P03-Technical-Architecture.md) |
| `GD-P04` | PROMPT 04 — Vertical Slice | skeleton | implementation | B | [P04-Vertical-Slice.md](../03-domains/games/P04-Vertical-Slice/P04-Vertical-Slice.md) |
| `GD-P05` | PROMPT 05 — Core Systems | skeleton | implementation | B | [P05-Core-Systems.md](../03-domains/games/P05-Systems/P05-Core-Systems.md) |
| `GD-P06` | PROMPT 06 — Content & Polish | skeleton | implementation | B | [P06-Content-Polish.md](../03-domains/games/P06-Content-Polish/P06-Content-Polish.md) |
| `GD-P07` | PROMPT 07 — Playtest & Validate | skeleton | diagnostic | B | [P07-Playtest-Validate.md](../03-domains/games/P07-Playtest-Validate/P07-Playtest-Validate.md) |
| `GD-P08` | PROMPT 08 — Game Development Master Orchestrator | skeleton | orchestration | A | [P08-Game-Development-Orchestrator.md](../03-domains/games/P08-Orchestrator/P08-Game-Development-Orchestrator.md) |
| `GD-P09` | PROMPT 09 — Save Data Migration and Compatibility | operational | implementation | C | [P09-Save-Migration.md](../03-domains/games/P09-Save-Migration/P09-Save-Migration.md) |
| `GD-P10` | PROMPT 10 — Multiplayer Netcode and Determinism | operational | diagnostic | B | [P10-Netcode.md](../03-domains/games/P10-Netcode/P10-Netcode.md) |

## `03-domains/mobile`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `MOB-P01` | PROMPT 01 — Store Release and Phased Rollout | operational | implementation | C | [P01-Store-Release.md](../03-domains/mobile/P01-Release/P01-Store-Release.md) |
| `MOB-P02` | PROMPT 02 — Crash Triage and Symbolication | operational | diagnostic | A | [P02-Crash-Triage.md](../03-domains/mobile/P02-Crashes/P02-Crash-Triage.md) |
| `MOB-P03` | PROMPT 03 — API Compatibility with Shipped Clients | operational | planning | B | [P03-Client-Compatibility.md](../03-domains/mobile/P03-Compatibility/P03-Client-Compatibility.md) |

## `03-domains/payments`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `PAY-P01` | PROMPT 01 — Money Model & Invariants | operational | diagnostic | A | [P01-Money-Model-Invariants.md](../03-domains/payments/P01-Model/P01-Money-Model-Invariants.md) |
| `PAY-P02` | PROMPT 02 — Idempotency & Unknown Outcomes | operational | diagnostic | B | [P02-Idempotency-Failure.md](../03-domains/payments/P02-Idempotency/P02-Idempotency-Failure.md) |
| `PAY-P03` | PROMPT 03 — Reconciliation & Change Safety | operational | specialised | C | [P03-Reconciliation-Change-Safety.md](../03-domains/payments/P03-Reconciliation/P03-Reconciliation-Change-Safety.md) |

## `03-domains/web3`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `CHAIN-P01` | PROMPT 01 — Smart Contract Threat Model and Review | operational | diagnostic | A | [P01-Contract-Threat-Model.md](../03-domains/web3/P01-Review/P01-Contract-Threat-Model.md) |
| `CHAIN-P02` | PROMPT 02 — Key Custody and Deployment Authority | operational | planning | C | [P02-Key-Custody.md](../03-domains/web3/P02-Custody/P02-Key-Custody.md) |
| `CHAIN-P03` | PROMPT 03 — Contract Upgrade and Storage Migration | operational | implementation | D | [P03-Upgrade-Migration.md](../03-domains/web3/P03-Upgrade/P03-Upgrade-Migration.md) |
| `CHAIN-P04` | PROMPT 04 — Exploit Response: funds are leaving right now | operational | specialised | D | [P04-Exploit-Response.md](../03-domains/web3/P04-Exploit/P04-Exploit-Response.md) |

## `04-process`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `A11Y-01` | PROMPT 01 — Accessibility Conformance Audit (WCAG 2.2 AA) | operational | diagnostic | A | [ACCESSIBILITY-AUDIT.md](../04-process/accessibility-audit/ACCESSIBILITY-AUDIT.md) |

## `04-process/agent-context`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `CTX-P01` | PROMPT 01 — Agent and Editor Surfaces | operational | diagnostic | A | [P01-Agent-Surfaces.md](../04-process/agent-context/P01-Surfaces/P01-Agent-Surfaces.md) |
| `CTX-P02` | PROMPT 02 — Authoring the Canonical Context | operational | implementation | B | [P02-Authoring-Canonical-Context.md](../04-process/agent-context/P02-Authoring/P02-Authoring-Canonical-Context.md) |
| `CTX-P03` | PROMPT 03 — Adherence Testing | operational | diagnostic | B | [P03-Adherence-Testing.md](../04-process/agent-context/P03-Adherence/P03-Adherence-Testing.md) |
| `CTX-P04` | PROMPT 04 — Maintenance and Drift Control | operational | continuous-improvement | B | [P04-Context-Maintenance.md](../04-process/agent-context/P04-Maintenance/P04-Context-Maintenance.md) |

## `04-process/code-review`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `CR-P01` | PROMPT 01 — Context & Goals | operational | diagnostic | A | [P01-Context-Goals.md](../04-process/code-review/P01-Context/P01-Context-Goals.md) |
| `CR-P02` | PROMPT 02 — Change Understanding | operational | diagnostic | A | [P02-Change-Understanding.md](../04-process/code-review/P02-Change-Understanding/P02-Change-Understanding.md) |
| `CR-P03` | PROMPT 03 — Structured Review | operational | diagnostic | A | [P03-Structured-Review.md](../04-process/code-review/P03-Review/P03-Structured-Review.md) |
| `CR-P04` | PROMPT 04 — Feedback Crafting | operational | implementation | A | [P04-Feedback-Crafting.md](../04-process/code-review/P04-Feedback/P04-Feedback-Crafting.md) |
| `CR-P05` | PROMPT 05 — Follow-up Support | operational | specialised | A | [P05-Follow-up-Support.md](../04-process/code-review/P05-Follow-up/P05-Follow-up-Support.md) |
| `CR-P06` | PROMPT 06 — Code Review Master Orchestrator | operational | orchestration | A | [P06-Code-Review-Orchestrator.md](../04-process/code-review/P06-Orchestrator/P06-Code-Review-Orchestrator.md) |

## `04-process/decommissioning`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `DEC-P01` | PROMPT 01 — Consumer Discovery | operational | diagnostic | A | [P01-Consumer-Discovery.md](../04-process/decommissioning/P01-Consumers/P01-Consumer-Discovery.md) |
| `DEC-P02` | PROMPT 02 — Deprecation Plan | operational | planning | A | [P02-Deprecation-Plan.md](../04-process/decommissioning/P02-Deprecation/P02-Deprecation-Plan.md) |
| `DEC-P03` | PROMPT 03 — Shutdown Execution | operational | specialised | C | [P03-Shutdown-Execution.md](../04-process/decommissioning/P03-Shutdown/P03-Shutdown-Execution.md) |
| `DEC-P04` | PROMPT 04 — Data and Asset Retirement | operational | specialised | D | [P04-Data-Asset-Retirement.md](../04-process/decommissioning/P04-Retirement/P04-Data-Asset-Retirement.md) |

## `04-process/dependency-management`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `DEP-P01` | PROMPT 01 — Dependency Inventory & Risk | operational | diagnostic | B | [P01-Dependency-Inventory-Risk.md](../04-process/dependency-management/P01-Inventory/P01-Dependency-Inventory-Risk.md) |
| `DEP-P02` | PROMPT 02 — Upgrade Planning & Breaking-Change Assessment | operational | planning | A | [P02-Upgrade-Planning.md](../04-process/dependency-management/P02-Planning/P02-Upgrade-Planning.md) |
| `DEP-P03` | PROMPT 03 — Upgrade Execution | operational | implementation | B | [P03-Upgrade-Execution.md](../04-process/dependency-management/P03-Execution/P03-Upgrade-Execution.md) |
| `DEP-P04` | PROMPT 04 — Upgrade Verification | operational | diagnostic | B | [P04-Verification.md](../04-process/dependency-management/P04-Verification/P04-Verification.md) |
| `DEP-P05` | PROMPT 05 — Dependency Policy & Ongoing Maintenance | operational | planning | B | [P05-Policy-Maintenance.md](../04-process/dependency-management/P05-Policy/P05-Policy-Maintenance.md) |

## `04-process/documentation`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `DOC-P01` | PROMPT 01 — Context and Document Products | operational | planning | A | [P01-Context-Scope.md](../04-process/documentation/P01-Context/P01-Context-Scope.md) |
| `DOC-P02` | PROMPT 02 — Documentation Inventory and Truth Audit | operational | diagnostic | A | [P02-Documentation-Inventory.md](../04-process/documentation/P02-Inventory/P02-Documentation-Inventory.md) |
| `DOC-P03` | PROMPT 03 — Audience, Jobs, and Structure | operational | planning | A | [P03-Audience-Goals.md](../04-process/documentation/P03-Audience-Goals/P03-Audience-Goals.md) |
| `DOC-P04` | PROMPT 04 — Gap Analysis and Consequence Ranking | operational | diagnostic | A | [P04-Gap-Analysis.md](../04-process/documentation/P04-Gap-Analysis/P04-Gap-Analysis.md) |
| `DOC-P05` | PROMPT 05 — Documentation Plan | operational | planning | A | [P05-Documentation-Plan.md](../04-process/documentation/P05-Plan/P05-Documentation-Plan.md) |
| `DOC-P06` | PROMPT 06 — Writing and Improvement | operational | implementation | B | [P06-Writing-Improvement.md](../04-process/documentation/P06-Writing/P06-Writing-Improvement.md) |
| `DOC-P07` | PROMPT 07 — Review, Export, and Publication | operational | diagnostic | B | [P07-Review-Validation.md](../04-process/documentation/P07-Review/P07-Review-Validation.md) |
| `DOC-P08` | PROMPT 08 — Documentation Orchestrator | operational | orchestration | B | [P08-Documentation-Orchestrator.md](../04-process/documentation/P08-Orchestrator/P08-Documentation-Orchestrator.md) |

## `04-process/feature-flags`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `FF-P01` | PROMPT 01 — Flag Inventory and Risk | operational | diagnostic | A | [P01-Flag-Inventory-Risk.md](../04-process/feature-flags/P01-Inventory/P01-Flag-Inventory-Risk.md) |
| `FF-P02` | PROMPT 02 — Flag Design and Safe Defaults | operational | planning | B | [P02-Flag-Design-Defaults.md](../04-process/feature-flags/P02-Design/P02-Flag-Design-Defaults.md) |
| `FF-P03` | PROMPT 03 — Progressive Rollout | operational | implementation | C | [P03-Progressive-Rollout.md](../04-process/feature-flags/P03-Rollout/P03-Progressive-Rollout.md) |
| `FF-P04` | PROMPT 04 — Kill-Switch Use Under Pressure | operational | specialised | C | [P04-Kill-Switch-Use.md](../04-process/feature-flags/P04-Kill-Switch/P04-Kill-Switch-Use.md) |
| `FF-P05` | PROMPT 05 — Flag Retirement | operational | implementation | B | [P05-Flag-Retirement.md](../04-process/feature-flags/P05-Retirement/P05-Flag-Retirement.md) |

## `04-process/git-operations`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `GIT-P01` | PROMPT 01 — State & Safety Check | operational | diagnostic | A | [P01-State-Safety-Check.md](../04-process/git-operations/P01-State/P01-State-Safety-Check.md) |
| `GIT-P02` | PROMPT 02 — Conflict Resolution | operational | implementation | B | [P02-Conflict-Resolution.md](../04-process/git-operations/P02-Conflicts/P02-Conflict-Resolution.md) |
| `GIT-P03` | PROMPT 03 — History Repair | operational | implementation | D | [P03-History-Repair.md](../04-process/git-operations/P03-History/P03-History-Repair.md) |
| `GIT-P04` | PROMPT 04 — Recovery | operational | specialised | B | [P04-Recovery.md](../04-process/git-operations/P04-Recovery/P04-Recovery.md) |
| `GIT-P05` | PROMPT 05 — Hygiene & Collaboration | operational | planning | A | [P05-Hygiene-Collaboration.md](../04-process/git-operations/P05-Hygiene/P05-Hygiene-Collaboration.md) |

## `04-process/governance-compliance`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `GOV-P01` | PROMPT 01 — Control Map | operational | diagnostic | A | [P01-Control-Map.md](../04-process/governance-compliance/P01-Control-Map/P01-Control-Map.md) |
| `GOV-P02` | PROMPT 02 — Evidence Collection & Control Testing | operational | diagnostic | A | [P02-Evidence-Testing.md](../04-process/governance-compliance/P02-Evidence/P02-Evidence-Testing.md) |
| `GOV-P03` | PROMPT 03 — Gap Remediation & Readiness Decision | operational | planning | A | [P03-Readiness-Decision.md](../04-process/governance-compliance/P03-Readiness/P03-Readiness-Decision.md) |

## `04-process/handover`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `HAND-P01` | PROMPT 01 — Scope, Receiver, and Terms | operational | planning | A | [P01-Handover-Scope.md](../04-process/handover/P01-Scope/P01-Handover-Scope.md) |
| `HAND-P02` | PROMPT 02 — State and Knowledge Capture | operational | diagnostic | B | [P02-State-and-Knowledge-Capture.md](../04-process/handover/P02-State/P02-State-and-Knowledge-Capture.md) |
| `HAND-P03` | PROMPT 03 — Access, Credentials, and Revocation | operational | implementation | D | [P03-Access-and-Credential-Transfer.md](../04-process/handover/P03-Access/P03-Access-and-Credential-Transfer.md) |
| `HAND-P04` | PROMPT 04 — Capability Verification by the Receiver | operational | diagnostic | C | [P04-Capability-Verification.md](../04-process/handover/P04-Competence/P04-Capability-Verification.md) |
| `HAND-P05` | PROMPT 05 — Acceptance and Closeout | operational | implementation | B | [P05-Acceptance-Closeout.md](../04-process/handover/P05-Acceptance/P05-Acceptance-Closeout.md) |

## `04-process/observability-reliability`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `OBS-P01` | PROMPT 01 — Observability Assessment | operational | diagnostic | B | [P01-Observability-Assessment.md](../04-process/observability-reliability/P01-Instrumentation/P01-Observability-Assessment.md) |
| `OBS-P02` | PROMPT 02 — Instrumentation: Logs, Metrics, Traces | operational | implementation | B | [P02-Instrumentation-Signals.md](../04-process/observability-reliability/P02-Signals/P02-Instrumentation-Signals.md) |
| `OBS-P03` | PROMPT 03 — SLOs and Alerting | operational | planning | B | [P03-SLOs-Alerting.md](../04-process/observability-reliability/P03-SLO-Alerting/P03-SLOs-Alerting.md) |
| `OBS-P04` | PROMPT 04 — On-Call Readiness and Runbooks | operational | implementation | B | [P04-Oncall-Runbooks.md](../04-process/observability-reliability/P04-Oncall-Runbooks/P04-Oncall-Runbooks.md) |
| `OBS-P05` | PROMPT 05 — Postmortem and Reliability Review | operational | audit-remediation | B | [P05-Postmortem-Reliability-Review.md](../04-process/observability-reliability/P05-Postmortem/P05-Postmortem-Reliability-Review.md) |

## `04-process/privacy-requests`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `PRIV-P01` | PROMPT 01 — Subject Data Inventory | operational | diagnostic | C | [P01-Data-Inventory.md](../04-process/privacy-requests/P01-Inventory/P01-Data-Inventory.md) |
| `PRIV-P02` | PROMPT 02 — Request Execution | operational | specialised | D | [P02-Request-Execution.md](../04-process/privacy-requests/P02-Execution/P02-Request-Execution.md) |
| `PRIV-P03` | PROMPT 03 — Retention & Systematisation | operational | planning | B | [P03-Retention-Systematise.md](../04-process/privacy-requests/P03-Retention/P03-Retention-Systematise.md) |

## `04-process/project-management`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `PM-P01` | PROMPT 01 — Context & Constraints | skeleton | implementation | C | [P01-Context-Constraints.md](../04-process/project-management/P01-Context/P01-Context-Constraints.md) |
| `PM-P02` | PROMPT 02 — Goals & Success Criteria | skeleton | planning | B | [P02-Goals-Success-Criteria.md](../04-process/project-management/P02-Goals/P02-Goals-Success-Criteria.md) |
| `PM-P03` | PROMPT 03 — Work Breakdown | skeleton | implementation | B | [P03-Work-Breakdown.md](../04-process/project-management/P03-Breakdown/P03-Work-Breakdown.md) |
| `PM-P04` | PROMPT 04 — Planning & Sequencing | skeleton | planning | B | [P04-Planning-Sequencing.md](../04-process/project-management/P04-Planning/P04-Planning-Sequencing.md) |
| `PM-P05` | PROMPT 05 — Execution Tracking | skeleton | implementation | B | [P05-Execution-Tracking.md](../04-process/project-management/P05-Execution-Tracking/P05-Execution-Tracking.md) |
| `PM-P06` | PROMPT 06 — Risk & Adjustment | skeleton | planning | B | [P06-Risk-Adjustment.md](../04-process/project-management/P06-Risk-Adjustment/P06-Risk-Adjustment.md) |
| `PM-P07` | PROMPT 07 — Review & Closeout | skeleton | diagnostic | B | [P07-Review-Closeout.md](../04-process/project-management/P07-Review/P07-Review-Closeout.md) |
| `PM-P08` | PROMPT 08 — Project Management Master Orchestrator | skeleton | orchestration | A | [P08-Project-Management-Orchestrator.md](../04-process/project-management/P08-Orchestrator/P08-Project-Management-Orchestrator.md) |

## `04-process/release-engineering`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `REL-P01` | PROMPT 01 — Release Readiness | operational | diagnostic | B | [P01-Release-Readiness.md](../04-process/release-engineering/P01-Readiness/P01-Release-Readiness.md) |
| `REL-P02` | PROMPT 02 — Versioning, Changelog & Release Notes | operational | implementation | B | [P02-Versioning-Changelog.md](../04-process/release-engineering/P02-Versioning/P02-Versioning-Changelog.md) |
| `REL-P03` | PROMPT 03 — Deployment Strategy, Migrations & Rollback | operational | planning | B | [P03-Deployment-Rollback.md](../04-process/release-engineering/P03-Deployment/P03-Deployment-Rollback.md) |
| `REL-P04` | PROMPT 04 — Post-Release Verification | operational | diagnostic | B | [P04-Post-Release-Verification.md](../04-process/release-engineering/P04-Verification/P04-Post-Release-Verification.md) |

## `04-process/research-and-development`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `RD-P01` | PROMPT 01 — Research Question | skeleton | research | B | [P01-Research-Question.md](../04-process/research-and-development/P01-Question/P01-Research-Question.md) |
| `RD-P02` | PROMPT 02 — Background Survey | skeleton | research | B | [P02-Background-Survey.md](../04-process/research-and-development/P02-Background/P02-Background-Survey.md) |
| `RD-P03` | PROMPT 03 — Hypotheses | skeleton | research | B | [P03-Hypotheses.md](../04-process/research-and-development/P03-Hypotheses/P03-Hypotheses.md) |
| `RD-P04` | PROMPT 04 — Method Design | skeleton | planning | B | [P04-Method-Design.md](../04-process/research-and-development/P04-Method/P04-Method-Design.md) |
| `RD-P05` | PROMPT 05 — Experimentation | skeleton | research | B | [P05-Experimentation.md](../04-process/research-and-development/P05-Experiment/P05-Experimentation.md) |
| `RD-P06` | PROMPT 06 — Analysis | skeleton | diagnostic | B | [P06-Analysis.md](../04-process/research-and-development/P06-Analysis/P06-Analysis.md) |
| `RD-P07` | PROMPT 07 — Decision & Next Steps | skeleton | implementation | B | [P07-Decision-Next-Steps.md](../04-process/research-and-development/P07-Decision/P07-Decision-Next-Steps.md) |
| `RD-P08` | PROMPT 08 — Research & Development Master Orchestrator | skeleton | orchestration | A | [P08-Research-Development-Orchestrator.md](../04-process/research-and-development/P08-Orchestrator/P08-Research-Development-Orchestrator.md) |

## `04-process/systems-building-improvement`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `SB-P01` | PROMPT 01 — Context & Scope | skeleton | implementation | C | [P01-Context-Scope.md](../04-process/systems-building-improvement/P01-Context/P01-Context-Scope.md) |
| `SB-P02` | PROMPT 02 — Current System Map | skeleton | implementation | B | [P02-Current-System-Map.md](../04-process/systems-building-improvement/P02-Current-System/P02-Current-System-Map.md) |
| `SB-P03` | PROMPT 03 — Desired Outcomes | skeleton | implementation | B | [P03-Desired-Outcomes.md](../04-process/systems-building-improvement/P03-Desired-Outcomes/P03-Desired-Outcomes.md) |
| `SB-P04` | PROMPT 04 — Diagnosis | skeleton | diagnostic | B | [P04-Diagnosis.md](../04-process/systems-building-improvement/P04-Diagnosis/P04-Diagnosis.md) |
| `SB-P05` | PROMPT 05 — System Design | skeleton | planning | B | [P05-System-Design.md](../04-process/systems-building-improvement/P05-Design/P05-System-Design.md) |
| `SB-P06` | PROMPT 06 — Implementation | skeleton | implementation | B | [P06-Implementation.md](../04-process/systems-building-improvement/P06-Implementation/P06-Implementation.md) |
| `SB-P07` | PROMPT 07 — Evaluation | skeleton | diagnostic | B | [P07-Evaluation.md](../04-process/systems-building-improvement/P07-Evaluation/P07-Evaluation.md) |
| `SB-P08` | PROMPT 08 — Systems-Building & Improvement Master Orchestrat | skeleton | orchestration | A | [P08-Systems-Building-Orchestrator.md](../04-process/systems-building-improvement/P08-Orchestrator/P08-Systems-Building-Orchestrator.md) |

## `04-process/testing-qa`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `QA-P01` | PROMPT 01 — Testing Context & Quality Goals | operational | planning | B | [P01-Context-Goals.md](../04-process/testing-qa/P01-Context/P01-Context-Goals.md) |
| `QA-P02` | PROMPT 02 — Current Test State Assessment | operational | diagnostic | B | [P02-Current-State-Assessment.md](../04-process/testing-qa/P02-Current-State/P02-Current-State-Assessment.md) |
| `QA-P03` | PROMPT 03 — Gap Analysis | operational | diagnostic | B | [P03-Gap-Analysis.md](../04-process/testing-qa/P03-Gap-Analysis/P03-Gap-Analysis.md) |
| `QA-P04` | PROMPT 04 — Test Strategy & Prioritisation | operational | planning | B | [P04-Strategy-Prioritization.md](../04-process/testing-qa/P04-Strategy/P04-Strategy-Prioritization.md) |
| `QA-P05` | PROMPT 05 — Test Implementation | operational | implementation | B | [P05-Implementation.md](../04-process/testing-qa/P05-Implementation/P05-Implementation.md) |
| `QA-P06` | PROMPT 06 — Validation & Measurement | operational | diagnostic | B | [P06-Validation-Measurement.md](../04-process/testing-qa/P06-Validation/P06-Validation-Measurement.md) |
| `QA-P07` | PROMPT 07 — Testing & QA Orchestrator | operational | orchestration | B | [P07-Testing-QA-Orchestrator.md](../04-process/testing-qa/P07-Orchestrator/P07-Testing-QA-Orchestrator.md) |

## `05-scenarios`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `JOBS-01` | PROMPT 01 — Background Jobs That Stop Doing Damage | operational | diagnostic | B | [BACKGROUND-JOBS.md](../05-scenarios/background-jobs/BACKGROUND-JOBS.md) |
| `DATALOSS-01` | Data-Loss Recovery | operational | specialised | D | [DATA-LOSS-RECOVERY.md](../05-scenarios/data-loss/DATA-LOSS-RECOVERY.md) |
| `DBG-01` | Systematic Debugging | operational | diagnostic | B | [SYSTEMATIC-DEBUGGING.md](../05-scenarios/debugging/SYSTEMATIC-DEBUGGING.md) |
| `DEPLOY-01` | Deploy to a Managed Platform | operational | implementation | C | [DEPLOY-TO-PLATFORM.md](../05-scenarios/deployment-target/DEPLOY-TO-PLATFORM.md) |
| `DEVENV-01` | Reproducible Dev Environment — one command, every editor, an | operational | implementation | B | [DEV-ENVIRONMENT.md](../05-scenarios/dev-environment/DEV-ENVIRONMENT.md) |
| `EMAIL-01` | PROMPT 01 — Email Deliverability: it is not in the spam fold | operational | diagnostic | B | [EMAIL-DELIVERABILITY.md](../05-scenarios/email-deliverability/EMAIL-DELIVERABILITY.md) |
| `FIXFAIL-01` | Failed Fix Escalation | operational | diagnostic | B | [FAILED-FIX-ESCALATION.md](../05-scenarios/failed-fix/FAILED-FIX-ESCALATION.md) |
| `FLAKE-01` | Flaky Test Triage | operational | diagnostic | B | [FLAKY-TEST-TRIAGE.md](../05-scenarios/flaky-tests/FLAKY-TEST-TRIAGE.md) |
| `HACK-01` | Hackathon Sprint — build the demo that gets judged | operational | autonomous-completion | B | [HACKATHON-SPRINT.md](../05-scenarios/hackathon-sprint/HACKATHON-SPRINT.md) |
| `INC-01` | Production Incident Response | operational | specialised | C | [PRODUCTION-INCIDENT.md](../05-scenarios/incident-response/PRODUCTION-INCIDENT.md) |
| `LEGACY-01` | Working with Legacy Code Prompt | skeleton | specialised | B | [WORKING-WITH-LEGACY.md](../05-scenarios/legacy-code/WORKING-WITH-LEGACY.md) |
| `SURFACE-01` | Live Surface Audit — a URL, host, or API from the outside | operational | diagnostic | B | [LIVE-SURFACE-AUDIT.md](../05-scenarios/live-surface-audit/LIVE-SURFACE-AUDIT.md) |
| `ONCALL-01` | On-Call Shift Handover | operational | specialised | B | [ONCALL-HANDOVER.md](../05-scenarios/on-call-handover/ONCALL-HANDOVER.md) |
| `ONBOARD-01` | Codebase Onboarding Prompt | skeleton | specialised | B | [CODEBASE-ONBOARDING.md](../05-scenarios/onboarding/CODEBASE-ONBOARDING.md) |
| `PERF-01` | Performance Investigation Prompt | skeleton | specialised | B | [PERFORMANCE-INVESTIGATION.md](../05-scenarios/performance-investigation/PERFORMANCE-INVESTIGATION.md) |
| `HOSTMIG-01` | Move a Running Service to Another Platform | operational | implementation | D | [PLATFORM-MIGRATION.md](../05-scenarios/platform-migration/PLATFORM-MIGRATION.md) |
| `PR-01` | Write a Strong Pull Request Prompt | skeleton | specialised | B | [WRITE-STRONG-PR.md](../05-scenarios/pr-authoring/WRITE-STRONG-PR.md) |
| `QUICK-01` | Safe Quick-Fix Prompt | skeleton | specialised | B | [SAFE-QUICK-FIX.md](../05-scenarios/quick-fixes/SAFE-QUICK-FIX.md) |
| `SECINC-01` | Security Incident Response | operational | specialised | D | [SECURITY-INCIDENT.md](../05-scenarios/security-incident/SECURITY-INCIDENT.md) |

## `06-interactive`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `INT-P02` | Contribution Intake Context Collector | skeleton | planning | A | [CONTRIBUTION-INTAKE.md](../06-interactive/context-collectors/CONTRIBUTION-INTAKE.md) |
| `INT-P03` | Greenfield / From-Scratch Intake Context Collector | skeleton | planning | A | [GREENFIELD-INTAKE.md](../06-interactive/context-collectors/GREENFIELD-INTAKE.md) |
| `INT-P01` | Project Intake Context Collector | skeleton | planning | A | [PROJECT-INTAKE.md](../06-interactive/context-collectors/PROJECT-INTAKE.md) |
| `WIZ-P01` | System Selector Wizard | skeleton | planning | A | [SYSTEM-SELECTOR.md](../06-interactive/multi-step-wizards/SYSTEM-SELECTOR.md) |

## `07-workflows`

| ID | Stage | Maturity | Mode | Risk | File |
|----|-------|----------|------|------|------|
| `WF-HANDOFF` | Handoff Contract | operational | planning | A | [HANDOFF-CONTRACT.md](../07-workflows/HANDOFF-CONTRACT.md) |
| `WF-AGENTADOPT` | Workflow — Adopting Coding Agents Without Losing Control | operational | orchestration | B | [agent-adoption.md](../07-workflows/agent-adoption.md) |
| `WF-AUDIT-REMEDIATE` | Workflow — Audit → Remediate | draft | audit-remediation | B | [audit-to-remediation.md](../07-workflows/audit-to-remediation.md) |
| `WF-IMPROVE` | Workflow — Continuous Improvement | draft | continuous-improvement | B | [continuous-improvement.md](../07-workflows/continuous-improvement.md) |
| `WF-INTEGRATE` | Workflow — Cross-Layer Integration | operational | specialised | B | [cross-layer-integration.md](../07-workflows/cross-layer-integration.md) |
| `WF-GREENFIELD` | Workflow — Greenfield Delivery | draft | autonomous-completion | B | [greenfield-delivery.md](../07-workflows/greenfield-delivery.md) |
| `WF-VERIFY` | Workflow — Independent Verification of Completed Work | operational | diagnostic | A | [independent-verification.md](../07-workflows/independent-verification.md) |
| `WF-MULTIAGENT` | Workflow — Multi-Agent Orchestration | operational | orchestration | B | [multi-agent-orchestration.md](../07-workflows/multi-agent-orchestration.md) |
| `WF-INCIDENT` | Workflow — Production Incident | draft | specialised | C | [production-incident.md](../07-workflows/production-incident.md) |
| `WF-PROMPTAUTH` | Workflow — Describe it, generate it, prove it, integrate it | operational | orchestration | A | [prompt-authoring-pipeline.md](../07-workflows/prompt-authoring-pipeline.md) |
| `WF-RECOVER` | Workflow — Recover an Abandoned or Broken Project | draft | autonomous-completion | B | [recover-abandoned-project.md](../07-workflows/recover-abandoned-project.md) |

