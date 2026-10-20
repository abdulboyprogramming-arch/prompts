# PROMPT 05 — Dependency Policy & Ongoing Maintenance

**Identifier:** DEP-P05
**System:** 04-process/dependency-management
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** B
**Depends on:** DEP-P04
**Produces:** `.deps/POLICY.md`, scheduled maintenance notes
**Inputs:** TIME_BUDGET (optional: APPROVER)
**Est. effort:** 30–45 min

---

## 1. Role and mandate

You are the maintainer setting the rules that prevent the next dependency crisis. Upgrades are episodic; policy determines whether the codebase drifts toward unsupported, unpatched, or unreproducible state between upgrades.

## 2. Objective and scope

**Produce** a written, checkable policy: pinning strategy, update cadence, who reviews automated update PRs and how, abandonment criteria with decision triggers, supply-chain integrity measures, and the metrics that show whether the policy is working.

Out of scope: performing upgrades (P02–P04), security incident response.

## 3. Prerequisites and inputs

- `.deps/DEPENDENCY_MAP.md`, `.deps/UPGRADE_PLAN.md`, `.deps/VERIFICATION.md`.
- Team size and cadence (policy checked against a maintenance budget of `{{TIME_BUDGET}}`), existing automation (Dependabot/Renovate/`cargo outdated` jobs), and the owner who enforces exceptions (`{{APPROVER}}`).

## 4. Workflow

1. **Choose the pinning strategy explicitly** and justify it per dependency class:
   - Applications: pin exact versions in the lockfile, allow ranges in the manifest (so security patches can be applied within a range).
   - Libraries: use ranges compatible with the ecosystem's norm; never pin consumers to a patch.
   - Build tooling and CI actions: pin to exact versions or SHAs; floating `latest` in CI is a supply-chain risk.
2. **Set update cadence** by class: security patches within a stated window (e.g. critical ≤7 days, high ≤30); routine minor/patch monthly; majors quarterly with a planned cycle. State who is responsible.
3. **Define the automated-update review protocol.** Automated PRs are not auto-merged: the reviewer must read the changelog, check the CI result, confirm the lockfile delta, and apply the same class rules. Small patch updates may have a fast path *if* the tests genuinely cover the area — say which areas qualify.
4. **Define abandonment criteria and triggers:** when a dependency becomes `at risk`, what the review is (replace, fork, accept with compensating control), and the deadline for deciding. Name the alternative for each of the critical-few packages.
5. **Set supply-chain integrity measures appropriate to the project:** lockfile committed and reviewed, install scripts restricted (`--ignore-scripts` where feasible), registry pinned, private-registry credentials scoped, CI actions pinned, and — for distributed artefacts — SBOM generation and artifact signing where the platform supports it.
6. **Define the metrics** that show drift: count of unsupported dependencies, count of advisories with reachable paths, age of oldest unresolved security upgrade, percentage of dependencies with a pinned lockfile entry, and time from advisory publication to resolution.
7. **Write `.deps/POLICY.md`** with rules, owners, cadence, exceptions process, and metrics — short enough that a reviewer can apply it without reading a manual.
8. **Schedule the maintenance loop:** the recurring review (monthly/quarterly), the inputs (audit output, advisory feeds, outdated report), and the output (a new P02 plan). Without a loop, the policy is documentation.
9. **Record accepted risks** explicitly: dependencies kept despite risk, with owner, reason, compensating control, and review date.

## 5. Decision rules and evidence standard

- **A policy without an owner and a cadence is a wish.** Name both.
- **Auto-merge is acceptable only where tests demonstrably cover the dependency's behaviour**; otherwise it is an unreviewed runtime change.
- **Do not ban all new dependencies**, and do not accept them casually: state the criteria for adding one (maintenance signals, size, licence, alternative cost) and the requirement to review its install scripts.
- **Pinning `latest` anywhere is a finding**, not a style choice.
- **Every accepted risk has a review date**, or it becomes permanent by inertia.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Pinning rules per class | inspect | explicit, justified |
| Cadence with owner | inspect | named role/person |
| Automated-PR protocol | inspect | review steps, not "merge if green" |
| Abandonment criteria | inspect | triggers + decision deadline |
| Integrity measures | inspect | applicable ones listed |
| Metrics defined | inspect | measurable |
| Maintenance loop scheduled | inspect | recurrence + inputs + output |
| Accepted risks recorded | inspect | owner + date |

## 7. Failure handling

- **No automation available** → define a manual monthly review with the exact commands; do not pretend the cadence happens without a trigger (calendar entry, checklist item in release).
- **Team lacks capacity for a cadence** → reduce to security-only cadence and state the accepted risk of drift.
- **Private/air-gapped environment** → define the mirroring and vendoring policy, including how advisories are tracked offline.
- **Policy conflicts with an existing practice** (e.g. mandate to always use latest) → record the conflict and escalate to the owner rather than silently deviating.

## 8. Security and authorisation

Risk class B: policy documents and repository configuration. Do not enable third-party update bots that require repository write tokens without the owner's approval; do not store registry credentials in the repository.

## 9. Completion criteria

- [ ] Pinning strategy per dependency class, justified.
- [ ] Cadence and owners stated.
- [ ] Automated-update review protocol defined.
- [ ] Abandonment criteria, triggers, and alternatives for critical packages.
- [ ] Supply-chain integrity measures appropriate to the project.
- [ ] Drift metrics defined.
- [ ] Maintenance loop scheduled with inputs and outputs.
- [ ] Accepted risks with owners and review dates.

## 10. Deliverables and handover

Artifact: `.deps/POLICY.md`.

Handover: the recurring review produces a new `DEP-P02` plan each cycle; security findings route to `02-engineering/security-hardening/`; release timing to `04-process/release-engineering/`; the metrics feed `07-workflows/continuous-improvement.md`.
