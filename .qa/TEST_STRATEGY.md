<!-- not-a-prompt -->
# Test Strategy — seven gaps, four at R1, ranked by what they let through

**Produced by:** `QA-P04` v1.1.0
**Target:** `720687c`
**Inputs:** [`GAPS.md`](GAPS.md), [`CURRENT_STATE.md`](CURRENT_STATE.md), [`QA_CONTEXT.md`](QA_CONTEXT.md)
**Time budget:** stated as 2–4 hours; used ~1.5 h. Author-run.

---

## 1. Level per gap

The repository's test convention is plain Python scripts with printable case lists — no
pytest, no fixtures framework. The plan fits it rather than replacing it: new cases go into
`scripts/test_validator.py`, which already owns the validator's rules.

| Gap | Level chosen | Why that level | Higher level rejected |
|---|---|---|---|
| G-01 unbracketed `TODO`/`FIXME` | unit, on `check()` over a temp tree | The rule is a text predicate; a three-file tree is the cheapest faithful setup | Integration with the real tree — a live tree cannot contain a deliberate TODO |
| G-02 tokens must block | unit, plus one assertion on the **severity** returned | Severity is the property under test, and it is only observable in the returned lists | Reading the code, which is what has been standing in for this test |
| G-03 empty required section | unit, on `check()` | Same | — |
| G-04 body-size overclaim | unit | Rule already exists; only a fixture is missing | — |
| G-05 duplicate identifier | unit, two-document tree | Requires two docs to collide | — |
| G-06 broken relative link | unit, one doc with a link | Link resolution is filesystem-relative | — |
| G-07 input/placeholder agreement | unit, both directions | Two rules in one function | — |

No integration or end-to-end level is proposed: there is no service boundary here, and the
repository has no second process to wire. That absence is recorded rather than solved —
`CURRENT_STATE.md` already notes that no end-to-end level exists.

## 2. Sequence

Ordered by the stage's own economics rule — cheapest test that reliably catches the failure —
and by risk:

1. **G-04, G-05, G-06, G-07 — fixtures for rules that already exist.** Four rules, ~40 lines
   of cases, no production change. These make the suite trustworthy before anything is added
   to it; a rule with no fixture is a rule a refactor can silently delete.
2. **G-01 and G-02 — the token scan.** Changes behaviour, so it goes second, after the
   existing rules are pinned.
3. **G-03 — empty required sections.** Changes severity, so it goes last, when every
   behaviour it could interact with is already covered by a fixture.

## 3. Test data strategy

- **Build the smallest tree that can express the failure.** A three-line helper writes one
  prompt file into `tempfile.mkdtemp()`; `load()` then reads it exactly as it reads the
  repository. No mocks, no monkeypatching, no shared fixture across cases.
- **No shared mutable state.** Each case gets its own directory and its own `load()`. The
  existing `build()` helper in `test_validator.py` already follows this and is reused.
- **Determinism.** No clock, no randomness, no network, no ordering dependence. The suite is
  already clean on every one of those signals (`CURRENT_STATE.md` §5) and the new cases keep it.
- **Severity is asserted, not implied.** A case that only checks "something was reported"
  would have passed for G-02 before the fix — that is precisely the false-confidence shape
  `CURRENT_STATE.md` §4 flagged. Every new case asserts which list the message landed in.

## 4. Flake policy

Unchanged from the existing suite, which has no flakes to manage: no `sleep`, no retries, no
`skip`/`xfail`, no time or network dependence. If a new case is intermittent it is deleted and
rewritten, not quarantined — a flaky check in a repository with no CI is worse than no check,
because nothing will ever surface it again.

## 5. Deliberate non-goals

| Not doing | Reason |
|---|---|
| Promoting every warning to an error | Empty non-required sections, extra H1s and optional metadata are style. Blocking on them would make the gate noisy, and a noisy gate gets bypassed. |
| A coverage target | Diagnostic by policy (`README.md`, coverage rule). |
| Extracting link/duplicate/overclaim checks into named functions | Tempting for testability, but it is a refactor of production code, which `QA-P05` forbids this cycle. `check()` is callable and returns the lists; that is enough. Worth doing next cycle with its own review. |
| Testing the CI workflow | It has never executed. Testing YAML would prove the file is well-formed, not that it runs. |
| Fence-aware token scanning | See §6 — decided against, on evidence. |

## 6. The design decision this stage got wrong, and the correction

**The plan said: scan the whole document and make the hit an error.** Before implementing,
searching the corpus for the unbracketed words showed why that plan would have failed on its
first run.

`grep -rniE "\b(TODO|FIXME|TBD|XXX)\b"` finds **seven legitimate mentions** in existing
operational prompts — sentences such as *"A component file with a TODO is not an interface"*
and *"No TODO in the diff lacks a log entry"*. A word-boundary scan promoted to an error would
have failed the build on the corpus that already exists, for prompts that are correct. The
plan's premise — that the token is rare enough to scan bluntly — was false, and the corpus
said so in one grep.

**The correction: key on the marker form, not the word.** A prompt that is unfinished writes a
marker — `TODO: fill this in`, `- FIXME: revisit`, `[TODO] —`. A prompt discussing the concept
writes the word inside a sentence. The rule now matches a token that *begins a line*
(optionally bulleted or bracketed) and is followed by a colon or dash:

```
^[ \t]*(?:[-*+]\s*)?\[(TODO|FIXME|TBD|XXX)\]?\s*[:\-—]
```

That pattern finds **0 hits across the 364 prompts** and catches every marker form the probe
tried. It is narrower than "any occurrence" and it is the narrower rule that is correct.

**Two things are deliberately not done.** Fences are not stripped: of the 364 prompts, zero
contain a fenced `TODO`, so strip-then-block would be a rule that cannot fire — the same
weakness as a rule that cannot fire at all, and the exemption can be added the first time a
legitimate case appears, with a fixture proving it. And the bracketed form `[TODO` stays in the
matcher, because it is the markdown-checkbox style the original rule was written for.

This is the sort of thing a second reader would settle in a minute, which is why the wrong
version of the plan is kept here rather than quietly replaced.

## 7. Measurable targets

| Target | Threshold | Basis |
|---|---|---|
| R1 behaviours with a fixture that fails when the rule breaks | **4 of 4** (B1, B2, B5, B6) plus the three promoted rules | `CURRENT_STATE.md` §3 |
| Gaps closed | 7 of 7 | `GAPS.md` |
| Suite runtime | **< 5 s** for `check_all.py` | 3.07 s measured; the target leaves room and still fits the 10-minute PR budget |
| New cases | ≥ 12 | one negative case per rule, plus severity assertions |
| Mutation survival | 0 of 5 sampled | `QA-P06` will re-prove by mutation, as it did last cycle |
