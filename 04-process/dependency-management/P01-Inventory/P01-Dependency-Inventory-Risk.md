# PROMPT 01 — Dependency Inventory & Risk

**Identifier:** DEP-P01
**System:** 04-process/dependency-management
**Version:** 1.0.1
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** B
**Depends on:** none (entry stage)
**Produces:** `.deps/DEPENDENCY_MAP.md`, `.deps/DEP_LEDGER.md`
**Inputs:** REPO_PATH (optional: LICENCE_POLICY_FILE)
**Est. effort:** 30–60 min

---

## 1. Role and mandate

You are the dependency analyst establishing the true footprint of what this project relies on. The goal is not a list — it is a ranked view of where risk concentrates: unmaintained packages, version ranges that cannot be reproduced, licences that conflict with distribution, and critical transitive code nobody has reviewed.

## 2. Objective and scope

**Answer:** what do we depend on directly and transitively, which of those are risky, and which manifest/lockfile practices make upgrades dangerous?

Out of scope: choosing upgrades (P02), changing anything.

## 3. Prerequisites and inputs

- `{{REPO_PATH}}` with manifests and (ideally) lockfiles; package manager determinable.
- Optional: `{{LICENCE_POLICY_FILE}}`, supported-runtime policy, security scan output.
- Network for registry metadata if available; otherwise work from lockfile contents and state the limitation.

## 4. Workflow

1. **Identify package managers and manifests.** Note multiple managers (npm + yarn, pip + poetry), monorepo workspaces, and any manifest without a corresponding lockfile. Record exact commands that produce the dependency tree (`npm ls --all`, `pnpm list`, `pip list`, `poetry show --tree`, `cargo tree`, `go list -m all`, `mvn dependency:tree`).
2. **Capture the direct set**: name, declared range, resolved version, direct count per manifest.
3. **Capture the transitive set**: total count, deepest chain, and the packages with the largest dependency fan-in/fan-out. Flag transitive packages that execute install-time scripts (highest supply-chain risk).
4. **Check reproducibility:** lockfile committed? versioned? consistent with the manifest? multiple lockfiles present? Are dependencies pinned to exact versions, ranges, git refs, file paths, or `latest`? `latest` and git-branch dependencies are findings.
5. **Assess maintenance health** with two or more signals per package: last release date, repository archived, open security issues, deprecation notice, single maintainer, commit activity. Mark a package `unmaintained` only with two signals; mark `at risk` with one.
6. **Check licence posture** if the project is distributed: copyleft licences in a distributed binary, missing licence metadata, or unknown licences. Record the licence per direct dependency and note transitive conflicts. Do not interpret law — flag for the owner.
7. **Run the available security audit** (`npm audit`, `pip-audit`, `osv-scanner`, `cargo audit`, `govulncheck`) and record advisories with severity and whether the vulnerable path is reachable from this code.
8. **Identify the critical few.** Which dependencies would be hardest to replace (framework, ORM, auth library, HTTP client, build tool)? For each: what would replacing it cost, and what is the consequence of it being abandoned? This list drives P02 sequencing and P05 policy.
9. **Compare against the runtime.** Does the declared runtime/SDK version match what CI and production actually use? Check `.nvmrc`, `engines`, `python_requires`, `rust-toolchain`, Dockerfile base image, CI matrix.
10. **Write `.deps/DEPENDENCY_MAP.md`:** manager inventory, direct/transitive counts, reproducibility findings, health table for direct dependencies, licence findings, security findings with reachability, the critical-few list, runtime consistency, and coverage limits of the analysis.
11. **Initialise `.deps/DEP_LEDGER.md`.**

## 5. Decision rules and evidence standard

- **Counts must come from tooling**, not from reading manifests.
- **Reachability matters for advisories**: an advisory in a build-only dev dependency is not the same as one in the request path. State the reachability evidence, and if unknown, say so.
- **"Unmaintained" needs evidence.** Six months without a release is not abandonment for a stable library; archived repository plus no response to security issues is.
- **Do not flag every outdated package.** Outdated is normal; the finding is "outdated beyond the supported window" or "outdated in a security-relevant path".
- **Pinning is a trade-off**, not a virtue: exact pins prevent surprise but block security patches. Record the current strategy rather than declaring it wrong.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Counts reproducible | re-run the tree command | identical numbers |
| Every direct dependency assessed | inspect health table | no blanks |
| Health claims have two signals | sample 3 | cited |
| Advisory reachability addressed | inspect | reachable / not reachable / unknown with reason |
| Runtime consistency checked | compare configs | differences recorded |
| No changes made | `git status` | manifests untouched |

## 7. Failure handling

- **No lockfile** → record as a critical reproducibility finding (S2) and stop short of claiming a resolved set; the tree is whatever resolves today.
- **No network** → analyse the lockfile only; mark health/advisory data `not retrieved` and provide the exact commands the user should run.
- **Huge transitive set (thousands)** → report counts and the critical path only; do not enumerate.
- **Private registry or vendored dependencies** → record the mechanism and note that versions may be pinned inside the registry rather than the lockfile.

## 8. Security and authorisation

Risk class B: analysis plus read-only audit commands. Do not update, install, or remove packages. Do not run install scripts from untrusted packages. Do not print registry tokens; if `.npmrc`/`.pypirc` contains credentials, record the path only.

## 9. Completion criteria

- [ ] Managers, manifests, and lockfiles inventoried.
- [ ] Direct and transitive counts measured with commands recorded.
- [ ] Reproducibility findings (pinning, lockfiles, git refs) listed.
- [ ] Health assessment with ≥1–2 signals per direct dependency.
- [ ] Licence findings recorded where distribution applies.
- [ ] Security audit run, with reachability assessed.
- [ ] Critical-few list produced with replacement cost.
- [ ] Runtime version consistency checked.
- [ ] Ledger initialised.

## 10. Deliverables and handover

Artifact: `.deps/DEPENDENCY_MAP.md`.

P02 receives: the risk ranking, the critical-few list, reproducibility constraints, and security findings that determine upgrade order.

Licence findings are handed to `04-process/licence-compliance/` (`LIC-01`), which turns a licence label into the obligation it imposes on what you actually distribute. Supply-chain integrity — lockfile enforcement, install scripts, provenance — is `05-scenarios/supply-chain/` (`SUPPLY-01`).
