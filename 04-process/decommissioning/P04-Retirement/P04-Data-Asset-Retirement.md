# PROMPT 04 — Data and Asset Retirement

**Identifier:** DEC-P04
**System:** 04-process/decommissioning
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** specialised
**Risk class:** D for data deletion; C for infrastructure
**Depends on:** DEC-P03 (quiescence observed, deletion authorised)
**Produces:** `.decommission/RETIREMENT_RECORD.md`
**Inputs:** TARGET_SERVICE, RETENTION_DAYS (optional: APPROVER)
**Est. effort:** 30–90 min

---

## 1. Role and mandate

You are the engineer retiring what remains: data, storage, infrastructure, credentials, DNS, monitoring, and references. Code is the easy part. Data deletion is irreversible, so it happens last, with an explicit decision, and never by default.

## 2. Objective and scope

**Produce:** a complete asset inventory, a retention decision per asset with an owner, deletion executed only for assets whose decisions are recorded, and a paper trail that survives the team.

Out of scope: deleting data that a legal hold, retention obligation, or another system's dependency covers.

## 3. Prerequisites and inputs

- `.decommission/SHUTDOWN_LOG.md` (quiescence evidence, asset inventory).
- Retention policy (`{{RETENTION_DAYS}}` for `{{TARGET_SERVICE}}`), legal holds, contractual data obligations, and the approver for irreversible deletion if shorter than policy (`{{APPROVER}}`).
- Access to infrastructure, storage, DNS, secrets, monitoring, and package registries.

## 4. Workflow

1. **Build the complete asset inventory** — the step most often skipped:

   | Asset class | Examples | Common miss |
   |-------------|----------|-------------|
   | Data stores | databases, schemas, buckets, volumes, search indexes | snapshots and replicas |
   | Backups | scheduled backups, archives, exports | archives held by a third party |
   | Infrastructure | compute, queues, topics, load balancers, DNS records | DNS and TLS certificates |
   | Identities | service accounts, API keys, OAuth clients, deploy keys | keys held in CI secrets |
   | Observability | dashboards, alerts, SLOs, log streams | alerts that silently stop firing |
   | Automation | CI pipelines, cron jobs, IaC modules, Terraform state | state files and remote backends |
   | References | docs, runbooks, catalog entries, code in other repos | example configs in onboarding guides |

2. **Decide per asset, in writing:** `delete now`, `archive (location + retention period)`, `transfer ownership`, or `retain with justification` (with owner and review date). No asset leaves this step with an implicit decision.
3. **Check legal and contractual obligations before any deletion.** Retention requirements, litigation holds, data-processing agreements, and audit requirements. Flag decisions that need legal input and stop on those assets.
4. **Verify data ownership.** Data in the retiring system may be the only copy of records another system legitimately needs. If so, transfer it or migrate the consumer first.
5. **Establish the deletion order**: derived assets first (indexes, caches, exports, replicas), then primary data, then infrastructure, then identities, then DNS, then monitoring. Deleting identities first can make remaining resources unmanageable.
6. **Take the archive before deleting**, and **verify the archive restores** (at least partially). An unverified archive is not a retention strategy — the same rule as `DB-P03`.
7. **Delete with evidence**: record the command or API call, the timestamp, and the operator. Prefer soft-delete/expiry where the platform supports it, so mistakes are recoverable for a defined period.
8. **Revoke identities and verify they are dead** by attempting to use one (read-only check, or observe rejection in the audit log). An API key that remains valid is a permanent liability.
9. **Retire observability and alerting deliberately.** Remove dashboards and SLOs, but confirm that the removal does not hide a shared dependency — and check that no alert was the only detector for another service.
10. **Clean the references**: documentation, runbooks, service catalogues, onboarding guides, architecture diagrams, and code in other repositories. Update `_meta/CATALOG`-equivalent inventories if the organisation keeps one.
11. **Write `.decommission/RETIREMENT_RECORD.md`:** asset inventory with decisions, retention basis, archive location and restore verification, deletion evidence with timestamps and operators, identity revocation verification, reference cleanup, residual assets with owners and review dates, and the date after which this record can itself be archived.
12. **Update the ledger and close the decommissioning.**

## 5. Decision rules and evidence standard

- **Deletion is a decision with a named decider**, not an engineering convenience.
- **Archive before delete, and verify the restore.** Treat archives as data you must be able to read in an emergency.
- **Data ownership is checked, not assumed.** The only copy of a needed record is not yours to delete.
- **Identities die last and are verified dead.** A valid credential for a deleted service is an unmonitored door.
- **Every residual asset has an owner and a date**, or it will outlive the team.
- **Documentation is part of the retirement.** A runbook that references a deleted service is an incident waiting for the next on-call engineer.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Inventory covers all asset classes | inspect | every class addressed |
| Every asset has a recorded decision | inspect | none implicit |
| Legal/retention obligations addressed | inspect | basis recorded or escalation |
| Archive verified by restore | test restore | data readable |
| Deletion evidence recorded | log | command + timestamp + operator |
| Identities revoked and dead | attempt use | rejected |
| Observability retirement reviewed | inspect | no shared detector removed |
| References cleaned | search | no stale references remain |

## 7. Failure handling

- **Legal hold discovered** → stop all deletion for affected assets; record the hold and the owner; resume only on written release.
- **Archive cannot be verified** → do not delete; either fix the archive or record an explicit decision to lose the data, signed by the owner.
- **Another system still depends on the data** → transfer ownership or migrate first; deletion waits.
- **An identity cannot be revoked** (external system, lost control) → record as a risk with an owner and compensating monitoring.
- **Shared infrastructure cannot be cleanly separated** → leave it, document the residual, and schedule the separation as its own change.
- **Deletion partially fails** → record exactly what remains; do not re-run blindly, since partial deletion changes the resource graph.

## 8. Security and authorisation

Risk class D for data deletion: every deletion requires a named approver recorded in the artifact. Do not delete audit logs that are subject to retention. Do not export personal data to unapproved storage when archiving. Revoke credentials rather than storing them "for reference".

## 9. Completion criteria

- [ ] Full asset inventory across all classes.
- [ ] Recorded decision per asset with owner.
- [ ] Legal/retention obligations checked and escalated where needed.
- [ ] Data ownership verified before deletion.
- [ ] Archive created and restore-verified.
- [ ] Deletions executed in dependency order with evidence.
- [ ] Identities revoked and verified dead.
- [ ] Observability and references retired.
- [ ] Residual assets listed with owners and review dates.
- [ ] Record written with a review/archive date.

## 10. Deliverables and handover

Artifacts: `.decommission/RETIREMENT_RECORD.md`, updated asset inventory.

Handover: residual assets → their owning teams with review dates; retention obligations → compliance owner; the record itself → the team's archive with a note of when it may be destroyed; lessons about undocumented consumers → `02-engineering/codebase-audit/` or the service catalogue.
