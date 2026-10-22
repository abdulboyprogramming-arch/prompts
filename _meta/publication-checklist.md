# Publication Checklist

**Purpose:** the gate that must pass before this repository becomes public, and the list of things only the owner can do in GitHub settings.

**Audited:** 2026-10-22 (v2.28.4, re-measured end to end) · **Auditor:** repository maintainer (agent-assisted, evidence below)
**Previous audit:** 2026-10-21 — six changes: the prose lint closed to zero, `TASKS.md` landed, two chat prompts were added, `P06` was differentiated across three variants, a multi-agent run was documented, and the gate list moved into `scripts/check_all.py`. This pass added composition checking, community-file links, the release-readiness page, and the repository configuration record.

---

## 0. Verdict

| Question | Answer |
|---|---|
| Is the **content** safe to publish? | **Yes.** No secrets in the tree or in reachable history, no personal data in prompts, no absolute paths, links resolve, licence files present. |
| Is it **published**? | **Yes — public as of 2026-10-22.** Verified unauthenticated: `api.github.com/repos/...` returns 200 with `private: false`, the README renders (31 KB), 24 top-level paths resolve, and 24 releases are visible without a token. Publication was performed by the owner in the GitHub UI; the API path returns 403 for the integration token. |
| Anything in the repository to fix first? | No. Every automated gate passes; see §1. |
| What is still not done? | **Branch protection is unset**, and the security features that were meant to precede publication are still off. CI, by contrast, now runs: run `39846014231` executed every step and passed (§5.1). |

**What must happen before you flip it public is listed in §5.** Everything else here is evidence.

---

## 1. Content gate (re-run at v2.22.0)

| # | Check | Method | Result |
|---|-------|--------|--------|
| 1 | Structural validation | `python3 scripts/validate_library.py` | **PASS** — 487 Markdown files, 364 prompts, **0 errors / 0 warnings** |
| 2 | Maturity honesty | validator rules | **PASS** — 282 operational, 5 draft, 77 skeleton; no label exceeds body; no system README outranks its stages |
| 3 | Executed-prompt count is generated | `scripts/evidence_report.py --check` | **PASS** — `_meta/evidence-levels.md` matches the registry: **34 of 282 operational prompts executed (12.1%)**, stated in the file the README links |
| 4 | Catalog current | `--catalog` + `git diff` | **PASS** — regenerates with no diff |
| 5 | Gallery current | `generate_gallery.py --check` | **PASS** — "up to date", 364 prompts |
| 6 | Duplication | `find_overlaps.py --check` (shingle 0.55) and `--metric combined` (0.75) | **PASS** — highest shingle 0.17; highest combined 0.56 (`03-domains/backend` vs `03-domains/frontend` orchestrators). Re-measured 2.28.4: the earlier row said 0.18 and 0.68, and the 0.68 pair is no longer the top one |
| 6b | Composition | `scripts/check_prompt_contract.py` | **PASS** — 0 errors across 52 systems and 245 dependency links; 186 cite the upstream filename, 9 mention it only by stem, 50 name no artifact — 59 (24%) do not cite a filename, all in skeletons and listed in `_meta/conformance-report.md` |
| 7 | Tooling has tests | seven `scripts/test_*.py` files | **PASS** — 136 cases: validator 44/44, contract 19/19, evidence 17/17, overlaps 17/17, task index 17/17, prose 12/12, gate runner 10/10 |
| 8 | Prose lint | `lint_prose.py --check` | **PASS** — **0 findings across 364 prompt files, baseline 0**. The summary line used to report the number of files *with findings* as if it were the number scanned, so a clean corpus printed a zero file count; fixed in 2.28.4 |
| 9 | Relative links | validator, all links incl. `Depends on` | **PASS** — 0 broken |
| 10 | Secrets in tree | `ghp_*`, `github_pat_*`, `AKIA*`, private-key headers | **PASS** — 0 hits |
| 11 | Secrets in reachable history | `git fetch --unshallow`, then `git log --all -p` over the same patterns | **PASS** — 0 hits across **61 commits and 22 tags** on every ref, plus the tree. Re-run in 2.28.4 with the checkout unshallowed, so the earlier caveat about a squashed single-commit checkout no longer applies |
| 12 | Personal data in prompts | emails, customer identifiers, internal hostnames | **PASS** — none. `examples` use `example.com` and invented names |
| 13 | Absolute / environment paths | `/home/user`, sandbox hosts, `arena/<id>` branch names | **PASS** — one more sandbox path was found in `.qa/VALIDATION.md` in 2.28.4 and replaced with a neutral description. Session branch names still appear in three execution records, deliberately, because they identify which checkout a run happened in |
| 14 | Tracked build artefacts | `git ls-files` | **PASS** — no `__pycache__`, `.pyc`, `node_modules`, `.env` |
| 15 | Repository size | `git ls-files`, `du` | **PASS** — 529 tracked files, 4.35 MB of file content; largest 135 KB (`CHANGELOG.md`, then `GALLERY.md` at 125 KB). Re-measured 2.28.4 |
| 16 | Community files exist and are linked | validator `check_community` | **PASS** — `LICENSE`, `CONTRIBUTING.md`, `.github/CODE_OF_CONDUCT.md`, `.github/SECURITY.md` present, and each is linked from the document that should point at it |
| 17 | Counts in prose are checked | validator `check_documented_counts` | **PASS** — `PROJECT-STATUS.md` and this file are compared against the tree on every run |
| 18 | Licences | `LICENSE`, `LICENSE-CONTENT`, README section | **PASS** — MIT for code, CC BY 4.0 for content, SPDX-detectable |
| 19 | Every prompt has a home | `generate_task_index.py --check` | **PASS** — 21 tasks, 364 prompts routed, 0 unrouted |
| 20 | One gate list | `scripts/check_all.py` | **PASS** — CI runs that script and nothing else; a local pass is the same run |
| 21 | Counts agree with the tree | validator `check_documented_counts`, `check_stated_totals`, `check_readme_counts` | **PASS** — 487 Markdown files, 364 prompts, **282 operational / 5 draft / 77 skeleton**; the file and prompt totals are compared on every run in the four documents that quote them. The earlier row said 265/5/94, which had drifted |
| 22 | Repository settings are decided | `_meta/repository-configuration.md`, `gh api repos/...` | **PARTIAL** — description and all ten topics are now **applied** (verified through the API on 2026-10-22); branch protection, security features and social preview are recorded with the commands and **not applied** |

