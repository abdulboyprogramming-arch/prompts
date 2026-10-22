# PROMPT 01 — Accessibility Conformance Audit (WCAG 2.2 AA)

**Identifier:** A11Y-01
**System:** 04-process/accessibility-audit
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A (read-only testing of a build you own or are authorised to test)
**Depends on:** none
**Produces:** `.a11y/AUDIT.md`, a conformance statement, a prioritised remediation list
**Inputs:** TARGET_URL (optional: PAGES, LEVEL, ASSISTIVE_TECH, TARGET_ENV)
**Est. effort:** 2–6 h for a representative page set

---

## 1. Role and mandate

You determine whether an interface meets WCAG 2.2 Level AA — by testing it, not by scanning it.

Automated scanners catch roughly a third of issues, mostly the mechanical ones. They cannot tell you that a modal traps focus, that a custom dropdown cannot be operated by keyboard, that an error message is announced before the field it describes, or that the "close" button has an accessible name of "×". A report built on a scanner's output is a report that both overstates and understates.

## 2. Objective and scope

**Produce:** a per-criterion conformance table for the audited pages, a prioritised defect list with reproductions, and a statement of what was and was not tested.

Out of scope: legal advice on compliance obligations, and design work — the audit states the failure and the required outcome, not the redesign.

## 3. Prerequisites and inputs

- `{{TARGET_URL}}` — the build under test; `{{PAGES}}` — a representative set, not the homepage: a form, a data table, a modal, a navigation flow, an error state, an empty state, and a page with media.
- `{{LEVEL}}` — default AA; `{{ASSISTIVE_TECH}}` — at least one screen reader (NVDA on Windows, VoiceOver on macOS/iOS) and keyboard-only.
- `{{TARGET_ENV}}` — an environment you are authorised to test, with test accounts, never production customer data.

## 4. Workflow

1. **Test keyboard-only first.** Tab through the whole flow: is every interactive element reachable, is the focus visible, is the order logical, does focus escape modals or hide behind them, is there a skip link, can you operate custom widgets (comboboxes, date pickers, sliders) with arrows, Enter, and Escape? Keyboard access is the highest-yield check and the one most often broken by component libraries.

2. **Test with a screen reader**, on at least one real flow. Listen for: whether the page has a sensible title and heading order, whether images and icon buttons have names, whether form fields announce their label, whether errors are announced when they appear, whether dynamic content changes are announced, and whether custom controls announce the role and state a native control would.

3. **Check contrast and non-text contrast** against the actual rendered colours: 4.5:1 for body text, 3:1 for large text, 3:1 for UI component boundaries and focus indicators. Measure it — do not eyeball it, and do not trust the design token, because opacity blends.

4. **Check reflow and zoom**: 320 CSS pixels wide without horizontal scrolling, 200% zoom without loss of content, text spacing overrides (1.5 line height, 0.12em letter spacing) without clipping, and landscape orientation support.

5. **Check the motion and timing criteria** that are usually skipped: pause/stop/hide for anything moving more than five seconds, no content that flashes more than three times per second, and respect for `prefers-reduced-motion`.

6. **Check the form against each criterion separately**: labels programmatically associated (not just visually adjacent), required fields indicated in text and not by colour alone, errors identified in text with a suggestion, error summary focusable at the top of the form, and autocomplete tokens present for personal data.

7. **Check the four WCAG 2.2 additions** specifically, because they are new and frequently missed. **Focus not obscured**: a sticky header must not cover the focused element. **Dragging movements** need a single-pointer alternative. **Target size** is at least 24×24 CSS px, or has 24 px of clear space around it. **Redundant entry** is avoided: do not re-ask for information already provided in the same process.

8. **Check the states nobody demonstrates**: empty lists, loading skeletons, error pages, session expiry, a very long error message, a table with 500 rows, and the mobile breakpoint. Components pass in the demo state and fail in the states that matter.

9. **Record every finding with a reproduction**: page, element, what you did, what happened, which criterion it violates, and the user impact in one line ("keyboard users cannot close the dialog"). Severity by impact and frequency, not by how unusual the element is.

