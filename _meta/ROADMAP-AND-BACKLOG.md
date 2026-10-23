# Roadmap & Backlog

**Version:** 1.1.0
**Last updated:** 2026-10-20

Coverage status per scenario lives in `_meta/coverage-matrix.md`; this file is the work queue derived from it.

Priority is by **practical usefulness × frequency × severity of the gap**, not by ease. Every item states what exists today, so nothing here pretends to be an absence when a partial implementation exists.

## P0 — Truth and maintainability (done in this cycle)

| Item | Status |
|------|--------|
| Honest maturity labelling for all 235 prompt files | Done — validator-enforced |
| Status overclaims in system READMEs removed | Done |
| Authoring standard with execution modes and required sections | Done (`_meta/prompt-authoring-standard.md`) |
| Quality rubric with anchors and critical failure gates | Done (`_meta/quality-rubric.md`) |
| Validator + generated catalog | Done (`scripts/validate_library.py`) |
| Continuation checkpoint | Done (`PROJECT-STATUS.md`) |

## P1 — Promote the weakest widely-used systems

These systems are referenced from the root README and workflows but consist of 20-line stage outlines. Their sequences are sound; their prompts are not yet operable.

| System | Stages | Why it matters | Target |
|--------|-------:|----------------|--------|
| ~~`02-engineering/security-hardening`~~ | 7 | **Done in 2.0.0** — authorisation gate, threat model, enforcement matrix, triage, proven remediation | operational |
| ~~`02-engineering/refactoring`~~ | 7 | **Done in 2.3.0** — measurable target, mutation-proven net, mechanical slices, equivalence + target measurement, old-path removal | done |
| `03-domains/backend` | 8 | Largest domain by usage; promoted to operational in 2.26.0 with a gate sequence, not yet executed | operational |
| `03-domains/frontend` | 8 | Accessibility and state management are named but have no pass criteria | operational |
| `04-process/code-review` | 6 | Reviews are where quality is actually decided | operational |
| `02-engineering/from-scratch` | 8 | First-contact system for new users; currently advisory | operational |
| `01-contribution/packages-libraries` | 8 | Compatibility work with real consumer risk | operational |
| `01-contribution/web/general` | 8 | Named gaps documented in its README | operational |
| `01-contribution/web3/general` | 8 | Funds-at-risk domain with only a heading for security | operational or explicit non-support |

Each promotion requires: full required sections, verification that can fail, failure routing, and a review record.

## P2 — Missing systems with high practical value

| Gap | Why it is missing from the library today | Proposed system |
|-----|------------------------------------------|-----------------|
| **Mobile (native + cross-platform)** | No coverage at all, despite `03-domains` listing it as an "area". Offline sync, store review, permissions, and lifecycle differ enough to need dedicated prompts | `03-domains/mobile` (6 stages) |
| ~~**Database engineering**~~ | **Done in 2.1.0** as `03-domains/database` (5 stages: schema truth, migration design, pre-flight, execution, rollback) | — |
| **API design & evolution** | `BE-P02` now carries idempotency, pagination and the error taxonomy; `API-VER-01` covers versioning. What remains is a worked example against a real public API | fold into backend, or `03-domains/api-design` |
| ~~**Dependency & toolchain management**~~ | **Done in 2.1.0** as `04-process/dependency-management` (5 stages) | — |
| **Accessibility & i18n** | Mentioned in frontend skeleton without criteria; WCAG conformance and localisation are engineering disciplines | `03-domains/frontend` sub-system or `05-scenarios/accessibility-audit` |
| **Data engineering** | `data-ml-ai` conflates pipelines with modelling; ingest/quality/lineage missing | split or extend `03-domains/data-ml-ai` |
| **Embedded / firmware** | No coverage; safety and hardware constraints are materially different | `03-domains/embedded` |
| **Desktop & CLI tools** | No coverage; packaging, updates, and terminal UX are distinct | `03-domains/desktop-cli` |
| **Documentation as engineering** | README reconstruction, ADRs, doc-code drift, SRS/handbook/PDF deliverables were all uncovered | promoted in 2.11.0 (`DOC-P01..P08`) |
| **Architecture decision records & governance** | ADRs are referenced but no prompt produces one | `05-scenarios/adr/` |
| **Multi-agent orchestration** | The library assumes single-agent use; parallel agents need ownership and conflict rules | multi-agent coordination workflow (planned) |
| **Compliance & enterprise readiness** | Only implied; audit/SBOM/change-management evidence is a real need | `04-process/governance-compliance` |

## P3 — Depth and coverage extensions inside existing systems

- `02-engineering/codebase-audit`: add a stage for licence/SBOM and one for data-flow/PII mapping.
- `02-engineering/project-recovery`: add a variant for monorepos with per-package state.
- `04-process/observability-reliability`: real dashboards-as-code examples, per-stack (Prometheus/OTel) — currently vendor-neutral only.
- `03-domains/ai-agentic`: add a stage for retrieval quality tuning and one for agent tool design.
- `05-scenarios`: add `dependency-hell`, `memory-leak`, `build-failure`, `api-breaking-change`, `code-review-of-ai-generated-code`.
- `06-interactive`: add intake prompts for recovery, security review, and release.

## P4 — Tooling

| Item | Rationale |
|------|-----------|
| Near-duplicate detection across prompts | Currently only exact identifier/link checks; overlapping prompts will accumulate as the library grows |
| Maturity-promotion checklist automation | Rubric scoring is manual and recorded in a log; a script could enforce presence of sections per mode |
| Link validation for backticked paths | Implemented as a warning; promote to error once existing references are clean |
| ~~CI workflow running the validator~~ | Done — `.github/workflows/validate.yml` calls `scripts/check_all.py`; the earlier per-command workflow was deleted in 2.22.0 because two workflows meant two gate lists |
| Empirical test log | No prompt has been exercised against a real repository in a recorded way; this is the largest credibility gap |

## Deliberately not planned

- A prompt per framework or library version. The library teaches transferable engineering; framework churn would create maintenance debt with no quality gain.
- Auto-generated prompt variants. Volume without differentiation is the failure mode this library explicitly rejects.
- A hosted service. The repository is usable as files; distribution is out of scope.