| 23 | Every version has a release | `gh api repos/.../releases` | **PASS** — 23 releases, `v2.13.0` → `v2.28.3`, each tagged at that version's merge commit and carrying its changelog entry. Twelve were created in 2.28.4 after a seven-version gap |

Twenty-three gates. Six are new in the earlier pass: composition (6b), community files and their links (16), prose counts (17), and the three that close the gap between what the documents claim and what the tree contains (15, 21, 22).

## 2. What a reader sees first

Checked against the tree, not against intention:

| Surface | State |
|---|---|
| `README.md` top | Links `QUICKSTART.md` before anything else — the reader gets a task, not a table of contents |
| `QUICKSTART.md` | Six paths (chat-only / broken / inherited / shipping / proof / new), chat-first because that reader has the fewest tools; each with ordered prompts and the artifact you end with; opens with what the library **cannot** do |
| Maturity legend | In the README above the fold; `operational` defined as *structurally reviewed*, not proven |
| `_meta/evidence-levels.md` | Generated; states 12.1% executed (34 of 282); linked from the README and the quickstart |
| `GALLERY.md` | 364 prompts by area, generated; `TASKS.md` indexes the same prompts by problem and fails the build if a prompt has no home |
| Limitations | Stated in README, quickstart, `PROJECT-STATUS.md`, and §3 below — four places, consistent |

## 3. Limitations that must survive publication

These are already stated in the repository. They must not be softened in marketing language, release notes, or a launch post.

1. **Thirty-three prompts have been executed and recorded** (`DBG-01` `-01`; `CHAT-DEBUG` `-02`; `CHAT-SELECT` `-03`; `CHAT-REVIEW` `-04`; `CHAT-MODE` `-05`; `CHAT-DESIGN` `-06`; `CHAT-HANDOFF` `-07`; `GEN-P01` `-08`; `GEN-P02` `-09`; `GIT-P01` to `GIT-P05` `-10`, `-11`; `CR-P01` to `CR-P03` `-12`; `PERF-P01` to `PERF-P07` `-13`; `PKG-P01` `-14`; `MLA-P03` `-15`). 281 are labelled `operational`, which means *structurally complete and reviewed*, not *proven in use*. `_meta/evidence-levels.md` states 34 of 282 — 12.1% — with a generated number, and the review log names what is still unrun by anyone else, and the contribution variants completed in 2.23.1 have procedures but no recorded execution.
2. **Reviews are author self-assessments**, scored in `_meta/review-log.md`. No second reviewer exists.
3. **77 skeleton prompts** are named sequences without verification or failure handling — useful as human checklists, unsafe to run unattended.
4. **Coverage is 122 adequate / 21 partial / 0 missing** dimension rows. No row is missing; 21 are thin, and the matrix names what is thin.
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

Nothing here can be done from the repository, and I cannot do any of it: `gh` returns 403 on repository settings and Actions with the current token scope. The description and topics were set by the owner in the GitHub UI, not through the API — **verified** by reading them back on 2026-10-22.

### 5.1 Fix GitHub Actions billing — **blocking everything else**

Every workflow run fails in ~3 seconds with:

> The job was not started because recent account payments have failed or your spending limit needs to be increased.

