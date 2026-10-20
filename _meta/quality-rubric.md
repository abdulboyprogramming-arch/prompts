# Prompt Quality Rubric

**Version:** 2.0.0
**Use:** scoring a prompt before it is labelled `operational` or `canonical`, and when triaging an existing prompt.

A score without anchors is decoration. Every band below defines what earns the points.

---

## 1. Scoring model

100 points across ten dimensions. Weights shift by **tier**, because a 40-line utility prompt and a nine-stage autonomous recovery prompt cannot be judged identically.

| Dimension | Full autonomous / recovery | Implementation | Diagnostic / utility |
|---|---:|---:|---:|
| 1. Objective and scope clarity | 10 | 10 | 15 |
| 2. Context acquisition and discovery | 10 | 10 | 15 |
| 3. Technical specificity | 15 | 15 | 15 |
| 4. Actionability and workflow | 15 | 15 | 15 |
| 5. Verification and acceptance criteria | 15 | 15 | 10 |
| 6. Safety and risk management | 10 | 10 | 5 |
| 7. Deliverable quality and handover | 10 | 10 | 10 |
| 8. Adaptability and reusability | 5 | 5 | 5 |
| 9. Composition and workflow compatibility | 5 | 5 | 5 |
| 10. Clarity, consistency, concision | 5 | 5 | 5 |
| **Total** | **100** | **100** | **100** |

Bands: **90–100** canonical-worthy · **75–89** operational · **60–74** draft · **<60** skeleton.

Tier selection: if the prompt can touch files, use the implementation column; if it can run an unbounded multi-stage loop, use the autonomous column; otherwise utility.

## 2. Anchors

### 1. Objective and scope clarity
- **0** — No discernible objective; reads as motivational text.
- **5** — Objective stated but not measurable; scope boundaries unstated.
- **8** — Clear objective and a short "not responsible for" list.
- **10** — Objective, success definition, and explicit out-of-scope items that a reviewer could use to reject scope creep.

### 2. Context acquisition and discovery
- **0** — Assumes facts about the target system.
- **5** — Tells the agent to "look at the repo" without specifying what to establish.
- **8** — Names the discovery targets (stack, test command, conventions, CI, Git state) and the order.
- **10** — Discovery is ordered, prioritised, and bounded (depth limits for large repos), with an instruction to distinguish verified from inferred.

### 3. Technical specificity
- **0** — Generic advice true of any project.
- **5** — Correct but shallow; no expert content a competent engineer would not already know.
- **10** — Demonstrates real domain knowledge: named failure modes, concrete commands/patterns, and the trade-off reasoning behind them.
- **15** — Would teach a strong engineer something: domain-specific traps, non-obvious verification, explicit criteria for hard judgement calls.

### 4. Actionability and workflow
- **0** — Vague exhortations.
- **5** — Numbered steps that still require invention to execute.
- **10** — Executable steps; each has an input, an action, and an output.
- **15** — Executable, dependency-aware, staged, with decision points and an explicit stopping rule matching the execution mode.

### 5. Verification and acceptance criteria
- **0** — No verification.
- **5** — "Run the tests."
- **10** — Named checks tied to the actual change, plus what to do when they fail.
- **15** — Multiple independent verification layers (e.g. unit → integration → manual repro), explicit pass thresholds, and a rule that distinguishes "check ran and passed" from "check could not be run".

### 6. Safety and risk management
- **0** — Encourages destructive or unauthorised action.
- **5** — Generic "be careful".
- **8** — Risk class declared; destructive actions named and gated.
- **10** — Risk class declared and justified; irreversible actions require explicit approval; secrets rules referenced; rollback defined for mutations.

### 7. Deliverable quality and handover
- **0** — No output defined.
- **5** — Deliverable named but not structured.
- **8** — Named artifacts with required contents.
- **10** — Named artifacts, required contents, quality bar for each, and a handover block the next stage can consume without re-reading everything.

### 8. Adaptability and reusability
- **0** — Hardcoded to one private project.
- **5** — Placeholders exist but mix discoverable and user-supplied information.
- **8** — Stack-agnostic; placeholders limited to genuinely external inputs.
- **5/5 max band** — Works across project sizes with explicit large-repo and monorepo adaptations.

### 9. Composition and workflow compatibility
- **0** — Contradicts other prompts in its system.
- **3** — Compatible in isolation; unclear inputs/outputs.
- **5** — Declared dependencies, compatible artifact names, no duplicated conflicting rules, referenced in at least one workflow or index.

### 10. Clarity, consistency, concision
- **0** — Internal contradictions, broken structure.
- **3** — Understandable but repetitive or padded.
- **5** — Tight, consistent terminology, no restated rules, no empty superlatives.

## 3. Critical failure conditions (automatic reject)

A prompt is **not ready**, regardless of score, if any of these hold:

1. Contradictory instructions (e.g. "read-only" plus "apply the changes").
2. Instructions that grant unauthorised or unbounded destructive autonomy.
3. Claims of capability the agent cannot be assumed to have (private APIs, unstated credentials, guaranteed network).
4. Missing acceptance criteria on a prompt that mutates code or infrastructure.
5. Ambiguity about whether the task is analysis or implementation.
6. An instruction to report success without verification, or to treat a passing build as proof of correctness.
7. Incompatible workflow dependencies (produces an artifact the next stage does not read, or reads one that is never produced).
8. Materially incorrect technical guidance (wrong command semantics, unsafe migration order, invalid security advice).
9. A maturity label that overstates the artifact.

Any of these blocks the `operational` label until fixed or explicitly waived in writing inside the file with justification.

## 4. Review record

When reviewing a prompt, append a short record to the review log (`_meta/review-log.md`):

```
AUDIT-P03 · 2026-10-20 · tier: diagnostic · score 88 · operational
Reason: complete workflow and evidence rules; verification lacks a
negative-path check for unparsable manifests. Follow-up: add it at v1.2.
```

Do not record a score without the reason: the reason is the artifact that helps the next reviewer.

## 5. System-level review

A multi-stage system is reviewed as a whole as well as per stage:

- **Coverage** — does the stage sequence cover discovery → decision → execution → verification → handover without a missing step?
- **Consistency** — do stages agree on artifact names, risk class, and stopping rules?
- **Weakest link** — the system's maturity is its weakest *required* stage.
- **Integration** — does the orchestrator actually instruct the agent to read each stage's declared artifact?
- **Failure paths** — is there a defined route when a middle stage is blocked?

Record system-level verdicts in the system's `README.md` and in `_meta/review-log.md`.
