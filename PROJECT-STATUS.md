# Project Status — Continuation Checkpoint

**As of:** 2026-10-22 · **Library version:** 2.26.0 · **Branch:** `main` (work delivered in a feature branch, merged by pull request)
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

- **494 Markdown files**, **365 prompt files**.
- Maturity: **286 operational**, **5 draft**, **74 skeleton**.
- **0 validation errors, 0 warnings**.
- Operational systems: open-source contribution agent (16), codebase audit (9), project recovery (7), security hardening (7), testing & QA (7), refactoring (7), database (5), cost engineering (4), privacy requests (3), payments (3), git operations (5), code review (6), feature flags (5), documentation (8), handover (5), hackathon sprint (1), agent context (4), deployment (2), dev environment (1), on-call handover (1), dependency management (5), decommissioning (4), governance and compliance (3), observability & reliability (5), release engineering (4), AI/agentic (5), feature completion (4), independent verification (1), plus licence compliance, standards conformance, automation of described tasks, client-side secrets, supply chain, data residency, feature sunset, incident communications, operational readiness, build performance, AI-output verification, debugging, incident response, flaky-test triage, failed-fix escalation, data-loss recovery, disaster recovery, security incident response, time correctness, third-party integration, file uploads, localisation, infrastructure as code, performance budgets, monorepo health, API versioning, and desktop/CLI (2 stages).
- Every prompt declares identifier, system, version, maturity, execution mode, and risk class.

**The honest summary:** about three quarters of the prompt files are developed to the standard (286 operational, 73%); the rest are outlines that name a sensible stage sequence but lack verification, evidence rules, and failure handling. Thirty-two prompts have been executed and recorded — all by their author, none by a second reader — which is 13.0% of the operational library. That ratio is generated from the registry, and the validator now fails the build if any count in this file or the publication checklist, including prose counts, disagrees with the tree.

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

1. **Little empirical testing.** Thirty-eight prompts have a recorded run — `DBG-01` (`_meta/empirical-evaluation-01.md`), `CHAT-DEBUG` (`-02`), `CHAT-SELECT` (`-03`), `CHAT-REVIEW` (`-04`), `CHAT-MODE` (`-05`), `CHAT-DESIGN` (`-06`), `CHAT-HANDOFF` (`-07`), `GEN-P01` (`-08`), `GEN-P02` (`-09`), `GIT-P01` to `GIT-P05` (`-10`, `-11`), `CR-P01` to `CR-P03` (`-12`) `PERF-P01` to `PERF-P07` (`-13`), `PKG-P01` (`-14`), `MLA-P03` (`-15`), `QA-P01`/`QA-P02` (`-16`, a two-stage composition run against this repository), `QA-P03` to `QA-P06` (`-17`, the rest of that system: seven gaps found, two rules made blocking, twelve fixtures added), `QA-P07` (`-17` §8, the orchestrator run over the six stages it coordinates), `INT-P01` (`-18`, the first `06-interactive` run, failed at v0.1.0 and passed at v1.1.0), and `WIZ-P01`/`INT-P02`/`INT-P03` (`-19`, completing that system: 5 of 14, 0 of 5 and 1 of 8 before their rebuilds). Two of the nine single-stage runs were executed against a real repository and one against a real git fixture; the rest are desk runs. `operational` means structurally reviewed, not proven in use — and 286 prompts carry that label; [`_meta/evidence-levels.md`](_meta/evidence-levels.md) reports 38 of 286, which is 13.3%.
2. **74 skeletons.** Nine families and nine single prompts: `02-engineering/` (architecture-review 7, feature-design-suggestion 7, from-scratch 8, patterns-strategies-methods 7, rewriting-migration 8); `04-process/` (project-management 8, research-and-development 8, systems-building-improvement 8); `01-contribution/language-design` (8); five single `05-scenarios` prompts; and four `06-interactive` stages. The games (2.24.0), data/ML/AI (2.25.0), backend (2.26.0), frontend (2.27.0) and devops-infra (2.28.0) domain families are now operational.
3. **Coverage is complete at the row level, which is not the same as depth.** Every row of `_meta/coverage-matrix.md` has a prompt; **21 of 143 dimension rows are still partial**. Six rows were re-assessed in 2.28.4 because they had been overtaken by completed systems; the other 21 were not re-reviewed, so the adequate count is a floor, not a fresh audit. A named prompt is not a solved problem.
4. **Reviews are self-assessments** by the authoring agent, recorded in `_meta/review-log.md`. Independence is not claimed.
5. **Workflows are untested compositions.** Artifact-name compatibility is maintained by convention and checked by the validator's link rules, not by execution. The multi-agent run documented in 2.22.0 is constructed, not observed.
6. **The duplicate metric cannot see the differentiation that matters.** `P06` now asks for different evidence in each contribution variant, and its vocabulary overlap barely moved; the instrument measures words, not standards of proof.
7. **Composition is checked, but not yet fully named.** Of 239 dependency links between stages, **92 (38%) do not cite the upstream artifact's filename**: 30 mention it only by stem — often a `{{PLACEHOLDER}}` that shares it — and 82 do not mention it at all. An agent moving from one prompt to the next must then invent the mapping. All 92 sit in skeletons without a prerequisites section, which is why the fix is part of promoting them. `_meta/conformance-report.md` lists every one by system.
8. **The chat prompts are barely executed.** `CHAT-DEBUG` and `CHAT-SELECT` have tabletop records; `CHAT-MODE`, `CHAT-REVIEW`, `CHAT-DESIGN` and `CHAT-HANDOFF` have none. The `CHAT-SELECT` run scored 4 of 6 routes against the generated index, which is the only measurement in the library with ground truth outside the prompt.
9. **No prompt has been run by an engineer other than its author**, so the library measures its own writing, not its usefulness.

