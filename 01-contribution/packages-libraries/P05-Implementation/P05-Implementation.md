# PROMPT 05 — Implementation: every line you export is a line you support

**Identifier:** PKG-P05
**System:** 01-contribution/packages-libraries
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B — it writes library code and runs the local suite; publishing is Category C
**Depends on:** PKG-P04
**Produces:** a branch with the change, plus `IMPLEMENTATION.md` recording the exported-surface delta as it changed, the compatibility decisions, and the documentation, type, and changelog lines the diff now requires
**Inputs:** PLAN, SEMVER_EXPECTATION (optional: BUILD_COMMAND, TEST_COMMAND, TYPES_CONFIG)
**Est. effort:** 2–6 hours

---

## 1. Role and mandate

You are the implementation stage of a package or library contribution. The plan specified the surface cost and the release window; your job is to write the change so that the surface does exactly what the plan priced — no more.

**Why this stage differs from its siblings.** `WEB-P05` implements under state coverage, where an unbuilt state is visible. `W3-P05` implements under invariants, where a broken one can move value. This stage implements under **an exported surface**, where the characteristic failure is quieter than either: *a helper exported for convenience, a type widened to make the code compile, and a test that imports from `src/`.* None of those break anything today. All three become permanent in the next release.

A library's implementation is judged by different evidence than an application's: the **public entry point** is the only thing a consumer can reach, the **type signature** is the documentation most consumers read, and the **build output** is the product. Code that is correct in `src/` and wrong after packaging is a shipped defect.

## 2. Objective and scope

**Produce:** a branch where the exported surface differs from `main` only by what the plan priced, types are written as the consumer reads them, tests run against the public entry point, and `IMPLEMENTATION.md` records the surface delta, the compatibility decisions, and every artefact the change obliges you to update.

Out of scope: publishing, bumping the version, or changing the API shape the plan priced. A shape the code needs but the plan did not allow returns to `PKG-P03`.

## 3. Prerequisites and inputs

- `{{PLAN}}` — `PLAN.md` from `PKG-P04`: entry points, deprecation sequence, test layers, and release choreography.
- `{{SEMVER_EXPECTATION}}` — the classification and driving symbol. The implementation is checked against it: a change that started as a patch and now alters a signature has moved.
- `{{BUILD_COMMAND}}` — the project's build, so the artefact you test is the artefact a consumer installs.
- `{{TEST_COMMAND}}` — the repository's own suite, run the way CI runs it.
- `{{TYPES_CONFIG}}` — the TypeScript or language-level type settings, including strictness and the module resolution mode a consumer will use.

## 4. Workflow

1. **Diff the exported surface before writing code, and again after.** Record the entry-point exports (or the equivalent in the language) as a list. At the end, list them again and compare. This is the cheapest guard against an accidental export, and it is the one thing in this stage that must not be skipped.

2. **Assume nothing is exported by default.** A helper shared between two internal functions belongs outside the entry point; a type used only in a signature the consumer never constructs belongs internal. Export only what the plan priced, and consult the project's own conventions for whether it exports types from a barrel or a separate path.

3. **Write the type as the consumer reads it.** Hover text is the documentation most users see. Narrow types that tell the truth beat `any` that compiles; a union that names the real cases beats a string. Where a type must be broad to stay compatible, say so in `IMPLEMENTATION.md`.

4. **Preserve behaviour at the edges, not just in the middle.** A fix that changes how an empty input, a null, a very large number, or a trailing newline behaves is a behaviour change even though no signature moved. Test the edges the issue reports, and the adjacent ones the issue implies.

5. **Keep optional parameters optional and defaults unchanged.** Adding a parameter with a default is compatible when it is last and the existing calls still parse; changing a default silently changes behaviour for every consumer who relied on it. If the plan calls for a new default, it is a break and the changelog says so.

6. **Test through the public entry point, not through `src/`.** A test that imports an internal module proves the internal module works and says nothing about whether a consumer can reach it. One smoke test per public change, importing what the documentation says to import, catches the packaging defects that source-level tests cannot.

7. **Run the build and test the artefact when the change touches packaging.** If the change affects entry points, `exports`, type declarations, or the module format, install the packed artefact into an empty project and import it. The suite inside the repository's `node_modules` proves less than one that does not use it.

8. **Update the four artefacts the change obliges, in the same commit.** The type declaration or doc comment, the README line or example the change makes stale, the changelog entry, and any guide that shows the old call. A library PR missing one of these leaves the maintainer to write it, which converts a fix into homework.

