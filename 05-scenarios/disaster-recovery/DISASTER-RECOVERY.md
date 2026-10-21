# PROMPT 01 — Disaster Recovery: prove the restore, not the backup

**Identifier:** DR-01
**System:** 05-scenarios/disaster-recovery
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** C for the plan and the drill in an isolated environment; **D** for any restore over production data
**Depends on:** none
**Produces:** `.dr/DR_PLAN.md`, `.dr/DRILL_LOG.md`, measured RTO/RPO
**Inputs:** SYSTEM_SCOPE, BACKUP_SOURCE (optional: RTO_TARGET, RPO_TARGET, DRILL_ENV, APPROVER)
**Est. effort:** 3–6 h for the plan and first drill

---

## 1. Role and mandate

You establish whether this system can be rebuilt after losing something it cannot lose — a database, a region, an account, or a cloud provider's trust in you.

The uncomfortable fact: **a backup that has never been restored is a hypothesis.** Backups fail silently in specific, recurring ways — the job ran but wrote nothing; the retention policy expired the only copy; the encryption key lived in the same account. Others survive the backup and fail the restore: nine hours against a four-hour target, or a restore the application cannot use because migrations, extensions, or sequences are missing.

You prove the restore, measure the time, and write down what breaks.

## 2. Objective and scope

**Produce:** a recovery plan per disaster class, a restore drill performed in an isolated environment, measured RTO and RPO against targets, and a gap register.

Out of scope: routine incident response (`05-scenarios/incident-response/`), single-record recovery (`05-scenarios/data-loss/`), and business continuity planning for staff and premises.

## 3. Prerequisites and inputs

- `{{SYSTEM_SCOPE}}` — what must survive: primary database, object storage, secrets, DNS, infrastructure definitions, queue state, and the code itself.
- `{{BACKUP_SOURCE}}` — where backups live, how often, how long they are retained, and whether they are encrypted with a key you would still have.
- `{{RTO_TARGET}}` — how long the business tolerates being down; `{{RPO_TARGET}}` — how much data loss is acceptable. Both are business decisions; if they do not exist, propose values and say they are provisional.
- `{{DRILL_ENV}}` — an isolated account/project for the drill, never production; `{{APPROVER}}`.

## 4. Workflow

1. **Enumerate the disaster classes** and treat each separately, because the recovery path differs:
   - data corruption or accidental deletion;
   - loss of a single service or instance;
   - loss of a region or zone;
   - loss of the cloud account (compromise, billing suspension, provider outage);
   - loss of the backup system itself;
   - ransomware or insider destruction of both data and backups.

2. **Inventory every asset that must be recoverable**, including the ones outside the database: object storage buckets, secrets and encryption keys, DNS zones, TLS certificates, infrastructure state, queue contents, cron definitions, and the CI configuration. A restored database with no secrets and no DNS is not a recovery.

3. **Check the backup chain for the six silent failures**: job succeeded but produced an empty file; retention deleted the copy you need; encryption key stored in the same account as the data. Then: backups in a single region matching the data's region; no verification that the backup is readable; and no record of which backup corresponds to which point in time.

4. **Write the restore procedure as exact commands**, not as principles. Who runs it, from where, with which credentials, in what order, and how you know each step succeeded. A procedure that says "restore from the latest backup" is a prompt for improvisation at 3am.

5. **Drill it in an isolated environment**, from the real backup, and time every phase: detect, decide, provision, restore, migrate, verify, and cut over. Record where the time actually went — it is almost never the restore step.

6. **Verify the restored system, not just the restore job.** Run the application against restored data: log in, read a record written yesterday, write a new one, check sequence values (a restored sequence starts behind and causes duplicate-key errors), confirm extensions and migrations, and validate row counts against the source of truth.

7. **Measure RPO honestly** by asking what the *newest* recoverable point in time is, not what the schedule claims. Then compare both numbers to `{{RTO_TARGET}}` and `{{RPO_TARGET}}` and state the gap in minutes.

8. **Plan for the account-loss case separately**, because it is the one nobody prepares for: backups in a second account or provider, an independent copy of the encryption keys, DNS held outside the primary account, and a documented way to bootstrap infrastructure from code when the original account is gone.

9. **Define the decision thresholds in advance**: who declares a disaster, at what evidence, and what is attempted before declaring it. Include the moment when restoring is slower than fixing forward, and who makes that call.

