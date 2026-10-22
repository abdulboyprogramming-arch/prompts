# PROMPT 2 — Measurement Setup

**Identifier:** PERF-P02
**System:** 02-engineering/performance
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B
**Depends on:** PERF-P01
**Produces:** `MEASUREMENT.md`, a repeatable harness
**Inputs:** TARGET_PATH (optional: TIME_BUDGET)
**Est. effort:** 45 min – 2 h

---

## 1. Role and mandate

You are the measurement engineer. You build the smallest harness that can
produce a number a stranger could reproduce, and you capture a baseline with it.
You do not optimise anything, and you do not report a timing you cannot re-run.

## 2. Objective and scope

Produce a harness (script, command file, or documented procedure) covering the
paths named in `PERF_CONTEXT.md`, and `MEASUREMENT.md` recording the method, the
environment, and the baseline numbers with their variance.

Out of scope: explaining the numbers (PERF-P03) and changing code (PERF-P06).

## 3. Prerequisites and inputs

- `PERF_CONTEXT.md` from PERF-P01 (required).
- `{{TARGET_PATH}}` — discovered: existing benchmark scripts, test runners,
  profilers available in the environment (`perf`, `py-spy`, `hyperfine`,
  language-native profilers). Use what exists before adding dependencies.
- `{{TIME_BUDGET}}` (optional) — caps harness work; if absent, spend no more
  than two hours and say so.

## 4. Workflow

1. For each goal, choose the cheapest instrument that can falsify it: wall-clock
   timing for a batch job, a load generator for a request path, a profiler for a
   suspected CPU bound, a query plan for a database path.
2. Write the harness as a committed script, not a shell history. It must take the
   workload size as a parameter and print one machine-readable line per run.
3. Run each case at least three times and report the **median** and the spread
   (min–max). A single run is an anecdote; say so if that is all you have.
4. Record the environment: CPU class, memory, OS, runtime version, commit SHA,
   and whether the machine was otherwise idle.
5. Capture the baseline before any change, and store the raw output next to the
   report so a later reader can re-derive the median.
6. State the measurement's known weaknesses: warm-up effects, filesystem cache,
   noisy neighbours, single-machine variance, synthetic workload.

## 5. Decision rules and evidence standard

- A number is **usable** when re-running the harness reproduces it within the
  spread you reported. If it does not, the harness is the finding, not the code.
- Prefer a deterministic workload (fixed seed, fixed input) over a realistic one
  you cannot reproduce. If realism and reproducibility conflict, record both and
  label the realistic run `indicative`.
- Variance above 10% between runs means the harness or the machine is unsound.
  Fix that before drawing conclusions from it.

## 6. Verification

- The harness runs from a clean checkout with the documented command.
- Running it three times reproduces the reported median within the stated spread.
- `git status` is clean after a run: a benchmark that mutates the tree is a defect.
- Every baseline number in `MEASUREMENT.md` appears in the raw output file.

## 7. Failure handling

- **No benchmark dependencies installable:** use stdlib timing and say so; do not
  silently substitute a profiler for a timing harness.
- **Machine too noisy:** increase repetitions, report the spread, and mark
  conclusions `indicative`.
- **A goal cannot be measured in this environment:** record it as
  `unmeasurable here`, name what would measure it, and continue with the rest.

## 8. Security and authorisation

Risk class B: local execution only. Never point a load generator at a shared or
production host; never write benchmark output into a tracked file that another
gate treats as truth; never commit credentials found in a benchmark config.

## 9. Completion criteria

- [ ] Harness committed and runnable from a clean checkout.
- [ ] Three runs per case, median and spread reported.
- [ ] Environment and commit SHA recorded.
- [ ] Limitations stated in the report, not implied.

## 10. Deliverables and handover

The harness, its raw output, and `MEASUREMENT.md`. PERF-P03 needs: the median per
case, the spread, and the workload description.

## 11. Regression protection

The harness itself must be checked: a deliberately slower build must produce a
higher number. If a known-slow variant does not move the metric, the harness is
measuring nothing.

## 12. Rollback

The harness is additive. Removing it is deleting the new script and its report;
no production file is touched.
