# Empirical evaluation 13 — the performance system, completed and then run on this repository

**Date:** 2026-10-22
**Prompts:** `PERF-P01` … `PERF-P07` (`02-engineering/performance/`)
**Target:** this repository's own gate suite, `python3 scripts/check_all.py`
**Evaluator:** the prompt's author (conflict of interest recorded: the author wrote
both the prompts and the tooling being measured)
**Status:** `TESTED — PASS` for the family, author-run. No independent run exists.

## 1. Why this family

`02-engineering/performance` was seven skeletons: a sequence with no evidence
rules, no verification, and no failure handling. It was also, unusually, a family
whose subject could be measured on the repository itself. Completing it and then
running it end to end produces two things at once — a usable procedure and a real
performance improvement with reproducible numbers.

## 2. What was executed

| Stage | Artifact | Gate outcome |
|-------|----------|--------------|
| P01 | goal: `check_all.py` wall clock, source: the contributor workflow | one measurable goal with a source |
| P02 | three-run median harness, per-gate breakdown | spread 9.7%, inside the 10% rule |
| P03 | time attribution across 15 gates | two gates owned 54% of gate time |
| P04 | ablation of the duplicate detector | confirmed, 0.84 s |
| P05 | two options, prediction written first | plan with a correctness test |
| P06 | both changes implemented and measured | suite green, 112 cases |
| P07 | stage log and gates | all six gates passed |

## 3. Measurements

Baseline, three runs of the whole suite:

| Run | Wall clock |
|-----|-----------:|
| 1 | 3.40 s |
| 2 | 3.34 s |
| 3 | 3.67 s |
| median | **3.40 s** |

Per-gate median over three runs (before the change): duplicate detector (shingle)
0.91 s, duplicate detector (combined) 0.83 s, prose lint 0.32 s, validator 0.27 s,
evidence report 0.20 s, and ten more below 0.15 s. Sum 3.20 s.

## 4. The bottleneck, demonstrated

`find_overlaps.py` loads the corpus, builds shingle, vocabulary and heading sets,
and scores **every pair on every metric on every run**. The gate list called it
twice, once per metric, so it built the same sets and walked the same 66,066 pairs
twice. An ablation — one process with both metrics — removed 0.84 s without
changing a single result.

Inside that single run, a component profile found the pair loop at 0.52 s of
0.80 s. Replacing 66,066 set intersections with one inverted-index pass over
171,325 postings brought it to 0.022 s. Correctness was checked against a direct
computation on 200 sampled pairs: zero mismatches.

## 5. Result

| | Before | After |
|---|---:|---:|
| Suite median | 3.40 s | **2.56 s** |
| Gate count | 15 | 14 |
| Detector cost in the suite | 1.74 s | 0.89 s |
| Self-test cases | 106 | 110 |

The improvement is **−25%**, measured on the same machine, same corpus, same
commit content, three runs each side. Every metric's text report and the `--json`
output were diffed against the pre-change version and are **byte-identical**, so
the optimisation changed speed and nothing else.

## 6. Prompt defects found and fixed

Both were found by running the stages, not by reading them.

1. **P02 had no soundness rule for the harness itself.** The first version of the
   prompt asked for three runs but never said what a spread of 9.7% means. The
   completed prompt states the 10% rule and requires the harness to be validated
   against a deliberately slower build — a benchmark that cannot detect a known
   regression measures nothing.
2. **P04 blurred "cost" and "contribution".** The skeleton asked for "estimated
   contribution" without a method, which invites reading a profile's slice size as
   a share. The completed prompt requires an ablation and defines the share as the
   difference between the run with the component and without it.

## 7. Limitations

- **Author-run, both sides.** The evaluator wrote the prompts and the tooling. This
  is the strongest available evidence here and the weakest kind.
- **One machine, one corpus.** 3.40 s → 2.56 s is reproducible on this checkout; it
  is not a claim about any other environment.
- **The first prediction was wrong.** Merging the two gates alone was predicted at
  0.9 s saved and delivered 0.26 s; the inverted index was what reached the
  target. Both numbers are recorded because a plan that is never wrong is a plan
  that was not written down.
- **P07's blocked-stage path was not exercised.** The run had no blocked stage, so
  the orchestrator's failure handling is untested.
