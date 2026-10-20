# Prompt Authoring Standard

**Version:** 2.0.0
**Applies to:** every prompt file in this repository
**Enforced by:** `scripts/validate_library.py`

This standard replaces the earlier loose template. It defines what a prompt file must contain, how it must be labelled, and what distinguishes an outline from an operational prompt.

---

## 1. Maturity levels (the honesty contract)

Every file declares exactly one maturity level. The level describes the artifact as it exists **now**, not what it is intended to become.

| Level | Meaning | Minimum characteristics |
|-------|---------|-------------------------|
| `skeleton` | Structural outline. Names the stage and the artifact, nothing more. | Title, metadata block, role, objective, 3–6 workflow steps, completion criteria. **Must not be presented to users as usable.** |
| `draft` | Substantive prompt, not yet reviewed against the rubric. | Full instruction set, verification section, failure handling; known gaps listed in the file. |
| `operational` | Complete and self-consistent; meets every required section; reviewed against `quality-rubric.md`. | All required sections, evidence rules, verification, failure handling, handover. |
| `canonical` | Reference implementation of this standard; other prompts should imitate its structure. | Everything in `operational`, plus demonstrated use on at least one real repository and cited in at least one workflow. |

Rules:

1. A `skeleton` file **must not** claim "Operational", "Production-ready", "Complete", or version `1.x`.
2. Maturity may only be raised when the acceptance conditions for that level are true. Raising it is a review decision, not a copy edit.
3. `operational` and `canonical` stages inside a multi-stage system require the system's entry point (orchestrator or README) to state the correct system-level maturity. A system is only as mature as its weakest required stage.
4. Demoting a maturity level is always allowed and must be recorded in `CHANGELOG.md`.

## 2. Metadata block (machine-readable, human-useful)

The first twelve lines of every prompt file carry a metadata block. Bold-key lines are parsed by the validator; keep the key names exact.

```markdown
# PROMPT 03 — Structural Mapping
**Identifier:** EXAMPLE-P03
**System:** codebase-audit
**Version:** 1.1.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A
**Depends on:** AUDIT-P02
**Produces:** `AUDIT_STRUCTURE.md`
**Est. effort:** 15–40 min
```

Field rules:

- `Identifier` — unique across the repository, `^[A-Z][A-Z0-9]*(-[A-Z0-9]+)*$`. System-prefixed (`AUDIT-P03`), never reused after deletion.
- `System` — the folder that owns the prompt (`codebase-audit`, `testing-qa`, `workflows`, …).
- `Version` — semantic version of the prompt file itself.
- `Maturity` — one of the four levels above, lowercase.
- `Execution mode` — exactly one primary mode (see §3). Secondary modes may be listed after the primary, comma-separated.
- `Risk class` — the **highest** action category the prompt can reach: `A` read-only, `B` local mutation, `C` external/network side effect, `D` high-risk. See `00-core/safety-and-security/ACTION-CATEGORIES.md`. A read-only audit prompt must be `A` even if the surrounding workflow is `C`.
- `Depends on` / `Produces` — identifiers and named artifacts. Use `none` when genuinely none.
- `Est. effort` — optional but encouraged; helps a human decide whether to run the stage now.

## 3. Execution modes

Pick the mode that matches what the agent is authorised to do. Modes are not decoration: they set the stopping rule.

| Mode | Agent may | Stopping rule |
|------|----------|---------------|
| `diagnostic` | Read, run non-destructive checks, report | Report delivered with evidence; **no file edits** |
| `planning` | Read, analyse, produce a plan | Plan with acceptance criteria and sequencing |
| `implementation` | Edit code/tests/docs within an authorised scope | Changes made **and** verification actually run |
| `audit-remediation` | Diagnose, prioritise, then fix authorised findings | Findings list + remediated subset + re-verification |
| `autonomous-completion` | Run the full loop across a larger workflow | End-to-end acceptance check, honest completion report |
| `research` | Investigate alternatives, prototype where cheap | Evidence-backed recommendation with confidence |
| `continuous-improvement` | Reassess, improve, re-validate | Measurable delta against a stated baseline |
| `orchestration` | Coordinate stages or specialist agents | All stages accounted for; integration verified |
| `specialised` | Domain-specific operation (migration, incident, security assessment) | Domain-specific exit criteria stated in the prompt |