## 8. Next actions, in order

Completed since this list was written: **conversational mode — any prompt usable in a chat window, with the capability delta stated** (2.21.0); **quickstart, usage metering, test data, worked failure examples, prose lint, and the contribution-variant decision** (2.20.0); **environment parity, capacity planning, vendor due diligence, abuse prevention, duplicate-detection signals, the generated evidence report, and a worked run sheet** (2.19.0); **data migration, access review, deletion verification** (2.18.0); **licence compliance, standards conformance, the compliance workflow, task automation, client-side secret exposure, supply chain integrity, data residency, feature sunset, incident communications, operational readiness, build performance, AI-output verification** (2.18.0); **disaster recovery, time correctness, third-party integration, uploads, localisation, IaC, performance budgets, monorepo, API versioning, desktop/CLI, validator self-tests** (2.17.0); **tenant isolation, secret rotation, background jobs, email deliverability, accessibility audit, data engineering, agent-adoption workflow** (2.16.0); **prompt generation and regression (`GEN-P01/P02`), web3, mobile, embedded/IoT, games save+netcode, RAG grounding, agent permissions** (2.15.0); **deployment targets, host migration, dev environment, agent context, on-call handover** (2.14.0), **project handover** (2.12.0), **documentation products and live surface audit** (2.11.0), **feature flags** (2.10.0), **input declarations across the operational library** (2.9.0 — 109/118 prompts, nine artifact-only stages exempt), **code review** (2.8.0), **git operations and the inputs convention** (2.7.0), **payments** (2.6.0).

