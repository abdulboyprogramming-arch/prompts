# PROMPT 01 — Monorepo Health: builds, boundaries, and ownership

**Identifier:** MONO-01
**System:** 05-scenarios/monorepo
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** audit-remediation
**Risk class:** B (changes build configuration and package boundaries; publishing is C)
**Depends on:** none
**Produces:** `MONOREPO_AUDIT.md`, a boundary map, a CI plan
**Inputs:** REPO_PATH, TOOLING (optional: PACKAGE_COUNT, CI_MINUTES, APPROVER)
**Est. effort:** 3–6 h

---

## 1. Role and mandate

You find why this monorepo is slow, fragile, or quietly coupled — and you fix the structure rather than the symptoms.

The three failures are distinct and often confused. **Slow:** every change rebuilds and retests the world. **Fragile:** a change in one package breaks another that nobody knew depended on it. **Coupled:** packages import each other's internals, share global state, or deploy only together, so the "monorepo" is one application wearing many folders.

## 2. Objective and scope

**Produce:** a package graph with real dependencies (not declared ones), a boundary violation register, an affected-only build/test plan, and an ownership map.

Out of scope: migrating between monorepo tools, and publishing strategy for external consumers (`04-process/release-engineering/`).

## 3. Prerequisites and inputs

- `{{REPO_PATH}}` with the workspace configuration and package manifests.
- `{{TOOLING}}` — pnpm/npm/yarn workspaces, Nx, Turborepo, Bazel, Rush, Cargo, Go modules; each detects "affected" differently and each can be defeated by the same mistakes.
- `{{PACKAGE_COUNT}}`, `{{CI_MINUTES}}` — to size the problem and the win.
- `{{APPROVER}}` — for changes that alter package boundaries.

## 4. Workflow

1. **Build the real dependency graph** from imports, not from manifests. Declared dependencies drift: packages import from siblings they never declared (workspace hoisting hides it), and declare dependencies they no longer use.

2. **Find the boundary violations**, which are the reason the graph is not a DAG in practice:
   - deep imports into another package's internals (`@scope/ui/src/internal/...`);
   - circular dependencies between packages;
   - shared global singletons (a config module, an event bus, a database client) that make every package implicitly global;
   - a "common"/"utils" package that everything imports and that imports nothing — the classic future God package.

3. **Check the build graph**: are tasks declared with inputs and outputs, so caching is possible? A task with no declared inputs cannot be cached and will always run. A task with declared outputs that are not reproducible (timestamps, absolute paths) produces cache misses that look like cache failures.

4. **Verify affected-only actually works**: change one leaf package and confirm that only its dependents build and test. If the whole repo runs, either the graph is wrong or a shared input (lockfile, root config, environment variable) is invalidating everything.

5. **Measure where CI time goes**: install, build, test, lint, e2e — by package. Most monorepo pain is one of these four, and the fix differs. Remote caching helps build+test; dependency pruning helps install; test sharding helps e2e.

6. **Check versioning and publishing coherence**: fixed (all packages share a version) versus independent. Mixed strategies produce version skew that consumers discover at install time. Internal ranges (workspace protocol versus a caret range) decide whether a published package references a version that exists.

7. **Check ownership**: `CODEOWNERS` or equivalent per package, and whether an uncontested package has no owner. Unowned packages accumulate the changes nobody reviews properly.

8. **Check the shared configuration trap**: one root `tsconfig`/`eslint`/`babel` config that every package extends means a root change invalidates every cache entry. That is sometimes correct; it should be a decision, not an accident.

9. **Look for the integration risk**: packages that must deploy together but are versioned separately; contracts duplicated across packages instead of imported from one source; and environment variables read by many packages with different defaults.

10. **Write `MONOREPO_AUDIT.md`**: package graph with violations, build-graph fixes, affected-only evidence, CI time breakdown with interventions ranked by minutes saved, ownership map, and the boundary rules adopted.

## 5. Decision rules and evidence standard

- **The import graph is the truth**; manifests are intentions.
- **Deep imports are boundary violations**, even when they compile.
- **A task without declared inputs cannot be cached**; caching failures are usually configuration.
- **Affected-only must be demonstrated**, not assumed — change a leaf and count what ran.
- **One source of truth per contract** (types, schemas, constants), imported rather than copied.
- **Every package has an owner**, or it has nobody.
- **Shared root config is a cache decision**, and should be made deliberately.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Real graph | Import analysis | Declared and actual dependencies compared |
| Violations listed | Graph output | Deep imports, cycles, globals enumerated |
| DAG | Cycle check | No cycles, or each documented with a removal plan |
| Task inputs/outputs | Tool config | Every cacheable task declares both |
| Affected-only | Leaf change | Only dependents build and test |
| Cache correctness | Two identical runs | Second run is a cache hit |
| CI breakdown | Timings per stage | Ranked, with the top cost identified |
| Versioning coherence | Manifest review | One strategy; internal ranges resolvable |
| Ownership | CODEOWNERS | Every package has an owner |
| Contract duplication | Search | No copied type or schema definitions |

## 7. Failure handling

- **Affected detection does not work** → check that the tool reads the real graph and that no root file is a blanket input; a root `.env` or lockfile in every task's inputs defeats it.
- **The dependency graph has cycles** → break them by extracting the shared piece into a new leaf package or by inverting the dependency; suppressing the warning is not a fix.
- **CI is slow because install is slow** → prune to the workspace subset, cache the store, and pin one package manager version.
- **A shared package is imported by everything and changes constantly** → split it by stability: stable primitives (rarely change) apart from convenience helpers (change often), so the cache invalidates narrowly.
- **Publishing is broken by version skew** → verify that every published package's internal ranges resolve to published versions; a package referencing an unpublished sibling fails only for consumers.
- **Teams want to split the repo** → state the actual problem (CI time, ownership, release cadence, access control) and whether a monorepo fix is cheaper; splitting is a migration, not a cleanup.

## 8. Security and authorisation

Risk class B. Workspace hoisting can install packages the manifest never declared — pin and audit at the lockfile level (`04-process/dependency-management/`). Shared CI caches can leak between branches and, in some configurations, between repositories: scope them. Publishing credentials belong to CI, not to developers' machines.

## 9. Completion criteria

- [ ] Real dependency graph built from imports and diffed against manifests.
- [ ] Boundary violations enumerated, including deep imports and globals.
- [ ] No dependency cycles, or each documented with a removal plan.
- [ ] Cacheable tasks declare inputs and outputs; cache hits verified.
- [ ] Affected-only demonstrated by a leaf change.
- [ ] CI time broken down and interventions ranked.
- [ ] Versioning strategy single and coherent; internal ranges resolvable.
- [ ] Every package has an owner.
- [ ] Contracts imported from one source, not duplicated.
- [ ] Boundary rules written down.

## 10. Deliverables and handover

Artifacts: `MONOREPO_AUDIT.md`, dependency graph, CI plan.

Handover: `04-process/release-engineering/` consumes the versioning decision; `03-domains/dependency-management` refs (`04-process/dependency-management/`) handles upgrades across the graph; `04-process/code-review/` uses the boundary rules as review criteria; `02-engineering/architecture-review/` takes any structural change that crosses package ownership.
