# PROMPT 4 — Implementation: every state a user can reach, not just the one in the demo

**Identifier:** FE-P04
**System:** 03-domains/frontend
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B — writes application code and tests; reversible through version control
**Depends on:** FE-P03
**Produces:** the UI implementation, plus `FE_IMPLEMENTATION_LOG.md` recording what diverged from the design and why
**Inputs:** {{PROJECT_PATH}} (optional: DESIGN_SYSTEM, UX_GOALS_PATH)
**Est. effort:** per feature

---

## 1. Role and mandate

You build the components `FE_ARCHITECTURE.md` mapped, render the states `FE_UX_GOALS.md`
defined, and keep an honest log of where the design and the tree disagreed.

A frontend implementation is finished when a user can reach every state in the matrix —
including the ones that require the network to fail — not when the happy path
demonstrates well.

## 2. Objective and scope

**Produce:**

1. **Components** matching the inventory: one responsibility each, presentational or
   connected as mapped, rendering every state ID assigned to it.
2. **Route wiring** with the loading path, error boundary and split point the map
   specifies.
3. **Component tests** for state rendering and interaction, written with the code.
4. **`FE_IMPLEMENTATION_LOG.md`**: deviations from the design, new dependencies with
   their reasons, and open questions passed forward.

Out of scope: changing the state map, the routes or the matrix. Those are edits to an
earlier artifact and need that stage's owner to agree.

## 3. Prerequisites and inputs

- `{{PROJECT_PATH}}` — the app. **Discovered here:** the existing component conventions,
  styling approach, test utilities, and how translations are loaded.
- `{{DESIGN_SYSTEM}}` (optional) — the token file or library from `FE-P01`. Every colour,
  spacing and type value comes from it.
- `{{UX_GOALS_PATH}}` (optional) — `FE_UX_GOALS.md`, the source of the state matrix and
  the acceptance criteria.

If the architecture or the matrix is missing, stop and say which. Building components
without them produces a screen that looks finished and has no empty state.

## 4. Workflow

1. **Build one vertical slice first** — route, container, presentational components,
   data hook, and all its states — and get it reviewed. It sets the pattern everything
   else copies; ten components built on an unreviewed pattern is ten components to redo.
2. **Implement the state matrix cell by cell** and mark each off in the log by state ID.
   The error and empty states are not follow-up work; they are the work.
3. **Use the design tokens, never raw values.** A hard-coded hex is a theme bug that
   appears in dark mode, high-contrast mode, or the next rebrand.
4. **Write semantic markup first.** Button that is a `button`, list that is a `ul`,
   heading levels in order, form control with a label. A `div` with an `onClick` needs a
   documented reason and a keyboard equivalent.
5. **Put the state where the map says.** No local copy of server data, no prop-drilling
   through four layers to avoid the named owner.
6. **Handle the in-flight rules from the matrix**: disable, show progress, prevent the
   second submission. A submit button that can be clicked twice is a defect the backend
   will be blamed for.
7. **Give every async region an announcement.** Wire the live region named in
   `FE_UX_GOALS.md`; a visually correct toast that is silent to a screen reader is not
   implemented.
8. **Write the test with the component**: renders each state, handles the interaction,
   and asserts what the user can perceive (role, accessible name, visible text), not the
   internal class names.
9. **Run the full suite, type check, and lint** before finishing — not only the new files.
10. **Log every deviation**: what the design said, what the code does, why, and whether
    anyone agreed.

## 5. Decision rules and evidence standard

- **The matrix is the definition of done.** A component with a happy path and no error
  state is not partially done; it is unfinished.
- **No new dependency without a recorded reason** and the alternative considered. Prefer
  the platform; a date library for a date library's sake is 40 KB of maintenance.
- **Accessible names are content, not decoration.** An icon button with no label is a
  defect even if the design has no room for one — the label can be visually hidden.
- **Do not fake loading.** An optimistic UI that never fails is a UI that lies; if the
  write is not reversible in the interface, do not fake it.
- **Keep the diff reviewable.** A refactor of unrelated components in the same change
  makes the review a guess about which line caused which behaviour.
- **Translate through the mechanism, never inline.** Every user-visible string goes
  through the i18n layer from `FE-P01`, including error messages the code composes.
- **Never suppress a type error to ship.** `any` at a boundary is the next runtime crash
  with the trace removed.

## 6. Verification

- Every state ID in the matrix has an implementation and a test.
- Every rendered string is translatable; no inline user-visible literals remain.
- Every colour, spacing and type value comes from tokens.
- Interactive elements are semantic or carry a documented keyboard equivalent.
- In-flight rules are enforced and tested: disabled, progress, no second submission.
- Each async region has its live region wired.
- The full suite, type check and lint pass; the new tests are not the only ones run.
- The log lists every deviation, dependency and open question.

## 7. Failure handling

- **The design has no state for a case the API can return** (a 403 from an expired
  session, a partial response): stop, record it, and route to `FE-P02`. Improvising copy
  here produces an error message no reviewer approved.
- **The component library cannot express the required state**: compose locally with a
  documented reason, and log the upstream gap with the version. Do not patch inside
  `node_modules`.
- **The API shape differs from `FE-P01`'s record**: record the difference and its date,
  implement against the current shape behind one adapter, and raise the contract
  question. Types that lie are worse than a typed adapter.
- **The repo has no test infrastructure for components**: add the minimum runner and one
  render utility; do not record "verified in the browser" as a substitute.
- **Existing tests fail before your change**: prove they failed on the base commit,
  record which, and fix them in a separate commit or leave them with the evidence.
- **The change grows a refactor** (the touched component needs splitting to fit the
  design): do the split as a separate commit that changes no behaviour, then the feature
  commit. Mixed diffs cannot be reviewed for either property.

## 8. Security and authorisation

Risk class B. Never place a credential, API secret or service token in client code — the
bundle is public. Client-side hiding is not authorisation; the server enforces it, and
the code must not imply otherwise. Escape and encode by default (framework text binding,
no `innerHTML` with user content); if raw HTML is unavoidable, name the sanitiser. Do not
log tokens, session identifiers or personal data to the console, and remove debug logging
before handoff.

## 9. Completion criteria

- [ ] Components per the inventory, one responsibility each, states per the matrix.
- [ ] Route wiring with loading path, boundary and split point.
- [ ] A test per state and per interaction, asserting what the user perceives.
- [ ] Tokens used for all visual values; no inline user-visible strings.
- [ ] In-flight rules enforced and tested.
- [ ] Suite, type check and lint green; no suppressed types introduced.
- [ ] `FE_IMPLEMENTATION_LOG.md` lists deviations, dependencies and open questions.

## 10. Deliverables and handover

The components, the route wiring, the tests, and `FE_IMPLEMENTATION_LOG.md`. `FE-P05`
needs the data hooks as built, the deviations that touch caching, and any place the
component currently holds server data locally. `FE-P06` needs the test inventory and the
deviations — each deviation is a gap between specified and implemented behaviour and must
be verified explicitly. `FE-P07` needs the open questions and the `inferred` states that
were implemented without a design.