A prompt that says "diagnose the codebase" must not start editing. A prompt that says "implement the fix" must not stop at a recommendation unless it records a concrete blocker.

## 4. Required sections

Every prompt at `draft` or above contains these sections, in this order. Headings may add detail but must keep these names discoverable.

1. **Role and mandate** — the specialist stance, in one short paragraph. No empty superlatives.
2. **Objective and scope** — what this stage is responsible for, and explicitly what it is *not*.
3. **Prerequisites and inputs** — required prior artifacts, tools, permissions, user-supplied context. Mark which are discovered vs supplied.
4. **Workflow** — numbered, concrete steps. Each step names what to inspect, what to decide, and what to write.
5. **Decision rules and evidence standard** — how to choose between options; what counts as sufficient evidence; how to mark uncertainty.
6. **Verification** — the checks to run or the evidence to produce, and what "passing" means.
7. **Failure handling** — what to do when context is missing, a tool fails, or the work is blocked.
8. **Security and authorisation** — the risk class restated in operational terms; what not to touch.
9. **Completion criteria** — a checklist that can be evaluated by a reviewer who trusts nothing.
10. **Deliverables and handover** — artifacts produced, their paths, and exactly what the next stage needs.

`implementation` and `audit-remediation` prompts additionally require:

11. **Regression protection** — what must not break, and how that will be checked.
12. **Rollback** — how to undo the change if verification fails.

## 5. Writing rules

- **Specific over inspirational.** "Run `pytest -q tests/unit` and paste the summary line" beats "ensure quality".
- **Name artifacts and paths.** A stage that produces "insights" produces nothing.
- **One authority per rule.** Do not restate the same constraint in four sections; reference `00-core/` primitives instead.
- **Adaptive, not stack-assuming.** Detect language, package manager, test runner. Never hardcode a convention the repository has not confirmed.
- **Proportional length.** A single-task prompt that fits in 40 lines should not be 300.
- **No invented capability.** Do not instruct the agent to use a tool, endpoint, credential, or sandbox it may not have. Phrase optional capabilities as "if available".
- **Uncertainty is labelled.** Every factual claim about the target system carries `verified` (with a path/command) or `inferred` (with reasoning) or `unknown`.
- **No prompt may instruct an agent to declare success without having run a check.**

## 6. Placeholders

Use bracketed, uppercase placeholders only for information the executing agent genuinely cannot discover:

`[REPOSITORY_PATH]` `[TARGET_BRANCH]` `[PRIMARY_OBJECTIVE]` `[TICKET_OR_ISSUE]` `[TIME_BUDGET]` `[CONSTRAINTS]`

Anything discoverable from the repository (stack, test command, conventions, architecture) must be **discovered**, not requested. Never ask the user for facts that are in the working tree.

## 7. Naming and placement

- Folders: `kebab-case`; stage folders: `P<NN>-Short-Name`.
- Files: `P<NN>-Descriptive-Name.md`; single-purpose prompts: `UPPER-KEBAB-CASE.md`.
- Stable entry point per system: `README.md` (overview, stage table, usage) plus an orchestrator prompt when the system is multi-stage.
- Workflow chains live in `07-workflows/`, never inside a system folder.
- Deprecated material moves to `archive/` with a `README.md` explaining why, and its identifier is retired, not reused.

## 8. Definition of done for a prompt

A prompt is done when all of the following are true:

- [ ] Metadata block complete and internally consistent (maturity matches content).
- [ ] Every required section present and non-empty.
- [ ] Role is a real specialist stance, not praise.
- [ ] Scope states what the stage is *not* responsible for.
- [ ] Workflow steps are executable without further interpretation.
- [ ] Deliverables name concrete artifacts.
- [ ] Verification is runnable and failure-aware.
- [ ] Risk class is honest; no hidden `C`/`D` actions in an `A` prompt.
- [ ] No contradiction with `00-core/` primitives.
- [ ] Passes `python3 scripts/validate_library.py`.
- [ ] Reviewed against `_meta/quality-rubric.md` at the tier for its mode.

`created` ≠ `reviewed` ≠ `validated` ≠ `empirically tested`. Do not collapse these in a status report.
