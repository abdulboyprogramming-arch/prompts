# Desktop & CLI Tooling

**Maturity: operational (v1.0.0).** Two stages for software that ships to a machine you do not control and runs in a terminal you cannot see.

**Entry point:** [`P01-Distribution/P01-CLI-Distribution.md`](P01-Distribution/P01-CLI-Distribution.md)
**Execution mode:** implementation
**Per stage:** implementation (P01, class C), implementation (P02, class A)
**Identifiers:** `DESK-P01..P02`

## Why this system exists

This was the last **Missing** row in the coverage matrix. A CLI has none of the protections a hosted service inherits: no rollout, no rollback, no server-side fix. Distribution is a trust boundary (`curl | sh`, global npm installs, unsigned binaries), and the terminal contract — stdout versus stderr, exit codes, signals, TTY detection — is an API that most tools break silently.

## Stages

| ID | Stage | Purpose | Produces |
|----|-------|---------|----------|
| DESK-P01 | [Distribution & updates](P01-Distribution/P01-CLI-Distribution.md) | Install paths, signed artifacts, checksums, updater threat model, channels and pinning, clean-machine evidence | `.cli/RELEASE.md` |
| DESK-P02 | [Terminal UX & signals](P02-Terminal-UX/P02-Terminal-UX.md) | Exit-code contract, stream separation, TTY detection, signal handling, help as documentation | `.cli/TERMINAL_UX.md` |

## The rules

1. **Every install path is a trust boundary** — verify downloads or do not offer the path.
2. **Never pipe `latest` into a shell**; pin and verify.
3. **The updater verifies signatures** — it is remote code execution by design.
4. **stdout is data, stderr is commentary.**
5. **Exit codes are the API**; no false success.
6. **Never prompt without a TTY**; never default to destructive.
7. **`NO_COLOR` is a compatibility requirement**, not a preference.
8. **Clean up on interruption**, and exit with conventional codes.

## Proportionality

| Situation | Run |
|-----------|-----|
| Releasing a CLI for the first time | DESK-P01 |
| A pipeline hangs on an interactive prompt | DESK-P02 |
| Adding auto-update | DESK-P01 step 4 — treat as a security review |
| Users report "it works but scripts break" | DESK-P02 |
| Publishing to Homebrew/apt/npm | DESK-P01 step 7 |

## Boundaries

- Desktop GUI packaging and app-store distribution: `03-domains/mobile/` patterns apply to stores; GUI frameworks are out of scope.
- The tool's runtime behaviour and configuration: the owning domain.
- Supply-chain compromise of a published package: `05-scenarios/security-incident/`.

## What this system will not do

- Guarantee that a package registry has not been compromised — it makes detection and response possible.
- Replace platform notarisation or signing services.
- Design the tool's command surface — only its contract with the shell.
