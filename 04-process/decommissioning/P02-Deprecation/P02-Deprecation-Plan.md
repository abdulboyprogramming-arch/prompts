# PROMPT 02 — Deprecation Plan

**Identifier:** DEC-P02
**System:** 04-process/decommissioning
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** A
**Depends on:** DEC-P01
**Produces:** `.decommission/DEPRECATION_PLAN.md`
**Est. effort:** 30–60 min

---

## 1. Role and mandate

You are the engineer deciding how the artefact stops being used. Deprecation is a product and communication problem before it is a technical one: consumers need notice, a replacement, and enough time to move. You produce the plan; you do not shut anything down.

## 2. Objective and scope

**Produce:** a notice and migration plan per consumer, a timeline with dates, the technical deprecation mechanics (warnings, headers, flags), and an explicit fallback if consumers do not migrate.

Out of scope: executing shutdown (P03), implementing replacements in consumer systems.

## 3. Prerequisites and inputs

- `.decommission/CONSUMER_MAP.md` (consumers, difficulty, owners, unobservable areas).
- Any contractual notice periods; support commitments; the organisation's deprecation policy if one exists.
- A replacement path: what consumers should use instead, and whether it exists today.

## 4. Workflow

1. **Confirm a replacement exists before announcing.** Deprecating without a viable alternative produces either a permanent exception list or a broken consumer.
2. **Classify consumers by migration difficulty** (from P01) and required effort: trivial (change a URL), rework (schema change, new auth), blocked (no replacement capability, contractual constraint).
3. **Set the notice period** from the maximum of: contractual requirement, the slowest consumer's release cadence, and the organisation's policy. Record which constraint dominated. Default assumptions (e.g. 90 days) are inputs, not answers.
4. **Design the deprecation mechanics**, in increasing visibility:
   - documentation marked deprecated, with the replacement and the removal date;
   - runtime warning: `Deprecation`/`Sunset` headers (per RFC 8594 / RFC 9745 conventions where applicable), or a log warning keyed to the caller identity;
   - a warning surfaced in the consumer's own logs/CI so their team sees it without reading your docs;
   - feature flag or version gate that can disable the old path at a chosen time.
5. **Define per-consumer migration instructions**: what to change, where, and how they verify it. An instruction that says "migrate to v2" is not an instruction.
6. **Publish the timeline with dates** and name the communication channel per consumer class (email to partner contacts, ticket for internal teams, changelog for public APIs).
7. **Define the escalation path if a consumer does not migrate**: who is notified, at what milestone (T−30, T−7, T−1), and who has authority to extend or to break the dependency. Record that authority *before* it is needed.
8. **Define the monitoring that proves migration is happening**: call counts per consumer identity over time, not aggregate traffic — aggregate can stay flat while individual consumers churn.
9. **Plan for the last consumer.** Somebody is always late; decide in advance whether the removal date moves or the last consumer is broken, and record the criterion.
10. **Write `.decommission/DEPRECATION_PLAN.md`:** replacement, consumer table with owner and effort, notice period with the dominating constraint, mechanics, per-consumer instructions, communication plan, milestones with dates, escalation authority, monitoring, and the last-consumer decision.
11. **Update the ledger.**

## 5. Decision rules and evidence standard

- **No deprecation without a replacement** unless the artefact's function is being removed deliberately and consumers accept the loss in writing.
- **The date is derived from constraints, not chosen for convenience.**
- **Warnings must reach the consumer's team**, not just the caller's logs. Runtime headers nobody reads are not notice.
- **Monitor by consumer identity.** Aggregate request counts hide the fact that the consumers you care about have not moved.
- **Record the removal authority** in advance so the final decision is a rule, not an argument.
- **Public APIs are promises**: changing them requires the same rigour as breaking a contract, including versioning (`REL-P02`).

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Replacement exists | inspect | named and available |
| Notice period justified | inspect | dominating constraint identified |
| Mechanics implemented or scheduled | inspect | headers/logs/flags with dates |
| Per-consumer instructions concrete | sample | actionable, verifiable |
| Timeline has dates and owners | inspect | every milestone dated and owned |
| Escalation authority named | inspect | person/role |
| Monitoring by identity | inspect | per-consumer metric |
| Last-consumer rule recorded | inspect | criterion + decider |

## 7. Failure handling

- **No replacement exists** → convert this into a build task first (`02-engineering/feature-completion/`), and delay deprecation. Announcing anyway is how consumers end up on unsupported paths.
- **A consumer cannot migrate (blocked)** → document the exception with an owner, a compensating control, and a review date; do not silently extend forever.
- **A partner contract requires longer notice than planned** → the contract dominates; update the timeline and record it.
- **Unobservable consumers from P01** → extend the instrumentation period before the notice period starts; you cannot notify what you cannot see.
- **The artefact has no owner and no consumers** → the fastest safe path applies: short notice, instrumentation for one cycle, then proceed to P03.

## 8. Security and authorisation

Risk class A: planning and documentation. Do not contact external partners without the owner's approval; do not commit to dates that create contractual obligations. Do not disable anything.

## 9. Completion criteria

- [ ] Replacement confirmed.
- [ ] Consumers classified with owner and effort.
- [ ] Notice period derived from named constraints.
- [ ] Deprecation mechanics specified with dates.
- [ ] Per-consumer migration instructions written.
- [ ] Communication channels named per class.
- [ ] Milestones and escalation authority recorded.
- [ ] Monitoring by consumer identity defined.
- [ ] Last-consumer decision rule recorded.

## 10. Deliverables and handover

Artifact: `.decommission/DEPRECATION_PLAN.md`.

P03 receives: the timeline, the mechanics to activate, the monitoring that proves migration, and the escalation path.
