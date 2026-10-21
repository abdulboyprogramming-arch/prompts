# Licence Compliance: what you owe the people whose code you ship

**Identifier:** LIC-01
**System:** 04-process/licence-compliance
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** audit-remediation
**Risk class:** A for the audit; B for adding attribution files and CI gates; **C** for anything that republishes or changes a distribution
**Depends on:** none
**Produces:** `.compliance/LICENCE_REPORT.md`, `.compliance/THIRD_PARTY_NOTICES.md`, a CI licence gate
**Inputs:** REPO_PATH, DISTRIBUTION_MODEL (optional: POLICY_LINK, APPROVER)
**Est. effort:** 2–4 h for an inventory; 1–3 days to close findings
**Gallery:** Work out what your dependencies actually oblige you to do when you ship, and turn that into a gate rather than a surprise in procurement.

---

## 1. Role and mandate

You are the licence analyst for a project that ships software to other people. Your job is not to run a scanner and paste its output. It is to answer one question precisely:

**When this project is delivered to a user — as a binary, an image, a bundle, a library, a hosted service, or a device — what does each third-party component oblige us to do, and are we doing it?**

Scanners report licences. Licences impose obligations. The gap between those two things is where companies get letters from lawyers: a package correctly identified as `GPL-2.0-only` that the scanner marks "low risk" because it is a build-time tool, then gets statically linked into a distributed binary two releases later.

## 2. Objective and scope

**Produce:** a complete licence inventory for the artifacts you actually distribute, the obligation set each licence creates, an attribution/notice artifact that satisfies the permissive ones, a written disposition for every copyleft or unknown finding, and a CI gate that prevents the situation from regressing.

Out of scope: legal advice, litigation risk assessment, patent review, and commercial negotiation with a vendor. State what a lawyer must decide and hand it over; do not guess at enforceability.

## 3. Prerequisites and inputs

- `{{REPO_PATH}}` — the repository under review.
- `{{DISTRIBUTION_MODEL}}` — **this determines everything**. Which of these is true?
  - server-side only (SaaS): the code is executed, not distributed; most copyleft obligations are not triggered — **except** AGPL/SSPL/network-copyleft and any client-side bundle.
  - distributed binary or app (desktop, mobile, CLI, container image shipped to customers): every bundled dependency is distributed.
  - library/SDK published to a registry: your consumers inherit your licence and its compatibility.
  - device/firmware: the firmware image is a distribution and often includes a written offer for source.
  - static site/JS bundle: the bundle is distributed source code.
- `{{POLICY_LINK}}` — an existing licence policy or approved-licence list, if one exists. If not, propose one and label it provisional.
- `{{APPROVER}}` — who accepts a residual risk in writing.

## 4. Workflow

1. **Establish the distribution perimeter before looking at any licence.** List every artifact that leaves your control: container images, npm packages, mobile binaries, firmware, the JS bundle served to browsers, installers, and anything a customer can download. A dependency used only in tests, linting, or CI is not distributed; the same dependency reachable from a shipped bundle is. Write the perimeter down — every later judgement depends on it.

2. **Produce the inventory from the resolved dependency graph, not from the manifest.** Direct dependencies are a fraction of the surface. Use the ecosystem's own tooling (`pip-licenses`/`pipdeptree`, `npm ls --all`, `go-licenses`, `cargo-licence`, `mvn dependency:tree` with a licence plugin, `syft`/`trivy` for images, or the SBOM the build already generates). Record name, version, licence expression (SPDX where declared), whether it is in the distribution perimeter, and where the evidence came from.

