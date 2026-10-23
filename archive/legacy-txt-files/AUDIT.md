<!-- not-a-prompt -->

# Audit of the archive — what needs correction, and what does not

**Date:** 2026-10-23
**Scope:** the twelve `.txt` files in this folder, read in full for the first time since they were
archived. The four short ones are rewritten in [`rewritten/`](rewritten/README.md); this file records
what is wrong with the rest.

**Posture:** these files are **provenance, not guidance**. Nothing here is edited. The corrections below
are notes about the record, kept so that a reader in two years can tell what these documents were, what
they got wrong, and which parts were good enough to survive into the library.

---

## 1. What is genuinely good, before the criticism

Three of these files are better than most prompt material written today, and it would be dishonest to
file them under "legacy" without saying so:

| File | What it does well |
|---|---|
| `issue creation.txt` | deduplicates against existing issues before creating any; classifies findings into eight types; states that *"not every finding should become an issue"*; forbids modifying application code |
| `code changes(changelog & commit).txt` | inspects git state before touching it; forbids force-pushing shared history; forbids artificial changes and unnecessary documentation; separates distinct engineering phases into distinct commits |
| `scaffold completion.txt` | has an explicit *"absolute non-assumption rule"* — do not trust a previous agent's claim that the code is scaffolded, verify it. That is the exact lesson the library later built its evidence rules on |

The defects below are real, but they sit on top of a structure that had the right instincts.

## 2. Findings, by consequence

### F-01 — Three versions of the same constitution, none marked superseded, ~270 KB

| File | Self-described version | Size |
|---|---|---|
| `process1(chat1).txt` | ASEOS **v2.0** | 93 KB |
| `process5(chat2).txt` | ASEOS **v3.0** | 92 KB |
| `scaffold completion.txt` | unversioned in-file; called v4.0 by `README.md` | 90 KB |

**Consequence:** there is no way for a reader to tell which one governed, which superseded which, or
whether v3.0 was ever used. The three overlap heavily and contradict each other in places (see F-04).

**Correction applied:** the version table above, and this note. The files stay as they are; the
history of an idea includes its drafts.

### F-02 — An instruction that cannot be followed, and therefore guarantees a false claim

`process1(chat1).txt:1`:

> ENSURE YOU READ EVERY FILE LINE BY LINE ONE BY ONE AFTER EACH OTHER

and `scaffold completion.txt:2797` describes the codebase as *"more than 1,000 files"*.

**Consequence:** no executor reads 1,000 files line by line. An agent given this instruction either
skims and reports that it read everything — a lie produced by the prompt, not by the model's character
— or spends the entire budget on one file type. This is the single most damaging instruction in the
archive, because it makes the completion report untrustworthy at the root.

**What the library does instead:** `scaffold completion`'s own *"do not treat one successful build as
proof"* rule survived into the evidence rules; the line-by-line demand did not. A modern equivalent
asks for **coverage accounting** — which files were read, which were skipped, and why — because that is
checkable.

### F-03 — Scope instructions with no stopping condition

| Location | Instruction |
|---|---|
| `process1(chat1).txt:1` | *"ADDITIONALS (AS MANY AS POSSIBLE)"* |
| `process6(chat2).txt:31` | *"Never wait for feature requests. / Invent the future."* |
| `process7(chat2).txt:1` | *"Add many more features… as many as possible… all possible features… that ever exist in the world"* |
| `scaffold completion.txt:3464` | *"Repeat it until the system reaches a stable production-ready state."* |

**Consequence:** none of these can terminate. A run either stops arbitrarily and claims completeness, or
never stops. `process7` is rewritten in [`rewritten/04-feature-portfolio.md`](rewritten/04-feature-portfolio.md)
as a portfolio decision with an explicit *not now* list, because the ambition was reasonable and only
the instruction was unusable.

### F-04 — Safety instructions that the library now forbids

