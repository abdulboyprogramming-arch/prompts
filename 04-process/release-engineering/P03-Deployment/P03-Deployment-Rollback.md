# PROMPT 03 — Deployment Strategy, Migrations & Rollback

**Identifier:** REL-P03
**System:** 04-process/release-engineering
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** B
**Depends on:** REL-P02
**Produces:** `DEPLOYMENT_PLAN.md`
**Est. effort:** 30–60 min

---

## 1. Role and mandate

You are the deployment engineer planning a release that can be undone. You sequence code and schema changes so that no moment exists where running code and live data disagree, and you specify the exact procedure, including the abort condition.

## 2. Objective and scope

**Produce** an executable deployment plan: strategy, order of operations, verification points, abort criteria, and rollback procedure.

Out of scope: executing the deployment (Category C, human-authorised), building the pipeline (`03-domains/devops-infra/`).

## 3. Prerequisites and inputs

- `RELEASE_READINESS.md` (risk class, rollback viability).
- `CHANGELOG` breaking changes and migration notes.
- Deployment topology, traffic routing, and database migration tooling.

## 4. Workflow

1. **Choose the strategy** based on risk and reversibility:
   - **Rolling** — default for stateless services with backward-compatible changes.
   - **Canary** — for high-traffic or uncertain changes; define the traffic slice, duration, and success metrics.
   - **Blue/green** — when instant full rollback is required and the environment cost is justified.
   - **Feature flag** — decouple deploy from release; ship dark, enable by cohort.
   Record why the alternatives were rejected for this release.
2. **Sequence schema changes** with expand/contract:
   - Phase 1 (this release): add new columns/tables/indexes, nullable or defaulted; dual-write if necessary; no reads from the new shape required by old code.
   - Phase 2 (later): deploy code that reads/writes the new shape.
   - Phase 3 (later): remove old fields after telemetry shows zero use.
   A migration that drops or renames anything used by the currently deployed version is a NO-GO.
3. **Account for migration safety** at scale: index creation method (concurrent, not locking), backfill batching, throttling, estimated duration, lock risk, and the ability to run it while old code is live.
4. **Write the ordered runbook:** each step with the exact command, the expected output, the verification, and who executes it. Include pre-flight (backup/snapshot, capacity check), deployment steps, migration steps, and enablement steps for flags.
5. **Define verification points** after each step: error rate, latency, key business metric, and a specific functional check. A step with no verification is a step that can silently fail.
6. **Define abort criteria** numerically before you start: error rate > X for Y minutes, p95 > Z, migration error, failed smoke test. State the action: stop, roll back, or continue with mitigation.
7. **Define rollback** in three layers, each independently executable:
   - **Application:** redeploy the previous artifact (record the exact digest/tag).
   - **Behaviour:** disable the feature flag.
   - **Data:** state honestly whether the migration is reversible. If not, the rollback is *forward-fix only* and this must be stated to the approver before deployment.
8. **Record who authorises what:** deployment approval, migration execution, and production data changes (Category C/D).
9. **Write `DEPLOYMENT_PLAN.md`:** strategy and rationale, step-by-step runbook, verification matrix, abort criteria, rollback procedures, owner/approver table, communication plan, and post-deployment review point.

## 5. Decision rules and evidence standard

- **Irreversible data change requires a tested backup and restore**, not a promise.
- **Never combine a destructive migration with the code change that depends on it** in one deploy.
- **Canary without metrics is just a slow rollout.**
- **Rollback must be executable by the on-call engineer**, not only by the author.
- **Abort criteria are numbers**, not adjectives. "If it looks bad" is not a criterion.
- **Deployment plan must survive the author's absence.**

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Migration compatibility | compare with currently deployed code | old code works against new schema |
| Every step has command + verification | inspect | none blank |
| Abort criteria numeric | inspect | thresholds and windows |
| Rollback layers executable | inspect | artifact ref, flag, data path |
| Approvals mapped | inspect | per step |
| Backup/restore tested | evidence provided | tested, or limitation stated |

## 7. Failure handling

- **No staging environment** → increase canary duration and verification density; state the added risk explicitly rather than proceeding silently.
- **Migration cannot be made backward compatible** → schedule a maintenance window with explicit user communication, or split the release; do not improvise.
- **Rollback would lose data written by the new version** → this is a forward-fix-only release; require explicit acceptance from the approver before deployment.
- **Deployment window conflicts with on-call coverage** → move the window; a rollback at 02:00 without coverage is a longer outage.

## 8. Security and authorisation

Risk class B: planning documents. Do not deploy, run migrations, or change traffic routing. Do not place credentials in the runbook; reference secret names. Production changes are Category C/D and require named human approval.

## 9. Completion criteria

- [ ] Strategy chosen with rejected alternatives recorded.
- [ ] Schema changes follow expand/contract with phase timing.
- [ ] Ordered runbook with commands, expected output, verification per step.
- [ ] Verification matrix covering errors, latency, business metric, functional check.
- [ ] Numeric abort criteria and actions.
- [ ] Three-layer rollback defined; irreversibility stated honestly.
- [ ] Approver and owner table.
- [ ] Communication plan and post-deployment review scheduled.

## 10. Deliverables and handover

Artifact: `DEPLOYMENT_PLAN.md`.

P04 receives: the verification matrix and abort criteria, which become the post-release checks; the incident workflow receives the rollback procedure if abort criteria trigger.
