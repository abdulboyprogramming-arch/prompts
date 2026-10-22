# PROMPT 3 — Architecture: the promotion path, and what a bad apply can destroy

**Identifier:** DI-P03
**System:** 03-domains/devops-infra
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** A — reads the estate and writes a design; changes nothing
**Depends on:** DI-P02 (`DI_REQUIREMENTS.md`)
**Produces:** `DI_ARCHITECTURE.md`: environment topology and isolation, the promotion path, the deployment strategy per service, blast radius per change, and the decisions with their rejected alternatives
**Inputs:** {{PROJECT_PATH}} (optional: REGIONS, TENANCY_MODEL, EXISTING_ADR)
**Est. effort:** 2–3 h

---

## 1. Role and mandate

You decide how environments are separated, how a change travels from a laptop to
production, and how much of the estate one mistake can destroy.

Infrastructure architecture is judged by its worst day. A design that is elegant on the
whiteboard and lets a single `apply` delete the shared database is not an architecture;
it is a single point of failure with documentation.

## 2. Objective and scope

**Produce:** `DI_ARCHITECTURE.md` containing:

1. **Environment topology.** Each environment with its account or project, region, data
   residency, and — critically — what it does not share with production.
2. **Isolation boundaries.** The account, network, and identity boundaries, and what each
   one prevents. Name the boundaries that do not exist.
3. **Promotion path.** Artifact flow from build to production: what is promoted, where it
   is signed or hashed, which environment validates it, and what has to be true before the
   next step runs.
4. **Deployment strategy per service**, with the reason: rolling, blue/green, canary, or
   recreate. Each with its failure behaviour and its rollback time.
5. **Blast radius table.** Per change type — network, database, cluster, IAM — what fails
   with it, and whether the failure is reversible.
6. **Shared-state register.** Every resource used by more than one environment or team,
   with its owner and the change procedure that protects it.
7. **Decisions** with context, choice, rejected alternatives, and reversal condition.
8. **Known isolation debts**, with the sequence that would remove them.

Out of scope: module layout and pipeline jobs (`DI-P04`), implementing anything (`DI-P05`).

## 3. Prerequisites and inputs

- `{{PROJECT_PATH}}` — the infrastructure tree and `DI_CONTEXT.md`, which already
  established what exists and what is shared.
- `{{REGIONS}}` (optional) — approved regions. If absent, read the provider config and
  cite it; a change of region is a compliance question before it is a technical one.
- `{{TENANCY_MODEL}}` (optional) — single-tenant or multi-tenant, and how tenants are
  isolated. If absent and the estate is multi-tenant, mark it `unverified` and say so.
- `{{EXISTING_ADR}}` (optional) — prior decisions, so you do not reverse one unknowingly.

## 4. Workflow

1. **Build the environment table with the "what is not shared" column filled first.** The
   usual finding is that staging shares a database, a VPC, or an identity with production;
   writing each of those down turns a promotion plan into an honest one.
2. **Name the isolation boundaries that exist and the ones that do not.** Account-level
   separation prevents an IAM mistake from reaching production; a naming convention does
   not. Record the difference explicitly.
3. **Design the promotion path as a chain of evidence.** The same artifact — by digest,
   not by branch name — is validated in the lower environment and promoted unchanged.
   Rebuilding between environments means what you tested is not what you shipped.
4. **Choose the deployment strategy from the failure mode.** Rolling is fine when instances
   are interchangeable and the change is backward compatible; blue/green when rollback must
   be instant and cost allows double capacity; canary when the risk is behavioural and you
   have the telemetry to see it. Write the decision and its rollback time in minutes.
5. **Fill the blast-radius table before designing modules.** For each change type, list what
   fails with it and whether that failure is reversible. Irreversible entries — a database
   replacement, a deleted state file, a certificate that expires during the apply — get a
   protection named in `DI-P04`.
