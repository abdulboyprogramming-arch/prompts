# PROMPT 01 — Performance Budgets and Core Web Vitals

**Identifier:** PERF-BUDGET-01
**System:** 05-scenarios/performance-budget
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B (changes build config and CI; no production mutation)
**Depends on:** none
**Produces:** `.perf/BUDGET.md`, a CI gate, a baseline report
**Inputs:** TARGET_URL, SURFACES (optional: DEVICE_CLASS, NETWORK_PROFILE, BUDGETS, TARGET_ENV)
**Est. effort:** 2–4 h

---

## 1. Role and mandate

You turn "the site feels slow" into a number that fails a build.

Performance work fails for a structural reason: it has no owner, no target, and no gate. Everyone agrees it matters; nobody can say what "fast enough" means; regressions arrive one 40 KB dependency at a time; and by the time it is a problem, the fix is a redesign.

A budget changes the economics. It is a number, checked automatically, that a change must not exceed — and when it is exceeded, the change that crossed it is the one that fixes it.

## 2. Objective and scope

**Produce:** measured baselines for the chosen metrics, budgets derived from user-perceptible thresholds, CI gates that block regressions, and a remediation list for what already exceeds them.

Out of scope: deep application profiling (see `05-scenarios/performance-investigation/`) and infrastructure capacity planning.

## 3. Prerequisites and inputs

- `{{TARGET_URL}}` — a production-like URL, not localhost; `{{SURFACES}}` — the pages that matter (landing, search, checkout, dashboard), because a budget on the homepage alone is decoration.
- `{{DEVICE_CLASS}}` and `{{NETWORK_PROFILE}}` — a mid-tier mobile device on a throttled connection is the honest baseline; a desktop on fibre is the flattering one.
- `{{BUDGETS}}` — any existing targets; `{{TARGET_ENV}}` — staging must be representative, or the numbers are fiction.

## 4. Workflow

1. **Baseline before budget.** Measure LCP, INP, CLS, TTFB, and total transfer size on `{{SURFACES}}` at p75 (not average), on the stated device and network profile, over several runs. Record variance; a single run is noise.

2. **Set budgets from user-perceptible thresholds**, not from current performance: LCP under 2.5 s, INP under 200 ms, CLS under 0.1 at p75 are the field-standard "good" boundaries. Then set a **regression ceiling** at the current measured value plus a small allowance, so the gate stops the next regression while the existing debt is paid down separately.

3. **Budget the causes, not only the symptoms**: JavaScript bundle size per route, total bytes, number of requests, font files, and third-party script count. Symptom metrics move slowly and noisily; a bundle-size check fails in seconds and points at the commit.

4. **Make the gate deterministic**: run in CI on a fixed profile with a warm cache policy stated, compare against the committed budget file, and fail with the delta and the offending route. Flaky measurements will be disabled by the team within a week — a noisy gate is worse than none.

5. **Attribute every regression to a change**: include the built bundle sizes per route in the pull request, so the reviewer sees "+38 KB on /checkout" rather than discovering it in a monthly report.

6. **Fix the highest-leverage item first**, in this order: bytes shipped (remove, split, defer), render-blocking resources, image dimensions and formats, font loading strategy, and only then micro-optimisations. A 200 KB dependency removed beats a week of memoisation.

7. **Distinguish lab from field.** Lab numbers (Lighthouse) are reproducible and gameable; field data (RUM, CrUX) is real and sampled. Use lab for the gate and field for the truth, and state both.

8. **Handle the third-party budget separately**: analytics, chat widgets, A/B tools, and payment iframes are usually the largest uncontrolled cost. Give them a byte and main-thread-time budget, load them after interaction where possible, and make adding one a reviewed decision.

9. **Budget the mobile app too** if applicable: startup time, binary size, and memory; the same discipline, different metrics.

10. **Write `.perf/BUDGET.md`**: surfaces, metrics, budgets, the device/network profile, the CI gate and how to change a budget deliberately, current baseline versus budget, and the remediation list with owners.

## 5. Decision rules and evidence standard

- **p75, not average** — the average hides the users who leave.
- **Mid-tier mobile on a throttled network is the baseline.**
- **Budgets come from user-perceptible thresholds**, with a separate regression ceiling for existing debt.
- **A gate must be deterministic** or it will be removed.
- **Bytes before milliseconds**: shipping less is the only reliable optimisation.
- **Third parties get a budget too**, or they will consume the whole thing.
- **Lab gates the build; field tells the truth.**

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Baseline measured | Repeated runs | p75 per metric per surface, variance noted |
| Budgets documented | File | Numbers with their source and rationale |
| Regression ceiling | File | Separate from the aspirational target |
| CI gate | Pipeline | Fails on a deliberate +50 KB regression |
| Determinism | Three consecutive runs | Same verdict each time |
| Attribution | PR output | Per-route size delta shown |
| Third-party budget | Config | Count and bytes capped |
| Lab vs field | Report | Both reported, difference explained |
| Remediation list | Document | Items ranked by leverage, with owners |

## 7. Failure handling

- **CI measurements are flaky** → pin the environment, run the same profile, average three runs, and gate on the median; if still noisy, gate on bundle size only and keep the metric report advisory.
- **The baseline is already far over budget** → split the budget into "must not regress" (today's number) and "target" (the goal), and fund the gap as work; a gate that is red from day one gets disabled.
- **A third-party script is the problem** → load on interaction, self-host where licence permits, or remove it; the vendor's own performance claim is marketing.
- **Staging is not representative** (different CDN, no cache) → measure production reads via RUM, and keep the CI gate relative rather than absolute.
- **The team wants to raise a budget to pass** → make it an explicit, reviewed change with a reason and a compensating improvement; the diff is the audit trail.
- **Metrics improve but users still complain** → check the interaction path (INP) and the first-load experience on a cold cache; LCP alone does not capture "clicking does nothing".

## 8. Security and authorisation

Risk class B: build configuration and CI. Measurement must not send real user data to third parties; RUM should be sampled and anonymised. Do not add a performance vendor's script to fix performance measurement — that is the failure mode being audited.

## 9. Completion criteria

- [ ] Baseline at p75 per surface, device, and network profile, with variance.
- [ ] Budgets documented with thresholds and rationale.
- [ ] Separate regression ceiling for existing debt.
- [ ] CI gate that fails a deliberate regression, deterministically.
- [ ] Per-route size deltas posted on pull requests.
- [ ] Third-party budget defined and enforced.
- [ ] Lab and field data both reported.
- [ ] Remediation list ranked by leverage with owners.
- [ ] Process for changing a budget deliberately, with review.

## 10. Deliverables and handover

Artifacts: `.perf/BUDGET.md`, CI gate, baseline report.

Handover: `05-scenarios/performance-investigation/` handles a specific unexplained slowdown; `03-domains/frontend/` (skeleton) owns the implementation techniques; `04-process/release-engineering/` adds the budget check to release readiness; `03-domains/cost-engineering/` benefits directly, because bytes shipped and egress are the same number viewed from two angles.
