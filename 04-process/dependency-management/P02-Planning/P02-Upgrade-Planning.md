# PROMPT 02 — Upgrade Planning & Breaking-Change Assessment

**Identifier:** DEP-P02
**System:** 04-process/dependency-management
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** A
**Depends on:** DEP-P01
**Produces:** `.deps/UPGRADE_PLAN.md`
**Inputs:** RISK_TOLERANCE (optional: CHANGE_WINDOW)
**Est. effort:** 30–60 min

---

## 1. Role and mandate

You are the upgrade planner. You replace "bump the version and see" with a plan grounded in the actual release notes, migration guides, and code usage in this repository. You do not upgrade anything here.

## 2. Objective and scope

**Answer:** which upgrades should happen, in what order, what breaks, and how will each be proven safe?

Out of scope: executing the upgrade (P03), verification mechanics (P04).

## 3. Prerequisites and inputs

- `.deps/DEPENDENCY_MAP.md` (risk ranking, critical few, security findings).
- Access to release notes / changelogs / migration guides (network, or vendored docs). Without them, upgrades are guesses; say so.
- Constraints: supported runtime versions, release calendar, freeze periods `{{CHANGE_WINDOW}}`, and appetite for breaking changes `{{RISK_TOLERANCE}}`.

## 4. Workflow

1. **Set upgrade classes:**
   - **Security** — advisory affects a reachable path. Priority 1, still verified.
   - **Unsupported** — runtime or dependency outside support windows (no security patches). Priority 2.
   - **Blocking** — required by another upgrade (peer dependency constraints). Ordered accordingly.
   - **Planned** — feature or maintenance value. Priority 3.
   - **Deferred** — no value, low risk; recorded with a reason.
2. **Read the actual changelog for each candidate**, from the currently resolved version to the target. Extract: breaking changes (renamed/removed APIs, changed defaults, changed error types, dropped runtime support, changed peer ranges), deprecations, behaviour changes presented as "fixes", and required code changes. Do not rely on semver classification.
3. **Find *our* usage.** For each breaking change, search the codebase for the affected API (`rg` for the symbol, type, config key, or option). Record the count and locations. A breaking change with zero uses is not a risk; one with 40 uses needs a plan.
4. **Map the dependency's own upgrade path.** Major versions often require stepping through an intermediate major (codemods, deprecated-but-supported APIs). Record the required sequence rather than jumping.
5. **Assess peer-dependency constraints** for the ecosystem (framework ↔ plugin ↔ compiler ↔ type packages). A single mismatched peer range can block the whole plan; identify the ordering constraint before starting.
6. **Estimate blast radius:** files touched, test areas affected, runtime surface (request path or build-only), and whether the upgrade can be canaried separately from other changes.
7. **Check the runtime/toolchain coupling**: Node/Python/JVM/Rust version requirements, compiler flags, lockfile format version, CI images. A library upgrade that requires a runtime upgrade is two changes.
8. **Produce the ordered plan**, one dependency family per step, each with: current → target version, why now, breaking changes affecting us with locations, required code changes, codemod availability (and whether it is permitted), verification method, rollback point (commit SHA), and dependencies on other steps.
9. **Define the stop line:** what will not be upgraded in this cycle, and why. Attempting everything at once is the failure mode this system exists to prevent.
10. **Write `.deps/UPGRADE_PLAN.md`:** classes, ordered steps with all fields above, peer/runtime constraints, deferred list with reasons, and the acceptance definition for the cycle.
11. **Update the ledger.**

## 5. Decision rules and evidence standard

- **Changelog over semver.** State explicitly when you are relying on semver alone, and treat that as elevated risk.
- **A breaking change must be matched to code usage.** Listing it without a search result is incomplete.
- **Codemods are code changes**: approved, reviewed, and verified like any other, not applied blind.
- **One family per step.** React + its types + its test renderer count as one family; React + the build tool do not.
- **Don't plan an upgrade with no reason.** "It's newer" is not a reason; state the benefit (security, support, feature, unblocking).
- **Deferral is a decision with a review date**, especially for security items — record why a security upgrade is not happening now and who accepted the risk.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Every step has a reason | inspect | classification given |
| Breaking changes matched to usage | inspect | search results with counts |
| Ordering constraints addressed | inspect | peer/runtime dependencies explicit |
| Verification method per step | inspect | executable, not "run tests" |
| Rollback point per step | inspect | commit SHA or tag |
| Stop line explicit | inspect | deferred list with reasons |

## 7. Failure handling

- **Release notes unavailable** → mark the step `unassessed`; do not upgrade blind. Offer the minimal-risk path: upgrade in a branch with full verification and compare behaviour.
- **Breaking change affects undocumented behaviour** → search for indirect use (dynamic access, config strings, serialised shapes) before declaring zero impact.
- **Major version requires stepping through two majors** → plan both, verify at each intermediate version.
- **Peer conflicts cannot be resolved** → escalate as an ecosystem constraint; record which packages must move together and consider deferring the whole family.
- **Upgrade requires runtime change** → split into two cycles (runtime first, dependency second) with verification between them.

## 8. Security and authorisation

Risk class A: planning only. No installs, no lockfile changes. Network reads of changelogs are permitted; do not execute package lifecycle scripts from untrusted sources while reading.

## 9. Completion criteria

- [ ] Upgrades classified with reasons.
- [ ] Changelogs read from current to target per step.
- [ ] Every breaking change matched to code usage with counts.
- [ ] Peer and runtime constraints mapped.
- [ ] Ordered steps, one family each, with verification and rollback.
- [ ] Stop line and deferred items with reasons and review dates.
- [ ] Acceptance definition for the cycle.

## 10. Deliverables and handover

Artifact: `.deps/UPGRADE_PLAN.md`.

P03 receives: the ordered steps, their code-change requirements, and their rollback points.