10. **Write `.a11y/AUDIT.md`** with the conformance table (criterion → pass / fail / not tested), the defect list, and an explicit statement of coverage: pages, states, assistive technology, and what remains untested.

## 5. Decision rules and evidence standard

- **Tested beats scanned.** A scanner's clean report is not conformance.
- **Keyboard before screen reader before scanner** — that is the order of yield.
- **Measure contrast in the rendered page**, not in the token file.
- **Component libraries are not accessible by default**; verify each custom widget.
- **"Not tested" is an honest result**; "passes" without a test is not.
- **Impact and frequency set severity**, not novelty.
- **A finding needs a reproduction** someone else can follow.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Keyboard-only flow | Manual | All elements reachable, focus visible and ordered |
| Focus containment | Modal test | Focus trapped while open, returned on close |
| Screen reader pass | NVDA or VoiceOver | Names, roles, states, announcements correct |
| Headings and landmarks | Structure inspection | Logical order, one H1, landmarks present |
| Contrast measured | Colour measurement | Text ≥4.5:1, UI ≥3:1, focus indicator ≥3:1 |
| Reflow | 320 px viewport | No horizontal scroll, no clipping |
| Zoom | 200% | No loss of content or function |
| Motion | Reduced-motion and flashing checks | Criteria met |
| Forms | Label and error tests | Programmatic labels, textual errors, summary |
| WCAG 2.2 additions | Four checks | Focus not obscured, dragging alternative, target size, redundant entry |
| States tested | Empty, loading, error, long content | Findings recorded |
| Coverage stated | Report | Pages, states, AT, and untested areas listed |

## 7. Failure handling

- **No screen reader available** → keyboard and structure testing still run; state clearly that AT testing was not performed, rather than implying it passed.
- **A third-party widget fails** (embedded map, payment form) → record it as a dependency finding with the wrapper's limitations; an inaccessible iframe is still your page's failure for the user.
- **The design itself cannot meet contrast** → report the specific token pairs and the required ratio; the fix is a design change, not a code tweak.
- **Fixing everything is out of scope now** → rank by user-blocking impact (cannot complete a task) over annoyance (harder to read), and publish the remediation order.
- **A page requires authentication you do not have** → record it as not tested, and list what would be needed; do not infer conformance.
- **The team disputes a finding** → cite the criterion, the reproduction, and the assistive technology; disputes about taste are not conformance questions.

## 8. Security and authorisation

Risk class A: read-only testing against an environment you own or are authorised to test. Use test accounts and synthetic data; screen-reader testing on production with real accounts risks exposing customer data aloud and in logs. Do not publish a conformance claim for pages you did not test — a false accessibility statement is worse than none, and in several jurisdictions it is a legal exposure.

## 9. Completion criteria

- [ ] Representative page set defined, including form, table, modal, error, and empty states.
- [ ] Keyboard-only pass completed with focus behaviour recorded.
- [ ] Screen reader pass completed on at least one full flow (or explicitly not tested).
- [ ] Contrast measured on rendered output for text, UI, and focus indicators.
- [ ] Reflow at 320 px and 200% zoom verified.
- [ ] Motion and timing criteria checked.
- [ ] Forms checked for labels, errors, and autocomplete.
- [ ] Four WCAG 2.2 additions checked.
- [ ] Dynamic and error states tested.
- [ ] Conformance table and defect list written with reproductions.
- [ ] Coverage statement honest about what was not tested.

## 10. Deliverables and handover

Artifacts: `.a11y/AUDIT.md`, conformance statement, prioritised remediation list.

Handover: remediation goes to `03-domains/frontend/` (currently a skeleton) or the implementation team. The conformance table becomes the evidence for any accessibility statement published externally. `04-process/testing-qa/` absorbs the reproducible checks (keyboard traversal, contrast thresholds) into CI where they can be automated, and keeps the rest as a manual release checklist — the automatable third is not the difficult third.
