# Automate a Described Task: turn "we do this by hand" into something that runs

**Identifier:** AUTO-01
**System:** 05-scenarios/automation
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B for local scripts and CI configuration; **C** where the automation acts on production, third parties, or money
**Depends on:** none
**Produces:** the automation itself, `.automation/RUNBOOK.md`, idempotency and failure tests
**Inputs:** TASK_DESCRIPTION (optional: EXECUTION_ENV, APPROVER, TIME_BUDGET)
**Est. effort:** 1 h to 2 days depending on the task and the number of decision points
**Gallery:** Someone describes a manual procedure — "every Monday we export this, rename it, upload it, then email finance" — and you need a script that does it safely, verifiably, and repeatedly.

---

## 1. Role and mandate

You take a task that a human currently performs by following a description, and you make it executable.

The description is almost never a specification. It omits the exceptions the human handles without noticing ("unless it's the last Friday of the quarter"), the values they read from a screen, the retry they do without thinking, and the judgement they apply to a suspicious number. Your job is to surface those, decide which must be automatised and which must remain a human decision, and then build the smallest reliable thing that does the rest.

**A good automation fails loudly, idempotently, and in the same place every time.** A bad one silently does half the task, which is worse than the manual version, because nobody is watching.

## 2. Objective and scope

**Produce:** a working automation (script, CI job, scheduled task, or workflow) that performs the described task, with explicit preconditions, idempotency, verification of the *outcome*, failure notification, and a written record of what remains manual and why.

Out of scope: redesigning the business process, replacing the systems being automated, and automating a task whose description you cannot resolve into deterministic steps — in that case the deliverable is the list of questions that would make it determinable.

## 3. Prerequisites and inputs

- `{{TASK_DESCRIPTION}}` — the task as a human would explain it: trigger, steps, inputs, outputs, exceptions, who is notified. Written descriptions are usually incomplete; a screen recording or a walkthrough with the person who does it is worth more.
- `{{EXECUTION_ENV}}` — where it will run: a developer machine, a CI runner, a scheduler (`cron`, systemd timer, GitHub Actions, Cloud Scheduler), or a serverless function. This constrains credentials, timeouts, and how failures are reported.
- `{{APPROVER}}` — required before any automation with external side effects is enabled on real data.
- `{{TIME_BUDGET}}` — a hard cap often changes the design: an hour gets you a script with a dry-run; a day gets you tests and a scheduler.

## 4. Workflow

1. **Watch the task once, if at all possible, and write down what actually happens** — every read, every click, every file, every value copied between systems. Shadowing beats interviewing: people omit the steps they consider obvious, and those are exactly the steps that break the automation.

2. **Decompose the description into steps with explicit inputs and outputs.** For each step record: what it reads, what it writes, whether it is reversible, and how the human knows it worked. Any step whose "how I know it worked" is "it usually does" is the first risk to resolve.

3. **Classify each step** as one of:
   - **Deterministic** — pure data transformation; automate directly.
   - **Fragile** — depends on a UI, a file layout, an email format, or an undocumented API; automate with validation and a loud failure.
   - **Judgement** — requires a human to decide (approve the refund, mark the anomaly as fraud, choose the carrier). Automate the *surroundings*: gather inputs, present the decision, record the outcome. Do not encode policy as a guess.
   - **Not automatable yet** — blocked by access, licensing, or a system with no interface. List it as a prerequisite, not a limitation to work around with screen scraping that will break next month.

4. **Define the trigger and the guard rails before writing code.** Trigger: schedule (with timezone — see `02-engineering/time-correctness/`), event, or manual. Guard rails: dry-run mode, a maximum change count (refuse to act if the batch is 10× the usual size), a lock so two runs cannot overlap, a timeout, and a kill switch.

5. **Make every step idempotent.** Re-running must not duplicate the effect: use a natural key with an upsert, a processed-marker, or a content hash. Ask the killer question for each side effect — *what happens if this runs twice?* — and write the answer in the runbook. For anything that leaves the machine, this is where `05-scenarios/third-party-integration/` (idempotency keys, unknown outcomes) applies.

6. **Handle the three failure shapes explicitly:**
   - **Partial failure** — step 4 of 7 fails: what has already happened, and how does the next run resume or roll back? Write the resume logic; do not assume a clean restart.
   - **Unknown outcome** — the request timed out: did it apply? Verify state before retrying, or attach an idempotency key so retrying is safe.
   - **Silent no-op** — the job ran and changed nothing because the input was empty. Most real incidents are this. Assert on the expected shape of the input (non-zero rows, expected date range, expected file present) and alert when the shape is wrong.

7. **Verify the outcome, not the exit code.** After the run, check the thing the human checks: the file exists and has rows, the record is in the target system with the right values, the totals reconcile, the email arrived. Encode that check in the automation and make its failure the one that notifies a person.

8. **Decide how failures reach a human.** A scheduled job with no failure channel is not automation, it is a hope. Choose a destination (CI annotation, issue, chat webhook, email, pager), include the run ID and the step, and make sure one run per failure arrives rather than one per minute. Note who owns the response.

