# PROMPT 06 — Validation & Compatibility: prove you did not break anyone's build

**Identifier:** PKG-P06
**System:** 01-contribution/packages-libraries
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A — it builds, installs, and tests; it does not publish
**Depends on:** PKG-P05
**Produces:** `VALIDATION.md` with the public-surface diff, the compatibility verdict, and the consumer smoke tests
**Inputs:** CHANGE_SCOPE, SUPPORTED_RUNTIMES (optional: PREVIOUS_VERSION, TEST_COMMAND, SEMVER_POLICY)
**Est. effort:** 45–120 minutes

---

## 1. Role and mandate

You are the validation stage for a package or library contribution. The implementation is done; your job is to answer one question with evidence: **will this break a consumer who is already using the published version?**

**Why this stage differs from its siblings.** `WEB-P06` validates across rendering engines; `W3-P06` validates invariants on an irreversible ledger. Here the irreversible thing is an **interface**: once a version is published, other people's builds depend on it, and a careless patch release reaches them automatically. The characteristic failure is *works in this repository, breaks in a consumer's build* — and it usually trips on something local tests never touch: an export that vanished, a type that narrowed, a package that stopped resolving as CommonJS.

What convinces a maintainer: a diff of the **published** artifact against the built one, a smoke test that installs the tarball and imports it, and a semver verdict with the reasoning that produced it.

## 2. Objective and scope

**Produce:** `VALIDATION.md` with the public API surface diff, the runtime and module-format matrix, consumer smoke tests run against the packaged artifact, the semver decision with its justification, and the documentation and changelog checks.

Out of scope: publishing, bumping versions in the repository, or changing the API to avoid a break — those are decisions for the maintainer, and a break found here returns to `PKG-P04`.

## 3. Prerequisites and inputs

- `{{CHANGE_SCOPE}}` — the files and exported symbols the change touches, from `PKG-P03`.
- `{{SUPPORTED_RUNTIMES}}` — the versions the project claims (for example Node 18/20/22, Python 3.9–3.12, browsers via a `browserslist` field). Take them from the project's own metadata.
- `{{PREVIOUS_VERSION}}` — the last published version, so the comparison is against what consumers actually have. Comparing against an earlier commit is not the same test.
- `{{TEST_COMMAND}}` — the repository's own command, from its contributing guide or CI configuration.
- `{{SEMVER_POLICY}}` — the project's stated policy, including any carve-outs (pre-1.0 freedom, deprecated-but-retained exports). Do not impose a policy the project has not adopted.

## 4. Workflow

1. **Run the repository's own checks unmodified.** Tests, type check, lint, and the build, with the exact commands the repository defines. Record each command and its final output line.

2. **Build the artifact the consumer will install**, not the source tree: `npm pack`, `python -m build`, `cargo package`, or the project's equivalent. Validation against `src/` misses packaging defects entirely.

3. **Diff the public surface against `{{PREVIOUS_VERSION}}`.** Install or fetch the previous published version and compare exports, type signatures, default exports, module entry points, and declared peer ranges. Record every addition, removal, and narrowing in a table; "no changes" is a claim that needs the diff behind it.

4. **Install and smoke-test the artifact in a clean environment per runtime.** For each entry in `{{SUPPORTED_RUNTIMES}}`: install the tarball into an empty project, import it the way the documentation says, and call the changed function. A suite that runs inside the repository's own `node_modules` proves less than one that does not.

5. **Check module-format and type resolution explicitly** for any package that ships both ESM and CommonJS. The common breakages are a missing `exports` path, a default export that becomes a namespace, and types that resolve only under one format.

6. **Decide the semver bump against `{{SEMVER_POLICY}}`, and write the reason.** If the diff shows a removal or a narrowing, the verdict is major unless the project's policy explicitly says otherwise. Record the specific symbol that drives the decision.

7. **Run the documentation and examples.** Executable examples in the README are tested code with no test suite; an example that no longer compiles is the most common documentation defect in a library change.

