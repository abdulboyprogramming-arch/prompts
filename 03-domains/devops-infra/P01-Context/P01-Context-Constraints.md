# PROMPT 1 — Context & Constraints: what breaks, for how many, and who can fix it at 3 a.m.

**Identifier:** DI-P01
**System:** 03-domains/devops-infra
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** A — reads the estate, its configuration and its history; changes nothing
**Depends on:** none (entry stage)
**Produces:** `DI_CONTEXT.md`: the systems and their owners, the environments and how they differ, the blast radius of each, the access model, and the constraints that bound every later stage
**Inputs:** {{PROJECT_PATH}} (optional: CLOUD_SCOPE, TEAM_OWNERSHIP, INCIDENT_HISTORY)
**Est. effort:** 45–90 min

---

## 1. Role and mandate

Before anyone writes a module or a pipeline, you establish **what exists, who owns it, and
what happens when it fails**. Infrastructure work has a property application work does not:
a mistake is applied to a shared estate, and the blast radius is measured in other teams'
outages.

Your output is the map every later stage navigates by. The promotion path in `DI-P03`,
the state layout in `DI-P04`, and the rollback in `DI-P05` all depend on knowing which
environments exist and what a change to each one can take down.

## 2. Objective and scope

**Produce:** `DI_CONTEXT.md` answering six questions:

1. **What is in the estate?** Compute, data stores, queues, networks, DNS, certificates,
   and the accounts or projects that hold them — from the provider configuration, not
   from a diagram that was accurate in March.
2. **Which environments exist, and how do they differ?** A "staging" that shares a
   database with production is not a staging environment, and the difference is a
   finding.
3. **What is the blast radius of each workspace or stack?** What else is destroyed when
   this one is misapplied — shared networking, a shared cluster, a shared identity.
4. **Who owns it, and who can change it?** The accountable team, the on-call rotation if
   one exists, and the identities with write access to the state and the control plane.
5. **How does change reach production today?** Manual console, a pipeline, a script on
   someone's laptop. Record the path and where it is unrecorded.
6. **What constraints bind the work?** Budget, compliance regime, data residency, uptime
   commitments, provider limits, and the tooling the team actually runs.

Out of scope: targets and budgets (`DI-P02`), topology (`DI-P03`), IaC layout (`DI-P04`).

## 3. Prerequisites and inputs

- `{{PROJECT_PATH}}` — the repository. **Discovered here:** the IaC tool and version, the
  state backend declaration, the provider and module pins, the pipeline definitions, and
  any scripts that call a cloud API.
- `{{CLOUD_SCOPE}}` (optional) — accounts, projects or subscriptions in scope. If absent,
  infer from provider credentials names in configuration and mark the list `inferred`.
- `{{TEAM_OWNERSHIP}}` (optional) — who is accountable. If absent, name the role and mark
  it `unconfirmed`.
- `{{INCIDENT_HISTORY}}` (optional) — the last five infra incidents. If absent, read the
  postmortem directory; if there is none, record `no recorded infra incidents`.

## 4. Workflow

1. **Read the estate from configuration.** Enumerate resources from the IaC tree and the
   provider configuration, not from memory. Note anything that exists in the cloud but has
   no code behind it — that is unmanaged inventory and it is the finding that matters most
   at this stage.
2. **Map environments and their true differences.** For each: account or project, region,
   size, data, and whether it shares any resource with production. A shared resource is
   written down with its name, because it constrains every later promotion decision.
3. **Compute blast radius per workspace.** List what lives in each state file and what
   else in the estate depends on it. Note the resources whose replacement would cause an
   outage rather than a blip: databases, load balancer front ends, DNS records, and the
   identity the pipeline itself uses.
4. **Record the access model.** Which identities can apply to each environment, whether
   that is a long-lived key or a federated role, where the state is stored and who can
   read it — state files contain secrets in plain text and are often more sensitive than
   the credentials.
5. **Trace how change reaches production.** Follow one recent change end to end from
   commit to apply. Record the approvals, the plan review, and anything done by hand
   outside the pipeline. Every manual step is a place where the code and the estate can
   diverge.
