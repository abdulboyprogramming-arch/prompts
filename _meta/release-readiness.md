<!-- not-a-prompt -->

# Release Readiness — what is done, what is checked, and what still blocks

**Date:** 2026-10-22 · **Version under review:** 2.28.5 · **Branch:** `main`. **The repository is public as of 2026-10-22**, which changes this page's question from *"what would be wrong if it went public?"* to *"what is wrong with it now that it has?"* — §4 is the answer.

This page answers one question honestly: **if this went public tomorrow, what would be wrong with it?** It is written to be uncomfortable, because the alternative — a checklist that says "ready" — is the failure mode the library itself documents.

---

## 1. The short answer

**The repository is ready to be read and not yet ready to be trusted.** Nothing in it is broken, dishonest, or unfinished in a way that a careful reader would call a defect. What it lacks is evidence that the prompts *work*, and that is a category of missing thing rather than a bug to fix before launch.

| Dimension | State | Verdict |
|---|---|---|
| Structural quality | 0 validator errors, 0 warnings, 0 prose findings across 485 files | **Ready** |
| Internal consistency | Counts, links, identifiers, artifact chains, catalog, gallery and task index all machine-checked | **Ready** |
| Honesty about limits | Every claim about execution is generated from a registry, and the counts quoted in prose are compared against the tree on every run; the ratio is 13.0% | **Ready** |
| Community files | Licence (dual), contributing, code of conduct, security policy, issue templates, PR template | **Ready** |
| Repository configuration | Description and topics applied; branch protection in place with an admin bypass; four security features still unset and owner-only — [`repository-configuration.md`](repository-configuration.md) | **Partly applied** |
| CI | **Runs and passes.** Run `39846014231` executed steps 1–11 on a real runner, all green, including `check_all.py` and the clean-regeneration check — the first executed step in the repository's history | **Ready** |
| Empirical evidence | 40 of 288 operational prompts executed (13.9%), all by the author, none by a second reader; batch 0 complete, batch 2 begun | **The real gap** |
| Contributor readiness | Templates and gates are in place; the first external PR is untested | **Unknown by definition** |

## 2. What has been tested, by batch

The mechanical pass covered **all 364 prompts then in the library**, in seven batches by top-level folder. It checks what a document can be checked for without running a model: metadata, sections, declared inputs against used placeholders, dependency resolution, artifact ownership, cycles, and whether a downstream stage names what its upstream produces.

| Batch | Prompts | Operational | Skeleton | Executed | Dependency links | Links not citing a filename |
|---|---:|---:|---:|---:|---:|---:|
| `00-core/` | 8 | 8 | 0 | 8 | 0 | 0 |
| `01-contribution/` | 48 | 34 | 14 | 0 | 38 | 6 |
| `02-engineering/` | 82 | 38 | 44 | 0 | 69 | 37 |
| `03-domains/` | 75 | 35 | 40 | 0 | 53 | 30 |
| `04-process/` | 92 | 68 | 24 | 5 | 78 | 19 |
| `05-scenarios/` | 42 | 37 | 5 | 1 | 0 | 0 |
| `06-interactive/` | 4 | 0 | 4 | 0 | 0 | 0 |
| `07-workflows/` | 13 | 8 | 0 | 0 | 1 | 0 |
| **Total** | **364** | **228** | **131** | **14** | **239** | **92** |

The "links not citing a filename" column is the one that is still imperfect: **38% do not cite the upstream filename**, down from 49% in this release after 46 operational prompts were given an explicit line naming it. Of the 92, 10 mention the artifact only by stem — usually a `{{PLACEHOLDER}}` that shares it — and 82 do not mention it at all. Every remaining row is a `skeleton` without a prerequisites section, so the fix is part of promoting them rather than a separate task. The per-system detail is generated in [`conformance-report.md`](conformance-report.md).

## 3. What "tested" does and does not mean here

