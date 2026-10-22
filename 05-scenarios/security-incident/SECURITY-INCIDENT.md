# Security Incident Response

**Identifier:** SECINC-01
**System:** 05-scenarios/security-incident
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** specialised
**Risk class:** D — actions taken here can destroy evidence or alert an attacker
**Depends on:** none; runs in parallel with availability recovery
**Produces:** `.security-incident/INCIDENT_LOG.md`, containment record, evidence index, disclosure decision record
**Inputs:** INCIDENT_ID, DISCLOSURE_OWNER (optional: DETECTION_SIGNAL)
**Est. effort:** hours to weeks

---

## 1. Role and mandate

You are the security incident lead. This is **not** a code review and **not** the same as an availability incident. The priorities are different:

| Availability incident | Security incident |
|-----------------------|-------------------|
| Restore service first | **Preserve evidence first**; containment may intentionally keep a system degraded |
| Fix the cause | Assume the attacker is still present until proven otherwise |
| Communicate status | Communicate carefully — disclosure has legal and safety consequences |
| Root cause in code | Root cause in access, identity, and blast radius |

Your job: contain the compromise without destroying the record of it, establish what was accessed, decide what must be rotated and disclosed, and only then remove the attacker's foothold.

## 2. Objective and scope

**Sequence:** detect and confirm → preserve evidence → contain → scope → eradicate → recover → disclose → learn.

Out of scope: legal advice, regulatory interpretation, law-enforcement liaison (flag these and escalate to the named owner), and code hardening (that is `02-engineering/security-hardening/` once the incident is closed).

## 3. Prerequisites and inputs

| Input | If missing |
|-------|------------|
| The detection signal `{{DETECTION_SIGNAL}}` for `{{INCIDENT_ID}}` (alert, report, anomaly, customer complaint) | Start from the report and treat it as credible until disproven |
| Access inventory: identities, keys, tokens, service accounts, third-party integrations | Cannot scope; begin inventorying immediately — this is the core work |
| Log retention and audit trails | Preserve what exists now, before it rotates |
| A named decision owner for disclosure and for taking systems offline: `{{DISCLOSURE_OWNER}}` | Escalate to get one; the recovery lead cannot also decide disclosure |

## 4. Workflow

### Stage 1 — Confirm and classify (minutes)

1. **Record the detection**: what was observed, when, by whom, and through which signal. Note what is *known* versus *inferred* — this distinction must survive the whole incident.
2. **Confirm it is a security event, not a functional failure.** Signs: unknown identities or sessions, access from unexpected geography, data volumes inconsistent with behaviour, unexpected configuration or permission changes, credentials used after they should have expired, alerts on secret scanning.
3. **Classify severity** by data sensitivity and reach: credentials exposed only → contained quickly; customer data accessed → high; production integrity modified → critical; active attacker with persistent access → critical, and containment decisions get harder.
4. **Open the incident log** with timestamps. Every action from here is recorded: who did what, when, and why. This log is evidence.

### Stage 2 — Preserve evidence (before you change anything)

5. **Snapshot before remediation.** Copy logs, audit trails, authentication records, database state, container images, and relevant configuration to a separate, access-controlled location. Record hashes where practical.
6. **Do not "clean up" the compromise yet.** Deleting the malicious user, revoking the key, or killing the process destroys attribution and may reveal that you noticed, prompting the attacker to act destructively.
7. **Document the artefacts** in an evidence index: name, source, timestamp range, hash, storage location, and who has access.
8. **Preserve in a way that survives**: rotating logs must be copied, short-retention audit logs must be exported, and ephemeral instances must be snapshotted before termination.

### Stage 3 — Contain (and avoid tipping off the attacker)

9. **Choose a containment strategy deliberately:**

   | Strategy | Use when | Cost |
   |----------|----------|------|
   | Immediate hard cut (revoke, block, terminate) | Attacker is causing active damage, or persistence is unknown and spreading | Loses visibility; attacker knows |
   | Silent observation | Damage is bounded and you need to understand the foothold | Requires monitoring capability and a decision owner |
   | Selective containment (one credential, one path) | Scope is understood | May leave other footholds |

10. **Contain at the identity layer first**: revoke sessions and tokens, disable compromised accounts, rotate service credentials — in dependency order, because rotating the wrong key first can blind your monitoring.
11. **Contain at the network and data layer**:  block the source, egress restrictions, read-only mode for affected systems, disable the vulnerable endpoint or feature.
12. **Verify the containment actually works** (attempt the blocked access yourself, or observe the denial in logs). A "blocked" rule that never matched is common.
13. **Do not destroy the instance you need** for forensics; isolate it instead of terminating it.

### Stage 4 — Scope

14. **Build the access map**: which identities were used, what they could reach, what they actually touched (from audit logs), and what data those paths expose. Distinguish *access* from *exfiltration* — and state when you cannot tell.
15. **Look for persistence**: new accounts, added keys, modified CI configuration, scheduled tasks, webhooks, OAuth grants, mailbox rules, and code pushed to repositories.
16. **Check the supply chain direction**: were your credentials used against third parties, or did a third party's compromise reach you? Both change the response.
17. **Determine the initial access vector** if evidence allows; if not, state it as unknown and do not close the incident until containment is robust without that knowledge.
18. **Quantify**: records, customers, and data categories potentially exposed. Where you cannot bound it, say so and treat the maximum as the working assumption.

