# Stage Prompt Template (superseded)

**Version:** 2.0.0
**Status:** Pointer — do not add new material here.

The canonical authoring standard is [`_meta/prompt-authoring-standard.md`](../../_meta/prompt-authoring-standard.md), with a filled example in [`_meta/prompt-template.md`](../../_meta/prompt-template.md) and the scoring model in [`_meta/quality-rubric.md`](../../_meta/quality-rubric.md).

This file is kept because existing systems reference it. It no longer defines its own format; maintaining two templates produced exactly the inconsistency the audit removed.

## Minimum viable stage prompt

A stage prompt is acceptable only when it states, in this order:

1. Who the agent is, in one sentence, plus what it must *not* do.
2. The objective and the out-of-scope boundary.
3. Prerequisites, and what to do if one is missing.
4. Numbered workflow steps, each ending in a concrete output.
5. How to decide between options and what counts as evidence.
6. How the result will be verified, including negative cases.
7. Failure handling.
8. Authorisation limits (risk class in operational terms).
9. Completion criteria a reviewer can check without trusting the agent.
10. The artifact produced and what the next stage needs from it.

Anything less is a `skeleton` and must be labelled as such.

## Anti-patterns

- Workflow steps that say "analyse" without saying what evidence is produced.
- "Ensure quality" as a completion criterion.
- A stage that ends in a recommendation when its mode is `implementation`.
- Naming artifacts in prose but not fixing their paths.
- Duplicating safety rules that live in `00-core/safety-and-security/`.
