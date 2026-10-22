<!-- not-a-prompt -->
# Current Test State — measured, not assumed

**Produced by:** `QA-P02` v1.1.0 (`.qa/` artifact)
**Target:** this repository at `b1cbc9a` (main, 2.28.0), assessed locally on 2026-10-22
**Evaluator:** the author of the prompts — an author-run assessment, not an independent one
**Risk map:** [`QA_CONTEXT.md`](QA_CONTEXT.md), behaviours B1–B10

---

## 1. Inventory

| Level | What exists | Count |
|---|---|---|
| Unit (fixture-driven) | seven hand-rolled case lists over the validators' pure functions | **7 files, 119 cases** |
| Gate (integration of the real tree) | `scripts/check_all.py` runs 15 gates against the working tree | **15 gates** |
| Contract | `scripts/check_prompt_contract.py` — dependency graph, artefact flow, cycles | 1 gate, 19 cases |
| End-to-end | none. No run applies a prompt to a real project inside the suite | 0 |
| Manual | the empirical evaluations in `_meta/empirical-evaluation-*.md` | 15 records, 26 prompts |

Test-to-source ratio: 1,217 lines of tests against 3,215 lines of tooling — 0.38. There is
no test directory excluded from CI; the workflow runs `check_all.py`, which runs all 15
gates and all seven test files.

| File | Cases | Lines |
|---|---:|---:|
| `scripts/test_validator.py` | 27 | 368 |
| `scripts/test_contract.py` | 19 | 247 |
| `scripts/test_evidence_report.py` | 17 | 132 |
| `scripts/test_task_index.py` | 17 | 107 |
| `scripts/test_overlaps.py` | 17 | 156 |
| `scripts/test_prose_lint.py` | 12 | 68 |
| `scripts/test_check_all.py` | 10 | 139 |

## 2. Suite run

| Command | Wall clock | Result |
|---|---|---|
| `python3 scripts/check_all.py` | **3.04 s** | 15/15 gates pass, 119/119 cases pass |
| `python3 scripts/validate_library.py` | 0.25 s | 0 errors, 0 warnings — 476 files, 364 prompts |
| seven `scripts/test_*.py` | 0.29 s total | 119/119 |
| re-run of `check_all.py` | 3.11 s | identical result |

Reproducible across two runs; no failures on the target commit. The suite is fast — far
inside the 10-minute target — and that is a real property, not an estimate.

**A finding from running it:** adding `.qa/` artefacts to this repository fails five gates
— two file-total claims (476 → 478) and two artefacts the validator does not recognise.
The validator's message names the escape hatch (`<!-- not-a-prompt -->`), which these files
now carry, and the totals were updated. This is correct behaviour, but it means **the QA
system cannot be run against this repository without editing it**, which is worth knowing
before the next engagement.

## 3. R1 coverage map

`covered` requires a demonstration. Each row below was tested by a deliberate mutation in
a throwaway copy of the tree (`/tmp/qa-mut`), not by reading the code. The mutation column
is what the gate actually did.

| # | Behaviour | Class | Evidence | Mutation result |
|---|---|---|---|---|
| B1 | maturity matches content | **covered** | `test_validator.py:119` `maturity-claim over skeletons is an error`; `:112` status-claim; `:128` prose claim | relabelled a skeleton `operational` → **ERROR**: *"'operational' prompt lacks a verification section"* |
| B2 | counts match the tree | **covered** | `test_validator.py:188` stale triplet; `:220` bare "N prompts carry that label"; `:242` stale file total; `:159` README row | changed 281 → 275 → **ERROR**: *"says 275 operational … but the tree has 281"* |
| B3 | links resolve | **covered** (mutation only) | no fixture test; `validate_library.py:328` | added a markdown link to `no-such-file.md` → **ERROR**: *"broken relative link"* |
| B4 | dependency graph composes | **covered** | `test_contract.py:154` missing dependency, `:189` cycle, `:204`-`:229` citation rules | 19/19 pass; mutation not needed |
| B5 | evidence registry is the source | **covered** | `test_evidence_report.py:76`–`:103`, including the exemption list | 17/17 pass |
| B6 | risk-A never invites a destructive action | **covered — after the fix below** | `validate_library.check_risk_class`, five fixtures in `test_validator.py` | first run: **WARNING only**, exit 0, `check_all` printed **"All gates passed"**; retest after 2.28.1: **ERROR**, validator exit 1, `check_all` exit 1 |
| B7 | generated files current | **covered** | `test_check_all.py:88`–`:112` (stale catalog, restore-on-failure); gate `catalog current` | 10/10 pass |
| B8 | declared inputs match placeholders | **covered** (mutation only) | no fixture test; `validate_library.py:156` | added `{{NOT_DECLARED_ANYWHERE}}` → **ERROR** |
| B9 | prose lint | **covered** | `test_prose_lint.py`, 12 cases | 12/12 pass |
| B10 | duplicate identifiers | **covered** (mutation only) | no fixture test; validator duplicate check | changed `FE-P03` to `FE-P02` → **ERROR**: *"duplicate identifier 'FE-P02'"* |

