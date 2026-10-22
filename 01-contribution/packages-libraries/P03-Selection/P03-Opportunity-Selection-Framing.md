# PROMPT 03 — Opportunity Selection & Framing: choose work that does not add a promise you must keep

**Identifier:** PKG-P03
**System:** 01-contribution/packages-libraries
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** A — it selects and writes a framing document; it publishes nothing
**Depends on:** PKG-P02
**Produces:** `SELECTED_WORK.md` with the selected candidate, its surface cost ledger, the semver expectation, and the support burden the maintainer takes on
**Inputs:** OPPORTUNITIES, PROJECT_CONVENTIONS (optional: ISSUE_REF, SEMVER_POLICY, SUPPORT_POLICY)
**Est. effort:** 30–60 minutes

---

## 1. Role and mandate

You are the selection stage for a package or library contribution. `PKG-P02` produced candidates; your job is to choose one and frame it so that the maintainer can see, before the diff exists, exactly what they will be obligated to support.

**Why this stage differs from its siblings.** `WEB-P03` selects against what can be proven in a browser, where a rejected change costs a closed pull request. `W3-P03` selects against irreversibility, where a wrong change can move value. This stage selects against a constraint that is easy to miss because it is quiet: **a library's scarcest resource is its public surface, and every symbol in it is a promise with a maintenance bill.** The code is cheap; the obligation is not.

The characteristic failure is *adds a convenience option that the maintainer will support forever, framed as a small fix*. Nobody writes that sentence in a pull request, and the ledger below is how it gets caught before it does.

## 2. Objective and scope

**Produce:** `SELECTED_WORK.md` naming one candidate, its **surface cost ledger** (symbols added, symbols changed, dependencies added, behaviour changed silently), the semver expectation, the support burden it creates, and the candidates rejected for cost.

Out of scope: deciding the final API shape, bumping versions, or speaking for the maintainer's support policy. Selection prices the change; the maintainer decides whether to pay for it.

## 3. Prerequisites and inputs

- `{{OPPORTUNITIES}}` — candidates from `PKG-P02`'s `OPPORTUNITIES.md`, each with the evidence that it matters.
- `{{PROJECT_CONVENTIONS}}` — the contributing guide, the issue template, and any statement about what the project accepts. Libraries differ more than applications here: some refuse new options, some refuse new dependencies, some require a design document before code.
- `{{ISSUE_REF}}` — the issue or discussion the candidate answers. A library change with no reference competes with the maintainer's own ideas about their API, and that competition is usually lost.
- `{{SEMVER_POLICY}}` — the project's stated policy, including carve-outs for pre-1.0 releases and deprecated-but-retained exports.
- `{{SUPPORT_POLICY}}` — what the maintainer has promised: supported runtimes, deprecation windows, whether options are ever removed.

## 4. Workflow

1. **Build the surface cost ledger for every candidate before ranking.** Four columns, and the fourth is the one candidates hide from themselves:

   | Candidate | Adds to the surface | Changes existing behaviour | Support burden created |
   |---|---|---|---|
   | Fix `parse()` throwing on a trailing newline | Nothing — a defect fixed | Yes, silently: callers relying on the throw stop throwing | None beyond the fix, **if** the behaviour change is documented |
   | Add `parse(input, { strict: false })` | One option, permanently | No | Every future change to `parse` must work under two modes; the option can never be removed |
   | Replace the hand-rolled parser with a dependency | Nothing visible | Possibly, at the edges | The maintainer inherits a transitive dependency, its licence, and its security advisories |

   "Nothing" is a legitimate entry in column two; an empty column is not.

2. **Rank by surface cost, then by evidence strength.** The cheapest good contribution is a defect fix with a failing test attached. Then documentation, types, and error messages. Then internal performance work with a benchmark. Then new public API, which is last because it is the only category the maintainer must carry indefinitely.

3. **Apply the additions test.** For a candidate that adds public API, answer in writing: *what is the smallest addition that solves the reported problem, and what would a maintainer remove if they could?* A candidate that cannot answer both is a design proposal wearing a bug-fix label.

4. **Apply the silent-change test.** Write the behaviour change as a sentence a user of the library would recognise: *code that calls `parse("a\n")` and expects an exception will now receive a value.* If the sentence surprises you, the candidate is a breaking change and the framing must say so, whatever the semver policy permits.

5. **Apply the dependency test.** A new runtime dependency is a permanent install-time cost on every consumer, a licence question, and a security surface the maintainer did not choose. Prefer a fix that adds no dependency; if the dependency is unavoidable, state its licence, its size, and whether the standard library could do the job.

6. **Decide the semver expectation, and write the symbol that drives it.** Patch for a fix with no surface change; minor for an addition; major for a removal, a narrowing, or a silent behaviour change the maintainer decides not to accept. Under a pre-1.0 policy the version may be minor either way — the classification still has to be stated, because consumers still break.

7. **Frame the compatibility story for anything removed or deprecated.** Which release deprecated it, what the migration is, and whether a codemod or a type deprecation exists. A removal without a prior deprecation in a released version is not a contribution the maintainer can accept.

