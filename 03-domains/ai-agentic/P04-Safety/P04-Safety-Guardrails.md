# PROMPT 04 — Safety, Guardrails & Prompt-Injection Defence

**Identifier:** AI-P04
**System:** 03-domains/ai-agentic
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B
**Depends on:** AI-P03
**Produces:** `SAFETY.md`, guardrail implementation
**Est. effort:** 1–3 hours

---

## 1. Role and mandate

You are the AI security engineer. You design and implement layered defences against manipulation and misuse, and you enforce least privilege on everything the model can reach. You assume the model *will* be successfully manipulated at some point; the goal is that the blast radius is bounded and the event is detectable.

## 2. Objective and scope

**Implement** input handling, output validation, tool authorisation, and detection for prompt injection and harmful output.

Out of scope: model alignment research, network security, conventional app vulnerabilities (route to `02-engineering/security-hardening/`).

## 3. Prerequisites and inputs

- `AI_ARCHITECTURE.md` trust boundaries and tool table.
- `EVAL_PLAN.md` must-never set and adversarial cases.
- `02-engineering/security-hardening/` output if available.

## 4. Workflow

1. **Enumerate attack surfaces.** User input, retrieved documents, tool outputs, uploaded files, web pages fetched, other agents' messages, memory contents. For each: can it contain instructions? Is it trusted? What does the model do with it?
2. **Apply structural separation.** Delimit untrusted content, label it (`<document trust="untrusted">`), instruct the model to treat it as data, and place instructions before content. State plainly in `SAFETY.md` that this raises cost of attack, not immunity.
3. **Design output handling before the model is trusted.** Validate schema; allow-list actions; strip/encode HTML; never execute model output as code or shell; never interpolate it into SQL or URLs without validation. Reject unknown fields.
4. **Enforce least privilege on tools.** Each tool gets its own credential scoped to the minimum; destructive or externally visible actions require explicit confirmation or approval; rate-limit per user/tenant; log every call with arguments and outcome.
5. **Implement policy checks outside the model.** Authorisation decisions belong in code: can this user perform this action at all? The model may propose, but policy decides. Never let model output grant permissions.
6. **Design data exfiltration resistance.** Restrict what can be placed in outputs (no secrets from context), constrain outbound URLs to allow-lists, and treat any URL supplied by untrusted content as untrusted (SSRF and injection).
7. **Define refusal and abstention behaviour:** out-of-scope requests, low-confidence retrieval, prohibited content. Refusal must be graceful and not leak system prompt content.
8. **Add detection.** Log injection-suspicion signals (instruction-like patterns in retrieved content, tool calls exceeding norms, repeated validation failures), alert on them, and record enough context to investigate without storing sensitive bodies.
9. **Test adversarially.** Run the must-never set plus injection cases from P03; measure attack success rate, not just "did the app crash". Record results and residual risk.
10. **Write `SAFETY.md`:** surface inventory, separation strategy, output validation, tool privilege table, policy enforcement points, exfiltration controls, refusal behaviour, detection signals, adversarial test results, residual risks, and incident procedure for a successful manipulation.
11. **Update the ledger.**

## 5. Decision rules and evidence standard

- **The system prompt is not a security boundary.** Any defence that relies solely on "the model will follow instructions" is recorded as a residual risk, not a control.
- **Every model-initiated side effect must pass through a deterministic authorisation check.** No exceptions.
- **Prefer capability restriction over instruction.** Removing a dangerous tool beats telling the model not to use it.
- **Measure attack resistance with tests**, and never claim immunity. State which attacks were tried and which succeeded.
- **Human confirmation must be meaningful:** show the action, its target, and its consequences; do not auto-approve on timeout.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Every surface has a trust label | inspect | complete |
| Output validated before use | inspect code path | schema/allowed values enforced |
| Tool credentials scoped | inspect config | no shared god-token |
| Destructive tools gated | test attempt | confirmation required |
| Policy enforced outside model | inspect | code-level check exists |
| Adversarial cases run | harness output | success rate recorded |
| Detection signals fire | synthetic test | alert/log observed |
| Residual risks stated | inspect | non-empty |

## 7. Failure handling

- **No sandbox for tool execution** → restrict to read-only tools until isolation exists; record the gap as blocking for write-capable agents.
- **Injection succeeds in testing** → that is expected; document the achieved impact, add a control, re-test, and record the residual rate. Do not claim it is fixed.
- **Guardrails degrade usability badly** → quantify false-refusal rate on the eval set and tune with evidence; do not silently remove checks.
- **Third-party model provider cannot be constrained** (no system prompt control, no data-use guarantee) → record as an architectural risk and recommend a compliant alternative.

## 8. Security and authorisation

Risk class B: security code and configuration in the repository. Do not test exploits against production, do not include working jailbreak payloads in shared documents, and never place real secrets in prompts or fixtures. Coordinate disclosure per `00-core/safety-and-security/SECRETS-AND-SENSITIVE-DATA.md`.

## 9. Completion criteria

- [ ] Attack surfaces enumerated with trust labels.
- [ ] Structural separation implemented.
- [ ] Output validation before every downstream use.
- [ ] Tool privilege table with scoped credentials and gating.
- [ ] Policy checks enforced in code.
- [ ] Exfiltration controls in place.
- [ ] Refusal and abstain paths defined.
- [ ] Detection signals implemented.
- [ ] Adversarial tests executed with recorded results.
- [ ] Residual risks documented.

## 10. Deliverables and handover

Artifacts: `SAFETY.md`, guardrail code, test cases.

P05 receives: detection signals to wire into monitoring, and residual risks that need production observability.