1. **Empirical test harness** — backlog #83/#91, with the batch queue in [`_meta/execution-batches.md`](_meta/execution-batches.md). Thirty-eight recorded runs exist, and `_meta/evidence-levels.md` states the ratio (38 of 286). The next unit of value is a run performed by someone other than the prompt author: the batch-0 batch is now fully executed by the author, and every remaining gain in trust needs a second reader.
2. **Execute a contribution stage end to end** — #107 is complete: six passes, 18 files, every pair at 0.29–0.38 combined. The three variants now need a real repository, not more rewriting. `WEB-P02`/`WEB-P07` and `PKG-P02`/`PKG-P07` are the cheapest first runs, because their outputs can be judged against a public issue tracker.
3. **Execute a prompt with an outside check** — the binding limit is no longer coverage. Every one of the 37 recorded runs is author-run; the next unit of trust is a run whose result can be graded by something other than the person who wrote the prompt.
4. **Promote `02-engineering/rewriting-migration` and `from-scratch`** — sixteen stages between them, the largest remaining block of skeletons now that every domain family except `language-design` is operational.
5. **Close the 21 partial coverage rows** — the largest clusters are testing depth, observability at the on-call level, and governance evidence.
6. **Consolidate the input vocabulary** (backlog #26) — cosmetic until a run sheet is reused across systems, then it becomes friction.

## 8a. Release readiness

The full answer is [`_meta/release-readiness.md`](_meta/release-readiness.md); the short version:

- **Content: ready.** 0 validator errors and warnings, 0 prose findings, all counts and links machine-checked, community files present and now linked.
- **Infrastructure: two external items left, both owner-only.** *Corrected in 2.28.8*: this line said "five external blockers" and listed Actions billing, branch protection, metadata and visibility alongside security. Re-measured against the live repository on 2026-10-23: billing cleared with publication (every run since executes all steps), the ruleset exists with an admin bypass, topics and description were applied in the UI, and the repository is public. What remains cannot be done from a token: **the four security settings** (secret scanning, push protection, CodeQL, private vulnerability reporting — all `403` from the API) and **the second sentence of the description** ("Audited by a repo, not a vibe.", also `403`). Both are recorded with the exact UI path in [`repository-configuration.md`](_meta/repository-configuration.md).
- **Trust: the real gap.** 38 of 286 operational prompts have been executed, all by the author, none by a second reader. Batch 0 is complete and has no independent verification.

## 9. How to resume

```bash
python3 scripts/check_all.py        # every gate CI runs, in the same order
python3 scripts/check_all.py --fix  # regenerate catalog, gallery, task index, evidence first
python3 scripts/find_overlaps.py --top 10          # before writing anything that may exist already
python3 scripts/find_overlaps.py --metric combined --top 10   # reworded clones
```

Then: read `_meta/prompt-authoring-standard.md`, copy the structure of an operational system (`02-engineering/codebase-audit/P03-Architecture/` is a compact example), pick an item from `_meta/ROADMAP-AND-BACKLOG.md`, and on completion update the system README status table, the root README table (the validator now fails when its counts disagree with the tree), `TASKS.md` via its generator, `CHANGELOG.md`, `_meta/review-log.md`, and this file.

Never regenerate a skeleton by copy-pasting another system's prose: the value of a prompt is in the domain-specific judgement it encodes.

## 10. Environment and repository facts

- Git: the history before this cycle contains a single commit (`a7aa3e0`), so there is no earlier transcript to recover; the prior state is the working tree itself, preserved and recorded in `CHANGELOG.md`. Work from this cycle reached `main` through one reviewed pull request.
- No `AGENTS.md`/`CLAUDE.md`/editor instruction files existed before this cycle; `AGENTS.md` now exists.
- No build system. `.github/workflows/validate.yml` runs `python3 scripts/check_all.py --verbose` and then fails if the regeneration changed the tree — one workflow, one gate list, the same one a contributor runs locally. **It executes.** *Corrected in 2.28.8*: this line said it failed at startup because Actions billing was blocked. That was true while the repository was private; the first run after publication (`39846014231`) executed steps 1–11 and passed, and every run since — including `39903440904` on 2026-10-23 — has done the same. All scripts are stdlib-only, Python 3.9+.
- `archive/legacy-txt-files/` contains 214 KB of original .txt prompt material. It is source material, not maintained content; do not treat it as canonical.
