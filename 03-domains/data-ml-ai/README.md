# Data / ML / AI Domain System

**Status:** Operational (v1.0)  
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