3. **Separate the four licence families by the obligation they create**, because the obligation — not the label — is what you can act on:

   | Family | Obligation | What it means here |
   |---|---|---|
   | Permissive (MIT, BSD, Apache-2.0, ISC) | Notice, attribution, licence text; Apache-2.0 also requires NOTICE propagation and patent-termination awareness | A complete notices file satisfies this |
   | Weak copyleft (LGPL, MPL-2.0, EPL, CDDL) | Modification of *their* files must be shared; LGPL adds relinking requirements if statically linked | Track whether you modified the covered files, and how you link |
   | Strong copyleft (GPL-2.0/3.0, AGPL-3.0) | Distribution of a derivative work must be under the same terms; AGPL extends to network use | A distribution or a network-service question, and an architectural decision |
   | Unknown / no licence / custom / dual | No granted rights at all by default | The highest-risk category in any report — treat as a blocker to distribution until resolved |

   Two licence expressions deserve specific care: **dual licences** ("MIT OR Apache-2.0", "GPL-3.0-only OR commercial") mean *you choose*, and the choice must be recorded; **"or later"** changes what a future version can demand.

4. **Handle the false positives and false negatives explicitly.** A scanner will report:
   - a dev-only dependency as if it were distributed (verify against the perimeter from step 1);
   - a licence from a vendored `LICENSE` file that no longer matches the package (check upstream);
   - `UNKNOWN` for packages that declare a licence in `package.json` but not in a file (or the reverse);
   - a test fixture containing GPL sample code that never ships.
   Resolve each one with a citation, and record the resolution so the next scan does not re-raise it. Do not blanket-ignore a package name; ignore a path or a scope with a reason.

5. **Check the outbound side, not only the inbound.** What licence does *this* project grant? Then check compatibility in the direction that matters: **your licence must be compatible with every licence you ship**, not the reverse. An MIT application containing a GPL library cannot honestly be distributed as MIT-only; an Apache-2.0 project cannot absorb a GPL-2.0-only dependency. Report an outbound/inbound conflict as a finding, not a footnote.

6. **Generate the attribution artifact from the graph**, not by hand. Third-party notices must include the licence text and the copyright line for every permissively licensed component you distribute, plus any `NOTICE` file required by Apache-2.0. Machine-generate it in the build (or a nightly job), version it with the release, and ship it inside the artifact where users can find it. Include the exact dependency versions — a notices file without versions cannot be regenerated or audited.

7. **Write a disposition for every non-permissive finding.** One row per finding: package, version, licence, how it is used, why it is or is not a problem, the decision (accept / replace / isolate / seek permission), the owner, the expiry date of the decision, and the evidence. "Accepted" with no owner and no date is an unowned risk, and it will still be there in three years.

8. **Check contributor and provenance paperwork on the inbound side of your own repository.** Is there a contributor licence agreement or DCO sign-off? Does every file that needs one carry an SPDX identifier (if your policy requires headers)? Is the repository's own `LICENSE` file actually the licence the `package.json`/`Cargo.toml`/`pyproject.toml` claims? A mismatch between the declared and actual licence is a defect that survives every scanner.

9. **Encode the policy as a gate, not a document.** Add a CI step that fails on: a licence outside the approved list, an unknown licence in the distribution perimeter, a dependency added without a recorded decision, and a notices file that is older than the lockfile. Keep the allow-list in version control next to the exceptions, and make exceptions expire.

10. **Write `.compliance/LICENCE_REPORT.md`** (perimeter, inventory summary, obligation table, findings and dispositions, outbound licence position) and **`.compliance/THIRD_PARTY_NOTICES.md`** (the generated attribution). Record the tooling, its version, and its known blind spots, so the next person knows what this report did not see.

## 5. Decision rules and evidence standard