## How to pick up this backlog

1. Read `PROJECT-STATUS.md` for the current state and the last change made.
2. Pick the highest-priority P1 system with no review record.
3. Follow `_meta/prompt-authoring-standard.md`; copy structure from an operational system (`02-engineering/codebase-audit`, `02-engineering/project-recovery`, `04-process/testing-qa`).
4. Run `python3 scripts/validate_library.py`.
5. Add a review record to `_meta/review-log.md`, update the system README and the root README status table, and add a `CHANGELOG.md` entry.

## Discovered in 2.1.0 (new, not previously recorded)

| Opportunity | Problem it solves | Why existing material is insufficient | Priority | Status |
|-------------|-------------------|----------------------------------------|----------|--------|
| **Data-loss recovery** (`05-scenarios/data-loss/`) | After accidental deletion, bad migration, or restore failure: what to do in the first hour | `DB-P04/P05` cover migration-caused damage only; nothing addresses scoping the loss, freezing writes, choosing restore vs reconstruct, or communicating | P0 | Discovered |
| **Decommissioning** (`04-process/decommissioning/`) | Retiring a service safely: finding consumers, deprecation window, data retention, teardown verification | Nothing exists; `REL-*` assumes the system continues | P1 | Discovered |
| **Security incident response** (`05-scenarios/security-incident/`) | Containment, evidence preservation, scoping an active compromise, disclosure obligations | `SEC-*` is assessment/remediation of code; `INC-01` is availability-focused and says "involve security" without a procedure | P0 | Discovered |
| **Integration workflow** (planned, in `07-workflows/`; file not yet written) | Merging independently developed frontend/backend/infra work | `REC-P04` verifies seams only; no merge/contract reconciliation procedure | P1 | Discovered |
| **Enterprise readiness** (`04-process/governance-compliance/`) | Control evidence, change management auditability, separation of duties | Only implied; audit produces findings, not control evidence | P2 | Discovered |
| **Data engineering** (`03-domains/data-engineering/`) | Ingest, quality checks, lineage, large backfills | `data-ml-ai` is a skeleton that conflates pipelines with modelling | P1 | Discovered |
| **Mobile / embedded / desktop-CLI domain systems** | Entire technology families with distinct constraints (offline, permissions, hardware, packaging) | No coverage at all | P2 | Discovered |
| **Prototype/spike discipline** (`05-scenarios/prototype/`) | Time-boxed throwaway work that must not leak into production | `from-scratch` assumes the artifact is kept | P3 | Discovered |
| **Failure-path test harness for prompts** | Empirically test prompts against a fixture repository and record outcomes | One run now exists (`_meta/empirical-evaluation-01.md`, `DBG-01`, 3 prompt fixes) but there is no fixture set, scoring sheet, or second-party authorship | P0 (credibility) | Under investigation |
| **Near-duplicate detection** | Detect overlapping prompts before they accumulate | Validator checks identifiers and links only | P2 | Discovered |
| **"Agent handoff" protocol as a reusable component** | Passing a half-finished task between agents without losing state | `WF-HANDOFF` covers stage handoff; not mid-task transfer with uncommitted work | P3 | Discovered |
| **Cost/latency engineering for AI features as its own stage** | Token spend and latency regressions ship silently | `AI-P05` treats it as one section | P3 | Discovered |

### Rejected or deliberately deferred

| Idea | Decision | Reason |
|------|----------|--------|
| A prompt per framework (Next.js, Django, Rails, Spring) | Rejected | Version churn creates maintenance debt and teaches nothing transferable; appendices inside domain systems are the right level |
| Auto-generated prompt variants | Rejected | Volume without differentiation is the failure mode this library exists to avoid |
| Separate "advanced" and "beginner" versions of every system | Rejected | Complexity for the maintainer, marginal benefit; the maturity labels already communicate readiness |
| Per-language prompt families | Deferred | Useful for idioms and tooling, but 5 skeleton systems need depth first |
| Hosted web UI for the catalog | Deferred | Files are the product; a generated catalog plus GitHub navigation is sufficient |

## Discovered in 2.4.0 — engineer problems still unrepresented

Recorded here rather than built immediately, because quality over volume applies to the backlog too. Each entry names the problem in the engineer's words, why the existing material does not solve it, and where it would live.

| # | Problem (as engineers describe it) | Why existing content is insufficient | Likely home | Priority | Status |
|---|-------------------------------------|---------------------------------------|-------------|----------|--------|
| 1 | "Feature flags never get removed and the code has three paths for everything" | `REF-P06` removes *a refactor's* old path; nothing governs flag lifecycle, ownership, or expiry across the product | `04-process/feature-flags/` (5 stages) | P1 | **Implemented** in 2.10.0 |
| 2 | "We broke a client's integration with an API change" | `decommissioning` covers external consumers of a *retired* service; nothing covers versioning, deprecation windows, and consumer tests for a *live* API | `03-domains/backend/` (when promoted) | P1 | Discovered |
| 3 | "The queue backs up at peak and nobody notices until customers do" | `observability` covers signals/SLOs; nothing covers backpressure, consumer lag, poison messages, or load shedding | `04-process/observability-reliability/` P06 | P1 | Discovered |
| 4 | "Tests pass locally and fail in CI" / "works on my machine" | `REC-P04` detects environment drift in recovery; no procedure for parity, containers, or CI-vs-local diagnosis | `05-scenarios/environment-parity/` | P1 | Discovered |
| 5 | "Nobody can reproduce the bug without production data" | `privacy-requests` forbids copying personal data; no procedure for synthetic, masked, or subset test data | `04-process/testing-qa/` P08 (test data) | P2 | Discovered |
| 6 | "Our build takes 25 minutes and CI is the bottleneck" | Nothing covers build-graph analysis, caching, or monorepo task orchestration | `03-domains/devops-infra/` (build systems) | P2 | Discovered |
| 7 | "A refund path double-charged a customer" | Money correctness has no dedicated treatment: idempotency keys, ledger invariants, reconciliation against the provider | `03-domains/payments/` | P1 | Discovered |
| 8 | "The screen reader cannot use our checkout" | `frontend` skeleton names accessibility; there is no audit procedure, criteria set, or verification method | `03-domains/frontend/` (when promoted) | P2 | Discovered |
| 9 | "Translations break layouts and plural forms are wrong" | No coverage of i18n/l10n mechanics: string extraction, pluralisation, locale formats, RTL | `03-domains/frontend/` appendix or its own stage | P3 | Discovered |
| 10 | "Estimates are always wrong and nobody trusts the plan" | `project-management` is a skeleton; no calibration, reference-class forecasting, or uncertainty ranges | `04-process/project-management/` P02 | P2 | Discovered |
| 11 | "Every incident postmortem produces actions nobody completes" | `INC-01` and `OBS-P05` produce actions; nothing tracks completion or verifies the fix prevented recurrence | `04-process/observability-reliability/` P05 extension | P1 | Discovered |
| 12 | "On-call handover loses all context" | `WF-HANDOFF` covers stage handoffs; no on-call-specific shift handover artifact | `05-scenarios/on-call/` | P2 | **Implemented** in 2.14.0 (`ONCALL-01`) |
| 13 | "We cannot tell whether the new prompt version is actually better" | The empirical harness has one run; no A/B evaluation, scoring sheet, or fixture set | `scripts/` + `_meta/empirical-evaluation-*` | P0 | Under investigation |
| 14 | "Three contribution systems say the same thing" | Overlap detection now quantifies it: web, web3, and packages skeletons share up to 18% of their shingles; they are near-variants rather than distinct systems | merge or differentiate when promoted | P2 | Discovered |

