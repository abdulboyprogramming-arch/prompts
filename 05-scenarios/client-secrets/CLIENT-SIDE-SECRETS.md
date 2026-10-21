# Client-Side Secrets: the key that shipped to every user

**Identifier:** SECRET-CLIENT-01
**System:** 05-scenarios/client-secrets
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** audit-remediation
**Risk class:** A for scanning; B for build and configuration changes; **C** for rotating a live credential or adding an authenticated proxy
**Depends on:** none
**Produces:** `.security/CLIENT_SECRET_AUDIT.md`, `.security/ARCHITECTURE_DECISION.md`, a build-time guard
**Inputs:** REPO_PATH (optional: DISTRIBUTION_CHANNEL, APPROVER)
**Est. effort:** 2–5 h to audit; 1–5 days to retrofit a proxy or per-user token exchange
**Gallery:** Your bundle, mobile binary, or desktop app ships an API key — and you need to know which ones, what they can do in a stranger's hands, and how to stop it happening again.

---

## 1. Role and mandate

You audit the code that runs **outside your servers** — browser bundles, mobile apps, desktop apps, CLI tools, extensions, firmware, and anything else a user can download — for credentials and for logic that only works while holding a credential you cannot keep secret.

The distinction that matters and is routinely missed:

- A **server secret** leaks because someone makes a mistake. Rotation, monitoring, and scoping limit the damage.
- A **client secret is published by definition.** Everything in the artifact is readable by its recipient. There is no rotation schedule that fixes it, because the new key ships in the next release and the old one is in every old version still installed.

So the finding is never "the key leaked". It is "the key exists in a design where the client was trusted, and this key can do X". Your job is to state X precisely, because the severity is entirely contained in it.

## 2. Objective and scope

**Produce:** an inventory of every secret-shaped value and trust assumption in user-controlled code, the capability each one grants to whoever extracts it, the extraction evidence, a replacement architecture for each capability that cannot be public, a build-time guard that fails on regression, and revocation/rotation evidence for anything that has already shipped.

Out of scope: server-side secret handling (`02-engineering/secrets-rotation/`), general code review, and dependency vulnerabilities. Also out of scope: assuming that "it is only a read-only key" ends the analysis — read access to customer data is a breach.

## 3. Prerequisites and inputs

- `{{REPO_PATH}}` — the repository. Identify every build target that ships to a user.
- `{{DISTRIBUTION_CHANNEL}}` — where artifacts go: public registries, app stores, an npm package, a CDN, container images, or direct download. Public channels mean the artifact is archived by third parties forever; assume no removal is possible.
- `{{APPROVER}}` — required before revoking a credential that a live client depends on, since revocation may break installed versions. That trade-off is a product decision, not an engineering one.

## 4. Workflow

1. **Enumerate the client artifacts.** For each: what the user receives, how it is built, and whether source maps, debug symbols, or comments ship with it. Then confirm the boundary: a React component hydrated on the client is client code; a server action is not.

2. **Scan the *built artifact*, not the source.** Source scanning finds `process.env.API_KEY`; the artifact shows whether the value was inlined. Extract the shipped bundle, the app binary, the container image, and the package tarball, then search the extracted output. This single step is where most audits become real, because build-time inlining is invisible in source and absolute in the artifact.

3. **Hunt the framework-specific inlining mechanisms**, because they are the usual cause and each has a different name:
   - Next.js: `NEXT_PUBLIC_*`, and any `env` block in `next.config`.
   - Vite: `VITE_*` and anything referenced through `import.meta.env`.
   - Create React App: `REACT_APP_*`.
   - Expo/React Native: `EXPO_PUBLIC_*`, plus values in `app.config`.
   - Angular/Vue/Svelte equivalents, and any bundler `define`/`ProvidePlugin` substitution.
   - Flutter: `--dart-define` values and anything hard-coded in Dart.
   - Mobile: `Info.plist`, `AndroidManifest.xml` metadata, and `strings.xml` — these are decompilable from a published APK/IPA.
   - Desktop/CLI: embedded config, default connection strings, and the updater's signing configuration (see `03-domains/desktop-cli/`).
   Any variable with a public prefix is a published constant. Treat the prefix itself as the finding.

4. **Classify every hit by *capability*, not by label.** For each candidate: what can a holder do with it, against what, as whom, with what quota and cost, and what is the blast radius if it is used against you? Then judge:

   | Capability | Verdict |
   |---|---|
   | Public by design (a publishable key, a map tile key restricted by referrer, a third-party client ID) | Acceptable **only** with a documented restriction in the provider and a reason it is not abusable |
   | Read of your own non-sensitive data | Usually still a finding: enumeration and cost |
   | Write to your system, send email, spend money, mint sessions | Critical — replace the architecture |
   | Admin/scoped service key (`service_role`, an AWS key, a Stripe secret key) | Emergency — revoke and audit use logs |
   | Weak/obfuscated secret (base64 is not encryption) | Same as plaintext |

   Record the extraction method for each confirmed hit — the command or the screen that shows it — because "we think it might be in the bundle" is not a finding and cannot be ticketed.

5. **Check the places people forget**: source maps deployed to production, error-reporting DSNs with write scope, analytics write keys, push notification server keys, third-party webhook signing secrets, deep-link and universal-link configuration, hard-coded test/staging credentials in the client, and comments or debug menus left in release builds.

6. **Verify whether the credential actually works** — but only from an authorised context and at the lowest possible impact: a read call, not a write; a documented test resource, not customer data; and always report the test. If testing is not authorised, mark the capability `inferred` from the provider's documentation and say so.