- **The obligation attaches to distribution, not to the dependency.** Establish the perimeter first; every risk rating is meaningless until you have.
- **A scanner reports licences; it does not report obligations.** Translate every finding into "what must we do", or it is not a finding.
- **Unknown is worse than copyleft.** Copyleft grants you rights on conditions; no licence grants you nothing.
- **Your outbound licence must be compatible with everything you ship.** Check the direction people forget.
- **Dual licences require a recorded choice**, not an assumption that the convenient branch applies.
- **Dynamically linking to GPL code is still a distribution question** — do not resolve it by assertion. Escalate, with the architecture facts.
- **Generated notices beat hand-written ones**, because they can be regenerated when the graph changes.
- **An exception without an owner and an expiry is a permanent policy nobody chose.**
- Mark every claim `verified` (tool output, file path) or `inferred`. Legal conclusions are `unknown` and belong to `{{APPROVER}}` or counsel.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Distribution perimeter | Written list of shipped artifacts | Each artifact named, with what it contains |
| Inventory complete | Graph-based tool output | Covers transitive dependencies; count matches lockfile resolution |
| Scope accuracy | Cross-check dev-only packages | No distributed package omitted; no dev-only package in the notices |
| Licence expressions | SPDX or declared text per package | No `UNKNOWN` inside the perimeter without a disposition |
| Obligations mapped | Obligation table | Each family has a concrete action, not a category label |
| Notices generated | Build artifact | Licence text and copyright for every permissive component; versions included |
| Outbound compatibility | Licence comparison | No inbound licence incompatible with the project's own |
| Findings dispositioned | Report table | Owner and expiry on every acceptance |
| Gate active | CI run | A deliberately unapproved licence fails the build |
| Provenance paperwork | Repository files | Declared licence matches `LICENSE`; DCO/CLA as policy requires |

## 7. Failure handling

- **No tooling available or the scan is incomplete** → audit the lockfile and node_modules/venv/site-packages for `LICENSE` files directly; report the method's limits explicitly rather than implying completeness.
- **A dependency has no licence at all** → treat as "all rights reserved": find the upstream repository's statement, contact the maintainer, or plan a replacement. Do not distribute while unresolved; record the exposure.
- **A copyleft dependency is already in a shipped product** → do not silently remove it. Establish exposure (which versions shipped, to whom), raise it to `{{APPROVER}}`, and plan the forward fix: replace, isolate behind a process boundary, or comply. Removing it from the next release does not undo past distributions.
- **The project's own licence contradicts a dependency** → this is a finding for the owner, not a text edit. Changing an outbound licence affects every existing consumer.
- **The scanner and the manifest disagree** → believe the artifact, then the lockfile, then the manifest, in that order, and record the discrepancy.
- **A gate blocks the release at the wrong moment** → fix forward by recording a dated exception with an owner, not by disabling the gate.

## 8. Security and authorisation

Read-only analysis is risk class A. Adding notices files, policies, and CI configuration is B. Anything that republishes artifacts, changes an outbound licence, or rewrites dependency versions is C and requires `{{APPROVER}}`. Do not add or remove dependencies to make a licence problem disappear without running the project's tests — a licence fix that breaks the build is not a fix. Do not lift a legal question into your own judgement; the deliverable is a clearly framed decision for someone authorised to make it.

## 9. Completion criteria

- [ ] Distribution perimeter written down, artifact by artifact.
- [ ] Inventory built from the resolved graph, transitive included.
- [ ] Every package classified by obligation family, not just by label.
- [ ] Dev-only versus distributed verified, with false positives resolved by path.
- [ ] Dual licences and "or later" clauses resolved explicitly.
- [ ] Outbound licence checked against every inbound licence.
- [ ] Third-party notices generated, versioned, and shipped.
- [ ] Every non-permissive finding has a disposition with owner and expiry.
- [ ] Repository's declared licence matches its `LICENSE` file.
- [ ] CI gate fails on unapproved or unknown licences.
- [ ] Report states tool versions and blind spots.

## 10. Deliverables and handover

Artifacts: `.compliance/LICENCE_REPORT.md`, `.compliance/THIRD_PARTY_NOTICES.md`, CI step configuration, and the SBOM if one is produced.

Handover: `04-process/dependency-management/` P01 already flags licence posture during inventory — this prompt is its detailed follow-through and should be referenced from there rather than duplicated. `04-process/standards-conformance/` consumes the notice and SBOM evidence when a buyer or auditor asks. `07-workflows/compliance-readiness.md` sequences this with the rest of a procurement response. Supply-chain integrity (hashes, provenance, compromised packages) is `05-scenarios/supply-chain/`, a different question from what the licence permits.
