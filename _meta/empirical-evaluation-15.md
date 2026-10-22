# Empirical evaluation 15 — `MLA-P03` run against a leakage trap it had to find

**Date:** 2026-10-22
**Prompt:** `MLA-P03` Data Assessment, `03-domains/data-ml-ai/`
**Target:** the committed churn fixture [`_meta/fixtures/ml-churn/`](fixtures/ml-churn/README.md)
(1,200 rows, 18 monthly cohorts, three planted leakage paths, one random-split defect)
**Evaluator:** the prompt's author (conflict of interest recorded)
**Status:** v1.0.0 `TESTED — FAIL`; v1.1.0 `TESTED — PASS` on the same fixture.

## 1. Why a fixture, and why this one

The completed `data-ml-ai` family had never been run. `MLA-P03` is the stage that
decides whether a model will be trained on the answer, so it is the one worth testing
first, and it can be tested objectively: the fixture contains **known** leaks, so the
question is not "does the output read well" but "did the procedure find them".

The fixture: 1,200 account-months, churn rate 32.25%, with

1. `cancel_reason` — populated only for churned accounts (structural leak),
2. `status` — a function of the label (structural leak),
3. `last_login_days` — innocently named, measured **after** the outcome window, and
   perfectly separating by threshold (≥31 ⇒ churned),
4. `train.py` — random shuffle split over time-ordered data.

Traps 1 and 2 give themselves away by name. Trap 3 does not, and that is the point:
it is the leak that ships.

## 2. Run 1 — v1.0.0, and what it missed

Following §4.2 as written — "build the leakage register **before profiling features** …
add what the schema reveals" — the artifact recorded traps 1, 2 and 4 and **missed
trap 3**. The procedure is schema-first and no step asks for a statistical scan, so an
executor who follows it faithfully cannot find a column whose name is innocent and
whose statistics are perfect.

The cost is not theoretical. With `last_login_days` in the feature frame the offline
recall is near 1.0, the model looks like a breakthrough, and it fails on every real
account because the value does not exist at prediction time. Measured on the fixture:

```
max(last_login_days | churned=0) = 30
min(last_login_days | churned=1) = 31
```

A two-line check finds it. Nothing in v1.0.0 asked for it.

Second defect, found while writing the artifact: **verification item 2 cannot be
honestly satisfied without a pipeline.** "Every register entry names its prevention and
the check that proves it" — but in a project whose training code has not been written
yet, there is nowhere for the check to live, so the executor either writes a check that
does not exist or leaves the row blank. The first is a false claim, the second fails the
gate. Measured against the fixture, all four mitigations were **specified but not
implemented**, and v1.0.0 had no vocabulary for that state.

| # | Sev | Defect |
|---|-----|--------|
| 1 | **High** | The register is built from the schema alone, so a statistically perfect but structurally innocent column is never found |
| 2 | **High** | A check with no pipeline to hold it has no honest state; the artifact reads as "prevented" when nothing prevents it |

## 3. The fixes, in v1.1.0

- **§2a, a label-determinism scan over every column**, with the method written out:
  categorical levels at 0% or 100% with ≥30 rows; numeric columns by threshold
  separation rather than by a single pure value, because one of 30 values will be pure
  by chance. The scan's per-column result goes in the artifact, including for columns
  that pass.
- **`pending — no pipeline yet`** as an explicit register state, with the assertion
  `MLA-P05` must implement written out. The register may not call such an entry
  prevented.
- A new failure path: a perfectly separating column with no owner and no known meaning
  is a leak by default; the owner has to prove it is measured before prediction time.

## 4. Run 2 — v1.1.0, same fixture

| Check | Run 1 | Run 2 |
|---|---|---|
| Finds `cancel_reason` | yes | yes |
| Finds `status` | yes | yes |
| Finds `last_login_days` | **no** | **yes**, via the threshold scan |
| Finds the random split | yes | yes |
| Honest state for an unimplemented check | **no vocabulary** | `pending — no pipeline yet`, four entries |
| Determinism result recorded per column | n/a | 8 of 8 |

Run 2 found all four defects and labelled every mitigation as pending rather than
prevented. The added step cost about ten minutes and one table.

## 5. What this says about the family

`MLA-P03` is one stage of eight. The other seven remain unexecuted, so the system is
`PARTIALLY TESTED` end to end, and the register now proves something narrower and more
useful: the stage that decides whether a model is trained on the answer can find a leak
that was designed to be hard to find.

## 6. Limitations

- **The fixture was built by the same author who wrote the prompt**, who knew where the
  traps were. The mitigation is that the *procedure*, not the author's knowledge, is
  what is being tested: run 1 followed the text and missed trap 3; run 2 followed the
  new text and found it. That is evidence about the text, but it is not an independent
  test.
- **One fixture, one domain.** A time-series or text corpus would exercise different
  leakage paths, and `pending — no pipeline yet` was never tested against a project
  that does have a pipeline.
- **The artifact was written by hand while following the prompt**, which is closer to a
  careful desk run than to an unaided model execution.
- **The fixture is now committed**, at [`_meta/fixtures/ml-churn/`](fixtures/ml-churn/README.md),
  with a fixed seed and a byte-identical regeneration check, so the run can be repeated
  by someone else. That closes the reproducibility gap this evaluation first opened with;
  it does not close the independence gap, because the author still built the traps.
