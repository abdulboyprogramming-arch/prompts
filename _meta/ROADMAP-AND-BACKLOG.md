# Roadmap & Backlog

**Version:** 1.0.0
**Last updated:** 2026-10-20

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
| `02-engineering/security-hardening` | 7 | Security claims are the highest-consequence; the current prompts cannot produce defensible findings | operational |
| `02-engineering/refactoring` | 7 | The most common engineering activity, and the most likely to break things | operational |
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
| **Database engineering** | Schema design, migration safety, indexing, and query tuning are scattered across backend/performance stubs | `03-domains/database` (6 stages) |
| **API design & evolution** | Backend P02 exists as an outline; versioning, idempotency, pagination, and error contracts need depth | fold into backend, or `03-domains/api-design` |
| **Dependency & toolchain management** | Referenced by audit P05 as a future system; upgrades, lockfile integrity, and breaking-change assessment have no home | `04-process/dependency-management` (5 stages) |
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
| CI workflow running the validator | Not yet present; would prevent regressions on PRs |
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
