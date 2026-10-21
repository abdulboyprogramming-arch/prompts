# Prompt Gallery

<!-- GENERATED FILE — do not edit by hand. Run: python3 scripts/generate_gallery.py --write -->

Every prompt in the library — **351** of them — with a direct link and the situation it is for, plus **8** foundational reference documents.
Generated from the prompt files, so it cannot drift from them; CI fails if this file is stale.

**Reading the columns**

| Column | Meaning |
|---|---|
| **ID** | Stable identifier used in cross-references and the catalog |
| **Prompt** | Direct link to the file |
| **Use it for** | The situation, taken from the prompt's own objective (or its author's `Gallery:` line) |
| **Maturity** | `operational` = complete and reviewable; `draft` = usable with supervision; `skeleton` = outline, not runnable |
| **Risk** | A = read-only, B = branch changes, C = shared environments, D = destructive |

**Browse by area**

| Area | Prompts | What it is for |
|---|---:|---|
| [00-core — foundations every prompt assumes](#00-core--foundations-every-prompt-assumes) | 2 | Rules and protocols that apply to every other prompt. |
| [01-contribution — contributing to open source](#01-contribution--contributing-to-open-source) | 48 | Stage systems for contributing to an unfamiliar project. |
| [02-engineering — building, auditing, and recovering code](#02-engineering--building-auditing-and-recovering-code) | 82 | Work on an existing codebase: audit, repair, complete, upgrade. |
| [03-domains — domain-specific engineering](#03-domains--domain-specific-engineering) | 75 | Stack-specific practice: data, AI, and the domains still being built out. |
| [04-process — delivering software responsibly](#04-process--delivering-software-responsibly) | 92 | The lifecycle around code: testing, release, observability, dependency and governance. |
| [05-scenarios — single-session, high-urgency situations](#05-scenarios--single-session-high-urgency-situations) | 36 | One prompt, one session, one pressing situation. |
| [06-interactive — conversations that clarify a request](#06-interactive--conversations-that-clarify-a-request) | 4 | Use when the request is vague and needs to be scoped first. |
| [07-workflows — multi-system procedures](#07-workflows--multi-system-procedures) | 12 | Composed sequences that route between systems and stop at human gates. |

*Maturity across the library: 197 operational, 5 draft, 149 skeleton, 351 total.*

---

## 00-core — foundations every prompt assumes

Rules and protocols that apply to every other prompt.

### All prompts in this area · 2 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `GEN-P01` | [The Prompt Forge: build a runnable prompt from a description](00-core/prompt-engineering/PROMPT-FORGE.md) | The prompt — paste-ready, complete, with all ten sections filled for its archetype. <br>**Inputs:** `PROMPT_INTENT, TARGET_AGENT, OPERATING_MODE, DOMAIN, STRICTNESS, OUTPUT_SHAPE, INTERVIEW_MAX, EXISTING_PROMPT, REPO_PATH` | operational | A |
| `GEN-P02` | [Prompt Regression: prove a prompt change is an improvement](00-core/prompt-engineering/PROMPT-REGRESSION.md) | A fixture set, a run protocol, per-case results, a score against _meta/quality-rubric.md, a comparison to the baseline where one exists, a decision, and the reason… <br>**Inputs:** `PROMPT_PATH, TEST_CASES, BASELINE_RESULTS, TARGET_AGENT, RUNS_PER_CASE, REPO_PATH` | operational | A |

## 01-contribution — contributing to open source

Stage systems for contributing to an unfamiliar project.

### language-design · 8 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `LD-P01` | [Vision & Motivation](01-contribution/language-design/P01-Vision/P01-Vision-Motivation.md) | Clarify why a new language, DSL, or language extension should exist and who it is for. | skeleton | B |
| `LD-P02` | [Requirements & Constraints](01-contribution/language-design/P02-Requirements/P02-Requirements-Constraints.md) | Turn the vision into concrete requirements and constraints. | skeleton | B |
| `LD-P03` | [Language Design](01-contribution/language-design/P03-Design/P03-Language-Design.md) | Shape the core design of the language or extension. | skeleton | B |
| `LD-P04` | [Specification](01-contribution/language-design/P04-Specification/P04-Specification.md) | Produce a clear, implementable specification of the language/extension MVP. | skeleton | B |
| `LD-P05` | [Implementation Plan](01-contribution/language-design/P05-Implementation-Plan/P05-Implementation-Plan.md) | Plan how the language/extension will be realized in software. | skeleton | B |
| `LD-P06` | [Prototype](01-contribution/language-design/P06-Prototype/P06-Prototype.md) | Build a minimal viable slice that proves the core design. | skeleton | A |
| `LD-P07` | [Evaluation](01-contribution/language-design/P07-Evaluation/P07-Evaluation.md) | Assess whether the design and prototype meet the original goals and what should happen next. | skeleton | B |
| `LD-P08` | [Language Design Master Orchestrator](01-contribution/language-design/P08-Orchestrator/P08-Language-Design-Orchestrator.md) | Runs the language design system end to end: gates, routing, and final acceptance. | skeleton | A |

### open-source/general-agent · 16 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `P01` | [System Architecture, Requirements & Execution Blueprint](01-contribution/open-source/general-agent/P01-System-Architecture/P01-System-Architecture-Requirements-Execution-Blueprint.md) | Transform a capable coding agent into a systematic, evidence-driven, professional open-source contributor <br>**Inputs:** `REPO_PATH, TARGET_AREA` | operational | C |
| `P02` | [Environment & Identity Bootstrap](01-contribution/open-source/general-agent/P02-Environment-Bootstrap/P02-Environment-Identity-Bootstrap.md) | Locate and safely parse MY_DETAILS.txt (or the user-specified equivalent). <br>**Inputs:** `REPO_PATH, MY_DETAILS_FILE` | operational | B |
| `P03` | [Repository Discovery & Initial Reconnaissance](01-contribution/open-source/general-agent/P03-Repo-Discovery/P03-Repository-Discovery-Initial-Reconnaissance.md) | Confirm the exact repository identity and its relationship to any target specified in MY_DETAILS.txt. <br>**Inputs:** `REPO_PATH, BASE_REF, MY_DETAILS_FILE` | operational | C |
| `P04` | [Deep Architectural Intelligence](01-contribution/open-source/general-agent/P04-Architectural-Intelligence/P04-Deep-Architectural-Intelligence.md) | Progressively deepen the understanding begun in P03. <br>**Inputs:** `REPO_PATH, BASE_REF` | operational | C |
| `P05` | [File, Module, Dependency & Component Understanding](01-contribution/open-source/general-agent/P05-File-Module-Understanding/P05-File-Module-Dependency-Component-Understanding.md) | Select and deeply inspect the components most relevant to potential contribution areas (or explicitly requested areas). <br>**Inputs:** `TARGET_AREA` | operational | B |
| `P06` | [Git History, Branches, Releases & Development Conventions](01-contribution/open-source/general-agent/P06-Git-History-Conventions/P06-Git-History-Branches-Releases-Development-Conventions.md) | Determine the branching model actually used. <br>**Inputs:** `REPO_PATH` | operational | C |
| `P07` | [GitHub Issues, Discussions, PRs & Documented Contribution Discovery](01-contribution/open-source/general-agent/P07-GitHub-Opportunities/P07-GitHub-Issues-Discussions-PRs-Contribution-Discovery.md) | Enumerate relevant open issues, especially those suitable for external contribution. <br>**Inputs:** `GITHUB_REPO_SLUG, REPO_PATH` | operational | C |
| `P08` | [Independent Defect Discovery & Technical Opportunity Analysis](01-contribution/open-source/general-agent/P08-Independent-Discovery/P08-Independent-Defect-Discovery-Technical-Opportunity-Analysis.md) | Search for real defects, edge-case failures, missing tests, documentation inconsistencies, and other material issues that maintainers would likely welcome being… <br>**Inputs:** `BUILD_COMMAND, TEST_COMMAND` | operational | A |
| `P09` | [Opportunity Verification, Prioritization & Task Selection](01-contribution/open-source/general-agent/P09-Opportunity-Selection/P09-Opportunity-Verification-Prioritization-Task-Selection.md) | Re-verify the current status of every promising candidate (has it been fixed, claimed, duplicated, or rejected since discovery?). <br>**Inputs:** `RISK_TOLERANCE` | operational | A |
| `P10` | [Implementation Planning & Change Isolation](01-contribution/open-source/general-agent/P10-Implementation-Planning/P10-Implementation-Planning-Change-Isolation.md) | Refine the high-level approach from CONTRIBUTION_PLAN.md into a precise sequence of code/test/doc changes. <br>**Inputs:** `BRANCH, BASE_REF` | operational | B |
| `P11` | [Engineering Execution & Code Modification](01-contribution/open-source/general-agent/P11-Engineering-Execution/P11-Engineering-Execution-Code-Modification.md) | Execute the implementation checklist from P10. <br>**Inputs:** `BRANCH` | operational | B |
| `P12` | [Testing, Security, Regression Analysis & Quality Assurance](01-contribution/open-source/general-agent/P12-QA-Validation/P12-Testing-Security-Regression-Quality-Assurance.md) | Execute the project’s relevant test, lint, type-check, build, and security checks. <br>**Inputs:** `BRANCH, TEST_COMMAND` | operational | A |
| `P13` | [Git Operations, Atomic Commits & Authorized Remote Publication](01-contribution/open-source/general-agent/P13-Git-Publication/P13-Git-Operations-Commits-Authorized-Remote-Publication.md) | Stage only the intended changes. <br>**Inputs:** `BRANCH, APPROVER, REMOTE_NAME` | operational | C |
| `P14` | [Issues, Pull Requests, Review Responses & Maintainer Communication](01-contribution/open-source/general-agent/P14-PR-Communication/P14-Issues-Pull-Requests-Review-Responses-Maintainer-Communication.md) | Open a new pull request (or update an existing one) that follows the project’s PR template and conventions. <br>**Inputs:** `PR_REF, BRANCH, APPROVER` | operational | C |
| `P15` | [Continuous Contribution Management, Monitoring & Recovery](01-contribution/open-source/general-agent/P15-Continuous-Management/P15-Continuous-Contribution-Management-Recovery.md) | Maintain an accurate, up-to-date picture of all in-progress and completed contribution work. <br>**Inputs:** `TIME_BUDGET` | operational | B |
| `P16` | [Final Autonomous Contribution Orchestrator](01-contribution/open-source/general-agent/P16-Master-Orchestrator/P16-Final-Autonomous-Contribution-Orchestrator.md) | Transform the raw inputs (repository + MY_DETAILS.txt + this orchestrator) into professional open-source contribution outcomes by <br>**Inputs:** `REPO_PATH, MY_DETAILS_FILE, APPROVER, BRANCH` | operational | C |

### packages-libraries · 8 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `PKG-P01` | [Context & Package Understanding](01-contribution/packages-libraries/P01-Context/P01-Context-Package-Understanding.md) | Understand the package’s purpose, public API, users, and contribution norms. | skeleton | B |
| `PKG-P02` | [Discovery & Opportunity Identification](01-contribution/packages-libraries/P02-Discovery/P02-Discovery-Opportunity-Identification.md) | Find valuable, realistic contribution opportunities for the package. | skeleton | A |
| `PKG-P03` | [Opportunity Selection & Framing](01-contribution/packages-libraries/P03-Selection/P03-Opportunity-Selection-Framing.md) | Select the best opportunity and frame it with explicit compatibility awareness. | skeleton | B |
| `PKG-P04` | [Planning & API Impact](01-contribution/packages-libraries/P04-Planning/P04-Planning-API-Impact.md) | Plan the change while explicitly considering public API impact and versioning. | skeleton | B |
| `PKG-P05` | [Implementation](01-contribution/packages-libraries/P05-Implementation/P05-Implementation.md) | Implement the planned change cleanly, preserving public API contracts unless a deliberate breaking change was approved in the plan. | skeleton | B |
| `PKG-P06` | [Validation & Compatibility](01-contribution/packages-libraries/P06-Validation/P06-Validation-Compatibility.md) | Verify correctness, compatibility expectations, and release readiness signals. | skeleton | C |
| `PKG-P07` | [PR & Communication](01-contribution/packages-libraries/P07-PR/P07-PR-Communication.md) | Prepare a clear pull request that makes compatibility impact and verification obvious to maintainers. | skeleton | B |
| `PKG-P08` | [Package & Library Contribution Master Orchestrator](01-contribution/packages-libraries/P08-Orchestrator/P08-Package-Contribution-Orchestrator.md) | Runs the packages libraries system end to end: gates, routing, and final acceptance. | skeleton | A |

### web/general · 8 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `WEB-P01` | [Context & Project Understanding](01-contribution/web/general/P01-Context/P01-Context-Project-Understanding.md) | Build a solid understanding of the target web project before proposing or making changes. | skeleton | B |
| `WEB-P02` | [Discovery & Opportunity Identification](01-contribution/web/general/P02-Discovery/P02-Discovery-Opportunity-Identification.md) | Find valuable, realistic contribution opportunities in the web project. | skeleton | A |
| `WEB-P03` | [Opportunity Selection & Framing](01-contribution/web/general/P03-Opportunity/P03-Opportunity-Selection-Framing.md) | Select the best opportunity for the current context and frame it clearly. | skeleton | B |
| `WEB-P04` | [Planning & Design](01-contribution/web/general/P04-Planning/P04-Planning-Design.md) | Produce a concrete plan for implementing the selected work while respecting web project conventions. | skeleton | B |
| `WEB-P05` | [Implementation](01-contribution/web/general/P05-Implementation/P05-Implementation.md) | Implement the planned change cleanly, following the project’s conventions and web best practices. | skeleton | B |
| `WEB-P06` | [Validation & Quality](01-contribution/web/general/P06-Validation/P06-Validation-Quality.md) | Verify that the change is correct, polished, and meets project quality bars. | skeleton | B |
| `WEB-P07` | [PR & Communication](01-contribution/web/general/P07-PR-Communication/P07-PR-Communication.md) | Prepare and submit a clear, professional pull request that reviewers will appreciate. | skeleton | B |
| `WEB-P08` | [Web Contribution Master Orchestrator](01-contribution/web/general/P08-Orchestrator/P08-Web-Contribution-Orchestrator.md) | Runs the general system end to end: gates, routing, and final acceptance. | skeleton | A |

### web3/general · 8 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `W3-P01` | [Context & Project Understanding](01-contribution/web3/general/P01-Context/P01-Context-Project-Understanding.md) | Build a solid understanding of the target Web3 project before proposing changes. | skeleton | B |
| `W3-P02` | [Discovery & Opportunity Identification](01-contribution/web3/general/P02-Discovery/P02-Discovery-Opportunity-Identification.md) | Find valuable, realistic contribution opportunities. | skeleton | A |
| `W3-P03` | [Opportunity Selection & Framing](01-contribution/web3/general/P03-Selection/P03-Opportunity-Selection-Framing.md) | Select the best opportunity and frame it clearly, with explicit risk awareness. | skeleton | B |
| `W3-P04` | [Planning & Design](01-contribution/web3/general/P04-Planning/P04-Planning-Design.md) | Produce a concrete plan that respects Web3 constraints and project conventions. | skeleton | B |
| `W3-P05` | [Implementation](01-contribution/web3/general/P05-Implementation/P05-Implementation.md) | Implement the planned change cleanly while preserving security and project conventions. | skeleton | B |
| `W3-P06` | [Validation & Security Checks](01-contribution/web3/general/P06-Validation/P06-Validation-Security.md) | Verify correctness, safety, and quality of the change. | skeleton | B |
| `W3-P07` | [PR & Communication](01-contribution/web3/general/P07-PR/P07-PR-Communication.md) | Prepare a clear, professional pull request that helps reviewers assess correctness and risk. | skeleton | B |
| `W3-P08` | [Web3 Contribution Master Orchestrator](01-contribution/web3/general/P08-Orchestrator/P08-Web3-Contribution-Orchestrator.md) | Runs the general system end to end: gates, routing, and final acceptance. | skeleton | A |

## 02-engineering — building, auditing, and recovering code

Work on an existing codebase: audit, repair, complete, upgrade.

### All prompts in this area · 4 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `ACCESS-01` | [Access Review: who can still get in, and should they?](02-engineering/access-review/ACCESS-REVIEW.md) | A quarterly access review, a leaver, an incident, or an audit question — establish what access exists today, who still needs it, and remove the rest with proof. <br>**Inputs:** `SYSTEM_SCOPE, REVIEW_PERIOD, APPROVER, TIME_BUDGET` | operational | A |
| `SEC-ROT-01` | [Secret Rotation: drill it before you need it](02-engineering/secrets-rotation/SECRETS-ROTATION.md) | An inventory of every secret with its owner, consumers, blast radius, and rotation mechanism; a per-class runbook; a drill performed on a non-production credential… <br>**Inputs:** `REPO_PATH, TARGET_ENV, SECRET_CLASSES, APPROVER, WINDOW, ONCALL` | operational | C |
| `TENANCY-01` | [Tenant Isolation Audit](02-engineering/tenancy-audit/TENANCY-AUDIT.md) | An inventory of every data store and channel that holds tenant data, the enforcement mechanism for each, the leak paths found with reproduction steps, and an… <br>**Inputs:** `REPO_PATH, TENANCY_MODEL, DATABASES, CACHE_LAYERS, STORAGE, SEARCH, TARGET_ENV` | operational | A |
| `TIME-01` | [Time and Date Correctness Audit](02-engineering/time-correctness/TIME-CORRECTNESS.md) | An inventory of time-bearing data and logic, a defect register with reproductions, boundary tests at DST and month-end, and a rule set for the codebase. <br>**Inputs:** `REPO_PATH, PRODUCT_TIME_ZONES, DATABASE, SCHEDULER, TARGET_ENV, REPORTING_PERIODS` | operational | A |

### architecture-review · 7 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `AR-P01` | [Context & Goals](02-engineering/architecture-review/P01-Context/P01-Context-Goals.md) | Establish the purpose of the system, the reasons for the review, and the specific questions the review must answer. | skeleton | B |
| `AR-P02` | [Current Architecture](02-engineering/architecture-review/P02-Current-Architecture/P02-Current-Architecture.md) | Produce an accurate, useful description of the as-is architecture. | skeleton | C |
| `AR-P03` | [Quality Attributes](02-engineering/architecture-review/P03-Quality-Attributes/P03-Quality-Attributes.md) | Identify the quality attributes that matter most for this system and define concrete scenarios that express them. | skeleton | B |
| `AR-P04` | [Evaluation](02-engineering/architecture-review/P04-Evaluation/P04-Evaluation.md) | Assess how well the current architecture supports the important quality attributes and identify significant risks and trade-offs. | skeleton | B |
| `AR-P05` | [Recommendations](02-engineering/architecture-review/P05-Recommendations/P05-Recommendations.md) | Produce concrete, justified recommendations that improve architectural fitness. | skeleton | B |
| `AR-P06` | [Roadmap](02-engineering/architecture-review/P06-Roadmap/P06-Roadmap.md) | Sequence the recommendations into a practical, risk-aware roadmap. | skeleton | B |
| `AR-P07` | [Architecture Review Master Orchestrator](02-engineering/architecture-review/P07-Orchestrator/P07-Architecture-Review-Orchestrator.md) | Runs the architecture review system end to end: gates, routing, and final acceptance. | skeleton | A |

### codebase-audit · 9 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `AUDIT-P01` | [Scope, Environment & Audit Contract](02-engineering/codebase-audit/P01-Bootstrap/P01-Audit-Environment-Bootstrap.md) | Produce a defensible audit contract: what commit is being audited, what questions the audit must answer, what is in and out of scope, what tooling is available, and… <br>**Inputs:** `REPO_PATH, AUDIT_QUESTIONS, TIME_BUDGET` | operational | B |
| `AUDIT-P02` | [Structural Mapping](02-engineering/codebase-audit/P02-Structure/P02-Structural-Mapping.md) | Answers: what are the components of this repository, how are they built and run, which files matter, and which directories are traps (generated, vendored, legacy… | operational | B |
| `AUDIT-P03` | [Architecture Recovery](02-engineering/codebase-audit/P03-Architecture/P03-Architectural-Analysis.md) | Answers: what are the real subsystems and boundaries, how does data and control flow between them, where are the load-bearing decisions, and which boundaries are… | operational | B |
| `AUDIT-P04` | [Code Quality & Maintainability](02-engineering/codebase-audit/P04-Quality/P04-Code-Quality-Maintainability.md) | Answers: where will the next change be expensive, and why? | operational | B |
| `AUDIT-P05` | [Tests, Dependencies & Build Health](02-engineering/codebase-audit/P05-Tests-Deps/P05-Tests-Dependencies-Health.md) | Answers: if we change this system tomorrow, what would catch a mistake — and what would silently ship? | operational | B |
| `AUDIT-P06` | [Security Surface & Documentation](02-engineering/codebase-audit/P06-Security-Docs/P06-Security-Surface-Documentation.md) | Answers: what does this system expose, who can reach it, where are the trust boundaries, and which review-visible weaknesses deserve a specialist engagement? <br>**Inputs:** `SECURITY_REVIEW_AUTHORISATION` | operational | A |
| `AUDIT-P07` | [Findings Synthesis & Prioritisation](02-engineering/codebase-audit/P07-Findings/P07-Findings-Synthesis-Prioritization.md) | Answers: which findings are real, how severe, how confident, and what should be done first? | operational | B |
| `AUDIT-P08` | [Improvement Roadmap & Final Report](02-engineering/codebase-audit/P08-Roadmap/P08-Improvement-Roadmap-Report.md) | Answers: what should be done, in what order, why that order, and what happens if nothing is done? <br>**Inputs:** `REPOSITORY_OWNER_CONSTRAINTS, TIME_BUDGET` | operational | B |
| `AUDIT-P09` | [Deep Codebase Audit Master Orchestrator](02-engineering/codebase-audit/P09-Orchestrator/P09-Deep-Codebase-Audit-Orchestrator.md) | Deliver a complete, internally consistent audit: scope contract → structure → architecture → quality → tests/dependencies → security/docs → validated findings →… <br>**Inputs:** `REPO_PATH, AUDIT_QUESTIONS, TIME_BUDGET, SECURITY_REVIEW_AUTHORISATION` | operational | B |

### feature-completion · 4 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `FC-P01` | [Completion Contract](02-engineering/feature-completion/P01-Contract/P01-Completion-Contract.md) | Produce a contract of observable behaviours across layers, roles, and states, plus the explicit non-goals. <br>**Inputs:** `FEATURE_REQUEST, TARGET_AREA` | operational | A |
| `FC-P02` | [Layer Inventory & Gap Map](02-engineering/feature-completion/P02-Layer-Map/P02-Layer-Gap-Map.md) | Answers: for this feature, which of the fourteen layers already exist, which are missing, and exactly where does each live or need to live? | operational | A |
| `FC-P03` | [Layer Implementation](02-engineering/feature-completion/P03-Implementation/P03-Layer-Implementation.md) | Implement the blocking and required gaps in an order that keeps the system runnable at each step, with tests for each layer's behaviour. <br>**Inputs:** `BRANCH` | operational | B |
| `FC-P04` | [End-to-End Acceptance](02-engineering/feature-completion/P04-Acceptance/P04-End-to-End-Acceptance.md) | Prove each acceptance statement from .feature/COMPLETION_CONTRACT.md, including the negative and edge cases, and identify what remains unverified. <br>**Inputs:** `TARGET_ENV, TEST_ACCOUNTS` | operational | B |

### feature-design-suggestion · 7 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `FD-P01` | [Context Gathering](02-engineering/feature-design-suggestion/P01-Context/P01-Context-Gathering.md) | Understand the product, its users, the current system capabilities, and any existing constraints or related work before proposing anything new. | skeleton | B |
| `FD-P02` | [Problem Framing](02-engineering/feature-design-suggestion/P02-Problem-Framing/P02-Problem-Framing.md) | Turn observed needs or vague ideas into a sharp, well-justified problem statement. | skeleton | B |
| `FD-P03` | [Ideation](02-engineering/feature-design-suggestion/P03-Ideation/P03-Ideation.md) | Generate a range of plausible approaches to solving the framed problem before converging. | skeleton | B |
| `FD-P04` | [Design](02-engineering/feature-design-suggestion/P04-Design/P04-Design.md) | Select and shape the preferred solution into a coherent design. | skeleton | A |
| `FD-P05` | [Trade-offs & Risks](02-engineering/feature-design-suggestion/P05-Tradeoffs/P05-Tradeoffs-Risks.md) | Make the costs, risks, and discarded alternatives visible so decisions are informed. | skeleton | B |
| `FD-P06` | [Specification](02-engineering/feature-design-suggestion/P06-Specification/P06-Specification.md) | Produce a concrete, reviewable feature specification that implementers can use. | skeleton | B |
| `FD-P07` | [Feature Design Master Orchestrator](02-engineering/feature-design-suggestion/P07-Orchestrator/P07-Feature-Design-Orchestrator.md) | Runs the feature design suggestion system end to end: gates, routing, and final acceptance. | skeleton | A |

### from-scratch · 8 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `FS-P01` | [Vision & Requirements Clarification](02-engineering/from-scratch/P01-Vision/P01-Vision-Requirements-Clarification.md) | Capture the core problem being solved and for whom. | skeleton | B |
| `FS-P02` | [High-Level Architecture](02-engineering/from-scratch/P02-Architecture/P02-High-Level-Architecture.md) | Propose a clean, appropriate architecture that satisfies the vision. | skeleton | A |
| `FS-P03` | [Stack & Tooling Decision](02-engineering/from-scratch/P03-Stack-Decision/P03-Stack-Tooling-Decision.md) | Select language(s), frameworks, major libraries, database (if any), and key infrastructure. | skeleton | C |
| `FS-P04` | [Project Scaffolding](02-engineering/from-scratch/P04-Scaffold/P04-Project-Scaffolding.md) | Initialize the repository structure. | skeleton | B |
| `FS-P05` | [Core Implementation](02-engineering/from-scratch/P05-Core-Implementation/P05-Core-Implementation.md) | Implement the highest-priority user-facing or system-critical paths first. | skeleton | B |
| `FS-P06` | [Testing & Quality](02-engineering/from-scratch/P06-Testing-Quality/P06-Testing-Quality.md) | Add meaningful automated tests for the core functionality. | skeleton | B |
| `FS-P07` | [Documentation & Polish](02-engineering/from-scratch/P07-Docs-Polish/P07-Documentation-Polish.md) | Write a clear, professional README. | skeleton | B |
| `FS-P08` | [From-Scratch Project Master Orchestrator](02-engineering/from-scratch/P08-Orchestrator/P08-From-Scratch-Project-Orchestrator.md) | Produces VISION.md, ARCHITECTURE.md, STACK.md | skeleton | A |

### patterns-strategies-methods · 7 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `PS-P01` | [Context & Goals](02-engineering/patterns-strategies-methods/P01-Context/P01-Context-Goals.md) | Understand the domain, the motivating need, and what a successful pattern or strategy should achieve. | skeleton | B |
| `PS-P02` | [Problem Analysis](02-engineering/patterns-strategies-methods/P02-Problem-Analysis/P02-Problem-Analysis.md) | Characterize the recurring problem deeply so that any proposed pattern actually addresses the real forces. | skeleton | B |
| `PS-P03` | [Existing Patterns Survey](02-engineering/patterns-strategies-methods/P03-Existing-Patterns/P03-Existing-Patterns-Survey.md) | Discover what relevant patterns, strategies, or methods already exist (in the codebase, in the literature, or in common practice). | skeleton | B |
| `PS-P04` | [Ideation & Adaptation](02-engineering/patterns-strategies-methods/P04-Ideation/P04-Ideation-Adaptation.md) | Generate candidate patterns or strategies, preferring adaptations of proven ideas when they fit. | skeleton | B |
| `PS-P05` | [Evaluation](02-engineering/patterns-strategies-methods/P05-Evaluation/P05-Evaluation.md) | Compare candidates rigorously and select the strongest approach (or a hybrid). | skeleton | B |
| `PS-P06` | [Specification & Guidance](02-engineering/patterns-strategies-methods/P06-Specification/P06-Specification-Guidance.md) | Produce a clear, practical description of the chosen pattern, strategy, or method so others can apply it. | skeleton | B |
| `PS-P07` | [Patterns, Strategies & Methods Master Orchestrator](02-engineering/patterns-strategies-methods/P07-Orchestrator/P07-Patterns-Strategies-Orchestrator.md) | Runs the patterns strategies methods system end to end: gates, routing, and final acceptance. | skeleton | A |

### performance · 7 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `PERF-P01` | [Context & Goals](02-engineering/performance/P01-Context/P01-Context-Goals.md) | Clarify what “good performance” means for this system and what constraints apply. | skeleton | B |
| `PERF-P02` | [Measurement Setup](02-engineering/performance/P02-Measurement/P02-Measurement-Setup.md) | Establish reliable ways to measure the relevant performance characteristics and capture a baseline. | skeleton | B |
| `PERF-P03` | [Analysis](02-engineering/performance/P03-Analysis/P03-Analysis.md) | Understand the current performance behavior in depth. | skeleton | B |
| `PERF-P04` | [Bottleneck Identification](02-engineering/performance/P04-Bottleneck-Identification/P04-Bottleneck-Identification.md) | Locate the actual primary constraints on performance rather than assumed ones. | skeleton | B |
| `PERF-P05` | [Optimization Design](02-engineering/performance/P05-Optimization-Design/P05-Optimization-Design.md) | Design targeted, high-leverage improvements that address the real bottlenecks. | skeleton | B |
| `PERF-P06` | [Implementation & Validation](02-engineering/performance/P06-Implementation-Validation/P06-Implementation-Validation.md) | Apply the planned optimizations carefully and prove that they improve the targeted metrics without breaking correctness. | skeleton | B |
| `PERF-P07` | [Performance Analysis & Optimization Master Orchestrator](02-engineering/performance/P07-Orchestrator/P07-Performance-Orchestrator.md) | Runs the performance system end to end: gates, routing, and final acceptance. | skeleton | A |

### project-recovery · 7 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `REC-P01` | [Containment & State Preservation](02-engineering/project-recovery/P01-Containment/P01-Containment-State-Preservation.md) | Produce a recoverable starting point and an exact record of it: Git state, uncommitted work, untracked files, running assumptions, and the safety checkpoint that… <br>**Inputs:** `REPO_PATH, WRITE_AUTHORITY` | operational | B |
| `REC-P02` | [Intent Reconstruction & Stopping Point](02-engineering/project-recovery/P02-Reconstruction/P02-Intent-Reconstruction.md) | Answers: what was being built, for whom, to what standard — and what was the author doing when they stopped? <br>**Inputs:** `USER_CONTEXT` | operational | A |
| `REC-P03` | [Completeness Audit](02-engineering/project-recovery/P03-Completeness/P03-Completeness-Audit.md) | Answers: for each requirement, how much of it is real, and what specifically is missing? | operational | A |
| `REC-P04` | [Environment & Integration Truth](02-engineering/project-recovery/P04-Integration/P04-Integration-Environment-Truth.md) | Answers: can this project be built and started here, what breaks first, and are the components actually connected? <br>**Inputs:** `TARGET_ENV` | operational | B |
| `REC-P05` | [Recovery Plan](02-engineering/project-recovery/P05-Plan/P05-Recovery-Plan.md) | Answers: what is the shortest sequence of changes that produces a working, verifiable critical flow, and what is the acceptance test for "working"? <br>**Inputs:** `ACCEPTANCE_FLOW` | operational | A |
| `REC-P06` | [Incremental Recovery Execution](02-engineering/project-recovery/P06-Execution/P06-Incremental-Recovery.md) | Implement the critical path to the acceptance flow defined in RECOVERY_PLAN.md, one increment at a time, on a dedicated recovery branch. <br>**Inputs:** `BRANCH` | operational | B |
| `REC-P07` | [Acceptance, Honest Reporting & Handoff](02-engineering/project-recovery/P07-Acceptance/P07-Acceptance-Handoff.md) | Answers: does the defined acceptance flow work end to end on this branch, and what exactly is the state of the project now? <br>**Inputs:** `TARGET_ENV` | operational | B |

### refactoring · 7 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `REF-P01` | [Assessment & Goal Clarification](02-engineering/refactoring/P01-Assessment/P01-Assessment-Goal-Clarification.md) | Answers: what pain does this area cause today, what measurable outcome would justify the work, which parts must change, and what would make us stop? <br>**Inputs:** `PERCEIVED_PROBLEM, TARGET_AREA, DEADLINE` | operational | A |
| `REF-P02` | [Refactoring Strategy](02-engineering/refactoring/P02-Strategy/P02-Refactoring-Strategy.md) | Produce a strategy: the technique, the slice sequence, the seams, the reversal points, and the estimate — sized against the stop conditions from P01. <br>**Inputs:** `TARGET_ENV, CHANGE_WINDOW` | operational | A |
| `REF-P03` | [Safety Net](02-engineering/refactoring/P03-Safety-Net/P03-Safety-Net.md) | Produce a safety net sufficient for the slices in the strategy: characterisation tests of current behaviour (including the odd parts), contract tests at seams, and… <br>**Inputs:** `REPO_PATH, PRODUCTION_DATA_SOURCE` | operational | B |
| `REF-P04` | [Execution](02-engineering/refactoring/P04-Execution/P04-Execution.md) | Execute the strategy's slices in order, keeping the trunk green, logging each step, and stopping when the stop conditions are reached. <br>**Inputs:** `BRANCH, BASE_REF` | operational | B |
| `REF-P05` | [Validation](02-engineering/refactoring/P05-Validation/P05-Validation.md) | Behaviour equivalence for the refactored area, no regression elsewhere, and movement on the P01 target — or state precisely which of these is not established. <br>**Inputs:** `HEAD_REF, BASE_REF` | operational | B |
| `REF-P06` | [Cleanup & Documentation](02-engineering/refactoring/P06-Cleanup/P06-Cleanup-Documentation.md) | Complete the change: remove the old path once telemetry proves it is unused, delete dead code with evidence, update documentation and diagrams, and write the… <br>**Inputs:** `TARGET_ENV, RETIREMENT_DATE` | operational | B |
| `REF-P07` | [Safe Refactoring Master Orchestrator](02-engineering/refactoring/P07-Orchestrator/P07-Safe-Refactoring-Orchestrator.md) | Run the stages in order, enforce the gates, route failures, and produce a final record of what was done, what changed, and what remains. <br>**Inputs:** `TARGET_AREA, APPROVER, DEADLINE` | operational | A |

### rewriting-migration · 8 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `RW-P01` | [Assessment & Goals](02-engineering/rewriting-migration/P01-Assessment/P01-Assessment-Goals.md) | Clarify the reasons for rewriting or migrating and define clear success criteria. | skeleton | B |
| `RW-P02` | [Target Design](02-engineering/rewriting-migration/P02-Target-Design/P02-Target-Design.md) | Define the desired end-state architecture, technology stack, and key design decisions for the rewritten/migrated system. | skeleton | B |
| `RW-P03` | [Migration Strategy](02-engineering/rewriting-migration/P03-Migration-Strategy/P03-Migration-Strategy.md) | Choose and document a realistic, low-risk approach to move from the current system to the target. | skeleton | B |
| `RW-P04` | [Safety Net](02-engineering/rewriting-migration/P04-Safety-Net/P04-Safety-Net.md) | Lock current behavior with characterization and critical-path tests before replacing implementations. | skeleton | B |
| `RW-P05` | [Incremental Migration](02-engineering/rewriting-migration/P05-Incremental-Migration/P05-Incremental-Migration.md) | Execute the migration in small, verified steps while keeping the system working. | skeleton | B |
| `RW-P06` | [Validation](02-engineering/rewriting-migration/P06-Validation/P06-Validation.md) | Prove that the migrated/rewritten system meets the goals and preserves required behavior. | skeleton | B |
| `RW-P07` | [Cleanup & Cutover](02-engineering/rewriting-migration/P07-Cleanup/P07-Cleanup-Cutover.md) | Remove obsolete code, finalize the transition, and leave the system in a clean, maintainable state. | skeleton | B |
| `RW-P08` | [Rewriting & Migration Master Orchestrator](02-engineering/rewriting-migration/P08-Orchestrator/P08-Rewriting-Migration-Orchestrator.md) | Runs the rewriting migration system end to end: gates, routing, and final acceptance. | skeleton | A |

### security-hardening · 7 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `SEC-P01` | [Authorisation, Scope & Rules of Engagement](02-engineering/security-hardening/P01-Context/P01-Context-Scope.md) | Answers: who authorised this work, what is in and out of scope, which techniques are permitted, how findings will be handled, and what happens if a critical issue… <br>**Inputs:** `SECURITY_AUTHORISATION, IN_SCOPE, DISCLOSURE_CONTACT, OUT_OF_SCOPE` | operational | A |
| `SEC-P02` | [Assets & Threat Model](02-engineering/security-hardening/P02-Threat-Model/P02-Threat-Model.md) | Produce an asset inventory, actor list, trust-boundary map, and a ranked set of abuse cases with the controls that should resist them. <br>**Inputs:** `TARGET_AREA, DATA_CLASSIFICATION` | operational | A |
| `SEC-P03` | [Control Review (Attack Surface Analysis)](02-engineering/security-hardening/P03-Surface-Analysis/P03-Surface-Analysis.md) | Answers: for each expected control, where is it enforced, which paths bypass it, and under what conditions does it fail? | operational | A |
| `SEC-P04` | [Findings & Triage](02-engineering/security-hardening/P04-Findings/P04-Findings-Prioritization.md) | Answers: which security weaknesses are real, how bad are they given exposure and reachability, and what is the minimum fix? <br>**Inputs:** `TARGET_ENV` | operational | A |
| `SEC-P05` | [Hardening Plan](02-engineering/security-hardening/P05-Hardening-Plan/P05-Hardening-Plan.md) | Produce an ordered remediation plan where each item is a bounded change with a verification method and a rollback, plus an explicit stop line. <br>**Inputs:** `RISK_TOLERANCE, CHANGE_WINDOW` | operational | A |
| `SEC-P06` | [Hardening Implementation & Verification](02-engineering/security-hardening/P06-Implementation-Validation/P06-Implementation-Validation.md) | Implement the approved plan items in order, with tests that demonstrate the gap before the fix and the closure after. <br>**Inputs:** `BRANCH, APPROVER` | operational | B |
| `SEC-P07` | [Security Hardening Orchestrator](02-engineering/security-hardening/P07-Orchestrator/P07-Security-Hardening-Orchestrator.md) | Run P01–P04 as read-only assessment, obtain explicit approval for P05, then run P06 for the approved items and verify independently. <br>**Inputs:** `SECURITY_AUTHORISATION, TARGET_COMMIT, APPROVER, DISCLOSURE_CONTACT` | operational | A |

## 03-domains — domain-specific engineering

Stack-specific practice: data, AI, and the domains still being built out.

### ai-agentic · 7 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `AI-P01` | [AI Context, Use Case & Risk](03-domains/ai-agentic/P01-Context/P01-Context-Risk.md) | Produce a use-case definition, a suitability verdict, a risk classification, and measurable success criteria before any prompt or architecture is written. <br>**Inputs:** `TARGET_SERVICE, WRONG_ANSWER_CONSEQUENCE` | operational | A |
| `AI-P02` | [AI Application Architecture](03-domains/ai-agentic/P02-Architecture/P02-Architecture.md) | Design a component architecture that makes model behaviour observable, constrainable, and replaceable. <br>**Inputs:** `LATENCY_BUDGET, COST_CEILING, DATA_RESIDENCY` | operational | A |
| `AI-P03` | [Evaluation-Driven Development](03-domains/ai-agentic/P03-Evaluation/P03-Evaluation.md) | Produce a versioned eval dataset, a metric suite with thresholds, and a reproducible harness runnable in CI. <br>**Inputs:** `EVAL_BUDGET, EVAL_DATASET_PATH` | operational | B |
| `AI-P04` | [Safety, Guardrails & Prompt-Injection Defence](03-domains/ai-agentic/P04-Safety/P04-Safety-Guardrails.md) | Implement input handling, output validation, tool authorisation, and detection for prompt injection and harmful output. <br>**Inputs:** `TARGET_SERVICE, APPROVER` | operational | B |
| `AI-P05` | [AI Production Operations](03-domains/ai-agentic/P05-Production/P05-Production-Operations.md) | Implement request-level telemetry, cost and latency accounting, quality monitoring, oversight checkpoints, and a safe release process for model/prompt changes. <br>**Inputs:** `TARGET_SERVICE, TARGET_ENV` | operational | B |
| `AI-P06` | [Grounded Retrieval: does the system answer from your documents?](03-domains/ai-agentic/P06-Retrieval/P06-Grounded-Retrieval.md) | A labelled evaluation set with answerable and unanswerable questions, retrieval metrics, groundedness measurement, an ablation over chunking and k, and a written… <br>**Inputs:** `REPO_PATH, CORPUS_SCOPE, EVAL_SET, EMBEDDING_MODEL, CHUNK_STRATEGY, LATENCY_BUDGET` | operational | B |
| `AI-P07` | [Agent Permissions and Tool Supply Chain](03-domains/ai-agentic/P07-Permissions/P07-Agent-Permissions.md) | A complete inventory of tools, servers, and capabilities; an effective-permission table; a least-privilege diff with each reduction applied where safe; an approval… <br>**Inputs:** `REPO_PATH, AGENT_CONFIG, ENVIRONMENT, TOOL_INVENTORY` | operational | B |

### backend · 9 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `API-VER-01` | [API Versioning and Consumer Contracts](03-domains/backend/P09-API-Versioning/P09-API-Versioning.md) | A versioning scheme, a consumer inventory, compatibility rules per change type, contract tests, a deprecation and sunset policy, and a migration path for anything… <br>**Inputs:** `API_SCOPE, CONSUMERS, CURRENT_VERSION, SUNSET_WINDOW, APPROVER` | operational | B |
| `BE-P01` | [Context & Constraints](03-domains/backend/P01-Context/P01-Context-Constraints.md) | Understand the service’s role, consumers, and hard constraints. | skeleton | B |
| `BE-P02` | [API / Interface Design](03-domains/backend/P02-API-Design/P02-API-Interface-Design.md) | Define clear contracts for the backend surface. | skeleton | B |
| `BE-P03` | [Architecture](03-domains/backend/P03-Architecture/P03-Backend-Architecture.md) | Structure the service for clarity, changeability, and operational health. | skeleton | B |
| `BE-P04` | [Data & Persistence](03-domains/backend/P04-Data/P04-Data-Persistence.md) | Design data models and persistence changes intentionally. | skeleton | B |
| `BE-P05` | [Implementation](03-domains/backend/P05-Implementation/P05-Implementation.md) | Implement the service/feature cleanly according to architecture and contracts. | skeleton | B |
| `BE-P06` | [Reliability & Operability](03-domains/backend/P06-Reliability/P06-Reliability-Operability.md) | Ensure the backend behaves well under failure and is operable in production. | skeleton | B |
| `BE-P07` | [Validation](03-domains/backend/P07-Validation/P07-Validation.md) | Verify correctness, contract fidelity, and release readiness. | skeleton | C |
| `BE-P08` | [Backend Master Orchestrator](03-domains/backend/P08-Orchestrator/P08-Backend-Orchestrator.md) | Runs the backend system end to end: gates, routing, and final acceptance. | skeleton | A |

### cost-engineering · 4 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `COST-P01` | [Cost Visibility & Attribution](03-domains/cost-engineering/P01-Visibility/P01-Cost-Visibility.md) | Answers: what did we spend, on what, attributed to whom, and what fraction is unattributable? <br>**Inputs:** `CLOUD_ACCOUNT, BILLING_EXPORT_PATH` | operational | A |
| `COST-P02` | [Waste Diagnosis](03-domains/cost-engineering/P02-Diagnosis/P02-Waste-Diagnosis.md) | Answers: for the top cost centres, what specific mechanism generates the spend, how much would removing it save, and what would break? <br>**Inputs:** `TARGET_SERVICE, BILLING_EXPORT_PATH` | operational | A |
| `COST-P03` | [Optimisation](03-domains/cost-engineering/P03-Optimisation/P03-Optimisation.md) | Execute the approved, quantified findings from P02 in order of value, each with a verification and a rollback. <br>**Inputs:** `APPROVER, TARGET_SERVICE, CHANGE_WINDOW` | operational | C |
| `COST-P04` | [Guardrails & Unit Economics](03-domains/cost-engineering/P04-Guardrails/P04-Guardrails-Unit-Economics.md) | Produce guardrails (tagging, budgets, alerts, policies) and unit economics (cost per request, per tenant, per job) with owners and thresholds. <br>**Inputs:** `COST_TARGET, VALUE_METRIC` | operational | B |

### data-engineering · 2 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `DE-P01` | [Pipeline Reliability: make the data trustworthy before it is fast](03-domains/data-engineering/P01-Pipelines/P01-Pipeline-Reliability.md) | A pipeline inventory with ownership and schedule, a failure-mode analysis, data tests for the properties that matter, freshness and volume contracts, and an… <br>**Inputs:** `REPO_PATH, PIPELINE_SCOPE, ORCHESTRATOR, WAREHOUSE, SLA_WINDOW, TARGET_ENV` | operational | B |
| `DE-P02` | [Backfill and Reconciliation](03-domains/data-engineering/P02-Backfills/P02-Backfill-Reconciliation.md) | A scoped backfill plan with a dry run, a reconciliation report proving the new data is correct, a list of affected downstream artefacts, and a rollback position. <br>**Inputs:** `TARGET_TABLE, DATE_RANGE, DOWNSTREAM_CONSUMERS, APPROVER, WAREHOUSE` | operational | C |

### data-ml-ai · 8 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `ML-P01` | [Context & Constraints](03-domains/data-ml-ai/P01-Context/P01-Context-Constraints.md) | Understand the product context, users, and constraints for the data/ML/AI work. | skeleton | B |
| `ML-P02` | [Problem Framing](03-domains/data-ml-ai/P02-Problem-Framing/P02-Problem-Framing.md) | Define the learning/prediction task and what success means. | skeleton | B |
| `ML-P03` | [Data Assessment](03-domains/data-ml-ai/P03-Data/P03-Data-Assessment.md) | Inventory available data and assess fitness for the framed problem. | skeleton | B |
| `ML-P04` | [Approach Design](03-domains/data-ml-ai/P04-Approach/P04-Approach-Design.md) | Select a practical modeling/pipeline approach and strong baselines. | skeleton | B |
| `ML-P05` | [Implementation](03-domains/data-ml-ai/P05-Implementation/P05-Implementation.md) | Build the data pipeline, features, and model/code paths cleanly. | skeleton | B |
| `ML-P06` | [Evaluation](03-domains/data-ml-ai/P06-Evaluation/P06-Evaluation.md) | Evaluate model/pipeline quality rigorously and analyze failures. | skeleton | B |
| `ML-P07` | [Deployment & Monitoring](03-domains/data-ml-ai/P07-Deployment-Monitoring/P07-Deployment-Monitoring.md) | Prepare for safe launch and ongoing quality monitoring. | skeleton | C |
| `ML-P08` | [Data / ML / AI Master Orchestrator](03-domains/data-ml-ai/P08-Orchestrator/P08-Data-ML-AI-Orchestrator.md) | Runs the data ml ai system end to end: gates, routing, and final acceptance. | skeleton | C |

### database · 5 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `DB-P01` | [Schema Truth](03-domains/database/P01-Schema/P01-Schema-Truth.md) | Answers: what tables, columns, constraints, indexes, and relationships exist; how do code models, migration history, and declarations disagree; what are the… <br>**Inputs:** `REPO_PATH, MIGRATIONS_DIR, DATABASE_ACCESS` | operational | A |
| `DB-P02` | [Migration Design](03-domains/database/P02-Design/P02-Migration-Design.md) | Produce a phased migration design (expand → migrate → contract) with compatibility analysis, backfill strategy, and explicit irreversibility decisions. <br>**Inputs:** `MIGRATIONS_DIR, CHANGE_WINDOW` | operational | A |
| `DB-P03` | [Pre-Flight Validation](03-domains/database/P03-Preflight/P03-Preflight-Validation.md) | The statements execute cleanly, in the expected duration, with the expected locking, producing the expected data state — and that you can get back. <br>**Inputs:** `PREFLIGHT_ENV, DATABASE_ACCESS` | operational | B |
| `DB-P04` | [Execution & Reconciliation](03-domains/database/P04-Execution/P04-Execution-Reconciliation.md) | Execute the validated plan against the target environment with monitoring, abort discipline, and post-run reconciliation. <br>**Inputs:** `APPROVER, TARGET_ENV, CHANGE_WINDOW` | operational | C |
| `DB-P05` | [Rollback & Post-Verification](03-domains/database/P05-Verification/P05-Rollback-Verification.md) | Prove the post-migration state is correct and stable, that the application behaves correctly against it, and that the reverse path remains executable (or is… <br>**Inputs:** `TARGET_ENV, PREVIOUS_VERSION` | operational | B |

### desktop-cli · 2 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `DESK-P01` | [CLI Distribution and Updates](03-domains/desktop-cli/P01-Distribution/P01-CLI-Distribution.md) | A distribution matrix per platform, signed and checksummed artifacts, an update mechanism with verification, a channel policy (stable/beta/nightly), and… <br>**Inputs:** `TOOL_NAME, DISTRIBUTION, PLATFORMS, PACKAGE_REGISTRY, AUTO_UPDATE, APPROVER` | operational | C |
| `DESK-P02` | [Terminal UX, Signals, and Exit Codes](03-domains/desktop-cli/P02-Terminal-UX/P02-Terminal-UX.md) | A specified behaviour matrix (TTY and non-TTY, each signal, each error class), corrected output handling, and tests that exercise it without a terminal. <br>**Inputs:** `TOOL_NAME, COMMANDS, PLATFORMS, SHELLS, TARGET_ENV` | operational | A |

### devops-infra · 8 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `DI-P01` | [Context & Constraints](03-domains/devops-infra/P01-Context/P01-Context-Constraints.md) | Understand the current operational landscape and constraints. | skeleton | B |
| `DI-P02` | [Requirements & SLOs](03-domains/devops-infra/P02-Requirements/P02-Requirements-SLOs.md) | Define delivery, reliability, and security requirements for the infra/pipeline work. | skeleton | C |
| `DI-P03` | [Architecture](03-domains/devops-infra/P03-Architecture/P03-Infra-Architecture.md) | Design environment topology and control-plane decisions. | skeleton | C |
| `DI-P04` | [IaC & Pipelines](03-domains/devops-infra/P04-IaC-Pipelines/P04-IaC-Pipelines.md) | Design infrastructure-as-code layout and CI/CD pipelines that implement the architecture safely. | skeleton | C |
| `DI-P05` | [Implementation](03-domains/devops-infra/P05-Implementation/P05-Implementation.md) | Apply infrastructure and pipeline changes with minimal blast radius. | skeleton | B |
| `DI-P06` | [Observability & Ops](03-domains/devops-infra/P06-Observability/P06-Observability-Ops.md) | Ensure the system can be monitored, diagnosed, and operated safely. | skeleton | B |
| `DI-P07` | [Validation](03-domains/devops-infra/P07-Validation/P07-Validation.md) | Verify safety, correctness, and operational readiness of the changes. | skeleton | B |
| `DI-P08` | [DevOps & Infrastructure Master Orchestrator](03-domains/devops-infra/P08-Orchestrator/P08-DevOps-Infra-Orchestrator.md) | Runs the devops infra system end to end: gates, routing, and final acceptance. | skeleton | A |

### embedded-iot · 2 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `IOT-P01` | [Firmware OTA with Rollback](03-domains/embedded-iot/P01-OTA/P01-Firmware-OTA.md) | A signed, versioned image; an update procedure with an atomic switch and tested rollback; a staged rollout with automatic abandonment; and a recovery path for… <br>**Inputs:** `DEVICE_CLASS, FIRMWARE_VERSION, FLEET_SIZE, CONNECTIVITY, POWER_SOURCE, APPROVER, ROLLBACK_SLOT` | operational | D |
| `IOT-P02` | [Fleet Health and Remote Recovery](03-domains/embedded-iot/P02-Fleet/P02-Fleet-Health.md) | A health model with explicit expectations (what a healthy device reports and how often), a triage method that separates the causes of silence, and bounded… <br>**Inputs:** `DEVICE_CLASS, FLEET_SIZE, TELEMETRY_SOURCE, HEARTBEAT_WINDOW, TARGET_ENV` | operational | B |

### frontend · 8 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `FE-P01` | [Context & Stack](03-domains/frontend/P01-Context/P01-Context-Stack.md) | Understand the product context, users, and frontend technical stack before designing or coding UI. | skeleton | C |
| `FE-P02` | [UX & Interaction Goals](03-domains/frontend/P02-UX-Goals/P02-UX-Interaction-Goals.md) | Define the interaction goals, key flows, and UI states that the implementation must support. | skeleton | B |
| `FE-P03` | [Frontend Architecture](03-domains/frontend/P03-Architecture/P03-Frontend-Architecture.md) | Design a clean component and boundary structure for the work. | skeleton | B |
| `FE-P04` | [Implementation](03-domains/frontend/P04-Implementation/P04-Implementation.md) | Implement the UI according to architecture, UX goals, and project conventions. | skeleton | B |
| `FE-P05` | [State & Data](03-domains/frontend/P05-State-Data/P05-State-Data.md) | Ensure client state, server data fetching, caching, and synchronization are correct and maintainable. | skeleton | B |
| `FE-P06` | [Quality & Accessibility](03-domains/frontend/P06-Quality/P06-Quality-Accessibility.md) | Raise the implementation to a professional quality bar. | skeleton | B |
| `FE-P07` | [Polish & Handoff](03-domains/frontend/P07-Polish/P07-Polish-Handoff.md) | Finish the slice so it is review-ready and pleasant to use. | skeleton | B |
| `FE-P08` | [Frontend Master Orchestrator](03-domains/frontend/P08-Orchestrator/P08-Frontend-Orchestrator.md) | Runs the frontend system end to end: gates, routing, and final acceptance. | skeleton | A |

### games · 10 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `GD-P01` | [Vision & Player Fantasy](03-domains/games/P01-Vision/P01-Vision-Player-Fantasy.md) | Define the core player fantasy, audience, and experience goal before mechanics or technology decisions. | skeleton | B |
| `GD-P02` | [Game Design](03-domains/games/P02-Design/P02-Game-Design.md) | Turn the vision into a concrete but minimal design for the first playable version. | skeleton | B |
| `GD-P03` | [Technical Architecture](03-domains/games/P03-Architecture/P03-Technical-Architecture.md) | Choose an appropriate technical approach for the MVP and define a clean project structure. | skeleton | B |
| `GD-P04` | [Vertical Slice](03-domains/games/P04-Vertical-Slice/P04-Vertical-Slice.md) | Build the smallest playable slice that proves the core fantasy and loop. | skeleton | B |
| `GD-P05` | [Core Systems](03-domains/games/P05-Systems/P05-Core-Systems.md) | Implement the additional systems required to support the MVP beyond the first slice. | skeleton | B |
| `GD-P06` | [Content & Polish](03-domains/games/P06-Content-Polish/P06-Content-Polish.md) | Improve playability through focused content, UX, and feedback work. | skeleton | B |
| `GD-P07` | [Playtest & Validate](03-domains/games/P07-Playtest-Validate/P07-Playtest-Validate.md) | Evaluate whether the game (or feature) delivers on its vision and is technically healthy enough to continue. | skeleton | B |
| `GD-P08` | [Game Development Master Orchestrator](03-domains/games/P08-Orchestrator/P08-Game-Development-Orchestrator.md) | Runs the games system end to end: gates, routing, and final acceptance. | skeleton | A |
| `GD-P09` | [Save Data Migration and Compatibility](03-domains/games/P09-Save-Migration/P09-Save-Migration.md) | A versioned save schema, forward migrations for every supported source version, a corruption-resistant read path, and tested evidence on real old saves. <br>**Inputs:** `SAVE_FORMAT, TARGET_VERSION, PLATFORM, CLOUD_SAVE, SUPPORT_WINDOW, APPROVER` | operational | C |
| `GD-P10` | [Multiplayer Netcode and Determinism](03-domains/games/P10-Netcode/P10-Netcode.md) | A diagnosis with measured numbers (latency, jitter, tick alignment, rollback depth), a corrected simulation or replication design where the bug is structural, and a… <br>**Inputs:** `TARGET_MODE, ENGINE, TICK_RATE, PLAYER_COUNT, REGIONS, REPRO_NOTES` | operational | B |

### mobile · 3 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `MOB-P01` | [Store Release and Phased Rollout](03-domains/mobile/P01-Release/P01-Store-Release.md) | A release plan with a signed build, store metadata, a staged rollout, a halt criterion defined *before* the rollout starts, and a post-release verification. <br>**Inputs:** `APP_ID, PLATFORM, TARGET_VERSION, TRACK, ROLLOUT_PERCENT, MIN_SUPPORTED_VERSION, APPROVER` | operational | C |
| `MOB-P02` | [Crash Triage and Symbolication](03-domains/mobile/P02-Crashes/P02-Crash-Triage.md) | A symbolicated, deduplicated crash inventory; a ranking by affected users and business impact (not raw count); a classification of each cluster (our bug /… <br>**Inputs:** `APP_ID, PLATFORM, RELEASE_VERSION, CRASH_SOURCE, SAMPLE_SIZE, TARGET_ENV` | operational | A |
| `MOB-P03` | [API Compatibility with Shipped Clients](03-domains/mobile/P03-Compatibility/P03-Client-Compatibility.md) | A client-version matrix (which versions exist, in what proportion), the compatibility contract for each supported version, a deprecation schedule, and a… <br>**Inputs:** `TARGET_SERVICE, MIN_SUPPORTED_VERSION, CLIENT_VERSIONS, DEPRECATION_WINDOW, APPROVER` | operational | B |

### payments · 3 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `PAY-P01` | [Money Model & Invariants](03-domains/payments/P01-Model/P01-Money-Model-Invariants.md) | Answers: how is money stored, computed, and rounded; what states can a payment take; and which invariants must hold across every operation? <br>**Inputs:** `REPO_PATH, SUPPORTED_CURRENCIES, PROVIDER_NAME` | operational | A |
| `PAY-P02` | [Idempotency & Unknown Outcomes](03-domains/payments/P02-Idempotency/P02-Idempotency-Failure.md) | Prove or disprove that each money-moving flow is idempotent, that unknown outcomes are handled as a state, and that no failure path can double-charge, silently… <br>**Inputs:** `PROVIDER_NAME, API_VERSION` | operational | B |
| `PAY-P03` | [Reconciliation & Change Safety](03-domains/payments/P03-Reconciliation/P03-Reconciliation-Change-Safety.md) | A working reconciliation between your records and the provider's, a drift classification with owners, and a change-safety checklist for every future money change. <br>**Inputs:** `PROVIDER_NAME, RECONCILIATION_WINDOW` | operational | C |

### web3 · 4 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `CHAIN-P01` | [Smart Contract Threat Model and Review](03-domains/web3/P01-Review/P01-Contract-Threat-Model.md) | An asset and trust inventory, an attack-surface map, ranked findings with concrete exploit paths, and a list of what was not reviewed. <br>**Inputs:** `REPO_PATH, CHAIN, CONTRACT_SCOPE, TVL_HINT, AUDIT_CONTEXT, TARGET_ENV` | operational | A |
| `CHAIN-P02` | [Key Custody and Deployment Authority](03-domains/web3/P02-Custody/P02-Key-Custody.md) | An authority matrix (role → capability → holder → threshold → delay → revocation path), a key inventory with custody tier per key, a rotation procedure that has… <br>**Inputs:** `CONTRACT_SCOPE, CHAIN, TEAM_SIZE, TREASURY_VALUE, COMPLIANCE_REGIME, TARGET_ENV` | operational | C |
| `CHAIN-P03` | [Contract Upgrade and Storage Migration](03-domains/web3/P03-Upgrade/P03-Upgrade-Migration.md) | A storage-layout diff, an upgrade plan with a fork rehearsal, an execution log, and post-upgrade verification evidence. <br>**Inputs:** `CONTRACT_SCOPE, CHAIN, TARGET_ENV, PROXY_PATTERN, FORK_BLOCK, APPROVER, TIMELOCK_DELAY` | operational | D |
| `CHAIN-P04` | [Exploit Response: funds are leaving right now](03-domains/web3/P04-Exploit/P04-Exploit-Response.md) | Immediate containment, a preserved evidence set, a written incident log with timestamps, a disclosure package for users, and a technical postmortem input. <br>**Inputs:** `TARGET_CONTRACT, CHAIN, ATTACK_TX, TREASURY_VALUE, COMMS_CHANNEL, APPROVER` | operational | D |

## 04-process — delivering software responsibly

The lifecycle around code: testing, release, observability, dependency and governance.

### All prompts in this area · 3 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `A11Y-01` | [Accessibility Conformance Audit (WCAG 2.2 AA)](04-process/accessibility-audit/ACCESSIBILITY-AUDIT.md) | A per-criterion conformance table for the audited pages, a prioritised defect list with reproductions, and a statement of what was and was not tested. <br>**Inputs:** `TARGET_URL, PAGES, LEVEL, ASSISTIVE_TECH, TARGET_ENV` | operational | A |
| `LIC-01` | [Licence Compliance: what you owe the people whose code you ship](04-process/licence-compliance/LICENCE-COMPLIANCE.md) | Work out what your dependencies actually oblige you to do when you ship, and turn that into a gate rather than a surprise in procurement. <br>**Inputs:** `REPO_PATH, DISTRIBUTION_MODEL, POLICY_LINK, APPROVER` | operational | A |
| `STD-01` | [Standards Conformance: prove the project against a named external standard](04-process/standards-conformance/STANDARDS-CONFORMANCE.md) | You have been told to comply with SOC 2, ISO 27001, PCI DSS, WCAG, a customer's security addendum, or an internal standard — and need evidence, not a claim. <br>**Inputs:** `REPO_PATH, STANDARD, POLICY_LINK, APPROVER, TIME_BUDGET` | operational | A |

### agent-context · 4 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `CTX-P01` | [Agent and Editor Surfaces](04-process/agent-context/P01-Surfaces/P01-Agent-Surfaces.md) | .agent-context/SURFACES.md — the tools in use, the files each one reads, what those files claim, which claims are true, where they conflict or duplicate, and which… <br>**Inputs:** `REPO_PATH, AGENT_TOOLS, TEAM_SIZE` | operational | A |
| `CTX-P02` | [Authoring the Canonical Context](04-process/agent-context/P02-Authoring/P02-Authoring-Canonical-Context.md) | A canonical AGENTS.md at the repository root (plus nested AGENTS.md only where a subtree genuinely differs), minimal per-tool adapters for ⟨AGENT_TOOLS⟩, and a… <br>**Inputs:** `REPO_PATH, AGENT_TOOLS, BRANCH, TEAM_SIZE` | operational | B |
| `CTX-P03` | [Adherence Testing](04-process/agent-context/P03-Adherence/P03-Adherence-Testing.md) | .agent-context/ADHERENCE.md — a set of probes, the observed behaviour per tool, the failures with their causes (missing instruction, ambiguous instruction, ignored… <br>**Inputs:** `REPO_PATH, AGENT_TOOLS, BRANCH, PROBE_BUDGET` | operational | B |
| `CTX-P04` | [Maintenance and Drift Control](04-process/agent-context/P04-Maintenance/P04-Context-Maintenance.md) | Automated checks that fail when the context is stale, an updating convention tied to real triggers, an ownership record, and a review cadence with a defined scope. <br>**Inputs:** `REPO_PATH, BRANCH, APPROVER, REVIEW_CADENCE` | operational | B |

### code-review · 6 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `CR-P01` | [Context & Goals](04-process/code-review/P01-Context/P01-Context-Goals.md) | Answers: what is this change trying to achieve, what does it touch, what risk does it carry, and what must this review establish to be worth the author's time? <br>**Inputs:** `BASE_REF, HEAD_REF, PR_DESCRIPTION, AUTHOR_INTENT` | operational | A |
| `CR-P02` | [Change Understanding](04-process/code-review/P02-Change-Understanding/P02-Change-Understanding.md) | Answers: what does this diff actually do — mechanically, semantically, and behaviourally — including the parts the description does not mention? <br>**Inputs:** `BASE_REF, HEAD_REF` | operational | A |
| `CR-P03` | [Structured Review](04-process/code-review/P03-Review/P03-Structured-Review.md) | A ranked set of findings, each with location, evidence, consequence, and a suggested direction; plus an explicit list of what was checked and found acceptable. <br>**Inputs:** `HEAD_REF, REPO_PATH` | operational | A |
| `CR-P04` | [Feedback Crafting](04-process/code-review/P04-Feedback/P04-Feedback-Crafting.md) | Produce review comments that state the problem, the evidence, and the requested change, ordered so the author knows what matters; plus a summary comment that makes… <br>**Inputs:** `REVIEW_FINDINGS_FILE, AUTHOR_CONTEXT` | operational | A |
| `CR-P05` | [Follow-up Support](04-process/code-review/P05-Follow-up/P05-Follow-up-Support.md) | A resolution for every finding, a re-verification of the fixes, and a tracked disposition for anything deferred. <br>**Inputs:** `PR_REF, AUTHOR_RESPONSES` | operational | A |
| `CR-P06` | [Code Review Master Orchestrator](04-process/code-review/P06-Orchestrator/P06-Code-Review-Orchestrator.md) | Run the stages, enforce the gates, decide when depth should increase or decrease, and produce a review record with a defensible decision. <br>**Inputs:** `BASE_REF, HEAD_REF, PR_REF, AUTHOR_CONTEXT` | operational | A |

### decommissioning · 4 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `DEC-P01` | [Consumer Discovery](04-process/decommissioning/P01-Consumers/P01-Consumer-Discovery.md) | Answers: who or what calls, reads, writes, or depends on this artefact, including the consumers that leave no trace in application logs? <br>**Inputs:** `TARGET_SERVICE, TARGET_AREA` | operational | A |
| `DEC-P02` | [Deprecation Plan](04-process/decommissioning/P02-Deprecation/P02-Deprecation-Plan.md) | A notice and migration plan per consumer, a timeline with dates, the technical deprecation mechanics (warnings, headers, flags), and an explicit fallback if… <br>**Inputs:** `TARGET_SERVICE, CHANGE_WINDOW` | operational | A |
| `DEC-P03` | [Shutdown Execution](04-process/decommissioning/P03-Shutdown/P03-Shutdown-Execution.md) | Execute the shutdown: stop new use, drain remaining traffic, confirm quiescence, and leave the system in a restorable state for a defined window. <br>**Inputs:** `TARGET_SERVICE, APPROVER, CHANGE_WINDOW` | operational | C |
| `DEC-P04` | [Data and Asset Retirement](04-process/decommissioning/P04-Retirement/P04-Data-Asset-Retirement.md) | A complete asset inventory, a retention decision per asset with an owner, deletion executed only for assets whose decisions are recorded, and a paper trail that… <br>**Inputs:** `TARGET_SERVICE, RETENTION_DAYS, APPROVER` | operational | D |

### dependency-management · 5 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `DEP-P01` | [Dependency Inventory & Risk](04-process/dependency-management/P01-Inventory/P01-Dependency-Inventory-Risk.md) | Answers: what do we depend on directly and transitively, which of those are risky, and which manifest/lockfile practices make upgrades dangerous? <br>**Inputs:** `REPO_PATH, LICENCE_POLICY_FILE` | operational | B |
| `DEP-P02` | [Upgrade Planning & Breaking-Change Assessment](04-process/dependency-management/P02-Planning/P02-Upgrade-Planning.md) | Answers: which upgrades should happen, in what order, what breaks, and how will each be proven safe? <br>**Inputs:** `RISK_TOLERANCE, CHANGE_WINDOW` | operational | A |
| `DEP-P03` | [Upgrade Execution](04-process/dependency-management/P03-Execution/P03-Upgrade-Execution.md) | Execute the plan's steps in order, one dependency family per commit, with verification after each. <br>**Inputs:** `REPO_PATH, BRANCH` | operational | B |
| `DEP-P04` | [Upgrade Verification](04-process/dependency-management/P04-Verification/P04-Verification.md) | Prove the upgrade is behaviour-preserving where required, that intended changes are actually in effect, and that nothing in the dependency graph changed in a way… <br>**Inputs:** `REPO_PATH, HEAD_REF, BASE_REF` | operational | B |
| `DEP-P05` | [Dependency Policy & Ongoing Maintenance](04-process/dependency-management/P05-Policy/P05-Policy-Maintenance.md) | Produce a written, checkable policy: pinning strategy, update cadence, who reviews automated update PRs and how, abandonment criteria with decision triggers… <br>**Inputs:** `TIME_BUDGET, APPROVER` | operational | B |

### documentation · 8 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `DOC-P01` | [Context and Document Products](04-process/documentation/P01-Context/P01-Context-Scope.md) | DOC_CONTEXT.md with the product summary, the document products in scope (each with reader, purpose, format, and definition of done), the source of truth for each… <br>**Inputs:** `REPO_PATH, DOC_PRODUCTS, AUDIENCE, APPROVER` | operational | A |
| `DOC-P02` | [Documentation Inventory and Truth Audit](04-process/documentation/P02-Inventory/P02-Documentation-Inventory.md) | DOC_INVENTORY.md — every significant document with its location, audience, source of truth, last-verified date, and a truth verdict backed by a check that was… <br>**Inputs:** `REPO_PATH, DOCS_DIR, BUILD_CHECK` | operational | A |
| `DOC-P03` | [Audience, Jobs, and Structure](04-process/documentation/P03-Audience-Goals/P03-Audience-Goals.md) | AUDIENCE_GOALS.md — personas with evidence, the top jobs per persona, the task-based structure per document product, entry points, success measures, and the… <br>**Inputs:** `DOC_PRODUCTS, REPO_PATH, SUPPORT_EVIDENCE` | operational | A |
| `DOC-P04` | [Gap Analysis and Consequence Ranking](04-process/documentation/P04-Gap-Analysis/P04-Gap-Analysis.md) | DOC_GAPS.md — each gap with the failed reader task, the evidence, the consequence, a severity class, and the fix's shape (rewrite, split, delete, generate). <br>**Inputs:** `DOC_PRODUCTS, INCIDENT_REF` | operational | A |
| `DOC-P05` | [Documentation Plan](04-process/documentation/P05-Plan/P05-Documentation-Plan.md) | DOC_PLAN.md — ordered deliverables with acceptance tests, per-item owner and review date, the maintenance mechanism per document class, the export/publish path, and… <br>**Inputs:** `DOC_PRODUCTS, TIME_BUDGET, APPROVER, CHANGE_WINDOW` | operational | A |
| `DOC-P06` | [Writing and Improvement](04-process/documentation/P06-Writing/P06-Writing-Improvement.md) | The planned documents on ⟨BRANCH⟩ in ⟨REPO_PATH⟩, each meeting its acceptance test, plus a log of what was written, what was verified and how, and what remains… <br>**Inputs:** `REPO_PATH, DOC_PRODUCTS, BRANCH, STYLE_GUIDE` | operational | B |
| `DOC-P07` | [Review, Export, and Publication](04-process/documentation/P07-Review/P07-Review-Validation.md) | A passed (or honestly failed) review against each acceptance test, verified exports where the product requires them, an approval record where required, and… <br>**Inputs:** `REPO_PATH, DOC_PRODUCTS, EXPORT_TARGET, APPROVER` | operational | B |
| `DOC-P08` | [Documentation Orchestrator](04-process/documentation/P08-Orchestrator/P08-Documentation-Orchestrator.md) | A routed run with the stages actually used, the gates recorded, and an honest statement of what was not done. <br>**Inputs:** `REPO_PATH, DOC_PRODUCTS, TIME_BUDGET, APPROVER, EXPORT_TARGET` | operational | B |

### feature-flags · 5 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `FF-P01` | [Flag Inventory and Risk](04-process/feature-flags/P01-Inventory/P01-Flag-Inventory-Risk.md) | A complete inventory of runtime switches with, per flag: identifier, type, owner, age, default state, exposure, where it is read, and risk class — plus a ranked… <br>**Inputs:** `REPO_PATH, FLAG_PROVIDER, TARGET_SERVICE` | operational | A |
| `FF-P02` | [Flag Design and Safe Defaults](04-process/feature-flags/P02-Design/P02-Flag-Design-Defaults.md) | A design record per flag: purpose and type, name, read sites, default and failure behaviour, targeting, owner, expiry or review date, test plan for both states, and… <br>**Inputs:** `TARGET_SERVICE, CHANGE_WINDOW, RISK_TOLERANCE, APPROVER` | operational | B |
| `FF-P03` | [Progressive Rollout](04-process/feature-flags/P03-Rollout/P03-Progressive-Rollout.md) | An executed or planned stage sequence with, per stage: exposure, cohort, duration, guardrail thresholds, the evidence to collect, the decision rule, and the… <br>**Inputs:** `TARGET_ENV, TARGET_SERVICE, APPROVER, CHANGE_WINDOW` | operational | C |
| `FF-P04` | [Kill-Switch Use Under Pressure](04-process/feature-flags/P04-Kill-Switch/P04-Kill-Switch-Use.md) | A recorded switch decision — observed symptom, hypothesis, expected effect, the flip, the measured result, and the residual state (including data written before the… <br>**Inputs:** `TARGET_SERVICE, INCIDENT_ID, APPROVER, TARGET_ENV` | operational | C |
| `FF-P05` | [Flag Retirement](04-process/feature-flags/P05-Retirement/P05-Flag-Retirement.md) | A removal commit that leaves one code path, no flag evaluation, no dead tests, and a record of the evidence and the residual risk. <br>**Inputs:** `REPO_PATH, BRANCH, FLAG_ID, BASE_REF, APPROVER` | operational | B |

### git-operations · 5 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `GIT-P01` | [State & Safety Check](04-process/git-operations/P01-State/P01-State-Safety-Check.md) | Answers: what is uncommitted, unpushed, in progress, recoverable, and shared — for ⟨REPO_PATH⟩ on ⟨BRANCH⟩. <br>**Inputs:** `REPO_PATH, BRANCH, BASE_REF` | operational | A |
| `GIT-P02` | [Conflict Resolution](04-process/git-operations/P02-Conflicts/P02-Conflict-Resolution.md) | Resolve every conflict with a justified decision per hunk, then prove the result preserves both intents by building and testing. <br>**Inputs:** `REPO_PATH, BRANCH, BASE_REF` | operational | B |
| `GIT-P03` | [History Repair](04-process/git-operations/P03-History/P03-History-Repair.md) | Produce the intended history with the least destructive method, on a branch whose safety has been established. <br>**Inputs:** `REPO_PATH, BRANCH, BASE_REF, SHARED_HISTORY, APPROVER` | operational | D |
| `GIT-P04` | [Recovery](04-process/git-operations/P04-Recovery/P04-Recovery.md) | Restore the lost commit, branch, or file, using git's own records, without disturbing unrelated work. <br>**Inputs:** `REPO_PATH, LOST_REF, BRANCH` | operational | B |
| `GIT-P05` | [Hygiene & Collaboration](04-process/git-operations/P05-Hygiene/P05-Hygiene-Collaboration.md) | Produce a short, enforceable convention covering branch model, commit granularity, merge strategy, review gates, tags, and the repository hazards specific to this… <br>**Inputs:** `REPO_PATH, TEAM_SIZE, RELEASE_CADENCE` | operational | A |

### governance-compliance · 3 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `GOV-P01` | [Control Map](04-process/governance-compliance/P01-Control-Map/P01-Control-Map.md) | Produce a control map: obligation → mechanism → owner → evidence → status (evidenced / weak / absent / not applicable). <br>**Inputs:** `CLAIMED_FRAMEWORKS, APPROVER` | operational | A |
| `GOV-P02` | [Evidence Collection & Control Testing](04-process/governance-compliance/P02-Evidence/P02-Evidence-Testing.md) | Prove or disprove that each evidenced/weak control from P01 operated over a defined period. <br>**Inputs:** `EVIDENCE_PERIOD, APPLICABLE_FRAMEWORKS` | operational | A |
| `GOV-P03` | [Gap Remediation & Readiness Decision](04-process/governance-compliance/P03-Readiness/P03-Readiness-Decision.md) | A remediation plan ordered by consequence, a risk-acceptance register with named owners, and a readiness statement per claim that an auditor or customer question… <br>**Inputs:** `AUDIT_DATE, APPROVER` | operational | A |

### handover · 5 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `HAND-P01` | [Scope, Receiver, and Terms](04-process/handover/P01-Scope/P01-Handover-Scope.md) | HANDOVER_SCOPE.md — the handover type, the receiver and their starting competence, the transfer inventory (assets, obligations, accesses, knowledge), what is… <br>**Inputs:** `TARGET_SERVICE, HANDOVER_RECEIVER, HANDOVER_DATE, APPROVER` | operational | A |
| `HAND-P02` | [State and Knowledge Capture](04-process/handover/P02-State/P02-State-and-Knowledge-Capture.md) | HANDOVER_STATE.md — what works and how that was proven, what is broken and what is at risk, open work with its exact position, decisions with their reasons… <br>**Inputs:** `REPO_PATH, TARGET_SERVICE, TARGET_ENV, HANDOVER_RECEIVER` | operational | B |
| `HAND-P03` | [Access, Credentials, and Revocation](04-process/handover/P03-Access/P03-Access-and-Credential-Transfer.md) | ACCESS_TRANSFER.md — every identity, role, and secret relevant to the system, its before/after holder, the transfer mechanism, the revocation performed, the… <br>**Inputs:** `TARGET_SERVICE, HANDOVER_RECEIVER, APPROVER, CHANGE_WINDOW` | operational | D |
| `HAND-P04` | [Capability Verification by the Receiver](04-process/handover/P04-Competence/P04-Capability-Verification.md) | CAPABILITY_REPORT.md — the exercise list, who performed what, evidence of success or the exact point of failure, the assistance given (and by whom), and the… <br>**Inputs:** `TARGET_ENV, HANDOVER_RECEIVER, REPO_PATH, APPROVER, CHANGE_WINDOW` | operational | C |
| `HAND-P05` | [Acceptance and Closeout](04-process/handover/P05-Acceptance/P05-Acceptance-Closeout.md) | HANDOVER_ACCEPTANCE.md — the verdict against the P01 acceptance criteria, the condition list with owners and dates, confirmation that access and obligations moved… <br>**Inputs:** `HANDOVER_RECEIVER, APPROVER, HANDOVER_DATE` | operational | B |

### observability-reliability · 5 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `OBS-P01` | [Observability Assessment](04-process/observability-reliability/P01-Instrumentation/P01-Observability-Assessment.md) | Answers: when this system breaks at 03:00, what will the responder know, how fast, and what will they still have to guess? <br>**Inputs:** `REPO_PATH, TARGET_SERVICE, OBS_DATA_SOURCE` | operational | B |
| `OBS-P02` | [Instrumentation: Logs, Metrics, Traces](04-process/observability-reliability/P02-Signals/P02-Instrumentation-Signals.md) | Implement correlation IDs, structured logging, golden-signal metrics, and trace propagation on the critical paths identified in P01. <br>**Inputs:** `IN_SCOPE` | operational | B |
| `OBS-P03` | [SLOs and Alerting](04-process/observability-reliability/P03-SLO-Alerting/P03-SLOs-Alerting.md) | Produce a small set of user-centred SLIs/SLOs with error budgets, and alert rules that fire on budget burn and hard failure — not on causes. <br>**Inputs:** `SLA_TARGET, APPROVER, ONCALL_ROTA` | operational | B |
| `OBS-P04` | [On-Call Readiness and Runbooks](04-process/observability-reliability/P04-Oncall-Runbooks/P04-Oncall-Runbooks.md) | Produce a runbook for every paging alert, plus an on-call guide covering escalation, access, and the top failure modes. <br>**Inputs:** `APPROVER, ONCALL_ROTA` | operational | B |
| `OBS-P05` | [Postmortem and Reliability Review](04-process/observability-reliability/P05-Postmortem/P05-Postmortem-Reliability-Review.md) | Produce a factual postmortem with owned actions, or a periodic reliability review that identifies systemic weakness across incidents. <br>**Inputs:** `INCIDENT_ID, TARGET_SERVICE, INCIDENT_TIMELINE_FILE` | operational | B |

### privacy-requests · 4 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `PRIV-P01` | [Subject Data Inventory](04-process/privacy-requests/P01-Inventory/P01-Data-Inventory.md) | Answers: in which systems does this subject's data exist, in what form, under what retention rule, and what did you *not* search? <br>**Inputs:** `SUBJECT_IDENTIFIERS, DATA_MAP_FILE` | operational | C |
| `PRIV-P02` | [Request Execution](04-process/privacy-requests/P02-Execution/P02-Request-Execution.md) | Export the subject's data, or delete it, with per-system verification and a complete record. <br>**Inputs:** `SUBJECT_IDENTIFIERS, VERIFICATION_METHOD, REQUEST_ID` | operational | D |
| `PRIV-P03` | [Retention & Systematisation](04-process/privacy-requests/P03-Retention/P03-Retention-Systematise.md) | A per-data-class retention schedule with enforcement, a self-service or documented request path, and the monitoring that proves deletions actually happen. <br>**Inputs:** `RETENTION_DAYS, APPROVER` | operational | B |
| `PRIV-P04` | [Deletion Verification: prove it is gone from the places you forgot](04-process/privacy-requests/P04-Verification/P04-Deletion-Verification.md) | You deleted a subject's data from the database — and now need to know whether it is still in the warehouse, the logs, the backups, the search index, or the vendor. <br>**Inputs:** `SUBJECT_SCOPE, RETENTION_DAYS, APPROVER` | operational | A |

### project-management · 8 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `PM-P01` | [Context & Constraints](04-process/project-management/P01-Context/P01-Context-Constraints.md) | Establish a clear picture of the initiative and the constraints it must operate within. | skeleton | C |
| `PM-P02` | [Goals & Success Criteria](04-process/project-management/P02-Goals/P02-Goals-Success-Criteria.md) | Define what success means and what is explicitly out of scope. | skeleton | B |
| `PM-P03` | [Work Breakdown](04-process/project-management/P03-Breakdown/P03-Work-Breakdown.md) | Decompose the initiative into actionable work packages. | skeleton | B |
| `PM-P04` | [Planning & Sequencing](04-process/project-management/P04-Planning/P04-Planning-Sequencing.md) | Sequence the work, surface dependencies, and define checkpoints. | skeleton | B |
| `PM-P05` | [Execution Tracking](04-process/project-management/P05-Execution-Tracking/P05-Execution-Tracking.md) | Keep status visible: what is done, what is in progress, what is blocked, and what is next. | skeleton | B |
| `PM-P06` | [Risk & Adjustment](04-process/project-management/P06-Risk-Adjustment/P06-Risk-Adjustment.md) | Handle emerging risks, delays, and scope pressure deliberately. | skeleton | B |
| `PM-P07` | [Review & Closeout](04-process/project-management/P07-Review/P07-Review-Closeout.md) | Evaluate outcomes against goals and capture lessons for future work. | skeleton | B |
| `PM-P08` | [Project Management Master Orchestrator](04-process/project-management/P08-Orchestrator/P08-Project-Management-Orchestrator.md) | Runs the project management system end to end: gates, routing, and final acceptance. | skeleton | A |

### release-engineering · 4 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `REL-P01` | [Release Readiness](04-process/release-engineering/P01-Readiness/P01-Release-Readiness.md) | Answers: is this exact commit safe to release, what could break for whom, and how would we undo it? <br>**Inputs:** `REPO_PATH, TARGET_COMMIT, RELEASE_VERSION, LAST_TAG` | operational | B |
| `REL-P02` | [Versioning, Changelog & Release Notes](04-process/release-engineering/P02-Versioning/P02-Versioning-Changelog.md) | Produce a correct semantic version, a changelog entry grouped by impact, and consumer-facing release notes for significant releases. <br>**Inputs:** `LAST_TAG, TARGET_COMMIT` | operational | B |
| `REL-P03` | [Deployment Strategy, Migrations & Rollback](04-process/release-engineering/P03-Deployment/P03-Deployment-Rollback.md) | Produce an executable deployment plan: strategy, order of operations, verification points, abort criteria, and rollback procedure. <br>**Inputs:** `TARGET_ENV, RELEASE_VERSION, CHANGE_WINDOW` | operational | B |
| `REL-P04` | [Post-Release Verification](04-process/release-engineering/P04-Verification/P04-Post-Release-Verification.md) | Answers: is the released version healthy by the metrics we chose before deployment, and did it do what the changelog claims? <br>**Inputs:** `TARGET_ENV, RELEASE_VERSION` | operational | B |

### research-and-development · 8 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `RD-P01` | [Research Question](04-process/research-and-development/P01-Question/P01-Research-Question.md) | Define a sharp research question tied to a real decision. | skeleton | B |
| `RD-P02` | [Background Survey](04-process/research-and-development/P02-Background/P02-Background-Survey.md) | Gather the minimum relevant prior knowledge needed to design good experiments. | skeleton | B |
| `RD-P03` | [Hypotheses](04-process/research-and-development/P03-Hypotheses/P03-Hypotheses.md) | State clear, testable hypotheses and the main alternatives under consideration. | skeleton | B |
| `RD-P04` | [Method Design](04-process/research-and-development/P04-Method/P04-Method-Design.md) | Design the smallest set of experiments, spikes, or measurements that can resolve the key uncertainties. | skeleton | B |
| `RD-P05` | [Experimentation](04-process/research-and-development/P05-Experiment/P05-Experimentation.md) | Execute the plan and collect evidence carefully. | skeleton | B |
| `RD-P06` | [Analysis](04-process/research-and-development/P06-Analysis/P06-Analysis.md) | Interpret the evidence against the original criteria and hypotheses. | skeleton | B |
| `RD-P07` | [Decision & Next Steps](04-process/research-and-development/P07-Decision/P07-Decision-Next-Steps.md) | Turn analysis into a clear recommendation. | skeleton | B |
| `RD-P08` | [Research & Development Master Orchestrator](04-process/research-and-development/P08-Orchestrator/P08-Research-Development-Orchestrator.md) | Runs the research and development system end to end: gates, routing, and final acceptance. | skeleton | A |

### systems-building-improvement · 8 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `SB-P01` | [Context & Scope](04-process/systems-building-improvement/P01-Context/P01-Context-Scope.md) | Clarify which system of work is under review and why improvement matters. | skeleton | C |
| `SB-P02` | [Current System Map](04-process/systems-building-improvement/P02-Current-System/P02-Current-System-Map.md) | Document how the system actually works today, not how it is supposed to work. | skeleton | B |
| `SB-P03` | [Desired Outcomes](04-process/systems-building-improvement/P03-Desired-Outcomes/P03-Desired-Outcomes.md) | Define what better looks like in measurable or clearly observable terms. | skeleton | B |
| `SB-P04` | [Diagnosis](04-process/systems-building-improvement/P04-Diagnosis/P04-Diagnosis.md) | Identify the highest-leverage constraints and failure modes. | skeleton | B |
| `SB-P05` | [System Design](04-process/systems-building-improvement/P05-Design/P05-System-Design.md) | Design practical interventions that address the diagnosed constraints. | skeleton | B |
| `SB-P06` | [Implementation](04-process/systems-building-improvement/P06-Implementation/P06-Implementation.md) | Apply the designed interventions incrementally and visibly. | skeleton | B |
| `SB-P07` | [Evaluation](04-process/systems-building-improvement/P07-Evaluation/P07-Evaluation.md) | Assess whether the interventions improved the system relative to desired outcomes. | skeleton | B |
| `SB-P08` | [Systems-Building & Improvement Master Orchestrator](04-process/systems-building-improvement/P08-Orchestrator/P08-Systems-Building-Orchestrator.md) | Runs the systems building improvement system end to end: gates, routing, and final acceptance. | skeleton | A |

### testing-qa · 7 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `QA-P01` | [Testing Context & Quality Goals](04-process/testing-qa/P01-Context/P01-Context-Goals.md) | Produce a quality contract: the R1–R4 risk map of the system's behaviours, the triggering problem, the constraints (time, CI budget, team skill), and the success… <br>**Inputs:** `REPO_PATH, TRIGGER, TIME_BUDGET` | operational | B |
| `QA-P02` | [Current Test State Assessment](04-process/testing-qa/P02-Current-State/P02-Current-State-Assessment.md) | Answers: what tests exist, do they pass, are they trustworthy, how fast are they, and which R1 behaviours are unprotected? <br>**Inputs:** `REPO_PATH, BASE_REF` | operational | B |
| `QA-P03` | [Gap Analysis](04-process/testing-qa/P03-Gap-Analysis/P03-Gap-Analysis.md) | Answers: where is the difference between the risk we carry and the protection we have — ranked by consequence? | operational | B |
| `QA-P04` | [Test Strategy & Prioritisation](04-process/testing-qa/P04-Strategy/P04-Strategy-Prioritization.md) | Answers: what is the most valuable test work this team can do next, at which level, in what order, and what are we consciously not doing? <br>**Inputs:** `REPO_PATH, TIME_BUDGET` | operational | B |
| `QA-P05` | [Test Implementation](04-process/testing-qa/P05-Implementation/P05-Implementation.md) | Implement the highest-priority work items from .qa/TEST_STRATEGY.md in the stated order, recording what was actually done, what was skipped, and why. <br>**Inputs:** `REPO_PATH, BRANCH` | operational | B |
| `QA-P06` | [Validation & Measurement](04-process/testing-qa/P06-Validation/P06-Validation-Measurement.md) | Verify that the new tests protect what they claim, that the suite is deterministic and enforced, and that the engagement's success measures from P01 were met. <br>**Inputs:** `REPO_PATH, HEAD_REF` | operational | B |
| `QA-P07` | [Testing & QA Orchestrator](04-process/testing-qa/P07-Orchestrator/P07-Testing-QA-Orchestrator.md) | Run P01–P06 in order, with a real stop-and-check between P04 (plan) and P05 (code), and a verification pass that does not trust P05's own log. <br>**Inputs:** `REPO_PATH, TRIGGER, TIME_BUDGET, APPROVER` | operational | B |

## 05-scenarios — single-session, high-urgency situations

One prompt, one session, one pressing situation.

### All prompts in this area · 36 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `AIVERIFY-01` | [Verifying AI Output: what did the agent actually do, as opposed to claim?](05-scenarios/ai-output-verification/AI-OUTPUT-VERIFICATION.md) | An agent says it is done — "tests pass, feature implemented, bug fixed" — and you need to know what is true before anyone trusts it. <br>**Inputs:** `CLAIM_SCOPE, AGENT_TRANSCRIPT, APPROVER, TIME_BUDGET` | operational | A |
| `AUTO-01` | [Automate a Described Task: turn "we do this by hand" into something that runs](05-scenarios/automation/AUTOMATE-TASK.md) | Someone describes a manual procedure — "every Monday we export this, rename it, upload it, then email finance" — and you need a script that does it safely, verifiabl <br>**Inputs:** `TASK_DESCRIPTION, EXECUTION_ENV, APPROVER, TIME_BUDGET` | operational | B |
| `BUILD-01` | [Build Performance: the feedback loop is a product](05-scenarios/build-performance/BUILD-PERFORMANCE.md) | CI takes 40 minutes, developers skip tests locally, or the cache never hits — measure where the time actually goes before optimising anything. <br>**Inputs:** `REPO_PATH, CI_PROVIDER, TIME_BUDGET, APPROVER` | operational | A |
| `DATA-MIG-01` | [Data Migration: move the records, not just the schema](05-scenarios/data-migration/DATA-MIGRATION.md) | Records must move between systems — a new CRM, a rebuilt service, a warehouse, a vendor change — and the plan must survive partial failure without losing or duplicat <br>**Inputs:** `SOURCE_SYSTEM, TARGET_SYSTEM, FREEZE_WINDOW, APPROVER, TIME_BUDGET` | operational | C |
| `DATALOSS-01` | [Data-Loss Recovery](05-scenarios/data-loss/DATA-LOSS-RECOVERY.md) | Contain the damage, then recover data from a backup, log replay, or an upstream source — and say precisely what is still gone. <br>**Inputs:** `TARGET_ENV, DATA_LOSS_WINDOW, APPROVER, BACKUP_INVENTORY` | operational | D |
| `DBG-01` | [Systematic Debugging](05-scenarios/debugging/SYSTEMATIC-DEBUGGING.md) | Establish the minimal conditions that produce the defect, the causal mechanism, and a fix that is verified against both the defect and the surrounding behaviour. <br>**Inputs:** `OBSERVED_BEHAVIOUR, EXPECTED_BEHAVIOUR, REPRODUCTION_INPUT, REPO_PATH` | operational | B |
| `DEPLOY-01` | [Deploy to a Managed Platform](05-scenarios/deployment-target/DEPLOY-TO-PLATFORM.md) | A documented target profile (runtime shape, build, config classes, limits, cost), a deployment that passes a real end-to-end check, and a rollback path that was… <br>**Inputs:** `DEPLOY_PLATFORM, REPO_PATH, TARGET_ENV, TARGET_SERVICE, DOMAIN_NAME, SPEND_LIMIT, APPROVER` | operational | C |
| `DEVENV-01` | [Reproducible Dev Environment — one command, every editor, any machine](05-scenarios/dev-environment/DEV-ENVIRONMENT.md) | A documented, reproducible environment path (container or scripted), pinned runtimes, editor-agnostic configuration, and a verification that was run on at least one… <br>**Inputs:** `REPO_PATH, TARGET_OS, EDITORS, RUNTIME_VERSION, TEAM_SIZE` | operational | B |
| `DR-01` | [Disaster Recovery: prove the restore, not the backup](05-scenarios/disaster-recovery/DISASTER-RECOVERY.md) | A recovery plan per disaster class, a restore drill performed in an isolated environment, measured RTO and RPO against targets, and a gap register. <br>**Inputs:** `SYSTEM_SCOPE, BACKUP_SOURCE, RTO_TARGET, RPO_TARGET, DRILL_ENV, APPROVER` | operational | C |
| `EMAIL-01` | [Email Deliverability: it is not in the spam folder, it never arrived](05-scenarios/email-deliverability/EMAIL-DELIVERABILITY.md) | An authentication record audit (SPF, DKIM, DMARC, alignment), a stream separation review, a bounce and complaint analysis, a suppression-list check, and a warm-up… <br>**Inputs:** `DOMAIN, SENDER_STACK, STREAM, VOLUME, BOUNCE_DATA, TARGET_ENV` | operational | B |
| `FIXFAIL-01` | [Failed Fix Escalation](05-scenarios/failed-fix/FAILED-FIX-ESCALATION.md) | An accurate record of what was tried and what it proved, an explicit statement of the current model of the defect and why it is probably wrong, and a decision —… <br>**Inputs:** `ORIGINAL_SYMPTOM, REPO_PATH, ATTEMPT_LIST` | operational | B |
| `FLAKE-01` | [Flaky Test Triage](05-scenarios/flaky-tests/FLAKY-TEST-TRIAGE.md) | Answers: which non-determinism the test depends on, and how to make it deterministic without weakening its coverage. <br>**Inputs:** `TEST_IDENTIFIER, REPO_PATH, CI_HISTORY` | operational | B |
| `HACK-01` | [Hackathon Sprint — build the demo that gets judged](05-scenarios/hackathon-sprint/HACKATHON-SPRINT.md) | A plan that fixes the demo path and the cut lines, a build that follows it, a rehearsed demo with fallbacks, and a submission that a judge can run without you. <br>**Inputs:** `HACKATHON_DEADLINE, JUDGING_CRITERIA, DEMO_FORMAT, TEAM_SIZE, TARGET_ENV` | operational | B |
| `HOSTMIG-01` | [Move a Running Service to Another Platform](05-scenarios/platform-migration/PLATFORM-MIGRATION.md) | A staged plan where both platforms serve traffic simultaneously, a verified cutover with a rollback that stays available for days, and a decommission step that only… <br>**Inputs:** `SOURCE_PLATFORM, TARGET_PLATFORM, DOMAIN_NAME, TARGET_ENV, APPROVER, CHANGE_WINDOW` | operational | D |
| `I18N-01` | [Localisation Correctness](05-scenarios/localization/LOCALIZATION.md) | A string inventory with context, a ruleset for translatable content, plural/format handling, layout and RTL verification, and per-locale evidence. <br>**Inputs:** `LOCALES, PLATFORM, STRING_FORMAT, TARGET_MARKETS, TARGET_ENV` | operational | B |
| `IAC-01` | [Infrastructure as Code: adopting it, or proving it matches reality](05-scenarios/infrastructure-as-code/INFRA-AS-CODE.md) | An inventory of resources and their provenance (code, console, script, unknown), a drift report with a decision per item, a state-management plan, and an adoption… <br>**Inputs:** `CLOUD_SCOPE, TOOLING, STATE_BACKEND, APPROVER, TARGET_ENV` | operational | C |
| `INC-01` | [Production Incident Response](05-scenarios/incident-response/PRODUCTION-INCIDENT.md) | Support stabilisation, diagnosis, and communication during an active incident, producing a timeline that can be used for a postmortem without reconstruction from… <br>**Inputs:** `INCIDENT_ID, TARGET_SERVICE, APPROVER, INCIDENT_START_TIME` | operational | C |
| `INC-COMMS-01` | [Incident Communications: tell the truth, on time, to the right people](05-scenarios/incident-communications/INCIDENT-COMMUNICATIONS.md) | An incident is live or has just ended and someone must write the customer update, the status-page entry, and the postmortem timeline without guessing or over-promisi <br>**Inputs:** `INCIDENT_SUMMARY, AUDIENCE, APPROVER, TIME_BUDGET` | operational | B |
| `INTEG-01` | [Third-Party Integration That Survives the Vendor](05-scenarios/third-party-integration/THIRD-PARTY-INTEGRATION.md) | An integration contract (what you depend on, what you assume), a failure-mode matrix with handling per mode, idempotency and retry design, contract tests, and a… <br>**Inputs:** `VENDOR, INTEGRATION_TYPE, CRITICALITY, SANDBOX, WEBHOOK_URL, TARGET_ENV` | operational | B |
| `JOBS-01` | [Background Jobs That Stop Doing Damage](05-scenarios/background-jobs/BACKGROUND-JOBS.md) | A per-job safety assessment (idempotent? <br>**Inputs:** `TARGET_SERVICE, JOB_SCOPE, SCHEDULER, QUEUE_BACKEND, INCIDENT_REF, TARGET_ENV` | operational | B |
| `LEGACY-01` | [Working with Legacy Code](05-scenarios/legacy-code/WORKING-WITH-LEGACY.md) | Change code nobody understands and nobody tested, without turning a small fix into a rewrite. | skeleton | B |
| `MONO-01` | [Monorepo Health: builds, boundaries, and ownership](05-scenarios/monorepo/MONOREPO.md) | A package graph with real dependencies (not declared ones), a boundary violation register, an affected-only build/test plan, and an ownership map. <br>**Inputs:** `REPO_PATH, TOOLING, PACKAGE_COUNT, CI_MINUTES, APPROVER` | operational | B |
| `ONBOARD-01` | [Codebase Onboarding](05-scenarios/onboarding/CODEBASE-ONBOARDING.md) | Join an unfamiliar codebase and need to become useful quickly: entry points, build, data flow, where the traps are. | skeleton | B |
| `ONCALL-01` | [On-Call Shift Handover](05-scenarios/on-call-handover/ONCALL-HANDOVER.md) | SHIFT_HANDOVER.md for the window — open and recent incidents, silences and their expiry, changes and deployments in flight, expiring certificates/tokens/quota… <br>**Inputs:** `TARGET_SERVICE, SHIFT_WINDOW, TARGET_ENV, INCIDENT_REF, ONCALL_ROTA` | operational | B |
| `OPS-01` | [Operational Readiness: would the on-call engineer survive this system?](05-scenarios/operational-readiness/OPERATIONAL-READINESS.md) | Before a launch, or after a painful incident — test whether this service can be operated at 03:00 by someone who did not build it. <br>**Inputs:** `SERVICE_SCOPE, SLO_TARGETS, APPROVER, TIME_BUDGET` | operational | A |
| `PERF-01` | [Performance Investigation](05-scenarios/performance-investigation/PERFORMANCE-INVESTIGATION.md) | Something is slow: measure before optimising, find the bottleneck, and decide whether to fix, budget, or accept it. | skeleton | B |
| `PERF-BUDGET-01` | [Performance Budgets and Core Web Vitals](05-scenarios/performance-budget/PERFORMANCE-BUDGET.md) | Measured baselines for the chosen metrics, budgets derived from user-perceptible thresholds, CI gates that block regressions, and a remediation list for what… <br>**Inputs:** `TARGET_URL, SURFACES, DEVICE_CLASS, NETWORK_PROFILE, BUDGETS, TARGET_ENV` | operational | B |
| `PR-01` | [Write a Strong Pull Request](05-scenarios/pr-authoring/WRITE-STRONG-PR.md) | Turn a finished change into a pull request a reviewer can approve quickly: scope, evidence, risk, and rollback. | skeleton | B |
| `QUICK-01` | [Safe Quick-Fix](05-scenarios/quick-fixes/SAFE-QUICK-FIX.md) | Fix a small, well-understood defect with the smallest correct diff — and know when the "quick" fix is not safe. | skeleton | B |
| `RESIDENCY-01` | [Data Residency: where the data actually is, and how you would prove it](05-scenarios/data-residency/DATA-RESIDENCY.md) | A contract, regulator, or customer says data must stay in a region — and you need to find every place it currently goes. <br>**Inputs:** `REPO_PATH, JURISDICTIONS, CONTRACT_CLAUSE, APPROVER` | operational | A |
| `SECINC-01` | [Security Incident Response](05-scenarios/security-incident/SECURITY-INCIDENT.md) | Detect and confirm → preserve evidence → contain → scope → eradicate → recover → disclose → learn. <br>**Inputs:** `INCIDENT_ID, DISCLOSURE_OWNER, DETECTION_SIGNAL` | operational | D |
| `SECRET-CLIENT-01` | [Client-Side Secrets: the key that shipped to every user](05-scenarios/client-secrets/CLIENT-SIDE-SECRETS.md) | Your bundle, mobile binary, or desktop app ships an API key — and you need to know which ones, what they can do in a stranger's hands, and how to stop it happening a <br>**Inputs:** `REPO_PATH, DISTRIBUTION_CHANNEL, APPROVER` | operational | A |
| `SUNSET-01` | [Feature Sunset: removing something customers depend on](05-scenarios/feature-sunset/FEATURE-SUNSET.md) | A feature is being retired and you need usage evidence, a notice that is not a surprise, a reversible switch-off, and a decision about the data. <br>**Inputs:** `FEATURE_SCOPE, NOTICE_PERIOD, APPROVER, TIME_BUDGET` | operational | B |
| `SUPPLY-01` | [Supply Chain: can you prove the thing you deployed is the thing you built?](05-scenarios/supply-chain/SUPPLY-CHAIN.md) | Assess whether a compromised package, a tampered build, or a substituted artifact could reach production — and what evidence you could produce if someone asked. <br>**Inputs:** `REPO_PATH, ARTIFACT_REGISTRY, APPROVER` | operational | A |
| `SURFACE-01` | [Live Surface Audit — a URL, host, or API from the outside](05-scenarios/live-surface-audit/LIVE-SURFACE-AUDIT.md) | An evidence-backed assessment of the target's externally visible surface — transport, headers, cookies, redirects, error behaviour, discoverability, performance… <br>**Inputs:** `TARGET_URL, AUDIT_AUTHORISATION, PAGE_LIMIT, REPORT_AUDIENCE` | operational | B |
| `UPLOAD-01` | [File Uploads and Object Storage](05-scenarios/file-uploads/FILE-UPLOADS.md) | A validated upload path with signed direct-to-storage transfers where appropriate, content verification, size and type limits, lifecycle rules for orphans and… <br>**Inputs:** `STORAGE_BACKEND, USE_CASES, MAX_SIZE, FILE_TYPES, TARGET_ENV, RETENTION` | operational | B |

## 06-interactive — conversations that clarify a request

Use when the request is vague and needs to be scoped first.

### All prompts in this area · 4 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `INT-P01` | [Project Intake Context Collector](06-interactive/context-collectors/PROJECT-INTAKE.md) | Start a project engagement: collect goals, constraints, stack, existing assets, and success criteria before choosing a system. | skeleton | A |
| `INT-P02` | [Contribution Intake Context Collector](06-interactive/context-collectors/CONTRIBUTION-INTAKE.md) | Before contributing to someone else's project: collect the repository, the maintainers' expectations, and the candidate tasks. | skeleton | A |
| `INT-P03` | [Greenfield / From-Scratch Intake Context Collector](06-interactive/context-collectors/GREENFIELD-INTAKE.md) | Starting from nothing: collect the product intent, constraints, and non-goals needed to pick a build strategy. | skeleton | A |
| `WIZ-P01` | [System Selector Wizard](06-interactive/multi-step-wizards/SYSTEM-SELECTOR.md) | You do not know which system applies: answer a short question set and get routed to the right prompt sequence. | skeleton | A |

## 07-workflows — multi-system procedures

Composed sequences that route between systems and stop at human gates.

### All prompts in this area · 12 prompts

| ID | Prompt | Use it for | Maturity | Risk |
|---|---|---|---|---|
| `WF-AGENTADOPT` | [Workflow — Adopting Coding Agents Without Losing Control](07-workflows/agent-adoption.md) | A written adoption plan with a bounded pilot, an evidence standard for "good enough", a permission profile reviewed as a security decision, an oversight model, and… <br>**Inputs:** `REPO_PATH, TEAM_SCOPE, AGENT_TOOLS, RISK_APPETITE, APPROVER` | operational | B |
| `WF-AUDIT-REMEDIATE` | [Workflow — Audit → Remediate](07-workflows/audit-to-remediation.md) | You need a defensible assessment of an existing codebase and then want the important parts fixed — without the audit becoming a permanent report nobody acts on, and… | draft | B |
| `WF-COMPLY` | [Workflow — Compliance Readiness](07-workflows/compliance-readiness.md) | A security questionnaire, an audit window, or a customer contract names a standard you must evidence — sequence the whole response instead of improvising it. <br>**Inputs:** `STANDARD, SYSTEM_SCOPE, APPROVER, TIME_BUDGET` | operational | A |
| `WF-GREENFIELD` | [Workflow — Greenfield Delivery](07-workflows/greenfield-delivery.md) | Produces a running, tested, documented, deployable initial version | draft | B |
| `WF-HANDOFF` | [Handoff Contract](07-workflows/HANDOFF-CONTRACT.md) | Define one compact block that carries: what was done, what is true now, what is uncertain, what is next, and what authority exists. | operational | A |
| `WF-IMPROVE` | [Workflow — Continuous Improvement](07-workflows/continuous-improvement.md) | Turn recurring pain into a measured improvement loop when nothing is currently on fire but the team keeps hitting the same problems. | draft | B |
| `WF-INCIDENT` | [Workflow — Production Incident](07-workflows/production-incident.md) | Production is broken now: restore service, keep evidence, communicate, then run the postmortem — in that order. | draft | C |
| `WF-INTEGRATE` | [Workflow — Cross-Layer Integration](07-workflows/cross-layer-integration.md) | Prove that the layers interoperate: contracts match, configuration is coherent, identity propagates, failures degrade as designed, and deployment order does not… <br>**Inputs:** `INTEGRATION_ENV, LAYER_BRANCHES` | operational | B |
| `WF-MULTIAGENT` | [Workflow — Multi-Agent Orchestration](07-workflows/multi-agent-orchestration.md) | Produce a decomposition with non-overlapping boundaries, per-agent contracts, a shared state protocol, and an integration-and-verification path. <br>**Inputs:** `SHARED_STATE_REF, TASK_PLAN_FILE, APPROVER` | operational | B |
| `WF-PROMPTAUTH` | [Workflow — Describe it, generate it, prove it, integrate it](07-workflows/prompt-authoring-pipeline.md) | You need a prompt that does not exist yet, or need to know whether a rewrite is better: describe, route against existing coverage, generate, evaluate, decide, integr <br>**Inputs:** `PROMPT_INTENT, TARGET_AGENT, LIBRARY_PATH, EVAL_FIXTURES` | operational | A |
| `WF-RECOVER` | [Workflow — Recover an Abandoned or Broken Project](07-workflows/recover-abandoned-project.md) | A repository exists, is supposed to work, and does not. | draft | B |
| `WF-VERIFY` | [Workflow — Independent Verification of Completed Work](07-workflows/independent-verification.md) | An agent or engineer reports work complete: reproduce the claims yourself, probe the tests, and audit the diff for undeclared scope. <br>**Inputs:** `BASE_REF, HEAD_REF, ACCEPTANCE_CLAIM_FILE` | operational | A |

## 00-core — reference documents

Foundational rules that the systems above assume. These are written as short reference
documents rather than staged prompts, so they carry no identifier or maturity label.

| Document | Use it for | Risk |
|---|---|---|
| [Multi-Stage Handover Protocol](00-core/agent-orchestration/MULTI-STAGE-HANDOVER.md) | A workflow spans more than one session and the next agent must continue without re-deriving context. | A |
| [Recovery & Failure Handling](00-core/agent-orchestration/RECOVERY-AND-FAILURE.md) | A stage fails, stalls, or produces something unverifiable, and the workflow must decide whether to retry, escalate, or stop. | A |
| [Run Sheet — fill this in once per engagement](00-core/inputs/RUN-SHEET.md) | REPO_PATH: BASE_REF: BRANCH: TARGET_AREA: OUT_OF_SCOPE | A |
| [Prompt Quality Bar](00-core/prompt-engineering/QUALITY-BAR.md) | You are writing or reviewing a prompt and need the minimum bar it must clear before anyone uses it. | A |
| [Stage Prompt Template (superseded)](00-core/prompt-engineering/STAGE-PROMPT-TEMPLATE.md) | You need the legacy stage-prompt skeleton for reference. Superseded by _meta/prompt-template.md. | A |
| [Action Categories & Authorization Boundaries](00-core/safety-and-security/ACTION-CATEGORIES.md) | You must classify an action as read-only, a local mutation, an external side effect, or high-risk before authorising it. | A |
| [Secrets & Sensitive Data Handling](00-core/safety-and-security/SECRETS-AND-SENSITIVE-DATA.md) | A task touches credentials, keys, tokens, or personal data and you need the handling rules. | A |
| [Base Engineering Agent Contract](00-core/system-prompts/BASE-ENGINEERING-AGENT.md) | You are configuring an engineering agent and need the default contract every stage prompt inherits. | A |

---

## Keeping this file current

This gallery is generated, not maintained by hand. Whenever a prompt is added, renamed,
or its objective changes:

```bash
python3 scripts/generate_gallery.py --write   # regenerate
python3 scripts/generate_gallery.py --check   # what CI runs
```

CI fails when `GALLERY.md` no longer matches the library. To control the wording of a row,
add a `**Gallery:** one line describing when to use this` metadata line to the prompt;
the generator prefers it over the extracted objective.

Related indexes: [`README.md`](README.md) routes by situation, [`_meta/CATALOG.md`](_meta/CATALOG.md)
lists metadata for tooling, and [`_meta/coverage-matrix.md`](_meta/coverage-matrix.md) tracks what is
covered — and what is not.