10. **Write `.dr/DR_PLAN.md`** (classes, assets, procedures, thresholds, roles, communication) and **`.dr/DRILL_LOG.md`** (dates, environment, phase timings, verification results, gaps, owners, next drill date).

## 5. Decision rules and evidence standard

- **A restore that has not been performed is not a backup.**
- **Measure RTO from the drill**, not from the schedule's promises.
- **The newest recoverable point defines RPO**, regardless of frequency.
- **Backups must not share fate with the data**: separate account, region, and key custody.
- **Verify the application against restored data**, not only the restore command's exit code.
- **Sequences, extensions, and migrations are part of the restore.**
- **Every drill produces a gap with an owner**, or it produced a reassuring story.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Disaster classes enumerated | Plan | Six classes, each with a route |
| Asset inventory | Plan | Data, storage, secrets, DNS, IaC, queues |
| Backup chain audited | Provider console | Six silent failures each checked |
| Backup readable | Test restore of a sample | Data returned, not an empty archive |
| Encryption key available independently | Access check | Key not co-located with the data |
| Restore procedure | Plan | Exact commands, roles, verification per step |
| Drill executed | Isolated environment | Completed end to end |
| RTO measured | Drill timings | Phase-by-phase, compared to target |
| RPO measured | Newest recoverable point | Stated in minutes, compared to target |
| Application verified | Functional test on restored data | Login, read, write, sequences valid |
| Account-loss path | Plan | Second account/provider, external DNS, key copy |
| Decision thresholds | Plan | Who declares, on what evidence |

## 7. Failure handling

- **There are no backups** → this is the finding; enable provider-native point-in-time recovery immediately as the minimum, and record the exposure window.
- **The restore exceeds the RTO** → measure where the time goes; usually provisioning, DNS propagation, or a manual step that should be automated. Report the gap rather than adjusting the target quietly.
- **The restore succeeds but the application fails** → the gap is in application-level recovery: migrations, sequences, secrets, or config. Add those steps to the procedure.
- **The backup is corrupt or unreadable** → rotate to a new backup chain now, and treat the interval as unprotected; check whether the corruption is systematic (same agent, same bucket).
- **The drill cannot run in isolation** (no spare account, no budget) → restore into a temporary namespace with production credentials revoked, or document that the drill is untested — an untested plan must be labelled as such wherever it is referenced.
- **A region loss would also take the backups** → replicate to a second region or provider; "the provider handles it" is not a recovery plan.
- **Restoring would overwrite data written since the backup** → that is a data-loss decision, not a technical one: capture the newer data first if possible, and have the business owner choose.

## 8. Security and authorisation

Risk class C for planning and isolated drills; **D** for any restore over production. Restoring into an isolated account with production data creates a second copy of personal data outside normal controls — use masked or synthetic data by default, and destroy the copy after verification with evidence. Backup credentials are among the most valuable in the estate: separate custody, MFA, and rotation (`02-engineering/secrets-rotation/`). Encryption keys must survive the loss of the account they protect.

## 9. Completion criteria

- [ ] Six disaster classes enumerated with a route each.
- [ ] Asset inventory covers data, storage, secrets, DNS, IaC, queues.
- [ ] Backup chain audited for the six silent failures.
- [ ] A sample backup proven readable and complete.
- [ ] Encryption keys recoverable independently of the data.
- [ ] Restore procedure with exact commands, roles, and per-step verification.
- [ ] Drill completed in an isolated environment.
- [ ] RTO and RPO measured and compared to targets.
- [ ] Application functionally verified against restored data, including sequences.
- [ ] Account-loss path documented.
- [ ] Decision thresholds and roles recorded.
- [ ] Gaps logged with owners and a next drill date.

## 10. Deliverables and handover

Artifacts: `.dr/DR_PLAN.md`, `.dr/DRILL_LOG.md`, measured RTO/RPO.

Handover: `05-scenarios/data-loss/` handles the single-record case; `05-scenarios/incident-response/` owns the live incident while DR owns the rebuild; `04-process/governance-compliance/` uses drill evidence for availability commitments; `_meta`-level `04-process/observability-reliability/` P04 keeps the runbook that points here; `04-process/handover/` P03 must transfer backup and key custody, because a handover that omits them transfers a system nobody can recover.
