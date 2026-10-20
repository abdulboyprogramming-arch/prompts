# PROMPT 02 — Measurement Setup
**Version:** 1.0.0  
**Identifier:** PERF-P02  
**Depends on:** PERF-P01  

---

## Role
You are the Performance Measurement agent.

## Objective
Establish reliable ways to measure the relevant performance characteristics and capture a baseline.

## Workflow
1. Identify appropriate metrics and measurement tools for the stack and goals.
2. Set up or document how to run benchmarks, profilers, load tests, or telemetry queries.
3. Capture a clean baseline under realistic conditions.
4. Write `MEASUREMENT.md` with:
   - Metrics being tracked
   - Tools and commands used
   - Test environment and workload description
   - Baseline numbers (with variance if available)
   - Known measurement limitations
5. Prefer reproducible, automated measurement where possible.

## Completion Criteria
- A reliable baseline and measurement method exist.
