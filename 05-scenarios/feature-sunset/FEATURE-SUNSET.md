# Feature Sunset: removing something customers depend on

**Identifier:** SUNSET-01
**System:** 05-scenarios/feature-sunset
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** B for analysis and flags; **C** for deprecation notices sent externally; **D** for disabling data or deleting records
**Depends on:** none
**Produces:** `.sunset/SUNSET_PLAN.md`, `.sunset/USAGE_EVIDENCE.md`, the removal checklist
**Inputs:** FEATURE_SCOPE (optional: NOTICE_PERIOD, APPROVER, TIME_BUDGET)
**Est. effort:** 2–4 h for the plan; the notice period dominates the calendar
**Gallery:** A feature is being retired and you need usage evidence, a notice that is not a surprise, a reversible switch-off, and a decision about the data.

---

## 1. Role and mandate

You plan the removal of one feature from a live product — not an entire system (`04-process/decommissioning/` covers that).

Feature sunsets fail in a predictable pattern: the notice goes out to nobody in particular, the usage measurement counted page views rather than workflows, a handful of large accounts depend on it in a way the dashboard never showed, and the removal takes out an integration nobody knew shared the same table. The feature is gone, and three customers are angry in public.

Your job is to make the removal **boring**: measured, announced, reversible for a defined window, and complete — including the code, the flags, the data, and the documentation.

## 2. Objective and scope

**Produce:** usage evidence by customer and by workflow, a dependency map of everything that shares the feature's code or data, a communicated deprecation timeline, a reversible disable switch, an exit path offered to affected users, and a removal checklist that includes the data decision.

Out of scope: deciding *whether* to sunset — that is a product decision you are given. Out of scope: contract renegotiation, though you must surface which customers have contractual commitments that prohibit the change.

## 3. Prerequisites and inputs

- `{{FEATURE_SCOPE}}` — what exactly is being removed, described precisely enough to be measured: the UI surface, the API endpoints, the jobs, the exports, and the data it owns.
- `{{NOTICE_PERIOD}}` — how much warning users get. Often set by contract or by the platform (app stores, marketplaces); if unset, derive it from usage concentration and say so.
- `{{APPROVER}}` — who accepts the customer impact.
- `{{TIME_BUDGET}}` — the analysis budget, not the calendar.

## 4. Workflow

1. **Define the feature as a measurable object.** List its surfaces: routes, API endpoints, UI entry points, background jobs, webhooks, exports, and stored data. Anything you cannot observe, you cannot declare unused.

2. **Measure usage properly, and be suspicious of the easy number.** Distinguish:
   - unique **accounts** touching it, not page views;
   - **workflows completed**, not just entry points hit (a click that abandons is not usage);
   - **frequency and recency** — daily users and once-a-quarter users have different needs;
   - **concentration** — if three accounts generate 80% of usage, the average is irrelevant;
   - **machine clients** — API integrations with no human behind them, which will break silently and loudly;
   - **indirect use** — data consumed by an export, a report, or another team's pipeline.

3. **Look for the users your telemetry misses.** The recurring blind spots: a customer whose integration authenticates but makes no UI requests; a scheduled job that writes to the feature's table; a partner reading an endpoint you consider internal; support staff using an admin interface; and a single large customer with an allowlisted beta. Check access logs and database writes, not only product analytics.

4. **Build the dependency map from the code and the data.** Which modules, tables, flags, jobs, tests, dashboards, alerts, and runbooks reference the feature? Which other features read its tables? Removing the UI while leaving a shared table in place means the removal is cosmetic; removing the table while an unexamined job reads it means an incident.

5. **Check contractual and platform obligations.** Do any customer contracts, SLAs, or platform policies (app stores, marketplaces, certifications) require the feature or a notice period? Are there users in regulated industries whose audit trail depends on it? This determines whether the plan is a plan or a negotiation.

6. **Choose the shutdown mechanism, in order of preference:**
   - **Flag off** for the UI, with the API and data intact — reversible in seconds.
   - **Degraded mode**: the feature stops accepting new work but existing data remains readable and exportable.
   - **Endpoints return a documented, specific error** (not a 500) with a link to the migration path.
   - **Removal of code and data** only after a quiescence window in which zero traffic has been observed.

7. **Design the exit path before the notice.** What should affected users do instead? A replacement feature, an export, an API alternative, or an apology and a date. A deprecation without an alternative is a hostage negotiation; a deprecation with a documented alternative is an upgrade.

8. **Write the notice as three communications, not one:** early heads-up to the concentrated users (personal where the account matters), the formal deprecation notice with dates and the migration path, and the final reminder two weeks before switch-off. Name a contact and a support route. Silence is not consent.

