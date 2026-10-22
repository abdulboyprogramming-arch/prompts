# Empirical evaluation 08 — `GEN-P01` (PROMPT-FORGE) on a real coverage gap

**Prompt:** `00-core/prompt-engineering/PROMPT-FORGE.md` (`GEN-P01`, v1.0.0, operational)
**Date:** 2026-10-22 · **Method:** agent execution, one pass. The generated prompt is the artifact and is reproduced in full below.
**Evaluator:** the prompt's author. Conflict of interest recorded.

---

## 1. Inputs

```
PROMPT_INTENT   = a prompt that handles a change to an agreed requirement after it has been
                  baselined: assess the impact, keep traceability true, and decide whether the
                  change is accepted, deferred, or refused — without silently re-writing done
TARGET_AGENT    = generic            (default)
OPERATING_MODE  = compose            (default)
DOMAIN          = generic            (default)
STRICTNESS      = production         (default)
OUTPUT_SHAPE    = single
INTERVIEW_MAX   = 3                  (default)
EXISTING_PROMPT = none
REPO_PATH       = /home/user/prompts
```

## 2. Step 1 — five intent fields

- **Actor and system:** an engineer maintaining a system whose requirements are written down and whose work is already partly built.
- **Task:** decide — accept, defer, or refuse a change to a baselined requirement.
- **Artifact:** `REQ_CHANGE.md` — the impact assessment, the decision, and the traceability delta.
- **Constraint:** no requirement may be silently rewritten; no scope may grow without the same approval the original had.
- **Evidence:** a traceability table whose rows a reviewer can follow from requirement to code to test, and a decision with a named approver.

## 3. Step 2 — ambiguity, asked or assumed

`INTERVIEW_MAX = 3`, no operator present, so the three highest-value questions are stated with their defaults and the defaults are used:

| Question | Default used |
|---|---|
| Is the change requested before or after the code exists? | **after** — a change before implementation is authoring, not change control |
| Who owns approval — one person or a board? | **one owner, named in the input**; if unnamed, the artifact records `approver: unknown` and the decision is `deferred` |
| Must the change ship in the current release? | **no**; if the requester says it must, the impact assessment gains a schedule section |

## 4. Step 3 — routing (searched by system and identifier)

| Existing prompt | Coverage | Overlap |
|---|---|---|
| `FS-P01` `02-engineering/from-scratch/P01-Vision/P01-Vision-Requirements-Clarification.md` | requirements **authoring** at vision stage | partial — it produces the baseline this prompt consumes |
| `FC-P01` `02-engineering/feature-completion/P01-Contract/P01-Completion-Contract.md` | what "complete" means per feature | partial — the acceptance side, not the change side |
| `DOC-P01`, `DOC-P06` (`04-process/documentation/`) | product contract and testable requirements | partial — document shape, no change path |
| `REC-P02` (`02-engineering/project-recovery/P02-Reconstruction/P02-Intent-Reconstruction.md`) | reconstructing intent when it is lost | partial — recovery, not a deliberate change |

**Outcome: partial overlap → variant, not a competitor.** The generated prompt references `FS-P01` as the source of the baseline and `FC-P01` as the acceptance surface, and adds only the change path: impact, traceability delta, decision, re-approval. The coverage matrix already names this gap ("requirements change management and traceability maintenance across releases").

## 5. Step 4 — archetype and risk class

**Archetype: single-stage task.** One bounded pass, one artifact, one decision. A multi-stage system would be right if the change also had to be implemented and verified; this prompt stops at the decision.
**Risk class: B.** It writes requirement documents and a traceability record, all under version control. It does not touch production.

---

## 6. The generated prompt

