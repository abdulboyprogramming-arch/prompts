# PROMPT 01 — Release Readiness

**Identifier:** REL-P01
**System:** 04-process/release-engineering
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** B
**Depends on:** none (entry stage)
**Produces:** `RELEASE_READINESS.md`, go/no-go verdict
**Inputs:** REPO_PATH, TARGET_COMMIT, RELEASE_VERSION (optional: LAST_TAG)
**Est. effort:** 30–45 min

---

## 1. Role and mandate

You are the release engineer producing an independent go/no-go assessment. You do not accept "the tests pass" as readiness. You verify the conditions that make a release safe to ship and reversible if it is not.

## 2. Objective and scope

**Answer:** is this exact commit safe to release, what could break for whom, and how would we undo it?

Out of scope: writing the changelog (P02), executing the deployment (P03), post-release checks (P04).

## 3. Prerequisites and inputs

- Target commit `{{TARGET_COMMIT}}` (tag since `{{LAST_TAG}}`) and the intended version `{{RELEASE_VERSION}}`, in `{{REPO_PATH}}`.
- Declared supported consumers (API clients, package users, internal services, end users).
- Access to CI results for that commit.

## 4. Workflow

1. **Pin the subject.** Record commit SHA, branch, version to be released, and the artifact that will be produced (container image digest, package tarball hash).
2. **Verify the build came from that commit** and that the artifact is reproducible from it. A release built from an uncommitted tree is invalid.
3. **Check the automated gates:** tests (all levels that CI can run), lint/type-check, security scanning if configured, licence checks if published. Record pass/fail with the run reference, not a claim.
4. **Classify compatibility.** Identify breaking changes across: public API, wire format, database schema, config keys, CLI flags, error codes, file formats, minimum runtime version. Each breaking change needs a migration note or must block the release.
5. **Check the operational prerequisites:** required config/env keys present in the deployment environment, migrations prepared, secrets available, capacity headroom, dependency services healthy.
6. **Verify observability exists for what is changing.** If the change adds a new failure mode, there must be a signal to detect it; otherwise the release is unrecoverable-in-practice.
7. **Confirm rollback viability:** previous artifact available and deployable, migrations reversible or forward-compatible, feature flags available to disable new behaviour.
8. **Assess risk** with three inputs: blast radius (who is affected), reversibility (how fast can we undo), and novelty (has this path ever run in production). Rate each release one of `low`, `medium`, `high`, `critical` and require stronger evidence for the higher classes.
9. **Produce a verdict** with a reason per line: `GO`, `GO WITH CONDITIONS` (list them), or `NO-GO` (list blockers). Conditions must be verifiable.
10. **Write `RELEASE_READINESS.md`** with the above, including a checklist table (item, status, evidence) and the explicit statement of what was not verified.

## 5. Decision rules and evidence standard

- **Evidence, not assertion.** "Tests pass" requires a CI run ID; "tested locally" is not readiness evidence for a production release.
- **NO-GO on any of:** failing required checks, unreviewed breaking change, untested irreversible migration, missing rollback, artifact not traceable to a commit.
- **Flaky tests are a no-go for the affected area.** A green run after three reds proves nothing.
- **Conditions must be checkable within the release window**, otherwise they are wishes.
- **Do not release on Friday afternoon** unless the team has declared on-call coverage; record the operational assumption either way.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Artifact traceable | compare digest/hash with CI build | matches commit |
| Gates run | CI records cited | all required checks green |
| Compatibility classified | inspect | every surface addressed |
| Prerequisites verified | env/config check | all present |
| Rollback viable | artifact + migration review | both confirmed |
| Verdict consistent | inspect | verdict matches checklist |

## 7. Failure handling

- **CI unavailable** → release is NO-GO for production; local evidence may support a pre-release/alpha with stated limits.
- **Unknown breaking change** → treat as breaking until proven otherwise; require a compatibility check or a deprecation path.
- **Migration irreversible** → NO-GO until expand/contract is applied or a verified backup and restore procedure is tested.
- **Time pressure** → reduce scope (release fewer commits), never reduce verification. A smaller release with the same gates is the correct response.

## 8. Security and authorisation

Risk class B: readiness documents. Do not deploy, publish, tag the release, or modify the deployment environment. Do not print secrets while verifying configuration — check presence by name only.

## 9. Completion criteria

- [ ] Commit, version, and artifact identified and traceable.
- [ ] Automated gates recorded with run references.
- [ ] Compatibility classified across all consumer surfaces.
- [ ] Operational prerequisites verified.
- [ ] Observability for new failure modes confirmed.
- [ ] Rollback viability confirmed.
- [ ] Risk assessed (blast radius, reversibility, novelty).
- [ ] Verdict with verifiable conditions.
- [ ] Unverified items stated.

## 10. Deliverables and handover

Artifact: `RELEASE_READINESS.md` with verdict.

P02 receives: the commit range and compatibility classification, which determine the version bump and the changelog's breaking-change section. P03 receives: the risk class and rollback requirements.
