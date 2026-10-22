# Data / ML / AI Domain System

> **Boundary.** Everything upstream of feature engineering — ingestion, freshness, idempotent loads, backfills, reconciliation — belongs to [`03-domains/data-engineering/`](../data-engineering/README.md) (`DE-P01..P02`). This system starts where the data is already trustworthy and asks what to do with it.

**Status:** Operational — eight stages (`MLA-P01`–`MLA-P08`). The system is built around two failures that look like success: a metric improved by **leakage**, and a model deployed with **no defined behaviour when it is wrong**. Context establishes the decision and the cost of each error before any modelling; framing derives the metric from that cost ratio and pre-registers the threshold; the data stage's deliverable is a leakage register with a prevention and a check per entry; the approach stage must measure a baseline before proposing a model; implementation makes a run reproducible or the number is a rumour; evaluation touches the held-out set once and reports the worst slice before the average; deployment defines the fallback and a numeric rollback trigger before the first prediction is served. **No stage has been executed against a real ML project**, so this is a complete procedure with no demonstrated run; [`_meta/release-readiness.md`](../../_meta/release-readiness.md) records that gap.
**Entry Point:** [`P08-Orchestrator/P08-Data-ML-AI-Orchestrator.md`](P08-Orchestrator/P08-Data-ML-AI-Orchestrator.md)

A multi-stage system for data, machine learning, and applied AI work — from problem framing through evaluation and operational monitoring.

Use for:
- ML model development and iteration
- Data pipelines and feature preparation
- Applied AI features inside products
- Evaluation harnesses and offline/online metrics
- Lightweight MLOps-minded deployment readiness

## Stages

| ID | Prompt | Purpose |
|----|--------|---------|
| ML-P01 | Context & Constraints | Understand product goal, users, and constraints |
| ML-P02 | Problem Framing | Define prediction/task objective and success metrics |
| ML-P03 | Data Assessment | Inventory data, quality, leakage risks, and splits |
| ML-P04 | Approach Design | Choose modeling/pipeline approach and baselines |
| ML-P05 | Implementation | Build pipeline, features, and model/code paths |
| ML-P06 | Evaluation | Offline metrics, error analysis, and validation |
| ML-P07 | Deployment & Monitoring | Launch readiness, feedback loops, drift signals |
| ML-P08 | Master Orchestrator | Coordinates the full data/ML/AI process |

## Principles

- Frame the decision/task before choosing models.
- Establish baselines early.
- Watch for leakage, bias, and unrepresentative data.
- Separate experimental notebooks from production paths.
- Evaluation and monitoring are part of done, not afterthoughts.