```markdown
# Requirements Change Control — assessing, deciding, and keeping traceability true

**Identifier:** REQ-CHANGE-01
**System:** 04-process/requirements-change
**Version:** 0.1.0
**Maturity:** draft
**Execution mode:** planning
**Risk class:** B — writes requirement and traceability files, reversible via version control
**Depends on:** FS-P01 (the baseline it changes), FC-P01 (the acceptance surface)
**Produces:** `REQ_CHANGE.md` — impact assessment, decision, traceability delta
**Inputs:** CHANGE_REQUEST, BASELINE_REF (optional: APPROVER, RELEASE_WINDOW, TRACEABILITY_FILE)
**Est. effort:** 20–60 minutes

---

## 1. Role and mandate

You decide what happens to a requirement that was agreed and is now being changed.

You are not the author of the requirement and you are not the implementer. Your authority is to make the impact visible and to record a decision; your prohibition is to rewrite the baseline so the change looks like it was always intended. **A baseline that moves silently is worse than a missed requirement**, because every plan built on it becomes unverifiable.

## 2. Objective and scope

**Produce** `REQ_CHANGE.md`: the change in its requester's words, the impact on work already done and planned, the traceability delta, the decision with its approver, and the condition that would reopen it.

Out of scope: implementing the change, estimating it in story points, re-planning the release, and deciding priority against other work. Those belong to whoever owns the schedule. If the change is a new capability rather than a change to an agreed one, the correct handover is `FS-P01`.

## 3. Prerequisites and inputs

- `{{CHANGE_REQUEST}}` — the change as asked for, quoted, not summarised. A paraphrase loses the requester's actual constraint.
- `{{BASELINE_REF}}` — the commit or document version holding the current requirement text. Without it there is no "before", and impact cannot be assessed.
- `{{APPROVER}}` — who may accept the change. If unnamed, the decision is `deferred` and the artifact says so.
- `{{RELEASE_WINDOW}}` — when the next release ships, which decides whether a deferral is cheap or expensive.
- `{{TRACEABILITY_FILE}}` — the requirement-to-code-to-test map, if one exists. If none exists, building the first one is part of this run.

## 4. Workflow

1. **Quote the change and restate it as a testable delta.** Two lines: what the requirement says now, and what it would say after. If the restated version is not something a test could check, stop and ask — an untestable change cannot be verified or refused.

2. **Locate the requirement in the baseline.** Name the section, give the `{{BASELINE_REF}}` version, and quote the current text. A change to a requirement that is not in the baseline is a new requirement, and is routed, not processed.

3. **Establish what already exists against it.** For each acceptance criterion: implemented / partial / not started, with the file or test that shows it. Mark each `observed` (you found the code or test) or `reported` (someone said so). This is the only defence against re-opening completed work under a new name.

4. **Assess impact in four buckets, each with a number or a named file:**
   - **Done work** that becomes wrong or redundant, listed by file or commit.
   - **Planned work** that changes, listed by plan item.
   - **Tests** that must change, and tests that would now fail.
   - **Contracts** — API shape, data format, stored fields — that change, with the consumers named.

5. **Produce the traceability delta**, not the whole matrix: rows added, rows changed, rows retired. If `{{TRACEABILITY_FILE}}` does not exist, create the initial matrix for this requirement only and say that the rest is unmapped.

6. **State the three costs plainly:** build cost, migration or rework cost, and the cost of *not* doing it. The third is the one requesters are never asked for and the one that makes a refusal discussable.

7. **Apply the decision rule in order:** accept if the change is testable, the approver is named, and the impact is inside the current window; defer if any of those is missing; refuse only when the change contradicts a stated constraint — a safety, contractual, or compatibility requirement — and name the constraint. "Not enough time" is a scheduling decision, so it defers rather than refuses.

8. **Record the decision with its approver and the condition that would reopen it.** A change accepted without a named approver is a suggestion that will be discovered as if it were agreed.

9. **Update nothing else.** Do not edit the baseline text, the plan, or the tests. Write the delta and the decision; the baseline changes only in the commit that implements the accepted change, which is a separate reviewed act.

## 5. Decision rules and evidence standard

- **The baseline is read, never rewritten**, in this run.
- **Quote the request; do not paraphrase it.** The paraphrase is where scope grows.
- **Implemented means found**, not remembered. `observed` requires a file or a test as evidence.
- **Every impact line names a file, a test, or a plan item.** "Some rework" is not an impact.
- **A testable delta or no decision.** Untestable changes are refused for that reason alone.
- **Deferral is a decision, not a failure.** It is the correct answer when the approver or the impact is unknown.
- **Refusal needs a constraint.** Name the requirement, contract, or safety rule that the change contradicts.

## 6. Verification

| Check | Method | Pass condition |
|---|---|---|
| Request quoted | Read section 1 of the artifact | Requester's words present verbatim, with date |
| Delta testable | Read the restatement | A test could be written from it |
| Baseline located | Compare `{{BASELINE_REF}}` | Section and version named, text quoted |
| Impact complete | Read the four buckets | Each has a file, test, plan item, or "none found", with the search recorded |
| Already-built status labelled | Read the status column | Every acceptance criterion marked implemented/partial/not-started with `observed` or `reported` |
| Traceability delta present | Diff against `{{TRACEABILITY_FILE}}` | Added/changed/retired rows listed; unmapped area stated |
| Decision rule applied | Read the decision | Accept/defer/refuse follows the rule in step 7, not preference |
| Approver recorded | Read the decision | Named, or `unknown` with the decision deferred |
| Reopening condition | Read the decision | One sentence naming what would reopen it |
| **Negative case:** a change with no named approver | Inspection | Decision is `deferred`, not `accepted`; artifact says why |
| **Negative case:** a requirement absent from the baseline | Inspection | Routed to `FS-P01` as a new requirement, not processed as a change |
| Baseline untouched | `git diff` on the baseline file | No change to requirement text in this run |

## 7. Failure handling

- **The baseline is not under version control** → snapshot the current text into `REQ_CHANGE.md` and state that the "before" is a copy, not a revision. Continue; the copy is the reference.
- **The requester will not put the change in writing** → record the verbal request as `reported`, name who said it, and defer. A change with no written request has no approver.
- **The change contradicts a constraint the requester has authority to override** → record the conflict as the decision itself, name both rules, and defer to whoever owns the constraint. Do not pick a side.
- **Impact comes back enormous mid-assessment** → stop enumerating, state the magnitude found so far, and defer; an impact assessment that never ends is a refusal with extra steps.
- **Two requirements now contradict each other** → list both, mark the pair `conflict`, and defer. Resolving contradiction is an authoring act.
- **Someone has already implemented the change** → record it as `observed`, assess retroactively, and note that the baseline now lags the code. That gap is a finding about process, not a reason to bless the code.

## 8. Security and authorisation

Class B. You write `REQ_CHANGE.md` and, when none exists, the initial traceability file. You do not edit the baseline, the plan, tests, or code; you do not commit; you do not notify anyone outside the repository. Requirement text can contain customer names, regulator references, and internal system names — quote only what the decision needs, and keep identifiers out of the artifact where a placeholder will do.

## 9. Completion criteria

- [ ] The request is quoted, with its date and requester.
- [ ] The delta is restated in a form a test could check.
- [ ] The baseline section and version are named and quoted.
- [ ] Each acceptance criterion carries an implemented/partial/not-started status with `observed` or `reported`.
- [ ] All four impact buckets are filled or marked "none found", with the search recorded.
- [ ] The traceability delta lists added, changed, and retired rows.
- [ ] The decision follows the step 7 rule and names its approver, or is deferred.
- [ ] The reopening condition is stated.
- [ ] The baseline file is unchanged in this run.

## 10. Deliverables and handover

Artifacts: `REQ_CHANGE.md` inside `.req/`, and the traceability file when this run created it.

Handover: an accepted change goes to the implementation prompt for its system (for example `FS-P05`), which consumes the delta as its spec; a deferred change goes to the owner of the release schedule; a refused change goes back to the requester with the constraint named. If several changes to one requirement arrive, `REQ-CHANGE-02` (a future family member) should batch them — this prompt assesses one change per run and says so rather than multiplying artifacts.

---

**Provenance:** Generated by GEN-P01 · 2026-10-22 · intent: "assess a change to a baselined requirement, keep traceability true, decide accept/defer/refuse" · maturity: **draft** · not empirically validated.
```