### Tools added this cycle

- `scripts/find_overlaps.py` — 5-word shingle containment + Jaccard across all prompts; CI fails above 0.55 containment (currently nothing is close; the highest pair is 0.18 inside the templated contribution skeletons).
- `scripts/new_prompt.py` — scaffolds a prompt with correct metadata and all ten sections, refusing overwrites and printing the index-regeneration commands.

## Discovered in 2.7.0 — prompt inputs and version control

| # | Problem | Why existing material is insufficient | Home | Priority | Status |
|---|---------|---------------------------------------|------|----------|--------|
| 15 | "The prompt says 'the target area' — which area?" | No prompt declared what it needed; `{{}}` placeholders: 0 occurrences, `**Inputs:**`: 0. Agents guessed scope, and multi-stage runs drifted stage to stage | `_meta/prompt-inputs.md`, `00-core/inputs/RUN-SHEET.md`, validator rule | P0 | **Implemented, Integrated** (convention, validator, run sheet; retrofit completed in 2.9.0 — see item 25) |
| 16 | "A merge conflict and the agent took 'ours' for 40 files" | Git appeared only as a prohibition and a push prompt; no resolution procedure, no intent analysis | `04-process/git-operations/P02` | P0 | **Implemented** |
| 17 | "I rewrote history on a shared branch and erased a colleague's work" | "Never rewrite history" was the whole guidance; no shared-vs-local gate, no lease, no coordination protocol | `GIT-P03` | P0 | **Implemented** |
| 18 | "My commits vanished after a bad rebase" | `reflog` appeared in zero prompts; recovery was undocumented and therefore unused | `GIT-P04` | P0 | **Implemented** |
| 19 | "Deleting a secret in a new commit does not remove it" | `00-core` covers handling secrets, not purging them from history, and not the rotate-first rule | `GIT-P03` §6 | P0 | **Implemented** |
| 20 | "We re-argue branch and merge policy every quarter" | No recorded convention, so no decision could be referenced | `GIT-P05` | P1 | **Implemented** |
| 21 | Lockfiles conflict on every branch merge | Mentioned nowhere; causes routine merge pain and broken installs | `GIT-P05` hazard checklist + `GIT-P02` regeneration rule | P1 | **Implemented** (as procedure, not a dedicated prompt) |
| 22 | CI clones the full history of a large monorepo | Not covered; shallow/partial clones and sparse checkout change what history-based prompts can do | `GIT-P05` appendix | P2 | Discovered |
| 23 | Large binaries bloat the repository and cannot be merged | LFS: 0 mentions; binary conflict handling exists, migration does not | `GIT-P05` / a future LFS migration stage | P2 | Discovered |
| 24 | Signed commits and provenance requirements | 0 mentions; increasingly required by enterprise buyers (`GOV-*` will ask for it) | `GIT-P05` + `GOV-P02` evidence | P2 | Discovered |
| 25 | Prompts cannot be composed programmatically because inputs are prose | Fixed by 2.7.0, but only new prompts declared inputs; a retrofit pass makes the whole library machine-runnable | `_meta/prompt-inputs.md` migration | P1 | **Implemented** in 2.9.0 — 109/118 operational prompts declare `Inputs:`; the other 9 are artifact-only stages where an input would be an unused declaration, recorded in `_meta/prompt-inputs.md` |
| 26 | 97 distinct input names for 118 prompts | The retrofit used each prompt's vocabulary; a flat vocabulary is harder to fill once and reuse. Not a correctness defect — every name is declared and used | `_meta/prompt-inputs.md` consolidation pass | P2 | Discovered |
| 27 | Nine operational stages declare no inputs | Not a gap: they are artifact-only stages where a declaration would be unused. Listed so a future reviewer does not "fix" them by inventing inputs | `_meta/prompt-inputs.md` § Migration status | P3 | Evaluated (justified non-implementation) |

## Discovered in 2.11.0 — documentation products and external surfaces

