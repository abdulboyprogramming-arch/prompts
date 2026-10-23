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
| `markdown-formatting-pass.txt` | **Rewritten 2026-10-23** — was `Format dot md file.txt`, one sentence |
| `deployment-to-a-url.txt` | **Rewritten 2026-10-23** — was `process3(chat1).txt`, seven words |
| `hackathon-submission.txt` | **Rewritten 2026-10-23** — was `process4(chat1).txt`, five questions |
| `feature-portfolio-decision.txt` | **Rewritten 2026-10-23** — was `process7(chat2).txt`, eleven wants |

## What was replaced on 2026-10-23

Four files in this folder were not prompts. They were fragments — a sentence, a paragraph, seven words —
that only made sense inside a conversation that has not survived. They have been **replaced in place**
with prompts that say the same thing properly, and the fragments are gone rather than kept beside their
replacements.

| Was | Was made of | Is now |
|---|---|---|
| `Format dot md file.txt` | *"i need you to properly format and organize the content of all .md file…"* — 133 bytes | `markdown-formatting-pass.txt`: a presentation-only pass with a measured baseline, an agreed rule set, batches of ten revertible commits, and the rule that **a file you formatted and a file you fixed are different claims** |
| `process3(chat1).txt` | *"how will i see it"* — 67 bytes, and "it" is named nowhere | `deployment-to-a-url.txt`: state, audience and spend limit as inputs; the truth about the build established first; names-only secrets; an end-to-end check from outside the machine; an exercised rollback |
| `process4(chat1).txt` | 315 bytes, five questions in one paragraph | `hackathon-submission.txt`: rules before advice, a backwards absolute-time timeline, a submission inventory, a four-minute demo path, and a real-versus-faked list |
| `process7(chat2).txt` | 410 bytes, eleven capabilities, no order and no stopping condition | `feature-portfolio-decision.txt`: restate each candidate as a user problem, score on four axes, sort into Now / Next / Not now, treat accounts and payments as their own risk class, then ship one slice end to end |

**What that cost, stated plainly:** the before-and-after is gone. Anyone reading this folder now sees
four competent prompts and cannot tell what they replaced, and the original wording survives only in git
history and in the audit's descriptions of it. That was a deliberate trade, made by the repository owner
on 2026-10-23, in exchange for a folder where every file is worth reading. The alternative — keeping the
fragments beside their replacements in a separate folder — was tried first and rejected as clutter.

The seven files that were always prompts or documents are untouched.

**The audit is separate and unchanged:** [`AUDIT.md`](AUDIT.md) records seven findings in the long
files — three unsuperseded constitutions, an instruction that cannot be followed, scope with no stopping
condition, four safety rules the library now forbids, "production-ready" defined as "the build passed",
missing provenance, and this README's own former habit of calling chat turns "prompts".
