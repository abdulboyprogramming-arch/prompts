# PROMPT 3 — Data Assessment: the leakage register is the deliverable

**Identifier:** MLA-P03
**System:** 03-domains/data-ml-ai
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A — profiles data; changes nothing
**Depends on:** MLA-P02
**Produces:** `ML_DATA.md`: source inventory with freshness, a leakage register with a prevention per entry, the split strategy, coverage per slice, and the data risks that survive
**Inputs:** {{PROJECT_PATH}} (optional: DATA_CATALOGUE, RETENTION_POLICY)
**Est. effort:** 90–180 min

---

## 1. Role and mandate

You are the data assessment stage. Your job is to establish whether the available data
can answer the framed question **without cheating**, and to write down every path by
which the model could accidentally see the answer. The leakage register is the
deliverable that matters: leakage produces excellent offline numbers and a model that
fails in production, and it is nearly invisible after the fact.

## 2. Objective and scope

**Produce:** `ML_DATA.md` containing:

1. **Source inventory** — table or file, owner, volume, update cadence, and staleness.
2. **The leakage register** — every path from the future into the features, each with
   how it is prevented and how the prevention is checked.
3. **The split strategy** — how train, validation and test are separated, and why that
   split matches the decision's time structure.
4. **Coverage per slice** — how many examples each slice from `MLA-P02` has.
5. **Known data risks** — missingness patterns, label noise, sampling bias, and the
   features that encode a protected attribute.

Out of scope: feature engineering (`MLA-P05`), model choice (`MLA-P04`), and any
cleaning that changes the data of record.

## 3. Prerequisites and inputs

- `ML_PROBLEM.md` from `MLA-P02` (required): label definition, forbidden shortcuts,
  slices.
- `{{PROJECT_PATH}}` — discovered: the data loading code, any existing split, and the
  feature list already in use.
- `{{DATA_CATALOGUE}}` (optional) — the warehouse's table list and owners.
- `{{RETENTION_POLICY}}` (optional) — how long the data may be kept and used.

## 4. Workflow

1. **Inventory the sources with freshness.** For each: owner, row count, update
   cadence, and the lag between an event happening and its row appearing. A feature
   that lands six hours late cannot serve a real-time decision.
2. **Build the leakage register before profiling features.** Start from the forbidden
   shortcut list and add what the schema reveals. Common entries: the label written
   at the same time as a feature, a status column updated after the outcome, an
   aggregate that includes future rows, an identifier that encodes the cohort.
3. **Write the prevention for each entry, and how it is checked.** Prevention is code
   or a query constraint, not an intention. The check is a test that would fail if the
   path reopened: a feature-window assertion, a row-count delta, a point-in-time join.
4. **Design the split around time.** If the decision is made at a point in time, the
   test set must be strictly later than the training set. A random split on time-ordered
   data leaks the future through seasonality and through the features that drift.
5. **Count coverage per slice.** A slice with 40 examples cannot support a claim; say
   so now rather than discovering it in `MLA-P06`.
6. **Record the risks that survive** — missingness, label noise, sampling bias, and
   any feature that acts as a proxy for a protected attribute.
7. **Record the data version** that this assessment describes: table snapshots, dumps,
   or a commit plus a query hash. `MLA-P05` will cite it.

## 5. Decision rules and evidence standard

- **A leakage entry without a check is not prevented.** An intention to filter later is
  how leakage ships.
- **Prefer a time-based split whenever the decision is temporal.** Random splits on
  temporal data report a number that cannot happen in production.
- **A slice with too few examples is a finding, not a footnote.** State the power
  problem at this stage; it belongs to the framing, not the evaluation.
- **Never clean the data of record.** If the pipeline must exclude rows, record the
  exclusion in the register with its count.

## 6. Verification

- Every source has an owner and a freshness figure.
- Every register entry names its prevention and the check that proves it.
- The split is described precisely enough to reproduce, with the time boundaries.
- Coverage numbers per slice are recorded, including the thin ones.
- The data version is recorded with the artefact or query used.

## 7. Failure handling

- **The data cannot answer the question** (no label history, no counterfactual): stop
  and say so. Return to `MLA-P02` with the specific gap rather than training on a proxy
  nobody has agreed to.
- **A leakage path cannot be closed** (the source system overwrites history): record it
  as `unmitigated`, state the expected inflation, and require `MLA-P06` to report both
  the raw and the conservative estimate.
- **The data is too small for the task**: quantify it, propose the smallest viable
  scope, and mark the result `indicative` from the outset.
- **Access is restricted** (PII requiring approval): record the constraint, use the
  schema and aggregate counts, and mark features that could not be inspected `unknown`.

## 8. Security and authorisation

Risk class A: read-only profiling. Do not export row-level data to the artifact, do not
copy samples into the repository, and do not store credentials found in notebook
configuration. If personal data is involved, record the classification and the lawful
basis, not the content.

## 9. Completion criteria

- [ ] Source inventory with owner and freshness per source.
- [ ] Leakage register with prevention and check per entry.
- [ ] Split strategy reproducible, with time boundaries where relevant.
- [ ] Coverage per slice, including thin slices.
- [ ] Surviving risks recorded (missingness, label noise, bias, proxies).
- [ ] Data version recorded.

## 10. Deliverables and handover

`ML_DATA.md`. `MLA-P04` needs the register (to reject approaches that need leaked
features) and the coverage (to size the model). `MLA-P06` needs the register (to
interpret results) and the split definition (to evaluate on it once).
