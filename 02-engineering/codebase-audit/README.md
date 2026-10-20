# Deep Codebase Audit & Analysis System

**Maturity: operational (v1.1.0).** All nine stages carry workflow, evidence rules, verification, failure handling, and completion criteria. The system is read-only with respect to source code: every stage writes only inside `.audit/`.

**Entry point:** [`P09-Orchestrator/P09-Deep-Codebase-Audit-Orchestrator.md`](P09-Orchestrator/P09-Deep-Codebase-Audit-Orchestrator.md)
**Execution mode:** diagnostic
**Risk class:** B — writes audit artifacts under `.audit/`; never edits application code, never publishes.

## What this system is for

You have an existing codebase — inherited, acquired, grown organically, or produced with heavy AI assistance — and need a defensible answer to: *what is actually here, what is wrong, what matters most, and in what order should it be fixed?*

It is not a linter run, and it is not a rewrite proposal. It produces evidence-backed findings and a sequenced roadmap that a competent engineer could act on.

## Stages

| ID | Stage | Produces | Maturity |
|----|-------|----------|----------|
| AUDIT-P01 | [Scope, environment & audit contract](P01-Bootstrap/P01-Audit-Environment-Bootstrap.md) | `.audit/AUDIT_SCOPE.md`, `.audit/AUDIT_LEDGER.md` | operational |
| AUDIT-P02 | [Structural mapping](P02-Structure/P02-Structural-Mapping.md) | `.audit/REPO_STRUCTURE.md` | operational |
| AUDIT-P03 | [Architecture recovery](P03-Architecture/P03-Architectural-Analysis.md) | `.audit/ARCHITECTURE.md` | operational |
| AUDIT-P04 | [Code quality & maintainability](P04-Quality/P04-Code-Quality-Maintainability.md) | `.audit/QUALITY.md` | operational |
| AUDIT-P05 | [Tests, dependencies & build health](P05-Tests-Deps/P05-Tests-Dependencies-Health.md) | `.audit/TEST_DEPS.md` | operational |
| AUDIT-P06 | [Security surface & documentation](P06-Security-Docs/P06-Security-Surface-Documentation.md) | `.audit/SECURITY_DOCS.md` | operational |
| AUDIT-P07 | [Findings synthesis & prioritisation](P07-Findings/P07-Findings-Synthesis-Prioritization.md) | `.audit/FINDINGS.md` | operational |
| AUDIT-P08 | [Roadmap & final report](P08-Roadmap/P08-Improvement-Roadmap-Report.md) | `.audit/ROADMAP.md`, `.audit/AUDIT_REPORT.md` | operational |
| AUDIT-P09 | [Master orchestrator](P09-Orchestrator/P09-Deep-Codebase-Audit-Orchestrator.md) | all of the above | operational |

## Shared contracts

These apply to every stage; individual prompts assume them rather than restating them.

### Evidence labels

Every factual claim in an artifact carries one of:

- `verified` — a file path with line range, or output of a command you ran.
- `inferred` — reasoning from verified facts; the reasoning is stated.
- `unknown` — could not be established; the reason and the cheapest way to establish it are given.

A finding without a `verified` or `inferred` basis is deleted at P07, not softened.

### Severity model (used from P04 onward, enforced at P07)

| Level | Definition | Required evidence |
|-------|------------|-------------------|
| **S1 – Critical** | Data loss, security breach, outage, or incorrect money/authorisation logic in normal operation | Reproducible path or concrete exploit/state-machine argument |
| **S2 – Major** | Likely production failure, silent incorrect behaviour, or a change-blocking structural defect | Specific code path + conditions |
| **S3 – Moderate** | Real cost (maintainability, performance, reliability) with a workaround | Example instances, not just a pattern name |
| **S4 – Minor** | Style, consistency, documentation drift, low-impact cleanup | Location list |

Severity measures **consequence**, not the effort to fix. Do not inflate: "no TLS pinning" in a hobby CLI is not S1.

### Finding schema

Every finding, in every stage artifact, uses the same fields:

```markdown
### F-<stage>-<n>: <one-line statement>
- Severity: S1 | S2 | S3 | S4
- Evidence: <path:lines | command output>   (label: verified/inferred)
- Impact: <what goes wrong, for whom, under what conditions>
- Confidence: high | medium | low — <why>
- Suggested action: <one sentence, not a full design>
- Blast radius if fixed: <files/modules>
```

### State

`.audit/AUDIT_LEDGER.md` records stage status, artifacts, open questions, and assumptions. Every stage updates it. On resume, read the ledger and existing artifacts before re-running anything.

## How to run it

1. Open the target repository at a known commit (`git rev-parse HEAD`) — record it in P01; an audit without a commit reference decays immediately.
2. Give your agent the P09 orchestrator, the repository path, and any audit questions you specifically care about.
3. Expect a first usable report after P01–P03 (structure and architecture), and the actionable output after P07–P08.
4. If a stage cannot run (missing toolchain, no test command), the agent records `not run: <reason>` rather than inferring success.

## What it will not do

- Fix anything. Use `02-engineering/refactoring/`, `05-scenarios/` fixes, or a planning prompt afterwards.
- Certify compliance. It can produce evidence toward a control; it cannot attest to one.
- Replace penetration testing. P06 maps attack surface and reviews obvious weaknesses; it is not an exploit campaign.
- Guarantee completeness on a very large monorepo. It will state coverage boundaries explicitly.

## Design principles

1. **Evidence over assertion** — no finding without a basis.
2. **Actual over intended architecture** — document what the code does, then note where docs disagree.
3. **Bounded depth** — sample deliberately and say what was sampled; do not claim to have read everything.
4. **Consequence over aesthetics** — severity reflects impact, not taste.
5. **Actionable output** — every finding suggests the next concrete step.
6. **Honest coverage** — coverage limits are part of the deliverable.

## Related

- Fix the findings: `02-engineering/refactoring/`, `02-engineering/security-hardening/`, `04-process/testing-qa/`
- Full workflow that consumes this audit: `07-workflows/README.md`
- Deep single-topic investigation: `05-scenarios/performance-investigation/`
