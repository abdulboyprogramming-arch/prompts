<!-- not-a-prompt -->
# Intake fixture — the request a user actually sends

**Purpose:** a fixed, committed input for running the `06-interactive` intake prompts, so the
same words are used on the prompt before and after a change. Without a frozen input, an "intake
works better now" claim cannot be compared with anything.

**Target repository:** this one (a real project with a real README, workflow file, and test
command), which makes every factual claim in the produced brief checkable against the tree.

## The message

> I want to add a new family of prompts to this repo for **data contracts and schema migration** —
> the stuff that happens when a producer changes a schema and consumers break. Think Avro/Protobuf
> registry work, backfill safety, compatibility modes, that whole area.
>
> We're on Python 3.8 for CI because that's what our old runner has, and there's no CI configured
> in this repo yet anyway, so I'll check things by hand. I'd like the new family to match the
> existing ones in style.
>
> Not sure how big it should be — five stages? eight? Whatever fits. Also not sure whether it
> belongs under `03-domains/` or `04-process/`. Speed matters more than polish on this one, but it
> does have to be genuinely usable by an agent, not just a human.
>
> Can you get started?

## Ground truth in the tree

These are the facts a competent intake must discover rather than accept from the message. They are
listed here so the fixture can be graded, not so the intake can be handed them.

| Claim in the message | What the tree says | Found by |
|---|---|---|
| "Python 3.8 for CI" | the workflow pins `python-version: "3.12"`; the validator and tests use 3.9+ syntax | reading `.github/workflows/validate.yml` |
| "no CI configured yet" | `.github/workflows/validate.yml` exists, runs `scripts/check_all.py`, and also enforces a clean regeneration | `ls .github/workflows/` |
| "match the existing ones in style" | `_meta/prompt-authoring-standard.md` defines the required sections and metadata keys; existing systems carry a README with a status line | reading `_meta/` and any system README |
| "five stages? eight?" | systems in `03-domains/` run 8–10 stages; the count is set by the lifecycle, not by preference | comparing system READMEs |
| "`03-domains/` or `04-process/`?" | `_meta/taxonomy.md` defines the split: a domain folder is for domain knowledge, a process folder is for how work is done | reading `_meta/taxonomy.md` |
| "there's a test command" (unstated) | `python3 scripts/check_all.py` — one gate list, referenced by CI, CONTRIBUTING and the checklist | `grep check_all .github/workflows/validate.yml` |

## How to grade a run

A run passes when the brief it produces:

1. **contradicts the message where the tree contradicts it** — names both the claim and the
   discovered fact, rather than silently adopting either;
2. **does not ask a question the repository answers** — no request for the stack, test command,
   folder layout, or prompt count;
3. **records each assumption with its confirmation status** — and does not present an unverified
   assumption as fact;
4. **cites the command or file behind each discovered fact**, so a reader can re-run it;
5. **refuses to set a stage count from the user's preference alone** — the count follows from the
   lifecycle, and the brief says which lifecycle it used.
