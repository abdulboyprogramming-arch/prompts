# PROMPT 01 — Context & Project Understanding: the run command is the instrument

**Identifier:** WEB-P01
**System:** 01-contribution/web/general
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A — reads the repository and starts the app locally; changes nothing that is committed
**Depends on:** none (entry stage)
**Produces:** `WEB_CONTEXT.md`: stack, routing, component conventions, the run command, and the quality gates a change must pass
**Inputs:** REPOSITORY_PATH (optional: BASELINE_BROWSERS, A11Y_TARGET)
**Est. effort:** 40–90 minutes

---

## 1. Role and mandate

You are the entry stage of a contribution to a web project. Your job is to get the
application running and to write down how it is built, because every later stage in
this system either observes the running app or edits it. A web defect that cannot
be reproduced in a browser is a guess about code.

**Why this stage differs from its siblings.** `PKG-P01` establishes a contract with
consumers it cannot see. `W3-P01` establishes an immutable on-chain state model.
A web project is neither: it is a **running system**, and its defects appear as a
wrong pixel, a broken route, or a slow interaction. The instrument is the run
command. Without it, `WEB-P02` degrades to a code review, and it must say so.

## 2. Objective and scope

**Produce:** `WEB_CONTEXT.md` answering four questions with citations:

1. **What kind of app is this, and in what stack?** Framework and version, language,
   styling approach, state management, data layer, build tool.
2. **How do you run it?** The exact commands for install, dev server, build, test,
   lint and type-check, copied from configuration; the port; and any required
   environment variables, named but never valued.
3. **How is it structured?** Routing model, component conventions, where shared
   state lives, and the boundary between server and client rendering.
4. **What are the quality gates?** Browser support, accessibility target,
   performance budget, and the CI jobs that must pass.

Out of scope: finding defects, choosing a contribution, and editing the app. Those
are `WEB-P02` and later.

## 3. Prerequisites and inputs

- `{{REPOSITORY_PATH}}` — a clone at the default branch. **Discovered here:** the
  manifest, lockfile, framework configuration, CI workflows, and the source tree.
- `{{BASELINE_BROWSERS}}` (optional) — the browsers a change must support. If the
  repository states a support matrix in `browserslist`, a Babel target, or a
  documented policy, that is the answer; cite it.
- `{{A11Y_TARGET}}` (optional) — the accessibility level the project claims. Look
  for it in the contribution guide, a lint configuration, or test assertions
  before asking.

## 4. Workflow

1. **Identify the rendering model first.** Server-rendered, statically generated,
   client-side, or hybrid. The answer changes where a defect can live, and it is
   visible in the framework configuration, not in the README.

2. **Install and start the app.** Follow the lockfile's own instructions
   (`npm ci`, `pnpm install --frozen-lockfile`, `yarn install --immutable`). Record
   every command and its outcome, including the failure if one occurs. Note the
   port actually bound, not the port the docs claim.

3. **Enumerate the routes from the router configuration.** For each, record the
   file that defines it, whether it is public or authenticated, and whether it
   renders on the server. A route list taken from the navigation menu is
   incomplete; the router is the source.

4. **Map the data layer.** Where requests are made, how they are cached, how errors
   surface to the user, and what happens while data loads. Record the loading and
   error states as they are implemented, not as they are described.

5. **Record the component conventions.** File naming, styling method, prop typing,
   and whether a design-system package is used. Cite two components as examples so
   a later stage can imitate the house style rather than invent one.

6. **Establish the gates.** The exact commands for test, lint, type-check and
   build, each copied from `package.json` scripts or CI. The browser support range,
   the accessibility target, and any bundle-size or Lighthouse budget enforced in CI.

7. **Write `WEB_CONTEXT.md`** with the four sections, the command table with
   observed outcomes, and an open-questions list.

## 5. Decision rules and evidence standard

- **A command is verified only when it ran.** Record the exit status. A command
  copied from a README that was never executed is `unverified`, and that label
  matters to every later stage.
- **Configuration outranks documentation** for ports, routes, browsers and
  budgets. Where they disagree, record both and say which you would trust.
- **Never record an environment variable's value.** Name the variable and the file
  that defines it, and note whether the app runs without it.
- Label every claim `verified` (command or `path:line`) or `inferred`.

## 6. Verification

- The dev server starts from a clean install, and the URL and port are recorded.
- Every route in `WEB_CONTEXT.md` resolves to a router entry with `path:line`.
- All four gate commands are listed with an observed exit status, or an explicit
  `unverified` and the reason.
- A reader who has never seen the repository can start the app from this file alone.

## 7. Failure handling

- **Install fails** (native dependency, private registry, missing toolchain): record
  the error verbatim, continue reading the code for the remaining sections, and
  mark the run command `blocked`. Say plainly that browser-observed evidence will
  be unavailable to `WEB-P02`.
- **The app needs secrets to boot:** name the variable, note the service it belongs
  to, and stop. Do not ask the user for a value in the artifact, and do not commit
  a placeholder that looks like one.
- **Multiple apps in one repository:** record each workspace's run command and pick
  the one the task names; list the others as out of scope for this run.
- **No CI configuration:** record `no automated gates found` rather than assuming
  the commands in the README are the gates.

## 8. Security and authorisation

Risk class A: read-only and local execution. Start the app on a local port bound to
`127.0.0.1`, never on a public interface. Do not paste API keys from `.env` files
into the artifact, the console or a screenshot; cite the variable name only. Do not
run a deployment command.

## 9. Completion criteria

- [ ] Rendering model identified with the configuration that proves it.
- [ ] Install, dev, build, test and lint commands recorded with observed outcomes.
- [ ] Routes enumerated from the router, each with `path:line`.
- [ ] Gates (browsers, accessibility, budgets) recorded with their source.
- [ ] Open questions listed, especially anything `WEB-P02` needs and does not have.

## 10. Deliverables and handover

`WEB_CONTEXT.md` at the repository root. `WEB-P02` needs from it: the run command
and port (without them it cannot reproduce anything), the route list, the data
layer map, and the accessibility and browser targets that decide what counts as a
defect.
