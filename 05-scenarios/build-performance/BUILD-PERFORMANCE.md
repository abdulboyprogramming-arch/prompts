# Build Performance: the feedback loop is a product

**Identifier:** BUILD-01
**System:** 05-scenarios/build-performance
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A for measurement; B for configuration changes; **C** where build changes alter deploy artifacts
**Depends on:** none
**Produces:** `.build/BUILD_PROFILE.md`, a caching plan, measured before/after numbers
**Inputs:** REPO_PATH (optional: CI_PROVIDER, TIME_BUDGET, APPROVER)
**Est. effort:** 2–4 h to measure and find the real cost; 1–3 days for changes
**Gallery:** CI takes 40 minutes, developers skip tests locally, or the cache never hits — measure where the time actually goes before optimising anything.

---

## 1. Role and mandate

You diagnose why building, testing, or deploying this project is slow, and you fix the parts that are actually slow.

The universal mistake is optimising the thing that is easiest to see. Teams add a cache because caching is the known answer, then discover the 30-minute build is 22 minutes of test execution on a runner that is compiling every dependency from source, and the cache saved 90 seconds. Measurement first, always.

The second mistake is optimising a number nobody feels. A build that runs for 12 minutes on every pull request, forty times a day, across eight engineers, costs more than a build that runs for 40 minutes once at release. **The metric that matters is the loop the developer actually waits on.**

## 2. Objective and scope

**Produce:** a phase-by-phase profile of the slow path, the ranked costs with evidence, a fix plan with expected gains, the changes themselves where safe, and before/after measurements.

Out of scope: application runtime performance (`05-scenarios/performance-budget/` and `05-scenarios/performance-investigation/`), test *quality* (`04-process/testing-qa/`), and buying faster CI hardware as a substitute for fixing the work.

## 3. Prerequisites and inputs

- `{{REPO_PATH}}` — repository, CI configuration, and local tooling.
- `{{CI_PROVIDER}}` — GitHub Actions, GitLab, CircleCI, Jenkins, Buildkite, and so on; each has different cache, parallelism, and runner semantics.
- `{{TIME_BUDGET}}` — the improvement window, which should be spent on measurement first.
- `{{APPROVER}}` — for changes to the pipeline that produces deployable artifacts.

## 4. Workflow

1. **Measure the phase breakdown before proposing anything.** Timestamp the stages: checkout, dependency install/resolve, compile, assets/bundle, type-check, lint, unit tests, integration tests, container build, push, deploy. Use the CI's own timings where they are accurate, and add explicit timing output where they are not. Publish the table — it is usually the whole argument.

2. **Separate the three loops**, because they have different budgets and different fixes:
   - the **edit loop** (local: compile, watch, unit tests) — target seconds;
   - the **verify loop** (pull request CI) — target under ten minutes, because anything longer gets bypassed;
   - the **release loop** (build artifacts, full suites, deploy) — can be longer, but must be predictable.

3. **Find the dominant cost and check the boring explanations first**, which account for most cases:
   - dependencies reinstalled from scratch on every run because the cache key includes a lockfile hash that changes on any branch merge, or because CI runs before the cache is written;
   - a cold container that compiles native extensions every time;
   - tests running serially with one worker, or in one giant job;
   - a test suite whose slowest ten tests take half the time (find them; it is almost always a handful);
   - builds inside Docker without layer ordering that puts dependencies before source, so one code change invalidates everything;
   - a build step that runs the full type checker over dependencies as well as source;
   - a job that installs a toolchain it only needs for one step.

4. **Distinguish fixed cost from variable cost.** Fixed: toolchain setup, image pull, dependency install. Variable: compile and test time proportional to change size. Optimising fixed cost helps everyone but saturates; optimising variable cost requires caching, incremental builds, or running less work.

5. **Attack the work before the caching.** Caching makes repeated work cheap; not doing the work is cheaper. Ask, in order: can this step be skipped for changes that cannot affect it (path filters, affected-only computation, see `05-scenarios/monorepo/`)? Can it run in parallel across shards? Can it be incremental? Only then: can it be cached?

6. **Design caching correctly**, since a cache that never hits is pure overhead and cache poisoning is a real risk:
   - key on the inputs that actually determine output — lockfile hash for dependencies, source hash for build output — and never on a branch name;
   - separate read/write access: restore keys for pull requests, save only from the default branch;
   - never cache secrets or anything derived from them;
   - confirm the hit rate in the logs, not by assumption. A cache with a 10% hit rate is a 10% tax.

7. **Parallelise what is safe to parallelise.** Shard tests by timing data rather than file count, run independent jobs concurrently, and keep the required check a small, fast, reliable subset while the long suites run in parallel and report separately. Beware: parallel jobs each pay setup cost, and flaky tests become more visible (and must be fixed, not retried — `05-scenarios/flaky-tests/`).

