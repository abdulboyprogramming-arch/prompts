# On-Call Shift Handover

**Identifier:** ONCALL-01
**System:** 05-scenarios/on-call-handover
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** specialised
**Risk class:** B (read-only in practice; class C if the handover authorises changes)
**Depends on:** none
**Produces:** `SHIFT_HANDOVER.md`, an updated alert/silence state list
**Inputs:** TARGET_SERVICE, SHIFT_WINDOW (optional: TARGET_ENV, INCIDENT_REF, ONCALL_ROTA)
**Est. effort:** 10–20 min at each shift change

---

## 1. Role and mandate

You transfer operational responsibility for a defined window to the next responder, so that they inherit **the true current state of the system** rather than a chat message saying "all quiet".

The test of a good handover: the incoming engineer can answer, without asking anyone, *what is broken right now, what is about to break, what changed, what is silenced, and what I would be paged for tonight.*

## 2. Objective and scope

**Produce:** `SHIFT_HANDOVER.md` for the window — open and recent incidents, silences and their expiry, changes and deployments in flight, expiring certificates/tokens/quota, degradations being watched, and the "if this pages you, do this" list.

Out of scope: incident command for an active incident (`05-scenarios/incident-response/`), the postmortem (`04-process/observability-reliability/` P05), project handover (`04-process/handover/`).

## 3. Prerequisites and inputs

- `{{TARGET_SERVICE}}` and `{{SHIFT_WINDOW}}` (start/end and timezone — a handover without a timezone causes real incidents).
- Access to: alerting system (state, silences, active alerts), deploy history, incident tracker, dashboards, and the change calendar.
- `{{TARGET_ENV}}` if multiple environments page; `{{INCIDENT_REF}}` for an ongoing incident; `{{ONCALL_ROTA}}` for who is incoming and who is backup.

## 4. Workflow

1. **Start from the system, not from memory.** Pull, in this order: active alerts and their age, silences (who created them, why, when they expire), deployments in the window, incidents opened or closed, and any error-budget burn.

2. **List what is broken right now**, each with: symptom in one line, when it started, what has been tried, current workaround, and who owns the fix. "Known and accepted" is a valid state — silence without a note is not.

3. **List what is about to break**, with dates: expiring TLS certificates and tokens, database storage or connection limits near threshold, quota exhaustion, deprecation deadlines, scheduled jobs with recent failures, dependency CVEs with a deadline.

4. **Record every silence and its justification.** A silence is a decision to not be paged; the incoming responder must know it exists, who owns it, and what it hides. Silences with no expiry are findings — recommend an end date.

5. **Summarise changes in the window**: what deployed, by whom, what was rolled back, and what is mid-rollout. Include config and infrastructure changes, not just application deploys — a Terraform apply at 17:55 is exactly what the incoming shift needs to know.

6. **State the fragile areas** the incoming responder should watch: recent error spikes, a service running without redundancy, a queue backing up slowly, a noisy alert that everyone ignores. Say which alerts are known-noise, because an alert everyone ignores is a control that has already failed.

7. **Write the "if this pages you tonight" list** — the three to five most likely pages, each with the first diagnostic step and the runbook link. This is the highest-value section and the one most often omitted.

8. **State the open follow-ups with owners and dates**: incident action items, tickets waiting for a deploy, temporary mitigations that must be removed (a flag left off, a rate limit raised, a manual failover).

9. **Do an explicit read-back.** The incoming responder summarises the state in their own words; the outgoing responder corrects. This takes two minutes and catches the misunderstanding that would otherwise be discovered at 03:00.

10. **Hand over authority explicitly**: who may change production during the window, who approves, who is backup, and what the escalation path is if the primary does not answer in N minutes.

## 5. Decision rules and evidence standard

- **State comes from systems, not memory.** Every claim links to an alert, a deploy, a ticket, or a dashboard reading.
- **Silences are decisions and must be justified** with an owner and an expiry.
- **"All quiet" is not a handover.** If nothing is broken, say what was checked and what would have shown a problem.
- **Open follow-ups need owners**, or they vanish at the shift boundary.
- **Temporary mitigations are liabilities**; list each with the condition for removing it.
- **Timezones and dates are explicit** — every time carries its zone.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Active alerts captured | alerting system | each with age and owner |
| Silences listed | alert tool | owner, reason, expiry |
| Changes in window | deploy/config history | all listed |
| About-to-break list | dates checked | certificate, quota, storage, deadlines |
| Known-noise named | review | alerts labelled |
| Top-3-pages section | inspect | diagnostic step + runbook link each |
| Follow-ups owned | tracker | owner and date per item |
| Read-back performed | both responders | incoming restates, outgoing corrects |
| Authority stated | artifact | who may change, who approves, backup, escalation |

## 7. Failure handling

- **An incident is active** → this handover is subordinate to it: the incoming responder joins the incident channel first, then reads the handover for context. Do not hand over a burning system with a document alone.
- **Alerting access is unavailable** → hand over what is observable (logs, dashboards, deploy history) and mark alert state *unknown* explicitly; never imply silence means health.
- **The outgoing responder cannot be reached** → reconstruct state from systems and label every inference; escalate to the on-call lead.
- **The handover grows past a page** → split it: the top third (what is broken, what pages tonight, silences) is read at handover; the rest is reference.
- **A silence belongs to someone who has left** → treat as an orphan: record it, and either adopt it with a reason or remove it in the window with the alert owner's agreement.

## 8. Security and authorisation

Risk class B: read-only. Do not include credentials, customer data, or exploit details in the handover note — it is often stored in a shared channel. Do not silence an alert to make the handover look clean; that is falsifying operational state. Any authority to change production transfers only if the rota and the incident process say so, and it is stated explicitly in the document.

## 9. Completion criteria

- [ ] Shift window and timezone recorded; incoming and backup responders named.
- [ ] Active alerts with age, owner, and workaround.
- [ ] Silences with owner, reason, and expiry.
- [ ] Changes in the window, including configuration and infrastructure.
- [ ] About-to-break list with dates.
- [ ] Known-noise alerts labelled.
- [ ] "If this pages you tonight" list with first diagnostic step and runbook link.
- [ ] Follow-ups with owners; temporary mitigations with removal conditions.
- [ ] Read-back completed; authority and escalation stated.

## 10. Deliverables and handover

Artifact: `SHIFT_HANDOVER.md` for the window (retained for at least the review period — it is the primary evidence for a postmortem that starts "the previous shift knew").

Handover: the incoming responder owns the system for the window; open follow-ups enter the team's tracker the same day; `04-process/observability-reliability/` P05 receives the handover note as evidence when an incident later traces back to a known condition.