9. **Sequence the removal so each step is reversible until the last:**
   measurement → notice → migration support → flag off (reversible) → quiescence observation → API endpoints retired → code removal → data retention decision → data deletion → documentation and changelog cleanup. Record the rollback for each step and the point after which rollback is no longer possible.

10. **Decide the data explicitly, and write it down.** Options: delete now; retain for a contractual period; export to the customer and delete; or anonymise and keep for analytics. Whichever is chosen must satisfy `04-process/privacy-requests/` retention rules and be recorded with a date, an owner, and evidence of execution. "We will leave the table there" is an unmade decision that becomes a compliance finding.

11. **Write `.sunset/SUNSET_PLAN.md`** (surfaces, usage evidence, dependencies, timeline, communications log, rollback points, data decision, completion evidence) and **`.sunset/USAGE_EVIDENCE.md`** (the queries, their results, and their limits — including what telemetry cannot see).

## 5. Decision rules and evidence standard

- **Accounts and workflows, not page views.** Volume alone does not tell you who will be affected.
- **Machine clients are customers too**, and they do not read release notes.
- **Never remove a surface you cannot measure.** Instrument first, wait, then judge.
- **Concentration beats averages.** Three accounts can be the whole feature.
- **Reversibility is a sequence, not a property** — say at which step it is lost.
- **A deprecation without an alternative is a break**, and should be approved as one.
- **Data retention is part of the sunset**, not a follow-up ticket. An orphaned table outlives everyone who knew why it was there.
- **Silence is not consent.** If the notice could not reach a group, say which group and why.
- Mark usage claims `verified` (query and date) or `inferred`.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Surfaces enumerated | Plan | Routes, endpoints, jobs, webhooks, exports, data listed |
| Usage by account | Telemetry query | Unique accounts, workflows completed, recency |
| Concentration identified | Query | Top accounts named (or "none above threshold") |
| Blind spots checked | Access logs, DB writes | Machine and admin usage examined separately |
| Dependency map | Code search + schema | Every table, flag, job, dashboard, runbook referenced |
| Contract check | Contract list / owner | Commitments surfaced before notice |
| Exit path documented | Plan | Alternative or export exists for every affected class |
| Communications logged | Plan | Three notices, dates, recipients, contact named |
| Reversibility per step | Plan | Rollback and the last reversible point stated |
| Data decision recorded | Plan | Option chosen, owner, date, execution evidence |
| Quiescence observed | Monitoring | Zero traffic for the stated window before code removal |

## 7. Failure handling

- **Usage cannot be measured** (no telemetry, no logs) → instrument now and delay the decision; removing an unmeasured feature is a coin flip. If delay is impossible, state the uncertainty in the notice and offer a longer window.
- **A contract requires the feature** → escalate to `{{APPROVER}}`; the options are renegotiation, an exception for that customer, or a longer timeline. Do not remove and apologise.
- **The affected users are numerous but low-value** → the decision is still product's; your job is to make the notice cheap and the exit path good.
- **The dependency map is incomplete** (dynamic references, external consumers) → treat unknown dependencies as present, keep the data readable longer, and monitor for 404s or errors after switch-off.
- **The team wants to skip the notice period** → quantify who would be surprised and offer the shortest defensible period with a direct outreach list.
- **Data cannot be deleted because another team's pipeline reads it** → that is a dependency, not a blocker for the decision: transfer ownership of the table explicitly or keep the feature.

## 8. Security and authorisation

Analysis and flag design are B. Sending external notices is C. Disabling a feature in production, or deleting data, is D and requires `{{APPROVER}}` plus a verified backup path (`05-scenarios/disaster-recovery/`) and a communication plan. Never delete a table to "complete" a sunset while a restore has never been tested. Exports containing customer data follow the same handling rules as production access.

## 9. Completion criteria

- [ ] Feature defined as measurable surfaces.
- [ ] Usage measured by account, workflow, recency, and concentration.
- [ ] Telemetry blind spots examined.
- [ ] Dependency map complete, including shared tables and jobs.
- [ ] Contractual obligations surfaced.
- [ ] Exit path documented for every affected user class.
- [ ] Three communications sent and logged.
- [ ] Reversibility stated per step, with the last reversible point.
- [ ] Quiescence window observed before code removal.
- [ ] Data decision recorded, owned, dated, and executed.
- [ ] Documentation, changelog, and flags cleaned up.

## 10. Deliverables and handover

Artifacts: `.sunset/SUNSET_PLAN.md`, `.sunset/USAGE_EVIDENCE.md`, communications log, data decision record.

Handover: `04-process/decommissioning/` handles whole systems and shares the notice and data-retirement machinery — do not re-derive it. `04-process/feature-flags/` owns the flag mechanics and the retirement of the flags themselves. `04-process/privacy-requests/` governs retention and deletion evidence. `04-process/documentation/` must update every document that mentions the feature, or the docs become a source of support tickets about a feature that no longer exists.
