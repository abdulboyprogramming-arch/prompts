# Software Engineering Prompt Library

A structured collection of prompts for AI coding agents, organised across the engineering lifecycle: understanding a codebase, deciding what to build, implementing it safely, verifying it, shipping it, and running it in production.

Every prompt declares what it does, what it may change, how much it can be trusted, and what it will not do. Nothing here claims a capability its files do not have — the repository is validated against that rule on every change.

**Browse everything:** [`GALLERY.md`](GALLERY.md) lists all 336 prompts with a direct link and one line on when to use each. It is generated from the prompts themselves and CI fails if it falls out of date, so it cannot drift from the library.

## Start here

Pick the row that matches your situation. Do not read the whole repository first.

| Your situation | Start with | Mode |
|----------------|-----------|------|
| Something is broken in production **right now** | [`05-scenarios/incident-response/`](05-scenarios/incident-response/PRODUCTION-INCIDENT.md) | Restore service first |
| A bug resists normal debugging | [`05-scenarios/debugging/`](05-scenarios/debugging/SYSTEMATIC-DEBUGGING.md) | Diagnostic |
| I inherited / abandoned project that half-works | [`02-engineering/project-recovery/`](02-engineering/project-recovery/README.md) → workflow [`recover-abandoned-project`](07-workflows/recover-abandoned-project.md) | Autonomous, containment first |
| I need to know what is wrong with this codebase | [`02-engineering/codebase-audit/`](02-engineering/codebase-audit/README.md) | Diagnostic (read-only) |
| My tests are slow, flaky, or absent where it matters | [`04-process/testing-qa/`](04-process/testing-qa/README.md) | Audit → write tests |
| I need to contribute to someone else's repository | [`01-contribution/open-source/general-agent/`](01-contribution/open-source/general-agent/README.md) | Autonomous |
| My alerts and runbooks are not useful | [`04-process/observability-reliability/`](04-process/observability-reliability/README.md) | Audit → implement |
| I need to ship a release without breaking production | [`04-process/release-engineering/`](04-process/release-engineering/README.md) | Audit → plan |
| I am building an LLM feature or agent | [`03-domains/ai-agentic/`](03-domains/ai-agentic/README.md) | Architecture → eval → safety |
| My RAG answers are confident and wrong | [`03-domains/ai-agentic/P06`](03-domains/ai-agentic/P06-Retrieval/P06-Grounded-Retrieval.md) | Groundedness, citations, abstention |
| I need to know what my coding agent can actually do | [`03-domains/ai-agentic/P07`](03-domains/ai-agentic/P07-Permissions/P07-Agent-Permissions.md) | MCP servers, shell, egress, credentials |
| I want to generate a new prompt from a description | [`00-core/prompt-engineering/PROMPT-FORGE.md`](00-core/prompt-engineering/PROMPT-FORGE.md) | Compose / improve / decompose |
| I need to know whether a prompt change is better | [`00-core/prompt-engineering/PROMPT-REGRESSION.md`](00-core/prompt-engineering/PROMPT-REGRESSION.md) | Fixtures, runs, score, decision |
| My team is adopting coding agents and I need guardrails | [`07-workflows/agent-adoption.md`](07-workflows/agent-adoption.md) | Evidence, permissions, oversight, rollback |
| I want to build and validate a whole prompt family | workflow [`prompt-authoring-pipeline`](07-workflows/prompt-authoring-pipeline.md) | Describe → generate → prove → integrate |
| I am shipping a smart contract or reviewing one | [`03-domains/web3/`](03-domains/web3/README.md) | Threat model → custody → upgrade |
| Funds are leaving a contract right now | [`03-domains/web3/P04`](03-domains/web3/P04-Exploit/P04-Exploit-Response.md) | Class D: contain first |
| I am releasing a mobile app | [`03-domains/mobile/`](03-domains/mobile/README.md) | Halt criterion before rollout |
| Crash rate spiked after a release | [`03-domains/mobile/P02`](03-domains/mobile/P02-Crashes/P02-Crash-Triage.md) | Symbolicate, segment, rank |
| I am pushing firmware to devices in the field | [`03-domains/embedded-iot/P01`](03-domains/embedded-iot/P01-OTA/P01-Firmware-OTA.md) | Class D: rollback or nothing |
| Devices stopped reporting and I cannot reach them | [`03-domains/embedded-iot/P02`](03-domains/embedded-iot/P02-Fleet/P02-Fleet-Health.md) | Cohorts before dispatch |
| A save file or a game's multiplayer is broken | [`03-domains/games/`](03-domains/games/README.md) | GD-P09 saves, GD-P10 netcode |
| I suspect one customer can see another's data | [`02-engineering/tenancy-audit/`](02-engineering/tenancy-audit/TENANCY-AUDIT.md) | Two synthetic tenants, every store |
| A job fired twice, or never | [`05-scenarios/background-jobs/`](05-scenarios/background-jobs/BACKGROUND-JOBS.md) | Idempotency, overlap, retries |
| Password resets and receipts are not arriving | [`05-scenarios/email-deliverability/`](05-scenarios/email-deliverability/EMAIL-DELIVERABILITY.md) | SPF/DKIM/DMARC alignment, streams |
| I need WCAG 2.2 AA conformance, not a scanner report | [`04-process/accessibility-audit/`](04-process/accessibility-audit/ACCESSIBILITY-AUDIT.md) | Keyboard + screen reader first |
| A dashboard is wrong, empty, or stale | [`03-domains/data-engineering/`](03-domains/data-engineering/README.md) | Tests, contracts, backfills |
| A key may be exposed and rotation is untested | [`02-engineering/secrets-rotation/`](02-engineering/secrets-rotation/SECRETS-ROTATION.md) | Inventory, runbook, drill |
| Something is off by a day, an hour, or a month | [`02-engineering/time-correctness/`](02-engineering/time-correctness/TIME-CORRECTNESS.md) | Instants vs dates, DST, boundaries |
| A vendor API is slow, wrong, or silently changed | [`05-scenarios/third-party-integration/`](05-scenarios/third-party-integration/THIRD-PARTY-INTEGRATION.md) | Eight failure modes, idempotency |
| Uploads are a security and cost surface I have not reviewed | [`05-scenarios/file-uploads/`](05-scenarios/file-uploads/FILE-UPLOADS.md) | Validation, signed URLs, lifecycle |
| We are launching in another language | [`05-scenarios/localization/`](05-scenarios/localization/LOCALIZATION.md) | Plurals, RTL, expansion |
| Infrastructure was built by hand / the code has drifted | [`05-scenarios/infrastructure-as-code/`](05-scenarios/infrastructure-as-code/INFRA-AS-CODE.md) | Provenance, drift decisions |
| "The site feels slow" and nobody owns it | [`05-scenarios/performance-budget/`](05-scenarios/performance-budget/PERFORMANCE-BUDGET.md) | Budgets that fail CI |
| CI rebuilds everything / packages are quietly coupled | [`05-scenarios/monorepo/`](05-scenarios/monorepo/MONOREPO.md) | Graph, boundaries, affected-only |
| I am shipping a CLI | [`03-domains/desktop-cli/`](03-domains/desktop-cli/README.md) | Signing, updates, terminal contract |
| A region or account is gone and I need to know recovery works | [`05-scenarios/disaster-recovery/`](05-scenarios/disaster-recovery/DISASTER-RECOVERY.md) | Prove the restore, measure RTO/RPO |
| My API is changing and partners depend on it | [`03-domains/backend/P09`](03-domains/backend/P09-API-Versioning/P09-API-Versioning.md) | Change classification + sunset |
| I am starting from nothing | [`02-engineering/from-scratch/`](02-engineering/from-scratch/README.md) + workflow [`greenfield-delivery`](07-workflows/greenfield-delivery.md) | Structural only (skeleton) |
| An agent says the work is complete and I need to trust it | [`07-workflows/independent-verification.md`](07-workflows/independent-verification.md) | Diagnostic |
| Data was deleted or corrupted and I need it back | [`05-scenarios/data-loss/`](05-scenarios/data-loss/DATA-LOSS-RECOVERY.md) | Containment first |
| I think we have been compromised | [`05-scenarios/security-incident/`](05-scenarios/security-incident/SECURITY-INCIDENT.md) | Preserve, contain, scope |
| Two fix attempts have failed and the bug is still there | [`05-scenarios/failed-fix/`](05-scenarios/failed-fix/FAILED-FIX-ESCALATION.md) | Diagnostic |
| I need to change a database schema without losing data | [`03-domains/database/`](03-domains/database/README.md) | Audit → drill → execute |
| I need to upgrade a framework or dependency safely | [`04-process/dependency-management/`](04-process/dependency-management/README.md) | Audit → plan → verify |
| I need to deploy to Vercel / Netlify / Render / Fly / Cloud Run / a VPS | [`05-scenarios/deployment-target/`](05-scenarios/deployment-target/DEPLOY-TO-PLATFORM.md) | Platform as a variable |
| I am moving a live service to another host | [`05-scenarios/platform-migration/`](05-scenarios/platform-migration/PLATFORM-MIGRATION.md) | Class D: DNS + data |
| My AI assistant keeps doing the wrong thing in this repo | [`04-process/agent-context/`](04-process/agent-context/README.md) | Test adherence, not existence |
| "Works on my machine" / onboarding takes a day | [`05-scenarios/dev-environment/`](05-scenarios/dev-environment/DEV-ENVIRONMENT.md) | One command, every editor |
| I am taking over an on-call shift | [`05-scenarios/on-call-handover/`](05-scenarios/on-call-handover/ONCALL-HANDOVER.md) | State, silences, tonight's pages |
| A hackathon or demo deadline is close and I need it to work on stage | [`05-scenarios/hackathon-sprint/`](05-scenarios/hackathon-sprint/HACKATHON-SPRINT.md) | Build backwards from the demo |
| I am taking over someone else's project (or handing mine over) | [`04-process/handover/`](04-process/handover/README.md) | Access transfer + capability test |
| A contractor or teammate is leaving and owns production | [`04-process/handover/P03`](04-process/handover/P03-Access/P03-Access-and-Credential-Transfer.md) | Class D: ownership + revocation |
| I need an SRS, a design doc, an engineer handbook, or a PDF/DOCX deliverable | [`04-process/documentation/`](04-process/documentation/README.md) | Source of truth gate |
| The docs are stale or nobody trusts them | [`04-process/documentation/P02`](04-process/documentation/P02-Inventory/P02-Documentation-Inventory.md) | Truth audit first |
| Audit a live URL, site, or API I do not have the source for | [`05-scenarios/live-surface-audit/`](05-scenarios/live-surface-audit/LIVE-SURFACE-AUDIT.md) | Read-only; authorisation first |
| Production behaves differently from staging and I suspect a flag | [`04-process/feature-flags/P01`](04-process/feature-flags/P01-Inventory/P01-Flag-Inventory-Risk.md) | Read-only audit |
| I need to ship behind a switch, or kill one during an incident | [`04-process/feature-flags/`](04-process/feature-flags/README.md) | Class C in production |
| Someone needs to review my change (or I need to review theirs) | [`04-process/code-review/`](04-process/code-review/README.md) | Proportional to risk |
| A merge or rebase stopped with conflicts | [`04-process/git-operations/`](04-process/git-operations/README.md) | Conflicts first, then verify |
| Commits, a branch, or a stash just vanished | [`04-process/git-operations/P04-Recovery`](04-process/git-operations/P04-Recovery/P04-Recovery.md) | Time-critical |
| I need to rewrite history or clean a secret out of it | [`04-process/git-operations/P03-History`](04-process/git-operations/P03-History/P03-History-Repair.md) | Category D if shared |
| I am splitting work across several agents | [`07-workflows/multi-agent-orchestration.md`](07-workflows/multi-agent-orchestration.md) | Orchestration |
| A customer or auditor asks for evidence of our controls | [`04-process/governance-compliance/`](04-process/governance-compliance/README.md) | Audit |
| I need to retire a service or endpoint safely | [`04-process/decommissioning/`](04-process/decommissioning/README.md) | Staged, reversible |
| The frontend and backend were built separately | [`07-workflows/cross-layer-integration.md`](07-workflows/cross-layer-integration.md) | Specialised |
| We charge money and cannot prove the books balance | [`03-domains/payments/`](03-domains/payments/README.md) | Specialised, money is Category C/D |
| The cloud bill doubled and nobody knows why | [`03-domains/cost-engineering/`](03-domains/cost-engineering/README.md) | Audit → change → guardrails |
| Someone asks us to delete or export their data | [`04-process/privacy-requests/`](04-process/privacy-requests/README.md) | Specialised, deletion is Category D |
| I need to restructure code without changing behaviour | [`02-engineering/refactoring/`](02-engineering/refactoring/README.md) | Diagnostic → implementation |
| A feature "works" but only in the UI | [`02-engineering/feature-completion/`](02-engineering/feature-completion/README.md) | Implementation |
| My request is vague and needs intake | [`06-interactive/`](06-interactive/README.md) | Interactive |

