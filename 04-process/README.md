# 04-Process

Engineering process as procedure: how work is verified, reviewed, released, operated, and communicated.

## Systems

| Path | Description | Stages | Maturity |
|------|-------------|-------:|----------|
| [`testing-qa/`](testing-qa/README.md) | Risk-based test strategy, gap analysis, test implementation, independent verification | 7 | **operational** |
| [`observability-reliability/`](observability-reliability/README.md) | Signals, SLOs, alerting, runbooks, postmortems | 5 | **operational** |
| [`release-engineering/`](release-engineering/README.md) | Readiness, versioning, deployment strategy, rollback, post-release verification | 4 | **operational** |
| [`dependency-management/`](dependency-management/README.md) | Dependency inventory, breaking-change assessment, upgrade execution, verification, policy | 5 | **operational** |
| [`decommissioning/`](decommissioning/README.md) | Consumer discovery, deprecation, staged shutdown, data and asset retirement | 4 | **operational** |
| [`governance-compliance/`](governance-compliance/README.md) | Control mapping, evidence testing, readiness decision for enterprise obligations | 3 | **operational** |
| [`privacy-requests/`](privacy-requests/README.md) | Locate a subject's data everywhere, export or delete with verification, retention that keeps it gone | 3 | **operational** |
| [`git-operations/`](git-operations/README.md) | State checks before destructive commands, conflict resolution, history repair, recovery, conventions | 5 | **operational** |
| [`code-review/`](code-review/README.md) | Intent, change understanding, evidenced findings, actionable feedback, verified fixes | 6 | **operational** |
| [`feature-flags/`](feature-flags/README.md) | Flag inventory and risk, safe defaults, progressive rollout, kill-switch use, retirement | 5 | **operational** |
| [`documentation/`](documentation/README.md) | Documentation inventory, gaps, writing, validation | 8 | skeleton |
| [`project-management/`](project-management/README.md) | Goals, breakdown, planning, tracking, risk | 8 | skeleton |
| [`research-and-development/`](research-and-development/README.md) | Question, hypotheses, method, experiment, decision | 8 | skeleton |
| [`systems-building-improvement/`](systems-building-improvement/README.md) | Diagnose a system, design and evaluate an improvement | 8 | skeleton |

## How the operational systems fit together

```
testing-qa ─────────────► produces the safety net that makes change safe
        │
        ▼
release-engineering ────► gates the change into production, reversibly
        │
        ▼
observability-reliability ► detects failure, shortens recovery, converts
                           incidents into prevention work
        └──────────────► feeds the next improvement cycle
```

- **Before** changing code: `testing-qa/` QA-P02–P04 identifies what is unprotected.
- **Before** shipping: `release-engineering/` REL-P01 gives a go/no-go with evidence.
- **After** shipping: REL-P04 verifies against pre-defined criteria; if criteria breach, `05-scenarios/incident-response/`.
- **After** an incident: OBS-P05 produces the postmortem and owned actions.

## Shared standards across process systems

- Every stage declares risk class; none modifies production without explicit authorisation.
- Verification must be executable and able to fail; "should work" is rejected.
- Artifacts live in a dot-directory (`.qa/`, `.obs/`) so they do not pollute the repository.
- No process system grades its own implementation work; verification is a separate stage.

## Planned

Dependency and toolchain management, governance and compliance evidence, and the remaining process gaps are tracked in [`_meta/ROADMAP-AND-BACKLOG.md`](../_meta/ROADMAP-AND-BACKLOG.md).
