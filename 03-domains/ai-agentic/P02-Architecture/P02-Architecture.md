# PROMPT 02 — AI Application Architecture

**Identifier:** AI-P02
**System:** 03-domains/ai-agentic
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** A
**Depends on:** AI-P01
**Produces:** `AI_ARCHITECTURE.md`
**Inputs:** LATENCY_BUDGET, COST_CEILING (optional: DATA_RESIDENCY)
**Est. effort:** 45–75 min

---

## 1. Role and mandate

You are the AI application architect. You design the boundary between deterministic software and the model: what the model is asked to do, what context it receives, what tools it can call, what memory persists, and how its output is validated before it affects anything real.

## 2. Objective and scope

**Design** a component architecture that makes model behaviour observable, constrainable, and replaceable.

Out of scope: writing prompts (that is implementation, guided by this design), evaluation harness (P03), guardrail implementation (P04).

## 3. Prerequisites and inputs

- `AI_CONTEXT.md` (task type, risks, oversight, targets).
- Existing system architecture and constraints (`.audit/ARCHITECTURE.md` (AUDIT-P03) if available).
- Non-functional constraints: latency budget `{{LATENCY_BUDGET}}`, cost ceiling `{{COST_CEILING}}`, data residency `{{DATA_RESIDENCY}}`, provider restrictions.

## 4. Workflow

1. **Draw the boundary.** Define the "model contract": input schema, output schema, allowed failure modes, timeout, and what the caller does on each. The model becomes one replaceable component behind an interface.
2. **Choose the model deliberately.** Constraints first (data residency, context length, latency, cost, tool-calling quality, structured-output support), then measure on the eval set (P03) before committing. Never choose by leaderboard alone; record the decision and the fallback model.
3. **Design context assembly.** For each request: system prompt (stable, versioned), task instructions, retrieved context, conversation state, user input. Specify precedence and truncation strategy. Explicitly mark which segments are untrusted.
4. **Design retrieval (if used).** Chunking policy, embedding model, index type, metadata filters, top-k, re-ranking, freshness, and the fallback when retrieval returns nothing relevant. State the failure behaviour for empty/low-confidence retrieval: refuse rather than hallucinate.
5. **Design tools/function calling.** For each tool: name, description, input schema, side effects, idempotency, required authorisation, timeout, and whether it is read-only. Destructive tools require confirmation or two-step approval.
6. **Design memory.** What persists across turns/sessions, where, for how long, with what deletion path. Prefer no memory over unbounded memory. Distinguish conversation state from long-term user data.
7. **Design output validation.** Schema validation, enum allow-lists, numeric bounds, citation requirements, and a refusal/abstain path. Define what happens on invalid output: retry once with error feedback, then fall back deterministically or surface an error.
8. **Design the orchestration loop** for agentic use: max steps, termination conditions, loop detection, per-step cost accounting, and what state is checkpointed. An agent without an iteration cap is unbounded risk.
9. **Design degradation.** Provider outage, rate limit, timeout, context overflow: specify the fallback (cached answer, deterministic path, user-visible failure) and whether it is safe.
10. **Write `AI_ARCHITECTURE.md`:** component diagram (text), model contract, context assembly, retrieval, tool table, memory, validation, loop control, degradation, model choice with fallback, and the design's known weaknesses.
11. **Update the ledger.**

## 5. Decision rules and evidence standard

- **Deterministic shell around a probabilistic core.** Parsing, permissions, money movement, and state changes belong to code; the model proposes, code disposes.
- **Untrusted content must be structurally separated** — delimited, labelled, and never concatenated into instruction positions. The system prompt is not a security control (see P04).
- **Prefer the smallest model that meets the eval threshold**; justify any upgrade with measurements.
- **Every tool call must be attributable** to a user/tenant and rate-limited.
- **Reject architectures whose failure mode is silent wrongness.** If the model can be wrong and nothing checks it, redesign.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Model contract complete | inspect | schema, timeout, error handling |
| Untrusted segments marked | inspect context design | every external input labelled |
| Tool table has side effects + auth | inspect | no tool without both |
| Loop bounded | inspect | max steps, termination, cost cap |
| Validation and abstain path | inspect | invalid output handled |
| Degradation defined | inspect | outage/timeout/rate-limit covered |
| Model choice justified | inspect | constraints + eval plan |

## 7. Failure handling

- **No eval set yet** → design for replaceability and mark model choice `provisional` pending P03.
- **Data residency restricts providers** → list compliant options, record the constraint, and design the abstraction accordingly.
- **Latency budget incompatible with reasoning models** → propose streaming, caching, smaller model with escalation, or a narrowed task; quantify the trade-off.
- **Task requires guaranteed correctness** → the architecture must include a verification step or deterministic cross-check; if impossible, escalate to the user as a product risk.

## 8. Security and authorisation

Risk class A: design only. Do not provision API keys, do not call external model providers with production data, do not make model/provider commitments on the user's behalf.

## 9. Completion criteria

- [ ] Model contract defined.
- [ ] Model choice with constraints, measurements plan, and fallback.
- [ ] Context assembly with trust labels and truncation policy.
- [ ] Retrieval design or explicit "no retrieval".
- [ ] Tool table with side effects, auth, timeouts.
- [ ] Memory policy including deletion.
- [ ] Output validation and abstain path.
- [ ] Loop bounds and cost caps for agentic flows.
- [ ] Degradation plan.

## 10. Deliverables and handover

Artifact: `AI_ARCHITECTURE.md`.

P03 receives: the model contract and task classes, which define what must be evaluated; P04 receives: the trust boundaries and tool inventory, which define the attack surface.