Full inventory, with maturity per prompt: [`_meta/CATALOG.md`](_meta/CATALOG.md).

## Maturity legend — read this before using anything

The library is deliberately honest about how developed each system is.

| Label | Meaning | Safe to use |
|-------|---------|-------------|
| **operational** | Full workflow, evidence rules, verification, failure handling, completion criteria; structurally reviewed | Yes, with a capable agent and normal supervision |
| **draft** | Substantive but not yet reviewed against the rubric; gaps are listed in the file | Yes, expect to fill gaps |
| **skeleton** | A stage sequence with a short outline. Names the artifact and a few steps; no verification or failure handling | As a **human checklist**, not for unsupervised autonomy |

Maturity is enforced, not decorative: `scripts/validate_library.py` fails if a prompt's label exceeds its content, or if a system README advertises more maturity than its stages have.

### Licence

Two licences, because the repository holds two kinds of thing:

- **Code** (`scripts/`, code samples) — MIT. See [`LICENSE`](LICENSE).
- **Prompts and prose** — [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): use, adapt, and redistribute commercially, with attribution and an indication of changes. See [`LICENSE-CONTENT`](LICENSE-CONTENT).

In short: take it, change it, ship it — say where it came from, and do not present modified prompts as this project's work.

### Where the depth actually is