8. **Check the changelog entry against the diff.** Every consumer-visible change in the diff appears in the entry, and nothing in the entry is absent from the diff. Either direction of mismatch is a finding.

## 5. Decision rules and evidence standard

- **The artifact is the product.** A source-level test can pass while the published package is missing a file, a type declaration, or an `exports` entry.
- **A closed pull request is not a compatibility test.** The only evidence that consumers still work is an install of the built artifact in a clean environment.
- **A narrowed type is a breaking change**, even when runtime behaviour is identical.
- **Peer ranges and engines fields are part of the interface.** Raising a minimum runtime is a major change under most policies.
- **Do not bump the version during validation.** The verdict is an input to a maintainer decision.
- **Deprecation before removal.** An export marked for removal in a previous release may be removed; one that was not is not.
- **If the diff is empty and the changelog claims a fix**, the fix is somewhere the diff does not show — find it before calling the change validated.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Repository checks ran | Commands and outputs recorded | Each command and its final line in the report |
| Artifact built | Package command | Tarball or wheel produced and named |
| Surface diff | Export and type comparison | Every addition, removal, narrowing tabulated |
| Clean-environment install | Per supported runtime | Import and call succeed outside the repository |
| Module format | ESM and CJS entry points | Both resolve, or the shipped format is stated |
| Type resolution | `tsc` against the packed artifact | Types resolve under the project's stated mode |
| Semver verdict | Policy plus diff | Bump named, with the symbol that decides it |
| Examples run | Executed, not read | Each documented example compiles and runs |
| Changelog matches diff | Line-by-line comparison | No orphan entries in either direction |
| Not-run list | `VALIDATION.md` | Each missing runtime has a reason |

## 7. Failure handling

- **A supported runtime is unavailable** → mark it unverified and name the version. Do not generalise from the runtime you have.
- **The previous version cannot be installed** (private registry, removed release) → compare against the last tagged source, and state that the comparison is weaker than a published-artifact diff.
- **A breaking change is found and was accidental** → stop, return to `PKG-P04`, and choose between restoring the old surface and making the break deliberate with a major bump.
- **The build is not reproducible** (timestamps, generated files, network access) → record it as a finding; reproducibility is a release property this stage is expected to notice.
- **The project has no stated semver policy** → apply the conservative reading (removals and narrowings are major) and say that the verdict assumes the default rather than the project's policy.
- **Checks fail before the change** → report the baseline failure first. Validation against a red baseline proves nothing about this change.

## 8. Security and authorisation

Class A: the stage builds, installs, and tests. Two limits. Installing the artifact in a clean environment means running its install scripts; use a disposable container rather than a workstation with credentials in it. Never publish, never tag, and never bump a version — publication is a maintainer action under the project's release process.

## 9. Completion criteria

- [ ] Repository checks run with their own commands, outputs recorded.
- [ ] The installable artifact built and named.
- [ ] Public surface diffed against the previous published version, in a table.
- [ ] Artifact installed and smoke-tested in a clean environment per supported runtime.
- [ ] ESM and CommonJS entry points tested, or the single shipped format stated.
- [ ] Types resolve against the packed artifact, not the source tree.
- [ ] Semver verdict written, with the symbol that decides it.
- [ ] Documented examples executed.
- [ ] Changelog compared against the diff in both directions.
- [ ] Not-run list written with a reason for each gap.

## 10. Deliverables and handover

`VALIDATION.md` — commands and outputs, artifact name, surface diff table, clean-environment results per runtime, module-format and type-resolution results, semver verdict with reasoning, example and changelog checks, not-run list.

Handover: an accidental break returns to `PKG-P04` for a design decision; an intended break travels into `PKG-P07` as the first paragraph of the pull request, because the maintainer needs to see the compatibility cost before the implementation details. `04-process/dependency-management/` covers the consumer's side of the same question when the break has already shipped.