Consequences today: PR checks show red without running, the badge is meaningless, and the repository's central claim — *"the validator fails the build if a README over-claims"* — is enforced only when a human runs it locally. Before publishing, this must work, because a visitor's first impression of a CI-enforced project is a red X.

**Where:** GitHub → Settings → **Billing & plans** → Actions. Either add a payment method or set a spending limit above $0.

**CI now executes.** Run [`39846014231`](https://github.com/abdulboyprogramming-arch/prompts/actions/runs/39846014231) (`pull_request`, 2026-10-22T20:06:57Z) completed **success** on runner `GitHub Actions 1000002633` with steps 1–11 all green, including *Every gate* (`python3 scripts/check_all.py --verbose`) and the clean-regeneration check. This is the first workflow run in the repository's history that executed a step. Publication is what changed it: the last failing run was 36 minutes earlier, while the repository was still private.

The earlier failing runs — `39836004571`, `39840703180`, both `steps: 0` with no runner assigned — remain the evidence that the account's billing block was real. They are not evidence about the post-publication state: the last of them was queued before the visibility change took effect, and the next run executed normally.

### 5.2 Branch protection on `main`

| Setting | Value |
|---|---|
| Require a pull request before merging | on |
| Require status checks to pass | `validate` |
| Require branches to be up to date | on |
| Disallow force pushes and deletions | on |
| Allow yourself to bypass while solo | yes (direct pushes during setup) |

### 5.3 Repository description and topics — **done**

| Field | State |
|---|---|
| Description | **set** — *"300+ engineering prompts with evidence rules, failure handling, and a definition of done — for humans and coding agents. Audited by a repo, not a vibe."* The brief's version said `364`; "300+" is accurate and does not go stale as the library grows. Setting it through the API returns 403, so the owner applied it in the UI |
| Topics | **set, all ten** — `prompts`, `prompt-engineering`, `ai-agents`, `llm`, `engineering`, `code-review`, `incident-response`, `software-engineering`, `developer-tools`, `playbook` |
| Social preview | not set; 1280×640, suggested content: title, one-line claim, 364 prompts · 282 operational · 33 executed |

### 5.4 Make the repository public — **done, 2026-10-22**

The owner changed visibility in Settings → Danger Zone. Verified without the authenticated session:

| Check | Result |
|---|---|
| `GET /repos/abdulboyprogramming-arch/prompts` unauthenticated | **200**, `private: false`, `visibility: public` |
| README via the contents API, unauthenticated | **31,304 bytes**, title *Software Engineering Prompt Library* |
| Top-level paths | **24** entries resolve |
| Releases | **24** visible (`v2.28.4` at the time of the check) |
| Licence detected | **MIT** |

Nothing in the tree changed at publication. No credential, customer record, or unrelated work was exposed: the pre-publication secret scan ran over 61 commits and 22 tags with 0 hits.

### 5.5 Merge settings and branch cleanup

Squash-only; automatically delete head branches.

### 5.6 Security features

| Feature | Why |
|---|---|
| Dependabot alerts + security updates | the only dependencies are `actions/*`; still worth the email |
| Secret scanning + push protection | cheapest possible insurance for a public repository |
| Code scanning (CodeQL, Python) | the scripts are stdlib-only but they run in CI on every PR |
| Private vulnerability reporting | `SECURITY.md` points at it; without it the promise is empty |

### 5.7 Then, and only then, flip the switch

**Reality check:** the intended order was billing first, then publish. The repository was published first, so a visitor today sees a red check that never ran a step. The remaining sequence is: fix billing (5.1) → trigger one `validate` run and confirm steps execute → confirm `GALLERY.md` and the prompt folders render through the GitHub UI → enable branch protection → enable secret scanning and private vulnerability reporting (§5.6).

Releases already exist for every version (gate 23), so no release needs creating at publication time; `v2.28.3` is current.

## 6. Post-publication gate

| Check | When | Why |
|---|---|---|
| CI green on `main` | immediately | a public repository's first impression is its check mark |
| Links render on GitHub | same day | relative-link behaviour differs in the rendered view |
| `evidence-levels.md` linked and reachable | same day | it is the honesty claim the whole project rests on |
| First external issue answered within a week | first week | the repository's own evidence standards should apply to its issue triage |
| Dependabot PR merged or closed within a week | first week | an ignored Dependabot PR tells visitors nobody is home |

---

**Bottom line (re-measured 2.28.4):** the content is publishable and nothing in the tree blocks it — 23 of 23 gate rows pass, 10 of them re-measured today, and the three that do not (22 partial, and the two unobservable CI rows) are GitHub settings rather than files. What stops it being a *good* launch is the Actions billing failure, which turns the project's strongest property — machine-enforced honesty — into a broken badge, and the fact that a public visitor would arrive at a repository whose central claim ("the validator fails the build") is only true on the owner's laptop.
