# PROMPT 02 — Authoring the Canonical Context

**Identifier:** CTX-P02
**System:** 04-process/agent-context
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B
**Depends on:** CTX-P01
**Produces:** `AGENTS.md` (canonical), thin tool adapters, `.agent-context/AUTHORING.md`
**Inputs:** REPO_PATH, AGENT_TOOLS (optional: BRANCH, TEAM_SIZE)
**Est. effort:** 1–3 h

---

## 1. Role and mandate

You write the one file that tells a coding agent how this repository works, and you make every other tool file a pointer to it. The measure of success is not length or completeness — it is whether an agent that reads only this file **does the right thing on the first attempt** and stops before doing the wrong one.

Agent context fails in four predictable ways: it is an essay nobody finishes, it repeats the README, it states things that are no longer true, and it never says *what not to do*.

## 2. Objective and scope

**Produce:** a canonical `AGENTS.md` at the repository root (plus nested `AGENTS.md` only where a subtree genuinely differs), minimal per-tool adapters for `{{AGENT_TOOLS}}`, and a short authoring record explaining the choices.

Out of scope: verifying adherence (P03) — though you write the probes P03 will use; human onboarding docs (`04-process/documentation/`, handbook product); CI changes beyond what an adapter needs.

## 3. Prerequisites and inputs

- `.agent-context/SURFACES.md` — what exists, what conflicts, what is missing.
- The repository at `{{REPO_PATH}}`, on `{{BRANCH}}`; `{{AGENT_TOOLS}}` determines which adapters are needed; `{{TEAM_SIZE}}` decides whether nested files are justified (a monorepo with separate teams may need them; a single team does not).

## 4. Workflow

1. **State the contract in the first screen.** Five things, in this order, before anything else:
   - what the project is (one sentence, not a pitch);
   - the three commands that matter (install, test, run);
   - the boundary — what an agent must never do without asking;
   - where the deeper documents live;
   - how to verify a change is correct.

   An agent that reads only the first fifteen lines should already be able to avoid the worst outcomes.

2. **Write commands that exist, exactly as they run.** Copy them from the build files, run each once, and paste the real invocation — including the working directory and any required environment (`pnpm --filter api test`, not "run the tests"). Commands are the most-used and most-stale part of agent context.

3. **Encode the conventions an agent cannot infer from the code**: where new modules belong, naming, error-handling style, test placement, commit and branch format, generated files that must not be edited by hand, and the migration workflow. Keep each to one line with a pointer to the canonical document.

4. **State the prohibitions explicitly and concretely.** "Be careful" is not a boundary. Write: do not modify `migrations/` directly; do not commit `.env`; do not run `deploy` on a shared branch; do not edit `src/generated/**`; ask before adding a dependency; do not touch `billing/` without a reviewer. Each prohibition should say *what to do instead*.

5. **Say how to verify.** The test command, the type-check, the lint, the definition of done. An agent that cannot self-check will declare completion on a green compile.

6. **Add a "when stuck" section**: what to do when a test fails twice, when the environment is missing a dependency, when the task is ambiguous. This is the section that stops agents from inventing a solution to a misread task.

7. **Keep the file small enough to be read every time.** Target under ~200 lines for the root file; every added line costs tokens on every request and competes for attention. If a section is reference material, it belongs in a linked document, not here.

8. **Convert every other tool file into a thin adapter** of five to fifteen lines that states the canonical source and adds only what that tool requires (rule globs, frontmatter, a tool-specific command). Never let two files carry the same guidance — that is how drift starts.

9. **Handle nested context deliberately.** A nested `AGENTS.md` is justified when a subtree has different commands, a different language, or a different ownership boundary. It is not justified for emphasis. Where used, it must not contradict the root; conflicts resolve upward.

10. **Do not put secrets, internal URLs, customer names, or credentials in any context file.** Point to the store instead. Do not describe security controls in enough detail to help someone bypass them.

11. **Write the adapters** for the tools in `{{AGENT_TOOLS}}`: `CLAUDE.md` → pointer, `.cursor/rules/*.mdc` with correct `globs`/`alwaysApply`, `.github/copilot-instructions.md`, `.windsurf/rules`, `.aider.conf.yml` (read-only files, lint/test commands). Verify each tool's expected format rather than assuming it.

12. **Record the decisions** in `.agent-context/AUTHORING.md`: what is canonical, why each adapter exists, what was removed as duplication, and the probes P03 should run.

## 5. Decision rules and evidence standard

- **One canonical source; every other file is an adapter.** Duplication is the defect this stage exists to remove.
- **Every command is executed once before it is written.** An unverified command is a trap.
- **Prohibitions are concrete and paired with an alternative.** "Ask before X, do Y instead."
- **Short beats complete.** If it will not be read, it does not exist. Reference material belongs behind a link.
- **Describe the repository as it is, not as it should be.** Aspirational instructions teach agents to write code that does not fit.
- **No secrets, no customer data, no bypass recipes.**
- **Nested files only for genuine divergence**, never for emphasis.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| First screen has the five elements | inspect | all present, in order |
| Commands executed | run each | works as written |
| Conventions are inferable-proof | review | each has a pointer to the canonical doc |
| Prohibitions concrete | inspect | what, and what to do instead |
| Verification section present | inspect | test/typecheck/lint defined |
| "When stuck" section present | inspect | escalation path stated |
| Root file under ~200 lines | word count | within budget or justified |
| Adapters thin | diff | ≤15 lines each, no duplicated guidance |
| No secrets or customer data | scan | none |
| Tool formats correct | per-tool doc check | frontmatter/globs valid |

## 7. Failure handling

- **A tool's format is unclear or changing** → write the adapter conservatively (plain Markdown pointer) and record the uncertainty; a wrong format is worse than a generic one.
- **Teams disagree on a convention** → the canonical file states the current practice with a link to the decision, and the disagreement goes to the owning document. Do not encode two options "for flexibility"; that is how agents pick the wrong one.
- **The repository has no conventions to document** → say so explicitly ("no enforced style; match the nearest file") rather than inventing rules the reviewers will not apply.
- **The file would exceed the size budget** → move reference sections to `docs/` and link; keep the operational core.
- **An existing instruction file is politically owned** (someone's personal rules) → convert it to an adapter with their content preserved in the canonical file or a linked doc; do not delete their work silently.

## 8. Security and authorisation

Risk class B: writes repository files. Do not include tokens, internal hostnames, customer identifiers, or security-control bypasses. If an existing file contains a secret, do not copy it — record the finding, remove it from the new file, and recommend rotation (P01 should already have flagged it). Adapters must not widen permissions: if a tool config grants shell or network access, that is a separate reviewed change.

## 9. Completion criteria

- [ ] Canonical `AGENTS.md` with the five-element first screen.
- [ ] Every command executed and recorded verbatim.
- [ ] Conventions listed with pointers to canonical docs.
- [ ] Concrete prohibitions, each with an alternative.
- [ ] Verification and "when stuck" sections present.
- [ ] Root file within the size budget.
- [ ] Thin adapters for each configured tool; no duplicated guidance.
- [ ] Nested files only where divergence is real.
- [ ] No secrets or customer data.
- [ ] `.agent-context/AUTHORING.md` records decisions and the P03 probes.

## 10. Deliverables and handover

Artifacts: `AGENTS.md`, the adapters, `.agent-context/AUTHORING.md`.

P03 receives: the probes — the tasks an agent should complete correctly and the actions it should refuse — to test whether the context is actually obeyed rather than merely present.
