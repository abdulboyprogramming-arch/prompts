# PROMPT 01 — Secret Rotation: drill it before you need it

**Identifier:** SEC-ROT-01
**System:** 02-engineering/secrets-rotation
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** C for the inventory and the drill plan; **D** for rotating a production credential (approver + window + rollback required)
**Depends on:** none
**Produces:** `SECRETS_INVENTORY.md`, a rotation runbook per class, a drill record
**Inputs:** REPO_PATH, TARGET_ENV (optional: SECRET_CLASSES, APPROVER, WINDOW, ONCALL)
**Est. effort:** inventory 2–4 h; first drill 1–2 h per class

---

## 1. Role and mandate

You make credential rotation a routine, verified operation instead of an emergency improvisation.

The failure is not "we never rotated". It is "we tried to rotate during an incident and discovered": nobody knows which services use the key, the old key still works because a worker caches it, rotation requires a dashboard only one person can access, and the deploy that would pick up the new value takes 40 minutes.

Rotation is a **capability**, and capabilities are demonstrated by drills.

## 2. Objective and scope

**Produce:** an inventory of every secret with its owner, consumers, blast radius, and rotation mechanism; a per-class runbook; a drill performed on a non-production credential; and a record of what broke.

Out of scope: secrets management vendor selection, and rotating production credentials without an approver and a window.

## 3. Prerequisites and inputs

- `{{REPO_PATH}}` — configuration, deployment manifests, CI workflows, and code that reads secrets.
- `{{TARGET_ENV}}` — the environment for the drill (staging or a dedicated test project, never production).
- `{{SECRET_CLASSES}}` — which classes exist: database passwords, API keys (inbound and outbound), signing keys, TLS certificates, OAuth client secrets, webhook signing secrets, encryption keys, service-account tokens, SSH keys.
- `{{APPROVER}}`, `{{WINDOW}}`, `{{ONCALL}}` — required before any production rotation.

## 4. Workflow

1. **Inventory by consumer, not by store.** For each secret: what reads it (service, job, third party), how it is delivered (env var, file, vault, CI secret), who owns it, what it grants, and what breaks if it is wrong. A secret with no named consumer is either unused or undocumented — both are findings.

2. **Classify by blast radius and rotation cost**:
   - **T0 — compromised key**: revoke first, rotate second, investigate third; never reuse it to authorise the rotation.
   - **T1 — signing/encryption keys**: rotation has a compatibility tail (old signatures must still verify); plan a key set with overlap, not a swap.
   - **T2 — outbound API credentials**: provider-specific; some issue a new key alongside the old, some revoke on creation.
   - **T3 — infrastructure credentials** (DB, cache, message broker): often embedded in connection pools and cached by drivers.

3. **Find the consumers people forget**: background workers and cron jobs on a separate deploy path, read replicas, analytics exporters, backups, local developer `.env` files, notebooks, mobile/desktop builds with embedded keys, third-party integrations that were given the key by email, and the previous employee's laptop.

4. **Write the runbook per class**, with exact commands and owner: create new → deploy consumers with both accepted (overlap) → verify the new one is in use → revoke the old → verify the old is rejected → record. Every step names who does it and how you know it worked.

5. **Design for the overlap**, because that is where rotations fail. Either the consumer accepts two credentials during migration, or the rotation is a hard cutover with a maintenance window. Say which, per class, and why.

6. **Automate the boring parts**: short-lived credentials via OIDC instead of static keys (the strongest rotation is the one that happens every hour without a human), secret injection at run time instead of baked into images, and a scheduled rotation for the classes that cannot be short-lived.

7. **Drill on a non-production credential and break it deliberately**: rotate, then verify the old credential is genuinely rejected (not just that the new one works). Check every consumer, including the job that runs at 03:00 — if it cannot be tested now, its first test will be in production.

8. **Time the drill.** Rotation that takes four hours is a rotation that will not happen during an incident; record the duration and the bottleneck.

