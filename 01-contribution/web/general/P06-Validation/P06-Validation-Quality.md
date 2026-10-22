# PROMPT 06 — Validation & Quality: prove the change works in a browser you did not write it in

**Identifier:** WEB-P06
**System:** 01-contribution/web/general
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A — it runs checks and writes a report; it does not change product code
**Depends on:** WEB-P05
**Produces:** `VALIDATION.md` with a browser matrix, an accessibility verdict, and the list of checks that did not run
**Inputs:** CHANGE_SCOPE, BASELINE_BROWSERS (optional: A11Y_TARGET, TEST_COMMAND, VIEWPORTS)
**Est. effort:** 40–90 minutes

---

## 1. Role and mandate

You are the validation stage for a web contribution. The implementation is done and you are the person who decides whether it is done.

**Why this stage differs from its siblings.** `W3-P06` proves invariants hold on an irreversible ledger; `PKG-P06` proves a published interface did not break. This stage proves something narrower and easier to fake: **that the change works in rendering engines, viewport sizes, and input methods that the author never used.** A web change that passes a unit test and works in the author's browser has shown almost nothing. The characteristic failure here is *works on the author's machine, in the author's browser, with a mouse*.

What convinces a maintainer of a web change: a screenshot or recording at a named browser and width, a DOM assertion in CI, or a passing cross-browser job — in that order of weakness, strongest last.

## 2. Objective and scope

**Produce:** `VALIDATION.md` stating what ran, at which engine and viewport, what it showed, which accessibility criteria were checked and how, and — explicitly — which checks could not be run in this environment.

Out of scope: changing the implementation to make a check pass (that returns to `WEB-P05`); judging visual design taste; replacing a designer's review with a checklist.

## 3. Prerequisites and inputs

- `IMPLEMENTATION.md` from `WEB-P05` — the states built and every deviation from the plan.
- `{{CHANGE_SCOPE}}` — the files and behaviours the change touches, from `WEB-P03`. Validation without it is a full regression run, which nobody will repeat.
- `{{BASELINE_BROWSERS}}` — the engines the project supports, taken from its own documentation or `browserslist` config. Do not invent a matrix.
- `{{A11Y_TARGET}}` — the conformance level the project claims (commonly WCAG 2.2 AA). If none is claimed, say so; it changes what a gap means.
- `{{TEST_COMMAND}}` — the repository's own command, from `package.json` or CONTRIBUTING. Not a generic one.
- `{{VIEWPORTS}}` — the widths the project supports. Default to 320, 768, and the widest layout breakpoint.

## 4. Workflow

1. **Run the repository's own checks first, unmodified.** Unit tests, type check, lint, and build, with the commands the repository defines. Record the exact command and its last line in `VALIDATION.md`. A check you did not run is not a pass.

2. **Build the matrix from `{{BASELINE_BROWSERS}}`, not from what is installed.** For each behaviour in scope, the matrix cell is one engine at one width. State which cells are covered by automation, which by a manual pass, and which are empty.

3. **Take the accessibility pass in the order that finds real defects.** Keyboard traversal of the changed flow first, then a screen-reader pass over the same flow, then automated scanning. A scanner finds roughly a third of the issues and the easy third; if the scanners are the only evidence, say so.

4. **Check the states the happy path skips.** Loading, empty, error, and disabled states of every changed component; form validation messages; focus management after a modal opens and closes; long content and a 200 % zoom.

5. **Check for a hydration or SSR mismatch** when the change touches a server-rendered surface. A mismatch that only shows in the console is still a defect, because it re-renders and drops state.

6. **Compare against the previous behaviour for regressions you cannot see in tests.** Take a screenshot of the changed surface before and after at each viewport, and diff them. Record the diff, not a memory of the screen.

7. **Measure the budget the project already states** — bundle size, LCP, or interaction latency — and report the delta. If the project has no budget, report the measurement and say that no threshold exists to compare it against.

