# Publication Checklist

**Purpose:** the gate that must pass before this repository becomes public, and the list of things only the owner can do in GitHub settings.

**Audited:** 2026-10-22 (v2.22.0) · **Auditor:** repository maintainer (agent-assisted, evidence below)
**Previous audit:** 2026-10-21 — six changes: the prose lint closed to zero, `TASKS.md` landed, two chat prompts were added, `P06` was differentiated across three variants, a multi-agent run was documented, and the gate list moved into `scripts/check_all.py`. This pass added composition checking, community-file links, the release-readiness page, and the repository configuration record.

---

## 0. Verdict

| Question | Answer |
|---|---|
| Is the **content** safe to publish? | **Yes.** No secrets in the tree or in reachable history, no personal data in prompts, no absolute paths, links resolve, licence files present. |
| Is it **ready** to publish? | **Content yes, infrastructure not yet.** Four things block a good launch, and none is in the repository: CI cannot run (GitHub Actions billing), branch protection is unset, the repository description/topics are unset, and the repository is private. |
| Anything in the repository to fix first? | No. Every automated gate passes; see §1. |

**What must happen before you flip it public is listed in §5.** Everything else here is evidence.

---

## 1. Content gate (re-run at v2.22.0)

| # | Check | Method | Result |
|---|-------|--------|--------|
| 1 | Structural validation | `python3 scripts/validate_library.py` | **PASS** — 476 Markdown files, 364 prompts, **0 errors / 0 warnings** |
| 2 | Maturity honesty | validator rules | **PASS** — 273 operational, 5 draft, 86 skeleton; no label exceeds body; no system README outranks its stages |
| 3 | Executed-prompt count is generated | `scripts/evidence_report.py --check` | **PASS** — `_meta/evidence-levels.md` matches the registry: **26 of 273 operational prompts executed (9.5%)**, stated in the file the README links |
| 4 | Catalog current | `--catalog` + `git diff` | **PASS** — regenerates with no diff |
| 5 | Gallery current | `generate_gallery.py --check` | **PASS** — "up to date", 364 prompts |
| 6 | Duplication | `find_overlaps.py --check` (shingle 0.55) and `--metric combined` (0.75) | **PASS** — highest shingle 0.18; highest combined 0.68, which is the known and *decided* contribution-variant case (`01-contribution/VARIANTS.md`) |
| 6b | Composition | `scripts/check_prompt_contract.py` | **PASS** — 0 errors across 52 systems and 239 dependency links; 147 cite the upstream filename, 10 mention it only by stem, 82 name no artifact — 92 (38%) do not cite a filename, all in skeletons and listed in `_meta/conformance-report.md` |
| 7 | Tooling has tests | `test_validator.py`, `test_overlaps.py`, `test_prose_lint.py`, `test_task_index.py`, `test_contract.py` | **PASS** — 23/23, 13/13, 12/12, 17/17, 19/19 |
| 8 | Prose lint | `lint_prose.py --check` | **PASS** — **0 findings at baseline 0**. The ratchet is now a gate: a new vague qualifier fails CI |
| 9 | Relative links | validator, all links incl. `Depends on` | **PASS** — 0 broken |
| 10 | Secrets in tree | `ghp_*`, `github_pat_*`, `AKIA*`, private-key headers | **PASS** — 0 hits |
| 11 | Secrets in reachable history | `git log --all -p` over the same patterns | **PASS** — 0 hits. *Caveat:* this sandbox checkout presents a single squashed commit, so the scan covers the tree and that commit; the pre-existing remote history was scanned in the 2.13.0 audit and is unchanged since. |
| 12 | Personal data in prompts | emails, customer identifiers, internal hostnames | **PASS** — none. `examples` use `example.com` and invented names |
| 13 | Absolute / environment paths | `/home/user`, sandbox hosts, `arena/<id>` branch names | **PASS** — 1 sandbox path found in `_meta/empirical-evaluation-08.md` on 2026-10-22 and replaced with a placeholder; session branch names still appear in three execution records, deliberately, because they identify which checkout a run happened in |
| 14 | Tracked build artefacts | `git ls-files` | **PASS** — no `__pycache__`, `.pyc`, `node_modules`, `.env` |
| 15 | Repository size | `git ls-files`, `du` | **PASS** — 513 tracked files, 3.6 MB of file content; largest 120 KB (`GALLERY.md`). Re-measured 2026-10-22: the earlier row said 471 files, 4.2 MB and a 112 KB largest file, and all three had drifted. |
| 16 | Community files exist and are linked | validator `check_community` | **PASS** — `LICENSE`, `CONTRIBUTING.md`, `.github/CODE_OF_CONDUCT.md`, `.github/SECURITY.md` present, and each is linked from the document that should point at it |
| 17 | Counts in prose are checked | validator `check_documented_counts` | **PASS** — `PROJECT-STATUS.md` and this file are compared against the tree on every run |
| 18 | Licences | `LICENSE`, `LICENSE-CONTENT`, README section | **PASS** — MIT for code, CC BY 4.0 for content, SPDX-detectable |
| 19 | Every prompt has a home | `generate_task_index.py --check` | **PASS** — 21 tasks, 364 prompts routed, 0 unrouted |
| 20 | One gate list | `scripts/check_all.py` | **PASS** — CI runs that script and nothing else; a local pass is the same run |
| 21 | Counts agree with the tree | validator `check_documented_counts`, `check_stated_totals`, `check_readme_counts` | **PASS** — 476 Markdown files, 364 prompts, 265/5/94 by maturity; the file and prompt totals are compared on every run in the four documents that quote them |
| 22 | Repository settings are decided | `_meta/repository-configuration.md` | **PASS** — description, topics, merge policy, security features and sponsorship decision recorded with the commands; **not yet applied** |

