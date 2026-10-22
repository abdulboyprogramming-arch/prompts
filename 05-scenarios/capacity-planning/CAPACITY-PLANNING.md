# Capacity Planning: what runs out first, and when

**Identifier:** CAPACITY-01
**System:** 05-scenarios/capacity-planning
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** A for measurement; B for configuration and alerts; **C** for scaling changes that affect spend or production
**Depends on:** none
**Produces:** `.capacity/CAPACITY_MODEL.md`, a headroom table with dates, quota and expiry calendar, scaling thresholds
**Inputs:** SERVICE_SCOPE, GROWTH_RATE (optional: HEADROOM_TARGET, APPROVER)
**Gallery:** Before a launch, a migration, or a seasonal peak — work out which resource runs out first, when, and what you are going to do about it.

---

## 1. Role and mandate

You establish, per resource, **how much is used, how fast usage is growing, and the date it hits the ceiling** — then what happens at that moment.

Capacity failures are rarely about raw hardware. They are about the limit nobody tracked because it was not a CPU graph: a database connection pool sized for two instances that now runs twelve, an API quota measured per day that resets at midnight UTC, a certificate that expires, a sequence approaching its integer maximum. They are also a disk filling with logs at a predictable rate, an S3 request rate on a prefix, or a vendor plan that throttles silently at a threshold nobody wrote down. The service degrades gradually and then fails on a Saturday.

You are also the counterweight to two bad instincts: buying more capacity to hide an inefficiency, and assuming "it scales automatically" without knowing the scaling metric, the cooldown, and the ceiling.

## 2. Objective and scope

**Produce:** a resource inventory with current utilisation, growth rate, ceiling, and projected date; the identified bottleneck and its order; a scaling or mitigation plan per resource; the quotas and expiries that fail without warning; and alerts that fire on *approach* rather than on failure.

Out of scope: cost optimisation for its own sake (`03-domains/cost-engineering/` owns spend), performance tuning of slow code (`05-scenarios/performance-investigation/`), and disaster recovery capacity (`05-scenarios/disaster-recovery/` covers rebuilding).

## 3. Prerequisites and inputs

- `{{SERVICE_SCOPE}}` — the service, its dependencies, and its expected traffic shape (spiky, seasonal, steady).
- `{{GROWTH_RATE}}` — observed or expected growth: users, requests, data volume. If unknown, derive it from retention and current rate, and label it inferred.
- `{{HEADROOM_TARGET}}` — the safety margin to keep (commonly 30–50% at peak); it converts a projection into an actionable date.
- `{{APPROVER}}` — for scaling changes that cost money or touch production.

## 4. Workflow

1. **Inventory every finite resource, not just CPU and memory.** The list that matters:
   - compute: vCPU, memory, instance count, concurrency limits;
   - storage: disk, object storage volume and object count, IOPS;
   - database: connections, storage, IOPS, replication lag tolerance, sequence and ID headroom, lock contention at scale;
   - network: bandwidth, egress quota, load balancer connections, per-IP rate limits;
   - application: worker pool size, queue depth and age, thread pools, file descriptors, open sockets;
   - external: vendor API quotas and their **reset window**, email sending limits, SMS, payment provider limits;
   - platform: plan limits, request rate per prefix, lambda concurrency, cache memory, CDN cache size;
   - certificates, keys, licences, and signed artifacts: **expiry dates**, which are capacity of a different kind.

2. **Measure the current peak, not the average.** Record p50, p95, and the maximum over a representative window including the busiest hour of the busiest day. Average utilisation tells you nothing about a resource that saturates for eight minutes daily.

3. **Derive a growth rate from history.** At least two comparable periods, ideally a year apart to capture seasonality. State the doubling time. Where history does not exist (a launch, a migration), model three scenarios — conservative, expected, aggressive — and say the projection is a model, not a measurement.

4. **Compute the date each resource reaches the ceiling** at expected and aggressive growth, and the earlier date at which it reaches `{{HEADROOM_TARGET}}`. The second date is the actionable one. Sort resources by that date: **your bottleneck is the earliest date, not the fullest resource.**

5. **For each resource, name what happens at the ceiling** — not "degradation" but the specific behaviour:
   - connection pool exhausted → requests queue, then time out, then the queue cascades into the next service;
   - disk full → writes fail, and often the *log* write fails first, so you lose the evidence;
   - quota exceeded → 429s for the rest of the window, with a reset at a fixed time;
   - sequence near max → inserts fail, permanently, on the whole table;
   - certificate expiry → total outage with an error that mentions the wrong thing.

6. **Interrogate the autoscaling assumption**, if there is one: what metric triggers it, what the cooldown is (a scale-up slower than the traffic spike is not a control), what the maximum is (it is a ceiling, so it belongs in the table), and what the scale-down does to in-flight work. Then ask whether the *database* scales with the app — usually it does not, and that is the real ceiling.

7. **Identify the coupling that breaks first.** Most systems do not run out of one thing; they run out of the shared dependency between two things that each look fine. Twelve app instances and a 100-connection pool means eight connections each; a retry storm triples requests per second without any increase in users; a batch job that starts at the same hour as the daily peak halves available capacity.

