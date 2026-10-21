# Tasks — start from the problem, not the folder tree

<!-- GENERATED FILE — do not edit by hand. Run: python3 scripts/generate_task_index.py --write -->

**364 prompts**, indexed by the situation you are in. Each task lists the prompts that are
**runnable** — `operational` and `draft`. The `skeleton` outlines are counted per task and linked
to the gallery, because a wall of outlines would bury the rows that work today.

Generated from the prompt files and checked in CI, so it cannot drift. Every prompt in the
library is reachable from at least one task: a prompt added without a home fails the build.

| | |
|---|---|
| Prompts indexed | 364 |
| Rows listed individually | 409 (a prompt can answer more than one task) |
| Of those, `operational` | 242 |

Not sure which task is yours? [`QUICKSTART.md`](QUICKSTART.md) routes five common situations,
[`06-interactive/multi-step-wizards/SYSTEM-SELECTOR.md`](06-interactive/multi-step-wizards/SYSTEM-SELECTOR.md)
asks three questions, and [`GALLERY.md`](GALLERY.md) is the complete flat list.

---

## Something is broken right now

Diagnosis first, mitigation second, cause third. Every prompt here forbids the reverse order.

**Start here.** Start with `DBG-01` if the failure is reproducible in a repository you can run. Start with `CHAT-DEBUG` if all you have is a pasted error. Start with `JOBS-01` if what stopped is scheduled work and nothing threw.

| ID | Prompt | Where | Use it for | Maturity |
|---|---|---|---|---|
| `CHAT-DEBUG` | [Chat Debugging: diagnose from a pasted error, and say what you cannot know](00-core/conversational/CHAT-DEBUG.md) | `conversational` | Something is broken, the only tool you have is a chat window, and you need the next test rather than five guesses. | operational |
| `CHAT-MODE` | [Conversational Mode: running any prompt in a chat window](00-core/conversational/CHAT-MODE.md) | `conversational` | You want to use this library in ChatGPT, Claude, Gemini, or any chat window — with no repository access, no shell, and no ability… | operational |
| `AIVERIFY-01` | [Verifying AI Output: what did the agent actually do, as opposed to claim?](05-scenarios/ai-output-verification/AI-OUTPUT-VERIFICATION.md) | `ai-output-verification` | An agent says it is done — "tests pass, feature implemented, bug fixed" — and you need to know what is true before anyone trusts… | operational |
| `JOBS-01` | [Background Jobs That Stop Doing Damage](05-scenarios/background-jobs/BACKGROUND-JOBS.md) | `background-jobs` | Diagnose why background work duplicates, drops, loops, or fails silently — and make every job safe to re-run. | operational |
| `DATALOSS-01` | [Data-Loss Recovery](05-scenarios/data-loss/DATA-LOSS-RECOVERY.md) | `data-loss` | Contain the damage, then recover data from a backup, log replay, or an upstream source — and say precisely what is still gone. | operational |
| `DBG-01` | [Systematic Debugging](05-scenarios/debugging/SYSTEMATIC-DEBUGGING.md) | `debugging` | Establish the minimal conditions that produce the defect, the causal mechanism, and a fix that is verified against both the… | operational |
| `DR-01` | [Disaster Recovery: prove the restore, not the backup](05-scenarios/disaster-recovery/DISASTER-RECOVERY.md) | `disaster-recovery` | A recovery plan per disaster class, a restore drill performed in an isolated environment, measured RTO and RPO against targets… | operational |
| `FIXFAIL-01` | [Failed Fix Escalation](05-scenarios/failed-fix/FAILED-FIX-ESCALATION.md) | `failed-fix` | An accurate record of what was tried and what it proved, an explicit statement of the current model of the defect and why it is… | operational |
| `FLAKE-01` | [Flaky Test Triage](05-scenarios/flaky-tests/FLAKY-TEST-TRIAGE.md) | `flaky-tests` | Answers: which non-determinism the test depends on, and how to make it deterministic without weakening its coverage. | operational |
| `INC-COMMS-01` | [Incident Communications: tell the truth, on time, to the right people](05-scenarios/incident-communications/INCIDENT-COMMUNICATIONS.md) | `incident-communications` | An incident is live or has just ended and someone must write the customer update, the status-page entry, and the postmortem… | operational |
| `INC-01` | [Production Incident Response](05-scenarios/incident-response/PRODUCTION-INCIDENT.md) | `incident-response` | Support stabilisation, diagnosis, and communication during an active incident, producing a timeline that can be used for a… | operational |
| `SECINC-01` | [Security Incident Response](05-scenarios/security-incident/SECURITY-INCIDENT.md) | `security-incident` | Detect and confirm → preserve evidence → contain → scope → eradicate → recover → disclose → learn. | operational |

