# Legacy source material

These files are the raw prompts and requests that the current library was built from: an early scaffold
request, a changelog/commit instruction, an issue-creation guide, a two-part "complete the codebase"
sequence, and two enterprise "operating system" prompt drafts.

**They are not part of the library.** They are kept for provenance, and they are explicitly excluded
from validation, the catalog, and the gallery (`archive/` is skipped by `scripts/validate_library.py`).

Read them as history, not as guidance:

- They predate the metadata standard, the maturity levels, and the verification rules this repository
  now enforces.
- Their claims are unchecked — some describe systems that were never built, and some instruct agents in
  ways the current library forbids (unbounded autonomy, "add every possible feature").
- The ideas that survived were rewritten into `00-core/`, `02-engineering/`, and `04-process/`; where a
  file here contradicts a current prompt, the current prompt wins.

Why keep them at all: a library that asks others to show their evidence should be able to show its own.

| File | What it is |
|------|------------|
| `code changes(changelog & commit).txt` | Instruction for change documentation, commit, and branch finalisation |
| `issue creation.txt` | Issue-deduction and implementation-planning agent draft |
| `process1(chat1).txt` | ASEOS **v2.0** constitution plus a full-codebase completion request |
| `process2(chat1).txt` | ASEOS autonomous completion system, second version of the request |
| `process5(chat2).txt` | ASEOS **v3.0** constitution draft |
| `process6(chat2).txt` | "Autonomous product evolution and feature invention" draft |
| `scaffold completion.txt` | ASEOS/EAEOS v4.0 constitution draft |
| `markdown-formatting-pass.txt` | Presentation-only Markdown pass — **complete prompt since 2026-10-23** |
| `deployment-to-a-url.txt` | First reachable URL — **complete prompt since 2026-10-23** |
| `hackathon-submission.txt` | Deadline-driven submission — **complete prompt since 2026-10-23** |
| `feature-portfolio-decision.txt` | Now / next / not-now portfolio — **complete prompt since 2026-10-23** |

## Rewritten in place on 2026-10-23

Four files in this folder were not prompts. They were fragments — a sentence, a seven-word question, a
paragraph of wants — that only made sense inside a conversation that has not survived. Each has been
**rewritten in place**: the fragment is gone rather than kept beside its replacement, the filename now
names the job, and what sits in the file is a complete prompt with inputs, an ordered procedure, failure
handling, and a definition of done.

| File | What it now does |
|---|---|
| `markdown-formatting-pass.txt` | A presentation-only pass: a measured baseline, an agreed rule set, batches of ten revertible commits, and the rule that **a file you reformatted and a file you fixed are different claims** |
| `deployment-to-a-url.txt` | State, audience and spend limit as inputs; the truth about the build established first; names-only secrets; an end-to-end check from outside the machine; an exercised rollback |
| `hackathon-submission.txt` | Rules before advice, a backwards absolute-time timeline, a submission inventory, a four-minute demo path, and a real-versus-faked list |
| `feature-portfolio-decision.txt` | Each candidate restated as a user problem, scored on four axes, sorted into Now / Next / Not now, with accounts and payments as their own risk class, then one slice shipped end to end |

**What that cost, stated plainly:** the original fragments are not reproduced anywhere in this folder. A
reader who wants to know what was wrong with them gets the audit's description instead of the text, and
the text itself survives only in git history. That was a deliberate trade, made by the repository owner
on 2026-10-23, in exchange for a folder where nothing you open is a half-formed note.

The seven files that were always documents are untouched.

**The audit is separate and unchanged:** [`AUDIT.md`](AUDIT.md) records seven findings in the long
files — three unsuperseded constitutions, an instruction that cannot be followed, scope with no stopping
condition, four safety rules the library now forbids, "production-ready" defined as "the build passed",
missing provenance, and this README's own former habit of calling chat turns "prompts".
