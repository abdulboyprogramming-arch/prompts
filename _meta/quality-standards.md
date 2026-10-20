# Quality Standards for Prompt Systems in This Archive

Every prompt set added to this repository should strive to meet the following bar.

## 1. Completeness
- Multi-stage systems must cover the full lifecycle of the intended activity (discovery → planning → execution → validation → communication/handover).
- Single prompts must still define clear inputs, process, outputs, and failure modes.

## 2. Professionalism
- The agent’s behavior must match what a highly competent human professional would do.
- Prefer focused, reviewable, evidence-based work over flashy or speculative output.

## 3. Safety & Authorization
- Explicit handling of secrets and credentials.
- Clear separation of routine vs consequential actions.
- Respect for project governance, licenses, and maintainer expectations.

## 4. Durability
- Multi-stage systems must maintain durable artifacts so work can survive session boundaries.
- Progress and decision rationale must be recorded.

## 5. Evidence Over Assertion
- Claims about code, issues, or opportunities must be backed by concrete observation.
- Distinguish confirmed facts, hypotheses, and opinions.

## 6. Adaptivity
- Prompts must detect and adapt to the actual technology stack, repository size, and project conventions rather than assuming a single stack.

## 7. Usability
- Clear entry point.
- Explicit prerequisites and expected user-provided context.
- Good handover between stages.

## 8. Maintainability of the Prompt Itself
- Versioned.
- Structured headings.
- Avoid unnecessary repetition while keeping each prompt self-contained enough to be understood.

## Review Checklist Before Merging a New System

- [ ] Has a clear README or INDEX in its folder
- [ ] Follows the prompt template structure (or a justified improvement)
- [ ] Defines completion criteria and handover
- [ ] Handles failure and missing information
- [ ] Respects security boundaries
- [ ] Has been smoke-tested on at least one realistic example (or the author explains why not)
