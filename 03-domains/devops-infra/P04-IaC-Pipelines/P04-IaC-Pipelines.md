# PROMPT 4 — IaC & Pipelines: state layout, plan review, and the gate that stops a destroy

**Identifier:** DI-P04
**System:** 03-domains/devops-infra
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** C — writes IaC and pipeline definitions; applying them is D and gated
**Depends on:** DI-P03 (`DI_ARCHITECTURE.md`)
**Produces:** `DI_IAC_PIPELINES.md`: module and state layout with locking, the pipeline stages and their gates, secret handling, and the rollback procedure per change type
**Inputs:** {{PROJECT_PATH}} (optional: STATE_BACKEND, PROVIDER_VERSIONS, APPROVER)
**Est. effort:** 2–4 h

---

## 1. Role and mandate

You design the two artifacts that decide whether infrastructure changes are safe: **where
state lives and how it is locked**, and **what a change must show before it is allowed to
apply**.

Almost every infrastructure catastrophe has one of two shapes: two applies running against
one state file, or an apply whose plan nobody read. Your design prevents both, and it
prevents them structurally, in the pipeline, rather than in a review checklist.

## 2. Objective and scope

**Produce:** `DI_IAC_PIPELINES.md` containing:

1. **Repository and module layout.** Directory per environment and per stack, shared
   modules with their inputs and outputs, and the rule for what may depend on what.
2. **State design.** One state per environment and stack, the remote backend, locking,
   encryption, versioning, and the recovery procedure when the state is lost or corrupted.
3. **Pipeline stages** with the command, the gate, and the failure behaviour: format, lint,
   validate, plan on pull request, policy check, apply on merge, verification.
4. **Approval gates.** What a human must approve, with what evidence in front of them:
   the plan summary, the destroy count, the replacement list, and the cost delta.
5. **Secret handling.** How the pipeline authenticates to the provider (federated
   short-lived credentials preferred), where secrets live, and the rule that no secret
   appears in plan output or logs.
6. **Rollback per change type**: revert-and-reapply, forward fix, restore from backup —
   and the cases where none is possible, which are the ones that needed a gate earlier.
7. **Drift detection** on a schedule, and what happens to the pipeline when drift is found.

Out of scope: choosing the topology (`DI-P03`), the actual apply (`DI-P05`), monitoring
(`DI-P06`).

## 3. Prerequisites and inputs

- `{{PROJECT_PATH}}` — the IaC tree and `DI_ARCHITECTURE.md`.
- `{{STATE_BACKEND}}` (optional) — where state is stored today. If absent, read the
  backend block; if there is none, `local state` is the finding and it is a blocking one.
- `{{PROVIDER_VERSIONS}}` (optional) — the pins. If absent, read the lock file; unpinned
  providers mean the plan you reviewed is not the plan that runs tomorrow.
- `{{APPROVER}}` (optional) — who approves production applies. If absent, name the role
  and mark it `unconfirmed`.

## 4. Workflow

1. **Fix the state layout first.** One state per environment and per stack, never one state
   for everything and never one state per resource. Record the backend, the lock mechanism,
   encryption at rest, and object versioning — versioning is what turns a corrupted state
   into an inconvenience instead of a rebuild.
2. **Write the state recovery procedure** before anything else in this document: who can
   restore a previous version, how the lock is released after a crash, and how to confirm
   the restored state matches reality before the next plan. A team that has never restored
   state will restore it during an incident, for the first time, under pressure.
3. **Write the plan gate.** On every pull request: `fmt -check`, `validate`, a plan against
   the target environment, a policy check, and the plan posted where the reviewer can read
   it. The gate fails on: any destroy of a resource marked irreversible in
   `DI_ARCHITECTURE.md`, any replacement of a stateful resource, a plan exceeding the
   change-size threshold, and any drift from `plan -refresh`.
4. **Make the apply a separate, gated job** on the default branch, pinned to the exact plan
   artifact, with the approval recorded. A pipeline that re-plans and applies in one step
   has removed the thing the reviewer approved.
5. **Choose the authentication mechanism and write down its scope.** Federated short-lived
   credentials per environment; if a long-lived key is unavoidable, name its rotation period
   and the reason. The production credential must not be available to pull-request jobs.
6. **Design the secret path.** Secrets are created outside IaC — by a secret manager or a
   rotation job — referenced by
   identifier, marked `sensitive`, and never rendered into plan output. Add the scan that
   proves no secret reached a log.
