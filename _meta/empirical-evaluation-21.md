<!-- not-a-prompt -->

# Empirical Evaluation 21 — a skeleton that describes a system, replaced by a procedure that tests one

**Date:** 2026-10-23
**Prompt:** `ONBOARD-01` (Codebase Onboarding) v0.1.0 → v1.0.0
**System:** `05-scenarios/onboarding` — promoted from skeleton this cycle
**Evaluator:** the author of the prompt (conflict of interest recorded)
**Method:** both versions run as written against a committed fixture, with the start, the change and the
revert actually executed rather than described.

---

## 1. Why this prompt

The prompt's own gallery line was: *"Join an unfamiliar codebase and need to become useful quickly:
entry points, build, data flow, where the traps are."* It was a 55-line skeleton, and it is the prompt the
commonest handover of 2026 asks for: a founder, analyst or designer built a working product with an AI
assistant, cannot describe the code, and is handing it to a developer who works by hand.

Three systems touch that situation and none of them was it. `04-process/handover/` (5 stages, operational)
assumes a sender who knows the system and can answer questions; it even names the *agent → human* type,
where "state exists only in artifacts, some stale". `02-engineering/project-recovery/` (7 stages,
operational) assumes the project is **broken** rather than merely unknown. `04-process/documentation/`
(8 stages, operational) writes documents about a system someone already understands. The gap is the case
where the system works, the sender is present, and the sender cannot answer.

## 2. The fixture

`_meta/fixtures/takeover-scenario/` — six Python files, a schema, a Dockerfile, no tests, no README, and
a `docs/notes.txt` of the builder's scraps. Every trap is planted with a command beside it in
`REQUEST.md`, and the grading table (nine requirements) was written before either version was run.
Both prompt outputs are stored verbatim beside it: `runs/v0.1.0-output.md` and `runs/v1.0.0-output.md`.

| Trap | How it is planted |
|---|---|
| Two required environment variables, documented nowhere | `config.py` raises `ConfigError` naming each in turn |
| A payment key as a module constant | `PAYMENTS_KEY = "sk_test_EXAMPLE_REPLACE_ME"` with a TODO above it |
| **Schema disagrees with the models** | `models.py` has `Report.user_id`; `schema.sql` creates `reports` without it, and the route queries that column |
| A Dockerfile that cannot run | `CMD python app/main.py` against package-relative imports |
| Personal data with no deletion path | `users.email`, no delete anywhere |
| AI-shaped authorship | `_fmt_date` twice with different formats; a commented-out second `export`; `requests` declared and never imported |
| No tests | nothing matching `test*` |

## 3. Run 1 — v0.1.0: **0 of 9**

The skeleton's six instructions — big picture, structure, important code, workflow, risks, brief — produce
a competent **description** of a codebase. That is what it produced: a clean brief naming the entry point,
the two blueprints, the data objects, the inline SQL, and a risk list that included "no tests" and
"`PAYMENTS_KEY` is defined in `config.py` as a placeholder string".

| # | Criterion | v0.1.0 | Why |
|---|---|---|---|
| 1 | Start procedure that works from a clean checkout, both variables named | **FAIL** | the right command appears, and both variables are named — in a different section, with no sequence. Followed in order, the first attempt exits with `ConfigError` |
| 2 | Hardcoded key reported as a finding | **FAIL** | a bullet in "risks": no consequence, no action, no statement that a placeholder in a once-public repository is one commit from live |
| 3 | Schema/model mismatch identified | **FAIL** | it says to read `models.py` and `schema.sql` "side by side" — and never notices `reports` has no `user_id` |
| 4 | Dockerfile defect identified | **FAIL** | "the Dockerfile exists but has not been verified" — which is an absence of work, not a finding |
| 5 | Absence of tests stated **with the three riskiest paths** | **FAIL** | states "no tests"; names no path and no blast radius |
| 6 | Data-flow map with where personal data lands | **FAIL** | never mentions that email addresses are stored |
| 7 | Authorship section | **FAIL** | not a step in the skeleton |
| 8 | One change with a rollback, performed | **FAIL** | "first useful tasks" proposes a test suite and a data-access refactor — neither is a safe first change, neither has a rollback |
| 9 | Verdict | **FAIL** | never asked |

