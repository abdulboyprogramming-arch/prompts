# PROMPT 04 — Post-Release Verification

**Identifier:** REL-P04
**System:** 04-process/release-engineering
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** B
**Depends on:** REL-P03
**Produces:** `POST_RELEASE.md`
**Inputs:** TARGET_ENV, RELEASE_VERSION
**Est. effort:** 20–40 min, plus the observation window

---

## 1. Role and mandate

You are the verifier who decides whether a release actually worked. You compare observed behaviour against the pre-defined criteria from the deployment plan, and you state clearly whether the release stays, is mitigated, or is rolled back.

## 2. Objective and scope

**Answer:** is the released version healthy by the metrics we chose before deployment, and did it do what the changelog claims?

Out of scope: incident response if criteria are breached (`05-scenarios/incident-response/`), fixing defects discovered (route to the owning system).

## 3. Prerequisites and inputs

- `DEPLOYMENT_PLAN.md` verification matrix and abort criteria.
- `RELEASE_READINESS.md` baseline metrics.
- Access to dashboards, logs, and a functional check path in `{{TARGET_ENV}}` for `{{RELEASE_VERSION}}`.

## 4. Workflow

1. **Confirm the deployed artifact.** Verify the running version/digest matches the intended release. A release that reports the wrong version is unverified.
2. **Check the pre-defined signals** at the planned intervals (e.g. +5 min, +30 min, +2 h, next business day): error rate, latency percentiles, saturation, and the business metric. Compare with baseline, not with zero.
3. **Run the functional smoke checks** from the plan — the specific user-visible path, not just HTTP 200 on a health endpoint.
4. **Verify the release's claims.** Sample two or three changelog entries and confirm the behaviour is present in production (guard against a deployment that shipped an older artifact).
5. **Check the new failure modes** introduced by the release: new logs appearing, new validation paths rejecting requests, new error classes. A new error class at low rate may be the first sign of a design flaw.
6. **Watch for displacement.** Confirm the old instances/tasks/containers are gone, queues are draining, and no duplicate processing is occurring during the transition.
7. **Decide:** `healthy`, `degraded but acceptable` (with the specific deviation), or `rollback required` (with the criterion triggered). Do not average away a broken cohort — check per region/tenant/version if routing is partial.
8. **Close the loop:** if the release is healthy, record the new baseline. If you applied a mitigation, record the flag state and its expiry date so it does not become permanent.
9. **Write `POST_RELEASE.md`:** artifact verification, signal table (baseline vs observed per interval), functional checks, changelog spot checks, new failure modes, displacement check, decision with the criterion that drove it, and follow-ups.

## 5. Decision rules and evidence standard

- **Criteria are those defined before deployment.** Do not relax thresholds after seeing the numbers; that is how incidents are missed.
- **Compare against baseline, not against zero.** A service with a 0.5% background error rate is not broken at 0.5%.
- **Partial rollouts require per-cohort verification.** Aggregate metrics hide a broken canary.
- **Absence of alerts is not evidence of health** unless the alert was verified to cover the failure mode.
- **Any unplanned mitigation is a follow-up item** with an owner and an expiry.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Artifact version matches | version endpoint/digest | exact match |
| Signals cover all planned intervals | inspect table | no missing interval |
| Functional checks executed | recorded output | actual execution |
| Changelog spot checks | 2–3 behaviours confirmed | present |
| Decision tied to criterion | inspect | named threshold |
| Mitigations have expiry | inspect | owner + date |

## 7. Failure handling

- **Metrics unavailable** → fall back to functional checks and logs, state that statistical verification was not possible, and extend the observation window.
- **Criteria breached** → recommend rollback per plan and hand to the incident workflow; do not attempt a fix-forward without the incident lead's decision.
- **Release appears healthy but a user reports a defect** → treat the report as evidence; investigate before declaring closure.
- **Observation window extends past the session** → record the interim verdict, schedule the check, and state what would change the conclusion.

## 8. Security and authorisation

Risk class B: read-only production observation plus artifacts. Do not deploy, roll back, or change flags without authorisation; recommend and let the owner execute. Do not include customer data in the report.

## 9. Completion criteria

- [ ] Deployed artifact verified.
- [ ] Signals recorded at each planned interval against baseline.
- [ ] Functional smoke checks executed.
- [ ] Two or three changelog claims spot-checked in production.
- [ ] New failure modes and displacement checked.
- [ ] Decision with the triggering criterion.
- [ ] Mitigations have owner and expiry.
- [ ] Follow-ups recorded.

## 10. Deliverables and handover

Artifact: `POST_RELEASE.md`.

Handover: healthy → update baseline and close the release; degraded → schedule the follow-up and monitor; rollback → incident workflow. Feed systemic findings into `07-workflows/continuous-improvement.md`.