Twenty-two gates. Six are new in this pass: composition (6b), community files and their links (16), prose counts (17), and the three that close the gap between what the documents claim and what the tree contains (15, 21, 22).

## 2. What a reader sees first

Checked against the tree, not against intention:

| Surface | State |
|---|---|
| `README.md` top | Links `QUICKSTART.md` before anything else — the reader gets a task, not a table of contents |
| `QUICKSTART.md` | Six paths (chat-only / broken / inherited / shipping / proof / new), chat-first because that reader has the fewest tools; each with ordered prompts and the artifact you end with; opens with what the library **cannot** do |
| Maturity legend | In the README above the fold; `operational` defined as *structurally reviewed*, not proven |
| `_meta/evidence-levels.md` | Generated; states 9.5% executed (26 of 273); linked from the README and the quickstart |
| `GALLERY.md` | 364 prompts by area, generated; `TASKS.md` indexes the same prompts by problem and fails the build if a prompt has no home |
| Limitations | Stated in README, quickstart, `PROJECT-STATUS.md`, and §3 below — four places, consistent |

## 3. Limitations that must survive publication

These are already stated in the repository. They must not be softened in marketing language, release notes, or a launch post.

1. **Twenty-six prompts have been executed and recorded** (`DBG-01` `-01`; `CHAT-DEBUG` `-02`; `CHAT-SELECT` `-03`; `CHAT-REVIEW` `-04`; `CHAT-MODE` `-05`; `CHAT-DESIGN` `-06`; `CHAT-HANDOFF` `-07`; `GEN-P01` `-08`; `GEN-P02` `-09`; `GIT-P01` to `GIT-P05` `-10`, `-11`; `CR-P01` to `CR-P03` `-12`; `PERF-P01` to `PERF-P07` `-13`; `PKG-P01` `-14`; `MLA-P03` `-15`). 247 are labelled `operational`, which means *structurally complete and reviewed*, not *proven in use*. `_meta/evidence-levels.md` states 26 of 273 — 9.5% — with a generated number, and the review log names what is still unrun by anyone else, and the contribution variants completed in 2.23.1 have procedures but no recorded execution.
2. **Reviews are author self-assessments**, scored in `_meta/review-log.md`. No second reviewer exists.
3. **86 skeleton prompts** are named sequences without verification or failure handling — useful as human checklists, unsafe to run unattended.
4. **Coverage is 116 adequate / 27 partial / 0 missing** dimension rows. No row is missing; 27 are thin, and the matrix names what is thin.
5. **The `01-contribution` variants are differentiated, and unexecuted.** Six stages across three systems now do different work, and every duplicate score is 0.29–0.38 combined. `P01` and `P08` remain outlines by recorded decision. None of the eighteen rewritten stages has been run, and the review log says so for each.
6. **The library cannot make an agent honest.** It defines constraints and evidence rules; a model may still ignore them. `07-workflows/independent-verification.md` and `05-scenarios/ai-output-verification/` exist for exactly that reason.

