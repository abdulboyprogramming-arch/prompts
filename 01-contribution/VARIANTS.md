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

## Pass 1 — `P06 Validation`, and why the metric barely moved

The method below was applied once, at v2.22.0, to the stage where the three domains diverge most. All three files were rewritten from outline to `operational`, each with its own evidence standard:

| Variant | What validation *is* here | The evidence that convinces a maintainer |
|---|---|---|
| `web/general` | The change works in engines, viewports, and input methods the author did not use | A screenshot at a named browser and width, or a passing cross-browser job |
| `web3/general` | The invariants hold when someone tries to break them | A violating case per invariant, an access-control matrix, a fork test pinned to a block |
| `packages-libraries` | The published interface did not break a consumer's build | A surface diff against the released version, an install of the artifact in a clean environment |

**The measurement, honestly:**

| Pair | Before (shingle / vocab) | After (shingle / vocab) |
|---|---|---|
| `web` ↔ `web3` | 0.03 / 0.28 | 0.00 / 0.23 |
| `web` ↔ `pkg` | 0.11 / 0.22 | 0.01 / 0.27 |
| `web3` ↔ `pkg` | 0.03 / 0.20 | 0.00 / 0.22 |

Vocabulary overlap barely changed, and one pair rose. That is not a failure of the work; it is a limitation of the instrument, and it has to be stated:

- **The `P06` outlines were two paragraphs each.** Short files have little vocabulary to overlap, so the 0.63–0.68 figures at the top of this record belong almost entirely to the longer stages (`P03`, `P07`), not to `P06`.
- **Length dilutes the metric.** Rewriting an outline into a developed prompt adds domain words and multiplies the denominator; a similarity score can fall because a file grew, not because two files diverged.
- **The differentiation here is a different evidence standard**, and no lexical metric can see the difference between "run the tests" and "a violating case per invariant". A reviewer or a maintainer can.

So the honest claim for this pass is the one a reviewer can check by reading: the three files now ask for different evidence, in different words, with different failure handling. The duplicate detector stays at its bar and remains useful for the case it was built for — a file copied and renamed.

## Current state, honestly

Seven of eight stages in each system are still outlines, and the combined similarity at the top of this record is unchanged because the files that produce it (`P03`, `P07`) have not been through a pass yet. Two things follow:## Current state, honestly

Seven of eight stages in each system are still outlines. The differentiation above is **stated in the READMEs and, for `P06` only, present in the stage files**, which is why the remaining combined similarity sits at 0.63–0.68 rather than something lower. Two things follow:

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
