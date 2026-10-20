# Reproducible Dev Environment — one command, every editor, any machine

**Identifier:** DEVENV-01
**System:** 05-scenarios/dev-environment
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B (class C if the environment reaches shared databases or cloud credentials)
**Depends on:** none
**Produces:** `.devenv/ENVIRONMENT.md`, a working container/setup path, editor configuration
**Inputs:** REPO_PATH, TARGET_OS (optional: EDITORS, RUNTIME_VERSION, TEAM_SIZE)
**Est. effort:** 1–3 h for a first setup; 10 min per editor verification

---

## 1. Role and mandate

You make "clone and run" true. Today it is usually false: the README assumes a version nobody has, the build works on macOS and fails on Windows because of path case, one developer's machine has a global package installed, and CI has a fourth configuration.

The measure is brutal and fair: **a new machine reaches a passing test run using only what is in the repository, on every OS the team uses, without asking anyone.**

## 2. Objective and scope

**Produce:** a documented, reproducible environment path (container or scripted), pinned runtimes, editor-agnostic configuration, and a verification that was run on at least one clean machine per supported OS class.

Out of scope: deployment environments (`05-scenarios/deployment-target/`), CI design beyond parity checks, production infrastructure.

## 3. Prerequisites and inputs

- `{{REPO_PATH}}` read-only first, then a branch to change.
- `{{TARGET_OS}}` — the OS classes that must work (`Linux`, `macOS`, `Windows + WSL`, `Windows native`). Do not claim Windows support you did not test.
- `{{EDITORS}}` — the editors actually in use (`VS Code`, `Cursor`, `Windsurf`, `JetBrains`, `Neovim`, `Zed`); `{{RUNTIME_VERSION}}` if a version is mandated; `{{TEAM_SIZE}}` to judge how much automation is worth it.

## 4. Workflow

1. **Measure the current gap before fixing it.** On a clean machine or fresh container, follow only the repository's instructions. Record: first failure, time to first green test, number of manual steps, and every undocumented prerequisite you had to install. This number is the baseline you will quote later.

2. **Pin every runtime the project needs**, in files the tools read automatically: `.nvmrc`/`.node-version`, `.python-version`, `.tool-versions` (asdf), `.ruby-version`, `.java-version`, plus the package manager (`packageManager` field, `volta`, `corepack`). A version in the README is a suggestion; a version file is enforced.

3. **Eliminate hidden global state.** Any tool that must be installed globally (CLI, code generator, linter) belongs in the repository's dependency list or the container image, invoked through a script — not in someone's shell profile. Search for `npm install -g`, `brew install`, `pip install --user` in docs and scripts and replace them.

4. **Provide one entry point**, and only one:
   - **Container first** (`.devcontainer/devcontainer.json` + `docker-compose.yml`): the strongest guarantee, works with VS Code, Cursor, Windsurf, JetBrains Gateway, and plain `docker`.
   - **Script fallback** for machines where containers are not allowed: `make setup`, `./scripts/bootstrap.sh`, or `task setup` — idempotent, re-runnable, and it must fail loudly with a remedy rather than half-succeed.
   - Document both; the script is not a second-class path, it is what CI and the container both call.

5. **Make the database and services reproducible**: `docker-compose` with pinned image tags, a seed fixture, and a migrate+seed command. "Ask someone for a dump" is not a setup step. Never seed with production data; generate or anonymise.

6. **Configure editors generically, not personally.** `.editorconfig` for whitespace and line endings across all editors; format-on-save and lint settings in the *shared* project files (`.vscode/settings.json` committed, with a documented "recommended extensions" list), not in a personal profile. Anything tool-specific goes in a file the tool reads and that is committed — VS Code `tasks.json` and `launch.json` for build/test/debug, and the equivalent for other editors if the team uses them.

7. **Handle the OS classes you claim**, deliberately:
   - **Line endings** — `.gitattributes` with `* text=auto` and explicit binary types, or Windows checkouts will produce whole-file diffs.
   - **Path case sensitivity** — CI is Linux; a file imported as `./Button` when it is `button.tsx` works locally and fails in CI. Add a check.
   - **Shell differences** — scripts invoked via `sh` are not `bash`; npm scripts that assume `rm -rf` fail on cmd/PowerShell. Prefer cross-platform tooling or documented PowerShell equivalents.
   - **File watching limits** on Linux (inotify), and Docker file-sharing performance on macOS — name the workaround.