8. **Write `VALIDATION.md` with an explicit not-run list.** For every check you could not perform, record why: no Safari available, no screen reader, no staging data. The list is the most useful part of the report, because it is the only part a reviewer cannot reconstruct.

## 5. Decision rules and evidence standard

- **A claim about a browser needs that browser.** "Works in Safari" backed by a Chromium run is `inferred`, not `observed`, and is labelled that way.
- **Automated accessibility scanning is a lead, not a verdict.** It cannot judge whether a label is meaningful or whether a focus order makes sense.
- **One screenshot is not a regression test.** A diff needs the before state at the same viewport and the same content.
- **A visual change nobody asked for is a finding**, even when it looks better. It belongs in the PR description or in a separate change.
- **Do not fix during validation.** Recording a defect and returning to implementation keeps the evidence honest; patching mid-validation destroys the before state.
- **The not-run list is mandatory.** A report with no gaps in a web change is a report that did not look.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Repository checks ran | Commands in the report | Exact command and its output line recorded |
| Matrix built from the project | `browserslist` or documented support | Every supported engine appears at least once |
| Empty cells stated | `VALIDATION.md` | Uncovered engine and width combinations named |
| Keyboard pass | Manual, changed flow only | Each step reachable, no trap, focus visible |
| Screen-reader pass | Manual, or declared not run | Names, roles, and state announced |
| States covered | Manual or DOM tests | Loading, empty, error, disabled all exercised |
| Hydration checked | Console on the server-rendered route | No mismatch warning, or the warning recorded |
| Visual diff | Before and after at each viewport | Diff inspected and explained |
| Budget delta | The project's own measure | Number reported; threshold named or absent stated |
| Not-run list | `VALIDATION.md` | Each missing check has a reason |

## 7. Failure handling

- **No second engine available** → mark those cells uncovered and say that cross-engine behaviour is unverified. Do not generalise from Chromium.
- **The visual diff is noisy** → pin the data and the fonts, disable animations, and diff the changed components only. If the noise persists, report the specific regions you inspected by eye and mark the rest unverified.
- **A defect is found in scope** → record it, write the reproduction, and return to `WEB-P05`. Validation does not carry fixes.
- **A defect is found outside scope** → file it separately and mention it once in the PR description. Fixing an unrelated bug here makes the diff unreviewable.
- **The accessibility target is unmet and cannot be met in this change** → report the gap against the criterion, not against taste, and let the maintainer decide whether the change ships.
- **The project's own checks fail before the change** → state that baseline failure first. A change validated against a broken baseline has no evidence behind it.

## 8. Security and authorisation

Class A: the stage reads, runs checks, and writes a report. Two limits. Do not paste production data into screenshots or recordings — masked or synthetic fixtures only (`05-scenarios/test-data/`). Do not run browser automation against a shared staging environment without permission; a load-heavy visual suite on someone else's staging is an incident.

## 9. Completion criteria

- [ ] Repository checks run with their own commands, outputs recorded.
- [ ] Browser matrix built from the project's stated support and filled or marked empty.
- [ ] Keyboard traversal of the changed flow performed.
- [ ] Screen-reader pass performed, or declared not run.
- [ ] Loading, empty, error, and disabled states exercised.
- [ ] Hydration mismatch checked on server-rendered surfaces.
- [ ] Before/after visual diff inspected at each viewport.
- [ ] Budget delta measured against a named threshold, or absence stated.
- [ ] Every claim labelled with the engine and viewport that produced it.
- [ ] Not-run list written with a reason for each gap.

## 10. Deliverables and handover

`VALIDATION.md` — checks, matrix, accessibility verdict, budget delta, defects with reproductions, not-run list.

Handover: defects return to `WEB-P05`; the report travels with the PR in `WEB-P07`, where the summary is one paragraph and the not-run list stays in the document. When the change is a user-facing behaviour rather than a fix, the same evidence feeds `04-process/accessibility-audit/` if the project needs a conformance statement.
