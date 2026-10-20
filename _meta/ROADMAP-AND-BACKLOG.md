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
| `03-domains/backend` | 8 | Largest domain by usage; API/data/reliability practice is thin | operational |
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
| **API design & evolution** | Backend P02 exists as an outline; versioning, idempotency, pagination, and error contracts need depth | fold into backend, or `03-domains/api-design` |
| ~~**Dependency & toolchain management**~~ | **Done in 2.1.0** as `04-process/dependency-management` (5 stages) | — |
| **Accessibility & i18n** | Mentioned in frontend skeleton without criteria; WCAG conformance and localisation are engineering disciplines | `03-domains/frontend` sub-system or `05-scenarios/accessibility-audit` |
| **Data engineering** | `data-ml-ai` conflates pipelines with modelling; ingest/quality/lineage missing | split or extend `03-domains/data-ml-ai` |
| **Embedded / firmware** | No coverage; safety and hardware constraints are materially different | `03-domains/embedded` |
| **Desktop & CLI tools** | No coverage; packaging, updates, and terminal UX are distinct | `03-domains/desktop-cli` |
| **Documentation as engineering** | `04-process/documentation` is a skeleton; README reconstruction, ADRs, and doc-code drift are common | promote existing system |
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
| ~~CI workflow running the validator~~ | Done — `.github/workflows/validate-library.yml` |
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
| 12 | "On-call handover loses all context" | `WF-HANDOFF` covers stage handoffs; no on-call-specific shift handover artifact | `05-scenarios/on-call/` | P2 | Discovered |
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
