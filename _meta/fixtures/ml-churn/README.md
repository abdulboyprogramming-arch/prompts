# Fixture: churn data with four planted defects

Built for [`empirical-evaluation-15.md`](../../empirical-evaluation-15.md), where
`MLA-P03` is run against data whose leakage paths are known in advance — so the
question is not whether the output reads well, but whether the procedure finds them.

| File | What it is |
|---|---|
| `make_fixture.py` | generator, fixed seed, no dependencies beyond the stdlib |
| `accounts.csv` | 1,200 account-months, 18 cohorts (2024-01 to 2025-06), churn rate 32.25% |
| `train.py` | the project's current training script, which uses all four defects |

## The planted defects

| # | Defect | How it shows up |
|---|---|---|
| 1 | `cancel_reason` populated only at cancellation | every non-empty value implies `churned_30d = 1` |
| 2 | `status` is a function of the label | `status == "cancelled"` agrees with the label on all 1,200 rows |
| 3 | `last_login_days` measured after the outcome window | `max(label=0) = 30`, `min(label=1) = 31` — no overlap |
| 4 | random shuffle split over time-ordered data | `train.py` seeds and shuffles the whole table |

Defects 1, 2 and 4 are visible from the schema or the code. **Defect 3 is not**, and it
is the one that matters: the column name is innocent and the statistics are perfect, so
a schema-first leakage register misses it. That is the finding this fixture exists to
reproduce.

## Reproduce

```
python3 _meta/fixtures/ml-churn/make_fixture.py   # rewrites accounts.csv beside itself
python3 _meta/fixtures/ml-churn/train.py          # prints the leaky feature list and baseline
```

The regenerated CSV is byte-identical to the committed one (`random.seed(7)`, no
floating-point drift in the columns that are written).
