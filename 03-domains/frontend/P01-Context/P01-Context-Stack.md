# PROMPT 1 — Context & Stack: what the browser is actually being asked to do

**Identifier:** FE-P01
**System:** 03-domains/frontend
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** A — reads the app, its build config and its callers; changes nothing
**Depends on:** none (entry stage)
**Produces:** `FE_CONTEXT.md`: the surface and its users, the stack as it is actually configured, the render mode per route, the browser and device floor, and the constraints that bound every later decision
**Inputs:** {{PROJECT_PATH}} (optional: BROWSER_SUPPORT, DESIGN_SYSTEM, ANALYTICS_EXPORT)
**Est. effort:** 45–90 min

---

## 1. Role and mandate

You establish what this frontend is, for whom, on what device, and with which
constraints — before anyone designs a component or picks a state library.

Frontend work fails late, not early: it compiles, it looks right on the developer's
laptop, and it breaks on the browser the support contract still covers, the screen
reader the audit will use, or the route that renders on the server where `window` does
not exist. Your job in this stage is to make those constraints visible while they are
still cheap.

## 2. Objective and scope

**Produce:** `FE_CONTEXT.md` answering five questions:

1. **What surface is this?** Marketing site, authenticated app, dashboard, embedded
   widget, email template, or a hybrid. The answer sets the performance budget and the
   render mode before any code exists.
2. **Who uses it, on what?** The device and browser distribution you actually have, or
   `no analytics` if you do not. The support floor is a number, not a preference.
3. **What is the stack, as configured?** Framework, version, styling approach, design
   system or token source, state and data libraries, router, build tool, and test runner
   — read from the manifest and config, not from memory or the README.
4. **What does each route render, and where?** Server-rendered, statically generated,
   client-only, or edge. A page that is server-rendered and reads `localStorage` is a
   defect that only appears in production.
5. **What constraints bind the work?** Design system rules, i18n and locales, auth model,
   CSP and third-party scripts, accessibility commitments, and who reviews UI changes.

Out of scope: the flows themselves (`FE-P02`), component structure (`FE-P03`), any code.

## 3. Prerequisites and inputs

- `{{PROJECT_PATH}}` — the repository. **Discovered here:** `package.json` and its
  lockfile, the framework config, `tsconfig`, the styling and token files, the test and
  lint configuration, CI, and the browser-support declaration if one exists.
- `{{BROWSER_SUPPORT}}` (optional) — the declared support matrix. If absent, read
  `browserslist` or the framework's default and **say which default you inherited**,
  because it is usually older than the team believes.
- `{{DESIGN_SYSTEM}}` (optional) — the component library, or the token file. If absent,
  discover whether tokens exist; their absence is a finding, not a licence to invent.
- `{{ANALYTICS_EXPORT}}` (optional) — a device/browser breakdown. If absent, record
  `no traffic data`; do not guess the distribution.

## 4. Workflow

1. **Read the manifest and the lockfile.** Framework and major versions, the actual
   installed version rather than the range, peer-dependency warnings, and the scripts a
   contributor is expected to run. List what a fresh clone must do to build.
2. **Establish the render mode per route** by reading the router and the framework
   config: which routes are static, which are server-rendered per request, which are
   client-only. Record the consequence for each: what may not run there (browser APIs,
   secrets, `Date.now()` in rendered output), and where hydration mismatch can appear.
3. **Find the design system or admit there is none.** Token files, theme objects, the
   component library version. If the app styles with ad-hoc values, record it as a
   finding — every later "match the design system" instruction becomes unenforceable.
4. **Record the browser and device floor** with its source: `browserslist`, a support
   policy document, or the analytics distribution. State which CSS or JS features that
   floor excludes, and mark it `assumed` where you inferred it.
5. **Map the data contracts this UI consumes.** For each backend endpoint or SDK the
   frontend calls: its owner, whether it is typed, and where the schema lives. An
   untyped response is a runtime crash waiting for a field name change.
