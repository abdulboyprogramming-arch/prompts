# Project Status — Continuation Checkpoint

**As of:** 2026-10-21 · **Library version:** 2.24.0 · **Branch:** `main` (work delivered in a feature branch, merged by pull request)
**Read this first** if you are continuing work on this repository. It replaces guesswork about what exists and what was intended.

---

## 1. Mission

Build the most practical, technically rigorous, well-organised software-engineering prompt library that can be maintained as a living repository: coverage of the full engineering lifecycle, honest quality signalling, enforceable standards, and composable systems — not maximum file count.

## 2. What this repository is

A collection of Markdown prompt systems for software engineering, organised by activity:

```
00-core/         Foundational primitives: safety categories, orchestration, base agent contract
01-contribution/ Contributing to existing projects (one developed system, four skeletons)
02-engineering/  Audits, recovery, architecture, refactoring, migration, performance, security
03-domains/      Backend, frontend, devops, data engineering, data/ML, games, AI-agentic, desktop/CLI
04-process/      Testing, review, documentation, PM, research, observability, release
05-scenarios/    Single-purpose prompts (debugging, incidents, flaky tests, onboarding, …)
06-interactive/  Context collectors and wizards
07-workflows/    Composed multi-system sequences with gates and a handoff contract
_meta/           Authoring standard, quality rubric, taxonomy, catalog, roadmap, review log
scripts/         validator, validator self-tests, gallery and catalog generators, overlap search, scaffolder
archive/         Legacy .txt source material, retained for provenance
```

## 3. Current state (measured)

Run `python3 scripts/validate_library.py` for live numbers. At the time of writing:

- **460 Markdown files**, **364 prompt files**.
- Maturity: **213 operational**, **5 draft**, **146 skeleton**.
- **0 validation errors, 0 warnings**.
- Operational systems: open-source contribution agent (16), codebase audit (9), project recovery (7), security hardening (7), testing & QA (7), refactoring (7), database (5), cost engineering (4), privacy requests (3), payments (3), git operations (5), code review (6), feature flags (5), documentation (8), handover (5), hackathon sprint (1), agent context (4), deployment (2), dev environment (1), on-call handover (1), dependency management (5), decommissioning (4), governance and compliance (3), observability & reliability (5), release engineering (4), AI/agentic (5), feature completion (4), independent verification (1), plus licence compliance, standards conformance, automation of described tasks, client-side secrets, supply chain, data residency, feature sunset, incident communications, operational readiness, build performance, AI-output verification, debugging, incident response, flaky-test triage, failed-fix escalation, data-loss recovery, disaster recovery, security incident response, time correctness, third-party integration, file uploads, localisation, infrastructure as code, performance budgets, monorepo health, API versioning, and desktop/CLI (2 stages).
- Every prompt declares identifier, system, version, maturity, execution mode, and risk class.

**The honest summary:** roughly two fifths of the prompt files are developed to the standard (213 operational); the rest are outlines that name a sensible stage sequence but lack verification, evidence rules, and failure handling. Two prompts have been empirically executed — one engineering (`DBG-01`), one conversational (`CHAT-DEBUG`) — which is 1.0% of the operational library. That ratio is stated everywhere it matters, and the validator fails the build if a README over-claims.

## 4. Standards that now govern the repository

| Concern | Authority |
|---------|-----------|
| What a valid prompt must contain | `_meta/prompt-authoring-standard.md` |
| How to score one | `_meta/quality-rubric.md` |
| Where it belongs | `_meta/taxonomy.md` |
| What is missing / next | `_meta/ROADMAP-AND-BACKLOG.md` |
| Review history and maturity justifications | `_meta/review-log.md` |
| Machine-readable inventory | `_meta/CATALOG.md` (generated) |
| Shared state passing between stages | `07-workflows/HANDOFF-CONTRACT.md` |

Non-negotiable rules established this cycle:

1. **Maturity is a claim about the artifact**, enforced by the validator. `skeleton` versions are `0.x`; `1.x` implies review.
2. **No status overclaim.** A system README cannot advertise operational status while its stages are outlines.
3. **Risk class is declared and honest.** Read-only prompts are `A`; a read-only prompt mentioning `git push` warns.
4. **One canonical template.** The old second template is now a pointer.
5. **No empty folders.** A domain folder exists only when it has content.

## 5. What changed in this cycle (2.0.0)

Full detail in `CHANGELOG.md`. Summary:

- Added the standards, rubric, validator, catalog, workflows, project-recovery, observability-reliability, release-engineering, and AI/agentic systems.
- Rewrote codebase-audit (9 stages), testing-qa (7), debugging, and incident response to operational depth.
- Migrated all prompt files to the metadata schema; demoted 172 outlines to `skeleton`; corrected two overclaiming READMEs.
- Replaced the root README's marketing claims with an accurate status table.

## 6. Decisions made (and why)

| Decision | Rationale |
|----------|-----------|
| Demote rather than delete the 172 outlines | The sequences are useful as human checklists and as scaffolding for future work; deleting would lose intent. Labelling makes them safe. |
| Rewrite two systems rather than start new ones | The advertised systems were the weakest; fixing them raises credibility more than adding breadth. |
| Add project-recovery as a new family | The most common real-world starting condition (inherited/interrupted project) had no coverage. |
| Keep identifiers global and system-prefixed | Bare `P03`-style IDs (used in the contribution agent) do not collide today but will; new systems use prefixes. Existing ones are flagged, not renamed, to avoid breaking references. |
| Vendor-neutral observability and release guidance | Stack-specific content dates quickly; the system teaches transferable procedure and leaves tooling to appendices. |
| CI validates structure, not quality | A workflow now runs the validator and catalog freshness check; empirical prompt testing remains an open gap. |

