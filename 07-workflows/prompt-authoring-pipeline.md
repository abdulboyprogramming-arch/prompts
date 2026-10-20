# Workflow — Describe it, generate it, prove it, integrate it

**Identifier:** WF-PROMPTAUTH
**System:** 07-workflows
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** orchestration
**Risk class:** A (generates and evaluates text; integrating into the repository is B and separately authorised)
**Depends on:** GEN-P01, GEN-P02
**Produces:** a reviewed prompt (or family) with evaluation evidence and an integration decision
**Inputs:** PROMPT_INTENT (optional: TARGET_AGENT, LIBRARY_PATH, EVAL_FIXTURES)
**Gallery:** You need a prompt that does not exist yet, or need to know whether a rewrite is better: describe, route against existing coverage, generate, evaluate, decide, integrate.

---

## When to run this

- Someone has a task in mind and no prompt for it: *"I need something that audits our Terraform state."*
- An existing prompt is underperforming and nobody knows whether a rewrite would help.
- A repeated ad-hoc request has become a family: *"we keep asking for X, Y, Z."*
- A prompt is being added to this library and must clear the maturity gate honestly.

Do **not** run it to manufacture volume. A generated prompt that is never evaluated is a draft with good formatting.

## Entry conditions

- A task with no prompt covering it, or a prompt underperforming without evidence about why.
- `{{LIBRARY_PATH}}` available if the result is meant to be integrated, so routing can check for existing coverage.
- `{{PROMPT_INTENT}}` stated in one or two sentences; if it cannot be, run the interview first. `{{TARGET_AGENT}}` determines which tool conventions the generated prompt must follow.
- `{{EVAL_FIXTURES}}` or the authority to create them.

## The sequence

| Step | Run | Gate | Handoff artifact |
|---|---|---|---|
| 1. Describe | `GEN-P01` in `interview` or `compose` mode | `[GATE]` the operator confirms the five intent fields (actor, task, artifact, constraint, evidence) | Intent statement |
| 2. Check coverage | `GEN-P01` step 3 (routing) | `[GATE]` if ≥70% overlap: improve the existing prompt instead of adding a competitor | Routing record: existing ID or "none found" |
| 3. Generate | `GEN-P01` | Self-score ≥70, or the weak dimensions are accepted explicitly | Prompt + `VARIABLES.md` + `TEST-CASES.md`, marked `draft` |
| 4. Evaluate | `GEN-P02` | Three fixtures, two runs each, traces captured | `PROMPT_EVAL.md` with behavioural grades |
| 5. Decide | `GEN-P02` step 9 | `[GATE]` ship / ship-with-limitation / do-not-ship | Decision with evidence |
| 6. Integrate | `_meta/prompt-authoring-standard.md` + indexes | Validator 0/0; catalog and gallery regenerated; system README counts updated | Committed prompt, updated indexes |
| 7. Reassess | `_meta/coverage-matrix.md`, backlog | A gap row is closed or a new one is opened with evidence | Matrix row, backlog entry |

## Rules specific to this pipeline

1. **Generation is not authoring, and authoring is not validation.** The three are separate steps with separate evidence; collapsing them is how a library fills with plausible-looking prompts nobody has run.
2. **A generated prompt enters as `draft`, always.** Promotion to `operational` requires either `GEN-P02` evidence or a recorded structural review that says, in writing, that execution was not possible and why.
3. **Fixtures are frozen before the first run.** Moving the test after seeing the result inverts the experiment.
4. **Routing beats creation.** If the library already answers the question, the correct output is a configuration of the existing prompt plus a patch, not a second prompt that will drift from the first.
5. **Counts do not move for drafts.** The headline number in this repository is operational prompts; adding a draft is not coverage.
6. **One evaluation is a data point, not a validation.** It justifies promotion; it does not establish the prompt is the best available design.

## Failure routes

- **Intent stays vague after the interview** → stop. Record what is missing. A prompt built on a vague intent encodes the vagueness and will fail in ways nobody can attribute.
- **Evaluation is inconclusive** (variance dominates) → raise the runs-per-case setting, narrow the fixture to the disputed behaviour, or accept the prompt as `draft` with the uncertainty stated.
- **The prompt fails its own verification table** → return to `GEN-P01` with the defect classification; fix the instruction, not the prose.
- **The prompt requires capabilities the operator lacks** (no staging, no archive RPC, no store account) → rewrite the verification to what is possible and mark the rest as a manual prerequisite. Do not delete the check, and do not pretend it ran.
- **The library grows faster than it is evaluated** → this is the failure mode the whole pipeline exists to prevent. Stop adding, start evaluating.

## Handoff at the end of each cycle

Fill the standard handoff block (`HANDOFF-CONTRACT.md`): what was generated, the evaluation evidence, the decision, the files changed, and which coverage-matrix rows moved. A prompt integrated without that record cannot be distinguished later from one that was merely written.

## Completion criteria

- [ ] Intent fields (actor, task, artifact, constraint, evidence) written and confirmed.
- [ ] Existing coverage checked; the routing record names an existing ID or states "none found".
- [ ] Prompt generated with variables table, three test cases, and a `draft` provenance line.
- [ ] Three fixtures written before the first run, including an adversarial case.
- [ ] Each fixture run twice in a fresh session, traces captured.
- [ ] Design score and behavioural grade both recorded in `PROMPT_EVAL.md`.
- [ ] Ship / do-not-ship decision recorded with its evidence.
- [ ] If integrated: validator 0/0, catalog and gallery regenerated, system README counts updated.
- [ ] Coverage-matrix row and backlog entry updated.
- [ ] Handoff block filled with what changed and why.

## Completion

The workflow is complete when the prompt is either integrated with a recorded decision or rejected with a recorded reason, and the coverage matrix reflects the change. Nothing in between counts as done.