| Location | Instruction | Why it is now wrong |
|---|---|---|
| `scaffold completion.txt:307` | *"Do not ask permission for routine work that is already logically required by an approved objective."* | the definition of "routine" is the executor's, and that is how a read-only task becomes a deploy |
| `scaffold completion.txt:4447` | *"DO NOT ASK ME TO DO WORK YOU CAN DO YOURSELF."* | correct as an anti-helplessness rule, wrong as an absolute: some work is the human's precisely because it is irreversible |
| `code changes(…).txt:392` | *"PUSH TO MAIN"* as a numbered step | direct pushes to `main` are now blocked by a ruleset; the work is a pull request |
| `issue creation.txt` §6–§10 | creates GitHub issues with **no approval step** between "classify the findings" and "create the issues" | issues are public and permanent; the prompt shows the user nothing before writing them |

**What the library does instead:** `00-core/safety-and-security/ACTION-CATEGORIES.md` splits actions
into four categories, and only A and B proceed without approval. The approval gate is not distrust of
the agent; it is the observation that *"routine"* and *"irreversible"* are different words.

**Correction applied:** recorded here. The one change worth making to practice — and it is a change to
the current prompts, not the archive — is that `issue creation`'s workflow would be safe today only with
a "show the list, get a yes, then create" step inserted between §8 and §10.

### F-05 — "Production-ready" accepted as an end state, defined as "the build passes"

`scaffold completion.txt` uses the phrase fourteen times, and its own prohibition list includes
*"Treat one successful build as proof that the system is production-ready"* — then its §11 is titled
*"PRODUCTION-READY CODE REQUIREMENT"* and its closing instruction is *"Continue until the entire system
reaches a stable, genuinely production-ready state."*

**Consequence:** a self-contradiction. The document knows the trap and then sets it as the goal. Nothing
in it defines what would make the claim true, so the claim is whatever the executor says at the end.

**What the library does instead:** `_meta/quality-standards.md` and every operational prompt require a
**definition of done with a checkable condition**, and the repository's own README refuses to call
anything production-ready on the strength of a passing build.

### F-06 — Provenance is missing on the two most specific files

`process7(chat2).txt` ends with a copy-paste marker, `[ PROMPT FROM PROCESS 5]`, and both `process4` and
`process7` refer to *"it"* and *"this software"* without ever naming the project. `scaffold completion.txt`
quotes *"`{{PROJECT_NAME}}`"* — a template variable that was never filled in.

**Consequence:** these are fragments of a conversation about a specific, unnamed project. Kept as
history that is fine; the risk is a reader treating them as general-purpose prompts and running them
against an unrelated repository.

**Correction applied:** `README.md` in this folder now says which three files are conversation turns
rather than prompts.

### F-07 — The folder's own README described all twelve as "prompts"

`process3`, `process4` and `process7` are single turns in a chat: `process3` is seven words with no
antecedent for *"it"*. Calling them prompts is the same class of error the library spends its time
correcting — a label that flatters the content.

**Correction applied:** `README.md` now distinguishes turns from prompts, and the table says which is
which.

## 3. What I did not change, and why

- **The twelve `.txt` files are byte-identical to what was archived.** Editing them would destroy the
  only thing they are kept for: the difference between what was asked and what the library became.
- **No new library prompts were created from this audit.** The four rewrites live in `rewritten/` and
  are marked as archive material. Where a current prompt covers the work, the rewrite points at it;
  where nothing does (feature portfolio, Markdown hygiene), the gap is named rather than filled with an
  unvalidated prompt — this repository's rule is that a prompt enters the library with fixture runs, not
  with good intentions.
- **`scaffold completion.txt` was not split or trimmed.** At 90 KB it is not a prompt, it is a constitution.
  Splitting it would create the illusion of four usable artifacts out of one unvalidated document.

## 4. The one thing worth doing next

`issue creation.txt` is the most reusable document in this folder and the one closest to being safe
today. It lacks exactly one step: **propose the issue list, show it, wait for a yes, then create.**
That is a ten-line change, and it is the difference between a helpful agent and one that fills a public
tracker with duplicates it has decided are real.

Recorded here rather than implemented, because a prompt change requires a fixture run — the same rule
this file exists to illustrate.