| # | Problem | Why existing material is insufficient | Home | Priority | Status |
|---|---------|---------------------------------------|------|----------|--------|
| 28 | "We need an SRS / design doc / handbook / a PDF for the client" | `documentation` was 8 outlines; no product contracts, no export discipline, no truth gate | `04-process/documentation/` (8 stages) | P0 | **Implemented** in 2.11.0 |
| 29 | "Audit this URL — I don't have the source" | Nothing covered black-box assessment; the naive versions are either useless (headers only) or unauthorised testing | `05-scenarios/live-surface-audit/` (`SURFACE-01`) | P1 | **Implemented** in 2.11.0 |
| 30 | 17 system READMEs claimed "Operational" over skeleton stages | The validator checked prompt overclaims, never system-level ones | `scripts/validate_library.py` `check_system_readmes()` | P0 | **Implemented** in 2.11.0 (fixture-tested) |
| 31 | Requirements change after approval: who updates the SRS, its traceability, and the tests? | Authoring is now covered; change control and traceability maintenance are not | `04-process/documentation/` new stage or `04-process/governance-compliance/` | P1 | Discovered |
| 32 | Accessibility is signal-level only, not WCAG conformance | `SURFACE-01` checks alt text, labels, heading order; conformance needs rendering, assistive tech, and a defined level (AA) | `04-process/accessibility-audit/` (`A11Y-01`) | P2 | **Implemented** in 2.16.0 |
| 33 | Authenticated live-surface testing (staging behind a login) | `SURFACE-01` stops at the login by design; authorised authenticated testing needs its own authorisation model and data-handling rules | `02-engineering/security-hardening/` extension | P2 | Discovered (deliberate exclusion) |
| 34 | Documentation localisation and multi-version docs | Nothing covers translation workflow, versioned doc sets, or "applies to v1.x only" navigation | `04-process/documentation/` P05/P07 extension | P3 | Discovered |
| 35 | Doc export toolchain failures (pandoc/LaTeX/DOCX style collapse) have no known-issue catalogue | P07 says "open every page" but not what usually breaks and how to fix it | `04-process/documentation/` appendix | P3 | Discovered |

## Discovered in 2.12.0 — ownership handover

| # | Problem | Why existing material is insufficient | Home | Priority | Status |
|---|---------|---------------------------------------|------|----------|--------|
| 36 | "The contractor left and still has production access" | Nothing covered revocation as part of a transfer; `WF-HANDOFF` is a state block, not an access procedure | `04-process/handover/P03` (class D) | P0 | **Implemented** in 2.12.0 |
| 37 | "I inherited a system and cannot deploy it" | Handover meant documents; no capability test existed anywhere in the library | `HAND-P04` receiver-performed exercises | P0 | **Implemented** in 2.12.0 |
| 38 | A long-running project resumes under a different agent | `WF-HANDOFF` was draft and had no machine-readable form or authority-boundary field | `WF-HANDOFF` v1.1.0 + `HAND-P02` | P1 | **Implemented** in 2.12.0 |
| 39 | On-call shift handover loses context | Backlog item 12; `HAND-P02`'s operational brief is a partial answer only | `05-scenarios/on-call/` | P2 | **Implemented** in 2.14.0 (`ONCALL-01`); `HAND-P02` still links to it |
| 40 | Legal/contract assignment on agency→client transfers | Handover records the blocker but cannot assign a contract; needs a legal-obligations checklist owned by the client | `04-process/handover/` appendix + `governance-compliance` | P2 | Discovered |
| 41 | Handover of a *portfolio* (many systems in one transfer) | P01 forces a boundary; no procedure for batching several systems with a shared receiver and a staged cutover | `04-process/handover/` P01 extension | P3 | Discovered |

## Discovered in 2.13.0 — timeboxed delivery

| # | Problem | Why existing material is insufficient | Home | Priority | Status |
|---|---------|---------------------------------------|------|----------|--------|
| 42 | A hackathon deadline with judges and a demo | `from-scratch` is a skeleton with no time bound; `quick-fixes` is for defects. Nothing mapped a judging rubric to a demo path, or reserved time for submission | `05-scenarios/hackathon-sprint/` (`HACK-01`) | P1 | **Implemented** in 2.13.0 |
| 43 | Team coordination inside a 24–48 hour event | `HACK-01` freezes scope but does not divide work, resolve merge conflicts between teammates under time pressure, or handle one member becoming unavailable | `05-scenarios/hackathon-sprint/` extension or `07-workflows/multi-agent-orchestration.md` | P2 | Discovered |
| 44 | No licence meant no legal permission to reuse | Default copyright is "all rights reserved"; nothing in the repository addressed it | `LICENSE` (MIT) + `LICENSE-CONTENT` (CC BY 4.0) | P0 | **Implemented** in 2.13.0 |

## Discovered in 2.14.0 — deployment targets, agent surfaces, environments

The batch began with two user questions and surfaced nine more gaps than it closed.

