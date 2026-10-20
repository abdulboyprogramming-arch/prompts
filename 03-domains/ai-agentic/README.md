# AI, LLM & Agentic Systems

**Maturity: operational (v1.0.0).** Five stages for building software whose behaviour is probabilistic and whose inputs may be adversarial.

**Entry point:** [`P01-Context/P01-Context-Risk.md`](P01-Context/P01-Context-Risk.md)
**Execution mode:** audit-remediation
**Risk class:** B — code, prompts, evaluation harnesses, configuration; no model fine-tuning or production deployment without authorisation

## Why this system exists

Conventional engineering prompts assume deterministic code: same input, same output, verifiable by assertion. LLM features break that assumption in three ways:

1. **Outputs vary.** Testing requires evaluation sets and acceptable thresholds, not equality assertions.
2. **Inputs are untrusted prose.** Prompt injection turns every retrieved document, tool result, and user message into potential instruction input.
3. **Failure is fluent.** A broken LLM feature usually produces a confident, plausible, wrong answer rather than an exception.

This system addresses those specifically. It is not a prompt-engineering tip list; it is the engineering discipline around a stochastic component: architecture, evaluation, safety, and operations.

## Stages

| ID | Stage | Produces |
|----|-------|----------|
| AI-P01 | [Context, use case & risk](P01-Context/P01-Context-Risk.md) | `AI_CONTEXT.md` |
| AI-P02 | [Architecture: model, tools, memory, retrieval](P02-Architecture/P02-Architecture.md) | `AI_ARCHITECTURE.md` |
| AI-P03 | [Evaluation-driven development](P03-Evaluation/P03-Evaluation.md) | `EVAL_PLAN.md`, eval harness |
| AI-P04 | [Safety, guardrails & prompt-injection defence](P04-Safety/P04-Safety-Guardrails.md) | `SAFETY.md`, guardrail code |
| AI-P05 | [Production: observability, cost, human oversight](P05-Production/P05-Production-Operations.md) | `AI_OPERATIONS.md` |

## Shared principles

1. **Evaluation before optimisation.** Without a fixed eval set and metric, every change is an opinion.
2. **Determinism where possible.** Temperature 0 for classification/extraction; prompt templates versioned; model version pinned. Introduce randomness deliberately.
3. **Treat all model input as untrusted.** Retrieved content, tool output, and user text are data — never instructions. The system prompt is not a security boundary.
4. **Validate outputs structurally.** Schema validation, type checks, allow-lists, and refusal handling before anything downstream consumes a model response.
5. **Least-privilege tools.** Every tool call runs with the narrowest credential and blast radius that satisfies the task; destructive tools require confirmation.
6. **Human oversight scales with consequence.** Read-only suggestions can be automatic; anything that writes, pays, or emails needs an approval step whose absence is visible in the design.
7. **Cost and latency are product requirements**, tracked per request and per feature, not discovered on the invoice.

## Relationship to other systems

- The prompts *inside* the product (system prompts, tool descriptions) are engineering artifacts: apply `_meta/prompt-authoring-standard.md`.
- Conventional backend concerns (auth, data model, rate limits) use `03-domains/backend/`.
- Injection defence overlaps `02-engineering/security-hardening/`; AI-P04 covers the LLM-specific surface.
- Evaluation harnesses are tests: reuse the discipline in `04-process/testing-qa/`.

## What this system will not do

- Guarantee that a model cannot be manipulated. Defence is layered and probabilistic; the design goal is bounded impact, not immunity.
- Provide model-selection advice without a task and eval set.
- Replace legal or regulatory review of data use.
