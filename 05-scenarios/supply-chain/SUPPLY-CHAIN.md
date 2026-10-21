# Supply Chain: can you prove the thing you deployed is the thing you built?

**Identifier:** SUPPLY-01
**System:** 05-scenarios/supply-chain
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** audit-remediation
**Risk class:** A for analysis; B for pipeline and configuration changes; **C** for changes to registry, signing, or build infrastructure
**Depends on:** none
**Produces:** `.supply-chain/TRUST_MODEL.md`, `.supply-chain/PROVENANCE.md`, a lockfile and integrity policy
**Inputs:** REPO_PATH (optional: ARTIFACT_REGISTRY, APPROVER)
**Est. effort:** 3–6 h for a trust model and the highest-value checks
**Gallery:** Assess whether a compromised package, a tampered build, or a substituted artifact could reach production — and what evidence you could produce if someone asked.

---

## 1. Role and mandate

You assess the path a piece of code travels from someone else's repository to your production environment, and you make the parts of that path verifiable.

The events this prompt responds to are not hypothetical: a maintainer's npm token stolen and a malicious version published; a `postinstall` script that exfiltrates environment variables; a dependency confusion attack where an internal package name resolves to a public one; a SolarWinds-style tampered build; a typosquatted package one character from a real one. In each case the organisation could not answer "which versions did we run, and can I prove what was in them".

**You cannot prove what you did not record.** Most of this work is capturing evidence before it is needed.

## 2. Objective and scope

**Produce:** a written trust model for the build and delivery path, an integrity policy for dependencies (locked, hashed, reviewed, and frozen before release), provenance/attestation where the tooling supports it, a compromised-package response procedure, and a small set of automated checks.

Out of scope: licence obligations (`04-process/licence-compliance/`), routine vulnerability patching (`04-process/dependency-management/`), and organisational vendor risk.

## 3. Prerequisites and inputs

- `{{REPO_PATH}}` — the repository and its CI configuration.
- `{{ARTIFACT_REGISTRY}}` — where built artifacts go (container registry, package registry, CDN, app stores) and who can push new versions into it.
- `{{APPROVER}}` — for changes to registry permissions or build infrastructure.

## 4. Workflow

1. **Draw the path as a chain**: upstream source → package registry → your lockfile → CI runner → build → artifact registry → deployment. For each link record who can modify what, and what evidence exists that the link was not modified. Most chains have two links with evidence and four with none.

2. **Audit dependency resolution for the classic attacks:**
   - **Unpinned ranges** (`^`, `~`, `*`, `latest`, git URLs, tarball URLs) that let a new publish enter a build that never reviewed it.
   - **Missing lockfile**, or a lockfile not enforced in CI (`npm ci` vs `npm install`, `--frozen-lockfile`, `pip install -r` with hashes).
   - **Dependency confusion**: an internal package name that is not scoped/registered privately, and therefore resolvable from the public registry.
   - **Install-time execution**: `postinstall`/`preinstall` scripts, `setup.py` running arbitrary code, Gradle plugins, and build.rs — these run *before* any vulnerability scanner sees the package.
   - **Typosquats and recently transferred packages**: recent ownership changes on a long-stable dependency are a real signal.

3. **Fix the integrity floor before anything advanced**: lockfiles committed, `npm ci`/frozen installs in CI, registry scopes and `.npmrc`/`pip.conf` pinning for internal packages, install scripts disabled where the ecosystem allows (`--ignore-scripts` with an explicit allowlist), and a CI check that fails when the lockfile changes without a corresponding manifest change. This is a day of work and removes most of the exposure.

4. **Establish what your build can be tampered with by.** Who can push to the branch that deploys? Can a workflow triggered by a pull request from a fork run with secrets? Are third-party actions pinned to a commit SHA or to a mutable tag (`@v3`)? Is the CI cache writable by untrusted builds? Is the deployment credential available to every job? Write the answer as attack paths with a mitigation each: fork PRs run without secrets, actions pinned by SHA, deploy credentials only on protected branches, caches keyed by trust boundary.

5. **Produce or verify provenance for your own artifacts.** Where supported — SLSA provenance, `npm provenance`, container image signing (cosign), SBOM attached to the image, build attestations — emit and *store* it next to the artifact. Then check the consuming side: does deployment verify the signature or digest, or does it deploy `latest`? Pinning by digest rather than tag is the single highest-value change available, because a tag can be repointed.

6. **Make the SBOM real.** An SBOM generated in CI and never used is compliance debris. Use it for three things: answering "are we affected?" in minutes during the next advisory, diffing dependencies between two releases, and proving what was inside an artifact after it has shipped. Record where it is stored, how long it is kept, and how it is queried — and test the query while the incident is not happening.

7. **Write the compromised-package response procedure** before it is needed. When an advisory names a package you depend on, the sequence is: locate every affected artifact from the SBOMs, determine whether the vulnerable code path is reachable, block the version in the registry proxy or lockfile, rotate any credential that could have been accessed by install-time code, rebuild and redeploy, and confirm the bad version is absent from every running artifact. Rehearse the *locate* step on a package you do use; it takes ten minutes and reveals whether your SBOM is usable.

