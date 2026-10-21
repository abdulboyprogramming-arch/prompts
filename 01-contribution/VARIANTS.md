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

**The measurement, honestly** — measured with the tools' own functions against the files at `060ffe5` and at the pass:

| Pair | Before (shr / voc / str / **combined**) | After |
|---|---|---|
| `web` ↔ `web3` | 0.03 / 0.44 / 0.60 / **0.26** | 0.00 / 0.38 / 0.83 / **0.32** |
| `web` ↔ `pkg` | 0.11 / 0.47 / 0.60 / **0.28** | 0.01 / 0.43 / 0.83 / **0.36** |
| `web3` ↔ `pkg` | 0.03 / 0.44 / 0.60 / **0.27** | 0.00 / 0.37 / 0.83 / **0.31** |

Combined similarity **rose** on all three pairs, from 0.26–0.28 to 0.31–0.36, and the reason is worth more than the direction:

- **Vocabulary fell** (0.44–0.47 → 0.37–0.43). The three files do share less language after the pass.
- **Structure rose** (0.60 → 0.83), because an outline has a handful of headings and a developed prompt has the ten the standard requires. The metric multiplies the two, so the structural term swamped a real lexical gain.
- **The differentiation here is a different evidence standard**, and no lexical metric can see the difference between "run the tests" and "a violating case per invariant". A reviewer or a maintainer can.

So the honest claim for this pass is the one a reviewer can check by reading: the three files now ask for different evidence, in different words, with different failure handling. The duplicate detector stays at its bar and remains useful for the case it was built for — a file copied and renamed.

**Correction to the first version of this section.** It reported vocabulary as 0.20–0.28 before and 0.20–0.22 after, and concluded that the metric "barely moved". Those figures came from a *different vocabulary function* than the one `find_overlaps.py` uses for the pair table at the top of this record: Jaccard over word sets rather than containment, so the numbers were not comparable with the 0.63–0.68 rows they sat under. Recomputed with the tool's own functions on both sides, vocabulary fell by about 0.06 and the combined score rose, as the table above shows. The conclusion survives — the instrument could not confirm this pass — and the comparison is now apples to apples.

## Pass 2 — `P03 Selection`, where the metric finally moves

`P03` was the harder pass and the more informative one. `P06` asked the three variants to prove different things about a finished change; `P03` asks them to **choose** differently, and the three answers had to be different instruments rather than different adjectives:

| Variant | How a candidate is selected | The sentence that disqualifies a candidate |
|---|---|---|
| `web/general` | By proof strength: the claim must be assertable at a named viewport and engine, and anything visible needs a named owner of the design decision | *No owner for the decision* — a visual change with nobody accountable for it is a design argument, not a contribution |
| `web3/general` | By **reversibility tier** — who can undo it if it is wrong — with tier 2 and 3 gated behind recorded maintainer approval **before** code exists | *No approval, no tier 2 or 3 selection* — consent is not inferred from an old issue |
| `packages-libraries` | By **surface cost ledger**: symbols added, behaviour changed silently, dependencies inherited, and the support burden the maintainer carries forever | *Adds a promise you must keep* — public API ranks last among equals |

Each stage's own text names the sibling it differs from and the characteristic failure it exists to catch: *picks a visible redesign and hands the maintainer an unauthorised design decision*; *submits a change to a value path described as a small fix*; *adds a convenience option the maintainer supports forever*.

**The measurement, for once, moved** — same functions, same method as the corrected pass-1 table:

| Pair | Before pass 2 (shr / voc / str / **combined**) | After pass 2 |
|---|---|---|
| `web` ↔ `web3` | 0.15 / 0.57 / 1.00 / **0.57** | 0.01 / 0.44 / 0.83 / **0.36** |
| `web` ↔ `pkg` | 0.00 / 0.54 / 1.00 / **0.54** | 0.02 / 0.45 / 0.83 / **0.38** |
| `web3` ↔ `pkg` | 0.11 / 0.68 / 1.00 / **0.68** | 0.01 / 0.44 / 0.83 / **0.36** |

Combined similarity fell from 0.54–0.68 to 0.36–0.38 across all three pairs, and every component moved the same way: structure broke from identical to 0.83, vocabulary from 0.54–0.68 to 0.44–0.45, shingle overlap to almost nothing. Unlike `P06`, this is not an artefact of length — the files grew, and the denominator grew with them, but the intersection shrank in absolute terms because three selection instruments share almost no sentences.

That contrast is the useful result of doing two passes. **`P06` was content differentiation inside a shared skeleton, and the metric punished it for using the shared structure. `P03` replaced the skeleton itself, and the metric agreed.** A future pass can predict which reading it will get. If the three files keep the ten standard sections and differ only in what they ask inside them, structure stays at 1.00 and combined similarity stays near 0.6. The measurable drop requires the *procedure* to differ, not just the nouns.

