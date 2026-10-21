# PROMPT 04 — Planning & Design: plan the states and the breakpoints, or plan to discover them in review

**Identifier:** WEB-P04
**System:** 01-contribution/web/general
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** A — it writes a plan; it changes no application code
**Depends on:** WEB-P03
**Produces:** `PLAN.md` with a state-by-breakpoint matrix, the test layer for each behaviour, the component-reuse decision, and the ordered steps with their verification
**Inputs:** SELECTED_WORK, PROJECT_CONVENTIONS (optional: COMPONENT_LIBRARY, BROWSER_SUPPORT, TEST_COMMAND)
**Est. effort:** 30–60 minutes

---

## 1. Role and mandate

You are the planning stage of a web contribution. `WEB-P03` chose the work and wrote the claim; your job is to turn that claim into an ordered set of steps whose completion can be checked without asking you what you meant.

**Why this stage differs from its siblings.** `W3-P04` plans a contract change, where the plan's centre of gravity is the storage layout and the deployment sequence. `PKG-P04` plans a library change, where it is the surface delta and the release choreography. This stage plans a **rendered change**, and its centre of gravity is a matrix: every surface the change touches, every state it can be in, every width it must survive. The characteristic failure is *a plan that describes the desktop happy path and calls it a design.*

A web plan is checkable in one specific way: **for each cell of the matrix, the plan says how it will be tested, at which layer, and what passing looks like.** A plan without that is a description of intent, and it produces an implementation that `WEB-P05` has to improvise.

## 2. Objective and scope

**Produce:** `PLAN.md` with the surface list, the state-by-breakpoint matrix with a test layer per row, the reuse-or-create decision with its reason, the ordered steps each ending in a verifiable state, and the risks that would change the plan.

Out of scope: writing code, choosing a framework, or reopening the selection. A plan that discovers the work is the wrong size returns it to `WEB-P03`.

## 3. Prerequisites and inputs

- `{{SELECTED_WORK}}` — from `WEB-P03`: the claim, surfaces, states, acceptance criteria, and the design owner for anything visible.
- `{{PROJECT_CONVENTIONS}}` — component structure, styling approach, test placement, and naming. A plan that ignores them produces an implementation that reads as foreign.
- `{{COMPONENT_LIBRARY}}` — what already exists. The reuse decision is made here, not during implementation.
- `{{BROWSER_SUPPORT}}` — the engines and widths the project claims, from `browserslist` or the documentation.
- `{{TEST_COMMAND}}` — the repository's own runner, so the test layer names a real command.

## 4. Workflow

1. **Restate the claim in one sentence, and stop if it cannot be restated.** The plan exists to make `WEB-P03`'s claim true; a plan that describes different work is a finding about the selection.

2. **Build the state-by-breakpoint matrix.** Rows are the states the change can be in — default, loading, empty, error, disabled, long content, and the unauthenticated variant where relevant. Columns are the widths the project supports, starting at 320 px. Every cell is one of: *built and covered by a test*, *built and manually checked*, *unchanged by this work*, or *out of scope with a reason*. Empty cells are not allowed, and they are the most common cause of a validation report full of surprises.

   | State | 320 px | 768 px | Widest | Test layer |
   |---|---|---|---|---|
   | Default | build + DOM test | build + DOM test | build + DOM test | component |
   | Empty | build + story | build | unchanged | component |
   | Error | build + DOM test | build + DOM test | build | component |
   | Loading | unchanged | unchanged | unchanged | — |

3. **Name the test layer for each behaviour, and only one.** Parsing and formatting logic: unit. Interaction, focus, conditional rendering: component or DOM. A flow that crosses a route or a service: end to end, and only then. Writing every behaviour as an end-to-end test makes the suite slow enough that it stops being run.

4. **Decide reuse before creation, and write the reason.** The nearest existing component, what it does not do that this change needs, and whether an extension serves both cases. "New component" is an acceptable answer with a sentence behind it; without one it is the beginning of a fork in the design system.

5. **Plan the data and state path, not just the component.** Where the data comes from, what happens while it is absent, how the component behaves when the request fails, and whether the state belongs to the component or a shared store. Most web complexity lives in this paragraph and most plans omit it.

6. **Plan the accessibility work as tasks, not as an adjective.** The heading level in the surrounding structure, the landmark the component sits in, the accessible name, the error association, the focus destination after a modal closes. Each is a step with a check, or it is a hope.