6. **Record the third-party surface.** Analytics, tag managers, chat widgets, fonts, and
   their load cost and privacy implication. These are usually the largest bundle
   contributors and are almost never in the performance conversation until they are.
7. **Name the constraints that will be cited later**: i18n mechanism and the locales
   shipped, auth token storage, CSP, and the accessibility commitment (WCAG level, if
   any) with its source.
8. **Mark every claim** `verified` (with path), `reported` (with who), or `unknown`.

## 5. Decision rules and evidence standard

- **The installed version is the fact, not the declared range.** `^18` with 18.2
  installed changes what APIs you may use.
- **Route render mode is a constraint, not an implementation detail.** It decides where
  state can live and which libraries are usable at all.
- **An absent design system is a blocker for "match the design", not permission to
  invent one.** Record the gap and route the decision to the design owner.
- **The support floor is the oldest browser in the data or the policy — whichever is
  older.** "It works in Chrome" is not a support statement.
- **Third-party script cost belongs in the budget** from this stage onward; discovering
  a 400 KB chat widget at `FE-P06` is discovering it too late.
- **No analytics is a finding.** Record it, and mark every device claim as an assumption.

## 6. Verification

- Framework, styling, state, router, build and test tooling listed with installed
  versions read from the lockfile.
- Every route has a render mode and, where it matters, the consequence written out.
- Design system or token source named, or its absence recorded as a finding.
- Browser and device floor stated with its source, and the excluded features named.
- Each consumed API has an owner and a typed/untyped verdict with the schema location.
- Third-party scripts listed with size and privacy implication, or `none`.
- i18n locales, auth token storage, CSP and accessibility commitment recorded, each with
  a source or `unknown`.

## 7. Failure handling

- **No manifest can be found** (static site, vendored build, or a snapshot): record the
  stack as `vendored, unverifiable`, list what can be seen in the served HTML, and stop
  before `FE-P03` — component work on an unbuildable tree produces diffs nobody can ship.
- **Two frameworks in one repo** (a half-finished migration): record both, which routes
  each owns, and which is the target. Do not plan new work in the one being retired.
- **The browser floor contradicts the framework's own requirement** (framework needs
  evergreen, policy promises IE-mode): record the contradiction and the number of users
  affected; escalate to the product owner rather than silently choosing.
- **Secrets or service credentials appear in frontend config.** Stop, record the file and
  the variable name only, and treat it as a security finding — every value in a client
  bundle is public. Do not paste the value anywhere.
- **The route list is generated or dynamic** (CMS slugs, catch-all routes): record the
  pattern and the render mode of the catch-all, and name the representative routes
  `FE-P02` should use.

## 8. Security and authorisation

Risk class A: read-only. Frontend code is public by construction — record where any
credential-like value is read, and never reproduce it. Do not copy customer data,
session cookies or tokens from a browser into the artifact; cite the key name and the
storage mechanism instead. If the app talks to a third-party API from the browser,
record whether that key is public-by-design and where the constraint is documented.

## 9. Completion criteria

- [ ] Surface and user distribution, or `no traffic data` with the assumption stated.
- [ ] Stack with installed versions from the lockfile.
- [ ] Render mode per route, with the consequence where it constrains state or APIs.
- [ ] Design system or tokens named, or their absence recorded as a finding.
- [ ] Browser/device floor with source and the features it excludes.
- [ ] Consumed APIs with owner and typing status.
- [ ] Third-party scripts with size and privacy implication.
- [ ] i18n, auth storage, CSP and accessibility commitment recorded with sources.

## 10. Deliverables and handover

`FE_CONTEXT.md` at the app root. `FE-P02` needs the surface, the representative routes
and the browser/device floor — those decide which flows and states matter. `FE-P03`
needs the render mode per route and the design system, because both constrain where
state can live. `FE-P06` needs the browser floor, the third-party surface and the
accessibility commitment to test against. Anything marked `unknown` travels with the
handover rather than being quietly resolved downstream.
