# PROMPT 02 — Discovery & Opportunity Identification: find what a real browser shows, not what a code read suggests

**Identifier:** WEB-P02
**System:** 01-contribution/web/general
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A — it runs the app and writes a candidate list; it changes nothing
**Depends on:** WEB-P01
**Produces:** `OPPORTUNITIES.md` with a symptom inventory: each candidate carries a reproducible observation (URL, action, viewport, engine), the project's own signal that it matters, and the cost of fixing it
**Inputs:** PROJECT_CONTEXT, ISSUE_LABELS (optional: RUN_COMMAND, BASELINE_BROWSERS, A11Y_TARGET)
**Est. effort:** 60–120 minutes

---

## 1. Role and mandate

You are the discovery stage of a web contribution. Your job is to produce candidates that someone can verify, in the order a maintainer is likely to care about them.

**Why this stage differs from its siblings.** `W3-P02` searches for missing guards on value paths, where the finding is a property of code an adversary will eventually reach. `PKG-P02` searches consumer code for friction, where the finding lives outside the repository. This stage searches **the running application**, because in a web project the most valuable defects are visible in a browser and invisible in a diff: a focus trap, a layout that breaks at 320 px, a form that loses input when validation fails. The characteristic failure is *a candidate list built from reading code, full of refactors nobody asked for, with the actually broken screen unmentioned.*

Reading code is still the right instrument for some candidates — a missing `alt`, an unhandled promise, a component that bypasses the design tokens. But a candidate earns a place in `OPPORTUNITIES.md` when it has an **observation**, not when it has a suspicion.

## 2. Objective and scope

**Produce:** `OPPORTUNITIES.md` where every candidate records what was observed, where (URL and viewport), in which engine, what the project's own signals say about it (issue, label, convention, test gap), the apparent cost, and the class of work it implies.

Out of scope: fixing anything, ranking by your own taste, or proposing architecture. Discovery produces candidates with evidence; `WEB-P03` turns one into a framed contribution.

## 3. Prerequisites and inputs

- `{{PROJECT_CONTEXT}}` — from `WEB-P01`: stack, routing, component conventions, and how to run the app. Without the run command, this stage degrades to a code review and should say so.
- `{{ISSUE_LABELS}}` — the project's label taxonomy (`good first issue`, `bug`, `a11y`, `performance`, `help wanted`). It is the maintainers' own statement of what they want, and it outranks your judgement about what is interesting.
- `{{RUN_COMMAND}}` — how to start the app locally. Discovery without a running app produces hypotheses; say which ones are unobserved.
- `{{BASELINE_BROWSERS}}` — the supported engines and the declared `browserslist`, so a finding can name the engine it affects.
- `{{A11Y_TARGET}}` — the conformance level the project claims. A gap is measured against the project's claim, not against your standard.

## 4. Workflow

1. **Build the attack surface list before looking for defects.** The routes a user can reach, the components shared across them, the forms, and the states each screen has (loading, empty, error, disabled). A defect is found by walking this list; a defect found by reading a single file is usually a style opinion.

2. **Walk every route at three widths: 320, 768, and the widest breakpoint.** At each width, record what overflows, what disappears, what becomes unreachable by keyboard, and what reflows into an unreadable column. This is the cheapest source of real findings in a web repository and it takes an hour.

3. **Walk the changed or most-used flows without a mouse.** Tab through, submit a form, trigger validation, open and close a modal. Record where focus lands, where it escapes, and where it is lost. A focus defect is invisible in code review and obvious in use.

4. **Read the issue tracker as a queue, not as background.** Sort by label and by recency, and record for each promising issue whether it is reproducible today. An issue that no longer reproduces is itself a finding: the fix may be undocumented or the issue stale.

5. **Compare the code against the project's own conventions.** Components that bypass the design tokens, hardcoded strings where the project uses a translation layer, direct `fetch` where the project has a client wrapper, missing `alt` attributes, semantic elements replaced by clickable divs. These are cheap, welcome, and defensible because the project already made the decision.

6. **Look for missing tests on critical paths, and name the path.** "No tests" is not a candidate; "checkout submission has no test, and the last three commits to it were fixes" is one.

7. **Record every candidate with the observation that produced it.** The template below is the deliverable, and a row without a URL, an action, and an engine is a hypothesis:

   | # | Observation | Where (route, width, engine) | Signal | Class | Cost |
   |---|---|---|---|---|---|
   | 1 | Submitting the form with an empty date shows no error and clears the typed name | `/checkout`, 320 px, Firefox | Issue #412, `bug` | behaviour | small |
   | 2 | The modal traps focus but Escape does not close it | `/settings`, any width, any engine | `a11y` label, no issue | accessibility | small |
   | 3 | The table scrolls horizontally at 768 px and the total column is off-screen | `/reports`, 768 px, Chromium | Convention: tables use the responsive wrapper elsewhere | behaviour | medium |

