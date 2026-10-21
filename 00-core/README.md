# 00-Core — Foundational Primitives

Shared substrate for every system in this library: authorisation categories, secret handling, orchestration and handover rules, the base agent contract, and the prompt-engineering standards.

Most of these files are **reference primitives, not task prompts.** They are meant to be read by the agent (or pasted ahead of a system prompt), not run on their own, and therefore carry no identifier, maturity, or execution-mode metadata.

The exception is `prompt-engineering/PROMPT-FORGE.md` and `PROMPT-REGRESSION.md` (`GEN-P01`, `GEN-P02`) and the four `conversational/` prompts (`CHAT-MODE`, `CHAT-REVIEW`, `CHAT-DEBUG`, `CHAT-DESIGN`): these are **executable prompts** with full metadata, because generating a prompt and running one in a chat window are both tasks with an artifact and a check. They appear in the catalog.

## Contents

| Path | Purpose |
|------|---------|
| [`safety-and-security/ACTION-CATEGORIES.md`](safety-and-security/ACTION-CATEGORIES.md) | A/B/C/D authorisation vocabulary and default rules |
| [`safety-and-security/SECRETS-AND-SENSITIVE-DATA.md`](safety-and-security/SECRETS-AND-SENSITIVE-DATA.md) | Secret handling, redaction, responsible disclosure, rotation |
| [`agent-orchestration/MULTI-STAGE-HANDOVER.md`](agent-orchestration/MULTI-STAGE-HANDOVER.md) | Handover contents and the progress-ledger pattern |
| [`agent-orchestration/RECOVERY-AND-FAILURE.md`](agent-orchestration/RECOVERY-AND-FAILURE.md) | Failure classes and the response pattern |
| [`system-prompts/BASE-ENGINEERING-AGENT.md`](system-prompts/BASE-ENGINEERING-AGENT.md) | Standing obligations for any engineering agent |
| [`prompt-engineering/QUALITY-BAR.md`](prompt-engineering/QUALITY-BAR.md) | Short statement of the bar (canonical detail lives in `_meta/`) |
| [`prompt-engineering/STAGE-PROMPT-TEMPLATE.md`](prompt-engineering/STAGE-PROMPT-TEMPLATE.md) | Pointer to the canonical authoring standard |
| [`prompt-engineering/PROMPT-FORGE.md`](prompt-engineering/PROMPT-FORGE.md) | **GEN-P01** — build a runnable prompt from a user's description (compose / interview / improve / decompose / port) |
| [`prompt-engineering/PROMPT-REGRESSION.md`](prompt-engineering/PROMPT-REGRESSION.md) | **GEN-P02** — prove a prompt change is an improvement: fixtures, runs, rubric score, defect classification |
| [`conversational/`](conversational/README.md) | **Chat mode** — run any prompt in a chat window with no repository access, plus chat-native review, debugging, and design |

## Authority

Where this folder and `_meta/` appear to overlap:

- **Behavioural rules** (authorisation, secrets, handover, failure) → this folder is authoritative.
- **Authoring rules** (metadata, sections, maturity, scoring) → `_meta/prompt-authoring-standard.md` and `_meta/quality-rubric.md` are authoritative. `prompt-engineering/QUALITY-BAR.md` remains as a short summary only; it does not define its own standard.

## Usage

Specialised systems reference these primitives rather than restating them. A prompt that repeats the A/B/C/D definitions instead of citing them is a maintenance liability: when the rule changes, copies drift.

Recommended preamble for a high-autonomy session:

```
Read and obey:
- 00-core/safety-and-security/ACTION-CATEGORIES.md
- 00-core/safety-and-security/SECRETS-AND-SENSITIVE-DATA.md
- 00-core/system-prompts/BASE-ENGINEERING-AGENT.md
Then execute the system named below, following its stage order and completion criteria.
```

## Gaps

- Multi-agent coordination is covered by [`agent-orchestration/MULTI-STAGE-HANDOVER.md`](agent-orchestration/MULTI-STAGE-HANDOVER.md) for state passing, and by `07-workflows/multi-agent-orchestration.md` for decomposition and integration. Neither is a `00-core` primitive yet; the gap is the primitive, not the guidance.
- No primitive for **long-session context compaction** beyond the ledger pattern.