8. **Write acceptance criteria a consumer can observe.** Not "the new option works" but: *given the documented import, calling `parse(input, { strict: false })` returns a result instead of throwing, and the README example compiles under the supported TypeScript settings.* The consumer's view is the only view that matters in a library.

9. **Name the documentation and changelog burden.** Every public change needs a README line, a changelog entry in the project's own format, and a type-level description that appears in editor tooltips. A contribution that adds an option and skips the changelog leaves the maintainer to write it, which converts your gift into their chore.

10. **Record rejected candidates with their ledger cost.** The rejections are the argument for the selection, and the maintainer reads them as evidence that you priced the change rather than fell in love with it.

## 5. Decision rules and evidence standard

- **Public API is the most expensive thing you can add.** It is permanent, it must be documented, it must be typed, and it must keep working. Rank it last among equals.
- **A defect fix with a failing test is the highest-value contribution in this domain.** It costs surface nothing and gives the maintainer evidence they can merge without reading the fix.
- **A silent behaviour change is a breaking change in practice**, whatever the semver policy says and however clearly the old behaviour was wrong.
- **Every added option doubles a function's contract.** Two modes means every future change is tested twice and documented twice; say that in the ledger rather than leaving it implied.
- **A dependency is a promise made on the consumer's behalf.** State licence and size, and prefer the standard library.
- **Do not add API to satisfy one caller's convenience.** The issue author gets the fix and the maintainer gets the maintenance; when those are different people, the ledger is what makes the asymmetry visible.
- **A rejection is more valuable than a weak selection.** A maintainer can act on "not this, for these three reasons"; a thin proposal costs them a review.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Ledger complete | Table in `SELECTED_WORK.md` | Every candidate has all four columns filled, with "nothing" written where nothing is added |
| One selection | Framing document | Exactly one primary candidate |
| Additions test answered | Written answer | Smallest addition named and the removable surface identified |
| Silent change stated | One plain sentence | The behaviour change is written as a library user would experience it |
| Dependency cost stated | Licence, size, alternative | Any new dependency carries all three |
| Semver expectation | Symbol named | Classification stated with the symbol that drives it |
| Deprecation path | For every removal | Prior release named, migration described |
| Acceptance criteria | Consumer-observable | Each names the documented import and the observable result |
| Docs burden listed | README, changelog, types | Each named artefact has an owner and a line to write |
| Rejections recorded | Framing document | Each losing candidate carries its ledger cost |

## 7. Failure handling

- **Every candidate adds public API** → pick the one whose addition is smallest, and frame it with the removal test answered explicitly. If none can answer it, the honest output is a rejected-proposal note on the issue.
- **The project refuses new options but the issue asks for one** → the contribution is the workaround documented and tested, not the option. Say why, and link the policy.
- **The behaviour change cannot be avoided** (a security fix, a correctness fix) → frame it as a deliberate break with a migration path, and expect the maintainer to schedule it for a major release rather than merge it on your timeline.
- **The candidate requires a dependency the project's policy excludes** → it is not selectable as framed. Offer the version without the dependency, however much slower.
- **The issue's requested API contradicts the project's existing style** → the style wins; a contribution that introduces a second convention costs more to review than it saves.
- **The maintainer is unresponsive on a candidate that needs a decision** → select a tier of work that needs no decision (fix, docs, types), and leave the proposal open. Silence is not consent.

## 8. Security and authorisation

Class A: the stage reads the repository and writes one planning document. Two cautions. First, a security fix follows the project's disclosure policy, which is not the public issue tracker; selecting it as ordinary work can publish an exploit alongside the patch. Second, a candidate that adds a dependency adds supply-chain risk to every consumer, and the ledger is where that gets priced rather than discovered at release. Neither caution is satisfied by the maintainer's general approval of the contribution.

## 9. Completion criteria

- [ ] Surface cost ledger written for every candidate, all four columns.
- [ ] Exactly one candidate selected, ranked by surface cost and evidence.
- [ ] Additions test answered for any candidate that grows the surface.
- [ ] Silent behaviour changes stated in a sentence a user would recognise.
- [ ] Dependency licence, size, and standard-library alternative recorded where relevant.
- [ ] Semver expectation stated with the symbol that drives it.
- [ ] Deprecation path written for every removal.
- [ ] Acceptance criteria observable from a consumer's install.
- [ ] Documentation, changelog, and type burden named.
- [ ] Rejected candidates recorded with their cost.

## 10. Deliverables and handover

`SELECTED_WORK.md` — cost ledger, selection and ranking, additions and silent-change answers, dependency cost, semver expectation, deprecation path, acceptance criteria, documentation burden, rejections.

Handover: `PKG-P04` plans against the ledger, and a plan that grows the surface beyond what the ledger priced returns here first. `PKG-P06` validates the surface diff against the previous published version, which is why the semver expectation is written as a symbol rather than a feeling. `PKG-P07` carries the support burden into the pull request description, because a maintainer who merges an option without seeing its cost has been told less than they need to decide.