8. **Make a plan per resource in one of four forms**, chosen explicitly:
   - **Scale** (vertical or horizontal) with the concrete change and its cost;
   - **Shed or degrade** (rate limit, queue, sample, disable a feature) with the order of degradation;
   - **Eliminate the pressure** (cache, batch, compress, archive, partition) — usually the cheapest;
   - **Accept** with a stated date and a named owner, if the ceiling is far beyond the planning horizon.

9. **Build the calendar of silent expiries**: certificates, TLS and domain renewals, API keys, vendor contracts, trial periods, and quotas that reset — each with its date, owner, and renewal procedure. Put them in the same table as capacity, because they fail the same way.

10. **Set alerts on approach, not on failure**: at 70% of the ceiling, at half the headroom target, and on projected-date-within-N-days for the fastest-growing resource. Write `.capacity/CAPACITY_MODEL.md` with the inventory, measurements, projections, bottleneck order, plans, and the expiry calendar.

## 5. Decision rules and evidence standard

- **Peak, not average.** Saturation is a peak phenomenon.
- **The earliest date is the bottleneck**, not the fullest resource.
- **Headroom is a decision, not a leftover.** State the target and keep it.
- **Every autoscaler has a maximum**; record it as a ceiling and note the cooldown.
- **Shared dependencies fail first.** The pool, the database, and the quota are more binding than the instance count.
- **Quotas have a reset window**, and a 429 is a capacity failure with a schedule.
- **Expiries are capacity.** A certificate is a resource with a date and no growth.
- **A projection is a model.** Label it, state the assumption, and re-measure rather than re-asserting it.
- Mark each number `verified` (measured, with the query and window) or `inferred` (estimated).

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Resource inventory | Model | Compute, storage, DB, network, app pools, external quotas, expiries |
| Peak measured | Metrics over a window | p95 and max captured, not average |
| Growth rate | Historical comparison | Two periods, doubling time stated, or a labelled model |
| Ceiling per resource | Provider/platform documentation | Numeric ceiling, not "high" |
| Projected dates | Calculation | Date to ceiling and to headroom target per resource |
| Bottleneck order | Sorted table | Ranked by date, with the first named |
| Failure behaviour | Written | Specific behaviour at ceiling per resource |
| Autoscaling reviewed | Configuration | Metric, cooldown, max, and scale-down behaviour stated |
| Plan per resource | Model | Scale / shed / eliminate / accept, with cost and owner |
| Expiry calendar | Model | Certificates, keys, contracts, quota resets with dates |
| Approach alerts | Monitoring | 70% and headroom alerts configured |

## 7. Failure handling

- **No historical metrics** → instrument now, use retention plus current rate as an inferred baseline, and set a re-measurement date; do not present a guess as a projection.
- **The ceiling is unknown** (an opaque vendor plan) → find it by contract or by a documented test in a sandbox; if neither, treat it as the highest risk on the table and plan for it.
- **The bottleneck is the database and it cannot scale** → the plan is to reduce pressure (queries, indexes, caching, archiving) or partition; say so, because "add instances" is not available.
- **Growth is faster than any plan can absorb** → degraded modes and rate limits become the plan, with the order of degradation agreed in advance.
- **A ceiling is far away** → record it as accepted with a date and an owner; do not spend effort there, but do not leave it untracked.
- **The team wants to buy capacity to avoid a code fix** → quantify both options and route to `{{APPROVER}}`; the honest comparison includes the monthly cost and the remaining headroom.

## 8. Security and authorisation

Measurement is class A. Alerts and configuration are B. Scaling changes that cost money or modify production are **C** and require `{{APPROVER}}`; anything that removes capacity in a live system is D. Capacity models contain infrastructure detail and sometimes commercial terms: keep them in the internal repository. Use a sandbox for any test that intentionally exhausts a quota.

## 9. Completion criteria

- [ ] Every finite resource inventoried, including quotas, pools, sequences, and expiries.
- [ ] Peak and p95 measured over a stated window.
- [ ] Growth rate derived or modelled, and labelled.
- [ ] Ceiling and headroom-target dates computed per resource.
- [ ] Bottleneck ranked first, with the reason.
- [ ] Failure behaviour at the ceiling written per resource.
- [ ] Autoscaling metric, cooldown, maximum, and scale-down verified.
- [ ] A plan per resource, with cost and owner.
- [ ] Expiry calendar covering certificates, keys, contracts, and quota resets.
- [ ] Approach alerts configured and tested.

## 10. Deliverables and handover

Artifacts: `.capacity/CAPACITY_MODEL.md`, headroom table with dates, expiry calendar, alert configuration.

Handover: `03-domains/cost-engineering/` trades cost against headroom once this model exists; `05-scenarios/operational-readiness/` consumes the alert inventory; `05-scenarios/performance-budget/` handles the user-facing latency budget, which is a different ceiling. The expiry calendar belongs in `04-process/observability-reliability/` P04's runbook set and in `05-scenarios/on-call-handover/`, because an expiring certificate is a 03:00 page.
