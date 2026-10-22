<!-- not-a-prompt -->
# Gap Analysis — risk minus protection

**Produced by:** `QA-P03` v1.1.0
**Target:** `720687c` (main, 2.28.1)
**Inputs:** [`CURRENT_STATE.md`](CURRENT_STATE.md) (R1 map, measurements), [`QA_CONTEXT.md`](QA_CONTEXT.md) (risk map)
**Evaluator:** the author — author-run

---

## How each absence was confirmed

Two methods, both described so the claim can be re-run:

1. **Search.** `grep -n "broken\|duplicate identifier\|NOT_DECLARED\|overclaim" scripts/test_*.py` — the
   fixtures name their rules, so an absent string means an absent fixture.
2. **Probe.** A three-file throwaway tree (`tempfile.mkdtemp`) fed through
   `validate_library.load()` and `check()`, printing the errors and warnings returned. This is
   how a rule that exists but is mis-scoped shows up: it must fire on the probe and it does not.

Every gap below was confirmed by one of those, at `720687c`.

## Ranked gaps

| ID | Behaviour | Risk | Type | Protection now | Failure it allows | Confirmed by |
|---|---|---|---|---|---|---|
| **G-01** | An unfinished prompt is detected before it ships | **R1** | Enforcement + missing coverage | `plain TODO`/`FIXME` → **silent**; only `[TODO` (bracketed) matches | A prompt whose body says `TODO: finish this` passes every gate, labelled operational | probe: `TODO: finish this` → SILENT; `FIXME: later` → SILENT |
| **G-02** | The same, enforced | **R1** | Enforcement | every placeholder token is a **warning**, so `check_all.py` still prints *"All gates passed"* | `[TODO]`, `TBD` or `lorem ipsum` inside a prompt does not stop a release | probe: `[TODO: finish]` → FLAGGED as a warning; validator exit 0 |
| **G-03** | A prompt's required sections have content, not just headings | **R1** | False confidence | an empty `## 6. Verification` **satisfies** the required-section check (which matches the word anywhere) and only warns | A procedure with a blank verification section is labelled operational; the reader gets a section that tells them nothing | probe: empty Verification + Failure handling + Completion criteria → `errors: []`, three warnings |
| **G-04** | Per-prompt maturity claim matches body size | **R1** | Missing coverage | rule exists (`labelled 'operational' but body is only N chars`); **no fixture** | A rule that has never been tested can be broken by a refactor and nobody notices | `grep overclaim scripts/test_*.py` → no match; probe fires |
| **G-05** | Duplicate identifiers | R2 | Missing coverage | rule exists; **no fixture** | Two prompts answer to one id; links and dependency edges become ambiguous | probe fires; no fixture |
| **G-06** | Broken relative links | R2 | Missing coverage | rule exists; **no fixture** | A reader follows a dead end | probe fires; no fixture |
| **G-07** | Declared inputs match placeholders | R3 | Missing coverage | rule exists; **no fixture** for either direction (undeclared placeholder / declared-but-unused input) | Minor friction; the agent asks for a value it was not told it needed | probe fires; no fixture |

**Seven gaps, four at R1.** The three R1 enforcement gaps (G-01…G-03) share one root cause:
**the validator has the knowledge but not the authority**. Each of those rules exists, was
written deliberately, and can only warn. A warning does not stop `check_all.py`, and
`check_all.py` is the only gate this repository has ever had execute.

## The top three, in prose

**G-01 — the placeholder rule matches a bracket, not a word.** The tuple is
`("[TODO", "TBD", "lorem ipsum", "<insert")`. `[TODO` catches the markdown-checkbox form and
misses the most common form of all: `TODO:` written as prose, and `FIXME`, which is not in the
list at all. A prompt can be half-written in the most obvious way possible and the lint is
silent. This is the sharpest gap in the set because it defeats the library's central claim in
one line of text.

**G-02 — and when it does match, it only warns.** Even a bracketed `[TODO` cannot stop a
release. The rule was presumably left as a warning because TODOs are legitimate *inside fenced
code examples* — a prompt that shows a code template containing `TODO` is not unfinished. That
worry is real but it is already handled: the token check runs on `d.text`, and the surrounding
structure check strips fences with `strip_fences`. Whether the token check should too is the
design question the strategy stage has to answer.

**G-03 — a heading is not a section.** "A prompt labelled operational must have a verification
section" is enforced by searching for the substring `verification` anywhere in the body. A
heading supplies that substring. So the check passes, and the empty-section detector reports a
warning nobody reads. The reader is told the procedure has a verification step; it has a
heading.

## Deliberate non-gaps

| Area | Why it is not listed |
|---|---|
| The risk-class-A rule | Fixed and pinned last cycle (2.28.1, five fixtures). Re-checking it here would be double counting. |
| Counts in prose | `check_documented_counts` covers three phrasings with fixtures; the third was added after it was found missing. |
| Generated-file currency (catalog, gallery, task index, conformance, evidence page) | Each has a gate and `test_check_all.py` covers the restore-on-failure path. |
| Prompt *content* quality | Out of scope by `QA_CONTEXT.md` §6: that needs a second reader, and no amount of tooling in this repository substitutes for one. |
| Coverage percentage | Diagnostic by policy; no gap is defined by it. |
| The 78 skeletons having no tests | They are outlines by declaration. The gap would be a skeleton labelled operational, which is G-01/G-03. |

## Coverage limits

- Author-run, and the author wrote both the rules and the probes. The probe output is in this
  file so a second reader can re-run each line.
- Probes run against `load()`/`check()` in a temporary tree, not against the live repository.
  The live tree reports 0 errors and 0 warnings, which is what makes promoting G-01…G-03 safe
  today; it also means those rules are currently unexercised by the real corpus.
- Seven gaps is well inside the 12–15 cap; no grouping was needed.
