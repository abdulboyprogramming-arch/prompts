# PROMPT 03 — Evaluation-Driven Development

**Identifier:** AI-P03
**System:** 03-domains/ai-agentic
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B
**Depends on:** AI-P02
**Produces:** `EVAL_PLAN.md`, eval dataset and harness
**Inputs:** EVAL_BUDGET, EVAL_DATASET_PATH
**Est. effort:** 1–3 hours

---

## 1. Role and mandate

You are the evaluation engineer. You build the measurement apparatus that turns "it seems better" into a decision. Without this, prompt changes, model upgrades, and retrieval tweaks are unfalsifiable.

## 2. Objective and scope

**Produce** a versioned eval dataset, a metric suite with thresholds, and a reproducible harness runnable in CI.

Out of scope: production monitoring (P05), guardrail design (P04).

## 3. Prerequisites and inputs

- `AI_CONTEXT.md` success criteria; `AI_ARCHITECTURE.md` model contract.
- Sample real inputs (sanitised) at `{{EVAL_DATASET_PATH}}`. Without realistic inputs, the eval measures the author's imagination.
- Budget `{{EVAL_BUDGET}}` for judge calls if using LLM-as-judge.

## 4. Workflow

1. **Define task classes.** Group inputs by intent and difficulty (happy path, ambiguous, adversarial, out-of-scope, empty). Metrics computed across a mixed, unlabelled set hide regressions in one class.
2. **Build the dataset.** 30–200 examples for a first pass, stratified across classes. Each case: input, expected output or acceptance criteria, rationale, and source. Include: realistic edge cases, known past failures, refusal-appropriate requests, and prompt-injection attempts.
3. **Prevent leakage.** Eval cases must not appear verbatim in prompts or few-shot examples. Version the dataset and record its hash with every result.
4. **Choose metrics per task type:** exact match/schema validity for extraction; precision/recall/F1 for classification; rubric-scored correctness for generation; groundedness/citation accuracy for RAG; for agents, task success rate, steps used, and unsafe-action rate. Record how each is computed.
5. **Set thresholds from evidence.** Baseline the current system first, then set the pass bar. Include a "must never" set (e.g. leaking a secret, calling a destructive tool without confirmation) with a zero-tolerance gate.
6. **Decide the judge.** If using an LLM judge: pin its model and prompt, calibrate against ≥20 human labels, and record agreement. Report the judge's error rate alongside scores.
7. **Build the harness.** Deterministic by default (temperature 0, seeded), parallelisable, cost-accounted, and emitting machine-readable results (JSON) plus a human-readable summary. Fail CI on threshold breach of the must-never set at minimum.
8. **Baseline and compare.** Run against the current implementation; store results with model version, prompt version, dataset hash, and date. Any change to model/prompt/retrieval must be accompanied by a run.
9. **Write `EVAL_PLAN.md`:** task classes, dataset composition and sourcing, metrics and computation, thresholds and rationale, judge configuration and agreement, must-never set, harness usage, baseline results, and known limitations.
10. **Update the ledger.**

## 5. Decision rules and evidence standard

- **No metric without a baseline and a threshold.** A score in isolation is trivia.
- **Report per-class results**, never only the aggregate.
- **Human review beats LLM judges for high-stakes accuracy**, and is expensive; use judges for scale, humans for calibration.
- **Small, curated datasets beat large, noisy ones** for the first iteration. Grow deliberately where the model fails.
- **Never tune on the eval set and then report its score as generalisation.** Hold out a set, or state clearly that the number is training-adjacent.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Dataset stratified | inspect composition | all task classes represented |
| No leakage | search prompts for eval samples | none found |
| Metrics reproducible | run harness twice at temp 0 | identical or explained variance |
| Judge calibrated | agreement recorded | ≥20 human labels or judge not used |
| Must-never gate enforced | CI config or harness check | fails the run |
| Results persisted with metadata | inspect output | version/hash/date present |

## 7. Failure handling

- **No realistic data available** → construct synthetic cases from the schema and document that distribution is unvalidated; recommend collecting real cases before launch.
- **Judge disagrees with humans** → reduce judge use to relative comparisons, widen human sampling, or switch metrics.
- **Eval too slow or costly** → split into smoke (fast, every commit) and full (nightly) suites; never drop the must-never set.
- **Variance dominates** (temp > 0) → run N samples per case and report distributions, not single scores.

## 8. Security and authorisation

Risk class B: local eval harness and data. Sanitise all real inputs; no customer PII in the dataset. Do not create provider keys without authorisation; if unavailable, build the harness and mark execution `not run`.

## 9. Completion criteria

- [ ] Task classes defined and dataset stratified.
- [ ] Eval cases with expected outputs and rationales.
- [ ] Leakage check performed.
- [ ] Metrics per class with computation method.
- [ ] Thresholds with baseline evidence; must-never set defined.
- [ ] Judge calibrated or unused.
- [ ] Harness runs reproducibly and emits JSON + summary.
- [ ] Baseline recorded with versions and dataset hash.

## 10. Deliverables and handover

Artifacts: `EVAL_PLAN.md`, dataset, harness, baseline results.

P04 receives: the must-never set and adversarial cases, which inform guardrail requirements; P05 receives: the harness hook for continuous evaluation.
