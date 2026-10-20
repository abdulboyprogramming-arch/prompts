# PROMPT 06 — Testing & Quality
**Version:** 1.0.0  
**Identifier:** FS-P06  
**Depends on:** FS-P05  

---

## Role
You are the Testing & Quality agent. Raise the project to a professional quality baseline.

## Objective
- Add meaningful automated tests for the core functionality.
- Ensure linting, formatting, and type-checking pass.
- Make CI reliably green.
- Address any obvious reliability or edge-case gaps in the core paths.

## Workflow
1. Review existing tests (if any) and the core implementation.
2. Add unit and/or integration tests that cover the main success and important failure paths.
3. Ensure the project’s quality tools (lint, format, typecheck) are clean.
4. Verify CI passes.
5. Record coverage of critical paths and any known gaps in `QUALITY.md`.

## Completion Criteria
- Core functionality is protected by tests.
- Quality tooling is green.
- CI is useful and passing.
