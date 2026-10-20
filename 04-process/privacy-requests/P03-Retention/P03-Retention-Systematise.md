# PROMPT 03 — Retention & Systematisation

**Identifier:** PRIV-P03
**System:** 04-process/privacy-requests
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** B
**Depends on:** PRIV-P02
**Produces:** `.privacy/RETENTION.md`
**Inputs:** RETENTION_DAYS (optional: APPROVER)
**Est. effort:** 30–60 min

---

## 1. Role and mandate

You are the engineer making the *next* request cheap. If handling one deletion took three days of discovery and manual SQL, the process will not survive volume, and it will fail quietly when someone is on holiday. Your output is retention rules that delete data before it becomes a liability, and a mechanism that makes requests routine.

## 2. Objective and scope

**Produce:** a per-data-class retention schedule with enforcement, a self-service or documented request path, and the monitoring that proves deletions actually happen.

Out of scope: legal determinations about retention periods (owner/legal), the deletion itself (P02).

## 3. Prerequisites and inputs

- `.privacy/DATA_MAP.md`, `.privacy/REQUEST_LOG.md` (what was manual, blocked, or repeated).
- Existing retention rules in code, lifecycle policies, and vendor settings.
- Contractual or regulatory minimums from the accountable owner (`{{RETENTION_DAYS}}` where fixed, approved by `{{APPROVER}}`) — record what you are told; do not invent periods.

## 4. Workflow

1. **Group data into classes with a retention basis**: account data, transaction records, support conversations, telemetry, marketing, logs, backups, derived analytics, ML training data. For each, record the driver (contractual, legal minimum, product need, no basis) and a period.
2. **Identify the classes with no retention rule.** These accumulate indefinitely and are the largest liability; they are also the easiest to fix with a lifecycle policy.
3. **Separate the *legal minimum* from the *product habit*.** "We keep everything forever in case" is a decision with a cost and a risk; surface it as one, with an owner.
4. **Make deletion structural, not manual**: database TTL jobs or partition drops, object lifecycle rules, log retention settings, index rotation, queue message TTLs, and vendor-side retention configuration. Prefer mechanisms that run without a human.
5. **Design the request path** scaled to expected volume:
   - **low volume**: a documented runbook plus the P01 map, executed by an engineer;
   - **medium**: a script that performs P01's search automatically for a given identifier and produces the deletion plan;
   - **high**: a self-service flow with verification and automatic execution per system, with an audit log.
6. **Build the verification into the mechanism**: a scheduled job that samples deletions and confirms the rows are gone from every mapped system, alerting when a system silently stops deleting.
7. **Handle the exceptions explicitly**: legal holds, financial records, fraud prevention, and safety data that must survive a deletion. Record the exemption, the authority, the access restriction, and the review date.
8. **Record the residual**: backups with their age-out dates, vendor copies awaiting confirmation, and archives. Each has an owner and a date.
9. **Write `.privacy/RETENTION.md`:** data class table with driver and period, enforcement mechanism per class, gaps with owners, request path design, verification job, exemptions, and residual list.
10. **Feed the gaps back**: every class without enforcement becomes a tracked item, and every blocked system from P02 becomes an owner action.

## 5. Decision rules and evidence standard

- **Retention must be enforced by a mechanism**, or it is an intention. A policy document with no TTL is not retention.
- **The default should be deletion**, with explicit exemptions — the opposite accumulates liability by inertia.
- **Never shorten retention below a legal or contractual minimum** without the owner's written decision.
- **Automate verification**, because silent failure of a deletion job looks exactly like success.
- **A blocked system is an owner action with a date**, not a footnote.
- **Record the basis for each period.** "90 days because finance said so" is auditable; "90 days" is not.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Every data class has a driver and period | inspect | no blanks |
| Enforcement mechanism per class | inspect | TTL/lifecycle/job named |
| Classes without rules listed | inspect | owners assigned |
| Request path defined for expected volume | inspect | matches volume |
| Verification job exists | run/inspect | samples and alerts |
| Exemptions recorded with authority | inspect | restricted access + review date |
| Residual list with dates | inspect | backups, vendors, archives |
| Delete jobs tested | observe a run | data actually removed |

## 7. Failure handling

- **No legal guidance available on periods** → record `period undetermined` with the owner's name, and implement the shortest defensible default with a review date; do not invent compliance.
- **A vendor cannot confirm deletion** → record as residual with a contractual route and a date; escalate if the contract does not provide one.
- **Deletion jobs conflict with reporting** → separate the reporting copy from the operational store and state which is authoritative; do not disable retention to fix a dashboard.
- **Volume exceeds the manual path** → build the scripted search first (P01's queries are already written), then self-service.
- **An exemption would cover most of the data** → the exemption is the policy; surface that to the owner, because it means the retention promise is largely unenforced.

## 8. Security and authorisation

Risk class B: configuration, jobs, and documentation. Retention jobs delete data — they require a reviewed, reversible-first rollout (dry run, then a scoped period). Do not build self-service deletion that bypasses identity verification. Keep the retention document free of personal data.

## 9. Completion criteria

- [ ] Data classes enumerated with driver and period.
- [ ] Enforcement mechanism per class, with gaps assigned to owners.
- [ ] Request path designed for expected volume.
- [ ] Verification job sampling deletions and alerting on failure.
- [ ] Exemptions recorded with authority, access restriction, and review date.
- [ ] Residual copies listed with owners and dates.
- [ ] Delete jobs dry-run and then tested on a scoped period.

## 10. Deliverables and handover

Artifact: `.privacy/RETENTION.md`.

Handover: retention mechanisms to `03-domains/database/` (schema-level TTL) and `03-domains/devops-infra/` (lifecycle policies); blocked systems to their owners with dates; the verification job to `04-process/observability-reliability/` so a silent failure alerts; the request runbook into onboarding documentation.
