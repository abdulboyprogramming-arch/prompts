# Legacy source material

These files are the raw prompts and requests that the current library was built from: an early scaffold request, a changelog/commit instruction, an issue-creation guide, a three-part "complete the codebase" sequence, and two enterprise "operating system" prompt drafts.

**They are not part of the library.** They are kept for provenance, and they are explicitly excluded from validation, the catalog, and the gallery (`archive/` is skipped by `scripts/validate_library.py`).

Read them as history, not as guidance:

- They predate the metadata standard, the maturity levels, and the verification rules this repository now enforces.
- Their claims are unchecked — some describe systems that were never built, and some instruct agents in ways the current library forbids (unbounded autonomy, "add every possible feature").
- The ideas that survived were rewritten into `00-core/`, `02-engineering/`, and `04-process/`; where a file here contradicts a current prompt, the current prompt wins.

Why keep them at all: a library that asks others to show their evidence should be able to show its own. The difference between these files and the prompts they became is the point of the repository.

| File | What it is | Prompts or chat turns |
|------|------------|------------------------|
| `Format dot md file.txt` | First request: format and organise the Markdown in the repo | prompt (one sentence) |
| `code changes(changelog & commit).txt` | Instruction for change documentation, commit, and branch finalisation | prompt |
| `issue creation.txt` | Issue-deduction and implementation-planning agent draft | prompt |
| `process1(chat1).txt` | ASEOS **v2.0** constitution plus a full-codebase completion request | request + document |
| `process2(chat1).txt` | ASEOS autonomous completion system, second version of the request | prompt |
| `process3(chat1).txt` | *"how will i see it"* — seven words, no antecedent | **chat turn** |
| `process4(chat1).txt` | Hackathon demo and submission question | **chat turn** |
| `process5(chat2).txt` | ASEOS **v3.0** constitution draft | document |
| `process6(chat2).txt` | "Autonomous product evolution and feature invention" draft | prompt |
| `process7(chat2).txt` | Request to add every possible feature | **chat turn** |
| `scaffold completion.txt` | ASEOS/EAEOS v4.0 constitution draft | document |

**Three of these are turns in a conversation, not prompts.** `process3`, `process4` and `process7` are
replies a person typed in the middle of a session: they refer to *"it"* and *"this software"* without
ever naming the project, and read alone they cannot be answered. They are kept because they show what a
real request looks like before it is structured — which is the point of the whole folder.

**Corrections and rewrites, 2026-10-23:**

- [`AUDIT.md`](AUDIT.md) — the seven findings that matter in the long files: three unsuperseded
  constitutions, an instruction that cannot be followed, scope with no stopping condition, four safety
  rules the library now forbids, "production-ready" defined as "the build passed", missing provenance,
  and this README's own former habit of calling chat turns "prompts".
- [`rewritten/`](rewritten/README.md) — the four short requests said properly, with the original kept
  verbatim alongside. Read [`rewritten/04-feature-portfolio.md`](rewritten/04-feature-portfolio.md) if
  you only read one: it turns *"add every possible feature"* into a decision that can be finished.

Nothing in the twelve `.txt` files was edited. The audit and the rewrites are additional documents.