7. **Write rollback per change type**, and mark the irreversible ones. For data migrations
   the rollback is a restore, with a tested backup; for a replaced instance it is the
   previous image; for a deleted resource it is a rebuild from code plus data, and the data
   part is the question that had to be answered earlier.
8. **Schedule drift detection** and define the response: report to the owner, open a ticket,
   do not auto-apply. Automatic reconciliation hides the console change that caused it.

## 5. Decision rules and evidence standard

- **No local state, ever, for anything shared.** A laptop state file means the estate can
  be edited by whoever holds the file.
- **The plan is the artifact under review.** Approval attaches to a plan, not to a commit;
  re-planning before apply invalidates the approval.
- **Destroy and replace are different risks and both must be visible.** A `-/+` on a
  database is an outage with a data question attached.
- **Every gate is a command with an exit code.** "We check the plan" is not a gate.
- **The pipeline that applies production does not run on pull requests.** Separate job,
  separate identity, separate approval.
- **Drift is reported, not auto-fixed.** Automatic apply hides the change and the person
  who made it.
- **Pinned versions are part of the safety story.** An unpinned provider turns a reviewed
  plan into a different plan next week.

## 6. Verification

- State per environment and stack, with backend, locking, encryption and versioning.
- State recovery procedure written, with the lock-release and reconciliation steps.
- Pipeline stages listed with commands and exit conditions.
- Plan gate fails on irreversible destroys, stateful replacements, size threshold and drift.
- Apply job is separate, gated, and pinned to the reviewed plan artifact.
- Provider authentication is federated and scoped per environment, or its exception recorded.
- Secret handling declared, with the scan that proves no secret in logs.
- Rollback procedure per change type, irreversible cases marked.
- Drift detection scheduled, with a response that is not auto-apply.

## 7. Failure handling

- **State is local or in a bucket without locking.** Stop. This is the blocking finding:
  two engineers applying concurrently will corrupt the state, and the corruption is not
  detectable until the next plan. Specify the migration to a locked backend as the first
  change, before any other infrastructure work.
- **No plan can be produced without production credentials.** Record `plan requires
  production credentials`; the design must then either provision a read-only plan identity
  or accept that review happens after the fact, in writing. Do not describe an unreviewed
  apply as gated.
- **The team applies from laptops.** Record it, name the drift and audit consequences, and
  specify the pipeline as the path with the laptop path deliberately removed rather than
  discouraged.
- **A resource has no rollback** (a deleted bucket with no versioning, an unrecoverable
  database): record it as irreversible, add the backup as a prerequisite with a tested
  restore, and gate the change behind a second approver.
- **Secrets currently live in the repository or in plaintext variables.** Stop, record the
  locations by name only, and make rotation plus migration to a secret store the first
  work item — before any pipeline change that would copy them somewhere new.
- **The org cannot use federated credentials** (an older provider or an on-prem control
  plane): record the exception, the rotation interval, the scope limit, and the compensating
  control. A long-lived credential scoped to one environment is a defensible compromise
  when it is written down and rotated.

## 8. Security and authorisation

Risk class C for authoring, D for applying. Never run `apply` or `destroy` from this
stage. Never place a credential in a `.tfvars`, a pipeline file, or a plan artifact. State
files and plan files contain secrets in plain text — restrict read access to them and say so
in the document. The pipeline's production identity must be assumable only from the default
branch job, and that restriction is a technical control, not a convention.

## 9. Completion criteria

- [ ] Layout with environment and stack separation, and the module dependency rule.
- [ ] State design with backend, locking, encryption, versioning.
- [ ] State recovery procedure, including lock release and reconciliation.
- [ ] Pipeline stages with commands and failure behaviour.
- [ ] Plan gate with its four failure conditions, published where the reviewer reads it.
- [ ] Apply job separate, gated, pinned to the reviewed plan.
- [ ] Provider auth federated and scoped, or the exception documented with rotation.
- [ ] Secret path and the scan that proves no secret in logs.
- [ ] Rollback per change type; irreversible cases marked and gated.
- [ ] Drift detection scheduled with a non-auto-apply response.

## 10. Deliverables and handover

`DI_IAC_PIPELINES.md` plus the pipeline definitions and state configuration.
`DI-P05` implements against this design and may not apply outside it. `DI-P06` needs the
drift signal and the apply-failure signal to instrument. `DI-P07` needs the gates as tests —
each gate becomes a check with a deliberately failing fixture, and the state recovery
procedure becomes a restore drill whose result is recorded rather than assumed.
