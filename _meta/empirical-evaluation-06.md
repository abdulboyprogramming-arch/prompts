# Empirical evaluation 06 — `CHAT-DESIGN` on a live decision in this repository

**Prompt:** `00-core/conversational/CHAT-DESIGN.md` (v1.0.0, operational)
**Date:** 2026-10-22 · **Method:** agent execution, one pass, agent-evaluated. No human operator supplied the constraints; they were read out of the repository, which is itself a finding (below).
**Evaluator:** the prompt's author. Conflict of interest recorded.

---

## 1. Inputs

```
DESIGN_QUESTION = should scripts/check_prompt_contract.py be merged into scripts/validate_library.py?
CONSTRAINTS     = one maintainer; GitHub Actions cannot run on this account (billing), so the local
                  command is the real gate; six documents reference both script names; both scripts
                  are imported directly by their self-test files
SCALE           = not applicable as traffic; as maintenance surface: 710 + 351 + 136 lines of tooling
TEAM_SIZE       = 1
DEADLINE        = none
EXISTING_STACK  = Python 3.12, no third-party dependencies, pytest not used (hand-rolled runners)
```

## 2. Measurements taken during the run

| Fact | Value | How |
|---|---|---|
| `validate_library.py` | 710 lines, 14 functions, median 0.25 s | `wc -l`, 3 runs timed |
| `check_prompt_contract.py` | 351 lines, 11 functions, median 0.10 s | same |
| `check_all.py` | 136 lines, 3.12 s (duplicate detectors dominate) | same |
| Shared code | contract imports `ROOT, Doc, is_archive, load` from the validator | `grep import` |
| Duplication | two function names collide (`check`, `main`); nothing else | AST-level name comparison |
| Documents naming the contract script | 6 | `grep -rl` |

**A repository defect found while measuring, not by the prompt:** the CI directory holds **two** workflows. `validate.yml` runs `check_all.py --verbose`; `validate-library.yml` re-lists twelve individual commands and does **not** run the composition gate. The release documentation claims "CI runs that script and nothing else". Two workflows mean a pull request can go green on the older one while the composition gate is red, and the duplication drifts on every gate change. Recorded separately as a repository defect (Medium), fixed after this batch.

## 3. The ADR produced

> **ADR-001 — Keep the composition gate in its own script**
> **Status:** accepted · 2026-10-22
>
> **Context.** Structure validation and composition validation are separate questions run by one command. They share a document loader. The maintainer is one person, and the local command is the only real gate because CI cannot run.
>
> **Decision.** Do not merge. `validate_library.py` owns structure, counts and links; `check_prompt_contract.py` owns dependency resolution, artifact ownership, cycles and the flow metric. Both are invoked by `check_all.py`.
>
> **Consequences.** Two scripts to keep consistent, and two places to add a check to. In exchange, a composition defect does not block a structural fix, the 19 contract fixtures keep a stable import path, and each script stays under 750 lines.
>
> **Alternatives rejected.** *Merge into one 1,061-line script* — breaks both self-test import paths and six document references, and makes the failure message ambiguous ("the validator failed" would mean either gate). *Extract a shared `promptlib.py`* — this is close to the current state already, since the contract script imports four helpers; the extraction would add a third file to save a four-name import, and it is cheap to do later if the shared surface grows. *One CLI with subcommands* — pure renaming; adds indirection without changing the maintenance surface.
>
> **Reopening condition.** Either script passing 900 lines, or a third script importing the shared loader, or the composition gate acquiring a second consumer.

## 4. Verification against the prompt's own table

| Check | Result |
|---|---|
| Question sharpened as a choice | yes — merge vs not, not "how should tooling be organised" |
| Constraints separated from preferences | partly — see finding 2 |
| Scale stated as numbers or labelled assumption | **no — see finding 3** |
| Two to four options including do-nothing | yes, four including do-nothing |
| Cost includes operation and maintenance | yes |
| Eliminations by constraint, not weights | yes |
| Leading option attacked, three reasons | yes (line growth, loader coupling, one-command habit) |
| Reversibility per option | yes |
| Six-section ADR, consequences honest | yes |
| Reopening condition | yes (three triggers) |
| Assumptions with a person who can confirm | **not applicable** — one person, who is the reader |

## 5. Findings about the prompt

| # | Severity | Finding |
|---|---|---|
| 1 | **Medium** | Step 4 requires "two to four real options, including do nothing", but nothing requires checking whether one of the options **is the current state**. During this run the option "extract a shared helper module" was drafted before the measurement showed the contract script already imports those helpers — the prompt would have produced an ADR recommending work that was already done, and nothing in it catches that. |
| 2 | **Low** | Step 2 requires constraints "as facts with an owner", and gives no rule for a constraint whose owner is unknown or is the reader. In a solo-maintainer decision the owner is always the person asking, which makes the column ceremonial. |
| 3 | **Medium** | The input set presumes a distributed-systems decision: `SCALE` is defined in §3 as "current and expected volume, with a number". For a decision about code structure or team process there is no volume, and the run had to reinterpret the field. The verification table then demands "scale stated: numbers or explicit assumption", which the run could only satisfy by redefining the word. |
| 4 | **Low** | The ADR's destination is never named. Step 8 says "an ADR the user can file", and for a repository decision "file" should mean a path — `docs/adr/`, `_meta/decisions/`. Every run will invent its own. |

## 6. Changes made

`CHAT-DESIGN` v1.1.0:

- Step 4: *"If the thing being decided already exists, one option must be the current state, described with the same costs as the others. An option list that omits the status quo will recommend work already done."*
- §3 `SCALE` redefined as **load**, with both senses named — traffic and volume for a service, size and rate of change for a codebase or process — and the verification row renamed to match.
- Step 8 names a destination rule: write the ADR to the repository's decision directory if one exists, otherwise state in the ADR where it will live.
- Step 2: a constraint whose owner is the reader is recorded as an assumption, not as an owner column entry.

## 7. Retest

Desktop re-run on a second real question — *"should the library's gates move from `check_all.py` into a `Makefile`?"* — with the revised text. The status-quo option was produced first and its cost (nothing to build, one more file to learn) sat beside the others, which changed the recommendation: the Makefile was rejected because it duplicates a working entry point rather than because it is worse. Finding 1's fix changed the output. Findings 2–4 changed only the formatting of the record.

## 8. Limitations

- One decision, chosen by the author, on a repository the author knows. The prompt's own failure mode — an enthusiastic architecture for a system the model cannot see — could not occur here, because the agent could see everything. That is the case the prompt was written for and the case this run does not test.
- "The user can file" was never exercised: no human filed the ADR, and nothing in this run shows that a human would.
- The defect the run found was in CI, not in the design question, which is a reminder that these prompts are better at provoking measurement than at producing prose.