6. **Check the design against the reliability targets from `DI-P02`.** A single-zone
   database cannot meet a target that requires survival of a zone failure; write the
   arithmetic rather than the hope.
7. **Record every shared resource** with its owner and the procedure that protects it: how
   a change is proposed, who reviews, and how it is rolled back.
8. **Write the decisions with rejected alternatives.** "Managed service over self-hosted"
   is a decision only when the alternative and its cost are recorded.

## 5. Decision rules and evidence standard

- **Production isolation is an account boundary or it is a convention.** State which one
  this estate has; every later safety claim depends on it.
- **Promote artifacts, not source.** Rebuilding per environment reintroduces an untested
  variable — the build itself.
- **Rollback must be a number.** "Fast" is not a rollback. State the time to the previous
  version, and the time to restore data if the change touched it.
- **Irreversible changes get a gate, not a warning.** A resource that cannot be recreated
  needs an approval step and a backup, both named.
- **Shared resources are a design smell with a cost, not a moral failing.** If sharing is
  necessary, the blast radius and the protection are written down.
- **Least privilege is a topology property.** The pipeline's identity is scoped per
  environment, so a compromised staging credential cannot reach production.
- **Fewer moving parts wins ties,** as long as the reliability target is met. Multi-region
  for a system with a 99.5 % target is money that would have been better spent on a backup
  restore test.

## 6. Verification

- Environment table with account, region, and explicit non-shared properties.
- Isolation boundaries named, and the absent ones recorded as debts.
- Promotion path promotes a digest-identified artifact, with the evidence at each step.
- Deployment strategy per service, with failure behaviour and rollback time.
- Blast-radius table complete, with reversibility marked per change type.
- Shared-state register with owner and protection procedure per resource.
- Reliability targets checked against the topology, with the arithmetic shown.
- Decisions carry rejected alternatives and reversal conditions.

## 7. Failure handling

- **Everything runs in one account.** Record it as the dominant risk, propose the
  smallest useful split (production in its own account), and sequence it as its own change
  rather than bundling a migration into feature work.
- **The promotion path currently rebuilds per environment.** Record the difference between
  what was tested and what ships, and specify artifact promotion as the fix with the
  pipeline change it requires in `DI-P04`.
- **No lower environment exists.** Record `no pre-production environment`; every safety
  step that assumed one is marked `unavailable`, and the design must state what replaces it
  — a plan-only gate, a canary with automatic abort, or explicit owner acceptance of direct
  production applies.
- **A resource cannot be recreated** (a database with no tested restore, a certificate
  with an external registration): record it in the blast-radius table as irreversible, and
  make its backup and restore test a prerequisite in `DI-P04`/`DI-P07`.
- **Tenancy isolation is unclear** (shared buckets, tenant ID in a path): record the
  ambiguity and route it to the security owner. Do not design around an isolation model
  nobody has confirmed.

## 8. Security and authorisation

Risk class A. Record the trust boundaries: which identity applies to which environment,
where network ingress enters, and where secrets are stored and read. A design that has the
pipeline holding an administrator credential for every environment fails this stage
regardless of how good the rest is. Never paste a credential into the document; name the
role and the scope policy.

## 9. Completion criteria

- [ ] Environment table with account, region and non-shared properties.
- [ ] Isolation boundaries, present and absent, recorded.
- [ ] Promotion path with digest-identified artifacts and evidence per step.
- [ ] Deployment strategy, failure behaviour and rollback time per service.
- [ ] Blast-radius table with reversibility per change type.
- [ ] Shared-state register with owner and protection.
- [ ] Reliability targets validated against the topology.
- [ ] Decision records with rejected alternatives.

## 10. Deliverables and handover

`DI_ARCHITECTURE.md`. `DI-P04` takes the environment map to lay out state, the promotion
path to lay out pipeline stages, the blast-radius table to place approval gates, and the
irreversible list to require backups. `DI-P05` takes the strategy and rollback time.
`DI-P07` takes the blast-radius and irreversible entries as the tests that matter most.
