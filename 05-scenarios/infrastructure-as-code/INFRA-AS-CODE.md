# PROMPT 01 — Infrastructure as Code: adopting it, or proving it matches reality

**Identifier:** IAC-01
**System:** 05-scenarios/infrastructure-as-code
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** audit-remediation
**Risk class:** C (reads cloud state; applying changes is D and requires a plan review and approver)
**Depends on:** none
**Produces:** `INFRA_STATE.md`, a drift register, an adoption plan
**Inputs:** CLOUD_SCOPE, TOOLING (optional: STATE_BACKEND, APPROVER, TARGET_ENV)
**Est. effort:** 3–8 h depending on estate size

---

## 1. Role and mandate

You establish the relationship between the infrastructure that is written down and the infrastructure that is running — then either close the gap or make it visible.

Two situations arrive here. **Adoption:** the estate was built by hand and someone now needs reproducibility, review, and recovery. **Drift:** the code exists, the deploy pipeline is authoritative in theory, but someone changed a security group in the console six weeks ago.

In both cases the dangerous state is the same: nobody can say what is actually running, and the code is a plausible fiction.

## 2. Objective and scope

**Produce:** an inventory of resources and their provenance (code, console, script, unknown), a drift report with a decision per item, a state-management plan, and an adoption sequence if the estate is unmanaged.

Out of scope: application deployment (`05-scenarios/deployment-target/`), cloud cost optimisation (`03-domains/cost-engineering/`), and IAM policy design (`02-engineering/security-hardening/`).

## 3. Prerequisites and inputs

- `{{CLOUD_SCOPE}}` — accounts, regions, and resource types in scope; start with one account.
- `{{TOOLING}}` — Terraform/OpenTofu, Pulumi, CloudFormation, CDK, or none yet.
- `{{STATE_BACKEND}}` — where state lives, whether it is locked, encrypted, and shared.
- `{{APPROVER}}` — required for any apply; `{{TARGET_ENV}}` — read-only audit is the default.

## 4. Workflow

1. **Establish the ground truth** from the provider's API, not from the console's default view: list resources by type and region, including the ones nobody remembers creating (old load balancers, unattached volumes, dormant databases, orphaned DNS records).

2. **Classify provenance** per resource: managed by code, created by hand, created by a script that is not in version control, or unknown. The unknown set is the risk.

3. **Run a plan against reality and read it as evidence.** For a codebase that claims to manage the estate, `plan` will propose deleting things that exist only in the console, recreating things that were renamed, or replacing resources because an immutable attribute changed. Every proposed destroy/replace is either drift to reconcile or a bug in the code.

4. **Decide per drifted resource**, and write the decision down:
   - **adopt** — import into state so the code manages it from now on;
   - **change the code** — the console change was correct and the code should match;
   - **revert** — the console change was unauthorised and should be undone;
   - **ignore with a reason** — genuinely ephemeral (autoscaled instances, generated secrets).

   Silent ignoring is how drift compounds.

5. **Fix the state backend first if it is weak**: remote, encrypted, locked, versioned, and access-controlled. A local state file on an engineer's laptop means the estate has one owner and no recovery.

6. **Handle secrets in state**: most tools persist values in plaintext. Either keep secrets out of state (references to a secret manager) or treat the state bucket as a secret store — encrypted, access-logged, and never copied into an artifact.

7. **Sequence an adoption** rather than importing the world: one resource group, then the module that will own it, then the pipeline that applies it. Import, plan, and confirm **no changes proposed** before moving to the next group. A big-bang import followed by an apply is how production is deleted.

8. **Prove the pipeline is the only path**: apply permissions are held by the CI role, humans have read-only or break-glass, and the console is restricted where the provider allows. A pipeline nobody is required to use is documentation.

9. **Add the guardrails that prevent recurrence**: `plan` on every pull request with the output posted for review, policy checks for the things that must never appear (public buckets, wildcard IAM, unencrypted volumes), and a scheduled drift detection that opens a ticket rather than a surprise.

10. **Write `INFRA_STATE.md`**: resource inventory with provenance, drift register with decisions, state-backend posture, adoption sequence, guardrails, and the remaining manual resources with owners.

## 5. Decision rules and evidence standard

- **The provider's API is the truth; the console view is a filtered opinion.**
- **Every `destroy` or `replace` in a plan is a decision**, never a formality.
- **Import before you re-create.** Re-creation of a database is data loss.
- **State is sensitive**: encrypted, locked, versioned, access-controlled.
- **A pipeline that is not the only path is not a control.**
- **Small, verified increments** beat a big-bang adoption.
- **Unmanaged resources are recorded with an owner**, even if the answer is "we accept this".

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Resource inventory | Provider API listing | All resources of each type listed with provenance |
| Unknowns quantified | Inventory | Count and owners stated |
| Plan reviewed | Tool output | Every destroy/replace explained |
| Drift decisions | Register | adopt / change code / revert / ignore-with-reason |
| State backend | Configuration | Remote, encrypted, locked, versioned |
| Secrets in state | Inspection | Referenced or the bucket treated as a secret |
| Import verified | Plan after import | No changes proposed |
| Pipeline authority | IAM review | CI role applies; humans read-only or break-glass |
| Policy checks | CI | Public bucket / wildcard IAM blocked |
| Drift detection | Scheduled job | Ticket opened on divergence |

## 7. Failure handling

- **The estate is enormous and undocumented** → scope to one account and one service; adopt the resources whose loss would be catastrophic first (databases, DNS, certificates).
- **`plan` proposes replacing a stateful resource** → stop; import or rename instead. A replacement of a database is a data-loss event, and the tool will not ask twice.
- **State is lost or corrupt** → restore from the versioned backend; if there is no versioned backend, reconstruct by importing into a fresh state, one resource group at a time, verifying no changes after each.
- **A console change was a legitimate emergency fix** → capture it in code immediately (the fix is not real until it survives the next apply), and add the break-glass process that makes the next emergency explicit.
- **Two teams manage overlapping scopes** → split state by boundary; shared state plus concurrent applies causes lock contention and lost changes.
- **The provider has no import support for a resource** → record it as manually managed with an owner and a documented configuration; do not pretend it is covered.

## 8. Security and authorisation

Risk class C: reads cloud state and writes infrastructure code. **Applying** is class D — require a saved plan, a named approver, a change window, and a rollback for anything stateful. Do not run `apply` against production from an engineer's laptop with personal credentials. State files and plan outputs can contain secrets; never attach them to a ticket.

## 9. Completion criteria

- [ ] Resource inventory from the provider API with provenance per resource.
- [ ] Unknown-provenance resources quantified and owned.
- [ ] `plan` run and every destroy/replace explained.
- [ ] Drift register complete with a decision per item.
- [ ] State backend remote, encrypted, locked, and versioned.
- [ ] Secrets either kept out of state or the state treated as a secret store.
- [ ] Imports verified with a no-change plan.
- [ ] CI holds apply rights; humans have read-only or break-glass.
- [ ] Policy checks in CI for the never-allowed resources.
- [ ] Scheduled drift detection opening tickets.
- [ ] Manually managed resources listed with owners.

## 10. Deliverables and handover

Artifacts: `INFRA_STATE.md`, drift register, imported modules, policy checks.

Handover: `05-scenarios/deployment-target/` consumes the platform resources this code defines; `02-engineering/secrets-rotation/` owns credentials used by the pipeline; `04-process/governance-compliance/` uses drift reports as evidence of change control; `04-process/decommissioning/` needs the inventory to retire anything safely.