| System | Prompts | Maturity |
|--------|--------:|----------|
| [`01-contribution/open-source/general-agent/`](01-contribution/open-source/general-agent/README.md) | 16 | operational |
| [`02-engineering/codebase-audit/`](02-engineering/codebase-audit/README.md) | 9 | operational |
| [`02-engineering/project-recovery/`](02-engineering/project-recovery/README.md) | 7 | operational |
| [`02-engineering/security-hardening/`](02-engineering/security-hardening/README.md) | 7 | operational |
| [`04-process/testing-qa/`](04-process/testing-qa/README.md) | 7 | operational |
| [`04-process/observability-reliability/`](04-process/observability-reliability/README.md) | 5 | operational |
| [`04-process/release-engineering/`](04-process/release-engineering/README.md) | 4 | operational |
| [`03-domains/ai-agentic/`](03-domains/ai-agentic/README.md) | 5 | operational |
| [`03-domains/database/`](03-domains/database/README.md) | 5 | operational |
| [`04-process/dependency-management/`](04-process/dependency-management/README.md) | 5 | operational |
| [`04-process/decommissioning/`](04-process/decommissioning/README.md) | 4 | operational |
| [`04-process/governance-compliance/`](04-process/governance-compliance/README.md) | 3 | operational |
| [`02-engineering/feature-completion/`](02-engineering/feature-completion/README.md) | 4 | operational |
| [`02-engineering/refactoring/`](02-engineering/refactoring/README.md) | 7 | operational |
| [`03-domains/cost-engineering/`](03-domains/cost-engineering/README.md) | 4 | operational |
| [`03-domains/payments/`](03-domains/payments/README.md) | 3 | operational |
| [`03-domains/web3/`](03-domains/web3/README.md) | 4 | operational |
| [`03-domains/mobile/`](03-domains/mobile/README.md) | 3 | operational |
| [`03-domains/embedded-iot/`](03-domains/embedded-iot/README.md) | 2 | operational |
| [`03-domains/data-engineering/`](03-domains/data-engineering/README.md) | 2 | operational |
| [`03-domains/desktop-cli/`](03-domains/desktop-cli/README.md) | 2 | operational |
| [`02-engineering/time-correctness/`](02-engineering/time-correctness/TIME-CORRECTNESS.md) | 1 | operational |
| [`02-engineering/tenancy-audit/`](02-engineering/tenancy-audit/TENANCY-AUDIT.md) | 1 | operational |
| [`02-engineering/secrets-rotation/`](02-engineering/secrets-rotation/SECRETS-ROTATION.md) | 1 | operational |
| [`04-process/accessibility-audit/`](04-process/accessibility-audit/ACCESSIBILITY-AUDIT.md) | 1 | operational |
| [`00-core/prompt-engineering/`](00-core/prompt-engineering/PROMPT-FORGE.md) | 2 | operational (GEN-P01, GEN-P02) |
| [`04-process/privacy-requests/`](04-process/privacy-requests/README.md) | 3 | operational |
| [`04-process/git-operations/`](04-process/git-operations/README.md) | 5 | operational |
| [`04-process/code-review/`](04-process/code-review/README.md) | 6 | operational |
| [`04-process/feature-flags/`](04-process/feature-flags/README.md) | 5 | operational |
| [`04-process/documentation/`](04-process/documentation/README.md) | 8 | operational |
| [`04-process/handover/`](04-process/handover/README.md) | 5 | operational |
| [`04-process/agent-context/`](04-process/agent-context/README.md) | 4 | operational |
| [`07-workflows/`](07-workflows/README.md) | 9 | mixed (3 operational: verification, integration, multi-agent) |
| [`05-scenarios/`](05-scenarios/README.md) | 26 | mixed (21 operational, 5 skeleton) |

