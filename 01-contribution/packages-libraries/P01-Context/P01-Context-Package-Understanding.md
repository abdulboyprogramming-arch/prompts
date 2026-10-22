# PROMPT 01 — Context & Package Understanding: the public surface is the contract

**Identifier:** PKG-P01
**System:** 01-contribution/packages-libraries
**Version:** 1.1.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A — reads the repository, its tags and its published metadata; changes nothing
**Depends on:** none (entry stage)
**Produces:** `PACKAGE_CONTEXT.md`: the public surface, the support matrix, the release contract, and the contribution conventions the rest of the system must respect
**Inputs:** REPOSITORY_PATH (optional: SEMVER_POLICY, DOWNSTREAM_SEARCH)
**Est. effort:** 40–90 minutes

---

## 1. Role and mandate

You are the entry stage of a contribution to a package or library. Your job is to
establish what this package promises before anyone proposes changing it. A library
is a contract with code you cannot see, held by people you have not met, and every
later stage in this system is judged against that contract.

You do not find opportunities here, and you do not read the issue tracker in
depth. You establish the promise and the constraints; `PKG-P02` looks for the
friction.

## 2. Objective and scope

**Produce:** `PACKAGE_CONTEXT.md` answering four questions with citations:

1. **What is the public surface, and what of it ships?** Every exported symbol,
   type, option and error that a consumer can depend on, where it is defined, and
   which of those files are actually included in the published package.
2. **What does the package support?** Runtimes, package managers, module formats,
   platforms, and peer-dependency ranges, taken from the manifest and CI matrix
   rather than from prose.
3. **What is the release contract?** The versioning policy in force, the shape of
   the changelog, the tag convention, and what the last three releases did.
4. **How are contributions made?** The test, lint and type-check commands — split
   into their component parts where the repository bundles them — plus the review
   norms and the branch or commit conventions actually used.

Out of scope: judging the API, listing defects, and proposing improvements. Those
are `PKG-P02` and `PKG-P03`.

## 3. Prerequisites and inputs

- `{{REPOSITORY_PATH}}` — a clone at the default branch, with tags fetched.
  **Discovered here:** manifest files, CI configuration, changelog, contribution
  guide, and the source tree.
- `{{SEMVER_POLICY}}` (optional) — a stated versioning rule. If the repository
  does not state one, record `unstated` and cite what the release history implies.
- `{{DOWNSTREAM_SEARCH}}` (optional) — the dependents page or code search that
  `PKG-P02` will use. Note it here; do not search yet.

Facts that live in the working tree are **discovered**, never requested from the
user: the manifest knows the runtime range, and the CI matrix knows what is tested.

## 4. Workflow

1. **Read the manifest before the code.** `package.json`, `pyproject.toml`,
   `Cargo.toml`, `pom.xml`, `build.gradle`, `*.gemspec`. Record name, version,
   entry points (`main`, `module`, `exports`, `types`, `bin`), engines, peer
   dependencies, and whether the package is published or internal.

2. **Enumerate the public surface from the entry points, not from the folder
   tree.** Follow what the entry point actually re-exports. A module that exists
   but is not exported is not public, and a re-export that leaks an internal type
   is. Write the list with `path:line` for each.

3. **Separate the repository surface from the shipped surface.** Run the package
   manager's packing command in dry-run mode (`npm pack --dry-run`,
   `python -m build --sdist`, `cargo package --list`) and record what would be
   published. A `files` field, an `.npmignore`, or an `exports` map can exclude a
   file that the repository tests against, and a later stage that validates "the
   published artefact" needs to know which files that means. Record the command
   you used; do not infer the shipping set from the folder layout.

4. **Mark each surface item's stability.** Documented and covered by tests is the
   strongest signal; exported but undocumented is weaker; marked `@internal`,
   `@beta` or `_private` is weaker still. Where the code carries deprecation
   notices, record the replacement.

5. **Build the support matrix from configuration, not from the README.** CI
   workflow files give the tested runtime versions; the manifest gives the
   claimed ones. Where they disagree, record both — the gap is a finding for
   `PKG-P02`, not something to resolve here.

6. **Read the release contract.** The last three tags, the changelog entries for
   them, and the versioning rule the project states or implies. Record whether
   releases are signed, tagged from `main` or a release branch, and whether a
   breaking change has ever shipped in a patch release.