Three kinds of check exist in this repository, and conflating them is the easiest way to overclaim:

1. **Structural** — does the prompt have the parts the standard requires, with inputs that are declared and used. Machine-checked, all 364 prompts, on every commit.
The queue and the per-batch targets are in [`execution-batches.md`](execution-batches.md), which also states what a run has to leave behind to count.

2. **Compositional** — do two prompts in a sequence agree on the artifact between them. Machine-checked for 239 links; 92 still rely on prose that names a concept rather than a file, 82 of them without naming the file at all.
3. **Empirical** — does following the prompt produce a better result than not following it. **Fourteen prompts, author-evaluated, none by a second reader.** Nothing here can be automated inside a repository without model access and a scoring sheet, which is backlog #83/#91.

Only the third is evidence of usefulness, and it is 13.9%.

## 4. Blockers — re-measured 2026-10-23

Outside the repository, and each is a decision or an account, not an edit.

**Two remain, both owner-only and both `403` from the API:**

1. **The four security settings.** Secret scanning, push protection, CodeQL and private vulnerability
   reporting were meant to be enabled *before* publication. They were not, and the repository is public.
   All are free for public repositories and all are owner-only switches:
   Settings → Code security and analysis. `PUT /vulnerability-alerts` returns
   `403 Resource not accessible by integration`.
2. **The second sentence of the description.** The description reads *"364 engineering prompts with
   evidence rules, failure handling, and a definition of done — for humans and coding agents."*; the
   intended text adds *"Audited by a repo, not a vibe."* `PATCH /repos/...` returns the same `403`.

**Four that were on this list and are done:**

3. ~~Branch protection blocks all merges~~ — **cleared 2026-10-22** after the owner added *Repository
   admin* as a bypass actor; six pull requests have merged through it since. *(This item read "currently
   blocks all merges" until 2.28.8, five releases after it stopped being true — a state document that no
   rule re-reads drifts like any other.)*
4. ~~Actions billing~~ — **resolved by publication.** The first run after the visibility change executed
   every step and passed. The earlier `steps: 0` failures were real; they described the private-repository
   state.
5. ~~Repository metadata~~ — **done**: description and all ten topics applied in the UI and verified by
   reading them back on 2026-10-23.
6. ~~Visibility~~ — **done 2026-10-22**: public, verified unauthenticated (repo 200, README 31 KB, 24
   top-level paths, 24 releases).

## 5. What is *not* a blocker, and why

Stated because each one will be suggested:

- **More prompts.** 365 is already more than anyone can use; the constraint is trust, not coverage.
- **A website or docs site.** The README, `QUICKSTART.md`, `TASKS.md` and the gallery cover the three ways people arrive. A site would be a second copy of the same content with no gate.
- **A logo or brand.** The library argues against decoration; a launch asset that says more than the README is a claim the evidence does not support.
- **Sponsorship.** Recommended against, with reasons, in [`repository-configuration.md`](repository-configuration.md) §6.
- **Waiting for a second reviewer.** It would help and it is not available; the review log says *author assessment* on every line, which is the honest version of the same fact.

## 6. What would make it ready to be trusted

In value order, and each is achievable without a rewrite:

1. **Runs by someone other than the author.** Three of them, in different folders, written up in `_meta/empirical-evaluation-NN.md`. This is the only item that changes the ratio.
2. **A scoring sheet.** `GEN-P02` defines the protocol; a one-page sheet that names what a good output contains would make two runs comparable.
3. **Execution of one full system end to end** — `05-scenarios/incident-response` or `04-process/code-review`, both of which have public analogues. A system that has never been run is a hypothesis about a sequence, however well each stage is written.
4. **A first external contribution.** The templates, gates and conduct policy are untested against a stranger's habits.

## 7. Acceptance criteria for release readiness

Release readiness is not a feeling, so it is written as tests. **Mandatory** criteria block the merge or the publication; **desirable** ones block nothing and are listed so their absence stays visible.