9. **Handle the emergency case separately**: a suspected leak has its own order (revoke → rotate → audit usage → notify), and it must not require the same approvals as a scheduled rotation, or it will not happen fast enough.

10. **Write `SECRETS_INVENTORY.md`** with class, owner, consumers, mechanism, last rotated, next due, and drill result; and a runbook per class.

## 5. Decision rules and evidence standard

- **A rotation is proven by rejection of the old credential**, not by acceptance of the new one.
- **Revoke first in a suspected compromise**; investigation second.
- **Overlap or outage** — choose deliberately, never accidentally.
- **Short-lived beats rotated**: prefer OIDC/workload identity to a password rotated quarterly.
- **The inventory's consumer list is the product**, not the secret names.
- **Untested consumers are untested controls**; the 03:00 cron is the test.
- **Time the drill** — a slow rotation is an unavailable capability.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Consumers identified | Code + config search | Each secret has a named consumer list |
| Owners assigned | Inventory | Every secret has a person, not a team alias |
| Blast radius recorded | Inventory | Class and impact per secret |
| Runbook per class | Document | Exact commands, owners, verification |
| Overlap strategy | Runbook | Stated per class |
| Drill executed | Non-prod record | Completed end to end |
| Old credential rejected | Direct test | Authentication fails after revocation |
| All consumers exercised | Drill log | Including scheduled jobs |
| Duration measured | Drill record | Minutes, with bottleneck named |
| Emergency path | Runbook | Shorter approval path defined |
| Automation where possible | Config | OIDC/short-lived used where supported |

## 7. Failure handling

- **A consumer cannot be identified** → search all repositories, CI variables, and running environments; if still unknown, treat it as unused and *disable in staging first* before revoking in production.
- **Rotation requires a vendor dashboard only one person can access** → this is the finding; add a second administrator and document the procedure before the drill.
- **A cached credential keeps working after rotation** → verify by forcing a connection reset; document the cache TTL as part of the runbook, because a revoked key that still authenticates is not revoked.
- **The 03:00 job cannot be tested** → run it on demand in staging; if the job has no manual trigger, add one — an untestable recovery path is a defect.
- **A key is found in git history** → it is compromised regardless of deletion (`04-process/git-operations/` P03): rotate, then purge, then verify no clone still has it.
- **Rotation causes an outage** → roll back by re-enabling the old credential if it is still valid; if it was revoked, you are in an incident — the overlap strategy failed, record that.
- **Nobody can rotate because everyone is unavailable** → the capability depends on one person; fix that before the next drill.

## 8. Security and authorisation

Risk class C, with production rotation at **D**. Never print, log, or record a secret value — the inventory holds identifiers, stores, and consumers only. Drills run in a non-production environment with an equivalent configuration. During a suspected compromise, revoke before investigating, and do not use the compromised credential to perform the rotation. All rotations are logged with actor, time, and scope; the log is evidence, not bureaucracy.

## 9. Completion criteria

- [ ] Every secret inventoried with class, owner, consumers, and blast radius.
- [ ] Orphan secrets flagged and resolved.
- [ ] Runbook written for each class with exact steps and verification.
- [ ] Overlap strategy chosen per class.
- [ ] Drill executed on a non-production credential.
- [ ] Old credential proven rejected after rotation.
- [ ] Scheduled jobs exercised, not assumed.
- [ ] Drill duration recorded with the bottleneck.
- [ ] Emergency rotation path defined with a shorter approval route.
- [ ] Short-lived credential automation adopted where supported.

## 10. Deliverables and handover

Artifacts: `SECRETS_INVENTORY.md`, runbooks, drill record.

Handover: `04-process/handover/` P03 uses the inventory as the access-transfer checklist — a secret missing there is a secret the new owner cannot rotate; `02-engineering/security-hardening/` owns remediation of exposed keys; `04-process/observability-reliability/` P03 adds expiry alerts for the classes with fixed lifetimes, because rotation fails quietly when the calendar is the only reminder.
