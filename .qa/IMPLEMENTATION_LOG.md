<!-- not-a-prompt -->

# Implementation log — QA-P05

**Cycle:** 2.28.2
**Prompt:** `04-process/testing-qa/P05-Implementation/P05-Implementation.md`
**Inputs:** `.qa/GAPS.md` (G-01…G-07), `.qa/TEST_STRATEGY.md` (§3 order, §6 design decision)
**Baseline commit:** `720687c`
**Status of this document:** records work that was run locally on the date shown. Nothing here was executed by another agent or by CI.

## 1. Scope actually implemented

The strategy named three R1 behaviours to pin and four R2/R3 rules that existed but had no
fixture. Both halves were implemented; no other validator rule was touched.

| # | Gap | Change in `scripts/validate_library.py` | New authority |
|---|-----|------------------------------------------|---------------|
| 1 | G-01 — plain `TODO:` / `FIXME:` were invisible | New module-level `PLACEHOLDER_MARKER` regex replacing the literal-token list | — |
| 2 | G-02 — every placeholder hit was a warning | Marker hits, `lorem ipsum`, and `<insert` now append to `errors` with `file:line` | build-failing |
| 3 | G-03 — an empty required section satisfied the required-section rule | Empty required section on a non-skeleton prompt is now an error; other empty sections stay warnings | build-failing |
| 4 | G-04 — body-size overclaim had no fixture | Fixture only; rule unchanged | now pinned |
| 5 | G-05 — duplicate identifier had no fixture | Fixture only; rule unchanged | now pinned |
| 6 | G-06 — broken relative link had no fixture | Fixture only; rule unchanged | now pinned |
| 7 | G-07 — input/placeholder agreement had no fixture | Two fixtures (undeclared placeholder = error; declared-but-unused = warning); rules unchanged | now pinned |

`check()` remains the only public entry point for these rules. No new named functions were added,
deliberately: the strategy's §5 lists `check()`-level fixtures as the contract, and splitting the
document rules into separate callables would create a second path that the gate does not exercise.

## 2. Deviation from the strategy, and why

`TEST_STRATEGY.md` §6 proposed a word-boundary token scan for G-01. Before writing it, the scan was
measured against the live corpus: seven operational prompts legitimately discuss `TODO` as a
concept (for example `02-engineering/feature-completion/P02-Layer-Map/P02-Layer-Gap-Map.md:52`,
"a component file with a TODO is not an interface"). Word-boundary matching would have failed the
build on correct prompts.

Shipped rule instead keys on the marker form — a token that opens a line, optionally bulleted,
either bracketed or followed by `:`/`-`/`—`:

```python
PLACEHOLDER_MARKER = re.compile(
    r"(?im)^[ \t]*(?:[-*+]\s*)?"
    r"(?:\[\s*(?:TODO|FIXME|TBD|XXX)\b[^\]\n]*\]"      # [TODO], [TODO: finish this]
    r"|(?:TODO|FIXME|TBD|XXX)\s*[:\-\u2014])"          # TODO:, FIXME - ...
)
```

Fenced code blocks are **not** stripped. That was checked rather than assumed: no prompt in the
corpus contains a fenced `TODO`-style line, so stripping would add untested complexity for no
measured gain.

### Correction found while writing fixtures

The first version of the regex required punctuation after a bracketed token, which silently
dropped `[TODO] finish the handover` — a form the pre-2.28.2 literal scan *did* catch. The
fixture "the bracketed markdown-checkbox form is still caught" failed on the first run, the regex
gained the bracket branch above, and the case now passes. Recorded here because it is a real
example of the fixtures catching a defect in the fix itself, not of them confirming it.

## 3. Corpus re-measurement after the change

| Check | Result |
|-------|--------|
| Marker hits across every prompt-shaped document (364 in the tree plus `_meta/prompt-template.md`) | 0 |
| Empty required sections introduced | 0 |
| Validator errors | 0 |
| `check_all.py` | All gates passed |
| `test_validator.py` | 44/44 (was 32) |

Zero hits is the expected result: the corpus was clean of unfinished markers before the rule
became blocking. The rule's value is that it stays clean, which the fixtures now enforce.

## 4. Files changed

| File | Change |
|------|--------|
| `scripts/validate_library.py` | `PLACEHOLDER_MARKER` added; placeholder findings promoted to errors with line numbers; empty-required-section logic promoted to error |
| `scripts/test_validator.py` | `prompt_messages()` helper added; 12 whole-document cases added; total 32 → 44 |
| `.qa/IMPLEMENTATION_LOG.md` | this file |
| `.qa/VALIDATION.md` | P06 results |
| `PROJECT-STATUS.md`, `_meta/publication-checklist.md` | file total 480 → 482 (the two `.qa` documents added by P03/P04) |

## 5. Deliberately not done

- **No workflow change.** No GitHub Actions step has ever executed in this repository
  (`steps: 0`, billing not enabled), so a workflow-level gate would claim enforcement that does not
  exist. Everything above is enforced by `scripts/check_all.py`, which the record says is how this
  repository has always been validated.
- **No new documentation of the validator's behaviour beyond these two `.qa` records.** The
  repository already describes the rules; the gap was authority and fixtures, not prose.
- **No fixture for the README/PROJECT-STATUS count agreement.** Those checks each read the real
  repository root, so a fixture would assert against live files and break on every legitimate
  count change. They are covered by `check_all.py` on the real tree instead.

## 6. Evidence status

| Claim | Status |
|-------|--------|
| Validator and self-tests behave as described | **verified** — commands run locally in this cycle, output in §3 |
| Seven prompts legitimately mention `TODO` | **verified** — grep output, paths recorded in §2 |
| Zero corpus marker hits | **verified** — scan over `load(ROOT)` |
| Fixtures catch regressions in the rules they pin | **verified** — mutation results in `.qa/VALIDATION.md` §3 |
| The rule is enforced in CI | **not claimed** — no CI step has ever run |