Everything else — backend, frontend, devops-infra, data-ml-ai, the eight game-design stages, architecture-review, from-scratch, migration, project management, research, systems improvement, language design, packages, web/web3 contribution — is a **skeleton**: a defensible sequence of stages with outline prompts. Those folders are useful for structuring a human-led session today; they are not yet safe to hand to an autonomous agent. Promotion order is in [`_meta/ROADMAP-AND-BACKLOG.md`](_meta/ROADMAP-AND-BACKLOG.md); per-scenario coverage with evidence is in [`_meta/coverage-matrix.md`](_meta/coverage-matrix.md).

## Structure

```
00-core/          Safety categories, orchestration primitives, base agent contract
01-contribution/  Contributing to existing projects (OSS, packages, web, web3, languages)
02-engineering/   Audits, project recovery, architecture, refactoring, migration, performance, security
03-domains/       Backend, frontend, devops, data/ML, games, AI-agentic, web3, mobile, embedded/IoT
04-process/       Testing, review, documentation, PM, research, observability, release
05-scenarios/     Single-purpose prompts for common situations
06-interactive/   Context collectors and intake wizards
07-workflows/     Composed multi-system sequences with gates and handoff contracts
_meta/            Authoring standard, rubric, taxonomy, catalog, roadmap, review log
scripts/          Validator and catalog generator
archive/          Legacy source material (not maintained)
```