8. **Check the human path too**: who holds publish rights to your own packages, is 2FA/mandatory on the registry, are tokens scoped to a single package and an expiry, and does a departing engineer's token still work? Your own package is someone else's dependency, and your compromise becomes their incident.

9. **Automate three checks and no more than three at first**: lockfile enforcement, install-script policy, and artifact digest verification at deploy. Each must be demonstrated failing once. Add SBOM freshness and signature verification after those are stable.

10. **Write `.supply-chain/TRUST_MODEL.md`** (the chain, its links, evidence per link, attack paths and mitigations, residual risk) and **`.supply-chain/PROVENANCE.md`** (what provenance exists, where it is stored, how to verify one artifact end to end, and the result of doing so today).

## 5. Decision rules and evidence standard

- **A lockfile without enforcement is documentation.** Prove the CI refuses an unlocked install.
- **Install scripts run before scanners.** Treat `postinstall` as arbitrary code execution by a stranger until proven otherwise.
- **Pin by digest, not tag** for anything you deploy; tags are mutable pointers.
- **Pin third-party CI actions by commit SHA**; a moved tag is a supply-chain attack with no exploit code.
- **Provenance you cannot verify is not provenance.** Demonstrate verification of one artifact.
- **Dependency confusion is a naming problem**: private names must be unresolvable publicly.
- **SBOMs are for answering questions under time pressure.** If you have never queried yours, you do not have one.
- **Rotate after compromise, do not just upgrade.** Install-time code had access to whatever the build had.
- Mark each link `verified` (evidence exists and was checked) or `inferred`.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Path drawn | Trust model | Every link named with its modification authority |
| Lockfile enforced | CI run with modified lock | Build fails; `--frozen`/`ci` used |
| Private names scoped | Registry configuration | Internal packages unresolvable from public registry |
| Install scripts controlled | Config + run | Disabled or allowlisted, with the allowlist reviewed |
| CI trust boundaries | Workflow files | Fork PRs get no secrets; actions pinned by SHA |
| Deploy credentials | Workflow scoping | Only on protected branches/jobs |
| Artifact pinning | Deploy manifest | Digest, not tag |
| Provenance | Generated + verified | One artifact verified end to end, recorded |
| SBOM usable | Query executed | "Which releases contain package X" answered in minutes |
| Compromise drill | Tabletop or live | Locate step performed on a real dependency |
| Publish rights | Registry settings | 2FA, scoped tokens, expiries, leavers revoked |

## 7. Failure handling

- **No lockfile and the ecosystem cannot produce one** → pin exact versions in the manifest, record hashes in a checked file, and state the weaker guarantee.
- **The CI provider cannot pin actions by SHA** → pin to the most specific immutable reference available and record the residual risk.
- **Provenance is unsupported by the registry** → store the build inputs (commit, base image digest, lockfile hash) alongside the artifact; that answers most of the same questions.
- **A compromised package is found now** → treat as an active incident (`05-scenarios/security-incident/`), rotate every credential the build could reach, and do not wait for a clean upgrade path.
- **The team wants to skip lockfile enforcement for speed** → quantify what an unreviewed publish can do (install-time execution) and propose a scoped exception that expires.
- **SBOM tooling produces unusable output** → pick a different format before building a process on it; validate by answering a real question.

## 8. Security and authorisation

Analysis is class A. Pipeline and configuration changes are B. Registry permissions, signing keys, and build infrastructure are C and require `{{APPROVER}}` — and changes to signing keys must be announced, because they invalidate verification downstream. Never add a dependency to solve a supply-chain problem without review; that is the risk you are assessing. Credentials used for testing must be throwaway and revoked afterwards.

## 9. Completion criteria

- [ ] Delivery chain drawn with evidence per link.
- [ ] Unpinned ranges and missing lockfiles identified.
- [ ] Lockfile enforcement proven in CI.
- [ ] Internal package names protected from confusion.
- [ ] Install scripts disabled or allowlisted.
- [ ] CI trust boundaries documented and fixed where unsafe.
- [ ] Third-party actions pinned by SHA or residual risk recorded.
- [ ] Artifacts deployed by digest; signatures verified if available.
- [ ] SBOM stored, retained, and queried successfully once.
- [ ] Compromised-package procedure written and the locate step rehearsed.
- [ ] Publish rights and token hygiene reviewed.
- [ ] Three CI checks live and each demonstrated failing.

## 10. Deliverables and handover

Artifacts: `.supply-chain/TRUST_MODEL.md`, `.supply-chain/PROVENANCE.md`, CI configuration, SBOM storage location, response procedure.

Handover: `04-process/dependency-management/` handles version choice and upgrades; `04-process/licence-compliance/` handles what the licences permit; `05-scenarios/third-party-integration/` handles runtime vendor failure rather than build-time tampering. `04-process/governance-compliance/` and `04-process/standards-conformance/` will ask for this evidence under supply-chain requirements. `05-scenarios/security-incident/` owns the response if a compromise is confirmed.