## Pass 3 — `P07 PR`, where the three variants address three different readers

`P07` had the highest score in the library (0.63–0.68) and the clearest reason to exist three times over: each variant's pull request is read by someone deciding something different.

| Variant | What the PR is for | The reader's decision | What it leads with |
|---|---|---|---|
| `web/general` | A viewing instruction | "Does this behave correctly where I can see it?" | A numbered reproduction recipe and labelled media (engine, width, state) |
| `web3/general` | A risk disclosure | "What happens to the money if this is wrong?" | Four facts: state change, tier, undo path, worst outcome |
| `packages-libraries` | A release note and a semver argument | "Which release can this ship in, and what do I tell users?" | The verdict and the symbol that drives it, then a draft changelog entry |

The disqualifying sentences are correspondingly different: *a screenshot with no viewing instruction*, *risk buried below the fold*, *a PR that cannot be described to a consumer*.

**Measurement:** combined similarity fell from 0.63–0.68 to 0.32–0.35; vocabulary containment 0.63–0.68 → 0.38–0.42; structure 1.00 → 0.83; shingle to 0.01.

## Pass 4 — `P02 Discovery`, where the search happens in three different places

Discovery was the last pair above 0.55, and the pass made explicit something that had been implicit in all three outlines: **the same word covers three different search spaces.**

| Variant | Where the candidates come from | The instrument | Characteristic failure |
|---|---|---|---|
| `web/general` | The running application | A surface list walked at 320/768/widest, a keyboard pass, the tracker by label | A list of refactors with the broken screen unmentioned |
| `web3/general` | The trust boundary | A five-part map — privileged surface, value paths, external calls, price inputs, upgrade surface — then missing guards | Gas savings listed, unguarded privileged function missing |
| `packages-libraries` | The consumers | Downstream code search for wrappers, copies, and pins, plus a clean install per runtime | API improvements nobody asked for, with no witness |

Each records a different kind of evidence, because each has a different notion of proof: an observation at a named viewport; a boundary with a failure class; a witness in someone else's repository.

**Measurement:** combined similarity fell from 0.56–0.65 to 0.29–0.32; vocabulary containment 0.56–0.65 → 0.35–0.38; structure 1.00 → 0.83; shingle to 0.01.

## Current state, honestly

Four of six overlapping stages are through a pass in all three variants: `P02`, `P03`, `P06` and `P07`. Two stages remain — `P04 Planning` and `P05 Implementation` — and with them `P01` and `P08`, which sit at 0.15–0.46 combined. Those last two are the stages where the variants arguably should be similar, because planning a change and implementing it in a repository are close to the same job in any language. Two things follow:

1. **They stay `skeleton`.** A system that cannot distinguish its stages is not ready to be called operational, whatever its prose says.
2. **The next person to touch them works one stage across all three**, not one system start to finish. That is the ordering that produces a real difference: pick `P06 Validation`, write web3's invariant checks and packages' compatibility matrix, and the web variant's cross-browser evidence — then the three files stop being the same file.

Recorded as backlog #107: *differentiate the 18 overlapping stages, one stage across all three variants per pass*. It is deliberately not a bulk rewrite, because a bulk rewrite of three systems by one author at one time would produce the same text again with different nouns. **Progress: 4 of 6 passes done (12 of 18 stage files), 2 stages left.** Next is `P05` or `P04`; the remaining decision worth recording is whether `P01` and `P08` should be differentiated at all, since their similarity is already low and their content is genuinely the same job.

## What this record prevents

- **A future agent "cleaning up duplication" by deleting two systems**, without noticing that the risk model and the approval model differ.
- **A future agent promoting all three at once** to make the folder look mature, adding 24 operational prompts whose content is one prompt repeated.
- **The duplicate detector being silenced** by raising a threshold instead of answering the question it asked.

## How to check the rule still holds

```bash
python3 scripts/find_overlaps.py --metric combined --top 12
```

If a pair inside `01-contribution` falls below 0.40, the differentiation work landed for that stage — `P03` and `P06` are there. If a pair *inside a single system* rises above 0.60, two stages of one system have collapsed into each other and one of them should go. The bar is the same 0.40 the CI gate uses for a different purpose, and it is a floor for this work, not proof: the `P06` pass is the standing reminder that a metric can miss a real difference and that reading the files is still the primary instrument.

## Related

- [`README.md`](README.md) — which system to choose.
- [`_meta/ROADMAP-AND-BACKLOG.md`](../_meta/ROADMAP-AND-BACKLOG.md) #100, #107.
- `scripts/find_overlaps.py` — the measurement, with the limits of the lexical method documented in the module.