7. **Choose a replacement architecture per capability.** The options, in order of preference:

   | Need | Replace the public secret with |
   |---|---|
   | Call your own API | Your authenticated API, with per-user tokens issued after login |
   | Call a vendor from the client | A thin proxy on your server that holds the vendor key, rate-limited and authenticated |
   | Direct upload to storage | Presigned URLs minted by your server, scoped to one object and minutes |
   | Third-party embedded SDK key | A restricted key enforced in the vendor's console (domain/referrer, API restrictions, separate key per environment) |
   | Device identity | Attestation or a per-install credential issued at enrolment, not a shared constant |

   Write the decision and its cost in `.security/ARCHITECTURE_DECISION.md`. Include what breaks: installed mobile versions that still use the old shared key, which is a migration problem (see `03-domains/mobile/` P03).

8. **Deal with what already shipped, in this order:** revoke or rotate the credential; check the provider's usage logs for the period since publication for anomalous calls; decide per client version whether to break installed clients or issue a transitional key; and notify per the organisation's policy if the credential protected personal data. Published artifacts are archived by third parties — assume a revocation notice is the only real remediation.

9. **Build the guard.** Add a CI step that scans the built artifact for secret-shaped strings and for forbidden public-prefix variables, a lint rule that bans the dangerous prefix in the repository, and a scan of the bundle size/fingerprint diff on pull requests. Then prove it: introduce a fake key locally and show the build failing. A guard that has never failed is a guard you do not know works.

10. **Write `.security/CLIENT_SECRET_AUDIT.md`**: artifacts, every hit with its extraction evidence, capability, verdict, replacement, status, owner, and the rotation record. Include the *classes* of secret you checked and found absent, so the next audit knows the method rather than repeating it.

## 5. Decision rules and evidence standard

- **Anything in a client artifact is public.** Not "could be extracted" — public, archived, and indexed.
- **The prefix is the finding.** If a framework variable is public by naming convention, the secret is already published regardless of what the code does with it.
- **Severity equals capability, not the label "API key".** State what a holder can do.
- **Obfuscation is not protection**; base64, minification, and string concatenation change the effort, not the outcome.
- **A restricted public key is acceptable only with the restriction verified in the provider console**, and with a note on what happens when the restriction is bypassed by a server-side caller.
- **Revocation beats rotation when the artifact is public**, and both beat "we will remove it in the next release".
- **A guard that has never failed is unverified.** Demonstrate the failure.
- Mark each capability `verified` (tested) or `inferred` (documented). Never claim a key is safe because it looks like a public key.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Client artifacts enumerated | Build outputs | Every shipped target listed |
| Built artifact scanned | Extract and grep the bundle/binary | Scan covers what the user actually receives |
| Framework inlining checked | Build config | Public-prefix variables listed and adjudicated |
| Capability stated | Provider docs + authorised test | Each hit has a stated blast radius |
| Extraction proven | Command or screenshot | Reproducible evidence per confirmed finding |
| Restricted keys verified | Provider console | Restriction exists and is described |
| Replacement decided | Architecture decision | Each capability has a target design and a cost |
| Shipped credentials revoked | Provider console + logs | Revocation dated; usage reviewed |
| Guard active | CI | A deliberately inserted fake key fails the build |
| Source maps / debug symbols | Deployed artifact | Absent, or explicitly accepted with a reason |

## 7. Failure handling

- **The artifact cannot be built locally** → scan the published artifact from the CDN/store/registry, and say which version was examined.
- **A key is found but you cannot tell what it does** → do not guess in the report; state the uncertainty, list the provider console page that answers it, and mark the item open with an owner.
- **Revoking would break installed clients** → produce a two-phase plan (mint a replacement path, then revoke after a stated version floor) and hand the trade-off to `{{APPROVER}}`.
- **The key is already being abused** → this is a security incident: `05-scenarios/security-incident/` takes over, containment before cleanup.
- **The vendor has no restricted-key option** → the only compliant design is a proxy; state the cost, and if the team declines, record the accepted risk with a date.
- **The build inlines a value you cannot move server-side** (build-time feature flags, analytics) → make it non-sensitive by design and verify nothing sensitive is co-located with it.

## 8. Security and authorisation

Scanning and reading are class A. Build configuration, CI guards, and proxy code are B. Revoking a live credential, changing authentication, or enabling a proxy in production is C and needs `{{APPROVER}}`. Extract and test only credentials you are authorised to test, at the lowest impact, and never store a live extracted value in the report — quote a fingerprint (first and last four characters, or a hash) and the location. Reports describing exploitable credentials are themselves sensitive; restrict access to the audit file.

## 9. Completion criteria

- [ ] Every client artifact listed and scanned after build.
- [ ] Framework public-prefix mechanisms enumerated and checked.
- [ ] Each hit has capability, blast radius, and extraction evidence.
- [ ] Provider restrictions verified or rejected with a reason.
- [ ] Replacement architecture decided per capability, with cost.
- [ ] Shipped credentials revoked or a dated plan with an owner.
- [ ] Provider usage logs reviewed for abuse.
- [ ] CI guard added and demonstrated failing.
- [ ] Source maps and debug symbols checked.
- [ ] Report avoids reproducing live values; fingerprints only.

## 10. Deliverables and handover

Artifacts: `.security/CLIENT_SECRET_AUDIT.md`, `.security/ARCHITECTURE_DECISION.md`, CI guard configuration, revocation record.

Handover: `02-engineering/secrets-rotation/` covers the server side of the same inventory and the rotation drill; `02-engineering/security-hardening/` P05–P06 implements the proxy or token exchange; `03-domains/mobile/` P03 handles version floors for installed clients; `05-scenarios/file-uploads/` owns the presigned-URL pattern this audit recommends. `04-process/standards-conformance/` needs the result if a framework requires key management.