9. **Record the automation's contract in `.automation/RUNBOOK.md`:** what it does, when it runs, preconditions, required secrets and where they come from, dry-run instructions, how to resume after partial failure, how to disable it, what remains manual and why, and the person to contact. This document is what makes the automation maintainable by someone who did not write it.

10. **Prove it before switching it on:** run in dry-run; run twice and show the second run is a no-op; run with malformed input and show it fails loudly without side effects; run with the dependency unavailable and show the failure is reported. Record these four results. Only then enable the schedule.

## 5. Decision rules and evidence standard

- **Automate the deterministic, surface the judgement, name the blocked.** Do not silently encode a policy decision.
- **Idempotency is a requirement, not a refinement.** If re-running is dangerous, the two runs will eventually overlap.
- **A silent no-op is a failure.** Assert on input shape; alert on an empty or unexpected batch.
- **The exit code proves the process ran.** Verify the outcome the human would verify.
- **No failure channel, no schedule.** A job nobody hears from is not running.
- **Prefer the boring mechanism** — a scheduled script with a lock and a log beats an event-driven pipeline whose failure modes you cannot enumerate.
- **Ambiguity in the description is a question, not a design decision.** List it and ask; do not pick the interpretation that is easier to code.
- **Every secret comes from the environment's secret store**, never from a file in the repository.
- Mark behaviour you observed as `verified` and behaviour you assumed as `inferred`.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Description resolved | Step table | Every step has input, output, reversibility, success signal |
| Judgement steps identified | Step table | Human decisions named, not encoded |
| Dry-run exists | Command | Runs end-to-end with no external side effect |
| Idempotent | Run twice | Second run produces no duplicate effect |
| Partial failure | Injected failure mid-run | Resume or rollback path works as documented |
| Unknown outcome | Simulated timeout | State verified before retry; no double effect |
| Input-shape guard | Empty/malformed input | Loud failure, no side effect, alert sent |
| Outcome verified | Post-run check | The human's acceptance test encoded and passing |
| Failure reaches a human | Deliberate failure | Exactly one notification with run ID and step |
| Credentials | Configuration review | Secret store only; none in the repository |
| Runbook | `.automation/RUNBOOK.md` | A second person can run, pause, and resume it |

## 7. Failure handling

- **The description is incomplete or contradictory** → stop automating and produce the question list. An automation built on a guessed rule will encode the guess into production.
- **The task depends on a UI with no API** → automate only what has an interface; for the rest, produce a checklist and a reminder. Screen scraping is acceptable only with a monitor that detects the break and a named owner.
- **The task needs credentials you do not have** → build it against a stub, document the required permission precisely (scope, resource, duration), and hand that to `{{APPROVER}}`. Do not request broad credentials to save time.
- **The automation would touch money, customers, or production data** → require `{{APPROVER}}`, a change limit, a dry run against a copy, and an easy rollback. Prefer a mode that produces a proposal a human applies.
- **It works but takes longer than the manual task** → say so. Sometimes a 20-minute script that runs reliably at 3am is still worth it; sometimes the answer is to leave the task manual and improve the checklist.
- **Someone asks to automate a judgement call** → automate the data gathering and the recording, keep the decision human, and write the reason.

## 8. Security and authorisation

Risk class B for local scripts and CI; C for anything with external side effects. Least privilege: the automation gets the narrowest scope that performs its task, ideally a dedicated identity, never a personal long-lived token. Secrets are injected at runtime, masked in logs, and rotated when a contributor leaves (`02-engineering/secrets-rotation/`). Never log payloads containing personal data. An automation that can delete is an automation that will eventually delete; put a limit and a confirmation path in front of it.

## 9. Completion criteria

- [ ] The task is decomposed into steps with inputs, outputs, and success signals.
- [ ] Judgement steps are identified and left to a human.
- [ ] Blocked steps are named with their prerequisite.
- [ ] Dry-run mode exists and was used.
- [ ] Re-running is proven safe.
- [ ] Partial failure and unknown outcome are handled and tested.
- [ ] Input-shape assertion exists with an alert.
- [ ] Outcome verification is encoded, not just an exit code.
- [ ] Failures reach a named human with run context.
- [ ] Secrets come from the environment's store.
- [ ] Runbook written; disable and resume documented.
- [ ] Four proofs recorded: dry-run, double-run, malformed input, dependency unavailable.

## 10. Deliverables and handover

Artifacts: the automation (script, workflow definition, or job configuration), its tests, `.automation/RUNBOOK.md`, and the four recorded proofs.

Handover: `05-scenarios/background-jobs/` governs retries, overlaps, and scheduling semantics once this runs on a schedule; `05-scenarios/email-deliverability/` applies if the automation sends email; `05-scenarios/third-party-integration/` if it calls a vendor; `04-process/observability-reliability/` P03 owns the alert that fires when it stops. `02-engineering/time-correctness/` matters for any schedule that runs across a daylight-saving boundary. Anything that must be reversible at speed belongs in `02-engineering/release-engineering/` thinking, not in the script alone.
