# PROMPT 2 — Requirements & SLOs: numbers that a pipeline step can fail on

**Identifier:** DI-P02
**System:** 03-domains/devops-infra
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** A — writes a requirements document; changes nothing
**Depends on:** DI-P01 (`DI_CONTEXT.md`)
**Produces:** `DI_REQUIREMENTS.md`: delivery targets, reliability objectives with their measurement, the security and compliance requirements, and the non-goals
**Inputs:** {{PROJECT_PATH}} (optional: SLO_TARGETS, COMPLIANCE_SCOPE, ERROR_BUDGET_POLICY)
**Est. effort:** 45–90 min

---

## 1. Role and mandate

You turn "we want reliable deploys" into numbers that a later stage can test and a
dashboard can show. A requirement that cannot fail is a wish: "high availability" and
"fast deploys" have cost every organisation that wrote them down without a measurement.

You produce targets and their measurement method. You do not design the topology
(`DI-P03`) or the pipeline (`DI-P04`).

## 2. Objective and scope

**Produce:** `DI_REQUIREMENTS.md` containing:

1. **Delivery targets** with a measurement each: deployment frequency, lead time for
   changes, change failure rate, and time to restore. The four that matter, defined
   precisely enough to compute from the pipeline's own records.
2. **Reliability objectives** per user-facing capability, each with its SLI (what is
   measured, numerator and denominator), the target, and the window.
3. **Error budget and its policy**: what happens when it is exhausted — freeze, escalate,
   or accept. A budget with no policy is a dashboard.
4. **Security requirements**: secret handling, least privilege, network exposure, patch
   cadence, and audit trail, each with a verification method.
5. **Compliance requirements** with their source and evidence artifact.
6. **Non-goals**, and the requirement each deferred capability would have needed.
7. **Which requirements are testable in this repository** and which need a live
   environment — stated up front, because `DI-P07` inherits the distinction.

Out of scope: architecture choices, pipeline design, monitoring implementation.

## 3. Prerequisites and inputs

- `{{PROJECT_PATH}}` — the repository and `DI_CONTEXT.md` from `DI-P01`. The incident
  history there is the fairest source of a restoration target.
- `{{SLO_TARGETS}}` (optional) — existing commitments from contracts or a service
  catalogue. If absent, derive from the incident history and mark each target `proposed`.
- `{{COMPLIANCE_SCOPE}}` (optional) — the regime. If absent, record `unstated`.
- `{{ERROR_BUDGET_POLICY}}` (optional) — the organisational rule. If absent, propose one
  and mark it `proposed — needs owner approval`.

## 4. Workflow

1. **Define each delivery metric with its formula and its data source.** "Lead time" is
   the time from first commit on the merged branch to running in production, computed from
   the pipeline's timestamps; if the pipeline does not record those timestamps, the
   requirement states that the data source must be added. A metric nobody can compute is
   not a target.
2. **Write SLIs as ratios.** Successful requests over total valid requests, excluding
   client errors that are the caller's fault and including timeouts as failures. State the
   exclusions explicitly — an SLI that quietly excludes the failures users notice is worse
   than none.
3. **Set the target from evidence.** The best target is the currently measured value,
   improved by a stated amount; the second best is the contract. Do not invent 99.99 %
   because it sounds professional — every nine multiplies the cost.
4. **Attach a window and an owner to each objective.** 30 days rolling is common; whatever
   you choose, the same window is used in the measurement or the numbers will disagree.
5. **Write the error-budget policy with a trigger.** "When more than 50 % of the monthly
   budget is spent, feature work pauses and reliability work is prioritised, decided by
   the service owner" is a policy. "We monitor the budget" is not.
6. **State security requirements as verifiable properties**: every credential federated
   rather than long-lived, no secret in any repository or plan output, no resource reachable
   from the internet without an explicit allowlist entry, and each with the check that
   proves it.
7. **Separate what this repository can test from what it cannot.** Pipeline conformance,
   secret scanning, plan review, and configuration checks are testable offline; latency and
   availability need a live environment. That split is `DI-P07`'s scope, so it is decided
   here rather than discovered there.
8. **Write the non-goals** and, for each, the requirement it would have imposed — that line
   is what stops the non-goal from being reversed silently in six months.

## 5. Decision rules and evidence standard

- **A requirement without a measurement is a preference.** Every line has a number, a
  formula, or a check that can fail.
- **Targets are proposed until an owner accepts them.** Mark them `proposed` and name who
  must accept; an unowned target is not a commitment.
- **Availability is measured at the user's boundary,** not the server's CPU. An SLI that
  measures what is easy to measure optimises the wrong thing.
- **Every nine costs evidence.** Raising a target requires a stated mechanism and its
  cost; otherwise it is a wish with a decimal point.
- **Restoration time comes from the incident history,** not from ambition. If the last
  three incidents took four hours, a one-hour target needs a stated change that delivers it.
- **Security requirements are properties, not tools.** "We use Vault" is not a
  requirement; "no secret exists in any repository, plan output or CI log" is.

## 6. Verification

- Four delivery metrics, each with formula, data source and current value or `no data`.
- Each SLI states numerator, denominator and exclusions; each target has a window.
- Error-budget policy has a trigger, an action and a decision owner.
- Security requirements are stated as testable properties with their check.
- Compliance requirements cite their source and their expected evidence.
- Each target marked `proposed` or `accepted by <owner>`.
- Non-goals listed, each with the requirement it defers.
- The testable-vs-live split is written down for `DI-P07`.

## 7. Failure handling

- **No metrics exist yet.** Record `no baseline`, set the target as `proposed` from the
  contract or the incident history, and make instrumenting the SLI the first requirement
  of the implementation — otherwise every later claim of meeting the target is unfalsifiable.
- **Nobody will own a target.** Record the requirement, name the role that must own it,
  and mark the requirement `blocked — no owner`. Do not silently drop it: an unowned
  availability target becomes an unowned outage.
- **A target is unachievable with the current architecture.** Say so, give the arithmetic
  (for example: single-AZ database caps availability well below three nines), and route
  the choice to `DI-P03` as a constraint rather than pretending the requirement is met.
- **Compliance scope is unknown.** Record `unstated`, list the requirements that would
  change if it were, and flag it as the highest-impact unknown in the document. Do not
  assume "none" because nobody said.
- **The business wants a number the estate cannot measure.** Record the requested number,
  the measurement cost, and the interim proxy with its limitations. Do not report a proxy
  as the target.

## 8. Security and authorisation

Risk class A. Requirements may state that secrets must not exist in repositories, plans or
logs; make sure this document does not contain one either. Do not quote customer
contract terms verbatim if they are confidential — cite the clause location and summarise
the obligation.

## 9. Completion criteria

- [ ] Four delivery metrics with formulas and data sources.
- [ ] SLI per capability with numerator, denominator, exclusions and window.
- [ ] Error-budget policy with trigger, action and owner.
- [ ] Security requirements as testable properties, each with a check.
- [ ] Compliance requirements with sources and evidence.
- [ ] Every target `proposed` or accepted, with the owner named.
- [ ] Non-goals with their deferred requirements.
- [ ] Testable-here versus needs-live-environment split recorded.

## 10. Deliverables and handover

`DI_REQUIREMENTS.md`. `DI-P03` takes the reliability targets as design constraints and the
blast-radius tolerance as a topology input. `DI-P04` takes the delivery metrics as pipeline
requirements — if lead time is a target, the pipeline must record the timestamps to compute
it. `DI-P06` takes the SLIs to instrument. `DI-P07` takes the testable split as its scope
boundary, and must not be blamed later for requirements that were declared untestable here.