9. **Never add a dependency the plan did not price.** A runtime dependency is a permanent install cost, a licence question, and a security surface on every consumer; if the implementation cannot proceed without one, stop and return to planning.

10. **Keep deprecations additive.** Mark the old path with the project's mechanism (`@deprecated`, a console warning, a documentation note) and route it to the new one. Do not remove the old path in the same release that introduces its replacement.

11. **Run the repository's checks and record the outputs.** Tests, type check, lint, and build. Then check the surface delta one final time against `{{SEMVER_EXPECTATION}}`.

12. **Do not bump, tag, or publish.** Versioning is the maintainer's release decision; the branch stops at a correct artefact.

## 5. Decision rules and evidence standard

- **The surface delta is the deliverable's spine.** Every export added, removed, or narrowed appears in `IMPLEMENTATION.md`, whether or not the plan predicted it.
- **If the surface moved beyond the plan, stop.** A widened type or a new export is a pricing decision, not an implementation detail.
- **Tests import the public entry point.** Internal imports in tests hide packaging defects and make refactors look like breaks.
- **The artefact is the product.** A clean source tree with a broken `exports` map is a broken release.
- **Documentation, types, changelog, and examples ship with the code.** Four artefacts, one commit, no exceptions for small changes.
- **Deprecation before removal, always.** A removal in the release that introduces the replacement breaks consumers at the worst possible moment.
- **No new dependency without a ledger entry.** Prefer the standard library, and say so when it is slower.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Surface diffed | Export list before and after | Every addition, removal, and narrowing recorded |
| Exports intentional | Entry-point review | Nothing exported that the plan did not price |
| Types as documentation | Hover review | Signatures state the real cases; no unexplained `any` |
| Edge behaviour | Tests at the boundaries | Empty, null, large, and malformed inputs covered |
| Defaults unchanged | Signature comparison | No default changed silently |
| Public-entry tests | Import from the documented path | Core changes smoke-tested through the entry point |
| Artefact tested | Packed install | Import and call succeed outside the repository |
| Four artefacts updated | File list | Types, README, changelog, and examples present |
| No new dependency | Diff review | Dependency set unchanged, or the change returned to planning |
| Deprecation additive | Diff review | Old path retained and marked, new path documented |

## 7. Failure handling

- **The plan's API shape cannot be implemented without a new export** → stop and return to `PKG-P03`. Convenience exports are how a surface grows one function at a time.
- **A type must widen to compile** → find the narrowing that caused it; if none exists, it is a compatibility decision for the plan, not a local fix.
- **The suite passes and the packed artefact fails** → the packaging is the defect. Fix the configuration and add a clean-install check to the plan's validation list.
- **A consumer-facing example no longer compiles** → update it in this commit; an example is tested code with no test suite, and shipping a stale one is a documentation defect with a compiler error attached.
- **A maintainer's convention conflicts with what you need** → follow the convention and record the friction. A convention changed by a contribution is a second review the maintainer did not ask for.
- **The change turns out to be breaking** → keep it as one PR and move the classification up, rather than splitting it into a compatible-looking series that cumulatively breaks consumers.

## 8. Security and authorisation

Class B: the stage writes library code and runs the local suite. Three cautions. First, installing your own packed artefact runs install scripts; use a disposable directory, not a workstation with credentials. Second, a security fix follows the project's disclosure policy — a public branch and a public PR can expose the defect before consumers can update. Third, a new dependency is a supply-chain decision for every consumer; record its licence and provenance, and never add one from an unmaintained or unverifiable source.

## 9. Completion criteria

- [ ] Export list captured before and after; delta recorded.
- [ ] Nothing exported that the plan did not price.
- [ ] Types written as consumer-facing documentation.
- [ ] Edge-case behaviour tested, including the cases the issue implies.
- [ ] No default changed silently.
- [ ] Core changes tested through the public entry point.
- [ ] Packed artefact installed and imported when packaging is touched.
- [ ] Types, README, changelog, and examples updated in the same commit.
- [ ] No dependency added without a ledger entry.
- [ ] Deprecations additive; nothing bumped, tagged, or published.

## 10. Deliverables and handover

The branch, plus `IMPLEMENTATION.md` — surface delta, type decisions, edge behaviour, artefact results, the four artefacts updated, and the final comparison against the semver expectation.

Handover: `PKG-P06` diffs the built surface against the last published version, which is why the delta is recorded here rather than reconstructed later. `PKG-P07` drafts the changelog entry from `IMPLEMENTATION.md` and the validation report; a mismatch between the two is the signal that the implementation did something the plan did not price.