6. **Read the incident history** for infra-specific failure patterns: a bad apply, a
   drifted resource, an expired certificate, a quota, a deleted state file. These predict
   the next failure better than any design review.
7. **Capture constraints with sources:** uptime commitments from contracts, compliance
   scope from the data classification, budget from the last invoice, residency from the
   provider region policy. A constraint with no source is a preference.
8. **Mark every claim** `verified` (with path), `reported` (with who), or `unknown`.

## 5. Decision rules and evidence standard

- **Unmanaged resources are a finding, not a gap to fill silently.** Record them; whether
  they are imported or retired is a decision for `DI-P03`.
- **Shared resources define the blast radius.** One database shared by two environments
  means neither can be reset safely, and the promotion path must say so.
- **State is a secret.** Anything in a state file is readable by anyone with bucket
  access; record where it lives and who reads it.
- **An environment that differs from production in an untracked way is a test that proves
  nothing.** Record the delta; `DI-P03` decides whether to close or accept it.
- **Manual changes are not automatically wrong, but they must be visible.** A console fix
  during an incident is legitimate; one that nobody records becomes drift.
- **Ownerless infrastructure is a risk, not an orphan.** Name the role, mark it
  `unconfirmed`, and escalate rather than adopting it by default.

## 6. Verification

- Every environment listed with account, region and its differences from production.
- Shared resources named explicitly, with the environments that share them.
- Blast radius recorded per workspace, including replacement-vs-update consequences.
- Access model: who can apply where, key type (federated or long-lived), state location
  and its readers.
- The production change path traced end to end with its manual steps identified.
- Incident history listed by date and cause, or `no recorded infra incidents`.
- Every constraint carries its source; every unknown is marked.

## 7. Failure handling

- **No IaC exists** (console-built estate): record `unmanaged estate`, list what can be
  observed from the provider's read-only APIs if available, and hand the adoption decision
  to `IAC-01` rather than writing Terraform for an estate nobody has mapped.
- **The state file cannot be read** (no access, or not where the config says): record
  `state inaccessible`, name what is therefore unverifiable, and stop before `DI-P04` —
  a pipeline designed against an unknown state layout is a plan for a lock conflict.
- **Two tools manage the same resources** (a half-finished CloudFormation-to-Terraform
  migration): record both, which resources each owns, and which is authoritative. Do not
  let both apply.
- **Credentials are found in the repository** (a provider key in a `.tfvars` or a pipeline
  file): stop, record the file and variable name only, treat it as a security finding, and
  flag rotation as an urgent action for the owner. Do not print the value.
- **Production has no separate account** (everything in one project, separated by naming
  convention): record it as the single largest constraint in the document and hand the
  isolation question to `DI-P03`. Every later "test in staging first" instruction depends
  on this answer.

## 8. Security and authorisation

Risk class A: read-only. Do not run `apply`, `destroy`, or any mutating cloud call. Do not
copy credentials, state files, or secret values into the artifact — cite the location and
the key name. If the estate has no audit trail of who changed what, record that absence;
it is a compliance finding, not an inconvenience.

## 9. Completion criteria

- [ ] Estate inventory from configuration, with unmanaged resources flagged.
- [ ] Environments with account, region, and stated differences from production.
- [ ] Shared resources named, with the environments affected.
- [ ] Blast radius per workspace, including replacement consequences.
- [ ] Access model with key types, state location and state readers.
- [ ] Production change path traced, with manual steps listed.
- [ ] Incident history, or its explicit absence.
- [ ] Constraints with sources; unknowns marked.

## 10. Deliverables and handover

`DI_CONTEXT.md` at the repository root of the infrastructure code. `DI-P02` needs the
uptime commitments and the incidents to set targets that mean something. `DI-P03` needs
the environment deltas, the shared resources and the blast radius. `DI-P04` needs the
state layout, the access model and the tool pins. Anything `unknown` travels with the
handover instead of being resolved by assumption downstream.
