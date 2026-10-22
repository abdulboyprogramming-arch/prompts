# Empirical evaluation 14 — `PKG-P01` executed against a real package

**Date:** 2026-10-22
**Prompt:** `PKG-P01` Context & Package Understanding, `01-contribution/packages-libraries/`
**Target:** `sindresorhus/p-map` at `d61b6a3` (tag `v7.1.1`), cloned from GitHub
**Evaluator:** the prompt's author (conflict of interest recorded)
**Status:** `TESTED — PASS` after two runs. First run `TESTED — FAIL` on four defects.
**Method:** executed the prompt as written against the real repository, wrote the
artifact it specifies, then checked the artifact against the prompt's own
verification section. Not a tabletop exercise.

## 1. Why this target

`p-map` was chosen because it exercises the rules rather than the happy path: no
`CONTRIBUTING.md`, no `CHANGELOG.md`, no lockfile, a compound test script, and a
published surface smaller than the repository. Each of those is a case a
contribution prompt meets constantly and a template usually ignores.

## 2. Run 1 — v1.0.0, four defects

The artifact was produced in 40 minutes and passed three of its four verification
items. The fourth could not pass, and the reason it could not is the most
important finding.

| # | Sev | Defect | Evidence from the run |
|---|-----|--------|-----------------------|
| 1 | **High** | The prompt says to record "the test command, lint command and type-check command, each copied from a file". Real projects bundle them: `"test": "xo && ava && tsd"`. The prompt gave no rule to decompose, so the artifact recorded one command four times or left two rows empty. A later stage told that `npm test` failed cannot say whether lint, tests or types failed. | `package.json:24`; `npx xo`, `npx ava`, `npx tsd` each run separately, exit 0 |
| 2 | **High** | The public surface and the **published** surface are different, and the prompt only asked for the first. `files` ships 5 of 11 top-level files. `PKG-P06` validates "the published artefact", so it was inheriting a set nobody had written down. | `npm pack --dry-run --json` → `['index.d.ts', 'index.js', 'license', 'package.json', 'readme.md']` |
| 3 | Medium | "Follow the lockfile's own instructions" has no fallback for a project with no lockfile. This one sets `package-lock=false`, so installs are not reproducible — a fact every later validation claim inherits and none recorded. | `.npmrc`; `npm install` exit 0, pulls current versions |
| 4 | **High** | Verification item 4 ("a reader can tell which changes are breaking") is unachievable when the versioning policy is `unstated`, and the prompt had no route for an unachievable check. An executor either drops the item silently or invents a policy. | no `CONTRIBUTING.md`, no stated semver rule |

What worked: the missing-changelog failure path fired correctly. The prompt tells
the executor to record `no release history available` and note the consequence for
`PKG-P02`, and the run did exactly that without improvisation.

## 3. The fixes, in v1.1.0

- **Decompose bundled scripts.** The workflow now requires the bundled command *and*
  each component with its source file, and says why: a later stage cannot split a
  compound script that was recorded as one line.
- **Record the shipped surface with a packing command.** `npm pack --dry-run`,
  `cargo package --list` and the equivalents, cited, rather than inferred from the
  folder layout.
- **Record install reproducibility.** Lockfile present, disabled, or absent — each
  with its consequence stated.
- **A check that cannot be satisfied is recorded, not dropped.** The verification
  section now ends with the rule, and the artifact header carries `partial` when an
  item could not pass.
- Two new failure paths: a compound script that cannot be split, and a packing
  command that needs network it does not have.

## 4. Run 2 — v1.1.0, same target

| Verification item | Run 1 | Run 2 |
|---|---|---|
| Public surface with `path:line` | pass | pass |
| Support matrix, claimed vs tested | pass | pass |
| Shipped surface with a packing command | **absent** | pass, 5 files named |
| Bundled script decomposed | **absent** | pass, 3 components with outcomes |
| Install reproducibility stated | **absent** | pass, `no lockfile` |
| Reader can tell what is breaking | **failed silently** | `partial`, reason recorded |

Run 2 added no new findings beyond the four. The artifact took 45 minutes against
40, which is the cost of the extra evidence, and it is the right trade.

## 5. Results worth keeping

- `p-map` 7.1.1: **423 tests passed, 1 skipped**; `xo` and `tsd` clean; 5 files
  published of 11 in the tree.
- The package claims Node `>=18` and CI tests 18, 20, 22, 24 and 26 — on Linux only.
  A platform-specific failure would be invisible in CI. That gap is now recorded in
  the artifact, and it is exactly what `PKG-P02` should be told.
- The repository has **no changelog**, so the downstream "regression reported twice"
  signal is unavailable. The failure path handled it; `PKG-P02` still needs its own
  plan for that case, which is unverified.

## 6. Limitations

- **One target, chosen by the author** who also wrote the prompt. A different
  ecosystem (Python, Rust) was not exercised, so the packing-command rule is proven
  only for `npm`.
- **The evaluator wrote the artifact by hand while reading the prompt**, which is
  closer to a desk run than to an independent model execution. The evidence is the
  commands, not the prose.
- **No maintainer interaction.** The prompt's claim that a context artifact makes a
  contribution more welcome is untested and cannot be tested here.
- `PKG-P02` through `PKG-P08` were **not** run. This evaluation covers the entry
  stage only, so the system remains `PARTIALLY TESTED` end to end.
