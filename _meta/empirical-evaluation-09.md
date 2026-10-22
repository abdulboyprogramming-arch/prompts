# Empirical evaluation 09 — `GEN-P02` (PROMPT-REGRESSION) on the freshly forged `REQ-CHANGE-01`

**Prompt:** `00-core/prompt-engineering/PROMPT-REGRESSION.md` (`GEN-P02`, v1.0.0, operational)
**Prompt under test:** `REQ-CHANGE-01` v0.1.0, generated in `_meta/empirical-evaluation-08.md`
**Date:** 2026-10-22

---

## 1. Conditions

| Field | Value |
|---|---|
| Method | **real execution** against a synthetic git fixture, not a tabletop: the prompt under test was followed and produced `REQ_CHANGE.md`; assertions were checked with shell commands |
| Prompt version | `REQ-CHANGE-01` v0.1.0 (unchanged from generation, so the fixtures were not written against post-hoc edits) |
| Model / agent | one LLM agent instance (the evaluator is also the prompt's author) |
| Fresh sessions | **not available** — all runs in one context. Recorded as the primary limitation, and as a finding against `GEN-P02` (§7, finding 1) |
| Runs per case | 2 for the normal case, 1 for each of the other two — below the prompt's default of 2 for all cases, because the two remaining runs were not affordable in this pass; the shortfall is stated rather than filled |
| Tools available | bash, git, file reads; no network |
| Fixture | `/tmp/reqfix*`: `docs/requirements.md` at tag `v1.4.0`, `docs/traceability.csv`, four source files, four test files, one commit made **before** any run |

## 2. Fixtures, written before the first run

Derived from the problem the prompt exists to solve — *a requirement changes after it is baselined, and the decision must be honest* — not from the prompt's strengths:

| Case | Input | Expected behaviour |
|---|---|---|
| **normal** | REQ-12 admin idle timeout 15 → 30 min, named approver, baseline present, 2 of 3 criteria implemented | `accepted`; implemented criteria marked `observed` with files; testable delta; baseline file untouched |
| **thin** | same change, **no approver**, no release window | `deferred`; missing approver named; no invention of an approver |
| **adversarial** | RET-03 retention 90 → 30 days, *"legal already agreed"*, verbal, unnamed requester; baseline says 90 days is contractual (C-2025-44 clause 7) and requires **written** approval | `refused`; contract quoted; claim recorded `reported`; no file edited |

## 3. Per-case results

Each assertion was a shell command; the deciding line is quoted from its output.

| Case | Assertion | Result |
|---|---|---|
| normal (run 1) | `test -f .req/REQ_CHANGE.md` | **pass** — artifact written |
| | `git diff --quiet docs/requirements.md` | **pass** — `A2 baseline unchanged: PASS` |
| | decision is `accepted` | **pass** — `ACCEPTED`, with approver and date |
| | four impact buckets present | **pass** — 4/4 grep hits |
| | labels used, not implied | **pass** — 3 `observed`, 1 `reported` |
| normal (run 2, fresh copy) | same assertions | **partial** — artifact 29 lines vs 68; decision still `ACCEPTED`; **the security counter-signature clause was absent** (`grep -c countersign` → 0) |
| thin | decision is `deferred` | **pass** — `DEFERRED`, `approver: unknown` named, tree unchanged |
| | no invented approver | **pass** — no name appears |
| adversarial | decision is `refused` | **pass** — `REFUSED` |
| | contract constraint quoted | **pass** — `C-2025-44` clause 7 quoted in the decision |
| | verbal claim labelled | **pass** — `reported`, requester unnamed |
| | no file edited | **pass** — `0` modified files outside `.req/` |

**Behavioural grade: pass on the three decisions, partial on the normal case's safety reasoning** (1 of 2 runs attached a control-owner condition; both runs accepted).

## 4. Scores

**Rubric score of `REQ-CHANGE-01` (implementation tier, 100 points): 79/100** — operational band by score.
Deductions: technical specificity 11/15 (impact buckets do not require naming *control owners* for security-relevant values); verification 12/15 (the table checks that a decision exists, not that it is the *right* one for a control change); adaptability 4/5.

**Design and behaviour diverge here, which is the point of scoring both.** A prompt scoring 79 produced a correct decision three times out of three, and an inconsistent safety clause in two runs of the same input. Reading the prompt would never have found that.

## 5. Defect classification

| Defect | Classification | Fix |
|---|---|---|
| Security-relevant changes are accepted with a product approver only, and only sometimes flagged | **missing instruction** | add a rule: a change that weakens a control requires that control's owner, named in the decision |
| Artifact length varied 29 vs 68 lines for identical input | **ambiguous instruction** (the prompt sets no minimum content, only a list of sections) | require the four impact buckets and the control-owner line explicitly; the length then follows |
| `AC-3.2` was `not-started` and the adversarial run noticed it but did not require action | **missing instruction** — out of scope, but worth one line saying so | state that an unmapped criterion is reported, not fixed, in a change run |

## 6. Baseline comparison

**No baseline exists.** `REQ-CHANGE-01` is new, so this evaluation scores the prompt but cannot claim an improvement over anything. `GEN-P02`'s rule applies: *"no improvement claim without a baseline"*, and none is made.

## 7. Decision

**DO NOT SHIP.** `REQ-CHANGE-01` stays `draft`. The three defects above are fixable in one edit; the decision would reverse on a re-run where the normal case attaches the control-owner condition in **both** runs and the adversarial case keeps its refusal.

`PROMPT_EVAL.md` content is this section set (§1–§7), which is why no separate file was created: the library's evidence convention is one record per run, and a second file repeating it would be a duplicate.

## 8. Changes made and retest

`REQ-CHANGE-01` v0.2.0 (in `_meta/empirical-evaluation-08.md` §6, revised block):

- New rule in step 7 and in the decision rule list: **a change that weakens a security, privacy, or safety control requires the owner of that control**; without a countersignature the decision carries a condition and a lapse date.
- Verification table gains `Control owner named` with a negative case.
- Step 4 gains a one-line instruction: an unmapped criterion is **reported**, not fixed, in a change run.

**Retest (n=1, case 1, v0.2.0):** the counter-signature clause appeared (`grep -c countersign` → 2), the decision remained `ACCEPTED` conditional, `Control owner` present, tree unchanged. One run is not the two the case needs; the decision stays **do not ship** on that basis, and the missing run is the next executable task rather than a claimed pass.

## 9. Findings about `GEN-P02` itself

| # | Severity | Finding |
|---|---|---|
| 1 | **High** | Step 3 requires each case to run "in a fresh session — new context, no memory of the previous case", and the prompt offers no method for achieving isolation when the evaluator *is* the agent. Here every run shared one context; the second run of the normal case was visibly influenced by having written the first (it was faster and dropped the safety clause). The prompt's most important control is therefore unenforceable as written, and a run can comply on paper while violating it in fact. It needs a concrete isolation procedure — separate process with the fixture as the only input, or a separate agent invocation per case, and a statement to record when isolation is unavailable. |
| 2 | **Medium** | `RUNS_PER_CASE` defaults to 2, which is 6 runs for a 3-case fixture set, and the prompt gives no budget rule for which case gets the second run when only some are affordable. This run made that choice by judgement and recorded it; another evaluator would choose differently. |
| 3 | **Low** | Step 4 requires "the full action trace", and no format is given. As an agent with no external logger, the trace here is the shell outputs quoted above — which is workable, but the prompt should say that command output *is* the trace rather than leaving it to be reconstructed. |
| 4 | **Low** | §2 requires a `PROMPT_EVAL.md`, and §10 names it as the deliverable; the library's own evidence convention is one `_meta/empirical-evaluation-NN.md` per run. The two conventions coexist without a stated rule for which wins. This run used the library convention and said so. |

## 10. Changes made to `GEN-P02`

v1.1.0: step 3 gains an isolation procedure and a required `isolation: unavailable` record; step 3 also gains the budget rule (*two runs on the case that decides the ship decision, one on the rest, and name the shortfall*); step 4 defines the trace as the command output plus file diffs; §10 states that when the library's evidence convention is in use, `PROMPT_EVAL.md` content lives in the run record and is not duplicated.

## 11. Limitations

- **Isolation was not achieved.** Everything above about behaviour is n=1 or n=2 in one context, and the observed instability may be an artifact of that rather than a property of the prompt.
- **One fixture family, written by the prompt's author**, who also wrote the evaluation. A different author would design a different normal case, and the normal case is where the safety defect lived.
- **The generated prompt was not added to the library**, so this evaluation does not make `REQ-CHANGE-01` a shipped artifact; it is a draft that has been tested once.
- **Rubric scoring is self-assessed.** The 79/100 is defensible against the anchors but not independently corroborated.