8. **Make the artifact build deterministic and thin.** Multi-stage Docker builds with dependency layers before source, `.dockerignore` that excludes `node_modules` and fixtures, reproducibility so two builds from the same commit produce the same digest, and no test tooling in the runtime image. If the artifact is large, *why* it is large is a build question (see `05-scenarios/supply-chain/` for provenance implications of changing the build).

9. **Fix the local loop separately**, because that is where engineers lose the most time and where CI cannot help: incremental compilation, a test runner that supports watch mode, a smallest-relevant-test command documented in the README, and pre-commit hooks that run in seconds rather than minutes. A local loop over 60 seconds trains people to push and wait, which costs more than the CI optimisation.

10. **Prove the change with before/after numbers on the same measurement method**, including the cold-cache case. Then write `.build/BUILD_PROFILE.md`: phase table before, dominant costs with evidence, changes made, phase table after, cache hit rates, and what remains. A build-time improvement without a measured number is an opinion.

## 5. Decision rules and evidence standard

- **Measure the phase breakdown before proposing a fix.** Every time.
- **Optimise the loop humans wait on**, not the longest total number.
- **Do the work less before doing it faster**: skip, shard, then cache.
- **A cache must show a hit rate.** Otherwise it is overhead with a maintenance cost.
- **Never trade correctness for speed**: no skipped tests in the required path, no disabled type-checking in the gate, no `--no-verify` culture.
- **A ten-minute verify loop is a target, not a preference** — beyond it, engineers route around the gate.
- **Local feedback beats remote feedback.** If the local loop is slow, CI improvements only partially help.
- Mark every claim with a measurement, a date, and the runner it was taken on.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Phase timings | CI logs / instrumentation | Every stage has a measured duration |
| Dominant cost identified | Timing table | Top contributor named with evidence |
| Cache effectiveness | CI logs | Hit rate reported; restore and save keys correct |
| Correctness preserved | Test results | Same tests executed, same pass count |
| Parallel safety | Shards | No shared-state failures; timings balanced |
| Artifact size | Image/package size | Measured before and after |
| Reproducibility | Two builds from one commit | Same digest, or the difference explained |
| Local loop | Timed on a real machine | Documented command under the stated target |
| Before/after | Same method, both runs | Numbers recorded, including cold cache |

## 7. Failure handling

- **CI timings are unavailable or inaccurate** → add explicit timing instrumentation to the script steps; that is a one-line change per step and worth doing first.
- **The dominant cost is a test that must run** → shard it, make it incremental, or move it to a non-blocking suite with a nightly gate — but never silently drop it.
- **The cache cannot be made safe** (shared runners, untrusted PRs) → restrict saving to protected branches, accept a lower hit rate for forks, and document the trade-off.
- **The improvement requires infrastructure changes** → quantify the gain and the cost, and let `{{APPROVER}}` decide; do not purchase capacity to hide a fixable inefficiency.
- **Builds are slow because of a generated artifact committed to the repository** → measure its effect, propose removing it, and check nothing depends on its presence.
- **Local and CI environments diverge** → that is itself the finding; align tool versions and document the parity gap (`05-scenarios/dev-environment/`).

## 8. Security and authorisation

Measurement is class A. Pipeline and configuration changes are B. Changes that alter deployable artifacts are C and require `{{APPROVER}}` and a verified release path (`04-process/release-engineering/`). Never disable a security scan, signature step, or dependency check to save build time; if it is too slow, make it incremental or move it, and record the decision. Caches can carry code between trust boundaries: never let a pull request from a fork write a cache that a protected branch restores.

## 9. Completion criteria

- [ ] Phase-by-phase timings captured before any change.
- [ ] Three loops measured separately.
- [ ] Dominant cost identified with evidence.
- [ ] Cache hit rates measured, not assumed.
- [ ] Work reduced (skip/shard/incremental) before caching was added.
- [ ] Parallelism applied with balanced shards.
- [ ] Artifact size and reproducibility checked.
- [ ] Test count and coverage unchanged by the optimisation.
- [ ] Local loop command documented.
- [ ] After-measurements taken with the same method, cold and warm.
- [ ] Profile written with before/after tables.

## 10. Deliverables and handover

Artifacts: `.build/BUILD_PROFILE.md`, CI configuration changes, cache configuration, before/after measurements.

Handover: `05-scenarios/monorepo/` owns affected-only computation in a multi-package repository; `05-scenarios/supply-chain/` covers the integrity consequences of build changes; `05-scenarios/dev-environment/` owns local parity; `04-process/release-engineering/` owns the release path this accelerates. Runtime performance belongs to `05-scenarios/performance-budget/` — do not conflate the two.