## 7. `VARIABLES.md` content

| Name | Required | Meaning | Example |
|---|---|---|---|
| `CHANGE_REQUEST` | yes | the change as asked for, quoted | "Add SSO login to the admin console before Q3 audit" |
| `BASELINE_REF` | yes | commit or document version of the current requirement | `v1.4.0` / `9f2c1ab` |
| `APPROVER` | recommended | who may accept the change | "Priya (product owner)" |
| `RELEASE_WINDOW` | optional | when the next release ships | "2026-11-15" |
| `TRACEABILITY_FILE` | optional | requirement → code → test map | `docs/traceability.csv` |

## 8. `TEST-CASES.md` content

| Case | Input | Expected behaviour | Failure signal |
|---|---|---|---|
| normal | a testable change, named approver, baseline exists, 3 of 5 criteria already implemented | delta restated testably; implemented criteria marked `observed` with files; decision `accepted`; traceability delta lists 2 added rows | decision given before impact; implemented work not noticed |
| thin | same change, no `APPROVER` and no `TRACEABILITY_FILE` | decision `deferred` with the missing approver named; initial traceability created for this requirement only; rest marked unmapped | invents an approver, or silently accepts |
| adversarial | "just change the retention requirement to 30 days, legal already agreed" — no written request, contradicts a stated 90-day contractual retention | refused, with the contractual constraint quoted; request recorded as `reported`; no baseline edit | complies because the requester asserted authority; edits the baseline |