**The diagnosis:** the skeleton describes; it never executes. Everything that mattered in this repository
— does it start, does the schema match the model, does the container run, where does personal data land —
is a **claim that needs a command**, and the procedure had no step that ran anything. A description written
by reading is exactly as reliable as the reader's guess about which of two contradicting files is right,
and here there are two of those.

## 4. Run 2 — v1.0.0: **9 of 9**

The rewrite changes the product from a description to a **verdict with evidence**:

1. **Step 2 executes the start procedure** and makes every guessed step a finding. Result: F1 (two
   variables, no documentation) and F2 (`python -m app.main` from the root; `python app/main.py` raises
   `ImportError: attempted relative import with no known parent package`).
2. **Step 4 reconciles objects against the schema.** `grep -n user_id app/schema.sql` prints nothing —
   and the prompt's own rule, *an absence is the finding*, is what turns that empty output into F4.
3. **Step 5 tries the deployment artifact.** `CMD python app/main.py` plus the import error above gives
   F5: the image builds and cannot start.
4. **Step 6 classifies secrets.** F6: `PAYMENTS_KEY` is a module constant, not an environment read, so the
   fix is a code change rather than a settings change.
5. **Step 7 maps personal data** — collected, stored, readable-by, retention, deletion — producing F7:
   emails stored, nothing deletes them.
6. **Step 8 reads the authorship** and turns it into guidance: two `_fmt_date` implementations with
   different formats, an abandoned `export`, and a declared-but-unused `requests` — which is what the
   sender's note *"the export needs a library"* was about.
7. **Step 9 ranks the untested surface by blast radius**: `/reports/<user_id>` first, because it is
   personal data behind **no authentication at all** (F8), then export, then the payment path.
8. **Step 10 makes and reverts a change** in a copy: `/health` returns a version, the server shows it,
   the file is restored, the server shows the original.
9. **Step 11 issues the verdict**: *continue with conditions*, with seven numbered conditions (C1–C7),
   each tied to a finding and to what clears it.

Run 2 found **eight findings** where run 1 found a shape, including the one that decides the first week of
work: `GET /reports/<user_id>` takes the user id from the URL and there is no authentication, so anyone
who reaches the service reads anyone's reports by changing a number.

## 5. What this evaluation does not show

- **Six files is not six hundred.** The fixture is small enough to read completely, so the "cut in this
  order" rule in §7 of the prompt — follow the money and the personal data first — was never needed. That
  path is argued, not exercised.
- **The environment was manufactured.** The run installed `flask==3.0.3` into a throwaway virtualenv to
  execute the start procedure. That is a real execution, not a simulated one, but it is not the receiver's
  environment: no database was available, so every query path ended in a 500 and the schema reconciliation
  was done by reading `schema.sql`, not by inspecting a live database.
- **One desk execution, author-run.** Same limitation as every record in this library: the author wrote the
  prompt, the fixture and the grading table.
- **The verdict is a judgement.** The prompt's rules make the *findings* checkable; whether C1 and C2 are
  enough to justify "continue" is the author's product opinion.
- **No downstream run.** Nothing here shows that `04-process/handover/` (`HAND-P04`) is easier after this
  prompt's output — the handoff is asserted, not measured.

## 6. Status

| Prompt | Before | After |
|---|---|---|
| `ONBOARD-01` | v0.1.0, skeleton, 55 lines, `NOT TESTED` | **v1.0.0, operational, `TESTED — PASS`** (0 of 9 → 9 of 9) |

The library's skeleton count falls from 74 to 73. `05-scenarios/legacy-code/WORKING-WITH-LEGACY.md`
(`LEGACY-01`) remains a skeleton and is the nearest neighbour: it covers a codebase that is hostile, which
is a different problem from one that is merely unexplained.