| # | Problem | Why existing material is insufficient | Home | Priority | Status |
|---|---------|---------------------------------------|------|----------|--------|
| 45 | "We deploy to Vercel — does the library know that?" | `vercel`, `netlify`, `railway`, `fly.io`, `heroku`, `cloud run`: **zero** mentions. Release engineering ended at the artifact; nobody provisioned a target, and the three env-var scopes (build / runtime / preview) that cause most "works locally" incidents were undocumented | `05-scenarios/deployment-target/` (`DEPLOY-01` + `PLATFORM-PROFILES.md`) | P0 | **Implemented**, Integrated |
| 46 | "Does it adapt to Cursor / VS Code / my assistant?" | `AGENTS.md` was something to read, never something to author, reconcile, or test. `CLAUDE.md` and `.cursor/rules` were unmentioned as a *set*; adherence was assumed | `04-process/agent-context/` (`CTX-P01..P04`) | P0 | **Implemented**, Integrated |
| 47 | "We are leaving Heroku for Render" | Deploy and decommission existed; the move between them did not. MX records, OAuth callbacks, egress allowlists, and duplicate cron are discovered mid-outage | `05-scenarios/platform-migration/` (`HOSTMIG-01`, class D) | P0 | **Implemented** |
| 48 | "Clone and run" is false | Setup was prose in `CONTRIBUTING.md`; nothing pinned runtimes, removed global installs, or checked case-sensitivity across OSes | `05-scenarios/dev-environment/` (`DEVENV-01`) | P1 | **Implemented** |
| 49 | On-call shift handover (items 12, 39) | Closed by `ONCALL-01`; operational state now has an artifact of its own, distinct from task handoff | `05-scenarios/on-call-handover/` | P1 | **Implemented** |
| 50 | Preview deployments do not match production | `DEPLOY-01` names preview scopes, but nothing covers *preview parity* as a review input: data shape, feature flags on in preview, auth differences, third-party sandboxes | `05-scenarios/deployment-target/` extension | P1 | Discovered |
| 51 | Secrets rotate on a schedule nobody executes | Rotation appears only as an incident response. There is no drill, no "who holds this key", no verification that the old key stopped working | `02-engineering/secrets-rotation/` (`SEC-ROT-01`) | P1 | **Implemented** in 2.16.0 |
| 52 | Performance is never a gate, only an opinion | No performance budget, no Core Web Vitals baseline, no "this PR regressed LCP by 400 ms" check | `05-scenarios/performance-budget/` (`PERF-BUDGET-01`) | P2 | **Implemented** in 2.17.0 |
| 53 | API changes break consumers silently | Contract testing and breaking-change detection are absent; the library reviews code, not interfaces | `03-domains/backend/P09` (`API-VER-01`) | P2 | **Implemented** in 2.17.0 |
| 54 | Monorepo tooling (task graphs, affected-only builds, package boundaries) | Mentioned nowhere; large repositories get advice designed for single-package projects | `05-scenarios/monorepo/` (`MONO-01`) | P2 | **Implemented** in 2.17.0 |
| 55 | SLO definition and error budgets | `observability-reliability` covers dashboards and alerts, not the target the alerts are measured against | — | P2 | **Rejected as duplicate**: `OBS-P03` already defines SLIs, SLOs, error budgets and burn-rate alerting. A draft was written in 2.16.0, compared, and deleted |
| 56 | Prompt injection through third-party agent configs (MCP servers, shared rules) | `CTX-P01` flags permission grants, but not the case where a fetched rule file or tool description carries instructions that redirect the agent | `04-process/agent-context/` extension + `03-domains/ai-agentic/` | P1 | Discovered |
| 57 | Infrastructure is hand-built and undocumented | `DEPLOY-01` provisions through a platform UI or CLI; nothing covers describing it as code, or adopting IaC for an existing estate | `05-scenarios/infrastructure-as-code/` (`IAC-01`) | P2 | **Implemented** in 2.17.0 |
| 58 | Cost of AI-assisted workflow itself (tokens, latency, retries) | `03-domains/cost-engineering/` optimises the product's cloud bill, not the engineering process's model spend | `03-domains/ai-agentic/` extension | P3 | Discovered |
| 59 | Mobile app store release (review, signing, staged rollout) | Release engineering is web/backend shaped; store review queues and phased rollouts have different failure modes | `04-process/release-engineering/` extension | P3 | Discovered |
| 60 | A model's answers drift between runs, so "it worked yesterday" is unverifiable | `_meta/empirical-evaluation` has one executed prompt; no regression suite for prompts themselves | `scripts/` + `_meta/` | P2 | Discovered (same problem as item 13, different angle) |

## Discovered in 2.15.0 — prompt generation, specialized domains, and what those exposed

The batch began with a direct question ("can I generate a prompt from a description?") and a request to deepen specialized fields. The audit that followed found both gaps real, and the work itself exposed eleven more.

| # | Problem | Why existing material is insufficient | Home | Priority | Status |
|---|---------|---------------------------------------|------|----------|--------|
| 61 | "Here's what I want — build me the prompt" | The library had standards for judging prompts (`quality-rubric`, `authoring-standard`) and a scaffolder that emits an empty skeleton, but **no prompt that turns a description into a runnable prompt**. `meta-prompt`, `prompt generator`, `prompt builder` returned zero files | `00-core/prompt-engineering/PROMPT-FORGE.md` (`GEN-P01`) | P0 | **Implemented**, Integrated |
| 62 | "Is the new version of this prompt actually better?" | `_meta/empirical-evaluation-01.md` contains one executed prompt (`DBG-01`); every other operational prompt is structurally reviewed only. No fixture protocol, no baseline comparison | `00-core/prompt-engineering/PROMPT-REGRESSION.md` (`GEN-P02`) | P0 | **Implemented** (protocol); empirical runs still outstanding — see #13/#60 |
| 63 | Blockchain engineering had no domain system | `01-contribution/web3/` answers "how do I contribute to someone's protocol". Nothing covered threat modelling, key custody, upgrades, or exploit response. `reentrancy`, `gas fee`, `EVM` appeared zero times | `03-domains/web3/` (`CHAIN-P01..P04`) | P0 | **Implemented**, Integrated |
| 64 | Mobile had no system at all; store release was backlog item 59 | The client cannot be rolled back and a reviewer gates the release; neither constraint appeared anywhere in the library | `03-domains/mobile/` (`MOB-P01..P03`) | P1 | **Implemented** (supersedes item 59) |
| 65 | Embedded/firmware had no system | Recovery is physical and silence is the dominant failure signal; `firmware` appeared only as a backlog row | `03-domains/embedded-iot/` (`IOT-P01..P02`) | P1 | **Implemented** |
| 66 | Game saves and netcode were unrepresented | `games/` was 8 design-stage skeletons; the two failures that end a player's relationship with a shipped game — corrupted saves and unfair-feeling latency — had no prompt | `03-domains/games/` (`GD-P09`, `GD-P10`) | P1 | **Implemented** (2 of 8 stages now operational) |
| 67 | RAG answers were confident and ungrounded | `AI-P02` chose a retrieval approach; nothing measured recall, citation correctness, abstention, or ACL leakage | `03-domains/ai-agentic/P06` (`AI-P06`) | P0 | **Implemented** |
| 68 | The engineering agent's own blast radius was unreviewed | `AI-P04` covers injection *inside the product*; nothing covered MCP servers, shell access, credential inheritance, unpinned `npx`, or rule files fetched from remote sources | `03-domains/ai-agentic/P07` (`AI-P07`) | P0 | **Implemented** |
| 69 | No empirical evidence for generated prompts | `GEN-P01` emits prompts marked `draft`, but nothing runs them; the draft→operational gate is procedural only | `GEN-P02` executions + `_meta/empirical-evaluation-*` | P1 | Discovered |
| 70 | `01-contribution/web3/README.md` claims "Operational" over 8 skeleton stages | The validator catches prompt-level overclaims and some system-level ones, but not this pattern (a system README claiming operational without a maturity line) | validator rule + README fix | P2 | **Implemented** in 2.16.0 — `README_CLAIM` now matches `**Maturity: operational`; a prose rule catches "Operational" when most stages are outlines and the README does not declare itself mixed. Found three real cases (web, web3, and a games false positive exempted by the mixed rule); the two genuine overclaims were rewritten |
| 71 | Desktop / CLI tooling has no system | A real gap left after this batch; `data engineering` also remains conflated inside `data-ml-ai` | new domain, after backend/frontend promotion | P2 | Discovered |
| 72 | No prompt family index for "make me a prompt for X, Y, Z" | `GEN-P01` handles one prompt at a time; a multi-prompt family request currently becomes several separate runs | `GEN-P01` `decompose` mode extension | P3 | Discovered |
| 73 | Specialized-domain verification is untested | `CHAIN-*`, `MOB-*`, `IOT-*`, `GD-P09/P10` are structurally reviewed, never executed — domain expertise is asserted, not demonstrated | `_meta/empirical-evaluation-*` | P1 | Discovered |
| 74 | Coverage matrix has no row for "domain expertise depth" | The matrix tracks breadth (does a prompt exist) but not whether a domain prompt is *deep enough* to be trusted by a practitioner | `_meta/coverage-matrix.md` §12 | P2 | Discovered |

