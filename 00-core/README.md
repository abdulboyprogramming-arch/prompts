# 00-Core — Foundational Primitives

Shared substrate for every system in this library: authorisation categories, secret handling, orchestration and handover rules, the base agent contract, and the prompt-engineering standards.

These files are **reference primitives, not task prompts.** They are meant to be read by the agent (or pasted ahead of a system prompt), not run on their own. They therefore carry no identifier, maturity, or execution-mode metadata and do not appear in the generated catalog.

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

- No primitive yet for **multi-agent coordination** (ownership, conflict resolution, integration). Tracked in the backlog.
- No primitive for **long-session context compaction** beyond the ledger pattern.