**Four R1 behaviours (B1, B2, B5, B6). Three were covered. B6 was the failure — and it
is now fixed, retested, and covered.**

### B6 in full, because it is the finding

A prompt declaring `Risk class: A` tells an agent the work is read-only. If that prompt
also says "deploy the change to production", the agent has been given a licence to act.
The validator has known about this since the risk-class rules were written and reports it
as a **warning**, so `check_all.py` — the single gate every contributor and CI runs —
passes. The library's own rule, written into its QA system, is that a test which cannot
fail is not a test; by the same logic a check that cannot fail a build is not a control.

No prompt currently trips it (0 warnings on the real tree), so promoting it to an error was
a safe change today. Leaving it a warning would have meant the first prompt that does trip
it ships.

**Fixed in 2.28.1.** The rule moved into `check_risk_class()` and appends to `errors`
rather than `warnings`; five fixtures pin it (error on an unnegated destructive verb, no
error under class B, no error when the sentence forbids the action, no error with no verb,
and a message that tells the author how to resolve it). Retest, in the same throwaway
copy: validator **exit 1**, `check_all` **exit 1**. On the real tree, 0 errors and 0
warnings — the rule blocks the contradiction without blocking anything that exists.

## 4. Quality sample — five tests, asked whether they could fail

| Test | Level | Would it fail if the implementation were subtly wrong? |
|---|---|---|
| `test_validator.py:227` "a stale triplet is reported once, not twice" | unit | **Yes.** Asserts `len(errors) == 1`, so a duplicate-reporting bug fails it. It was added after exactly that bug. |
| `test_contract.py:229` "a substring of an unrelated word is not a citation" | unit | **Yes.** False-positive citation detection is the thing that would weaken the composition report silently. |
| `test_evidence_report.py:95` "a zeroth count is skipped" + `:96` "a stale non-zero count on a similar line is still reported" | unit | **Yes**, and the pair is the point: the exemption is tested on both sides. |
| `test_check_all.py:89` "a failing validator leaves the catalog unchanged" | unit | **Yes.** This asserts a file-system side effect, not a return value — it caught the catalog being rewritten on a failed run (`a6d849a`). |
| `test_task_index.py` "build returns the unrouted list rather than hiding it" | unit | **Weak on reading, adequate on test.** It asserts `build()` does not raise, so it proves the function returns; the name reads as though it proves the opposite. A reader scanning failures would misread it. |

No assertion-free tests, no snapshot-only assertions, no test asserting a mock. The
weakness is naming, not rigour.

## 5. Reliability signals

| Signal | Result |
|---|---|
| `sleep` in tests | **none** |
| network calls in unit tests | **none** |
| random / time-dependent assertions | **none** (dates are injected in the fixtures that need them) |
| `skip` / `xfail` / `|| true` | **none**; the one "skip" in `test_evidence_report.py` is a product rule (zero counts), tested on both sides |
| ordering dependencies | **none found**; each file is independent and passes in isolation |
| shared global state | temp directories per case, cleaned up |
| flaky results | none in two consecutive runs |

## 6. Feedback latency against the target

| Measurement | Value | Target |
|---|---|---|
| Full suite, local | 3.04 s | 10 min |
| Unit tests only | 0.29 s | — |
| PR pipeline | **never measured — it has never run** | 10 min |

## 7. CI enforcement

`.github/workflows/validate.yml` exists, runs on push and pull request to `main`, and calls
`check_all.py`. It is correctly written and correctly scoped.

**It has never executed a step.** Every run recorded by the API — including this cycle's —
reports `conclusion=failure` with `steps: 0`, which is a startup failure before the runner
is allocated. The cause is account billing, not the workflow.

Consequence for this assessment: **no change to this repository has ever been blocked by a
remote check.** Every gate is a local command somebody has to remember. That is why B2, the
count-integrity behaviour, has failed three times: the only enforcement is a human running
the gate before pushing.

## 8. Coverage reality

`no instrumentation` — no coverage tool is installed or configured, and no line-coverage
figure is claimed anywhere in this repository. Nothing here should be read as a percentage.

What can be said without instrumentation: every one of the 15 gates has at least one test
that exercises its failure path, except the four noted in §3 (`B3`, `B6`, `B8`, `B10` have
no fixture test; three of those were confirmed by mutation and one — B6 — does not fail a
build at all).

## 9. Coverage limits of this assessment

- **Author-run.** The person who wrote the prompts wrote this assessment, and designed the
  mutations. It shows the machinery works as described; it does not show that an outside
  reader would find the same.
- **The mutation copy is not the live tree.** Mutations were applied in `/tmp/qa-mut`, a
  full copy, and reverted; the live tree was never put into a failing state.
- **No end-to-end level exists to test.** Nothing here exercises a prompt against a real
  project inside the suite; that lives in the 15 evaluation records and is why the executed
  ratio stays the library's weakest number.
- **CI is unverified as a control.** This assessment can say the workflow file is correct
  and that it has never run. It cannot say the pipeline would pass.