## Discovered in 2.16.0 — cross-cutting runtime failures

This batch came from asking "what breaks in production that no prompt here would catch?" rather than from a topic list. All six were absent from the library by keyword search, and all six are common enough that most teams will meet them.

| # | Problem | Why existing material is insufficient | Home | Priority | Status |
|---|---------|---------------------------------------|------|----------|--------|
| 75 | Desktop / CLI tooling has no system | The last remaining **Missing** row in the coverage matrix; a CLI's distribution, upgrade, and terminal-accessibility problems are unlike anything covered | `03-domains/desktop-cli/` (`DESK-P01..P02`) | P2 | **Implemented** in 2.17.0 |
| 76 | Date and time correctness (DST, timezones, month arithmetic) | `JOBS-01` covers scheduling in UTC, but not storage formats, DST boundaries in business rules, client-side rendering, or the "off by one day" class of bugs in reports | `02-engineering/time-correctness/` (`TIME-01`) | P1 | **Implemented** in 2.17.0 |
| 77 | Third-party API integration resilience | Nothing covers vendor outage, sandbox-versus-production parity, retry/idempotency across a dependency, or contract drift in someone else's API | `05-scenarios/third-party-integration/` (`INTEG-01`) | P1 | **Implemented** in 2.17.0 |
| 78 | Localisation correctness (plurals, RTL, concatenation, dates, currency) | Docs export (`04-process/documentation/` P07) covers document translation, not UI strings; string concatenation and plural rules break in most non-English locales | `05-scenarios/localization/` (`I18N-01`) | P2 | **Implemented** in 2.17.0 |
| 79 | File uploads and object storage | `DEPLOY-01` mentions ephemeral disk; no prompt covers size limits, MIME sniffing, virus scanning, signed URLs, orphaned objects, or EXIF/personal data in images | `05-scenarios/file-uploads/` (`UPLOAD-01`) | P2 | **Implemented** in 2.17.0 |
| 80 | Search relevance has no evaluation method | `AI-P06` measures RAG grounding, but product search (filters, ranking, typo tolerance, zero-result queries) has no measurement discipline anywhere in the library | `03-domains/frontend/` promotion or a new stage under `03-domains/data-engineering/` | P3 | Discovered |
| 81 | API versioning strategy beyond mobile | `MOB-P03` covers client-version compatibility for apps; public/partner APIs need their own deprecation, sunset and compatibility policy | `03-domains/backend/P09` (`API-VER-01`) | P2 | **Implemented** in 2.17.0 |
| 82 | The validator itself has no regression tests | `check_system_readmes` changed in 2.16.0 and was verified against three real repository cases, not fixtures; a future edit can silently reopen the overclaim it closed | `scripts/test_validator.py` + CI step | P1 | **Implemented** in 2.17.0 — six fixtures; writing them immediately exposed a second defect (the `**Maturity: operational` form was never matched at all) |
| 83 | Domain expertise is asserted, never demonstrated | The matrix now says "Adequate" for web3/mobile/embedded/data on structural review alone; nothing distinguishes a prompt written by someone who has run a production incident in that domain from one that merely sounds right | `_meta/coverage-matrix.md` §12, `GEN-P02` executions | P1 | Discovered (extends #73) |

## Discovered in 2.17.0 — completing the map, and what completeness exposed

The batch closed the last missing domain and nine cross-cutting prompts. Writing them produced four new findings and corrected one earlier judgement.

| # | Problem | Why existing material is insufficient | Home | Priority | Status |
|---|---------|---------------------------------------|------|----------|--------|
| 84 | Disaster recovery had **zero** mentions | `data-loss` handles a deleted table; nothing covered region, account, or provider loss, or proved that a restore works. The most severe untested assumption in the library | `05-scenarios/disaster-recovery/` (`DR-01`) | P0 | **Implemented** in 2.17.0 |
| 85 | Feature sunset (removing a feature customers use) | `decommissioning` retires whole systems; nothing covers retiring one feature, its data, its flags, and its communications | `05-scenarios/feature-sunset/` (`SUNSET-01`) | P2 | **Implemented** in 2.18.0 |
| 86 | Client-side secret leakage (keys in bundles, mobile apps, `EXPO_PUBLIC_*`) | `security-hardening` looks server-side; the build-time-inlined secret is a distinct failure and it ships to every user | `05-scenarios/client-secrets/` (`SECRET-CLIENT-01`) | P1 | **Implemented** in 2.18.0 |
| 87 | Cost anomaly detection (spend spike, runaway query, egress) | `cost-engineering` optimises known spend; nothing alerts on a 10× day or a recursive job | `03-domains/cost-engineering/` extension | P2 | Discovered (assessed in 2.18.0: `COST-P01..P04` already covers anomaly response; a dedicated prompt would duplicate P01's attribution step) |
| 88 | Dependency licence compliance and SBOM consumption | `dependency-management` covers versions and vulnerabilities; licence obligations and SBOM output for customers are governance work nobody owns | `05-scenarios/supply-chain/` (`SUPPLY-01`) | P2 | **Implemented** in 2.18.0 — licence obligations went to `04-process/licence-compliance/` (`LIC-01`), supply-chain integrity to `SUPPLY-01`, because they are different questions |
| 89 | Multi-region and failover design (not just recovery) | `DR-01` restores after loss; nothing describes running actively in two regions without split-brain or double-processing | `02-engineering/architecture-review/` promotion | P3 | Discovered |
| 90 | Data residency and cross-border transfer | Mentioned inside three prompts as a consideration; no procedure for mapping, restricting, or evidencing where data lives | `05-scenarios/data-residency/` (`RESIDENCY-01`) | P2 | **Implemented** in 2.18.0 |
| 91 | The "evidence level" is still not tracked per prompt | The matrix says adequate on structural review; #83 remains open and now applies to 182 operational prompts | `_meta/coverage-matrix.md` §12, `GEN-P02` | P1 | Discovered (unchanged scope, larger surface — now 194 operational prompts) |

## Discovered in 2.18.0 — the compliance and operations layer

The 2.18.0 batch answered three direct questions: does the library cover licences and standards (it now does, `LIC-01`, `STD-01`, `WF-COMPLY`), does it cover automating a described task (`AUTO-01`), and what else was missing. Writing them exposed eight further gaps.

| # | Problem | Why existing material is insufficient | Home | Priority | Status |
|---|---------|---------------------------------------|------|----------|--------|
| 92 | Regression and incident **review of AI-authored changes at scale** | `AIVERIFY-01` verifies one change set; nothing measures whether a team's agent adoption is increasing defect density over time | `07-workflows/agent-adoption.md` extension | P2 | Discovered |
| 93 | **Data migration** between systems (not schema, not platform) | `DB-P01..P05` migrate schema; `05-scenarios/platform-migration/` migrates hosts; nothing covers moving the *records* with reconciliation and a dual-write window | `05-scenarios/data-migration/` (`DATA-MIG-01`) | P1 | **Implemented** in 2.18.0 |
| 94 | **Third-party due diligence** (questionnaires *you* send to vendors) | `std-conformance` answers inbound questionnaires; nothing structures evaluating a vendor's security posture before adoption | `05-scenarios/vendor-due-diligence/` (`VENDOR-01`) | P2 | **Implemented** in 2.19.0 |
| 95 | **Deletion and retention verification across backups** | `PRIV-P02` deletes from systems; backups, logs, and data warehouses are the places deletion is claimed but never checked | `04-process/privacy-requests/P04` (`PRIV-P04`) | P1 | **Implemented** in 2.18.0 |
| 96 | **Capacity planning and quota exhaustion** | `cost-engineering` optimises spend; nothing predicts exhaustion of quotas, connection limits, or storage growth before it becomes an incident | `05-scenarios/capacity-planning/` (`CAPACITY-01`) | P2 | **Implemented** in 2.19.0 |
| 97 | **Access review as a recurring procedure** (not a control claim) | `STD-01` finds that reviews are unevidenced; the actual quarterly procedure — who reviews, against what, with what removal proof — has no home | `02-engineering/access-review/` (`ACCESS-01`) | P1 | **Implemented** in 2.18.0 |
| 98 | **Library-level duplicate detection is shallow** | `find_overlaps.py` measures shingle containment only; prompts can be semantically duplicated with different vocabulary and pass at 0.11 | `scripts/find_overlaps.py` + a second signal | P2 | **Implemented** in 2.19.0 — vocabulary containment, structure similarity, and their product, with `scripts/test_overlaps.py`; embeddings still not used, and the limits of the lexical approach are documented in the module |
| 99 | **No run-sheet examples for multi-prompt sessions** | `00-core/inputs/RUN-SHEET.md` defines the form; there is no worked example joining two systems, so composition is asserted rather than shown | `00-core/inputs/RUN-SHEET-EXAMPLE.md` | P2 | **Implemented** in 2.19.0 |

## Discovered in 2.19.0 — the estate, and the library measuring itself

| # | Problem | Why existing material is insufficient | Home | Priority | Status |
|---|---------|---------------------------------------|------|----------|--------|
| 100 | The `01-contribution` family holds **parallel near-duplicates** | web, web3, and packages-libraries repeat the same stage sequence with different nouns; the combined duplicate metric ranks them highest in the library (0.68). They are legitimately domain-specific *and* legitimately duplicated — nobody has decided which | `01-contribution/VARIANTS.md` | P2 | **Decided** in 2.20.0 — keep three, each overlapping stage must state its domain difference; promotion stays blocked until it does. The differentiation work is #107 |
| 101 | **No worked failure example** for a workflow gate or a failed stage | Workflows define gates and failure routing; nothing shows a refusal being handled. Asserted behaviour, not demonstrated | `07-workflows/failure-examples.md` (`WF-FAILURE`) | P2 | **Implemented** in 2.20.0 |
| 102 | **Abuse and rate limiting** as an engineering problem | `security-hardening` covers admin auth; `02-engineering/tenancy-audit` covers isolation. Credential stuffing, scraping, enumeration, and cost-based abuse of a public endpoint have no home | `05-scenarios/abuse-prevention/` (`ABUSE-01`) | P1 | **Implemented** in 2.19.0 |
| 103 | **Test and fixture data management** (synthetic data, PII in fixtures, seeding) | `testing-qa` writes tests; `privacy-requests` governs production data. The test database full of copied real records, and the fixture that leaks into a screenshot, belong to nobody | `05-scenarios/test-data/` (`TESTDATA-01`) | P2 | **Implemented** in 2.20.0 |
| 104 | **Analytics data modelling** (facts, dimensions, metric definitions) | `data-engineering` covers pipelines, tests and backfills; nothing covers whether the warehouse schema and the metric definitions can answer a question consistently | `03-domains/data-engineering/` extension | P2 | Discovered |
| 105 | **Usage metering and entitlement enforcement** | `payments` handles money movement, `cost-engineering` handles spend; metering a customer's usage against a plan and enforcing limits is a distinct mechanism with its own correctness risks | `05-scenarios/usage-metering/` (`METER-01`) | P2 | **Implemented** in 2.20.0 |
| 106 | **Prompt prose quality is unmeasured** | The validator checks structure, not whether a prompt's instructions are ambiguous or unreadable. A low-cost readability and ambiguity lint would catch the defects a structural check cannot | `scripts/lint_prose.py` + `scripts/test_prose_lint.py` + baseline | P2 | **Implemented** in 2.20.0 — ratchet at 171 findings |

## Discovered in 2.20.0 — usability, and the debt the new measurement exposed

| # | Problem | Why existing material is insufficient | Home | Priority | Status |
|---|---------|---------------------------------------|------|----------|--------|
| 107 | **18 overlapping stages across the three contribution variants** | `VARIANTS.md` decided to keep three systems, but the stage files still differ mainly in nouns; they cannot be promoted until each stage states its domain difference | `01-contribution/{web,web3,packages-libraries}/P02–P07` | P2 | **Implemented** in 2.22.0 — six passes, 18 stage files, each pair now 0.29–0.38 combined (from 0.26–0.68). `P01`/`P08` were left alone by recorded decision; they are low-similarity and genuinely the same job. What remains is execution, not differentiation |
| 108 | **Prose lint baseline of 171 findings** | The ratchet stops regression but the existing corpus still contains "etc." and "where possible" where a prompt should name the items. 68 of the 171 are `etc.`, concentrated in the 16-stage open-source agent | `01-contribution/open-source/general-agent/` first | P2 | **Implemented** in 2.22.0 — burned to **0 findings**; the ratchet is now a gate at zero |
| 109 | **No worked example of a multi-agent run** | `WF-MULTIAGENT` defines ownership and interface freezing; nothing shows two agents integrating, and the failure mode (interface drift) is only described | `07-workflows/multi-agent-worked-example.md` | P2 | **Implemented** in 2.22.0 — two agents, one frozen event schema, one added required field; three rules added to `WF-MULTIAGENT` from the run |
| 110 | **The gallery is a flat list of 358 prompts** | `GALLERY.md` is generated but not navigable by task; a reader who does not know the vocabulary cannot find the right prompt. The quickstart routes five situations and stops there | `scripts/generate_gallery.py` + task index | P2 | **Implemented** in 2.22.0 as `TASKS.md` (21 tasks), with every prompt required to have a home |

## Discovered in 2.21.0 — after conversational mode

| # | Problem | Why existing material is insufficient | Home | Priority | Status |
|---|---------|---------------------------------------|------|----------|--------|
| 111 | **No prompt for the chat session itself as an artifact** | `CHAT-MODE` produces a run, but a long engagement across several chats has no handoff: the state block is described, not specified | `00-core/conversational/` extension | P2 | **Implemented** in 2.22.0 as `CHAT-HANDOFF` |
| 112 | **Prompt selection in chat is still a human task** | `GEN-P01` builds a prompt and `06-interactive/SYSTEM-SELECTOR` routes, but neither is a chat-native "tell me your situation and I will pick the prompt" interaction | `06-interactive/` promotion | P2 | **Implemented** in 2.22.0 as `CHAT-SELECT` — routes labelled `observed` when `TASKS.md` is pasted, `inferred` when not |
| 113 | **The gallery is not navigable by task** | 362 prompts in a flat area list; a visitor who does not know the vocabulary cannot find the right one, and `QUICKSTART` covers five situations only | `scripts/generate_gallery.py` | P2 | **Implemented** in 2.22.0 — `scripts/generate_task_index.py`, `scripts/test_task_index.py`, CI check |
| 114 | **Conversational prompts are unexecuted like the rest** | `CHAT-MODE` is the most testable prompt in the library — two people can run the same chat task and compare outputs — and it has no recorded run | `_meta/evidence.json` | P1 | **Partly done** — `CHAT-DEBUG` executed (2.21.1, `empirical-evaluation-02.md`), `CHAT-SELECT` executed (2.22.0, `empirical-evaluation-03.md`, 4 of 6 routes correct against the generated index); `CHAT-MODE`, `CHAT-REVIEW`, `CHAT-DESIGN`, `CHAT-HANDOFF` still unexecuted |

## Discovered in 2.28.x — the archive audit, and the drift it exposed

The backlog stopped being appended after 2.21.0. Six releases of findings — `06-interactive`'s
four gaps, and the two capability gaps the archive audit named on 2026-10-23 — were recorded in
`review-log.md` and the changelog and never entered here, which is the document that says what to
do next. They are entered now, in the order they were noticed, without renumbering anything.

| # | Problem | Why existing material is insufficient | Home | Priority | Status |
|---|---------|---------------------------------------|------|----------|--------|
| 115 | **Markdown formatting is nobody's job** | `04-process/documentation/DOC-P07` publishes and reviews documentation; it does not restyle an existing tree without touching prose. The audited library can be internally consistent and still visually ragged, and every hand-fix is an unrecorded edit to content | `04-process/documentation/` or `05-scenarios/` (`MARKDOWN-01`) — presentation only, batches of ten, revertible, "a file you formatted and a file you fixed are different claims" | P2 | Discovered 2026-10-23 (`archive/legacy-txt-files/markdown-formatting-pass.txt` is the working draft) |
| 116 | **Nothing decides *between* candidate features** | `02-engineering/feature-design-suggestion` designs a feature once it has been chosen; its stages are skeletons and its P03 *generates* options, it does not score them against each other or against capacity. "Add every possible feature" (`process7(chat2).txt`) has no procedure that ends in a decision | `02-engineering/` (`PORTFOLIO-01`) — restate as a user problem, score on four axes, Now / Next / Not-now, one end-to-end slice; feeds `FD-P01` once a feature is chosen | **P1** | Discovered 2026-10-23; worked example in `archive/legacy-txt-files/feature-portfolio-decision.txt` |
| 117 | **State sentences drift and no gate can see them** | The validator reads counts, identifiers, links, sections and maturity claims. Seven statements about CI, merges and maturity were false for up to five releases in the README and four state documents, because nothing re-reads a sentence that describes state (2.28.8) | A short list in `_meta/release-readiness.md`: the sentences to re-read whenever visibility, CI, rulesets or release count change — plus the habit of dating the correction rather than deleting the error | P2 | Corrected 2026-10-23; the checklist item is not yet written |

