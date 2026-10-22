# PROMPT 05 — Implementation: build every state the plan named, and no more

**Identifier:** WEB-P05
**System:** 01-contribution/web/general
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B — it writes application code on a branch; it does not push to a protected branch or deploy
**Depends on:** WEB-P04
**Produces:** a branch with the change, plus `IMPLEMENTATION.md` recording the states built, the semantic decisions, and every deviation from the plan
**Inputs:** PLAN, PROJECT_CONVENTIONS (optional: COMPONENT_LIBRARY, DESIGN_TOKENS, TEST_COMMAND)
**Est. effort:** 2–6 hours

---

## 1. Role and mandate

You are the implementation stage of a web contribution. The plan named the surfaces, the states, and the acceptance criteria; your job is to make them true in code a maintainer recognises as belonging to this project.

**Why this stage differs from its siblings.** `W3-P05` implements under invariants, where a careless line can move value and the review is adversarial. `PKG-P05` implements under a public surface, where an accidental export becomes a promise. This stage implements under **semantics and state coverage**, and the characteristic failure is *the happy path ships, the loading state is a spinner nobody can cancel, and the clickable `div` replaces a `button` that already worked.*

Two things make a web diff expensive to review: it changes more of the page than the claim required, and its behaviour is undefined in the states nobody demonstrated. Both are prevented here, not in validation.

## 2. Objective and scope

**Produce:** a branch implementing the plan, with every state from `PLAN.md` present, native semantics used wherever they exist, the diff limited to the named surfaces, and `IMPLEMENTATION.md` listing what was built, the semantic choices made, and every deviation with its reason.

Out of scope: redesigning the component, adding states the plan did not name, fixing adjacent defects, or running the validation pass. `WEB-P06` validates; this stage makes validation possible.

## 3. Prerequisites and inputs

- `{{PLAN}}` — from `WEB-P04`: surfaces, states, acceptance criteria, and the test layer per behaviour.
- `{{PROJECT_CONVENTIONS}}` — the component patterns, styling approach, naming, and file layout. Deviating from them makes the diff unreadable to the people who maintain it.
- `{{COMPONENT_LIBRARY}}` — the existing components and design tokens. A new bespoke component where one exists is the most common reason a web PR is sent back.
- `{{DESIGN_TOKENS}}` — spacing, colour, and typography scales. Hardcoded values are a defect even when they look right.
- `{{TEST_COMMAND}}` — the repository's own command, so the tests you add run the way the project runs them.

## 4. Workflow

1. **Re-read the plan's state list before writing code, and treat it as the definition of done.** Loading, empty, error, disabled, and the unauthenticated variant if it exists. Implementation is finished when every state renders correctly, not when the happy path does.

2. **Write the failing test for each acceptance criterion first**, at the layer the plan named — a unit test for parsing, a DOM test for behaviour, an end-to-end test only where the flow crosses a boundary. A criterion you cannot express as a test is one you should have caught in planning; say so instead of silently redefining it.

3. **Use the platform before the library.** A `button` with a `disabled` attribute before a `div` with `role="button"`, `tabindex`, and a keydown handler. Native `dialog` or `details` before a hand-rolled equivalent. A real `label` before `aria-label`. Every ARIA attribute is a promise to reimplement what the browser already does, and most of them are kept badly.

4. **Match the nearest sibling component rather than inventing a shape.** Find the component that most resembles what you are building — a list with states, a form with validation, a panel with a toggle — and follow its structure, its prop naming, and its test style. A contribution that reads as foreign is reviewed line by line; one that reads as native is reviewed for correctness.

5. **Style through the tokens and the existing utilities.** If a value is not in the scale, use the nearest scale value and record the difference in `IMPLEMENTATION.md` rather than introducing a new constant. A one-off hex colour is how design systems rot.

6. **Build the states as visible, reachable variants.** Each state should be exercisable without editing code — a query parameter, a fixture, a story, or a test — so that `WEB-P06` can demonstrate it and a reviewer can see it. A state only reachable when the network fails is a state nobody will check.

7. **Handle the transitions, not just the states.** Focus when a modal opens and when it closes; the button that must be disabled while submitting; the double-submit that must not send twice; the optimistic update that must roll back. Transitions are where web defects live and where tests are thinnest.

8. **Keep the diff behaviour-only.** No reformatting, no import reordering in untouched files, no dependency bumps, no "while I was here" fixes. If you found an adjacent defect, record it in `IMPLEMENTATION.md` and leave it for its own change.

