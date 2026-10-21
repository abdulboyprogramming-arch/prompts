# PROMPT 04 — Planning & API Impact: plan the release, not just the patch

**Identifier:** PKG-P04
**System:** 01-contribution/packages-libraries
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** A — it writes a plan; it publishes nothing
**Depends on:** PKG-P03
**Produces:** `PLAN.md` with the surface delta the change is allowed to make, the deprecation sequence where one is needed, the test layer per behaviour, and the choreography of release artefacts
**Inputs:** SELECTED_WORK, SEMVER_EXPECTATION (optional: CHANGELOG_FORMAT, SUPPORT_POLICY, DOWNSTREAM_CONSUMERS)
**Est. effort:** 30–60 minutes

---

## 1. Role and mandate

You are the planning stage of a package or library contribution. `PKG-P03` priced the change; your job is to design it as a **release**, with the surface delta fixed in advance and every artefact the maintainer must publish accounted for.

**Why this stage differs from its siblings.** `WEB-P04` plans against a state matrix and `W3-P04` against a deployment sequence. Both plan a change to a system the contributor can observe. This stage plans a change to **an interface other people compiled against**, which means the plan has to answer a question neither sibling faces: *what will consumers have to do when this ships, and when do we tell them?*

The characteristic failure is *a plan for the implementation with the release as a final line*, and it produces a PR that is technically correct and practically unshipable — a break with no deprecation, an option with no documentation, a fix that cannot go in a patch because nobody checked whether it could.

## 2. Objective and scope

**Produce:** `PLAN.md` with the allowed surface delta (symbols added, changed, removed — and nothing else), the deprecation sequence where a removal is involved, the test layer per behaviour including one public-entry smoke test, and the release choreography: which artefacts change, which version range this can ship in, and what consumers will read.

Out of scope: writing code, deciding the version number, or negotiating with the maintainer. The plan states the release consequence and lets the maintainer choose the release.

## 3. Prerequisites and inputs

- `{{SELECTED_WORK}}` — from `PKG-P03`: the surface cost ledger, the semver expectation with its driving symbol, and the support burden accepted.
- `{{SEMVER_EXPECTATION}}` — the classification. The plan is checked against it and may not silently escalate it.
- `{{CHANGELOG_FORMAT}}` — the project's own format and section names, copied from its last three entries.
- `{{SUPPORT_POLICY}}` — the runtime range, the deprecation window, and whether options are ever removed. It constrains both the sequence and the ship window.
- `{{DOWNSTREAM_CONSUMERS}}` — known large consumers, if they exist. A break that inconveniences three well-known projects is priced differently from one that inconveniences an unknown number.

## 4. Workflow

1. **Fix the allowed surface delta in a table before planning anything else.** Added, changed, removed, each with its justification and the ledger entry it corresponds to. This table is the boundary: an implementation that touches a symbol not listed here has changed the plan.

   | Delta | Symbol | Justification | Ship window |
   |---|---|---|---|
   | None | `parse()` behaviour fix | Defect against documented behaviour; no signature change | patch |
   | Add (optional) | `parse(input, options?)` | Not planned — rejected at selection | — |

2. **Decide the deprecation sequence for anything removed or renamed.** Which release marks it, what the mark is (a type-level annotation, a runtime warning, a documentation note), how long it stays, and what the migration path is. A removal with no prior deprecation is not planable in a library that promises semver: it is a major, and the plan says so explicitly rather than letting it arrive as a surprise at release time.

3. **Plan the test layer per behaviour, with exactly one public-entry test.** Unit tests for logic, type tests where the project has them, and at least one test that imports the documented entry point and calls the changed function. A suite that only imports internals will pass while the package is unimportable.

4. **Plan the packaging check whenever the change touches entry points, types, or module format.** Which build command, which clean install, which runtime versions. It is a step in the plan, not a discovery during validation.

5. **Plan the four artefacts as steps, with the exact file and the exact change.** Type declaration or doc comment, README line or example, changelog entry in the project's format, and any guide that shows the old call. Each is a step with a verification; none is a "and update docs".

6. **Answer the ship-window question, and plan a subset if the answer is "not yet".** If the full change needs a major, identify the part that can ship in a patch and plan that first. A contribution that waits for a major release competes with the maintainer's roadmap and usually loses.

7. **Plan the consumer communication.** The changelog entry drafted in advance, and — where the project has a mailing list, a migration guide, or a deprecation policy — the sentence consumers will see. If a break needs a codemod or a migration note, plan who writes it.