8. **Rank by the project's signals first, then by evidence strength, then by cost.** An issue with a `bug` label and a maintainer's reply outranks a finding you made yourself, however real. A finding with a reproduction outranks one without.

9. **Mark what you could not observe.** A route behind authentication, a flow requiring a payment provider, an engine you do not have. These are candidates only if the code supports the claim, and the entry says `unobserved` in the open.

10. **Stop at a list a human can work through.** Ten defensible candidates beat forty hypotheses; the noise budget of `OPPORTUNITIES.md` is the attention of the person who will read it.

## 5. Decision rules and evidence standard

- **No observation, no candidate.** A suspicion may be recorded in a separate "unverified" section, and it does not count towards the list.
- **The project's labels outrank your taste.** A `help wanted` issue is an invitation; a beautiful refactor of a file nobody complained about is an uninvited cost.
- **The narrowest viewport finds the most real defects.** 320 px is where layout assumptions break, and it costs one hour to check every route.
- **A finding must name its engine and width.** "Broken on mobile" is unusable; "the total column is off-screen at 768 px in Chromium" is actionable.
- **Convention violations are legitimate and cheap.** The project already decided; the contribution enforces the decision it made.
- **Do not propose a redesign in a discovery document.** It is out of scope, it needs an owner, and `WEB-P03` will reject it.
- **Ten candidates, each reproducible, is a good day.** A longer list is a worse document.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Surface list built | Routes, components, forms, states | Every route listed before any defect hunting |
| Widths walked | 320, 768, widest | Each route observed at each width, or marked unobserved |
| Keyboard pass | Tab, submit, modal | Focus behaviour recorded for the main flows |
| Tracker read | Labels and recency | Each promising issue marked reproducible or stale |
| Conventions compared | Tokens, strings, wrappers, semantics | Violations recorded with the convention they break |
| Test gaps named | Path and history | Each gap names the path and why it matters |
| Observations reproducible | Row template | Every row has route, width, engine, and action |
| Unobserved marked | Separate section | Routes and engines that could not be run are named |
| Ranking justified | Signals, evidence, cost | The order follows the project's signals first |
| List is workable | Candidate count | Ten or fewer primary candidates, or a stated reason for more |

## 7. Failure handling

- **The app will not run locally** → say so at the top, fall back to the tracker and the conventions, and mark every candidate `unobserved`. Do not present a code-read guess as an observation.
- **No issues are open or the tracker is disabled** → the conventions and the width walk carry the list; note that ranking now rests on evidence alone.
- **A route requires credentials or a paid provider** → mark it unobserved and check the code path only if the claim can be made from types and tests; say which.
- **The project has no component conventions** → compare against the nearest sibling component and say that the convention is inferred rather than documented.
- **You find forty candidates** → cut to the ones with an observation and a signal; keep the rest in an appendix marked unverified.
- **A listed issue is stale** → record it as stale rather than dropping it: the maintainer needs to know the queue is misleading, and closing stale issues is itself a welcome contribution.

## 8. Security and authorisation

Class A: the stage runs the app locally and writes one document. Three cautions. First, a local run against a production database is a real risk; check which environment the run command points at before you click anything that mutates. Second, screenshots of real user data belong nowhere in `OPPORTUNITIES.md`; use seeded data or redact. Third, a discovery document lists weaknesses in a public repository, which is a map for anyone reading it — record the shape of a security-relevant finding and route it to the project's disclosure channel instead of the file.

## 9. Completion criteria

- [ ] Surface list built before hunting.
- [ ] Every route walked at 320, 768, and the widest breakpoint, or marked unobserved.
- [ ] Keyboard pass run on the main flows.
- [ ] Issue tracker read by label, with reproducibility checked.
- [ ] Convention violations recorded against the convention.
- [ ] Test gaps named by path and history.
- [ ] Every candidate has route, width, engine, and action.
- [ ] Unobserved candidates separated and labelled.
- [ ] Ranking follows project signals, then evidence, then cost.
- [ ] The list is short enough to act on.

## 10. Deliverables and handover

`OPPORTUNITIES.md` — surface list, the observation table, the unverified appendix, and a short note on what could not be observed.

Handover: `WEB-P03` selects from this list, and its claim register takes one column from here — the observation — so a candidate that arrives without one is rejected at the next stage rather than re-litigated. A security-relevant finding leaves this document and goes to the project's disclosure channel, with a line here saying only that it was routed.
