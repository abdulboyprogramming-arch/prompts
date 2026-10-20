# Publication Checklist

**Purpose:** the gate that must pass before this repository becomes public. Every line is a check that was run, with its result. A check that was not run is listed as *not run*, not assumed.

**Audited:** 2026-10-20 · **Version:** 2.13.0 · **Auditor:** repository maintainer (agent-assisted, evidence below)

---

## 1. Content gate

| # | Check | Method | Result |
|---|-------|--------|--------|
| 1 | Structural validation | `python3 scripts/validate_library.py` | **PASS** — 370 Markdown files, 293 prompts, 0 errors / 0 warnings |
| 2 | Maturity honesty | validator rules | **PASS** — 139 operational, 5 draft, 149 skeleton; no label exceeds body; no README outranks its stages |
| 3 | Catalog current | `validate_library.py --catalog` + `git diff` | **PASS** — `_meta/CATALOG.md` regenerates with no diff |
| 4 | Gallery current | `generate_gallery.py --check` | **PASS** — "GALLERY.md is up to date" |
| 5 | Duplication | `find_overlaps.py --check` (bar 0.55) | **PASS** — no pair above threshold |
| 6 | Relative links | 966 links resolved against the filesystem | **PASS** — 0 broken |
| 7 | Secrets in tree | patterns: `ghp_*`, `github_pat_*`, `AKIA*`, private-key headers, `password|secret|token = "…"` | **PASS** — 0 hits |
| 8 | Secrets in history | `git log --all -p` over the same patterns | **PASS** — 0 hits |
| 9 | Personal data in prompts | grep for emails, customer identifiers, internal hostnames | **PASS** — none in prompt content; commit authorship is the maintainer's own |
| 10 | Absolute or environment paths | grep `/home/user`, sandbox hosts, session branch names | **PASS** — 0 hits (3 fixed this cycle: `PROJECT-STATUS` branch line, an `arena/…` example, and a stale version header) |
| 11 | Compiled artifacts | `git ls-files` review | **FIXED** — 3 `__pycache__/*.pyc` files were tracked; removed and `.gitignore` added |
| 12 | Repository size | `git ls-files` + `du` | **PASS** — 388 tracked files, 3.0 MB total; largest file 92 KB |
| 13 | CI on the head commit | `gh run list`, PR checks | **PASS** — 4 gates green (validate, catalog freshness, gallery freshness, overlaps) |
| 14 | Repo hygiene | root listing | **PASS** — no `node_modules`, no `.env`, no editor droppings, no build output |

## 2. Community and policy files

| File | Status |
|------|--------|
| `README.md` | present — routing table, maturity table, honest limitations |
| `CONTRIBUTING.md` | present — standards, validation commands, promotion bar |
| `AGENTS.md` | present — instructions for agents working in this repository |
| `.github/SECURITY.md` | **added this cycle** — scope, private reporting route, response times |
| `.github/CODE_OF_CONDUCT.md` | **added this cycle** — evidence-based conduct, private reporting |
| `.github/pull_request_template.md` | **added this cycle** — reproduces the library's own bar as checkboxes |
| `.github/ISSUE_TEMPLATE/{bug,prompt-request}.md` + `config.yml` | **added this cycle** — no blank issues; security routed privately |
| `LICENSE` | **added 2.13.0, corrected 2.13.1** — exact MIT text so GitHub detects SPDX `MIT` (the appended scope note made it read as "Other") |
| `LICENSE-CONTENT` | **added 2.13.0** — CC BY 4.0 for prompts and prose, with attribution and endorsement boundary |
| `CHANGELOG.md` | present — 2.6.0 → 2.12.0 in this cycle |
| `.gitignore` | **added this cycle** |

## 3. Known limitations that must survive publication

These are stated in the repository and must not be quietly dropped from the public framing:

1. **One prompt has been empirically executed** (`DBG-01`, `_meta/empirical-evaluation-01.md`). Every other `operational` label means *structurally complete and reviewed*, not *proven in use*.
2. **Reviews are author self-assessments** with rubric scores in `_meta/review-log.md`. There is no second, independent reviewer.
3. **149 skeleton systems** are named sequences without verification or failure handling. They are labelled as such in every index.
4. **Coverage is 72 adequate / 30 partial / 4 missing** dimension rows. The four missing are named: data engineering, mobile, embedded, desktop/CLI.
5. **The library cannot make an agent honest.** It defines constraints and evidence rules; a model may still ignore them. The prompts that verify another agent's claims (`07-workflows/independent-verification.md`) exist for exactly that reason.

