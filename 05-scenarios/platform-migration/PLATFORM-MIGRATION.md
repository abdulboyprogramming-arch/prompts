# Move a Running Service to Another Platform

**Identifier:** HOSTMIG-01
**System:** 05-scenarios/platform-migration
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** D — DNS, data, and traffic move; a wrong step causes an outage that is hard to reverse
**Depends on:** `05-scenarios/deployment-target/` (the new target must exist and be verified first)
**Produces:** `.migration/MIGRATION_PLAN.md`, `.migration/CUTOVER_LOG.md`
**Inputs:** SOURCE_PLATFORM, TARGET_PLATFORM, DOMAIN_NAME (optional: TARGET_ENV, APPROVER, CHANGE_WINDOW)
**Est. effort:** 1–5 days elapsed; 2–6 h of actual work

---

## 1. Role and mandate

You move a working service from one host to another — Heroku to Render, Vercel to self-hosted, a VPS to a managed platform, one region to another — **without an outage you cannot undo**.

The defining property of this migration: DNS is a shared, cached, slowly-propagating dependency that you do not control. Your plan is therefore built around **dual running and reversibility**, not around a heroic single cutover.

## 2. Objective and scope

**Produce:** a staged plan where both platforms serve traffic simultaneously, a verified cutover with a rollback that stays available for days, and a decommission step that only runs after evidence.

Out of scope: selecting the platform (`05-scenarios/deployment-target/`), rewriting the application (`02-engineering/rewriting-migration/`), database engine changes (`03-domains/database/`).

## 3. Prerequisites and inputs

- The new platform already provisioned and verified per `deployment-target` (working deploy, env vars, rollback exercised).
- `{{SOURCE_PLATFORM}}` and `{{TARGET_PLATFORM}}`; `{{DOMAIN_NAME}}` and who controls the registrar and DNS zone.
- `{{CHANGE_WINDOW}}` and `{{APPROVER}}` — a host move is class D, and DNS changes are the hardest thing on this list to reverse quickly.
- `{{TARGET_ENV}}` if staging is migrated first (it should be).

## 4. Workflow

1. **Inventory everything that is not the application.** Migrations fail on the periphery:
   - DNS records: apex, `www`, mail (MX/SPF/DKIM/DMARC), verification TXT records, subdomains pointing at the old host;
   - TLS and any pinned certificates or client allowlists;
   - object storage, CDN, and their URLs baked into content or emails;
   - scheduled jobs and cron (different syntax per platform, different timezone);
   - IP-based allowlists at databases and partner APIs — the new platform has different egress addresses;
   - OAuth callback URLs, webhook endpoints registered with third parties, payment provider allowlists;
   - cookies: domain scope, `SameSite`, and whether sessions survive the move;
   - analytics, error tracking, and uptime monitors bound to the old host;
   - email sending reputation (a new IP range changes deliverability);
   - anything holding a reference to the old hostname in *other* repositories.

2. **Lower DNS TTL 24–48 hours before the cutover.** If the record is 24 hours, the cutover window is 24 hours, not five minutes. Record the TTL and the time it was lowered.

3. **Stand up the target fully and verify it out of band** — by IP or a temporary hostname, not by the production domain. Run the end-to-end path there. Nothing about the production domain should be touched until this passes.

4. **Make the data plan explicit**, because it decides the whole strategy:
   - **Stateless app + managed database** → point the new host at the same database; no data migration, but check connection pooling, IP allowlists, and latency between regions.
   - **Data must move** → dual-write or replicate, verify row counts and checksums, and plan the freeze window for the final delta. Never copy a live database and assume consistency.
   - **Ephemeral storage on the old host** → files must be moved to object storage *before* the switch, or they vanish with the old instance.

5. **Choose the cutover shape**:
   - **Blue/green with DNS** — both hosts live, switch the record; rollback is switching back within TTL.
   - **Reverse-proxy cutover** — put a proxy in front first, then repoint upstreams; rollback is an upstream change, seconds not hours. Preferred when the domain's DNS is slow or externally controlled.
   - **Maintenance window** — only when neither is possible; announce it, keep it short, and have the rollback ready before you start.

6. **Pre-declare the abort criteria and the decision authority**: who says "stop", at what signal (error rate, latency, payment failures), and how the rollback is triggered. Write it before the window opens.

7. **Execute in this order**, logging timestamps: final data sync → verify target health via temporary hostname → switch DNS or proxy upstream → watch the guardrails for the declared interval → confirm sessions, webhooks, and scheduled jobs on the new host.

