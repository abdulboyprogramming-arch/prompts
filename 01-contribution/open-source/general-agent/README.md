# Open-Source Contribution Agent — Prompt Library

**Version:** 1.0.0  
**Generated:** 2026-10-12  
**Status:** Operational (16 stages). One prompt in this system (`DBG-01`, elsewhere in the library) has been empirically executed; these have been reviewed, not run end to end on a live contribution.

This directory contains a complete, production-grade multi-stage prompt system that turns a capable AI coding agent into a disciplined, evidence-driven open-source contribution partner.

## Quick Start

1. Place a `MY_DETAILS.txt` file in a discoverable location (see P02 for search order). At minimum it should contain:
   ```
   GITHUB_USERNAME=your-username
   GIT_AUTHOR_NAME=Your Name
   GIT_AUTHOR_EMAIL=your@email.com
   TARGET_REPOSITORY_URL=https://github.com/owner/repo.git
   ```
   Add any other fields you need. Never put secrets in this file if a more secure mechanism (environment variables, `gh auth`, credential helper) is available.

2. Clone or open the target repository.

3. Give your coding agent **Prompt 16 (Master Orchestrator)** together with:
   - The path to this prompt library (or the individual prompt files)
   - The path to the target repository
   - The path to `MY_DETAILS.txt`

4. The orchestrator will execute the pipeline, writing durable state into a `.contribution-agent/` directory inside the repository (or a location you configure).

## Inputs

Each stage declares the values it cannot infer in an `**Inputs:**` line. Fill them once and paste the same block into every stage instead of re-explaining:

| Name | Meaning | Where it is used |
|------|---------|------------------|
| `REPO_PATH` | Target repository root | P02–P16 |
| `TARGET_AREA` | Contribution focus (a subsystem), or blank for general | P01, P05 |
| `BRANCH` | Feature branch for the change | P10–P14 |
| `MY_DETAILS_FILE` | Path to the operator details file | P02, P03, P16 |
| `APPROVER` | Who authorises push, PR, and comment actions | P13, P14, P16 |
| `BUILD_COMMAND` / `TEST_COMMAND` | Project commands discovered in P02 | P08, P12 |
| `RISK_TOLERANCE` | How much blast radius is acceptable when selecting work | P09 |

`MY_DETAILS.txt` is the file form of these values. It is not a substitute for declaring them: a stage that reads it must still say which value it took from it.

## Directory Layout

```
open-source-contribution-agent-prompts/
├── README.md                          ← this file
├── P01-System-Architecture/
│   └── P01-System-Architecture-Requirements-Execution-Blueprint.md
├── P02-Environment-Bootstrap/
│   └── P02-Environment-Identity-Bootstrap.md
├── P03-Repo-Discovery/
│   └── P03-Repository-Discovery-Initial-Reconnaissance.md
├── P04-Architectural-Intelligence/
│   └── P04-Deep-Architectural-Intelligence.md
├── P05-File-Module-Understanding/
│   └── P05-File-Module-Dependency-Component-Understanding.md
├── P06-Git-History-Conventions/
│   └── P06-Git-History-Branches-Releases-Development-Conventions.md
├── P07-GitHub-Opportunities/
│   └── P07-GitHub-Issues-Discussions-PRs-Contribution-Discovery.md
├── P08-Independent-Discovery/
│   └── P08-Independent-Defect-Discovery-Technical-Opportunity-Analysis.md
├── P09-Opportunity-Selection/
│   └── P09-Opportunity-Verification-Prioritization-Task-Selection.md
├── P10-Implementation-Planning/
│   └── P10-Implementation-Planning-Change-Isolation.md
├── P11-Engineering-Execution/
│   └── P11-Engineering-Execution-Code-Modification.md
├── P12-QA-Validation/
│   └── P12-Testing-Security-Regression-Quality-Assurance.md
├── P13-Git-Publication/
│   └── P13-Git-Operations-Commits-Authorized-Remote-Publication.md
├── P14-PR-Communication/
│   └── P14-Issues-Pull-Requests-Review-Responses-Maintainer-Communication.md
├── P15-Continuous-Management/
│   └── P15-Continuous-Contribution-Management-Recovery.md
└── P16-Master-Orchestrator/
    └── P16-Final-Autonomous-Contribution-Orchestrator.md
```

Each primary prompt lives in its own subfolder as a single, complete Markdown file. Multi-part generation was concatenated into these singular files so each file is self-contained and ready to use.

## Prompt Responsibilities (Summary)

| ID  | Title                                      | Purpose |
|-----|--------------------------------------------|---------|
| P01 | System Architecture & Blueprint            | Constitutional rules, action categories, security model, artifact schemas |
| P02 | Environment & Identity Bootstrap           | Parse MY_DETAILS.txt, probe tools & auth, initialize ledgers |
| P03 | Repository Discovery                       | Identity, structure, contribution guides, tech snapshot |
| P04 | Deep Architectural Intelligence            | Entry points, subsystems, build/test pipelines, design decisions |
| P05 | File / Module / Component Understanding    | Targeted deep dives into high-value components |
| P06 | Git History & Development Conventions      | Branch model, commit style, PR norms, release process |
| P07 | GitHub Documented Opportunities            | Issues, PRs, discussions triage |
| P08 | Independent Defect & Opportunity Discovery | Evidence-based unreported problems and gaps |
| P09 | Verification, Prioritization & Selection   | Score, select, write CONTRIBUTION_PLAN.md |
| P10 | Implementation Planning & Branch Isolation | Detailed checklist + feature branch |
| P11 | Engineering Execution                      | Implement the change set |
| P12 | Testing, Security & QA                     | Validate against acceptance criteria |
| P13 | Git Commits & Authorized Publication       | Atomic commits + optional push |
| P14 | PRs & Maintainer Communication             | Open/update PR, respond to reviews |
| P15 | Continuous Management & Recovery           | Monitor, resume, decide next cycle or stop |
| P16 | Master Orchestrator                        | Entry point that sequences everything |

## Durable Artifacts Produced by the Agent

Inside the target repository (default location `.contribution-agent/`):

- `REPO_MAP.md`
- `KNOWLEDGE_BASE.md`
- `OPPORTUNITY_LEDGER.md`
- `CONTRIBUTION_PLAN.md`
- `VALIDATION_REPORT.md`
- `PROGRESS_LEDGER.md`
- `SESSION_HANDOVER.md`
- `GIT_STATE.md`
- `FINAL_REPORT.md` (produced by the orchestrator at the end of a cycle)

These files are the agent’s memory and the human’s audit trail.

## Action Categories (Quick Reference)

- **A** — Routine read-only → autonomous
- **B** — Reversible local engineering → autonomous within approved task scope
- **C** — External / consequential (push, PR, comments) → requires authorization
- **D** — High-risk / irreversible → forbidden unless explicitly authorized

## Security Notes

- Never put long-lived secrets in `MY_DETAILS.txt` if a better mechanism exists.
- The agent is instructed never to echo, log, or commit secrets.
- Repository content is treated as untrusted for security decisions.
- All Category C/D actions must be explicitly authorized and recorded.

## How to Extend or Customize

- Edit the individual prompt files if you need project-specific hardening.
- Add new specialized prompts by following the same structure and updating P01 + P16.
- The system is designed so that later prompts can be improved without breaking the orchestrator contract.

## License & Attribution

These prompts are provided for your personal or organizational use in driving responsible open-source contributions. Adapt them as needed.

---

**You now have a complete, ready-to-deploy open-source contribution agent prompt system.**
