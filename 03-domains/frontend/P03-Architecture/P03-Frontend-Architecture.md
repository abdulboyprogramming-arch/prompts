# PROMPT 3 — Frontend Architecture: who owns the data, where state lives, what renders where

**Identifier:** FE-P03
**System:** 03-domains/frontend
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** A — reads the app and writes a design; changes nothing
**Depends on:** FE-P02
**Produces:** `FE_ARCHITECTURE.md`: route and component structure, the state ownership map, the data-flow per flow, the render-mode decision per route, and the decisions with their rejected alternatives
**Inputs:** {{PROJECT_PATH}} (optional: TEAM_STRUCTURE, EXISTING_ADR)
**Est. effort:** 2–3 h

---

## 1. Role and mandate

You decide where things live before they are built: which component owns a piece of
state, which layer talks to the server, which routes render on the server, and where the
code splits.

Frontend architecture is mostly a state-ownership problem wearing a component hat. A
codebase with two sources of truth for the same list — a cache and a `useState` copy —
produces bugs that no amount of component tidying fixes.

## 2. Objective and scope

**Produce:** `FE_ARCHITECTURE.md` containing:

1. **Route map.** Every route touched by this work, its render mode (from `FE-P01`), its
   loading and error boundary, and its code-splitting boundary.
2. **Component inventory.** Per component: responsibility, the states it renders (by ID
   from `FE_UX_GOALS.md`), whether it is presentational or connected, and whether it is
   reused or new.
3. **State ownership map.** For every piece of state: owner (server cache, URL, form,
   component, global store), lifetime, and who may write it. One owner each.
4. **Data flow per flow.** Where the request originates, what caches it, what invalidates
   it, and what the user sees while it is in flight.
5. **Boundaries.** Where error and suspense boundaries sit, and what a failure inside
   each one takes down with it.
6. **Decisions** with context, choice, rejected alternatives, and reversal condition.
7. **Debts and violations** in the existing tree that this design must not perpetuate.

Out of scope: the code (`FE-P04`), the cache policy details (`FE-P05`), test design
(`FE-P06`).

## 3. Prerequisites and inputs

- `{{PROJECT_PATH}}` — the app. **Discovered here:** the router configuration, existing
  component conventions, the state libraries already installed, and the folder layout.
- `{{TEAM_STRUCTURE}}` (optional) — who owns which area, if the app is split by team.
- `{{EXISTING_ADR}}` (optional) — prior architecture decisions, so you do not reverse
  one by accident.

## 4. Workflow

1. **Read the router first.** Route definitions tell you the app's real structure; the
   folder tree tells you where someone once put files. Note nested layouts, catch-alls,
   and route-level guards.
2. **Assign one owner per piece of state.** Server data belongs to a query cache; the URL
   owns anything a user should be able to link to or reload into; forms own their own
   draft; components own ephemeral UI state. Anything in two places at once is a bug with
   a schedule.
3. **Decide what goes in the URL.** Filters, sort order, pagination, selected tab and
   search query are URL state if a user would expect to share or reload them. Write the
   decision per item, including the ones you keep out and why.
4. **Choose the render mode per route and write the consequence.** Server rendering
   forbids browser-only APIs at module scope and moves data-fetching earlier; client-only
   means a loading state is mandatory and SEO is off the table. Where a route mixes the
   two, say where the boundary is.
5. **Place the boundaries.** One error boundary per independently failing region, not one
   for the app; a failure in a sidebar must not blank the page. Note which errors are
   retryable from the boundary and which need a reload.
6. **Set the splitting points.** By route by default; by interaction for heavy widgets
   behind a click; never by component-size guessing. State the budget effect each split
   is expected to have, since `FE-P06` will measure it.
7. **Check each flow against the map.** Walk `FE-P02`'s flows through the components and
   confirm no step needs state that has no owner, and no state has two writers.
8. **Record each decision** with the alternative you rejected. "We used a global store
   because it existed" is a debt, not a decision — record it in the debts list instead.

## 5. Decision rules and evidence standard

- **One owner per state.** Two owners is a synchronisation bug; zero owners is a
  component that fetches in a render path.
- **Server state is not client state.** Caching, deduping, retrying and invalidating
  belong to a query layer, not to `useEffect` plus `useState` in each component.
- **URL is the cheapest persistence.** If a user would be annoyed to lose it on reload,
  it belongs in the URL.
- **Fetch in the route, not in the leaf.** A component that fetches is a component that
  cannot be tested without a network mock and cannot be rendered twice cheaply.
- **A boundary per failure domain.** Boundaries are cheap; a blank page is not.
- **Follow the existing conventions or record the exception.** A new pattern needs a
  reason in the decision record, not preference.
- **Accessibility is structural.** Landmark roles, heading order and focus order are
  decided by the component tree; a `<div>` soup layout cannot be fixed in `FE-P06`.

## 6. Verification

- Every route has a render mode, a loading path, an error boundary and a split point.
- Every component states its responsibility, the state IDs it renders, and its kind.
- Every piece of state has exactly one owner, a lifetime, and its permitted writers.
- URL state is decided per item, including the exclusions.
- Each flow walks from route to component to data source with no orphan step.
- Boundaries map to independent failure regions, each with its retry behaviour.
- Each decision has a rejected alternative and a reversal condition.
- Existing violations are listed by path, and this design adds none.

## 7. Failure handling

- **The app has no router** (single-page with manual view switching): record the current
  mechanism, propose the smallest routeable structure, and flag that URL state is
  unavailable until it exists. Do not build a router as a side effect of a feature.
- **Two state libraries are already installed** (a half-finished migration): pick one for
  new work, name the other as debt with an owner, and forbid new writes to it.
- **A flow needs state that must survive a reload and a cross-tab change.** Record it as
  persistence, name the mechanism and the storage medium, and hand the security
  constraint to `FE-P05` — sensitive data in `localStorage` is a finding.
- **The route is a catch-all rendered by a CMS or a widget host.** Record how the
  catch-all resolves its content, and which of the matrix states the host guarantees
  versus which this app must handle.
- **The component library cannot express a required state** (no disabled styling, no
  error variant): record the gap, decide between extending the library and a local
  composition, and name who owns the long-term fix. Do not fork the library silently.

## 8. Security and authorisation

Risk class A. Authorisation is enforced by the server; a route guard is a usability
improvement, and the artifact must say so rather than implying the client check is a
control. Record where the app would cache or persist sensitive data, and record the trust
boundary for any third-party script named in `FE-P01`. Never render secrets into the
bundle as a "temporary" measure.

## 9. Completion criteria

- [ ] Route map with render mode, loading path, boundary and split point.
- [ ] Component inventory with responsibility, state IDs and kind.
- [ ] State ownership map with one owner, lifetime and writers per item.
- [ ] URL state decided per item, exclusions included.
- [ ] Flow walk through components and data sources with no orphans.
- [ ] Boundary placement per failure region with retry behaviour.
- [ ] Decision records with rejected alternatives and reversal conditions.
- [ ] Existing violations listed; no new ones introduced.

## 10. Deliverables and handover

`FE_ARCHITECTURE.md` at the app root. `FE-P04` builds the components as mapped.
`FE-P05` implements the state owners and the cache behaviour the map specifies, and may
not add a second owner. `FE-P06` tests the flows and the boundaries, and measures the
split points against their expected effect. `FE-P07` uses the debts list as the honest
limitations section of the handoff.
