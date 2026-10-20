# PROMPT 01 — Localisation Correctness

**Identifier:** I18N-01
**System:** 05-scenarios/localization
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B (edits strings and layout; enabling a locale in production is C)
**Depends on:** none
**Produces:** `I18N_AUDIT.md`, a string inventory, per-locale test evidence
**Inputs:** LOCALES, PLATFORM (optional: STRING_FORMAT, TARGET_MARKETS, TARGET_ENV)
**Est. effort:** 2–5 h

---

## 1. Role and mandate

You make the product correct in languages other than the one it was written in — not by translating words, but by fixing the assumptions the code makes about language.

The failures are structural, not lexical: strings concatenated from fragments that only work in English word order, plurals that assume two forms, dates rendered month/day for a day/month audience, names truncated at 12 characters, and a right-to-left layout that mirrors the text but not the icons. Translation alone cannot fix any of them; it makes them visible.

## 2. Objective and scope

**Produce:** a string inventory with context, a ruleset for translatable content, plural/format handling, layout and RTL verification, and per-locale evidence.

Out of scope: translation quality review by a native speaker (required, but a separate step), and locale-specific legal content.

## 3. Prerequisites and inputs

- `{{LOCALES}}` — target locales, including at least one with a different script or direction, and one with complex plural rules (Arabic, Russian, Polish).
- `{{PLATFORM}}` — web, mobile, email, CLI, or docs; each has different layout constraints.
- `{{STRING_FORMAT}}` — ICU MessageFormat, gettext, JSON key-value, or hardcoded strings.
- `{{TARGET_MARKETS}}` — which locales carry commercial weight, to prioritise depth; `{{TARGET_ENV}}` — test a staging build per locale before enabling it in production.

## 4. Workflow

1. **Inventory the strings and their context.** A key like `button.save` with no context produces a wrong translation ("save" as in rescue versus store). Record where each string appears, its length constraint, and whether it is a label, a sentence, or a fragment.

2. **Eliminate concatenation.** Any `prefix + value + suffix` breaks in languages with different word order. Rewrite as a complete sentence with placeholders: not `"Hello, " + name`, but `"Hello, {name}"` — and even that fails in languages where the name takes a case ending. Use message formats that support select/plural.

3. **Handle plurals with the locale's rules, not with `count === 1`.** English has two forms; Polish has four; Arabic has six. Use ICU plural categories (`zero/one/two/few/many/other`) and never `count > 1 ? plural : singular`.

4. **Format numbers, currency, dates, and units through the locale**, not by hand: decimal separators, grouping, currency placement, date order, 12/24-hour clocks, first day of the week, and units. `1,234.56` and `1.234,56` are the same number to a parser and different to a reader.

5. **Design for text expansion**: German and Finnish run 30–40% longer than English, and CJK can be shorter but needs different line breaking. Fixed-width buttons, single-line table cells, and absolutely positioned labels break first. Test with pseudo-localisation (accented characters plus 40% expansion) before any real translation exists.

6. **Verify the right-to-left case properly**: `dir="rtl"` on the document, logical CSS properties (`margin-inline-start`, not `margin-left`), mirrored icons where direction is meaningful (back arrows) and **not** mirrored where it is not (clock faces, media controls, brand marks), and bidirectional text isolation for user content (a phone number inside Arabic text).

7. **Handle names, addresses, and personal data**: name fields cannot assume first/last, address formats differ by country, and honourifics are not universal. Truncation and initials are locale-specific.

8. **Check sorting and search**: alphabetical sorting is locale-dependent (Swedish puts Å after Z), case folding differs (Turkish dotless i), and search normalisation must handle accents and width variants.

9. **Include the non-UI surfaces**: emails, notifications, error messages, PDFs, CLI output, and anything an agent or API returns that a human reads. Machine-readable error codes should be stable and separate from localised text.

10. **Write `I18N_AUDIT.md`** with the string inventory, the ruleset, the plural and format handling, layout evidence per locale, RTL verification, and what was not covered.

## 5. Decision rules and evidence standard

- **Translate messages, never fragments.**
- **Plural rules come from the locale data**, not from arithmetic.
- **Format through the platform's locale APIs**, never by string manipulation.
- **Pseudo-localise before translating** — it finds layout bugs without waiting for translators.
- **RTL is a layout change, not a text change.**
- **Error codes are stable; messages are localised.**
- **A locale is not "done" without a screenshot from that locale.**

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| String inventory | Extraction tool | Every user-visible string keyed with context |
| No concatenation | Code search | No fragment assembly of sentences |
| Plural handling | Test with 0, 1, 2, 5, 21 in a complex locale | Correct forms per locale rules |
| Number/date/currency | Render per locale | Separators and order correct |
| Pseudo-localisation | Run with expanded strings | No clipping or overlap |
| RTL layout | Render an RTL locale | Direction, margins, icons correct |
| Bidi content | User-supplied Latin text in RTL UI | Isolated correctly |
| Sorting/search | Locale-specific test | Swedish/Turkish cases pass |
| Non-UI surfaces | Email/PDF/CLI check | Localised, with stable error codes |
| Untranslated strings | Fallback audit | Visible, not silently blank |

## 7. Failure handling

- **Translations arrive after launch** → ship the infrastructure (ICU, plural rules, layout) with pseudo-localisation first; retrofitting after strings are hardcoded is a rewrite.
- **A translation does not fit** → shorten the source string or allow reflow; never shrink the font per locale.
- **The translation is wrong for the context** → add context to the key and re-translate; the fix is in the pipeline, not the UI.
- **A locale requires a different script direction mid-page** → isolate each user-content region rather than flipping the document.
- **The string format cannot express plurals** → migrate that surface to ICU message format before adding locales; JSON key-value with `_plural` suffixes is a trap.
- **Legal or regulatory text differs by country** → route to the content owner; do not machine-translate legal copy.

## 8. Security and authorisation

Risk class B. Localised strings are still injection surfaces: never interpolate unescaped user content into translated messages, and keep placeholders in the format layer. Translation vendors receive your UI copy — ensure no secrets, internal identifiers, or customer data are in the string catalogue. Right-to-left and mixed-script input can bypass naive validation; validate by semantics, not by character class.

## 9. Completion criteria

- [ ] Every user-visible string inventoried with context and constraints.
- [ ] No sentence is assembled from concatenated fragments.
- [ ] Plural handling uses locale rules and is tested with 0/1/2/5/21.
- [ ] Dates, numbers, currency, and units formatted through locale APIs.
- [ ] Pseudo-localisation run; no clipping at +40% expansion.
- [ ] RTL verified with logical properties and correct icon mirroring.
- [ ] Bidi content isolated.
- [ ] Sorting and search tested for locale-specific behaviour.
- [ ] Emails, PDFs, CLI, and notifications included.
- [ ] Missing-translation fallback is visible and intentional.
- [ ] Screenshots captured per target locale.

## 10. Deliverables and handover

Artifacts: `I18N_AUDIT.md`, string inventory, layout evidence per locale.

Handover: translators receive the catalogue with context, not bare keys; `04-process/documentation/` applies the same rules to docs; `A11Y-01` verifies that language attributes are set (`lang="ar"`) so screen readers switch voices; a new locale launch follows `04-process/release-engineering/` with its own staged rollout.
