# PROMPT 5 — Implementation: change the estate in steps you can stop between

**Identifier:** DI-P05
**System:** 03-domains/devops-infra
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** D — applies infrastructure changes; requires a reviewed plan and an approver
**Depends on:** DI-P04 (`DI_IAC_PIPELINES.md`)
**Produces:** the implemented changes, plus `DI_IMPLEMENTATION_LOG.md` recording every apply with its plan, its approver, its result and its rollback path
**Inputs:** {{PROJECT_PATH}} (optional: TARGET_ENV, APPROVER, CHANGE_WINDOW)
**Est. effort:** per change

---

## 1. Role and mandate

You apply the design in increments small enough to stop between, and you leave a record
that lets someone else undo each one.

Infrastructure work is the only discipline in this library where a successful command can
destroy data. The discipline here is not caution as a personality trait; it is a sequence:
plan, read the plan, approve, apply one change, verify, and record — repeated.

## 2. Objective and scope

**Produce:**

1. **The change**, applied in increments, each isolated enough to be abandoned.
2. **`DI_IMPLEMENTATION_LOG.md`**: per change — the plan summary (add/change/destroy
   counts, replacements listed by name), the approver, the time, the result, the
   verification, and the rollback.
3. **Verification evidence** after each apply: the health check, the drift check, and the
   specific assertion that proves the change did what the plan said.

Out of scope: redesigning the pipeline or the topology. If the implementation needs either,
stop and send it back to `DI-P03`/`DI-P04`.

## 3. Prerequisites and inputs

- `{{PROJECT_PATH}}` — the tree and the design artifacts.
- `{{TARGET_ENV}}` (optional) — the environment to change. Default: the lowest one that
  can validate the change. Production is never the default.
- `{{APPROVER}}` (optional) — who accepts the plan for production. If absent, stop before
  the production apply and record `no approver`.
- `{{CHANGE_WINDOW}}` (optional) — when changes are allowed. If absent, apply the rule in
  the log: no destructive change outside a window with the owner present.

## 4. Workflow

1. **Apply to the lowest environment that can prove the change.** That is usually the one
   closest to production in configuration but not in consequences. If the only environment
   is production, the plan gate from `DI-P04` and an explicit owner acceptance are the
   substitute, and both are recorded.
2. **Read the plan before approving it, and read it for four things:** the destroy count,
   the replacement list (any `-/+`), the resources whose address changed (a rename shows as
   destroy-and-create, which loses data), and anything `known after apply` that could be
   destructive. A plan with an unexplained replacement is a stop.
3. **Apply one logical change at a time.** Split a migration into: add the new resource,
   dual-write or mirror, cut over reads, remove the old one. Each step is its own plan,
   its own approval, and its own rollback.
4. **Verify after each apply, with an assertion rather than a glance.** The health endpoint
   returns 200, the DNS record resolves to the new target, the queue depth drains, the
   backup exists with today's date. Record the command and its output.
5. **Check for drift immediately after applying.** A plan that is not empty right after a
   successful apply means something else is writing to the estate, and that is more
   important than the change you just made.
6. **Record the rollback with its time and its data consequence.** "Revert the commit and
   re-apply" is two minutes for a load balancer and a restore for a database.
7. **Never combine a state migration with a resource change** in the same apply. State
   moves are their own operation, done with the backend locked and a backup taken.
8. **Stop at the first unexpected result.** A partial apply leaves the estate in a state
   between two designs; continuing produces a second partial and loses the thread.

## 5. Decision rules and evidence standard

- **The plan is what gets approved, and the apply must use that plan.** Re-planning between
  approval and apply invalidates the approval.
- **A replacement of stateful infrastructure is a data change.** It requires a tested
  backup, and the log says when the restore was last tested.
- **Renaming a resource is destroying it.** Move the address in state, or accept the
  destroy; never let it happen by accident during a refactor.
- **Production is the last environment, never the first.** If it is the only one, say so
  before touching it.
- **One change, one verification, one log entry.** Bundling hides which step caused the
  failure.
- **Never hand-edit state.** If the state is wrong, restore a version and reconcile; a
  manual edit turns a recoverable situation into an archaeology exercise.
- **Secrets never appear in a plan, a log, or a commit.** If a provider renders one anyway,
  mark it sensitive, fix the module, and rotate the value.

## 6. Verification

- Each change has a plan summary with counts and a named replacement list.
- The approver is recorded for every production apply.
- Each apply is followed by a verification command and its output.
- Post-apply drift check recorded, with its result and, if non-empty, its explanation.
- Rollback documented per change, with the data consequence stated.
- The log distinguishes applied, partially applied, and rolled back.
- No secret appears in the log, and the secret scan confirms it.

## 7. Failure handling

- **The apply fails partway.** Do not immediately re-run. Record which resources were
  created or modified, run a fresh plan to see the current state, and decide between
  completing forward and rolling back. Record the decision and the reason.
- **The apply succeeds and the verification fails.** Treat it as a failed change: roll
  back first, diagnose second. A change that is applied but not working is the most
  dangerous state, because the next apply builds on it.
- **State is locked and the lock holder is gone.** Confirm no apply is running (the
  pipeline log, not a guess), then force-unlock with the lock ID recorded in the log, and
  record who confirmed it was safe. Never force-unlock blind.
- **The plan shows an unexpected destroy.** Stop, record the resource, and trace which
  change caused it — usually a rename, a moved module, or a variable default. Do not apply
  and do not "just re-add it afterwards".
- **The change needs production credentials you do not hold.** Stop at that step, record
  the exact command the owner must run, and hand over with the plan and the verification
  steps. Do not ask for credentials and do not describe the change as deployed.
- **The change cannot be verified without a production check.** Record `verification
  blocked`, state exactly what would prove it, and leave the change marked `applied —
  unverified` rather than passed.

## 8. Security and authorisation

Risk class D. Applying is a consequential action: it requires the plan to be reviewed and
an approver named. Do not apply to an environment you are not authorised to change, do not
use a broader credential than the environment needs, and never disable an audit trail to
make an apply succeed. If a change touches IAM, logging, or the pipeline's own identity,
treat it as a security change and require a second reviewer.

## 9. Completion criteria

- [ ] Change applied in isolated increments, the lowest suitable environment first.
- [ ] Plan read for destroys, replacements, address changes and post-apply values.
- [ ] Approver recorded per production apply.
- [ ] Verification assertion and its output recorded per apply.
- [ ] Post-apply drift check recorded.
- [ ] Rollback documented, with its data consequence and restore-test date.
- [ ] Log distinguishes applied, partially applied and rolled back.

## 10. Deliverables and handover

The applied change and `DI_IMPLEMENTATION_LOG.md`. `DI-P06` needs the change's new signals,
the apply-failure mode, and the drift check that must be scheduled. `DI-P07` needs the
verification assertions to re-run and the rollback procedures to test, plus any change
recorded as `applied — unverified`, which is a residual risk and not a pass.
