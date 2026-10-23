<!-- not-a-prompt -->

# Rewrites — the short archive prompts, said properly

**What this folder is:** the clear statement of what four short, ungrammatical, or fragmentary requests
in this archive were actually asking for. Each rewrite keeps the original verbatim, explains what it was
trying to say, names why the original does not work as a prompt, and then gives a structured version
that could be run.

**What this folder is not:** part of the library. These are archive material. They carry no
`**Identifier:**` metadata, they are not counted as prompts, and they are not validated beyond being
readable Markdown. Where a current prompt covers the same work — and for three of the four it does —
that prompt is the one to run, and the rewrite says so.

**The originals are untouched.** All twelve `.txt` files in the parent folder are byte-identical to
what was archived. That is deliberate: the value of this folder is the distance between what was asked
and what the library became, and editing the "before" would delete the measurement.

---

## The four

| # | Original | Size | What it was trying to say | Rewritten |
|---|---|---|---|---|
| 01 | `Format dot md file.txt` | 133 B, one sentence | make the Markdown consistent without changing what it says | [`01-format-markdown.md`](01-format-markdown.md) |
| 02 | `process3(chat1).txt` | 67 B, one sentence | take me from "it runs here" to "someone else can open it at a URL" | [`02-see-it-running.md`](02-see-it-running.md) |
| 03 | `process4(chat1).txt` | 315 B, one paragraph | I am in a hackathon and I do not know what must be submitted, by when, or what to prepare | [`03-hackathon-submission.md`](03-hackathon-submission.md) |
| 04 | `process7(chat2).txt` | 410 B, one paragraph | the product feels thin; tell me which of these capabilities to build and in what order | [`04-feature-portfolio.md`](04-feature-portfolio.md) |

## The pattern in all four

Every one of them has the same shape of defect, and it is worth naming once because it is the thing a
first-time prompt writer does not see:

| What was written | What a model receives | What is missing |
|---|---|---|
| an **adjective** ("properly", "clean", "well presented", "as many as possible") | no standard to meet | a checkable rule |
| a **noun with no antecedent** ("it", "this software") | a guess | an input |
| a **list with no order** (eleven capabilities in one sentence) | an arbitrary sequence | a priority and a stopping condition |
| a **request with no state** ("what's next") | a generic answer | where things stand now |
| **five questions in one paragraph** | an answer to whichever one the model finds most interesting | one question, or a numbered set |

None of these is a grammar problem in the ordinary sense. The sentences are short and their *intent* is
perfectly clear to a human reader, because a human supplies the missing state from context. A model
cannot, and it does not say so — it fills the gap confidently, which is worse than failing.

That is why the rewrites are longer than the originals. The length is not padding: it is the context
that was in the writer's head and never made it onto the page.

## How to use these

- **As a model for your own requests.** The "what changed, phrase by phrase" table at the end of each
  rewrite shows the actual transformation, sentence by sentence.
- **As an entry point.** Each rewrite ends with the current library prompt that supersedes it
  (`DOC-P07`, `DEPLOY-01`, `HACK-01`, the feature-design system). Start there for real work.
- **Not as validated prompts.** Nothing in this folder has been run against a fixture. The library's
  own rule — a prompt is `operational` after recorded runs, not after good drafting — applies here too,
  which is exactly why these are filed as archive.

## Where the two genuine gaps are

Two of the four have **no current prompt that covers them**, and both are named rather than filled:

1. **A mechanical Markdown formatting pass** — `DOC-P07` publishes documentation, the validator checks
   links and structure, but nothing performs "presentation only, no prose changes" over an existing
   tree with a batch-and-revert protocol.
2. **Deciding between candidate features** — `feature-design-suggestion` designs a feature once it has
   been chosen, and its stages are still skeletons. Nothing decides *which* candidates earn a place.

Both are recorded in the parent [audit](../AUDIT.md) and are candidates for the backlog, not additions
made on the strength of a good draft.