8. **Add a parity check** so the environment cannot drift from CI: the same commands CI runs must be runnable locally, with the same versions. If CI uses Node 22, `.nvmrc` says 22; if CI runs `pnpm test`, the setup installs pnpm at the pinned version.

9. **Verify on clean machines, not on yours.** Run the full path in a fresh container and on one machine per OS class. Record the commands, the time, and any manual step that remained. A step that cannot be automated is documented as a manual prerequisite with a check that detects its absence.

10. **Write `.devenv/ENVIRONMENT.md`:** supported OS classes with what was actually tested, the one-command path, the fallback, pinned versions, service topology, editor configuration, the manual steps that remain, the baseline time-to-green, and the known platform quirks.

## 5. Decision rules and evidence standard

- **Untested platform claims are false.** Mark unsupported OSes as unsupported rather than "should work".
- **Pinned, not documented.** A version in prose is a suggestion; a version file is enforcement.
- **One entry point.** Two setup paths diverge, and the second one rots.
- **Idempotent and loud.** A setup script that half-succeeds leaves a machine nobody can debug; it must stop at the first failure and say what to do.
- **Never seed production data.** Synthetic or anonymised fixtures only.
- **Editor config is shared or absent.** Personal dotfiles do not travel with the repository.
- **CI is the reference environment.** Local dev should match it, not the other way round.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Baseline measured | clean container run | first failure and time recorded |
| Runtimes pinned | version files exist | auto-read by the tools |
| No global installs | search docs/scripts | every dependency is local or containerised |
| One entry point works | fresh container | green tests from a clean clone |
| Services reproducible | compose up + seed | database ready with fixtures |
| Editor config committed | repo check | settings/tasks/launch present and generic |
| OS claims tested | per-OS run | only tested OSes claimed |
| Line endings and case | `.gitattributes` + case check | no spurious diffs, no case-only imports |
| CI parity | compare versions and commands | identical |
| Time to green recorded | second clean run | stated, with manual steps listed |

## 7. Failure handling

- **Containers are not allowed** (corporate policy, no Docker Desktop licence) → the script becomes the primary path; make it more defensive, and record the reduced guarantee.
- **A dependency cannot be installed offline or in the sandbox** → vendor it or document the mirror; do not leave a silent network requirement.
- **Windows native behaves differently from WSL** → recommend WSL as the supported path and say plainly that native Windows is untested, rather than shipping a half-working script.
- **The database dump is the only source of schema** → treat that as a finding: migrations are the source of truth (`03-domains/database/` P01), and the dump is a fixture at best.
- **Setup takes longer than 20 minutes on a clean machine** → measure where the time goes; cache dependencies in the image, and report the number. Long setups get bypassed, and bypassed setups rot.
- **CI and local disagree** → CI wins; fix the local path, and add the parity check that would have caught it.

## 8. Security and authorisation

Risk class B: writes repository and container configuration. Never bake secrets or personal credentials into an image, a compose file, or a committed `.env`; use `.env.example` with names only. Development containers and MCP/agent tooling frequently mount the Docker socket or the home directory — do not add those mounts without saying what they grant. Seed data must be synthetic: a "small copy of production" is a data-protection incident with a friendly name.

## 9. Completion criteria

- [ ] Baseline measured on a clean machine, with the first failure recorded.
- [ ] All runtimes pinned in tool-readable files.
- [ ] No global installs required; dependencies are repository-local or containerised.
- [ ] One entry point, verified from a clean clone.
- [ ] Services reproducible with pinned images and a synthetic seed.
- [ ] Editor configuration committed and generic; recommended extensions listed.
- [ ] `.gitattributes` handles line endings; case-sensitivity check exists.
- [ ] CI parity confirmed (versions and commands).
- [ ] Each claimed OS tested; untested ones marked unsupported.
- [ ] Time to green and remaining manual steps recorded.

## 10. Deliverables and handover

Artifacts: `.devenv/ENVIRONMENT.md`, the container/script path, editor configuration.

Handover: `04-process/documentation/` P06 uses `.devenv/ENVIRONMENT.md` as the source for the handbook's setup page (it is the executed version, not a guess); `04-process/agent-context/` P02 links the setup command as the canonical "how to run" for agents; `05-scenarios/deployment-target/` reuses the pinned runtime versions so the platform build matches local.
