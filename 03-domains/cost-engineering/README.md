# Cost Engineering

**Maturity: operational (v1.0.0).** Four stages for finding where the money goes, removing what is wasted, and keeping spend from creeping back.

**Entry point:** [`P01-Visibility/P01-Cost-Visibility.md`](P01-Visibility/P01-Cost-Visibility.md)
**Execution mode:** audit-remediation
**Risk class:** A for analysis, B for infrastructure changes, C for anything reaching production

## Why this system exists

Cloud cost is the only engineering metric that arrives as an invoice, after the fact, with no line pointing at the decision that caused it. Teams respond by guessing at savings ("we should right-size those instances") and by cutting things that turn out to matter. Meanwhile the costs that actually dominate are usually unglamorous: idle environments, unbounded log retention, cross-region egress, orphaned volumes, and a query that scans a table forty times a minute.

This system treats cost like reliability: measure, attribute, diagnose the specific mechanism, change it with a rollback path, and install guardrails so the regression cannot silently recur.

## Stages

| ID | Stage | Purpose | Produces |
|----|-------|---------|----------|
| COST-P01 | [Visibility & attribution](P01-Visibility/P01-Cost-Visibility.md) | What is spent, by which service/team/environment, and what is unattributable | `.cost/COST_MAP.md` |
| COST-P02 | [Waste diagnosis](P02-Diagnosis/P02-Waste-Diagnosis.md) | Find the specific mechanisms of waste, sized in money | `.cost/WASTE_FINDINGS.md` |
| COST-P03 | [Optimisation](P03-Optimisation/P03-Optimisation.md) | Change the top items safely, with a verification and rollback | `.cost/OPTIMISATION_LOG.md` |
| COST-P04 | [Guardrails & unit economics](P04-Guardrails/P04-Guardrails-Unit-Economics.md) | Budgets, alerts, tagging, and cost per unit of product | `.cost/GUARDRAILS.md` |

## Rules

1. **Cost is a metric with an owner**, like latency. Unattributed spend cannot be managed.
2. **Size every finding in money per month** — an unquantified recommendation will not be prioritised.
3. **Never optimise by degrading reliability without a recorded decision.** A cheaper system that fails is not a saving.
4. **Change one cost mechanism at a time**, and verify the bill moves in the expected direction.
5. **Install the guardrail with the fix**, or the waste returns with the next feature.

## Boundaries

- Performance as experienced by users: `02-engineering/performance/`.
- Instance and topology changes: `03-domains/devops-infra/`.
- Query and index work: `03-domains/database/`.
- Incident-driven escalations: `05-scenarios/incident-response/`.

## What this system will not do

- Negotiate contracts or commitments. It quantifies what a commitment would need to cover.
- Guess at numbers it cannot source from billing data. Unattributable spend is reported as such.
- Cut cost by removing safety: redundancy, backups, and monitoring have owners and thresholds like anything else.
