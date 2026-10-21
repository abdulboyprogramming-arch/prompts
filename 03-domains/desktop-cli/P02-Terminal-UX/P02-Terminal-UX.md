# PROMPT 02 — Terminal UX, Signals, and Exit Codes

**Identifier:** DESK-P02
**System:** 03-domains/desktop-cli
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** A (reads and modifies the tool's own output code; no destructive actions)
**Depends on:** none
**Produces:** `.cli/TERMINAL_UX.md`, a behaviour test matrix
**Inputs:** TOOL_NAME, COMMANDS (optional: PLATFORMS, SHELLS, TARGET_ENV)
**Est. effort:** 2–3 h

---

## 1. Role and mandate

You make the tool behave correctly when it is *not* a human watching a terminal — which is most of the time.

The contract of a well-behaved CLI is older and stricter than most modern tools assume: stdout is for data and can be piped; stderr is for humans and diagnostics; exit codes are the API; signals are how the outside world says stop; and a TTY may not exist at all. Break any of these and the tool becomes unusable in scripts, CI, and automation — the environments where it matters most.

## 2. Objective and scope

**Produce:** a specified behaviour matrix (TTY and non-TTY, each signal, each error class), corrected output handling, and tests that exercise it without a terminal.

Out of scope: distribution (`DESK-P01`), and the tool's core functionality.

## 3. Prerequisites and inputs

- `{{TOOL_NAME}}`, `{{COMMANDS}}` — the commands whose output contract matters (data-producing, interactive, destructive).
- `{{PLATFORMS}}` — Linux, macOS, Windows (where signals differ substantially), and `{{SHELLS}}` — bash, zsh, fish, PowerShell, cmd.
- `{{TARGET_ENV}}` — test in a container and in a real terminal; both, because they behave differently.

## 4. Workflow

1. **Define the exit-code contract before touching output**: `0` success, `1` general failure, `2` usage error (the shell's convention), and documented distinct codes for the cases scripts must branch on (not found, conflict, permission denied). Never return `0` on a partial failure — a script that cannot detect failure is worse than a tool that crashes.

2. **Separate the streams**: machine-readable data on stdout, everything else (progress, warnings, prompts, colour) on stderr. `tool list | jq` must work with no flags, and `tool list > file` must produce a clean file.

3. **Detect the TTY and adapt**: no colour, no spinners, no progress bars, no interactive prompts when stdout or stderr is not a terminal. Provide explicit overrides (`--color=auto|always|never`, `--no-progress`, `--yes`) because CI sometimes *is* a TTY through a wrapper.

4. **Support the environment variables users already have**: `NO_COLOR`, `CLICOLOR`, `TERM=dumb`, `CI`, and `FORCE_COLOR`. Ignoring `NO_COLOR` is a compatibility bug in 2026, not a preference.

5. **Handle signals explicitly**: on `SIGINT` (Ctrl-C), stop work, clean up temporary files and lock files, and exit with the conventional code (`130`); on `SIGTERM`, do the same and exit promptly; on `SIGPIPE` (a piped consumer closed early, e.g. `| head`), exit quietly rather than printing a stack trace. Never leave a half-written file or a held lock.

6. **Make interactive prompts safe**: never prompt when stdin is not a TTY (fail with a clear message and a flag to supply the value); never default to destructive; require explicit confirmation for irreversible operations; and make `--yes` documented and visible in `--help`.

7. **Design `--help` and error messages as the primary documentation**: usage, a realistic example per subcommand, exit codes, and where to report bugs. An error must name what was wrong, where, and what to do next — not print a stack trace unless `--debug` was requested.

8. **Handle Windows differences explicitly**: signal semantics, `\r\n`, path separators, ANSI support, and console encoding. A tool that only works in WSL should say so.

9. **Support machine-readable output deliberately**: `--json` (or a structured format) for the data commands, with a stable schema and a documented version. Humans get tables; scripts get JSON; never both on the same stream.

10. **Write `.cli/TERMINAL_UX.md`** with the exit-code table, per-command behaviour in TTY and non-TTY, signal handling, environment-variable support, and the test matrix used to verify it.

## 5. Decision rules and evidence standard

- **stdout is data; stderr is commentary.**
- **Exit codes are the API** and must distinguish the cases scripts branch on.
- **Never prompt without a TTY**; never default to destructive.
- **Honour `NO_COLOR`**, and provide explicit flags for the rest.
- **SIGPIPE is normal**, not an error to report.
- **Clean up on interruption** — temp files, locks, partial downloads.
- **A stack trace is not an error message.**

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Exit codes | Script asserting each case | Documented code per outcome; no false success |
| Stream separation | `tool cmd > out` | File contains data only |
| Pipe safety | `tool cmd \| head -1` | No broken-pipe traceback |
| Non-TTY | Run with stdin/stdout redirected | No spinner, no colour, no prompt |
| NO_COLOR | Set the variable | No ANSI sequences |
| --color override | Each mode | Behaviour matches the flag |
| SIGINT | Send during a long operation | Clean exit 130, no residue |
| SIGTERM | Send during work | Prompt exit, cleanup performed |
| Interactive prompt | stdin closed | Fails with a message and a flag |
| Destructive default | Inspect | Confirmation required |
| --help | Read | Usage, examples, exit codes, bug link |
| --json | Pipe to a parser | Valid and stable schema |
| Windows | Run the matrix | Documented behaviour; unsupported modes stated |

## 7. Failure handling

- **A destructive command is used in a script** → require `--yes` or an explicit non-interactive flag and refuse otherwise; a prompt in a pipeline is a hang.
- **Colour leaks despite `NO_COLOR`** → check every output path, including error formatting and third-party logger defaults.
- **SIGINT leaves a lock file** → install a cleanup handler for every resource the command acquires, and write lock files with a PID and timestamp so a stale one can be detected.
- **Windows signals differ** → implement the Ctrl-C handler in the runtime's portable form, and document what is not interruptible.
- **Users pipe JSON output into tools that expect tables** → keep the human format default only for interactive use; when piping, print data, or require `--json` explicitly and say so in `--help`.
- **The output schema changes** → version it and note the change; a script that parses your output is a consumer with the same rights as an API consumer (`API-VER-01`).

## 8. Security and authorisation

Risk class A: changes its own output and signal handling. Never print secrets, tokens, or full request payloads in verbose mode; redact by default and require an explicit debug flag to show more (with a warning). Prompts that ask for credentials must not echo input. Colour codes must not be used to convey meaning alone (the same rule as `A11Y-01`).

## 9. Completion criteria

- [ ] Exit-code table documented and implemented; no false success on partial failure.
- [ ] Data on stdout, everything else on stderr.
- [ ] Non-TTY behaviour verified (no colour, spinner, or prompt).
- [ ] `NO_COLOR` and `--color` honoured.
- [ ] SIGINT/SIGTERM clean up and exit with conventional codes.
- [ ] SIGPIPE handled quietly.
- [ ] Prompts require a TTY; destructive actions require explicit confirmation.
- [ ] `--help` includes examples, exit codes, and a bug link.
- [ ] `--json` output stable and documented.
- [ ] Windows behaviour tested and documented.
- [ ] Behaviour test matrix in CI, at least for the signals above.

## 10. Deliverables and handover

Artifacts: `.cli/TERMINAL_UX.md`, behaviour tests, updated help text.

Handover: `04-process/documentation/` uses the tested `--help` content as the reference page; `A11Y-01` applies the same non-colour-only rule to terminal output; `API-VER-01`'s compatibility rules apply to the JSON schema, because a script that parses it is a consumer; `05-scenarios/background-jobs/` reuses the exit-code contract when the tool is invoked from cron.
