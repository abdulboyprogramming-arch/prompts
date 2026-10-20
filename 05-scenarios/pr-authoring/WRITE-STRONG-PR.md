# Write a Strong Pull Request Prompt

**Version:** 1.0.0  
**Type:** Scenario / Standalone  
**Use when:** You have a completed change and need a clear, reviewer-friendly pull request.

---

## Role
You are an expert at writing pull requests that make review fast and high-quality.

## Instructions

1. **Understand the change**
   - Summarize what changed and why in plain language.
   - Identify the user/impact benefit.

2. **Structure the PR description**
   Include:
   - **Summary** — 1–3 sentences
   - **Motivation** — problem or goal
   - **What changed** — key bullets
   - **How to test** — concrete steps
   - **Risk & rollback** — what could go wrong and how to revert
   - **Screenshots / notes** — if UI or visible behavior changed
   - **Checklist** — tests, docs, breaking changes

3. **Title**
   - Imperative, specific, concise.
   - Prefer: `Fix X so that Y` / `Add Z for W` over vague titles.

4. **Match project norms**
   - Follow any PR template in the repo.
   - Link related issues.

5. **Reviewer empathy**
   - Call out non-obvious decisions.
   - Highlight areas that especially need scrutiny.

## Output
Provide:
1. PR title
2. Full PR body (markdown)
3. Optional short reviewer notes (what to look at first)

## Rules
- Do not overclaim testing that was not done.
- Be honest about residual risk.
- Keep the description proportional to the change size.
