# Legacy source material

These files are the raw prompts and requests that the current library was built from: an early scaffold request, a changelog/commit instruction, an issue-creation guide, a three-part "complete the codebase" sequence, and two enterprise "operating system" prompt drafts.

**They are not part of the library.** They are kept for provenance, and they are explicitly excluded from validation, the catalog, and the gallery (`archive/` is skipped by `scripts/validate_library.py`).

Read them as history, not as guidance:

- They predate the metadata standard, the maturity levels, and the verification rules this repository now enforces.
- Their claims are unchecked — some describe systems that were never built, and some instruct agents in ways the current library forbids (unbounded autonomy, "add every possible feature").
- The ideas that survived were rewritten into `00-core/`, `02-engineering/`, and `04-process/`; where a file here contradicts a current prompt, the current prompt wins.

Why keep them at all: a library that asks others to show their evidence should be able to show its own. The difference between these files and the prompts they became is the point of the repository.

| File | What it is |
|------|------------|
| `Format dot md file.txt` | First request: format and organise the Markdown in the repo |
| `code changes(changelog & commit).txt` | Instruction for change documentation, commit, and branch finalisation |
| `issue creation.txt` | Issue-deduction and implementation-planning agent draft |
| `process1–4(chat1).txt` | Requests for full-codebase completion, plus deployment and submission questions |
| `process5–7(chat2).txt` | "Enterprise autonomous engineering operating system" drafts and a feature-expansion request |
| `scaffold completion.txt` | ASEOS/EAEOS v4.0 constitution draft |
