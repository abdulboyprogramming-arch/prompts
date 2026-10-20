# PROMPT 04 — Guardrails & Unit Economics

**Identifier:** COST-P04
**System:** 03-domains/cost-engineering
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** B
**Depends on:** COST-P03
**Produces:** `.cost/GUARDRAILS.md`
**Inputs:** COST_TARGET, VALUE_METRIC
**Est. effort:** 30–60 min

---

## 1. Role and mandate

You are the engineer making the saving durable. Optimisation without guardrails decays: the next feature adds a debug log in the hot path, the next environment is never scheduled off, the next snapshot never expires. Your output is the smallest set of automated controls and the one number that tells the team whether the system is getting more or less efficient.

## 2. Objective and scope

**Produce** guardrails (tagging, budgets, alerts, policies) and unit economics (cost per request, per tenant, per job) with owners and thresholds.

Out of scope: implementing application changes, financial planning, contract negotiation.

## 3. Prerequisites and inputs

- `.cost/COST_MAP.md`, `.cost/WASTE_FINDINGS.md`, `.cost/OPTIMISATION_LOG.md`.
- A usage metric that represents product value: `{{VALUE_METRIC}}` (requests, active users, jobs processed, GB stored), against a cost ceiling of `{{COST_TARGET}}`.
- Existing alerting and policy tooling (budgets, quota policies, IaC modules).

## 4. Workflow

1. **Pick the unit.** Cost per 1,000 requests, per active tenant per month, per processed job, per GB ingested. Choose the unit that changes when engineering behaviour changes; a unit driven by headcount teaches nothing.
2. **Compute the current unit cost** over at least three months and plot the trend. Absolute spend rising while unit cost falls is usually healthy growth; the inverse is the alarm.
3. **Set thresholds**, not just dashboards: unit cost above X for two consecutive weeks, spend above budget by Y%, a resource type growing faster than traffic. Every threshold needs an owner and a response, or it becomes noise that is muted within a month.
4. **Install the mechanical guardrails**, cheapest first:
   - **Tagging enforcement** in IaC (a resource cannot merge without owner/environment tags) — the highest-leverage control, because it makes attribution automatic.
   - **Budgets with alerts** at 50/80/100% per account or team, routed to a person who can act.
   - **Lifecycle policies** for storage, snapshots, and logs — these fix waste permanently rather than monthly.
   - **Scheduling** for non-production environments, with an explicit exception list.
   - **Quota/policy limits** on the resource types that have caused runaway spend (high-cardinality metrics, expensive instance families, egress).
5. **Handle the exception path.** A guardrail with no exception process is either bypassed or blocks legitimate work; define who can approve an exception and for how long.
6. **Connect cost to the engineering workflow**: a PR that adds a logging statement in a hot path, an unbounded retention rule, or a new always-on environment should trigger a cost review. Add it to the review checklist rather than creating a separate process.
7. **Define the review cadence**: monthly unit-cost review with the trend and top movers; quarterly waste sweep re-running P02. Name the owner.
8. **Record what should not be optimised**: redundancy, backup retention, audit logging, and security tooling have standing exemptions with thresholds, so they are not re-litigated every cycle.
9. **Write `.cost/GUARDRAILS.md`:** unit definition and current value with trend, thresholds with owners and responses, controls with implementation status, exception process, review cadence, and standing exemptions.

## 5. Decision rules and evidence standard

- **Unit economics beat absolute spend** for judging engineering quality; state both.
- **Every alert has an owner and an action**, or it will be muted.
- **Prefer a policy over a monthly cleanup** — automation is what survives team turnover.
- **Do not set a budget you cannot influence**; a threshold on a fixed contract teaches the team to ignore alerts.
- **Never trade a security or reliability control for a cost target** without a recorded decision by the owner.
- **Guardrails must be testable**: show that an untagged resource fails the pipeline, or the control is decorative.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Unit defined and computed | billing + usage | 3-month trend |
| Thresholds have owners and responses | inspect | per threshold |
| Tagging enforcement tested | create untagged resource in a branch | pipeline rejects |
| Budget alerts routed | inspect config | named recipient |
| Lifecycle/scheduling active | console/IaC state | applied, with exceptions |
| Exception process defined | inspect | approver + expiry |
| Review cadence with owner | inspect | scheduled |
| Standing exemptions recorded | inspect | reliability/security items |

## 7. Failure handling

- **No usage metric available** → choose the closest proxy (requests from gateway logs) and label it; do not abandon unit economics.
- **Tagging cannot be enforced yet** (legacy infrastructure) → enforce on new resources via IaC and track a remediation list for the rest.
- **Alerts would fire constantly** → the threshold is wrong or the baseline is unknown; calibrate against three months of history before enabling.
- **A guardrail blocks legitimate work** → fix the exception path, not the guardrail; record the case that exposed it.
- **Finance reporting conflicts with engineering attribution** (different cost centres) → record both mappings and agree which is authoritative for engineering decisions.

## 8. Security and authorisation

Risk class B: policy-as-code and alerting configuration in the repository and cloud account. Do not add cost controls that reduce audit logging or access logging. Budget alerts contain account identifiers — keep configuration free of secrets and avoid committing billing exports.

## 9. Completion criteria

- [ ] Unit defined, computed, and trended.
- [ ] Thresholds with owners and defined responses.
- [ ] Tagging enforcement implemented and tested.
- [ ] Budget alerts routed to an owner.
- [ ] Lifecycle and scheduling controls applied with exception lists.
- [ ] Quota/policy limits on runaway resource types.
- [ ] Exception process and review cadence agreed.
- [ ] Standing exemptions documented.

## 10. Deliverables and handover

Artifact: `.cost/GUARDRAILS.md`.

Handover: the monthly review produces new P02 findings; tagging requirements go into the IaC modules owned by `03-domains/devops-infra/`; hot-path cost checks enter code review; realised savings feed the team's reporting with the evidence in `.cost/OPTIMISATION_LOG.md`.
