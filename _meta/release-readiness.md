<!-- not-a-prompt -->

# Release Readiness — what is done, what is checked, and what still blocks

**Date:** 2026-10-22 · **Version under review:** 2.22.0 · **Branch:** `main` (PR #12 merged, `1dc6f25`; history rewritten the same day, `main` at `3a62a6b`)

This page answers one question honestly: **if this went public tomorrow, what would be wrong with it?** It is written to be uncomfortable, because the alternative — a checklist that says "ready" — is the failure mode the library itself documents.

---

## 1. The short answer

**The repository is ready to be read and not yet ready to be trusted.** Nothing in it is broken, dishonest, or unfinished in a way that a careful reader would call a defect. What it lacks is evidence that the prompts *work*, and that is a category of missing thing rather than a bug to fix before launch.

| Dimension | State | Verdict |
|---|---|---|
| Structural quality | 0 validator errors, 0 warnings, 0 prose findings across 462 files | **Ready** |
| Internal consistency | Counts, links, identifiers, artifact chains, catalog, gallery and task index all machine-checked | **Ready** |
| Honesty about limits | Every claim about execution is generated from a registry, and the counts quoted in prose are compared against the tree on every run; the ratio is 1.8% | **Ready** |
| Community files | Licence (dual), contributing, code of conduct, security policy, issue templates, PR template | **Ready** |
| Repository configuration | Documented in [`repository-configuration.md`](repository-configuration.md), not yet applied | **Action, not debt** |
| CI | The workflow is correct and runs one command; it cannot run on this account because of Actions billing | **Blocked outside the repo** |
| Empirical evidence | 14 of 228 operational prompts executed (6.1%), all by the author, none by a second reader; batch 0 complete, batch 2 begun | **The real gap** |
| Contributor readiness | Templates and gates are in place; the first external PR is untested | **Unknown by definition** |

## 2. What has been tested, by batch

The mechanical pass covers **all 364 prompts**, in seven batches by top-level folder. It checks what a document can be checked for without running a model: metadata, sections, declared inputs against used placeholders, dependency resolution, artifact ownership, cycles, and whether a downstream stage names what its upstream produces.

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

Only the third is evidence of usefulness, and it is 6.1%.

## 4. Blockers, in the order they must be cleared

Outside the repository, and each is a decision or an account, not an edit:

1. **Actions billing.** CI cannot run on this account; the workflow is correct and unexercised. Until it runs once, branch protection cannot require it.
2. **Branch protection on `main`.** Require `validate`, no force pushes, no deletions, linear history. Depends on 1.
3. **Repository metadata.** Description, ten topics, Discussions on, wiki off, squash-only merges. Copy-paste commands in [`repository-configuration.md`](repository-configuration.md).
4. **Security features.** Dependabot, secret scanning with push protection, CodeQL, private vulnerability reporting. All free for public repositories; all enable before the code is public, not after.
5. **Visibility.** Public. Last, because every item above is cheaper to do quietly.

## 5. What is *not* a blocker, and why

Stated because each one will be suggested:

- **More prompts.** 364 is already more than anyone can use; the constraint is trust, not coverage.
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
| 1 | Every structural gate passes on the tree | `python3 scripts/check_all.py` exits 0 | Mandatory | **met** — 15 gates |
| 2 | Counts quoted in prose equal the tree | validator `check_documented_counts`, `check_stated_totals` | Mandatory | **met** |
| 3 | Every prompt composes with its neighbours | `check_prompt_contract.py`, 0 errors; no cycle; no two writers | Mandatory | **met** |
| 4 | No secrets, no personal data, no absolute paths | publication checklist rows 10–13 | Mandatory | **met** |
| 5 | Licence, contributing, conduct, security policy exist **and** are linked | validator `check_community` | Mandatory | **met** |
| 6 | Execution claims are generated from a registry, never hand-maintained | `evidence_report.py --check` | Mandatory | **met** — 9 of 228, 3.9% |
| 7 | Every gate that can be tested has a self-test | five suites, 84 cases total | Mandatory | **met** |
| 8 | Every document that quotes a total is covered by a rule | `DOC_TOTAL_FILES` list | Mandatory | **met** for 4 documents; `_meta/` pages are ordinary prose and were corrected by hand in this pass — a gap, recorded rather than hidden |
| 9 | At least one batch fully executed and written up | batch 0: 8 of 8 | Mandatory | **met** |
| 10 | At least one prompt executed against a real repository, not a fixture | evidence records with a repository target | Mandatory | **met** — `CHAT-REVIEW`, `CHAT-DESIGN` |
| 11 | At least one system executed end to end | an evidence record spanning every stage of one system | Desirable | **partial** — all five `git-operations` stages ran, but across two records (`-10.md`, `-11.md`), not one continuous incident |
| 12 | At least three runs by someone other than the author | evidence entries whose evaluator is not the author | Desirable — and the single biggest gap | **not met**, 0 of 3 |
| 13 | A second reader can resume from the documentation alone | a stranger follows `QUICKSTART.md` and reports | Desirable | **untested** |
| 14 | CI runs the gates on every pull request | a green check on a PR | Mandatory for publication, blocked externally | **blocked** — Actions billing |

**Read the criteria as a pair.** Criteria 1–10 are satisfied, which means the repository can be published as *an audited library*. Criteria 11–13 are not, which means it cannot be published as *a validated one*. Any announcement has to pick one of those two sentences, and the README already picks the first.

## 8. The honest one-line status

> Structurally clean, internally consistent, and unusually candid about its own limits. **Fourteen of 228 procedures have ever been run, all by their author.** Treat it as a well-audited library of procedures, not as a validated one, and say that in any announcement.

## Related

- [`publication-checklist.md`](publication-checklist.md) — the 22 gates and their current state.
- [`repository-configuration.md`](repository-configuration.md) — the settings and the commands.
- [`evidence-levels.md`](evidence-levels.md) — the generated execution count.
- [`conformance-report.md`](conformance-report.md) — the generated composition detail.
