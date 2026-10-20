# Project Status — Continuation Checkpoint

**As of:** 2026-10-20 · **Library version:** 2.1.0 · **Branch:** `arena/d745d222-prompts`
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
03-domains/      Backend, frontend, devops, data/ML, games, AI-agentic
04-process/      Testing, review, documentation, PM, research, observability, release
05-scenarios/    Single-purpose prompts (debugging, incidents, flaky tests, onboarding, …)
06-interactive/  Context collectors and wizards
07-workflows/    Composed multi-system sequences with gates and a handoff contract
_meta/           Authoring standard, quality rubric, taxonomy, catalog, roadmap, review log
scripts/         validate_library.py (validator + catalog generator)
archive/         Legacy .txt source material, retained for provenance
```

## 3. Current state (measured)

Run `python3 scripts/validate_library.py` for live numbers. At the time of writing:

- **362 Markdown files**, **287 prompt files**.
- Maturity: **132 operational**, **6 draft**, **149 skeleton**.
- **0 validation errors, 0 warnings**.
- Operational systems: open-source contribution agent (16), codebase audit (9), project recovery (7), security hardening (7), testing & QA (7), refactoring (7), database (5), cost engineering (4), privacy requests (3), payments (3), git operations (5), code review (6), feature flags (5), documentation (8), dependency management (5), decommissioning (4), governance and compliance (3), observability & reliability (5), release engineering (4), AI/agentic (5), feature completion (4), independent verification (1), plus debugging, incident response, flaky-test triage, failed-fix escalation, data-loss recovery, and security incident response.
- Every prompt declares identifier, system, version, maturity, execution mode, and risk class.

**The honest summary:** roughly two fifths of the prompt files are developed to the standard (132 operational); the rest are outlines that name a sensible stage sequence but lack verification, evidence rules, and failure handling. One prompt has been empirically executed. That ratio is stated everywhere it matters, and the validator fails the build if a README over-claims.

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

1. **No empirical testing.** No prompt has a recorded run against a real repository. `operational` means structurally reviewed, not proven.
2. **165 skeletons.** Domains most affected: backend, frontend, devops-infra, data-ml-ai, games, security-hardening, refactoring, architecture-review, migration, PM, documentation, code review.
3. **Missing families:** mobile, database, embedded, desktop/CLI, dependency management, governance/compliance, multi-agent orchestration, accessibility/i18n depth.
4. **Reviews are self-assessments** by the authoring agent, recorded in `_meta/review-log.md`. Independence is not claimed.
5. **No duplicate/near-duplicate detection** beyond identifiers and titles.
6. **Workflows are untested compositions**; artifact-name compatibility is maintained by convention.
7. **`01-contribution/open-source/general-agent` has no "check ran vs not run" distinction**; its inputs are now declared like the rest of the library, but its stage artifacts are still free-form.

## 8. Next actions, in order

Completed since this list was written: **documentation products and live surface audit** (2.11.0), **feature flags** (2.10.0), **input declarations across the operational library** (2.9.0 — 109/118 prompts, nine artifact-only stages exempt), **code review** (2.8.0), **git operations and the inputs convention** (2.7.0), **payments** (2.6.0).

1. **Empirical test harness** — one executed run now exists (`_meta/empirical-evaluation-01.md`: `DBG-01` against a synthetic fixture, three prompt fixes). Next: a fixture set, a scoring sheet, and fixtures authored by someone other than the prompt author. Every other `operational` label remains a structural review.
2. Promote `03-domains/backend` (8 stages) — highest-value remaining skeleton; it also supplies the home for live-API versioning.
3. `03-domains/data-engineering/` (ingest, quality, lineage) — the largest remaining missing dimension.
4. Empirical evaluation of a second prompt, ideally by someone other than its author.
5. Mobile / embedded / desktop-CLI domain systems, in that order of demand.
6. Consolidate the input vocabulary (97 names; backlog item 26) — cosmetic until a run sheet is reused across systems, then it becomes friction.

## 9. How to resume

```bash
python3 scripts/validate_library.py            # must show 0 errors
python3 scripts/validate_library.py --catalog  # regenerate _meta/CATALOG.md after changes
```

Then: read `_meta/prompt-authoring-standard.md`, copy the structure of an operational system (`02-engineering/codebase-audit/P03-Architecture/` is a compact example), pick an item from `_meta/ROADMAP-AND-BACKLOG.md`, and on completion update: the system README status table, root README table, `CHANGELOG.md`, `_meta/review-log.md`, and this file.

Never regenerate a skeleton by copy-pasting another system's prose: the value of a prompt is in the domain-specific judgement it encodes.

## 10. Environment and repository facts

- Git: branch `arena/d745d222-prompts`, branched from `main` at `a7aa3e0` ("chore: archived my previous prompts set"). History contains one commit before this cycle, so there is no earlier agent transcript to recover — the prior state is the working tree itself, which has been preserved and is recorded in `CHANGELOG.md`.
- No `AGENTS.md`/`CLAUDE.md`/editor instruction files existed before this cycle; `AGENTS.md` now exists.
- No build system and no tests. CI (`.github/workflows/validate-library.yml`) runs the validator and the catalog freshness check. The only executable artifact is `scripts/validate_library.py` (stdlib-only, Python 3.9+).
- `archive/legacy-txt-files/` contains 214 KB of original .txt prompt material. It is source material, not maintained content; do not treat it as canonical.