### Stage 5 — Eradicate and recover

19. **Remove every foothold found**, not just the first: accounts, keys, tokens, grants, scheduled jobs, modified configuration, malicious code. Compare against a known-good baseline (image, IaC state, or repository history) rather than "looking for bad things".
20. **Rebuild rather than clean** where the compromise touched the runtime. A cleaned host is a hypothesis; a rebuilt one is a fact.
21. **Rotate everything that could have been exposed**, in dependency order, and verify old credentials no longer work. Record rotations — never print secret values in the log.
22. **Restore service and verify** with the functionality checks from `REL-P04`, plus a security check: the vulnerable path is closed, not just the session ended.
23. **Keep monitoring for re-entry** with a defined window and named owner. Re-compromise after a partial eradication is common and obvious in hindsight.

### Stage 6 — Disclose and learn

24. **Prepare the disclosure decision record**: what happened, what data, who is affected, what you have done, what you recommend, and which obligations may apply (contractual, regulatory, privacy). Name the decision owner and their decision with a timestamp. **You do not make the legal call**; you make the facts clear enough to make it.
25. **Draft communication that is accurate and does not speculate.** Do not name an attacker, do not claim "no data was accessed" unless evidence supports it, and do not omit the uncertainty.
26. **Run the postmortem** with a blameless timeline, then route the technical cause to `02-engineering/security-hardening/` for remediation with `WF-VERIFY` on the fix, and the process gaps to `07-workflows/continuous-improvement.md`.

## 5. Decision rules and evidence standard

- **Evidence before remediation.** An incident you cannot explain is an incident you cannot prove is closed.
- **Known vs inferred is marked in every statement**, and never upgraded silently.
- **Assume persistence until the baseline comparison proves otherwise.**
- **Rotating credentials is not eradication.** New keys with the same vulnerable path are a re-entry ticket.
- **Do not state "no data was accessed"** without audit evidence; state what you can prove and what you cannot.
- **Containment that is not verified is not containment.**
- **Two competing responders cause damage**: one lead, one log, one decision owner for disclosure.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Evidence preserved before changes | evidence index | timestamps precede remediation |
| Containment verified | attempted access denied | observed |
| Footholds removed against baseline | diff vs known-good | no unexplained differences |
| Credentials rotated and old ones dead | test old credential | rejected |
| Access vs exfiltration separated | audit analysis | stated with evidence or uncertainty |
| Disclosure decision recorded | decision log | owner + timestamp |
| Re-entry monitoring active | alert configured | named owner and window |
| Incident log complete | read chronologically | every action attributed |

## 7. Failure handling

- **No audit logs / logs already rotated** → state the blindness explicitly; containment must then assume the worst case, and the incident cannot be closed as "fully scoped".
- **Attacker still active during response** → prioritise containment of the highest-impact path; accept reduced visibility and record the trade-off.
- **Compromise reached a third party** → notify through the contractual contact, in parallel with your own containment; do not wait for full scoping.
- **A responder deletes evidence** → record it, stop destructive actions, and note the limitation in the final report rather than hiding it.
- **Insider involvement suspected** → restrict the response team's access to the evidence, involve the designated owner, and do not confront the individual.
- **Regulatory deadline unknown** → escalate immediately; treat the shortest plausible deadline as the planning constraint.

## 8. Security and authorisation

Risk class D. Every containment action requires a named approver for that specific action. Do not access systems or data beyond what the response requires. Do not include secret values or personal data in the incident log — cite locations and record rotation times. Preserve chain-of-custody information if legal action is possible. Never attempt to access the attacker's infrastructure.

## 9. Completion criteria

- [ ] Detection recorded with known/inferred separation.
- [ ] Severity classified.
- [ ] Evidence preserved and indexed before remediation.
- [ ] Containment strategy chosen, applied, and verified.
- [ ] Access map built with access vs exfiltration stated.
- [ ] Persistence search performed across accounts, keys, CI, integrations.
- [ ] Initial vector identified or explicitly unknown.
- [ ] Footholds removed against a known-good baseline.
- [ ] Credentials rotated; old ones confirmed dead.
- [ ] Service restored with the vulnerable path closed.
- [ ] Re-entry monitoring active with an owner.
- [ ] Disclosure decision recorded with owner and timestamp.
- [ ] Postmortem completed; remediation routed with verification.

## 10. Deliverables and handover

Artifacts: `.security-incident/INCIDENT_LOG.md`, evidence index, containment record, disclosure decision record, postmortem.

Handover: technical fixes → `02-engineering/security-hardening/` (with `WF-VERIFY` on the remediation); process/prevention → `07-workflows/continuous-improvement.md`; data consequences → `05-scenarios/data-loss/` if integrity was affected; customer communication → the named owner, not the engineer.