8. **Plan the compatibility surface the change must not disturb**, and check it explicitly: unsupported runtimes, peer dependency ranges, the module formats shipped, and any documented behaviour that is not in the type system. Silent behaviour changes live in the last category.

9. **Name the risks that would change the plan**, each with a trigger and a response: a maintainer who wants the API shaped differently, a consumer who depends on the behaviour being removed, a runtime that cannot support the implementation, a dependency that would have to be added.

10. **Write the definition of done as the delta table plus the artefacts.** The plan is complete when the allowed delta is fixed, the artefacts are enumerated, and the ship window is answered.

## 5. Decision rules and evidence standard

- **The delta table is a contract with the implementation.** A symbol that is not in it does not change.
- **Removal requires a prior deprecation in a released version.** Otherwise the plan says "major" and the maintainer decides when.
- **One public-entry test is mandatory.** It is the only test that proves the package can be consumed.
- **Packaging is a planned step.** A clean install is not something to discover at release.
- **Four artefacts, four steps.** Types, README, changelog, examples; a plan that names them as one line produces three of them.
- **Ship window before completeness.** A patch-shippable subset today beats a better change next quarter.
- **Silent behaviour changes are in scope of the plan.** If the type system does not show it, the plan names it and the changelog records it.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Delta table fixed | Symbols with justification | Every added, changed, removed symbol listed, or "none" stated |
| Deprecation sequence | Prior release and mechanism | Removal has a marked prior release with a migration path |
| Test layers | One per behaviour | Every behaviour has exactly one layer |
| Public-entry test | Import from the documented path | At least one planned test calls through the entry point |
| Packaging step | Build and clean install | Present whenever entry points or types change |
| Four artefacts | Named files | Type, README, changelog, and examples each a step |
| Ship window | Patch, minor, major | Answered, with a subset identified when the answer is "not yet" |
| Consumer communication | Changelog draft | Entry drafted in the project's format |
| Compatibility surface | Runtimes, peers, formats | Each checked, including behaviour not visible in types |
| Risks | Trigger and response | Two or three, each actionable |

## 7. Failure handling

- **The implementation cannot express the change within the allowed delta** → return to `PKG-P03`. Widening the delta during planning is the same decision made with less information.
- **The removal has no deprecation behind it** → plan it as a major with a migration note, and expect the maintainer to schedule it. Do not plan a patch that quietly breaks consumers.
- **The project has no release process documented** → plan against the last three releases' shape, and say that the process is inferred.
- **A well-known consumer depends on the behaviour being fixed** → the plan records the dependency and proposes the deprecation path; the maintainer decides whether to break it.
- **The change needs a dependency the policy excludes** → the plan is not viable as written; return to selection with the constraint recorded.
- **The maintainer wants the API reshaped** → rewrite the delta table first, then replan. Editing the implementation before the table is how a plan and a codebase disagree at review.

## 8. Security and authorisation

Class A: the stage writes a plan. Two cautions. First, a security fix planned in the open tells consumers which version to diff against; the plan records that the release timing is coordinated with disclosure, and the changelog entry says no more than the advisory does. Second, a dependency added for the implementation is a supply-chain decision; if the plan includes one, it names the licence, the maintenance status, and the alternative considered.

## 9. Completion criteria

- [ ] Allowed surface delta fixed in a table, including "none".
- [ ] Deprecation sequence written for anything removed or renamed.
- [ ] Test layer chosen per behaviour, with one public-entry test.
- [ ] Packaging step planned where entry points or types change.
- [ ] Four release artefacts each planned as a step.
- [ ] Ship window answered, with a patch-shippable subset where relevant.
- [ ] Changelog entry drafted.
- [ ] Compatibility surface checked: runtimes, peers, formats, silent behaviour.
- [ ] Risks carry triggers and responses.
- [ ] Definition of done is the delta plus the artefacts.

## 10. Deliverables and handover

`PLAN.md` — delta table, deprecation sequence, test layers, packaging step, four artefacts, ship window, changelog draft, compatibility surface, risks.

Handover: `PKG-P05` implements to the delta table and re-diffs the exports as it works; a symbol outside the table is a planning finding. `PKG-P06` diffs the built surface against the last published version and turns the plan's expectations into a verdict. `PKG-P07` writes the description from the delta table and the changelog draft, which is why both exist before the code does.