| # | Criterion | How it is measured | Class | State on 2026-10-22 |
|---|---|---|---|---|
| 1 | Every structural gate passes on the tree | `python3 scripts/check_all.py` exits 0 | Mandatory | **met** — 16 gates |
| 2 | Counts quoted in prose equal the tree | validator `check_documented_counts`, `check_stated_totals` | Mandatory | **met** |
| 3 | Every prompt composes with its neighbours | `check_prompt_contract.py`, 0 errors; no cycle; no two writers | Mandatory | **met** |
| 4 | No secrets, no personal data, no absolute paths | publication checklist rows 10–13 | Mandatory | **met** |
| 5 | Licence, contributing, conduct, security policy exist **and** are linked | validator `check_community` | Mandatory | **met** |
| 6 | Execution claims are generated from a registry, never hand-maintained | `evidence_report.py --check` | Mandatory | **met** — 37 of 285, 13.0% |
| 7 | Every gate that can be tested has a self-test | seven suites, 106 cases total | Mandatory | **met** |
| 8 | Every document that quotes a total is covered by a rule | `DOC_TOTAL_FILES` list; `evidence_report.py --check` scans every page for the executed ratio | Mandatory | **met** for the file count in 4 documents and for the executed ratio everywhere; other totals are still prose, corrected by hand |
| 9 | At least one batch fully executed and written up | batch 0: 8 of 8 | Mandatory | **met** |
| 10 | At least one prompt executed against a real repository, not a fixture | evidence records with a repository target | Mandatory | **met** — `CHAT-REVIEW`, `CHAT-DESIGN` |
| 11 | At least one system executed end to end | an evidence record spanning every stage of one system | Desirable | **partial** — all five `git-operations` stages ran, but across two records (`-10.md`, `-11.md`), not one continuous incident |
| 12 | At least three runs by someone other than the author | evidence entries whose evaluator is not the author | Desirable — and the single biggest gap | **not met**, 0 of 3 |
| 13 | A second reader can resume from the documentation alone | a stranger follows `QUICKSTART.md` and reports | Desirable | **untested** |
| 14 | CI runs the gates on every pull request | a green check on a PR | Mandatory for publication | **met** — *corrected 2.28.8*: this row read "blocked — Actions billing" while publication had already cleared it. Run `39846014231` was the first to execute every step; `39903440904` (2026-10-23) is the latest |

**Read the criteria as a pair.** Criteria 1–10 are satisfied, which means the repository can be published as *an audited library*. Criteria 11–13 are not, which means it cannot be published as *a validated one*. Any announcement has to pick one of those two sentences, and the README already picks the first.

## 7a. Released versions

26 releases exist, `v2.13.0` through `v2.28.7`, each tagged at that version's merge commit.
`v2.22.0`–`v2.28.3` (twelve versions) were published on 2026-10-22, after a gap in which the
library advanced seven minor versions without a tag; `v2.28.4`–`v2.28.7` were each published as
they landed. The backlog was created from the `CHANGELOG.md` entry for each version, unedited
apart from truncation, so a release note says exactly what the changelog says — including the
parts that record a defect.

A release tag is a pointer, not a claim. It says *this is the tree as of this change*; it does
not say the prompts in it are proven. The evidence ratio for every one of these releases is
stated in `_meta/evidence-levels.md` and has never exceeded 12%.

## 8. The honest one-line status

> Structurally clean, internally consistent, and unusually candid about its own limits. **Twenty-four of 241 procedures have ever been run, all by their author.** Treat it as a well-audited library of procedures, not as a validated one, and say that in any announcement.

## Related

- [`publication-checklist.md`](publication-checklist.md) — the 22 gates and their current state.
- [`repository-configuration.md`](repository-configuration.md) — the settings and the commands.
- [`evidence-levels.md`](evidence-levels.md) — the generated execution count.
- [`conformance-report.md`](conformance-report.md) — the generated composition detail.