## 4. Decisions required before publication

| # | Decision | Options | Recommendation |
|---|----------|---------|----------------|
| 1 | ~~**Licence**~~ | — | **RESOLVED 2.13.0**: dual — MIT for code, CC BY 4.0 for content. `LICENSE` + `LICENSE-CONTENT` added, README section added. |
| 2 | ~~**`archive/legacy-txt-files/`**~~ | — | **RESOLVED 2.13.0**: kept, with the README rewritten as provenance framing — what they are, that they are excluded from validation, that their claims are unchecked. No history rewrite. |
| 3 | **Commit author email** | keep · switch going forward | **Decided: keep.** It is the maintainer's public contact for a project that asks people to report issues; changing it now would not remove it from history anyway. |
| 4 | **Merge strategy** | squash · merge commit · rebase | **Squash** — one development cycle, and the CHANGELOG carries the narrative. Applied to PR #1. |
| 5 | **Tag / release** | `v2.13.0` with release notes from the CHANGELOG | **Done** — tag and release created after the merge, so the public reference matches a validated tree. |

## 5. Platform settings to apply (outside the repository)

GitHub → repository → **Settings**:

| Area | Setting | Suggested value |
|------|---------|-----------------|
| General | Description | "292 prompts for AI coding agents: audits, refactors, migrations, incidents, reviews, releases, documentation, handover. Every prompt declares scope, risk class, and what it will not do — and the repo is validated against those claims in CI." |
| General | Topics | `ai-agents`, `prompt-engineering`, `llm`, `coding-agents`, `software-engineering`, `code-review`, `incident-response`, `documentation`, `migration`, `developer-tools`, `claude`, `gpt` |
| General | Website | leave empty unless you publish a docs site |
| General | Social preview | 1280×640 image — title, one-line claim, the four numbers (292 / 138 / 0 errors / 4 gates) |
| General | Features | Issues **on**; Discussions **optional** (off is fine — the library prefers issues with evidence); Wiki **off** (docs live in the repo); Projects **off** unless you plan a roadmap board |
| General | Merge button | Allow **squash** only; disable merge commits and rebase if you want a linear history |
| General | Automatically delete head branches | **on** |
| Branches | Default branch | `main` |
| Branches | Protection on `main` | Require the `validate` check to pass; require a PR before merging; disallow force pushes and deletions (allow yourself to bypass while solo) |
| Actions | General | Allow actions and reusable workflows; default `GITHUB_TOKEN` permissions **read-only** (the workflow already declares `contents: read`) |
| Security | Dependabot alerts + security updates | **on** (the only dependency is `actions/*`, pinned to major tags) |
| Security | Secret scanning + push protection | **on** where available on your plan |
| Security | Code scanning (CodeQL) | **on** — Python only, cheap, and it closes the "no static analysis" gap |
| Security | Private vulnerability reporting | **on** — `SECURITY.md` points at it |
| Moderation | Interaction limits / blocked users | leave default |

After publication, in the repository:

- Create release **`v2.12.0`**, target `main`, notes: the `[2.12.0]` section of `CHANGELOG.md` plus a link to `_meta/coverage-matrix.md` and the limitations in §3 above.
- Pin an issue titled **"Read this before trusting an `operational` label"** if you want the limitation visible at the top of the issue list; the README states it, but pins are read more often.

## 6. Post-publication gate

| Check | When | Why |
|-------|------|-----|
| CI green on `main` after merge | immediately | proves the merged tree, not just the branch, validates |
| `GALLERY.md` renders with working links on GitHub | within a day | relative links behave differently in the rendered view |
| `SECURITY.md` visible under the **Security** tab | within a day | GitHub only surfaces it once it is on the default branch |
| Community standards checklist | within a day | should show 5/5 once a licence exists |
| First external issue answered within a week | first week | the repository's own claims about evidence apply to its issue triage too |

---

**Verdict:** the repository content passes every automated gate and every manual check that was run, and both blocking decisions (licence, archive framing) are resolved as of 2.13.0. What remains in §5 is GitHub configuration, not repository risk.
