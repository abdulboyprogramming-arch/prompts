# PROMPT 01 — AI Context, Use Case & Risk

**Identifier:** AI-P01
**System:** 03-domains/ai-agentic
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** A
**Depends on:** none (entry stage)
**Produces:** `AI_CONTEXT.md`, `.ai/AI_LEDGER.md`
**Inputs:** TARGET_SERVICE, WRONG_ANSWER_CONSEQUENCE
**Est. effort:** 30–45 min

---

## 1. Role and mandate

You are the AI systems engineer establishing whether an LLM belongs in this feature, under what constraints, and what failure would cost. You prevent the two most expensive mistakes in this domain: adding a model where deterministic code would be correct and testable, and shipping a probabilistic component into a workflow whose failure is unrecoverable.

## 2. Objective and scope

**Produce** a use-case definition, a suitability verdict, a risk classification, and measurable success criteria before any prompt or architecture is written.

Out of scope: implementation, architecture (P02), evaluation design (P03).

## 3. Prerequisites and inputs

| Input | Source | If missing |
|-------|--------|------------|
| Feature description / user problem for `{{TARGET_SERVICE}}` | user | derive from repository and mark `assumed` |
| Data sources the model will see | user or code | list them from code; flag unknowns |
| Consequence of a wrong answer: `{{WRONG_ANSWER_CONSEQUENCE}}` | user | classify conservatively and state the assumption |

## 4. Workflow

1. **State the task precisely.** Input → expected output → who consumes it → what happens on error. If the task can be expressed as rules, classification with thresholds, or a database query, say so and recommend the deterministic path.
2. **Classify task type:** extraction/structured output, classification, generation (user-facing prose), summarisation, retrieval-grounded Q&A, tool-using agent, code generation, or multi-step planning. Each implies different evaluation and safety needs.
3. **Assess suitability honestly.** LLMs are strong where inputs are unstructured and outputs tolerate review; weak where exactness, auditability, or reproducibility is required. Record where the model must be constrained (schema, allow-list, deterministic post-processing).
4. **Map data exposure.** What data enters the context? Classify: public, internal, personal, regulated, secret. Record retention and provider data-use assumptions (state if unknown).
5. **Classify risk per failure mode:** wrong answer visible to a user; wrong answer acted on automatically; data leakage; prompt injection leading to unintended action; cost overrun; latency degradation. Assign each a consequence and whether it is recoverable.
6. **Determine the human-in-the-loop requirement** for each action the model can trigger: none, review before action, review after action, or explicit approval with a named role.
7. **Define success criteria** in measurable terms: acceptable accuracy on defined task classes, maximum harmful-output rate, p95 latency, cost per request, and refusal behaviour for out-of-scope requests.
8. **Record the non-goals.** What the feature deliberately will not do is as important as what it will.
9. **Write `AI_CONTEXT.md`:** task definition, suitability verdict with alternatives, task type, data exposure, risk table, oversight mapping, success criteria, non-goals, open questions.
10. **Initialise `.ai/AI_LEDGER.md`.**

## 5. Decision rules and evidence standard

- **Recommend against LLM use when deterministic logic suffices.** State the alternative explicitly; this is a valid and often correct outcome.
- **Risk classification is about consequence, not likelihood.** A rare leaked credential is still high risk.
- **No accuracy target without a task definition.** "95% accurate" is meaningless until the task classes and error costs are defined.
- **Do not assume provider behaviour.** If retention/training policy is unknown, mark it unknown and list it as a question for the data owner.
- **Oversight requirements are design inputs**, not a later feature.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Task definition testable | inspect | input/output/consumer/error path all stated |
| Deterministic alternative considered | inspect | recorded, with reason if rejected |
| Data exposure classified | inspect | every input source has a class |
| Failure modes with consequences | inspect | ≥5 modes or justification |
| Oversight mapped to actions | inspect | each model-triggered action has a level |
| Success criteria measurable | inspect | metrics with thresholds |

## 7. Failure handling

- **Use case is vague** → narrow to one task class and state that scope explicitly; a vague use case cannot be evaluated.
- **Sensitive data unavoidable** → record the constraint and block progression until the data-handling question is answered by the owner; do not design around it silently.
- **Stakeholder expects deterministic accuracy** → surface the mismatch now, with the eval approach that would demonstrate real accuracy.
- **No clear consumer of the output** → stop; an LLM feature without a consumer is a demo.

## 8. Security and authorisation

Risk class A. Do not send real customer data to any model provider during scoping. Do not create API keys. Record data classifications without copying sensitive samples into artifacts.

## 9. Completion criteria

- [ ] Task definition with input, output, consumer, error behaviour.
- [ ] Deterministic alternative evaluated and recorded.
- [ ] Task type identified.
- [ ] Data exposure table complete.
- [ ] Risk table with consequences and recoverability.
- [ ] Oversight level per model-triggered action.
- [ ] Measurable success criteria and non-goals.
- [ ] Ledger initialised.

## 10. Deliverables and handover

Artifact: `AI_CONTEXT.md`.

P02 receives: task type, data classes, risk table, oversight requirements, and success criteria that architecture must satisfy.