## How prompts are written

Every prompt follows [`_meta/prompt-authoring-standard.md`](_meta/prompt-authoring-standard.md) and carries a metadata block:

```markdown
**Identifier:** AUDIT-P03
**System:** 02-engineering/codebase-audit
**Version:** 1.1.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A
**Depends on:** AUDIT-P02
**Produces:** `.audit/ARCHITECTURE.md`
```

- **Execution mode** sets the stopping rule: a `diagnostic` prompt reports, an `implementation` prompt ships verified changes, an `autonomous-completion` prompt runs the full loop with gates.
- **Risk class** is the highest action category the prompt can reach: `A` read-only, `B` local mutation, `C` external side effect, `D` high-risk. Publishing, deploying, and pushing are always `C` and always require explicit authorisation.
- **Evidence labels** (`verified` / `inferred` / `unknown`) are used rather than confident prose.

Quality is scored with [`_meta/quality-rubric.md`](_meta/quality-rubric.md) — 100 points, anchors per band, nine critical failure conditions that block the `operational` label.

## Composing systems

Individual prompts solve a task. Real work is a sequence with handoffs and decisions. [`07-workflows/`](07-workflows/README.md) defines five such sequences, each with explicit gates where a human must decide, failure routing, and acceptance criteria for the whole chain:

- [Recover an abandoned or broken project](07-workflows/recover-abandoned-project.md)
- [Audit → remediate](07-workflows/audit-to-remediation.md)
- [Production incident](07-workflows/production-incident.md)
- [Greenfield delivery](07-workflows/greenfield-delivery.md)
- [Continuous improvement](07-workflows/continuous-improvement.md)

Stages exchange state using the [handoff contract](07-workflows/HANDOFF-CONTRACT.md), so a second session or a different agent can continue without replaying the conversation.

## The safety floor

All systems inherit [`00-core/safety-and-security/ACTION-CATEGORIES.md`](00-core/safety-and-security/ACTION-CATEGORIES.md):

- **A — read-only**: reading, searching, non-destructive checks.
- **B — local mutation**: edits, commits, test runs, artifacts.
- **C — external side effects**: push, publish, deploy, comment, paid APIs. Requires explicit authorisation.
- **D — high-risk**: production secrets, destructive data operations, irreversible infrastructure. Requires specific approval.

No prompt may silently escalate its own category. [`00-core/safety-and-security/SECRETS-AND-SENSITIVE-DATA.md`](00-core/safety-and-security/SECRETS-AND-SENSITIVE-DATA.md) covers secret handling and responsible disclosure.

## Contributing and validating

```bash
python3 scripts/validate_library.py            # must report 0 errors
python3 scripts/validate_library.py --catalog  # regenerate _meta/CATALOG.md
```

The validator checks metadata completeness, identifier uniqueness, version/maturity consistency, required sections, broken links (Markdown and backticked paths), empty sections, risk-class honesty, and README status overclaims. CI runs it on every pull request and fails if `_meta/CATALOG.md` is stale (`.github/workflows/validate-library.yml`).

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before adding a system, and [`AGENTS.md`](AGENTS.md) if you are an AI agent working in this repository.

## Known limitations

- **165 of 235 prompts are skeleton outlines.** They are labelled as such everywhere.
- **No prompt has been empirically tested against a real repository and recorded.** `operational` means structurally complete and reviewed, not proven in practice.
- **Mobile, database, embedded, desktop/CLI, dependency management, governance, and multi-agent orchestration have no dedicated systems yet.** They are prioritised in the backlog.
- **Reviews are self-assessments** recorded in [`_meta/review-log.md`](_meta/review-log.md); independent verification has not been performed.
- CI validates the library on pull requests; it does not test prompts empirically (no such harness exists).

Coverage per engineering scenario, with an honest status for each: [`_meta/coverage-matrix.md`](_meta/coverage-matrix.md).

Current state, decisions, and next actions: [`PROJECT-STATUS.md`](PROJECT-STATUS.md). Change history: [`CHANGELOG.md`](CHANGELOG.md).