*Plus **2** `skeleton` prompts in these homes — a defensible stage sequence without verification or failure handling. Use them to structure a human-led session, not to drive an agent: [00-core](GALLERY.md#00-core--foundations-every-prompt-assumes), [05-scenarios](GALLERY.md#05-scenarios--single-session-high-urgency-situations).*

## I have to work in a codebase I have never seen

Reconnaissance, then orientation, then a first contribution that survives review.

**Start here.** `ONBOARD-01` produces the orientation document; the `01-contribution` systems take it from there.

| ID | Prompt | Where | Use it for | Maturity |
|---|---|---|---|---|
| `P01` | [System Architecture, Requirements & Execution Blueprint](01-contribution/open-source/general-agent/P01-System-Architecture/P01-System-Architecture-Requirements-Execution-Blueprint.md) | `P01-System-Architecture` | Transform a capable coding agent into a systematic, evidence-driven, professional open-source contributor | operational |
| `P02` | [Environment & Identity Bootstrap](01-contribution/open-source/general-agent/P02-Environment-Bootstrap/P02-Environment-Identity-Bootstrap.md) | `P02-Environment-Bootstrap` | Locate and safely parse MY_DETAILS.txt (or the user-specified equivalent). | operational |
| `P03` | [Repository Discovery & Initial Reconnaissance](01-contribution/open-source/general-agent/P03-Repo-Discovery/P03-Repository-Discovery-Initial-Reconnaissance.md) | `P03-Repo-Discovery` | Confirm the exact repository identity and its relationship to any target specified in MY_DETAILS.txt. | operational |
| `P04` | [Deep Architectural Intelligence](01-contribution/open-source/general-agent/P04-Architectural-Intelligence/P04-Deep-Architectural-Intelligence.md) | `P04-Architectural-Intelligence` | Progressively deepen the understanding begun in P03. | operational |
| `P05` | [File, Module, Dependency & Component Understanding](01-contribution/open-source/general-agent/P05-File-Module-Understanding/P05-File-Module-Dependency-Component-Understanding.md) | `P05-File-Module-Understanding` | Select and deeply inspect the components most relevant to potential contribution areas (or explicitly requested areas). | operational |
| `P06` | [Git History, Branches, Releases & Development Conventions](01-contribution/open-source/general-agent/P06-Git-History-Conventions/P06-Git-History-Branches-Releases-Development-Conventions.md) | `P06-Git-History-Conventions` | Determine the branching model actually used. | operational |
| `P07` | [GitHub Issues, Discussions, PRs & Documented Contribution Discovery](01-contribution/open-source/general-agent/P07-GitHub-Opportunities/P07-GitHub-Issues-Discussions-PRs-Contribution-Discovery.md) | `P07-GitHub-Opportunities` | Enumerate relevant open issues, especially those suitable for external contribution. | operational |
| `P08` | [Independent Defect Discovery & Technical Opportunity Analysis](01-contribution/open-source/general-agent/P08-Independent-Discovery/P08-Independent-Defect-Discovery-Technical-Opportunity-Analysis.md) | `P08-Independent-Discovery` | Search for real defects, edge-case failures, missing tests, documentation inconsistencies, and other material issues that… | operational |
| `P09` | [Opportunity Verification, Prioritization & Task Selection](01-contribution/open-source/general-agent/P09-Opportunity-Selection/P09-Opportunity-Verification-Prioritization-Task-Selection.md) | `P09-Opportunity-Selection` | Re-verify the current status of every promising candidate (has it been fixed, claimed, duplicated, or rejected since discovery?). | operational |
| `P10` | [Implementation Planning & Change Isolation](01-contribution/open-source/general-agent/P10-Implementation-Planning/P10-Implementation-Planning-Change-Isolation.md) | `P10-Implementation-Planning` | Refine the high-level approach from CONTRIBUTION_PLAN.md into a precise sequence of code/test/doc changes. | operational |
| `P11` | [Engineering Execution & Code Modification](01-contribution/open-source/general-agent/P11-Engineering-Execution/P11-Engineering-Execution-Code-Modification.md) | `P11-Engineering-Execution` | Execute the implementation checklist from P10. | operational |
| `P12` | [Testing, Security, Regression Analysis & Quality Assurance](01-contribution/open-source/general-agent/P12-QA-Validation/P12-Testing-Security-Regression-Quality-Assurance.md) | `P12-QA-Validation` | Execute the project’s relevant test, lint, type-check, build, and security checks. | operational |
| `P13` | [Git Operations, Atomic Commits & Authorized Remote Publication](01-contribution/open-source/general-agent/P13-Git-Publication/P13-Git-Operations-Commits-Authorized-Remote-Publication.md) | `P13-Git-Publication` | Stage only the intended changes. | operational |
| `P14` | [Issues, Pull Requests, Review Responses & Maintainer Communication](01-contribution/open-source/general-agent/P14-PR-Communication/P14-Issues-Pull-Requests-Review-Responses-Maintainer-Communication.md) | `P14-PR-Communication` | Open a new pull request (or update an existing one) that follows the project’s PR template and conventions. | operational |
| `P15` | [Continuous Contribution Management, Monitoring & Recovery](01-contribution/open-source/general-agent/P15-Continuous-Management/P15-Continuous-Contribution-Management-Recovery.md) | `P15-Continuous-Management` | Maintain an accurate, up-to-date picture of all in-progress and completed contribution work. | operational |
| `P16` | [Final Autonomous Contribution Orchestrator](01-contribution/open-source/general-agent/P16-Master-Orchestrator/P16-Final-Autonomous-Contribution-Orchestrator.md) | `P16-Master-Orchestrator` | Transform the raw inputs (repository + MY_DETAILS.txt + this orchestrator) into professional open-source contribution outcomes by | operational |
| `PKG-P06` | [Validation & Compatibility: prove you did not break anyone's build](01-contribution/packages-libraries/P06-Validation/P06-Validation-Compatibility.md) | `P06-Validation` | VALIDATION.md with the public API surface diff, the runtime and module-format matrix, consumer smoke tests run against the… | operational |
| `WEB-P06` | [Validation & Quality: prove the change works in a browser you did not write it in](01-contribution/web/general/P06-Validation/P06-Validation-Quality.md) | `P06-Validation` | VALIDATION.md stating what ran, at which engine and viewport, what it showed, which accessibility criteria were checked and how… | operational |
| `W3-P06` | [Validation & Security: prove the invariants, not the test suite](01-contribution/web3/general/P06-Validation/P06-Validation-Security.md) | `P06-Validation` | VALIDATION.md containing the invariant list with the test that proves each, the access-control matrix, the value-flow review, the… | operational |
| `AUDIT-P01` | [Scope, Environment & Audit Contract](02-engineering/codebase-audit/P01-Bootstrap/P01-Audit-Environment-Bootstrap.md) | `P01-Bootstrap` | Produce a defensible audit contract: what commit is being audited, what questions the audit must answer, what is in and out of… | operational |
| `AUDIT-P02` | [Structural Mapping](02-engineering/codebase-audit/P02-Structure/P02-Structural-Mapping.md) | `P02-Structure` | Answers: what are the components of this repository, how are they built and run, which files matter, and which directories are… | operational |
| `AUDIT-P03` | [Architecture Recovery](02-engineering/codebase-audit/P03-Architecture/P03-Architectural-Analysis.md) | `P03-Architecture` | Answers: what are the real subsystems and boundaries, how does data and control flow between them, where are the load-bearing… | operational |
| `AUDIT-P04` | [Code Quality & Maintainability](02-engineering/codebase-audit/P04-Quality/P04-Code-Quality-Maintainability.md) | `P04-Quality` | Answers: where will the next change be expensive, and why? | operational |
| `AUDIT-P05` | [Tests, Dependencies & Build Health](02-engineering/codebase-audit/P05-Tests-Deps/P05-Tests-Dependencies-Health.md) | `P05-Tests-Deps` | Answers: if we change this system tomorrow, what would catch a mistake — and what would silently ship? | operational |
| `AUDIT-P06` | [Security Surface & Documentation](02-engineering/codebase-audit/P06-Security-Docs/P06-Security-Surface-Documentation.md) | `P06-Security-Docs` | Answers: what does this system expose, who can reach it, where are the trust boundaries, and which review-visible weaknesses… | operational |
| `AUDIT-P07` | [Findings Synthesis & Prioritisation](02-engineering/codebase-audit/P07-Findings/P07-Findings-Synthesis-Prioritization.md) | `P07-Findings` | Answers: which findings are real, how severe, how confident, and what should be done first? | operational |
| `AUDIT-P08` | [Improvement Roadmap & Final Report](02-engineering/codebase-audit/P08-Roadmap/P08-Improvement-Roadmap-Report.md) | `P08-Roadmap` | Answers: what should be done, in what order, why that order, and what happens if nothing is done? | operational |
| `AUDIT-P09` | [Deep Codebase Audit Master Orchestrator](02-engineering/codebase-audit/P09-Orchestrator/P09-Deep-Codebase-Audit-Orchestrator.md) | `P09-Orchestrator` | Deliver a complete, internally consistent audit: scope contract → structure → architecture → quality → tests/dependencies →… | operational |

*Plus **31** `skeleton` prompts in these homes — a defensible stage sequence without verification or failure handling. Use them to structure a human-led session, not to drive an agent: [01-contribution](GALLERY.md#01-contribution--contributing-to-open-source), [02-engineering](GALLERY.md#02-engineering--building-auditing-and-recovering-code), [05-scenarios](GALLERY.md#05-scenarios--single-session-high-urgency-situations).*

## I need to change existing code without breaking it

Safety net, smallest change, evidence that nothing else moved.

**Start here.** `05-scenarios/quick-fixes/` when the change is small; `02-engineering/refactoring/` when it is not.

| ID | Prompt | Where | Use it for | Maturity |
|---|---|---|---|---|
| `FC-P01` | [Completion Contract](02-engineering/feature-completion/P01-Contract/P01-Completion-Contract.md) | `P01-Contract` | Produce a contract of observable behaviours across layers, roles, and states, plus the explicit non-goals. | operational |
| `FC-P02` | [Layer Inventory & Gap Map](02-engineering/feature-completion/P02-Layer-Map/P02-Layer-Gap-Map.md) | `P02-Layer-Map` | Answers: for this feature, which of the fourteen layers already exist, which are missing, and exactly where does each live or… | operational |
| `FC-P03` | [Layer Implementation](02-engineering/feature-completion/P03-Implementation/P03-Layer-Implementation.md) | `P03-Implementation` | Implement the blocking and required gaps in an order that keeps the system runnable at each step, with tests for each layer's… | operational |
| `FC-P04` | [End-to-End Acceptance](02-engineering/feature-completion/P04-Acceptance/P04-End-to-End-Acceptance.md) | `P04-Acceptance` | Prove each acceptance statement from .feature/COMPLETION_CONTRACT.md, including the negative and edge cases, and identify what… | operational |
| `REC-P01` | [Containment & State Preservation](02-engineering/project-recovery/P01-Containment/P01-Containment-State-Preservation.md) | `P01-Containment` | Produce a recoverable starting point and an exact record of it: Git state, uncommitted work, untracked files, running… | operational |
| `REC-P02` | [Intent Reconstruction & Stopping Point](02-engineering/project-recovery/P02-Reconstruction/P02-Intent-Reconstruction.md) | `P02-Reconstruction` | Answers: what was being built, for whom, to what standard — and what was the author doing when they stopped? | operational |
| `REC-P03` | [Completeness Audit](02-engineering/project-recovery/P03-Completeness/P03-Completeness-Audit.md) | `P03-Completeness` | Answers: for each requirement, how much of it is real, and what specifically is missing? | operational |
| `REC-P04` | [Environment & Integration Truth](02-engineering/project-recovery/P04-Integration/P04-Integration-Environment-Truth.md) | `P04-Integration` | Answers: can this project be built and started here, what breaks first, and are the components actually connected? | operational |
| `REC-P05` | [Recovery Plan](02-engineering/project-recovery/P05-Plan/P05-Recovery-Plan.md) | `P05-Plan` | Answers: what is the shortest sequence of changes that produces a working, verifiable critical flow, and what is the acceptance… | operational |
| `REC-P06` | [Incremental Recovery Execution](02-engineering/project-recovery/P06-Execution/P06-Incremental-Recovery.md) | `P06-Execution` | Implement the critical path to the acceptance flow defined in RECOVERY_PLAN.md, one increment at a time, on a dedicated recovery… | operational |
| `REC-P07` | [Acceptance, Honest Reporting & Handoff](02-engineering/project-recovery/P07-Acceptance/P07-Acceptance-Handoff.md) | `P07-Acceptance` | Answers: does the defined acceptance flow work end to end on this branch, and what exactly is the state of the project now? | operational |
| `REF-P01` | [Assessment & Goal Clarification](02-engineering/refactoring/P01-Assessment/P01-Assessment-Goal-Clarification.md) | `P01-Assessment` | Answers: what pain does this area cause today, what measurable outcome would justify the work, which parts must change, and what… | operational |
| `REF-P02` | [Refactoring Strategy](02-engineering/refactoring/P02-Strategy/P02-Refactoring-Strategy.md) | `P02-Strategy` | Produce a strategy: the technique, the slice sequence, the seams, the reversal points, and the estimate — sized against the stop… | operational |
| `REF-P03` | [Safety Net](02-engineering/refactoring/P03-Safety-Net/P03-Safety-Net.md) | `P03-Safety-Net` | Produce a safety net sufficient for the slices in the strategy: characterisation tests of current behaviour (including the odd… | operational |
| `REF-P04` | [Execution](02-engineering/refactoring/P04-Execution/P04-Execution.md) | `P04-Execution` | Execute the strategy's slices in order, keeping the trunk green, logging each step, and stopping when the stop conditions are… | operational |
| `REF-P05` | [Validation](02-engineering/refactoring/P05-Validation/P05-Validation.md) | `P05-Validation` | Behaviour equivalence for the refactored area, no regression elsewhere, and movement on the P01 target — or state precisely which… | operational |
| `REF-P06` | [Cleanup & Documentation](02-engineering/refactoring/P06-Cleanup/P06-Cleanup-Documentation.md) | `P06-Cleanup` | Complete the change: remove the old path once telemetry proves it is unused, delete dead code with evidence, update documentation… | operational |
| `REF-P07` | [Safe Refactoring Master Orchestrator](02-engineering/refactoring/P07-Orchestrator/P07-Safe-Refactoring-Orchestrator.md) | `P07-Orchestrator` | Run the stages in order, enforce the gates, route failures, and produce a final record of what was done, what changed, and what… | operational |

*Plus **16** `skeleton` prompts in these homes — a defensible stage sequence without verification or failure handling. Use them to structure a human-led session, not to drive an agent: [02-engineering](GALLERY.md#02-engineering--building-auditing-and-recovering-code), [05-scenarios](GALLERY.md#05-scenarios--single-session-high-urgency-situations).*

## I am starting something from nothing

Scope, architecture, then a scaffold whose first commit a stranger can run.

**Start here.** `02-engineering/from-scratch/` for a project; `05-scenarios/hackathon-sprint/` when the deadline is days, not months.

| ID | Prompt | Where | Use it for | Maturity |
|---|---|---|---|---|
| `CHAT-DESIGN` | [Chat Design: thinking architecture through in conversation](00-core/conversational/CHAT-DESIGN.md) | `conversational` | Choosing between two approaches, sizing a design before building it, or writing the decision record afterwards. | operational |
| `HACK-01` | [Hackathon Sprint — build the demo that gets judged](05-scenarios/hackathon-sprint/HACKATHON-SPRINT.md) | `hackathon-sprint` | A plan that fixes the demo path and the cut lines, a build that follows it, a rehearsed demo with fallbacks, and a submission… | operational |

*Plus **22** `skeleton` prompts in these homes — a defensible stage sequence without verification or failure handling. Use them to structure a human-led session, not to drive an agent: [00-core](GALLERY.md#00-core--foundations-every-prompt-assumes), [02-engineering](GALLERY.md#02-engineering--building-auditing-and-recovering-code), [05-scenarios](GALLERY.md#05-scenarios--single-session-high-urgency-situations).*

## I need to know whether this codebase is healthy

Audit and measurement, with the difference between 'no evidence of a problem' and 'evidence of no problem' kept explicit.

**Start here.** `02-engineering/codebase-audit/` is the general instrument; the scenarios answer one question each.

| ID | Prompt | Where | Use it for | Maturity |
|---|---|---|---|---|
| `ACCESS-01` | [Access Review: who can still get in, and should they?](02-engineering/access-review/ACCESS-REVIEW.md) | `access-review` | A quarterly access review, a leaver, an incident, or an audit question — establish what access exists today, who still needs it… | operational |
| `AUDIT-P01` | [Scope, Environment & Audit Contract](02-engineering/codebase-audit/P01-Bootstrap/P01-Audit-Environment-Bootstrap.md) | `P01-Bootstrap` | Produce a defensible audit contract: what commit is being audited, what questions the audit must answer, what is in and out of… | operational |
| `AUDIT-P02` | [Structural Mapping](02-engineering/codebase-audit/P02-Structure/P02-Structural-Mapping.md) | `P02-Structure` | Answers: what are the components of this repository, how are they built and run, which files matter, and which directories are… | operational |
| `AUDIT-P03` | [Architecture Recovery](02-engineering/codebase-audit/P03-Architecture/P03-Architectural-Analysis.md) | `P03-Architecture` | Answers: what are the real subsystems and boundaries, how does data and control flow between them, where are the load-bearing… | operational |
| `AUDIT-P04` | [Code Quality & Maintainability](02-engineering/codebase-audit/P04-Quality/P04-Code-Quality-Maintainability.md) | `P04-Quality` | Answers: where will the next change be expensive, and why? | operational |
| `AUDIT-P05` | [Tests, Dependencies & Build Health](02-engineering/codebase-audit/P05-Tests-Deps/P05-Tests-Dependencies-Health.md) | `P05-Tests-Deps` | Answers: if we change this system tomorrow, what would catch a mistake — and what would silently ship? | operational |
| `AUDIT-P06` | [Security Surface & Documentation](02-engineering/codebase-audit/P06-Security-Docs/P06-Security-Surface-Documentation.md) | `P06-Security-Docs` | Answers: what does this system expose, who can reach it, where are the trust boundaries, and which review-visible weaknesses… | operational |
| `AUDIT-P07` | [Findings Synthesis & Prioritisation](02-engineering/codebase-audit/P07-Findings/P07-Findings-Synthesis-Prioritization.md) | `P07-Findings` | Answers: which findings are real, how severe, how confident, and what should be done first? | operational |
| `AUDIT-P08` | [Improvement Roadmap & Final Report](02-engineering/codebase-audit/P08-Roadmap/P08-Improvement-Roadmap-Report.md) | `P08-Roadmap` | Answers: what should be done, in what order, why that order, and what happens if nothing is done? | operational |
| `AUDIT-P09` | [Deep Codebase Audit Master Orchestrator](02-engineering/codebase-audit/P09-Orchestrator/P09-Deep-Codebase-Audit-Orchestrator.md) | `P09-Orchestrator` | Deliver a complete, internally consistent audit: scope contract → structure → architecture → quality → tests/dependencies →… | operational |
| `SEC-ROT-01` | [Secret Rotation: drill it before you need it](02-engineering/secrets-rotation/SECRETS-ROTATION.md) | `secrets-rotation` | An inventory of every secret with its owner, consumers, blast radius, and rotation mechanism; a per-class runbook; a drill… | operational |
| `SEC-P01` | [Authorisation, Scope & Rules of Engagement](02-engineering/security-hardening/P01-Context/P01-Context-Scope.md) | `P01-Context` | Answers: who authorised this work, what is in and out of scope, which techniques are permitted, how findings will be handled, and… | operational |
| `SEC-P02` | [Assets & Threat Model](02-engineering/security-hardening/P02-Threat-Model/P02-Threat-Model.md) | `P02-Threat-Model` | Produce an asset inventory, actor list, trust-boundary map, and a ranked set of abuse cases with the controls that should resist… | operational |
| `SEC-P03` | [Control Review (Attack Surface Analysis)](02-engineering/security-hardening/P03-Surface-Analysis/P03-Surface-Analysis.md) | `P03-Surface-Analysis` | Answers: for each expected control, where is it enforced, which paths bypass it, and under what conditions does it fail? | operational |
| `SEC-P04` | [Findings & Triage](02-engineering/security-hardening/P04-Findings/P04-Findings-Prioritization.md) | `P04-Findings` | Answers: which security weaknesses are real, how bad are they given exposure and reachability, and what is the minimum fix? | operational |
| `SEC-P05` | [Hardening Plan](02-engineering/security-hardening/P05-Hardening-Plan/P05-Hardening-Plan.md) | `P05-Hardening-Plan` | Produce an ordered remediation plan where each item is a bounded change with a verification method and a rollback, plus an… | operational |
| `SEC-P06` | [Hardening Implementation & Verification](02-engineering/security-hardening/P06-Implementation-Validation/P06-Implementation-Validation.md) | `P06-Implementation-Validation` | Implement the approved plan items in order, with tests that demonstrate the gap before the fix and the closure after. | operational |
| `SEC-P07` | [Security Hardening Orchestrator](02-engineering/security-hardening/P07-Orchestrator/P07-Security-Hardening-Orchestrator.md) | `P07-Orchestrator` | Run P01–P04 as read-only assessment, obtain explicit approval for P05, then run P06 for the approved items and verify… | operational |
| `TENANCY-01` | [Tenant Isolation Audit](02-engineering/tenancy-audit/TENANCY-AUDIT.md) | `tenancy-audit` | An inventory of every data store and channel that holds tenant data, the enforcement mechanism for each, the leak paths found… | operational |
| `TIME-01` | [Time and Date Correctness Audit](02-engineering/time-correctness/TIME-CORRECTNESS.md) | `time-correctness` | An inventory of time-bearing data and logic, a defect register with reproductions, boundary tests at DST and month-end, and a… | operational |
| `SURFACE-01` | [Live Surface Audit — a URL, host, or API from the outside](05-scenarios/live-surface-audit/LIVE-SURFACE-AUDIT.md) | `live-surface-audit` | An evidence-backed assessment of the target's externally visible surface — transport, headers, cookies, redirects, error… | operational |
| `MONO-01` | [Monorepo Health: builds, boundaries, and ownership](05-scenarios/monorepo/MONOREPO.md) | `monorepo` | A package graph with real dependencies (not declared ones), a boundary violation register, an affected-only build/test plan, and… | operational |

*Plus **7** `skeleton` prompts in these homes — a defensible stage sequence without verification or failure handling. Use them to structure a human-led session, not to drive an agent: [02-engineering](GALLERY.md#02-engineering--building-auditing-and-recovering-code), [05-scenarios](GALLERY.md#05-scenarios--single-session-high-urgency-situations).*

## I am shipping a release

Deployment, flags, supply chain, and the verification that the release is what you think it is.

**Start here.** `04-process/release-engineering/` runs the sequence; the scenarios cover the decisions around it.

| ID | Prompt | Where | Use it for | Maturity |
|---|---|---|---|---|
| `DEP-P01` | [Dependency Inventory & Risk](04-process/dependency-management/P01-Inventory/P01-Dependency-Inventory-Risk.md) | `P01-Inventory` | Answers: what do we depend on directly and transitively, which of those are risky, and which manifest/lockfile practices make… | operational |
| `DEP-P02` | [Upgrade Planning & Breaking-Change Assessment](04-process/dependency-management/P02-Planning/P02-Upgrade-Planning.md) | `P02-Planning` | Answers: which upgrades should happen, in what order, what breaks, and how will each be proven safe? | operational |
| `DEP-P03` | [Upgrade Execution](04-process/dependency-management/P03-Execution/P03-Upgrade-Execution.md) | `P03-Execution` | Execute the plan's steps in order, one dependency family per commit, with verification after each. | operational |
| `DEP-P04` | [Upgrade Verification](04-process/dependency-management/P04-Verification/P04-Verification.md) | `P04-Verification` | Prove the upgrade is behaviour-preserving where required, that intended changes are actually in effect, and that nothing in the… | operational |
| `DEP-P05` | [Dependency Policy & Ongoing Maintenance](04-process/dependency-management/P05-Policy/P05-Policy-Maintenance.md) | `P05-Policy` | Produce a written, checkable policy: pinning strategy, update cadence, who reviews automated update PRs and how, abandonment… | operational |
| `FF-P01` | [Flag Inventory and Risk](04-process/feature-flags/P01-Inventory/P01-Flag-Inventory-Risk.md) | `P01-Inventory` | A complete inventory of runtime switches with, per flag: identifier, type, owner, age, default state, exposure, where it is read… | operational |
| `FF-P02` | [Flag Design and Safe Defaults](04-process/feature-flags/P02-Design/P02-Flag-Design-Defaults.md) | `P02-Design` | A design record per flag: purpose and type, name, read sites, default and failure behaviour, targeting, owner, expiry or review… | operational |
| `FF-P03` | [Progressive Rollout](04-process/feature-flags/P03-Rollout/P03-Progressive-Rollout.md) | `P03-Rollout` | An executed or planned stage sequence with, per stage: exposure, cohort, duration, guardrail thresholds, the evidence to collect… | operational |
| `FF-P04` | [Kill-Switch Use Under Pressure](04-process/feature-flags/P04-Kill-Switch/P04-Kill-Switch-Use.md) | `P04-Kill-Switch` | A recorded switch decision — observed symptom, hypothesis, expected effect, the flip, the measured result, and the residual state… | operational |
| `FF-P05` | [Flag Retirement](04-process/feature-flags/P05-Retirement/P05-Flag-Retirement.md) | `P05-Retirement` | A removal commit that leaves one code path, no flag evaluation, no dead tests, and a record of the evidence and the residual risk. | operational |
| `GIT-P01` | [State & Safety Check](04-process/git-operations/P01-State/P01-State-Safety-Check.md) | `P01-State` | Answers: what is uncommitted, unpushed, in progress, recoverable, and shared — for ⟨REPO_PATH⟩ on ⟨BRANCH⟩. | operational |
| `GIT-P02` | [Conflict Resolution](04-process/git-operations/P02-Conflicts/P02-Conflict-Resolution.md) | `P02-Conflicts` | Resolve every conflict with a justified decision per hunk, then prove the result preserves both intents by building and testing. | operational |
| `GIT-P03` | [History Repair](04-process/git-operations/P03-History/P03-History-Repair.md) | `P03-History` | Produce the intended history with the least destructive method, on a branch whose safety has been established. | operational |
| `GIT-P04` | [Recovery](04-process/git-operations/P04-Recovery/P04-Recovery.md) | `P04-Recovery` | Restore the lost commit, branch, or file, using git's own records, without disturbing unrelated work. | operational |
| `GIT-P05` | [Hygiene & Collaboration](04-process/git-operations/P05-Hygiene/P05-Hygiene-Collaboration.md) | `P05-Hygiene` | Produce a short, enforceable convention covering branch model, commit granularity, merge strategy, review gates, tags, and the… | operational |
| `REL-P01` | [Release Readiness](04-process/release-engineering/P01-Readiness/P01-Release-Readiness.md) | `P01-Readiness` | Answers: is this exact commit safe to release, what could break for whom, and how would we undo it? | operational |
| `REL-P02` | [Versioning, Changelog & Release Notes](04-process/release-engineering/P02-Versioning/P02-Versioning-Changelog.md) | `P02-Versioning` | Produce a correct semantic version, a changelog entry grouped by impact, and consumer-facing release notes for significant… | operational |
| `REL-P03` | [Deployment Strategy, Migrations & Rollback](04-process/release-engineering/P03-Deployment/P03-Deployment-Rollback.md) | `P03-Deployment` | Produce an executable deployment plan: strategy, order of operations, verification points, abort criteria, and rollback procedure. | operational |
| `REL-P04` | [Post-Release Verification](04-process/release-engineering/P04-Verification/P04-Post-Release-Verification.md) | `P04-Verification` | Answers: is the released version healthy by the metrics we chose before deployment, and did it do what the changelog claims? | operational |
| `DEPLOY-01` | [Deploy to a Managed Platform](05-scenarios/deployment-target/DEPLOY-TO-PLATFORM.md) | `deployment-target` | A documented target profile (runtime shape, build, config classes, limits, cost), a deployment that passes a real end-to-end… | operational |
| `SUNSET-01` | [Feature Sunset: removing something customers depend on](05-scenarios/feature-sunset/FEATURE-SUNSET.md) | `feature-sunset` | A feature is being retired and you need usage evidence, a notice that is not a surprise, a reversible switch-off, and a decision… | operational |
| `IAC-01` | [Infrastructure as Code: adopting it, or proving it matches reality](05-scenarios/infrastructure-as-code/INFRA-AS-CODE.md) | `infrastructure-as-code` | An inventory of resources and their provenance (code, console, script, unknown), a drift report with a decision per item, a… | operational |
| `HOSTMIG-01` | [Move a Running Service to Another Platform](05-scenarios/platform-migration/PLATFORM-MIGRATION.md) | `platform-migration` | A staged plan where both platforms serve traffic simultaneously, a verified cutover with a rollback that stays available for… | operational |
| `INTEG-01` | [Third-Party Integration That Survives the Vendor](05-scenarios/third-party-integration/THIRD-PARTY-INTEGRATION.md) | `third-party-integration` | An integration contract (what you depend on, what you assume), a failure-mode matrix with handling per mode, idempotency and… | operational |

## I need confidence that the tests mean something

Test strategy, the fixtures that make it real, and triage for the tests that fail intermittently.

**Start here.** `04-process/testing-qa/` sets the risk map before any test is written.

| ID | Prompt | Where | Use it for | Maturity |
|---|---|---|---|---|
| `QA-P01` | [Testing Context & Quality Goals](04-process/testing-qa/P01-Context/P01-Context-Goals.md) | `P01-Context` | Produce a quality contract: the R1–R4 risk map of the system's behaviours, the triggering problem, the constraints (time, CI… | operational |
| `QA-P02` | [Current Test State Assessment](04-process/testing-qa/P02-Current-State/P02-Current-State-Assessment.md) | `P02-Current-State` | Answers: what tests exist, do they pass, are they trustworthy, how fast are they, and which R1 behaviours are unprotected? | operational |
| `QA-P03` | [Gap Analysis](04-process/testing-qa/P03-Gap-Analysis/P03-Gap-Analysis.md) | `P03-Gap-Analysis` | Answers: where is the difference between the risk we carry and the protection we have — ranked by consequence? | operational |
| `QA-P04` | [Test Strategy & Prioritisation](04-process/testing-qa/P04-Strategy/P04-Strategy-Prioritization.md) | `P04-Strategy` | Answers: what is the most valuable test work this team can do next, at which level, in what order, and what are we consciously… | operational |
| `QA-P05` | [Test Implementation](04-process/testing-qa/P05-Implementation/P05-Implementation.md) | `P05-Implementation` | Implement the highest-priority work items from .qa/TEST_STRATEGY.md in the stated order, recording what was actually done, what… | operational |
| `QA-P06` | [Validation & Measurement](04-process/testing-qa/P06-Validation/P06-Validation-Measurement.md) | `P06-Validation` | Verify that the new tests protect what they claim, that the suite is deterministic and enforced, and that the engagement's… | operational |
| `QA-P07` | [Testing & QA Orchestrator](04-process/testing-qa/P07-Orchestrator/P07-Testing-QA-Orchestrator.md) | `P07-Orchestrator` | Run P01–P06 in order, with a real stop-and-check between P04 (plan) and P05 (code), and a verification pass that does not trust… | operational |
| `BUILD-01` | [Build Performance: the feedback loop is a product](05-scenarios/build-performance/BUILD-PERFORMANCE.md) | `build-performance` | CI takes 40 minutes, developers skip tests locally, or the cache never hits — measure where the time actually goes before… | operational |
| `FLAKE-01` | [Flaky Test Triage](05-scenarios/flaky-tests/FLAKY-TEST-TRIAGE.md) | `flaky-tests` | Answers: which non-determinism the test depends on, and how to make it deterministic without weakening its coverage. | operational |
| `TESTDATA-01` | [Test Data: the fixture that holds a real customer](05-scenarios/test-data/TEST-DATA.md) | `test-data` | A test database seeded from production, a fixture with a real email address, or a screenshot in a pull request — find it, replace… | operational |

## I have to review a change, or get mine reviewed

A review that states what it did not see, and a pull request a maintainer can act on.

**Start here.** `04-process/code-review/` with repository access; `CHAT-REVIEW` when the diff arrives as a paste.

| ID | Prompt | Where | Use it for | Maturity |
|---|---|---|---|---|
| `CHAT-MODE` | [Conversational Mode: running any prompt in a chat window](00-core/conversational/CHAT-MODE.md) | `conversational` | You want to use this library in ChatGPT, Claude, Gemini, or any chat window — with no repository access, no shell, and no ability… | operational |
| `CHAT-REVIEW` | [Chat Code Review: reviewing a paste, with the limits stated](00-core/conversational/CHAT-REVIEW.md) | `conversational` | You paste a function, a file, or a diff into a chat window and want a review that is useful and does not pretend to have read the… | operational |
| `CR-P01` | [Context & Goals](04-process/code-review/P01-Context/P01-Context-Goals.md) | `P01-Context` | Answers: what is this change trying to achieve, what does it touch, what risk does it carry, and what must this review establish… | operational |
| `CR-P02` | [Change Understanding](04-process/code-review/P02-Change-Understanding/P02-Change-Understanding.md) | `P02-Change-Understanding` | Answers: what does this diff actually do — mechanically, semantically, and behaviourally — including the parts the description… | operational |
| `CR-P03` | [Structured Review](04-process/code-review/P03-Review/P03-Structured-Review.md) | `P03-Review` | A ranked set of findings, each with location, evidence, consequence, and a suggested direction; plus an explicit list of what was… | operational |
| `CR-P04` | [Feedback Crafting](04-process/code-review/P04-Feedback/P04-Feedback-Crafting.md) | `P04-Feedback` | Produce review comments that state the problem, the evidence, and the requested change, ordered so the author knows what matters… | operational |
| `CR-P05` | [Follow-up Support](04-process/code-review/P05-Follow-up/P05-Follow-up-Support.md) | `P05-Follow-up` | A resolution for every finding, a re-verification of the fixes, and a tracked disposition for anything deferred. | operational |
| `CR-P06` | [Code Review Master Orchestrator](04-process/code-review/P06-Orchestrator/P06-Code-Review-Orchestrator.md) | `P06-Orchestrator` | Run the stages, enforce the gates, decide when depth should increase or decrease, and produce a review record with a defensible… | operational |
| `GIT-P01` | [State & Safety Check](04-process/git-operations/P01-State/P01-State-Safety-Check.md) | `P01-State` | Answers: what is uncommitted, unpushed, in progress, recoverable, and shared — for ⟨REPO_PATH⟩ on ⟨BRANCH⟩. | operational |
| `GIT-P02` | [Conflict Resolution](04-process/git-operations/P02-Conflicts/P02-Conflict-Resolution.md) | `P02-Conflicts` | Resolve every conflict with a justified decision per hunk, then prove the result preserves both intents by building and testing. | operational |
| `GIT-P03` | [History Repair](04-process/git-operations/P03-History/P03-History-Repair.md) | `P03-History` | Produce the intended history with the least destructive method, on a branch whose safety has been established. | operational |
| `GIT-P04` | [Recovery](04-process/git-operations/P04-Recovery/P04-Recovery.md) | `P04-Recovery` | Restore the lost commit, branch, or file, using git's own records, without disturbing unrelated work. | operational |
| `GIT-P05` | [Hygiene & Collaboration](04-process/git-operations/P05-Hygiene/P05-Hygiene-Collaboration.md) | `P05-Hygiene` | Produce a short, enforceable convention covering branch model, commit granularity, merge strategy, review gates, tags, and the… | operational |

*Plus **1** `skeleton` prompt in these homes — a defensible stage sequence without verification or failure handling. Use them to structure a human-led session, not to drive an agent: [00-core](GALLERY.md#00-core--foundations-every-prompt-assumes), [04-process](GALLERY.md#04-process--delivering-software-responsibly), [05-scenarios](GALLERY.md#05-scenarios--single-session-high-urgency-situations).*

## I am handing over a system, or taking one over

What the receiver can do unaided, not what the sender explained.

**Start here.** `04-process/handover/` for a person; `05-scenarios/on-call-handover/` for a rota change at speed.

| ID | Prompt | Where | Use it for | Maturity |
|---|---|---|---|---|
| `CHAT-HANDOFF` | [Chat Handoff: carrying a long engagement between conversations](00-core/conversational/CHAT-HANDOFF.md) | `conversational` | One message block, short enough to paste into a new conversation, containing the constraints, the established facts with labels… | operational |
| `DOC-P01` | [Context and Document Products](04-process/documentation/P01-Context/P01-Context-Scope.md) | `P01-Context` | DOC_CONTEXT.md with the product summary, the document products in scope (each with reader, purpose, format, and definition of… | operational |
| `DOC-P02` | [Documentation Inventory and Truth Audit](04-process/documentation/P02-Inventory/P02-Documentation-Inventory.md) | `P02-Inventory` | DOC_INVENTORY.md — every significant document with its location, audience, source of truth, last-verified date, and a truth… | operational |
| `DOC-P03` | [Audience, Jobs, and Structure](04-process/documentation/P03-Audience-Goals/P03-Audience-Goals.md) | `P03-Audience-Goals` | AUDIENCE_GOALS.md — personas with evidence, the top jobs per persona, the task-based structure per document product, entry… | operational |
| `DOC-P04` | [Gap Analysis and Consequence Ranking](04-process/documentation/P04-Gap-Analysis/P04-Gap-Analysis.md) | `P04-Gap-Analysis` | DOC_GAPS.md — each gap with the failed reader task, the evidence, the consequence, a severity class, and the fix's shape… | operational |
| `DOC-P05` | [Documentation Plan](04-process/documentation/P05-Plan/P05-Documentation-Plan.md) | `P05-Plan` | DOC_PLAN.md — ordered deliverables with acceptance tests, per-item owner and review date, the maintenance mechanism per document… | operational |
| `DOC-P06` | [Writing and Improvement](04-process/documentation/P06-Writing/P06-Writing-Improvement.md) | `P06-Writing` | The planned documents on ⟨BRANCH⟩ in ⟨REPO_PATH⟩, each meeting its acceptance test, plus a log of what was written, what was… | operational |
| `DOC-P07` | [Review, Export, and Publication](04-process/documentation/P07-Review/P07-Review-Validation.md) | `P07-Review` | A passed (or honestly failed) review against each acceptance test, verified exports where the product requires them, an approval… | operational |
| `DOC-P08` | [Documentation Orchestrator](04-process/documentation/P08-Orchestrator/P08-Documentation-Orchestrator.md) | `P08-Orchestrator` | A routed run with the stages actually used, the gates recorded, and an honest statement of what was not done. | operational |
| `HAND-P01` | [Scope, Receiver, and Terms](04-process/handover/P01-Scope/P01-Handover-Scope.md) | `P01-Scope` | HANDOVER_SCOPE.md — the handover type, the receiver and their starting competence, the transfer inventory (assets, obligations… | operational |
| `HAND-P02` | [State and Knowledge Capture](04-process/handover/P02-State/P02-State-and-Knowledge-Capture.md) | `P02-State` | HANDOVER_STATE.md — what works and how that was proven, what is broken and what is at risk, open work with its exact position… | operational |
| `HAND-P03` | [Access, Credentials, and Revocation](04-process/handover/P03-Access/P03-Access-and-Credential-Transfer.md) | `P03-Access` | ACCESS_TRANSFER.md — every identity, role, and secret relevant to the system, its before/after holder, the transfer mechanism… | operational |
| `HAND-P04` | [Capability Verification by the Receiver](04-process/handover/P04-Competence/P04-Capability-Verification.md) | `P04-Competence` | CAPABILITY_REPORT.md — the exercise list, who performed what, evidence of success or the exact point of failure, the assistance… | operational |
| `HAND-P05` | [Acceptance and Closeout](04-process/handover/P05-Acceptance/P05-Acceptance-Closeout.md) | `P05-Acceptance` | HANDOVER_ACCEPTANCE.md — the verdict against the P01 acceptance criteria, the condition list with owners and dates, confirmation… | operational |

*Plus **1** `skeleton` prompt in these homes — a defensible stage sequence without verification or failure handling. Use them to structure a human-led session, not to drive an agent: [00-core](GALLERY.md#00-core--foundations-every-prompt-assumes), [04-process](GALLERY.md#04-process--delivering-software-responsibly), [05-scenarios](GALLERY.md#05-scenarios--single-session-high-urgency-situations).*

## Something costs too much or runs too slowly

Measurement before optimisation, in money and in milliseconds.

**Start here.** `05-scenarios/performance-investigation/` when it is slow now; `03-domains/cost-engineering/` when the invoice is the symptom.

| ID | Prompt | Where | Use it for | Maturity |
|---|---|---|---|---|
| `COST-P01` | [Cost Visibility & Attribution](03-domains/cost-engineering/P01-Visibility/P01-Cost-Visibility.md) | `P01-Visibility` | Answers: what did we spend, on what, attributed to whom, and what fraction is unattributable? | operational |
| `COST-P02` | [Waste Diagnosis](03-domains/cost-engineering/P02-Diagnosis/P02-Waste-Diagnosis.md) | `P02-Diagnosis` | Answers: for the top cost centres, what specific mechanism generates the spend, how much would removing it save, and what would… | operational |
| `COST-P03` | [Optimisation](03-domains/cost-engineering/P03-Optimisation/P03-Optimisation.md) | `P03-Optimisation` | Execute the approved, quantified findings from P02 in order of value, each with a verification and a rollback. | operational |
| `COST-P04` | [Guardrails & Unit Economics](03-domains/cost-engineering/P04-Guardrails/P04-Guardrails-Unit-Economics.md) | `P04-Guardrails` | Produce guardrails (tagging, budgets, alerts, policies) and unit economics (cost per request, per tenant, per job) with owners… | operational |
| `BUILD-01` | [Build Performance: the feedback loop is a product](05-scenarios/build-performance/BUILD-PERFORMANCE.md) | `build-performance` | CI takes 40 minutes, developers skip tests locally, or the cache never hits — measure where the time actually goes before… | operational |
| `CAPACITY-01` | [Capacity Planning: what runs out first, and when](05-scenarios/capacity-planning/CAPACITY-PLANNING.md) | `capacity-planning` | Before a launch, a migration, or a seasonal peak — work out which resource runs out first, when, and what you are going to do… | operational |
| `PERF-BUDGET-01` | [Performance Budgets and Core Web Vitals](05-scenarios/performance-budget/PERFORMANCE-BUDGET.md) | `performance-budget` | Measured baselines for the chosen metrics, budgets derived from user-perceptible thresholds, CI gates that block regressions, and… | operational |
| `METER-01` | [Usage Metering and Entitlements: count what you bill, enforce what you sold](05-scenarios/usage-metering/USAGE-METERING.md) | `usage-metering` | You charge by usage, seat, or request — and the number that reaches the invoice has to be reproducible, explainable, and correct… | operational |

*Plus **7** `skeleton` prompts in these homes — a defensible stage sequence without verification or failure handling. Use them to structure a human-led session, not to drive an agent: [02-engineering](GALLERY.md#02-engineering--building-auditing-and-recovering-code), [03-domains](GALLERY.md#03-domains--domain-specific-engineering), [05-scenarios](GALLERY.md#05-scenarios--single-session-high-urgency-situations).*

## I need to move or delete data

Migrations and deletions that can be verified, not merely executed.

**Start here.** `05-scenarios/data-migration/` for movement; `04-process/privacy-requests/` when the request is a legal obligation.

| ID | Prompt | Where | Use it for | Maturity |
|---|---|---|---|---|
| `DB-P01` | [Schema Truth](03-domains/database/P01-Schema/P01-Schema-Truth.md) | `P01-Schema` | Answers: what tables, columns, constraints, indexes, and relationships exist; how do code models, migration history, and… | operational |
| `DB-P02` | [Migration Design](03-domains/database/P02-Design/P02-Migration-Design.md) | `P02-Design` | Produce a phased migration design (expand → migrate → contract) with compatibility analysis, backfill strategy, and explicit… | operational |
| `DB-P03` | [Pre-Flight Validation](03-domains/database/P03-Preflight/P03-Preflight-Validation.md) | `P03-Preflight` | The statements execute cleanly, in the expected duration, with the expected locking, producing the expected data state — and that… | operational |
| `DB-P04` | [Execution & Reconciliation](03-domains/database/P04-Execution/P04-Execution-Reconciliation.md) | `P04-Execution` | Execute the validated plan against the target environment with monitoring, abort discipline, and post-run reconciliation. | operational |
| `DB-P05` | [Rollback & Post-Verification](03-domains/database/P05-Verification/P05-Rollback-Verification.md) | `P05-Verification` | Prove the post-migration state is correct and stable, that the application behaves correctly against it, and that the reverse… | operational |
| `PRIV-P01` | [Subject Data Inventory](04-process/privacy-requests/P01-Inventory/P01-Data-Inventory.md) | `P01-Inventory` | Answers: in which systems does this subject's data exist, in what form, under what retention rule, and what did you *not* search? | operational |
| `PRIV-P02` | [Request Execution](04-process/privacy-requests/P02-Execution/P02-Request-Execution.md) | `P02-Execution` | Export the subject's data, or delete it, with per-system verification and a complete record. | operational |
| `PRIV-P03` | [Retention & Systematisation](04-process/privacy-requests/P03-Retention/P03-Retention-Systematise.md) | `P03-Retention` | A per-data-class retention schedule with enforcement, a self-service or documented request path, and the monitoring that proves… | operational |
| `PRIV-P04` | [Deletion Verification: prove it is gone from the places you forgot](04-process/privacy-requests/P04-Verification/P04-Deletion-Verification.md) | `P04-Verification` | You deleted a subject's data from the database — and now need to know whether it is still in the warehouse, the logs, the… | operational |
| `DATALOSS-01` | [Data-Loss Recovery](05-scenarios/data-loss/DATA-LOSS-RECOVERY.md) | `data-loss` | Contain the damage, then recover data from a backup, log replay, or an upstream source — and say precisely what is still gone. | operational |
| `DATA-MIG-01` | [Data Migration: move the records, not just the schema](05-scenarios/data-migration/DATA-MIGRATION.md) | `data-migration` | Records must move between systems — a new CRM, a rebuilt service, a warehouse, a vendor change — and the plan must survive… | operational |
| `RESIDENCY-01` | [Data Residency: where the data actually is, and how you would prove it](05-scenarios/data-residency/DATA-RESIDENCY.md) | `data-residency` | A contract, regulator, or customer says data must stay in a region — and you need to find every place it currently goes. | operational |

## I am building with AI or agents

Agent contracts, evaluation, permissions, and the context an agent needs to be useful rather than confident.

**Start here.** `00-core/` states the rules the agent systems assume; `03-domains/ai-agentic/` builds the product.

| ID | Prompt | Where | Use it for | Maturity |
|---|---|---|---|---|
| `AI-P01` | [AI Context, Use Case & Risk](03-domains/ai-agentic/P01-Context/P01-Context-Risk.md) | `P01-Context` | Produce a use-case definition, a suitability verdict, a risk classification, and measurable success criteria before any prompt or… | operational |
| `AI-P02` | [AI Application Architecture](03-domains/ai-agentic/P02-Architecture/P02-Architecture.md) | `P02-Architecture` | Design a component architecture that makes model behaviour observable, constrainable, and replaceable. | operational |
| `AI-P03` | [Evaluation-Driven Development](03-domains/ai-agentic/P03-Evaluation/P03-Evaluation.md) | `P03-Evaluation` | Produce a versioned eval dataset, a metric suite with thresholds, and a reproducible harness runnable in CI. | operational |
| `AI-P04` | [Safety, Guardrails & Prompt-Injection Defence](03-domains/ai-agentic/P04-Safety/P04-Safety-Guardrails.md) | `P04-Safety` | Implement input handling, output validation, tool authorisation, and detection for prompt injection and harmful output. | operational |
| `AI-P05` | [AI Production Operations](03-domains/ai-agentic/P05-Production/P05-Production-Operations.md) | `P05-Production` | Implement request-level telemetry, cost and latency accounting, quality monitoring, oversight checkpoints, and a safe release… | operational |
| `AI-P06` | [Grounded Retrieval: does the system answer from your documents?](03-domains/ai-agentic/P06-Retrieval/P06-Grounded-Retrieval.md) | `P06-Retrieval` | A labelled evaluation set with answerable and unanswerable questions, retrieval metrics, groundedness measurement, an ablation… | operational |
| `AI-P07` | [Agent Permissions and Tool Supply Chain](03-domains/ai-agentic/P07-Permissions/P07-Agent-Permissions.md) | `P07-Permissions` | A complete inventory of tools, servers, and capabilities; an effective-permission table; a least-privilege diff with each… | operational |
| `CTX-P01` | [Agent and Editor Surfaces](04-process/agent-context/P01-Surfaces/P01-Agent-Surfaces.md) | `P01-Surfaces` | .agent-context/SURFACES.md — the tools in use, the files each one reads, what those files claim, which claims are true, where… | operational |
| `CTX-P02` | [Authoring the Canonical Context](04-process/agent-context/P02-Authoring/P02-Authoring-Canonical-Context.md) | `P02-Authoring` | A canonical AGENTS.md at the repository root (plus nested AGENTS.md only where a subtree genuinely differs), minimal per-tool… | operational |
| `CTX-P03` | [Adherence Testing](04-process/agent-context/P03-Adherence/P03-Adherence-Testing.md) | `P03-Adherence` | .agent-context/ADHERENCE.md — a set of probes, the observed behaviour per tool, the failures with their causes (missing… | operational |
| `CTX-P04` | [Maintenance and Drift Control](04-process/agent-context/P04-Maintenance/P04-Context-Maintenance.md) | `P04-Maintenance` | Automated checks that fail when the context is stale, an updating convention tied to real triggers, an ownership record, and a… | operational |
| `AIVERIFY-01` | [Verifying AI Output: what did the agent actually do, as opposed to claim?](05-scenarios/ai-output-verification/AI-OUTPUT-VERIFICATION.md) | `ai-output-verification` | An agent says it is done — "tests pass, feature implemented, bug fixed" — and you need to know what is true before anyone trusts… | operational |

## I am building a game

Vertical slice first, then systems, then content — with a playable build at every stage boundary.

**Start here.** `03-domains/games/` runs the ten stages end to end.

| ID | Prompt | Where | Use it for | Maturity |
|---|---|---|---|---|
| `GD-P09` | [Save Data Migration and Compatibility](03-domains/games/P09-Save-Migration/P09-Save-Migration.md) | `P09-Save-Migration` | A versioned save schema, forward migrations for every supported source version, a corruption-resistant read path, and tested… | operational |
| `GD-P10` | [Multiplayer Netcode and Determinism](03-domains/games/P10-Netcode/P10-Netcode.md) | `P10-Netcode` | A diagnosis with measured numbers (latency, jitter, tick alignment, rollback depth), a corrected simulation or replication design… | operational |

*Plus **8** `skeleton` prompts in these homes — a defensible stage sequence without verification or failure handling. Use them to structure a human-led session, not to drive an agent: [03-domains](GALLERY.md#03-domains--domain-specific-engineering).*

## I am building on a blockchain

Contract-level discipline: invariants, access control, upgrade paths, and the audit trail a reviewer expects.

**Start here.** `03-domains/web3/` for a new protocol; `01-contribution/web3/` to contribute to an existing one.

| ID | Prompt | Where | Use it for | Maturity |
|---|---|---|---|---|
| `W3-P06` | [Validation & Security: prove the invariants, not the test suite](01-contribution/web3/general/P06-Validation/P06-Validation-Security.md) | `P06-Validation` | VALIDATION.md containing the invariant list with the test that proves each, the access-control matrix, the value-flow review, the… | operational |
| `PAY-P01` | [Money Model & Invariants](03-domains/payments/P01-Model/P01-Money-Model-Invariants.md) | `P01-Model` | Answers: how is money stored, computed, and rounded; what states can a payment take; and which invariants must hold across every… | operational |
| `PAY-P02` | [Idempotency & Unknown Outcomes](03-domains/payments/P02-Idempotency/P02-Idempotency-Failure.md) | `P02-Idempotency` | Prove or disprove that each money-moving flow is idempotent, that unknown outcomes are handled as a state, and that no failure… | operational |
| `PAY-P03` | [Reconciliation & Change Safety](03-domains/payments/P03-Reconciliation/P03-Reconciliation-Change-Safety.md) | `P03-Reconciliation` | A working reconciliation between your records and the provider's, a drift classification with owners, and a change-safety… | operational |
| `CHAIN-P01` | [Smart Contract Threat Model and Review](03-domains/web3/P01-Review/P01-Contract-Threat-Model.md) | `P01-Review` | An asset and trust inventory, an attack-surface map, ranked findings with concrete exploit paths, and a list of what was not… | operational |
| `CHAIN-P02` | [Key Custody and Deployment Authority](03-domains/web3/P02-Custody/P02-Key-Custody.md) | `P02-Custody` | An authority matrix (role → capability → holder → threshold → delay → revocation path), a key inventory with custody tier per… | operational |
| `CHAIN-P03` | [Contract Upgrade and Storage Migration](03-domains/web3/P03-Upgrade/P03-Upgrade-Migration.md) | `P03-Upgrade` | A storage-layout diff, an upgrade plan with a fork rehearsal, an execution log, and post-upgrade verification evidence. | operational |
| `CHAIN-P04` | [Exploit Response: funds are leaving right now](03-domains/web3/P04-Exploit/P04-Exploit-Response.md) | `P04-Exploit` | Immediate containment, a preserved evidence set, a written incident log with timestamps, a disclosure package for users, and a… | operational |

*Plus **7** `skeleton` prompts in these homes — a defensible stage sequence without verification or failure handling. Use them to structure a human-led session, not to drive an agent: [01-contribution](GALLERY.md#01-contribution--contributing-to-open-source), [03-domains](GALLERY.md#03-domains--domain-specific-engineering).*

## I am building a specific kind of application

Backend, frontend, mobile, desktop, embedded, data, or ML — each with its own failure modes.

**Start here.** Pick the directory for your stack; each is a staged system with the same shape.

| ID | Prompt | Where | Use it for | Maturity |
|---|---|---|---|---|
| `API-VER-01` | [API Versioning and Consumer Contracts](03-domains/backend/P09-API-Versioning/P09-API-Versioning.md) | `P09-API-Versioning` | A versioning scheme, a consumer inventory, compatibility rules per change type, contract tests, a deprecation and sunset policy… | operational |
| `DE-P01` | [Pipeline Reliability: make the data trustworthy before it is fast](03-domains/data-engineering/P01-Pipelines/P01-Pipeline-Reliability.md) | `P01-Pipelines` | A pipeline inventory with ownership and schedule, a failure-mode analysis, data tests for the properties that matter, freshness… | operational |
| `DE-P02` | [Backfill and Reconciliation](03-domains/data-engineering/P02-Backfills/P02-Backfill-Reconciliation.md) | `P02-Backfills` | A scoped backfill plan with a dry run, a reconciliation report proving the new data is correct, a list of affected downstream… | operational |
| `DESK-P01` | [CLI Distribution and Updates](03-domains/desktop-cli/P01-Distribution/P01-CLI-Distribution.md) | `P01-Distribution` | A distribution matrix per platform, signed and checksummed artifacts, an update mechanism with verification, a channel policy… | operational |
| `DESK-P02` | [Terminal UX, Signals, and Exit Codes](03-domains/desktop-cli/P02-Terminal-UX/P02-Terminal-UX.md) | `P02-Terminal-UX` | A specified behaviour matrix (TTY and non-TTY, each signal, each error class), corrected output handling, and tests that exercise… | operational |
| `IOT-P01` | [Firmware OTA with Rollback](03-domains/embedded-iot/P01-OTA/P01-Firmware-OTA.md) | `P01-OTA` | A signed, versioned image; an update procedure with an atomic switch and tested rollback; a staged rollout with automatic… | operational |
| `IOT-P02` | [Fleet Health and Remote Recovery](03-domains/embedded-iot/P02-Fleet/P02-Fleet-Health.md) | `P02-Fleet` | A health model with explicit expectations (what a healthy device reports and how often), a triage method that separates the… | operational |
| `MOB-P01` | [Store Release and Phased Rollout](03-domains/mobile/P01-Release/P01-Store-Release.md) | `P01-Release` | A release plan with a signed build, store metadata, a staged rollout, a halt criterion defined *before* the rollout starts, and a… | operational |
| `MOB-P02` | [Crash Triage and Symbolication](03-domains/mobile/P02-Crashes/P02-Crash-Triage.md) | `P02-Crashes` | A symbolicated, deduplicated crash inventory; a ranking by affected users and business impact (not raw count); a classification… | operational |
| `MOB-P03` | [API Compatibility with Shipped Clients](03-domains/mobile/P03-Compatibility/P03-Client-Compatibility.md) | `P03-Compatibility` | A client-version matrix (which versions exist, in what proportion), the compatibility contract for each supported version, a… | operational |

*Plus **32** `skeleton` prompts in these homes — a defensible stage sequence without verification or failure handling. Use them to structure a human-led session, not to drive an agent: [03-domains](GALLERY.md#03-domains--domain-specific-engineering).*

## I need to answer someone outside engineering

Compliance, vendors, contracts, and the evidence that survives an auditor who asks for a date and a sample.

**Start here.** `04-process/governance-compliance/` maps a requirement to a practice and a piece of dated evidence.

| ID | Prompt | Where | Use it for | Maturity |
|---|---|---|---|---|
| `A11Y-01` | [Accessibility Conformance Audit (WCAG 2.2 AA)](04-process/accessibility-audit/ACCESSIBILITY-AUDIT.md) | `accessibility-audit` | A per-criterion conformance table for the audited pages, a prioritised defect list with reproductions, and a statement of what… | operational |
| `GOV-P01` | [Control Map](04-process/governance-compliance/P01-Control-Map/P01-Control-Map.md) | `P01-Control-Map` | Produce a control map: obligation → mechanism → owner → evidence → status (evidenced / weak / absent / not applicable). | operational |
| `GOV-P02` | [Evidence Collection & Control Testing](04-process/governance-compliance/P02-Evidence/P02-Evidence-Testing.md) | `P02-Evidence` | Prove or disprove that each evidenced/weak control from P01 operated over a defined period. | operational |
| `GOV-P03` | [Gap Remediation & Readiness Decision](04-process/governance-compliance/P03-Readiness/P03-Readiness-Decision.md) | `P03-Readiness` | A remediation plan ordered by consequence, a risk-acceptance register with named owners, and a readiness statement per claim that… | operational |
| `LIC-01` | [Licence Compliance: what you owe the people whose code you ship](04-process/licence-compliance/LICENCE-COMPLIANCE.md) | `licence-compliance` | Work out what your dependencies actually oblige you to do when you ship, and turn that into a gate rather than a surprise in… | operational |
| `STD-01` | [Standards Conformance: prove the project against a named external standard](04-process/standards-conformance/STANDARDS-CONFORMANCE.md) | `standards-conformance` | You have been told to comply with SOC 2, ISO 27001, PCI DSS, WCAG, a customer's security addendum, or an internal standard — and… | operational |
| `ABUSE-01` | [Abuse Prevention: when a legitimate endpoint gets used illegitimately](05-scenarios/abuse-prevention/ABUSE-PREVENTION.md) | `abuse-prevention` | Credential stuffing, scraping, enumeration, signup spam, or a bill that grows with someone else's traffic — separate abuse from… | operational |
| `SECRET-CLIENT-01` | [Client-Side Secrets: the key that shipped to every user](05-scenarios/client-secrets/CLIENT-SIDE-SECRETS.md) | `client-secrets` | Your bundle, mobile binary, or desktop app ships an API key — and you need to know which ones, what they can do in a stranger's… | operational |
| `EMAIL-01` | [Email Deliverability: it is not in the spam folder, it never arrived](05-scenarios/email-deliverability/EMAIL-DELIVERABILITY.md) | `email-deliverability` | An authentication record audit (SPF, DKIM, DMARC, alignment), a stream separation review, a bounce and complaint analysis, a… | operational |
| `UPLOAD-01` | [File Uploads and Object Storage](05-scenarios/file-uploads/FILE-UPLOADS.md) | `file-uploads` | A validated upload path with signed direct-to-storage transfers for files over the size limit of the application server, content… | operational |
| `I18N-01` | [Localisation Correctness](05-scenarios/localization/LOCALIZATION.md) | `localization` | A string inventory with context, a ruleset for translatable content, plural/format handling, layout and RTL verification, and… | operational |
| `SUPPLY-01` | [Supply Chain: can you prove the thing you deployed is the thing you built?](05-scenarios/supply-chain/SUPPLY-CHAIN.md) | `supply-chain` | Assess whether a compromised package, a tampered build, or a substituted artifact could reach production — and what evidence you… | operational |
| `VENDOR-01` | [Vendor Due Diligence: evaluating a supplier before you depend on it](05-scenarios/vendor-due-diligence/VENDOR-DUE-DILIGENCE.md) | `vendor-due-diligence` | Choosing a vendor, or a procurement request arrives — assess what happens if this supplier is breached, fails, raises prices, or… | operational |

## I have to operate this in production

Instrumentation, alerting, runbooks, and the handover that decides whether an on-call engineer can act alone.

**Start here.** `05-scenarios/operational-readiness/` before launch; `04-process/observability-reliability/` once it is live.

| ID | Prompt | Where | Use it for | Maturity |
|---|---|---|---|---|
| `OBS-P01` | [Observability Assessment](04-process/observability-reliability/P01-Instrumentation/P01-Observability-Assessment.md) | `P01-Instrumentation` | Answers: when this system breaks at 03:00, what will the responder know, how fast, and what will they still have to guess? | operational |
| `OBS-P02` | [Instrumentation: Logs, Metrics, Traces](04-process/observability-reliability/P02-Signals/P02-Instrumentation-Signals.md) | `P02-Signals` | Implement correlation IDs, structured logging, golden-signal metrics, and trace propagation on the critical paths identified in… | operational |
| `OBS-P03` | [SLOs and Alerting](04-process/observability-reliability/P03-SLO-Alerting/P03-SLOs-Alerting.md) | `P03-SLO-Alerting` | Produce a small set of user-centred SLIs/SLOs with error budgets, and alert rules that fire on budget burn and hard failure — not… | operational |
| `OBS-P04` | [On-Call Readiness and Runbooks](04-process/observability-reliability/P04-Oncall-Runbooks/P04-Oncall-Runbooks.md) | `P04-Oncall-Runbooks` | Produce a runbook for every paging alert, plus an on-call guide covering escalation, access, and the top failure modes. | operational |
| `OBS-P05` | [Postmortem and Reliability Review](04-process/observability-reliability/P05-Postmortem/P05-Postmortem-Reliability-Review.md) | `P05-Postmortem` | Produce a factual postmortem with owned actions, or a periodic reliability review that identifies systemic weakness across… | operational |
| `CAPACITY-01` | [Capacity Planning: what runs out first, and when](05-scenarios/capacity-planning/CAPACITY-PLANNING.md) | `capacity-planning` | Before a launch, a migration, or a seasonal peak — work out which resource runs out first, when, and what you are going to do… | operational |
| `DEVENV-01` | [Reproducible Dev Environment — one command, every editor, any machine](05-scenarios/dev-environment/DEV-ENVIRONMENT.md) | `dev-environment` | A documented, reproducible environment path (container or scripted), pinned runtimes, editor-agnostic configuration, and a… | operational |
| `ENVPARITY-01` | [Environment Parity: why it works here and not there](05-scenarios/environment-parity/ENVIRONMENT-PARITY.md) | `environment-parity` | "It works locally", staging behaves differently from production, or a bug reproduces on one machine and not another — find the… | operational |
| `IAC-01` | [Infrastructure as Code: adopting it, or proving it matches reality](05-scenarios/infrastructure-as-code/INFRA-AS-CODE.md) | `infrastructure-as-code` | An inventory of resources and their provenance (code, console, script, unknown), a drift report with a decision per item, a… | operational |
| `ONCALL-01` | [On-Call Shift Handover](05-scenarios/on-call-handover/ONCALL-HANDOVER.md) | `on-call-handover` | SHIFT_HANDOVER.md for the window — open and recent incidents, silences and their expiry, changes and deployments in flight… | operational |
| `OPS-01` | [Operational Readiness: would the on-call engineer survive this system?](05-scenarios/operational-readiness/OPERATIONAL-READINESS.md) | `operational-readiness` | Before a launch, or after a painful incident — test whether this service can be operated at 03:00 by someone who did not build it. | operational |

## I am running the work, not just the code

Process design, decommissioning, and the improvement cycle that survives a busy quarter.

**Start here.** `04-process/systems-building-improvement/` for the process; `04-process/project-management/` for the plan.

| ID | Prompt | Where | Use it for | Maturity |
|---|---|---|---|---|
| `DEC-P01` | [Consumer Discovery](04-process/decommissioning/P01-Consumers/P01-Consumer-Discovery.md) | `P01-Consumers` | Answers: who or what calls, reads, writes, or depends on this artefact, including the consumers that leave no trace in… | operational |
| `DEC-P02` | [Deprecation Plan](04-process/decommissioning/P02-Deprecation/P02-Deprecation-Plan.md) | `P02-Deprecation` | A notice and migration plan per consumer, a timeline with dates, the technical deprecation mechanics (warnings, headers, flags)… | operational |
| `DEC-P03` | [Shutdown Execution](04-process/decommissioning/P03-Shutdown/P03-Shutdown-Execution.md) | `P03-Shutdown` | Execute the shutdown: stop new use, drain remaining traffic, confirm quiescence, and leave the system in a restorable state for a… | operational |
| `DEC-P04` | [Data and Asset Retirement](04-process/decommissioning/P04-Retirement/P04-Data-Asset-Retirement.md) | `P04-Retirement` | A complete asset inventory, a retention decision per asset with an owner, deletion executed only for assets whose decisions are… | operational |
| `AUTO-01` | [Automate a Described Task: turn "we do this by hand" into something that runs](05-scenarios/automation/AUTOMATE-TASK.md) | `automation` | Someone describes a manual procedure — "every Monday we export this, rename it, upload it, then email finance" — and you need a… | operational |
| `JOBS-01` | [Background Jobs That Stop Doing Damage](05-scenarios/background-jobs/BACKGROUND-JOBS.md) | `background-jobs` | Diagnose why background work duplicates, drops, loops, or fails silently — and make every job safe to re-run. | operational |

*Plus **24** `skeleton` prompts in these homes — a defensible stage sequence without verification or failure handling. Use them to structure a human-led session, not to drive an agent: [04-process](GALLERY.md#04-process--delivering-software-responsibly), [05-scenarios](GALLERY.md#05-scenarios--single-session-high-urgency-situations).*

## I am writing a prompt, or setting up an agent

The meta level: how a prompt is built, routed, and kept honest about what it cannot do.

**Start here.** `00-core/prompt-engineering/` writes the prompt; `06-interactive/` gathers the context it needs first.

| ID | Prompt | Where | Use it for | Maturity |
|---|---|---|---|---|
| `CHAT-SELECT` | [Chat Select: choosing the right prompt inside a conversation](00-core/conversational/CHAT-SELECT.md) | `conversational` | A routing card with one primary prompt, the reason it fits, the one fact that would overturn the choice, what the user should… | operational |
| `GEN-P01` | [The Prompt Forge: build a runnable prompt from a description](00-core/prompt-engineering/PROMPT-FORGE.md) | `prompt-engineering` | The prompt — paste-ready, complete, with all ten sections filled for its archetype. | operational |
| `GEN-P02` | [Prompt Regression: prove a prompt change is an improvement](00-core/prompt-engineering/PROMPT-REGRESSION.md) | `prompt-engineering` | A fixture set, a run protocol, per-case results, a score against _meta/quality-rubric.md, a comparison to the baseline where one… | operational |

*Plus **4** `skeleton` prompts in these homes — a defensible stage sequence without verification or failure handling. Use them to structure a human-led session, not to drive an agent: [00-core](GALLERY.md#00-core--foundations-every-prompt-assumes), [06-interactive](GALLERY.md#06-interactive--conversations-that-clarify-a-request).*

## The work spans several systems

Composed procedures with named human gates and a handoff contract between stages.

**Start here.** `07-workflows/` sequences the other systems; start from the README's routing table.

| ID | Prompt | Where | Use it for | Maturity |
|---|---|---|---|---|
| `WF-AGENTADOPT` | [Workflow — Adopting Coding Agents Without Losing Control](07-workflows/agent-adoption.md) | `07-workflows` | A written adoption plan with a bounded pilot, an evidence standard for "good enough", a permission profile reviewed as a security… | operational |
| `WF-AUDIT-REMEDIATE` | [Workflow — Audit → Remediate](07-workflows/audit-to-remediation.md) | `07-workflows` | You need a defensible assessment of an existing codebase and then want the important parts fixed — without the audit becoming a… | draft |
| `WF-COMPLY` | [Workflow — Compliance Readiness](07-workflows/compliance-readiness.md) | `07-workflows` | A security questionnaire, an audit window, or a customer contract names a standard you must evidence — sequence the whole… | operational |
| `WF-FAILURE` | [Workflow — Failure Examples](07-workflows/failure-examples.md) | `07-workflows` | When a workflow gate refuses, a stage fails, or an agent reports success that is not true — what the correct handling looks like… | operational |
| `WF-GREENFIELD` | [Workflow — Greenfield Delivery](07-workflows/greenfield-delivery.md) | `07-workflows` | Produces a running, tested, documented, deployable initial version | draft |
| `WF-HANDOFF` | [Handoff Contract](07-workflows/HANDOFF-CONTRACT.md) | `07-workflows` | Define one compact block that carries: what was done, what is true now, what is uncertain, what is next, and what authority… | operational |
| `WF-IMPROVE` | [Workflow — Continuous Improvement](07-workflows/continuous-improvement.md) | `07-workflows` | Turn recurring pain into a measured improvement loop when nothing is currently on fire but the team keeps hitting the same… | draft |
| `WF-INCIDENT` | [Workflow — Production Incident](07-workflows/production-incident.md) | `07-workflows` | Production is broken now: restore service, keep evidence, communicate, then run the postmortem — in that order. | draft |
| `WF-INTEGRATE` | [Workflow — Cross-Layer Integration](07-workflows/cross-layer-integration.md) | `07-workflows` | Prove that the layers interoperate: contracts match, configuration is coherent, identity propagates, failures degrade as… | operational |
| `WF-MULTIAGENT` | [Workflow — Multi-Agent Orchestration](07-workflows/multi-agent-orchestration.md) | `07-workflows` | Produce a decomposition with non-overlapping boundaries, per-agent contracts, a shared state protocol, and an… | operational |
| `WF-PROMPTAUTH` | [Workflow — Describe it, generate it, prove it, integrate it](07-workflows/prompt-authoring-pipeline.md) | `07-workflows` | You need a prompt that does not exist yet, or need to know whether a rewrite is better: describe, route against existing… | operational |
| `WF-RECOVER` | [Workflow — Recover an Abandoned or Broken Project](07-workflows/recover-abandoned-project.md) | `07-workflows` | A repository exists, is supposed to work, and does not. | draft |
| `WF-VERIFY` | [Workflow — Independent Verification of Completed Work](07-workflows/independent-verification.md) | `07-workflows` | An agent or engineer reports work complete: reproduce the claims yourself, probe the tests, and audit the diff for undeclared… | operational |

## I only have a chat window

What survives when there is no repository, no shell, and no way to run a test.

**Start here.** `CHAT-MODE` adapts any other prompt; the three task prompts are already written for chat.

| ID | Prompt | Where | Use it for | Maturity |
|---|---|---|---|---|
| `CHAT-DEBUG` | [Chat Debugging: diagnose from a pasted error, and say what you cannot know](00-core/conversational/CHAT-DEBUG.md) | `conversational` | Something is broken, the only tool you have is a chat window, and you need the next test rather than five guesses. | operational |
| `CHAT-DESIGN` | [Chat Design: thinking architecture through in conversation](00-core/conversational/CHAT-DESIGN.md) | `conversational` | Choosing between two approaches, sizing a design before building it, or writing the decision record afterwards. | operational |
| `CHAT-HANDOFF` | [Chat Handoff: carrying a long engagement between conversations](00-core/conversational/CHAT-HANDOFF.md) | `conversational` | One message block, short enough to paste into a new conversation, containing the constraints, the established facts with labels… | operational |
| `CHAT-MODE` | [Conversational Mode: running any prompt in a chat window](00-core/conversational/CHAT-MODE.md) | `conversational` | You want to use this library in ChatGPT, Claude, Gemini, or any chat window — with no repository access, no shell, and no ability… | operational |
| `CHAT-REVIEW` | [Chat Code Review: reviewing a paste, with the limits stated](00-core/conversational/CHAT-REVIEW.md) | `conversational` | You paste a function, a file, or a diff into a chat window and want a review that is useful and does not pretend to have read the… | operational |
| `CHAT-SELECT` | [Chat Select: choosing the right prompt inside a conversation](00-core/conversational/CHAT-SELECT.md) | `conversational` | A routing card with one primary prompt, the reason it fits, the one fact that would overturn the choice, what the user should… | operational |

---

## How this index stays honest

`scripts/generate_task_index.py` reads the prompt files, assigns each to the tasks whose homes
contain it, and fails when a prompt belongs to none of them. Two rules follow from that:

1. **A new prompt needs a home.** Add its directory to a task in the generator; the build stops
   until you do. The index cannot quietly fall behind the library.
2. **Maturity is not rounded up.** A task that lists four runnable prompts and eleven outlines
   says exactly that, because the counts come from the same metadata the validator checks.

Related: [`GALLERY.md`](GALLERY.md) by area · [`_meta/CATALOG.md`](_meta/CATALOG.md) for tooling ·
[`_meta/coverage-matrix.md`](_meta/coverage-matrix.md) for what is covered and what is not.