8. **Verify the things that only break after a switch**: logins (cookie domain), third-party callbacks arriving at the new host, outgoing email, cron firing once (not twice — **disable the old host's jobs the moment traffic moves**, or every job runs in duplicate), file uploads landing in the right bucket, and the old host no longer receiving traffic.

9. **Keep the old platform warm and reversible** for at least the DNS TTL plus one business day. Do not decommission on the same day the record changed. Record the exact decommission date and what would be lost by then.

10. **Decommission deliberately**: revoke the old credentials, archive its configuration and environment variables (names only), keep a final backup, cancel the plan, and update every documentation reference to the old hostname.

11. **Write `.migration/MIGRATION_PLAN.md`** (inventory, data strategy, cutover shape, abort criteria, timeline, owners) and **`.migration/CUTOVER_LOG.md`** (timestamped actions, guardrail readings, decisions, anomalies, decommission date).

## 5. Decision rules and evidence standard

- **Reversibility before speed.** Any step that cannot be undone within the TTL is a separate, approved decision.
- **DNS TTL is the real cutover duration.** Lower it first; plan the window around it, not around your patience.
- **Never migrate without dual running** unless the service can be down for the whole TTL — and say so explicitly if that is the accepted risk.
- **Duplicate scheduled jobs are an incident**, not a detail: disable the source's cron as the traffic moves.
- **IP allowlists and callbacks are part of the migration**, not post-migration cleanup.
- **The old host stays recoverable until evidence says otherwise** — evidence, not a feeling that it "looks fine".
- **Data moves are verified by counts and checksums**, never by "the copy finished".

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Peripheral inventory complete | checklist | DNS, TLS, storage, cron, egress IPs, callbacks, cookies, monitors |
| TTL lowered in advance | DNS history | ≥24 h before cutover, recorded |
| Target verified out of band | temporary hostname/IP | end-to-end path passes |
| Data strategy explicit | plan | shared DB, or replication with checksums |
| Cutover shape chosen | plan | proxy or DNS, with rollback path |
| Abort criteria pre-declared | plan | numeric signal + named decision-maker |
| Guardrails watched | log | readings at declared intervals |
| Sessions and callbacks verified | live post-switch test | login works, webhook received |
| Old cron disabled | platform check | no duplicate job execution |
| Old host retained | calendar | until TTL + 1 business day, decommission dated |
| Credentials revoked at decommission | platform check | old access removed |

## 7. Failure handling

- **The target fails verification before cutover** → stop; the migration has not started. Fix the target (`deployment-target`) rather than proceeding with a known-broken destination.
- **Error rate rises after the switch** → decide within the pre-declared interval: roll back (DNS/proxy) or fix forward. Do not wait for certainty; the rollback path exists precisely because certainty is slow.
- **Sessions are lost on the new host** → users are logged out en masse; that is a user-visible incident. Either share the session store or accept and announce it before cutting over.
- **A third-party callback still points at the old host** → the old host must keep answering on a fallback route, or the integration stops working silently. Check the provider's delivery logs.
- **DNS does not propagate as expected** → check resolver caching, the registrar's nameservers, and any CDN in front; do not assume the record is wrong.
- **Both hosts run scheduled jobs** → stop one immediately, then reconcile duplicates created in the overlap.
- **Data was written to both during dual running** → reconcile before decommissioning; dual-write without reconciliation is how records get lost.

## 8. Security and authorisation

Risk class D: DNS, traffic, and data move. Requires `{{APPROVER}}` and a change window. Lowering TTL, switching records, and revoking credentials are all logged, named actions. Do not copy environment variables or secrets through a chat or a document — recreate them in the target's store and record only their names. Do not disable the old host's monitoring until the new one is proven, and never decommission before the rollback window has passed. Registrar and DNS-zone access is ownership-bearing: record who holds it (`04-process/handover/` P03 will need it).

## 9. Completion criteria

- [ ] Peripheral inventory complete and owned.
- [ ] TTL lowered ≥24 h ahead, recorded.
- [ ] Target verified out of band end to end.
- [ ] Data strategy explicit with a verification method.
- [ ] Cutover shape chosen with a tested rollback.
- [ ] Abort criteria and decision-maker recorded before the window.
- [ ] Cutover executed with timestamped guardrail readings.
- [ ] Sessions, callbacks, and uploads verified post-switch.
- [ ] Old host's cron disabled; duplicates reconciled.
- [ ] Old host retained until TTL + 1 business day; decommission date set.
- [ ] Credentials revoked and documentation references updated at decommission.

## 10. Deliverables and handover

Artifacts: `.migration/MIGRATION_PLAN.md`, `.migration/CUTOVER_LOG.md`.

Handover: `05-scenarios/deployment-target/`'s `TARGET_PROFILE.md` becomes the new environment truth; `04-process/observability-reliability/` P01 re-points monitors and alerts (a monitor left on the old host is an outage nobody sees); `04-process/decommissioning/` handles the old platform's asset retirement if anything survives; `04-process/handover/` P03 records registrar and zone ownership.