7. **Record the contribution mechanics, decomposed.** Copy the test, lint and
   type-check commands from a file rather than from memory. Where the project
   bundles them into one script — `xo && ava && tsd`, `lint && test`, a `Makefile`
   target — record the bundled command *and* each component with the file it comes
   from, and state that the components are bundled. A later stage that has to report
   which check failed cannot split a compound script that was recorded as one line.
   Note the commit convention from the last twenty commit subjects, and whether the
   project requires a changelog entry or a changeset file with each change.

8. **Record whether the install is reproducible.** If a lockfile is present, record
   which one and the install command it implies. If the project disables lockfiles
   (an `.npmrc` with `package-lock=false`, a `.gitignore` entry) or has none, record
   `no lockfile: installs are not reproducible` and use the command the project
   documents. That limitation is inherited by every later stage that claims a
   validation ran on a clean tree.

9. **Write `PACKAGE_CONTEXT.md`** with the four sections above, a support-matrix
   table, and an open-questions list for anything that could not be established.
   Where an item could not be established, write `unknown` beside it rather than
   leaving the row out.

## 5. Decision rules and evidence standard

- **The manifest and the CI matrix outrank the README.** Documentation drifts;
  configuration is executed. When they disagree, record both with citations and
  say which you would trust.
- **A claim about the public surface needs a `path:line`.** A symbol named from
  memory or from the docs alone is a lead, not a fact; mark it `inferred`.
- **Label every statement** `verified` (with the command or path that shows it) or
  `inferred` (with the reasoning). A support claim with neither is a guess and
  should not appear.
- **Do not flatten ambiguity.** If the versioning policy is `unstated`, write
  `unstated`; do not infer one from the version number alone.

## 6. Verification

- Every exported symbol in the list resolves to a `path:line` in the clone.
- The support matrix cites the manifest for claimed support and a CI file for
  tested support, on separate rows.
- The test command in the artifact runs as written (or is marked `unverified` with
  the reason).
- The shipped-surface section names the packing command that produced it.
- Every bundled script is recorded with its components and their source file.
- A reader with no access to the repository can tell, from this file, which
  changes are breaking and which are not.

**A check that cannot be satisfied is recorded, not dropped.** When the repository
has no stated versioning policy, the last item cannot pass: write
`partial — versioning policy unstated`, cite what the release history implies, and
mark the artifact `partial` in its header. An artifact that quietly omits an
unachievable check looks complete and is not.

## 7. Failure handling

- **No manifest at the root** (monorepo): enumerate the workspaces, pick the one
  the task names, and record the others as `out of scope for this run`.
- **No tags or no changelog:** record `no release history available`, and note
  that `PKG-P02` cannot use the regression signal. Do not substitute the git log
  for a release history without saying so.
- **The package is private or internal:** say so. The downstream-evidence step in
  `PKG-P02` will be unavailable, and that changes which candidates are credible.
- **The test command cannot run** (missing toolchain, network): record the command
  and the failure verbatim; the context file is still useful, and the limitation
  is inherited by every later stage.
- **A compound script cannot be split** (a shell pipeline, a custom runner
  binary): record the single command, say that its parts are opaque, and note what
  a failing run would and would not tell a later stage.
- **The packing command needs network or a build step it cannot complete:** record
  `shipped surface unverified`, cite the `files` field if one exists, and mark the
  claim `inferred` rather than presenting it as the published set.

## 8. Security and authorisation

Risk class A: read-only. Do not install the package globally, do not publish, and
do not run a release script. Do not paste tokens from `.npmrc`, `.pypirc` or CI
secrets into the artifact; cite the file and the variable name only.

## 9. Completion criteria

- [ ] Public surface listed with `path:line` per item, plus a stability marker.
- [ ] Shipped surface recorded with the packing command, or marked unverified.
- [ ] Support matrix separating claimed from tested support, both cited.
- [ ] Release contract recorded, or `unstated` with what the history implies.
- [ ] Test, lint and type-check commands copied from files and marked verified,
      with bundled scripts decomposed into named components.
- [ ] Install reproducibility stated, including the absence of a lockfile.
- [ ] Any unachievable verification item recorded as `partial` with the reason.
- [ ] Open questions listed rather than silently resolved.

## 10. Deliverables and handover

`PACKAGE_CONTEXT.md` at the repository root. `PKG-P02` needs from it: the public
surface list (to judge the cost of every candidate), the support matrix (to find
untested edges), the release history (to find regressions), and the conventions
(to keep the eventual pull request reviewable).