7. **Plan the visual regression surface.** The components and tokens the change touches, and every screen that consumes them. A shared button changed for one screen is changed for all of them, and the plan says which the reviewer must check.

8. **Order the steps so each ends in a verifiable state.** A step that leaves the app broken until step six is a step that cannot be reviewed alone; where a change genuinely requires sequencing (a migration, a flag, a data shape), state the sequence and what is true after each.

9. **Name the risks that would change the plan.** A shared-component dependency, an API that cannot return the needed field, a design decision still outstanding. Each risk gets the trigger and the alternative, so implementation does not stop to negotiate.

10. **Write the definition of done as the matrix, not as a paragraph.** The plan is complete when every cell is filled and every behaviour has a layer. That is a check `WEB-P05` and `WEB-P06` can both run.

## 5. Decision rules and evidence standard

- **Every matrix cell is filled.** "Not considered" is not a state; "unchanged by this work" is.
- **One test layer per behaviour.** The cheapest layer that can catch the defect wins.
- **Reuse is the default; creation needs a sentence.** A one-off component that duplicates ninety per cent of an existing one is how a design system becomes a set of near-duplicates.
- **Accessibility is planned as tasks.** An adjective in a plan becomes a retrofitted attribute in code.
- **A step without a verification is not a step.** If you cannot say what is true after it, it is not planned.
- **The plan names the risk and the alternative.** A plan that depends on an unknown is a plan that stops mid-implementation.
- **Do not relitigate the selection.** If the work does not fit, return it rather than plan around it.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Claim restated | First paragraph | One sentence, matching `WEB-P03` |
| Matrix complete | Every cell filled | No blank cells; each is built, unchanged, or out of scope with a reason |
| Test layers named | One per behaviour | Each behaviour has exactly one layer and a command |
| Reuse decided | Component named | Existing component extended or the reason for a new one written |
| Data path planned | Where, while absent, on failure | All three stated |
| Accessibility tasks | Heading, landmark, name, focus, error | Each is a step with a check |
| Regression surface | Consumers of changed components | Every consuming screen named |
| Steps verifiable | Ordered list | Each step states what is true afterwards |
| Risks and alternatives | Two or three entries | Trigger and fallback for each |
| Definition of done | The matrix | Completion is checkable without interpretation |

## 7. Failure handling

- **The matrix reveals the work is three times larger than the claim** → return to `WEB-P03` and select the narrower claim. Planning a large change from a small claim is how a contribution becomes unreviewable.
- **The needed data field does not exist** → plan the smallest server or client change that provides it, and treat that as its own step with its own risk. Do not assume an endpoint will grow a field.
- **The design owner has not responded** → plan the behaviour-neutral parts and mark the visual decision blocked. Do not decide it in the plan and call it agreed.
- **No component library exists** → the reuse decision becomes "match the nearest sibling file", and the plan says which one.
- **The project has no test runner for the layer the behaviour needs** → choose the nearest available layer, record the gap, and let `WEB-P06` report it rather than introducing a framework inside a contribution.
- **Two risks both trigger** → stop and return to selection. A plan with two unresolved dependencies is a plan that will be abandoned mid-way.

## 8. Security and authorisation

Class A: the stage writes a plan. Two cautions. First, a plan that includes a screenshot or a data sample from a production environment carries personal data into a repository; specify seeded data in the plan's data-path paragraph. Second, a change to an authentication screen, a payment form, or anything that renders untrusted markup deserves an explicit security risk in the plan, because those surfaces are where a web contribution can do the most damage.

## 9. Completion criteria

- [ ] Claim restated in one sentence.
- [ ] State-by-breakpoint matrix complete, no blank cells.
- [ ] A test layer and command per behaviour.
- [ ] Reuse-or-create decision written with its reason.
- [ ] Data path planned: source, absence, failure.
- [ ] Accessibility work broken into named tasks.
- [ ] Regression surface named for every shared component touched.
- [ ] Steps ordered, each verifiable.
- [ ] Risks carry triggers and alternatives.
- [ ] Definition of done is the matrix.

## 10. Deliverables and handover

`PLAN.md` — claim, matrix, test layers, reuse decision, data path, accessibility tasks, regression surface, ordered steps, risks.

Handover: `WEB-P05` implements to the matrix and records deviations; a cell it cannot build is a planning finding, not an implementation failure. `WEB-P06` validates against the matrix, so a state added during implementation appears in validation as scope growth. `WEB-P07` derives the reviewer's recipe from the cells that were built and tested, which is why the matrix is worth filling in honestly.
