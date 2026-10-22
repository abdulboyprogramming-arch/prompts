# Empirical Evaluation 18 — an intake that believed the user instead of the repository

**Date:** 2026-10-22
**Prompts:** `INT-P01` Project Intake Context Collector, v0.1.0 (`TESTED — FAIL`) → v1.1.0 (`TESTED — PASS`)
**System:** `06-interactive`, the first run of this system
**Target:** this repository, driven by the frozen request in
[`_meta/fixtures/intake-scenario/REQUEST.md`](fixtures/intake-scenario/REQUEST.md)
**Evaluator:** the author of the prompt (conflict of interest recorded)
**Method:** desk run against a committed fixture; every factual claim in the produced brief checked
against the tree.

---

## 1. Why this prompt, and why a fixture

`06-interactive` is the smallest system in the library and the only one in which **nothing** has ever
been executed: four prompts, all `skeleton`, and a README that lists four known gaps before promotion.
It is also the system every other system depends on — if intake hands downstream work a wrong fact,
no later stage can recover, because no later stage re-checks it.

It is runnable in a way that can be graded: the input is fixed, and every claim the brief makes about
the repository is checkable. That is the same property that made `CHAT-SELECT` the library's one run
with outside ground truth — except here the ground truth is the tree itself.

The fixture request is a plausible contributor message about adding a data-contracts family, and it
contains, deliberately:

- **two false statements** — "we're on Python 3.8 for CI" and "there's no CI configured in this repo
  yet" — where the workflow file exists and pins 3.12;
- **one question the repository already answers** — whether the family belongs under `03-domains/`
  or `04-process/`;
- **one preference masquerading as a design decision** — "five stages? eight? Whatever fits."

## 2. Run 1 — v0.1.0, and what it produced

Executed as the reading sequence says these prompts are used: the prompt text plus the user's message,
interactively. v0.1.0 contains no discovery step — its instruction is to "collect (or infer with
explicit assumptions)" the five categories — so the run produced a brief assembled from the message
and plausible defaults.

What that brief said, verbatim in substance:

| Section | Content it produced | Problem |
|---|---|---|
| Known facts | "Python 3.8 in CI" · "no CI configured" · "repo uses prompt files in numbered folders" | the first two are false; the third was inferred, not read |
| Assumptions | "5 stages" · "03-domains, probably" · "standard autonomy" | no confirmation status, no basis, no falsifier |
| Open questions | stack? · which folder? · how many stages? · who reviews? | the first three are answerable from the tree |
| Recommendation | "start with a data-contracts system of about five stages" | a stage count taken from a preference |

### Graded against the fixture's five criteria

| # | Criterion | v0.1.0 |
|---|---|---|
| 1 | Contradicts the message where the tree contradicts it | **FAIL** — both false statements became facts |
| 2 | Asks nothing the repository answers | **FAIL** — three of four questions were answered by `ls`, `_meta/taxonomy.md`, and a system README |
| 3 | Assumptions carry confirmation status | **FAIL** — a list with no basis, no owner, no falsifier |
| 4 | Facts cite a command or file | **FAIL** — zero sources |
| 5 | Stage count follows the lifecycle, not preference | **FAIL** — adopted "five" |

**5 of 5 failed.** The failure is not stylistic. If this brief is handed to a builder, the builder
inherits a CI assumption that will break the first workflow it writes, and a stage count that nothing
in the library supports.

## 3. The diagnosis, and why it is not "add more questions"

The obvious fix is to ask the user about the stack and the CI. That is the wrong repair: the
repository answers both, and asking a contributor what their own CI runs is how an intake becomes an
interrogation that the system's README already prohibits — "**ask only what the repository cannot
answer**".

The real defect is ordering. v0.1.0 starts with the user and never reaches the tree, so every
statement in the message becomes an input rather than a claim. The repair is to make discovery the
first step, make the message a set of **claims to check**, and make a disagreement between the two a
first-class output rather than something to resolve silently.

## 4. The change — v1.0.0, promoted to v1.1.0 after retest

Six additions, each traceable to a failed criterion:

| Criterion it fixes | What v1.1.0 requires |
|---|---|
| 4 (sources) | §4.1 "read before asking" names the files; §5 requires a source column per fact |
| 1 (contradictions) | §4.3 checks every user statement against the fact table and puts disagreements in §2 of the brief — "never average the two" |
| 2 (no answerable questions) | §4.4 restricts questions to the residue, each with a default |
| 3 (assumptions) | §5 §3 of the brief: basis, confirmer, falsifier; at most five put to the user |
| 5 (stage count) | §7 failure handling: the count follows the lifecycle; the user cuts scope instead |
| — (verification) | §6 seven checks, including "brief is usable cold" and "no secrets" |

Two sections were added that a skeleton cannot have: **§6 Verification** and **§7 Failure handling**,
plus completion criteria — which is what the maturity label `operational` means in this library.

## 5. Run 2 — v1.1.0 on the same fixture

Same request, same target, same executor. Discovery ran first (`ls`, `README.md`,
`.github/workflows/validate.yml`, `_meta/taxonomy.md`, `PROJECT-STATUS.md`, a `03-domains` system
README), and then:

| # | Criterion | v1.1.0 | Evidence |
|---|---|---|---|
| 1 | Contradictions surfaced | **PASS** | both appear in §2 of the brief: "Python 3.8" vs `python-version: "3.12"` in `.github/workflows/validate.yml`; "no CI" vs the existence of that file, which also enforces a clean regeneration |
| 2 | No answerable questions | **PASS** | four questions asked, none about stack, CI, test command, layout, taxonomy or count — each has a default and each is about intent or authority |
| 3 | Assumptions bounded | **PASS** | five assumptions, each with basis and falsifier; two escalated to the user, three kept unconfirmed and labelled risk |
| 4 | Facts sourced | **PASS** | 11 facts, 11 sources, each a command or a file path |
| 5 | Count from lifecycle | **PASS** | the brief proposes the data-contract lifecycle (contract definition → compatibility policy → registry/versioning → producer change → consumer migration → verification) and states that stage count is 6 because of those gates, not preference |

It also produced something v0.1.0 never could: a **first action** rather than a summary — resolve the
CI contradiction before any prompt is written, because it changes which verification gates the new
family can rely on.

## 6. What this run does not show

- **One executor, one fixture, one prompt.** The other three `06-interactive` prompts are still
  skeletons and unrun; `SYSTEM-SELECTOR`'s known gap (it predates the 2.x systems) is untouched.
- **The brief is graded, not measured in use.** Nothing here shows whether a downstream stage that
  consumes this brief produces better work — that would need the composition test this library still
  lacks.
- **Desk run.** The contributor did not exist; the request is a fixture written by the prompt's
  author. A real user may answer a contradictory question in ways this run cannot foresee.
- **No independent review.** Author-run, as with every other record in `_meta/evidence.json`.

## 7. Status

| Version | Status | Date |
|---|---|---|
| `INT-P01` v0.1.0 | `TESTED — FAIL` (5 of 5 criteria) | 2026-10-22 |
| `INT-P01` v1.1.0 | `TESTED — PASS` (5 of 5 criteria) | 2026-10-22 |