## 4. Resolved decisions (kept for the record)

| # | Decision | Resolution |
|---|----------|------------|
| 1 | Licence | **Dual**: MIT for code, CC BY 4.0 for content. `LICENSE`, `LICENSE-CONTENT`, README section, SPDX-detectable. (2.13.0) |
| 2 | `archive/legacy-txt-files/` | **Kept** as provenance, excluded from validation, claims explicitly unchecked in its README. (2.13.0) |
| 3 | Commit author email | **Kept** — public contact for a project that asks for issue reports. |
| 4 | Merge strategy | **Squash**, one cycle per PR, narrative in `CHANGELOG.md`. |
| 5 | Contribution variants | **Keep three, differentiate or delete per stage** — `01-contribution/VARIANTS.md` (2.20.0). |

## 5. What only you can do — blocking, in order

Nothing here can be done from the repository, and I cannot do any of it: `gh` returns 403 on repository settings, topics, and Actions with the current token scope.

### 5.1 Fix GitHub Actions billing — **blocking everything else**

Every workflow run fails in ~3 seconds with:

> The job was not started because recent account payments have failed or your spending limit needs to be increased.

Consequences today: PR checks show red without running, the badge is meaningless, and the repository's central claim — *"the validator fails the build if a README over-claims"* — is enforced only when a human runs it locally. Before publishing, this must work, because a visitor's first impression of a CI-enforced project is a red X.

**Where:** GitHub → Settings → **Billing & plans** → Actions. Either add a payment method or set a spending limit above $0.

### 5.2 Branch protection on `main`

| Setting | Value |
|---|---|
| Require a pull request before merging | on |
| Require status checks to pass | `validate` |
| Require branches to be up to date | on |
| Disallow force pushes and deletions | on |
| Allow yourself to bypass while solo | yes (direct pushes during setup) |

### 5.3 Repository description, topics, and social preview

| Field | Suggested |
|---|---|
| Description | "364 prompts for AI coding agents, organised across the engineering lifecycle. Every prompt declares its scope, risk class, and what it will not do — and the repository is validated against those claims in CI." |
| Topics | `ai-agents`, `prompt-engineering`, `llm`, `coding-agents`, `software-engineering`, `code-review`, `incident-response`, `documentation`, `migration`, `developer-tools` |
| Social preview | 1280×640 — title, one-line claim, and the honest numbers: 364 prompts · 273 operational · 17 executed |

### 5.4 Merge settings and branch cleanup

Squash-only; automatically delete head branches.

### 5.5 Security features

| Feature | Why |
|---|---|
| Dependabot alerts + security updates | the only dependencies are `actions/*`; still worth the email |
| Secret scanning + push protection | cheapest possible insurance for a public repository |
| Code scanning (CodeQL, Python) | the scripts are stdlib-only but they run in CI on every PR |
| Private vulnerability reporting | `SECURITY.md` points at it; without it the promise is empty |

### 5.6 Then, and only then, make it public

After the above, in this order: publish → confirm the first Actions run is green on `main` → check `GALLERY.md` renders with working links → confirm the **Security** tab shows `SECURITY.md` → confirm the community-standards checklist is complete → create the release for the current tag.

## 6. Post-publication gate

| Check | When | Why |
|---|---|---|
| CI green on `main` | immediately | a public repository's first impression is its check mark |
| Links render on GitHub | same day | relative-link behaviour differs in the rendered view |
| `evidence-levels.md` linked and reachable | same day | it is the honesty claim the whole project rests on |
| First external issue answered within a week | first week | the repository's own evidence standards should apply to its issue triage |
| Dependabot PR merged or closed within a week | first week | an ignored Dependabot PR tells visitors nobody is home |

---

**Bottom line:** the repository is publishable. What stops it being a *good* launch is the Actions billing failure, which turns the project's strongest property — machine-enforced honesty — into a broken badge.