## 7. Known weaknesses (do not paper over)

1. **Almost no empirical testing.** One prompt has a recorded run against a synthetic fixture (`_meta/empirical-evaluation-01.md`, `DBG-01`). `operational` means structurally reviewed against the rubric, not proven on a real repository — and 208 prompts now carry that label; [`_meta/evidence-levels.md`](_meta/evidence-levels.md) reports how many have been executed, which is one.
2. **149 skeletons.** Concentrated in `02-engineering/` (architecture-review, migration, performance-investigation), `03-domains/` (frontend, devops-infra, data-ml-ai, games, security, backend's seven remaining stages) and `04-process/` (PM, code review variants).
3. **Coverage is complete at the row level, which is not the same as depth.** Every row of `_meta/coverage-matrix.md` has a prompt; **27 of 143 dimension rows are still partial**, and 5 of 15 workflow rows. A named prompt is not a solved problem.
4. **Reviews are self-assessments** by the authoring agent, recorded in `_meta/review-log.md`. Independence is not claimed.
5. **Workflows are untested compositions.** Artifact-name compatibility is maintained by convention and checked by the validator's link rules, not by execution.
6. **`01-contribution/open-source/general-agent` has no "check ran vs not run" distinction.**
7. **No prompt has been run by an engineer other than its author**, so the library measures its own writing, not its usefulness.

## 8. Next actions, in order

Completed since this list was written: **conversational mode — any prompt usable in a chat window, with the capability delta stated** (2.21.0); **quickstart, usage metering, test data, worked failure examples, prose lint, and the contribution-variant decision** (2.20.0); **environment parity, capacity planning, vendor due diligence, abuse prevention, duplicate-detection signals, the generated evidence report, and a worked run sheet** (2.19.0); **data migration, access review, deletion verification** (2.18.0); **licence compliance, standards conformance, the compliance workflow, task automation, client-side secret exposure, supply chain integrity, data residency, feature sunset, incident communications, operational readiness, build performance, AI-output verification** (2.18.0); **disaster recovery, time correctness, third-party integration, uploads, localisation, IaC, performance budgets, monorepo, API versioning, desktop/CLI, validator self-tests** (2.17.0); **tenant isolation, secret rotation, background jobs, email deliverability, accessibility audit, data engineering, agent-adoption workflow** (2.16.0); **prompt generation and regression (`GEN-P01/P02`), web3, mobile, embedded/IoT, games save+netcode, RAG grounding, agent permissions** (2.15.0); **deployment targets, host migration, dev environment, agent context, on-call handover** (2.14.0), **project handover** (2.12.0), **documentation products and live surface audit** (2.11.0), **feature flags** (2.10.0), **input declarations across the operational library** (2.9.0 — 109/118 prompts, nine artifact-only stages exempt), **code review** (2.8.0), **git operations and the inputs convention** (2.7.0), **payments** (2.6.0).

1. **Empirical test harness** — backlog #83/#91. Two executed runs exist, and `_meta/evidence-levels.md` now states the ratio (2 of 213 operational prompts). The next unit of value is a fixture set, a scoring sheet, and runs performed by someone other than the prompt author. Until then every `operational` label is a structural claim.
2. **Differentiate the 18 overlapping contribution stages** (backlog #107) — one stage across all three variants per pass; #100 decided the policy and this is the work.
3. **Promote `03-domains/backend`'s seven remaining skeleton stages** — it is the largest domain and now has a ninth stage (`P09`) that is operational while stages P01–P08 are outlines.
4. **Promote `03-domains/frontend`** — accessibility and state management are named but lack pass criteria; `PERF-BUDGET-01` now covers budgets, but only from the outside.
4. **Close the 29 partial coverage rows** — the largest clusters are testing depth, observability at the on-call level, and governance evidence.
6. **Burn down the prose-lint baseline** (backlog #108) — 171 findings, starting with the 68 `etc.` in the open-source agent.
7. Consolidate the input vocabulary (backlog #26) — cosmetic until a run sheet is reused across systems, then it becomes friction.

## 9. How to resume

```bash
python3 scripts/test_validator.py               # validator self-tests, must be 6/6
python3 scripts/validate_library.py             # must show 0 errors
python3 scripts/validate_library.py --catalog   # regenerate _meta/CATALOG.md after changes
python3 scripts/generate_gallery.py --write     # regenerate GALLERY.md
python3 scripts/find_overlaps.py --top 10       # before writing anything that may exist already
```

Then: read `_meta/prompt-authoring-standard.md`, copy the structure of an operational system (`02-engineering/codebase-audit/P03-Architecture/` is a compact example), pick an item from `_meta/ROADMAP-AND-BACKLOG.md`, and on completion update: the system README status table, root README table, `CHANGELOG.md`, `_meta/review-log.md`, and this file.

Never regenerate a skeleton by copy-pasting another system's prose: the value of a prompt is in the domain-specific judgement it encodes.

## 10. Environment and repository facts

- Git: the history before this cycle contains a single commit (`a7aa3e0`), so there is no earlier transcript to recover; the prior state is the working tree itself, preserved and recorded in `CHANGELOG.md`. Work from this cycle reached `main` through one reviewed pull request.
- No `AGENTS.md`/`CLAUDE.md`/editor instruction files existed before this cycle; `AGENTS.md` now exists.
- No build system. CI (`.github/workflows/validate-library.yml`) runs `scripts/test_validator.py` (six fixtures for the validator's own rules), then the validator, then the catalog and gallery freshness checks. All scripts are stdlib-only, Python 3.9+.
- `archive/legacy-txt-files/` contains 214 KB of original .txt prompt material. It is source material, not maintained content; do not treat it as canonical.
