# 06-Interactive — Context Collectors & Multi-Step Wizards

Prompts designed to intelligently gather missing information from the user before launching a deeper multi-stage system or performing focused work.

These are especially useful when:
- The user’s request is underspecified
- A major system (audit, contribution, from-scratch, migration, etc.) needs structured intake
- You want to avoid premature assumptions

## Structure

| Path | Purpose |
|------|---------|
| `context-collectors/` | Focused intake prompts that produce a clean brief |
| `multi-step-wizards/` | Guided multi-turn flows for complex setup |

## Design Principles

- Ask only high-leverage questions
- Prefer structured output the next system can consume
- Offer reasonable defaults / assumptions when the user is unsure
- Minimize back-and-forth while maximizing clarity
- Explicitly separate known facts, assumptions, and open questions
