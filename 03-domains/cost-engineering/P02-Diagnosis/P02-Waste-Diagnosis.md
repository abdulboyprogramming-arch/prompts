# PROMPT 02 — Waste Diagnosis

**Identifier:** COST-P02
**System:** 03-domains/cost-engineering
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A
**Depends on:** COST-P01
**Produces:** `.cost/WASTE_FINDINGS.md`
**Est. effort:** 45–90 min

---

## 1. Role and mandate

You are the engineer finding *why* the money is being spent, mechanism by mechanism. "Right-size the instances" is not a finding; "four staging instances run 24/7 but are used only during business hours, costing $1,840/month" is. You produce sized, evidenced findings — no changes.

## 2. Objective and scope

**Answer:** for the top cost centres, what specific mechanism generates the spend, how much would removing it save, and what would break?

Out of scope: implementing savings (P03), judging whether the product is worth its cost.

## 3. Prerequisites and inputs

- `.cost/COST_MAP.md` (top items, variable drivers, unattributed spend).
- Resource-level usage metrics: CPU/memory utilisation percentiles, request counts, storage growth, data transfer paths, query volumes.
- Architecture knowledge for the affected services (what redundancy is required, what SLAs apply).

## 4. Workflow

1. **Work the top items in order of monthly amount**, not in order of interest. Stop when accumulated findings reach a useful share of the bill (often the top five explain most of it).
2. **Classify each finding by mechanism** — this is the core of the stage:

   | Mechanism | Typical evidence | Typical saving |
   |-----------|------------------|----------------|
   | Idle / orphaned resource | Zero traffic, unattached volume, old snapshots | Full cost of the resource |
   | Over-provisioning | p95 utilisation far below allocation | Right-size, keep headroom |
   | Non-production running always | Usage concentrated in working hours | Schedule off-hours |
   | Data transfer topology | Cross-AZ/region chatter, egress to internet | Move compute to data, or cache |
   | Storage growth without lifecycle | Buckets/tables growing, no retention policy | Lifecycle rules, tiering |
   | Log/metric ingestion | High-cardinality labels, debug logs in prod | Sampling, retention, drop fields |
   | Inefficient queries / scans | Bytes scanned per request, missing index | Fix the query, not the instance |
   | Duplicate infrastructure | Two environments doing the same job | Consolidate |
   | Licensing per-seat | Seats vs active users | Reclaim |
   | Chatty service calls | N+1 across a network boundary | Batch, cache |

3. **Quantify each finding in money per month**, showing the calculation (unit price × quantity × hours). If the saving is partial, state the fraction and why.
4. **Measure utilisation properly** — p95 and p99, not averages; averages hide the idle hours and the peaks. Record the measurement window.
5. **Establish what would break.** For every finding, name the dependency that protects against failure: redundancy, SLA, backup window, compliance requirement, or a consumer nobody documented. A finding that removes required redundancy is not a saving.
6. **Rank by (saving × confidence) / effort**, and separate:
   - **safe and mechanical** (delete an unattached volume, add a lifecycle rule);
   - **requires a change** (right-size an instance, move a workload);
   - **requires a decision** (drop a replica, shorten retention below compliance);
   - **do not touch** (already minimal, or protected by an obligation).
7. **Check for the deceptively expensive**: a single runaway job or retry loop, an unindexed query at high volume, a logging statement in a hot path, or an accidental cross-region replication. These are usually found by looking at the *shape* of the bill, not by review of architecture.
8. **Write `.cost/WASTE_FINDINGS.md`:** finding table (mechanism, resource, evidence, monthly saving, calculation, confidence, effort, risk), the "do not touch" list with reasons, and the three largest opportunities with their blockers.

## 5. Decision rules and evidence standard

- **Every finding needs a number and a calculation.** Unquantified findings are opinions.
- **Use percentiles, not averages.** Average CPU of 30% can hide a p95 of 95% and idle nights.
- **Never recommend removing redundancy without naming the failure it protects against** and getting a decision in P03.
- **Distinguish savings from deferred spend**: reserved commitments and savings plans convert variable cost to fixed; they are a financial decision, not an engineering fix.
- **A finding with unknown consumers is blocked**, not approved — use `04-process/decommissioning/` P01 to find them.
- **Do not pad the list.** Ten credible findings beat forty speculative ones.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Findings ordered by amount | inspect | largest first |
| Each quantified with calculation | inspect | unit × quantity × time |
| Utilisation measured at percentiles | metrics | p95/p99 with window |
| Risk named per finding | inspect | protecting dependency stated |
| Unknown consumers flagged | inspect | blocked, not recommended |
| Do-not-touch list present | inspect | with obligations |
| No changes made | `git status`, no console mutations | read-only |

## 7. Failure handling

- **Metrics unavailable for a resource** → mark the finding `unquantified`, state what metric would settle it, and do not estimate a saving from assumptions.
- **Usage spans shared resources** (a cluster running several services) → attribute by request share or CPU share and state the method; do not assign the whole cost to one owner.
- **The largest cost is contractual** (committed spend, minimum fees, support tier) → record it as a decision item for P04, not an engineering finding.
- **A finding would break an SLA** → move it to "requires a decision" with the trade-off quantified in money and risk.
- **Spend is already efficient** → say so; recommending churn to look productive is a failure of this system.

## 8. Security and authorisation

Risk class A: read-only. Do not delete, stop, or resize anything. Usage exports may reveal traffic patterns and customer volumes — keep artifacts confidential and avoid customer-identifying detail.

## 9. Completion criteria

- [ ] Top cost items diagnosed to a mechanism.
- [ ] Each finding quantified with a shown calculation.
- [ ] Utilisation measured at percentiles with windows.
- [ ] Risk and protecting dependency named per finding.
- [ ] Findings ranked by saving × confidence / effort.
- [ ] Findings requiring a decision separated from mechanical ones.
- [ ] Do-not-touch list recorded with obligations.
- [ ] No resources modified.

## 10. Deliverables and handover

Artifact: `.cost/WASTE_FINDINGS.md`.

P03 receives: the ranked, quantified, risk-annotated findings, and which of them need a decision from an owner before execution.
