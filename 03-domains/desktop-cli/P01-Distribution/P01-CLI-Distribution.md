# PROMPT 01 — CLI Distribution and Updates

**Identifier:** DESK-P01
**System:** 03-domains/desktop-cli
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** C (signing keys and release channels; publishing to a package registry is outward-facing)
**Depends on:** none
**Produces:** `.cli/RELEASE.md`, a signing and checksum record, a channel policy
**Inputs:** TOOL_NAME, DISTRIBUTION (optional: PLATFORMS, PACKAGE_REGISTRY, AUTO_UPDATE, APPROVER)
**Est. effort:** 2–5 h

---

## 1. Role and mandate

You get a command-line tool onto other people's machines, and keep it there safely.

A CLI is distributed software with none of the platform's protections: no app store review, no notarisation by default, no automatic rollback. Users install it with `npm i -g`, `brew install`, `curl | sh`, or a binary they downloaded from a page that may or may not be yours. Every one of those paths is an integrity and trust decision that you either make deliberately or leave to chance.

## 2. Objective and scope

**Produce:** a distribution matrix per platform, signed and checksummed artifacts, an update mechanism with verification, a channel policy (stable/beta/nightly), and install/test evidence on clean machines.

Out of scope: GUI desktop application packaging (separate concerns), and marketing.

## 3. Prerequisites and inputs

- `{{TOOL_NAME}}` and `{{DISTRIBUTION}}` — package registry, GitHub Releases, Homebrew, apt/rpm, container image, or direct download, and the platform combinations that matter.
- `{{PLATFORMS}}` — macOS (Intel/ARM), Linux (glibc/musl, x64/ARM), Windows (x64/ARM), and whether WSL is the supported path.
- `{{PACKAGE_REGISTRY}}`; `{{AUTO_UPDATE}}` — yes/no, and if yes, whether the user can disable it.
- `{{APPROVER}}` — for signing keys and publishing.

## 4. Workflow

1. **Decide the install paths and own each one.** A `curl | sh` script is an execution primitive: it must serve a specific version (not `latest`), verify a checksum, and fail closed. A global npm install is convenient and slow, and inherits the user's Node version — if you ship one, say which versions are supported and enforce it at runtime with a clear error.

2. **Build reproducible, static artifacts**: one binary per platform/architecture, with the version embedded (`--version` must print something a bug report can use: version, commit, build date, target triple).

3. **Sign everything, and make verification possible**: cosign/minisign/GPG signatures or platform signing (macOS notarisation, Windows Authenticode). Publish checksums alongside, and make the install script verify them. An unsigned binary triggers a scary OS warning the user will click through.

4. **Design the update mechanism as a security boundary.** The updater fetches code and executes it: it must verify a signature over the artifact, pin to a channel, refuse downgrades unless asked, and never update silently mid-command. If auto-update cannot be made safe, do not ship it — print an upgrade hint on a schedule instead.

5. **Channels and pinning**: stable / beta / nightly, each with its own artifacts and its own users. A user must be able to pin a version and get it back (`<tool>@1.4.2`) — the absence of a pin is why "it worked yesterday" is unanswerable.

6. **Handle PATH and shell integration honestly**: document where the binary goes, whether a shell restart is needed, and how to uninstall completely. A tool that leaves shims, completions, and config behind after uninstall is resented.

7. **Handle the package-manager ecosystems correctly**: Homebrew formula/tape, apt/rpm with a signed repository, a container image with a pinned digest. Each has its own update cadence and its own way of being wrong (stale formula, unsigned repo, mutable tag).

8. **Test installation on clean machines**, per platform: a fresh container or VM, no pre-installed runtime, following only the documented instructions. Record time to first successful command, and every manual step that remained.

9. **Publish what the artifact contains**: version, changelog, supported platforms, checksums, signatures, and the licence. A release page without checksums is a download you cannot verify.

10. **Write `.cli/RELEASE.md`**: install paths, artifact matrix, signing and verification steps, update mechanism and its threat model, channels and pinning, uninstall procedure, and the clean-machine test log.

## 5. Decision rules and evidence standard

- **Every install path is a trust boundary**; verify downloads or do not offer the path.
- **Never serve `latest` to a pipe-to-shell script** — pin and verify.
- **`--version` must identify the build** precisely enough for a bug report.
- **The updater verifies signatures**; otherwise it is a remote code execution channel by design.
- **Users can pin, and pinning works.**
- **Clean-machine installs are the evidence**, not a successful local build.
- **Uninstall is part of the product.**

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Install on clean OS | Fresh VM/container per platform | Works from the documented steps alone |
| Version output | `--version` | Version, commit, build date, target |
| Checksums | Compare download to published value | Match; mismatch fails closed |
| Signature | Verify artifact | Valid; unsigned path absent |
| Install script | Inspect | Pinned version, verified checksum, no silent fallback |
| Update path | Test from previous version | Signature verified, no downgrade |
| Channels | Install from each | Correct version per channel |
| Pinning | `tool@x.y.z` | Exact version restored |
| PATH and shell | Fresh shell | Command resolves; docs match reality |
| Uninstall | Remove and reinstall | No residue, or documented residue |
| Package manager | brew/apt/npm install | Same version and binary behaviour |

## 7. Failure handling

- **The OS blocks an unsigned binary** → sign and notarise, or document the bypass precisely; do not tell users to disable Gatekeeper.
- **A dependency cannot be built for an architecture** → ship a pure-Go/Rust-style static binary, or state the unsupported combination explicitly rather than publishing a broken artifact.
- **The update mechanism breaks a user's workspace** (new major version changes behaviour) → pin major versions in the updater, and require explicit consent for major upgrades.
- **The registry is compromised or a package is hijacked** → this is a supply-chain incident (`05-scenarios/security-incident/`): revoke, deprecate the version, publish a security advisory, and rotate any token used to publish.
- **Users install an old version from a stale mirror** → publish checksums and a version endpoint so support can identify the build from `--version`.
- **The install script needs `sudo`** → that is a design smell; prefer a user-local path or a package manager, and say why if not.

## 8. Security and authorisation

Risk class C. Signing keys live in CI or an HSM, never on a laptop; publishing tokens are scoped to the single package and rotated (`02-engineering/secrets-rotation/`). The updater is the highest-risk component in the product: it downloads executable code, so it must verify signatures against a pinned public key and refuse to run unsigned artifacts. Install scripts must not read unrelated files or environment variables.

## 9. Completion criteria

- [ ] Install paths chosen, documented, and each tested on a clean machine.
- [ ] Artifacts built per platform/architecture with embedded version metadata.
- [ ] Checksums published; install script verifies them and fails closed.
- [ ] Artifacts signed; verification documented.
- [ ] Updater verifies signatures, respects channels, and cannot downgrade silently.
- [ ] Channels defined; version pinning works.
- [ ] PATH, shell integration, and uninstall documented and tested.
- [ ] Package-manager paths tested with signed repositories.
- [ ] Release page lists version, changelog, checksums, signatures, licence.
- [ ] Time to first command recorded per platform.

## 10. Deliverables and handover

Artifacts: `.cli/RELEASE.md`, signed artifacts, checksums, clean-install log.

Handover: `04-process/release-engineering/` owns the version scheme and changelog; `02-engineering/secrets-rotation/` registers signing keys and publishing tokens; `04-process/documentation/` publishes the install guide that was actually tested; `04-process/legacy... ` — if the tool replaces an older one, `04-process/decommissioning/` retires the old distribution channel and its credentials.