9. **Write accessible markup as you go, not as a later pass.** The heading order, the landmark structure, the `alt` text, the error message associated with its field via `aria-describedby`. Retrofitting accessibility means rewriting the markup, which means the tests written against it move too.

10. **Record every deviation from the plan, with the reason.** A deviation is fine; an unrecorded one is a defect in the process, because `WEB-P06` validates against the plan and will otherwise report a mismatch it cannot explain.

11. **Run the repository's checks before handing over.** Tests, type check, lint, and build, with the project's commands. A branch that fails its own lint is not ready to validate.

12. **Do not push to a protected branch, force-push, or open the PR.** Those are later stages and Category C; keep the work on a branch.

## 5. Decision rules and evidence standard

- **Native before ARIA, ARIA before JavaScript.** Each step down that ladder adds behaviour you must test and maintain.
- **The state list is the definition of done.** A change with a loading state and no error state is half a change, whatever the diff looks like.
- **Reuse before creation.** A new component needs a reason the existing one cannot serve, written in `IMPLEMENTATION.md`.
- **Tokens before literals.** A hardcoded colour or spacing value is a defect with a nice-looking screenshot.
- **One claim, one diff.** Adjacent improvements are recorded and deferred; mixing them makes the change unreviewable and un-revertable.
- **Tests at the boundary the plan named.** Unit tests for logic, DOM tests for behaviour, end-to-end only for flows that cross systems.
- **A deviation is recorded, never hidden.** The record is what lets validation and review agree about what was built.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| States built | Render each state | Every state in `PLAN.md` exists and is reachable |
| Acceptance tests | Test run | One failing-then-passing test per criterion, at the planned layer |
| Native semantics | Markup review | Native element used wherever one exists |
| Sibling match | Diff against nearest component | Structure, prop names, and test style match |
| Tokens used | Style review | No literal colour, spacing, or type size outside the scale |
| Transitions handled | Manual exercise | Focus, double-submit, and rollback behave |
| Diff scope | File list | Only the planned surfaces changed; no reformatting or bumps |
| Accessibility built in | Markup review | Heading order, landmarks, labels, and error association present |
| Deviations recorded | `IMPLEMENTATION.md` | Every deviation has a reason |
| Repository checks | Project commands | Tests, types, lint, and build pass |

## 7. Failure handling

- **The plan's acceptance criterion cannot be tested as written** → implement the closest testable version, record the change, and flag it for `WEB-P06`; do not quietly weaken the criterion.
- **The existing component almost fits** → extend it with a variant rather than forking it, and say why in `IMPLEMENTATION.md`. Two components that differ by one prop is how design systems split.
- **The change requires touching a shared component** → do it, and list every consumer the diff can affect so validation knows where to look. Hiding a shared change inside a feature PR is the defect this rule prevents.
- **A dependency seems necessary** → try the platform first; if it is genuinely needed, record the size and licence and expect review to push back.
- **The design intent is unclear** → implement the least surprising behaviour, mark the ambiguity in `IMPLEMENTATION.md`, and ask before the PR rather than after.
- **Tests pass locally but the state is unreachable** → the state is not built. A conditional branch no input reaches is dead code that reads as a feature.

## 8. Security and authorisation

Class B: the stage writes code on a branch. Two cautions. First, rendering untrusted content is a security decision: use the framework's escaping, never `innerHTML` with interpolated data, and treat a rich-text field as an attack surface. Second, a change to authentication screens, token storage, or `dangerouslySetInnerHTML` deserves a second reader; say so in `IMPLEMENTATION.md` so the reviewer knows to look. Never commit credentials, API keys, or fixtures containing personal data.

## 9. Completion criteria

- [ ] Every state in the plan implemented and reachable.
- [ ] One test per acceptance criterion, at the planned layer.
- [ ] Native elements used wherever they exist.
- [ ] Structure and naming match the nearest sibling component.
- [ ] No literal value outside the design tokens.
- [ ] Transitions handled: focus, double-submit, rollback.
- [ ] Diff limited to the planned surfaces; nothing reformatted.
- [ ] Accessibility written in, not retrofitted.
- [ ] Every deviation recorded with a reason.
- [ ] Repository checks pass; nothing pushed to a protected branch.

## 10. Deliverables and handover

The branch, plus `IMPLEMENTATION.md` — states built, semantic choices, reuse decisions, deviations with reasons, and any adjacent defects deferred.

Handover: `WEB-P06` validates against the states and criteria recorded here, and a state that validation cannot reach is a finding against this stage. `WEB-P07` writes the reviewer's recipe from `IMPLEMENTATION.md` and the validation report, which is why the deviations are written down: the description must not claim more than the diff does.