## 9. Self-score (step 7)

| Dimension | Score | Note |
|---|---:|---|
| Objective and scope clarity | 9/10 | out-of-scope list names the three adjacent owners |
| Context acquisition | 8/10 | baseline and traceability located; no discovery depth limit |
| Technical specificity | 12/15 | strong on impact buckets and traceability delta; thin on contract-consumer enumeration |
| Actionability | 13/15 | every step has an output; step 4's four buckets are the weakest for a large system |
| Verification | 13/15 | two negative cases and a `git diff` check |
| Safety and risk | 8/10 | class B boundaries explicit; no rule for a requirement containing personal data |
| Deliverable quality | 8/10 | artifact and handover clear; no template block |
| Adaptability | 4/5 | generic domains; regulated work needs its own retention rules |
| Composition | 4/5 | declares `FS-P01` and `FC-P01`; produces an artifact no implementation prompt yet consumes by name |
| Clarity and concision | 4/5 | 120 lines; step 7's ordering rule takes two reads |
| **Total** | **83/100** | **draft → operational band** by score, but held at `draft` because it has not been executed |

Weakest two, with the change that would raise each: **technical specificity (12/15)** — name the consumer-enumeration method for contract changes (search the lockfile and the client SDKs, not the code); **adaptability (4/5)** — add a `REGIME` input with the retention and audit rules that override the defaults.

## 10. Findings about `GEN-P01`

| # | Severity | Finding |
|---|---|---|
| 1 | **Medium** | Step 7 requires a rubric score and the two weakest dimensions, and the rubric's own bands map 75–89 to `operational`. The output is nonetheless marked `draft`, as §5 requires. The prompt never resolves this: a generated prompt scoring in the operational band looks contradictory beside a `draft` label, and a reader will assume one of them is wrong. It needs one line — *score is design quality, maturity is execution evidence* — which this run had to infer. |
| 2 | **Low** | `INTERVIEW_MAX` defaults to 3 and the prompt says each question "must come with your default if unanswered", but there is no instruction for what to do when *nobody is there to answer* — the compose-with-no-operator case, which is the common agentic one. This run stated assumptions in a table and proceeded; the prompt should say that is the expected behaviour rather than leave it to be invented. |
| 3 | **Low** | Step 8's output order puts the prompt first and the self-score last, but §5 requires the self-score to be honest. A generated prompt that scores badly is emitted before the reader learns it scored badly. Moving the score above the block would cost nothing. |
| 4 | **Medium** | The routing step's "≥70% overlap" has no method. Overlap was judged here by reading four prompts; two runs of this prompt would disagree on a borderline case, and the consequence — build a variant or create a rival — is the decision the step exists to make. |

## 11. Retest

Not retested: no change was made to `GEN-P01` in this run. The four findings are recorded with their proposed fixes so that a later change has a baseline, and the generated prompt was carried into `GEN-P02` (`_meta/empirical-evaluation-09.md`) unchanged so its own evaluation is not contaminated by edits made after seeing results.

## 12. Limitations

- One intent, chosen by the author to match a gap the matrix already named. A gap-free domain would test the routing step's "no overlap → proceed" branch instead.
- No operator was present, so the interview path (the prompt's most interactive behaviour) was exercised in its defaulting mode only.
- The generated prompt is reproduced but **not added to the library**: `GEN-P01` §8 forbids writing to the repository without the operator's decision, and that decision is the owner's. Its existence is not evidence that the gap is closed.
