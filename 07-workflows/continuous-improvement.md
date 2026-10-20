# Workflow — Continuous Improvement

**Identifier:** WF-IMPROVE
**System:** 07-workflows
**Version:** 1.0.0
**Maturity:** draft
**Execution mode:** continuous-improvement
**Risk class:** B
**Depends on:** `04-process/systems-building-improvement/`, `02-engineering/performance/`, `04-process/testing-qa/`
**Produces:** a measured improvement cycle with a new baseline

---

## When to use this

Nothing is on fire. The project works, but velocity, quality, or cost is drifting, and "we should improve things" has produced no durable change. This workflow replaces intention with a cycle that has a baseline, a hypothesis, and a measurement.

## The cycle

| # | Step | Prompt / method | Output |
|---|------|-----------------|--------|
| 1 | Baseline | this workflow | `IMPROVEMENT_BASELINE.md` |
| 2 | Find the constraint | `systems-building-improvement/` P02–P04 | constraint statement with evidence |
| 3 | Choose one change | P05 + prioritisation | one hypothesis, one owner, one metric |
| 4 | Design the experiment | P05, `04-process/research-and-development/` P04 | expected effect, measurement method, stop condition |
| 5 | Implement narrowly | relevant system prompt | branch commit |
| 6 | Measure | P07 | before/after with the same method |
| 7 | Keep, adjust, or revert | this workflow | decision recorded |
| 8 | Update baseline | this workflow | new baseline; return to 2 |

## Rules that make the cycle work

1. **One change at a time per metric.** Improvements that bundle three changes cannot be evaluated, so no one learns anything.
2. **Measure with the same method before and after.** Changing the measurement invalidates the comparison.
3. **Baseline must be repeatable** — record the command, the environment, and the variance. A single noisy sample is not a baseline.
4. **Define revert criteria in advance.** "If p95 does not improve by 10% within a week, revert." Without it, every change becomes permanent by inertia.
5. **A failed experiment is a successful cycle.** Record what was learned; do not repeat the same hypothesis.
6. **Cap work in progress.** Two concurrent improvement efforts per team is the practical maximum; more is usually avoidance of a harder constraint.

## Choosing the constraint

Look for the thing that makes everything else slower or riskier:

| Symptom | Likely constraint | System |
|---------|-------------------|--------|
| Every change is scary | missing regression tests | `04-process/testing-qa/` |
| Changes take days to reach users | pipeline and release process | `04-process/release-engineering/` |
| Only one person understands the system | knowledge concentration, poor structure | `02-engineering/refactoring/`, `04-process/documentation/` |
| Slow pages / high cost | performance, queries, bundle | `02-engineering/performance/` |
| Incidents recur | observability and follow-through | `04-process/observability-reliability/` |
| Repeated rework | requirements/ambiguity | `04-process/project-management/`, feature design |

Do not pick a constraint because it is pleasant to work on.

## Gates

- **GATE 1 — baseline accepted.** Human confirms the baseline and metric are meaningful for the business, not just technically convenient.
- **GATE 2 — keep/revert.** a human decision, informed by the measurement, not by sunk cost.

## Failure handling

- **Baseline cannot be established** → the cycle cannot start; name the measurement gap as the first improvement item.
- **Measurement contradicts expectation** → report the measurement, not the expectation; do not re-measure until the number is acceptable.
- **Change cannot be isolated** (bundled with other work) → postpone the measurement to the next clean change; record that this cycle is unmeasured.
- **Revert required** → revert the change, keep the measurement, and record the hypothesis as falsified.
- **Cycle abandoned mid-way** → record the baseline and the change state so the next cycle does not repeat the experiment blindly.

## Completion criteria for the cycle

1. Baseline exists with method, environment, and variance.
2. The change is traceable to the constraint and to a hypothesis.
3. Measurement uses the same method, with a stated observation window.
4. Decision (keep/adjust/revert) recorded with reasoning.
5. Baseline updated; next constraint identified.
6. Nothing else changed simultaneously with the measured change.

## Anti-patterns

- "Modernisation" programmes with no metric.
- Measuring developer sentiment as a proxy for throughput and calling it done.
- Reverting only when the change breaks something visible, never when it fails to help.
- Improvement work that is never scheduled because feature work always wins — make the cycle time-boxed and visible.
