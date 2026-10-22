# PROMPT 5 — Implementation: reproducible, or the number is a rumour

**Identifier:** MLA-P05
**System:** 03-domains/data-ml-ai
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B — writes pipelines and training code
**Depends on:** MLA-P04
**Produces:** the pipeline and training code, `ML_IMPLEMENTATION_LOG.md` with the run register: config, data version, seed, and result per run
**Inputs:** {{PROJECT_PATH}} (optional: COMPUTE_BUDGET, ARTIFACT_STORE)
**Est. effort:** 1–5 days depending on the pipeline

---

## 1. Role and mandate

You are the implementation stage. You build the data path and the training path so that
a run can be repeated by someone else and produce the same artefact. In ML the
reproducibility is not hygiene; it is the difference between a measurement and an
anecdote.

## 2. Objective and scope

**Produce:**

1. **A reproducible pipeline** — data preparation, feature construction, training, and
   a scored artefact — runnable from one documented command.
2. **`ML_IMPLEMENTATION_LOG.md`** — the run register: for each run, the config, the data
   version, the seed, the environment, the metric, and the artefact path.
3. **Separation of experimental and candidate code** — notebooks or scratch scripts may
   explore; only reviewed code produces the artefact that `MLA-P06` scores.

Out of scope: final evaluation (`MLA-P06`), serving (`MLA-P07`), and any metric change.

## 3. Prerequisites and inputs

- `ML_APPROACH.md` from `MLA-P04` (required): feature plan, training procedure, seeds.
- `ML_DATA.md` from `MLA-P03` — the data version and the leakage register.
- `{{PROJECT_PATH}}` — discovered: the language, package manager, test command and
  existing pipeline conventions. Follow the repository's conventions before inventing
  a framework.
- `{{COMPUTE_BUDGET}}` (optional) — caps the search; if absent, cap it yourself and
  record the cap.
- `{{ARTIFACT_STORE}}` (optional) — where models are stored. If absent, use a local
  directory that is not committed.

## 4. Workflow

1. **Build the data path first and test it in isolation.** A feature pipeline that
   cannot be run without training is a feature pipeline nobody can debug. Assert the
   leakage checks from `ML_DATA.md` here: the point-in-time join, the window bound, the
   excluded columns.
2. **Freeze the split.** Write it as code that produces the same assignment every time,
   and record the hash or boundary dates in the log. A split regenerated per run
   invalidates every comparison.
3. **Make the config explicit.** Every hyperparameter, feature group, and data version
   in one file, logged with the run. Defaults hidden in code are the most common cause of
   "it worked yesterday".
4. **Fix the seed policy and record it.** Deterministic where the library allows it;
   where it does not, run k times and log the spread rather than a single number.
5. **Keep the run register current.** Every run appends a row: date, commit, config
   hash, data version, metric, artefact path. A run that is not in the register does not
   exist for `MLA-P06`.
6. **Write the smallest test suite that proves the pipeline**: a schema test on the
   feature frame, an assertion that no future-dated rows enter the training window, and
   a smoke test that trains on a small sample and produces a scored artefact.
7. **Record the cost of a full run** — wall time and, where it applies, spend. `MLA-P07`
   needs it to size retraining.

## 5. Decision rules and evidence standard

- **A number without a config and a data version is not a result.** It cannot be
  reproduced and cannot be compared.
- **Never tune against the test set.** Hyperparameter search runs on validation; if the
  code does not enforce it, the reviewer cannot tell, and neither can the metric.
- **Notebooks explore; the pipeline produces.** The artefact scored in `MLA-P06` comes
  from the pipeline, never from a notebook cell.
- **Log failures too.** A run that diverged or produced a worse score is a data point
  about the approach.

## 6. Verification

- One documented command reproduces the artefact from a clean checkout.
- The split is fixed and its identity is recorded.
- Every run in the register has config, data version, seed and metric.
- The leakage assertions run as tests and fail if a future-dated row enters training.
- The candidate artefact was produced by pipeline code under version control.

## 7. Failure handling

- **Results are not reproducible between runs:** stop and fix the seed, the split or an
  unordered join before producing more numbers. Record the variance observed.
- **A leakage assertion fails:** fix the join, not the assertion. Record the discovery
  and note that any earlier result is void.
- **The training cannot fit the compute budget:** reduce the search space, record the
  reduction, and note that the result is bounded by it.
- **The data version changed mid-project:** record both versions, re-run the baseline,
  and mark earlier comparisons void rather than mixing them.

## 8. Security and authorisation

Risk class B: local code and artefacts. Do not commit datasets, model binaries or
credentials; do not log rows of personal data; do not call a paid vendor API during
training without an authorised budget. Artefact directories belong in `.gitignore`.

## 9. Completion criteria

- [ ] One-command reproduction of the scored artefact.
- [ ] Split fixed and identified.
- [ ] Run register complete for every run cited later.
- [ ] Leakage assertions implemented as tests.
- [ ] Experimental and candidate code separated.
- [ ] Full-run cost recorded.

## 10. Deliverables and handover

The pipeline, the tests and `ML_IMPLEMENTATION_LOG.md`. `MLA-P06` needs the candidate
artefact, its config, and its run-register row. `MLA-P07` needs the cost of a run and
the serving interface the pipeline exposes.

## 11. Regression protection

Changing the pipeline must not silently change the artefact's inputs. Pin the feature
list in a test; a feature added by a colleague without the register entry is how a leak
returns after it was closed.

## 12. Rollback

Every artefact is versioned in the register with its config, so rollback is pointing
serving at the previous artefact. If the pipeline change cannot be reverted without
retraining, record that cost before shipping the change.
