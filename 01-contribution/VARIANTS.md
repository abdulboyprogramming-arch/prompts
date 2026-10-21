<!-- not-a-prompt -->

# Contribution Variants — why three near-identical systems exist, and what keeps them honest

**Status:** decision record · **Date:** 2026-10-20 · **Backlog:** #100

---

## The measurement that raised the question

`scripts/find_overlaps.py --metric combined` ranks the `01-contribution` parallel variants as the most similar prompts in the entire library:

| Pair | Shingle | Vocabulary | Structure | Combined |
|---|---:|---:|---:|---:|
| `packages-libraries/P07` ↔ `web3/general/P07` | 0.06 | 0.68 | 1.00 | **0.68** |
| `packages-libraries/P03` ↔ `web3/general/P03` | 0.11 | 0.68 | 1.00 | **0.68** |
| `web/general/P07` ↔ `web3/general/P07` | 0.11 | 0.66 | 1.00 | **0.63** |

Three systems — `web/general/`, `web3/general/`, `packages-libraries/` — each hold eight skeleton stages with the same sequence, the same artifact names, and the same structure, differing mainly in nouns. A shingle-only detector reported 0.06–0.18 and made them look unremarkable. They are the clearest duplication in the repository, and until 2.19.0 nobody had measured it.

## The options

| Option | Cost | Consequence |
|---|---|---|
| **Delete two of the three**, keep one parameterised sequence | Low | Loses the domain-specific judgement that is the only reason to have three; invalidates 16 existing identifiers that other files reference |
| **Promote all three to operational** | Very high (24 prompts) | Triples the maintenance surface of the least-used folder while `02-engineering/backend` still has seven skeletons |
| **Keep three, and make the differences explicit and enforceable** | Medium | Preserves domain judgement, removes the ambiguity about which one to use, and gives each file a defensible reason to exist |

**Decision: the third option.** The three systems are kept, and this file is the contract between them.

## The rule the three systems now obey

> **Any stage that appears in more than one variant must state, in its own text, what is different about it in this domain.** A stage that cannot state a difference is a duplicate and should be deleted rather than maintained three times.

The differences are real and they are axes, not adjectives:

| Axis | `web/general` | `web3/general` | `packages-libraries` |
|---|---|---|---|
| Primary risk | UX regression, accessibility, layout | **Irreversible on-chain state, funds** | **Breaking downstream consumers** |
| Definition of "done" | Works in browsers, passes a11y checks | Invariants hold, no privileged path widened | Versioned, documented, no API break |
| Evidence that convinces a maintainer | Screenshots, recordings, cross-browser runs | Test coverage plus adversarial review and gas reasoning | Compatibility matrix, changelog, deprecation path |
| Approval model | Normal review | Explicit human approval for anything that moves value | Maintainer-defined version policy |
| Characteristic failure | Works on the author's browser | Works in the test suite, drains the contract | Works here, breaks a consumer's build |

## Current state, honestly

These are skeletons. The differentiation above is **stated in the READMEs and largely absent from the stage files**, which is why the combined similarity sits at 0.63–0.68 rather than something lower. Two things follow:

1. **They stay `skeleton`.** A system that cannot distinguish its stages is not ready to be called operational, whatever its prose says.
2. **The next person to touch them works one stage across all three**, not one system start to finish. That is the ordering that produces a real difference: pick `P06 Validation`, write web3's invariant checks and packages' compatibility matrix, and the web variant's cross-browser evidence — then the three files stop being the same file.

Recorded as backlog #107: *differentiate the 18 overlapping stages, one stage across all three variants per pass*. It is deliberately not a bulk rewrite, because a bulk rewrite of three systems by one author at one time would produce the same text again with different nouns.

## What this record prevents

- **A future agent "cleaning up duplication" by deleting two systems**, without noticing that the risk model and the approval model differ.
- **A future agent promoting all three at once** to make the folder look mature, adding 24 operational prompts whose content is one prompt repeated.
- **The duplicate detector being silenced** by raising a threshold instead of answering the question it asked.

## How to check the rule still holds

```bash
python3 scripts/find_overlaps.py --metric combined --top 6
```

If a pair inside `01-contribution` falls below 0.40, the differentiation work landed. If a pair *inside a single system* rises above 0.60, two stages of one system have collapsed into each other and one of them should go.

## Related

- [`README.md`](README.md) — which system to choose.
- [`_meta/ROADMAP-AND-BACKLOG.md`](../_meta/ROADMAP-AND-BACKLOG.md) #100, #107.
- `scripts/find_overlaps.py` — the measurement, with the limits of the lexical method documented in the module.
