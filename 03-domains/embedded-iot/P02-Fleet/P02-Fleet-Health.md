# PROMPT 02 — Fleet Health and Remote Recovery

**Identifier:** IOT-P02
**System:** 03-domains/embedded-iot
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** B (reads telemetry and issues bounded remote commands; mass commands are C)
**Depends on:** IOT-P01 (update and rollback design)
**Produces:** `.fleet/HEALTH_MODEL.md`, `.fleet/TRIAGE.md`
**Inputs:** DEVICE_CLASS, FLEET_SIZE (optional: TELEMETRY_SOURCE, HEARTBEAT_WINDOW, TARGET_ENV)
**Est. effort:** 2–4 h to establish; 30 min per triage cycle

---

## 1. Role and mandate

You determine the health of a device fleet from the only evidence available — intermittent telemetry — and you distinguish between the three states that look identical in a dashboard: **healthy**, **silently dead**, and **alive but wrong**.

A server fleet tells you when a process dies. A device fleet tells you nothing when the modem fails, the battery dies, the firmware bricks, or the device is sitting in a warehouse with no SIM. Silence is the most common failure signal and the least informative.

## 2. Objective and scope

**Produce:** a health model with explicit expectations (what a healthy device reports and how often), a triage method that separates the causes of silence, and bounded remote-recovery actions.

Out of scope: pushing firmware (`IOT-P01`), physical maintenance scheduling, and any command that changes device state irreversibly.

## 3. Prerequisites and inputs

- `{{DEVICE_CLASS}}`, `{{FLEET_SIZE}}`, `{{TELEMETRY_SOURCE}}` — what each device actually sends and how it is stored.
- `{{HEARTBEAT_WINDOW}}` — the interval within which a healthy device must be heard from; this is the single most important number in the model.
- `{{TARGET_ENV}}` — production, pilot, or lab; a lab fleet's absence is not an incident.
- `.ota/OTA_PLAN.md` — written by `IOT-P01`; read it before starting rather than re-deriving it.

## 4. Workflow

1. **Define health as an expectation, not a feeling.** For each device class, write: what it reports, how often, what a normal value range looks like, and what it must report after a reboot. Every alert must be traceable to one of these expectations.

2. **Model the three axes**:
   - **Liveness** — heard from within `{{HEARTBEAT_WINDOW}}` × tolerance;
   - **Correctness** — reported values inside expected ranges, with plausible timestamps (clock drift and timezone bugs are endemic);
   - **Version/compliance** — running a supported firmware, with the expected configuration.

3. **Classify silence by cohort, not by device**:
   - a whole site silent → network, gateway, or power at the site;
   - devices shipped in one batch silent → manufacturing or provisioning defect;
   - devices updated in the last 24 h silent → firmware or rollout failure (`IOT-P01`);
   - a single device silent → hardware, battery, or physical removal.

   This classification is the difference between dispatching a technician and restarting a gateway.

4. **Build the baseline before you need it**: normal reporting rate by hour, by site, by model; typical battery drain; typical reboot frequency. Without a baseline, "the fleet looks quiet" is indistinguishable from "the fleet is fine".

5. **Investigate the correlated failures first**: timestamps clustered at the same minute indicate a server-side change (deploy, certificate expiry, broker restart), not 200 simultaneous hardware faults.

6. **Check the boring server-side causes before the exotic device ones**: expired TLS certificate on the broker, DNS change, a queue backing up, a rate limit, a deployment that changed the topic or payload schema. Half of "fleet down" incidents are infrastructure.

7. **Use bounded recovery actions, escalating in cost**: re-request a heartbeat → send a configuration change → reboot the modem → reboot the device → re-provision → dispatch. Each action has a blast radius and an expected response time; state what "it worked" looks like before sending it.

8. **Never send a mass command because the dashboard is empty.** Verify the control path itself with a single device or a lab device first; a broken control path plus a mass command equals a fleet-wide outage initiated by you.

9. **Quantify what remains unknown.** A device that has been silent for 30 days is not "probably fine"; it is a device whose state you do not know. Report the count and the age distribution.

10. **Write `.fleet/HEALTH_MODEL.md`** (expectations, thresholds, baseline metrics, silence classification) and **`.fleet/TRIAGE.md`** (current state, cohorts, hypotheses, actions taken with results, devices requiring physical intervention).

## 5. Decision rules and evidence standard

- **Silence is a signal, not an absence of one** — but it needs a baseline to mean anything.
- **Cohort patterns indicate shared cause**; single-device anomalies indicate hardware.
- **Check the server before the device.** It is faster and more often right.
- **Every remote command has a defined success signal**; otherwise you have not verified anything.
- **Escalate by cost of intervention**, not by intuition.
- **Unknown is a state to report**, not a gap to paper over.
- **A device that is alive but reporting nonsense is down** for the purposes of the users depending on it.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Expectations written | Health model | Report type, interval, ranges per class |
| Heartbeat threshold defined | Config | Numeric, with tolerance |
| Baseline exists | Metrics | Hourly reporting rate by cohort |
| Silence classified | Triage table | Each cohort assigned a cause category |
| Server-side causes excluded | Checks | Cert, DNS, queue, deploy reviewed |
| Correlated timestamps examined | Query | Clustering checked before per-device work |
| Recovery actions bounded | Procedure | Escalation ladder with blast radius |
| Mass commands gated | Procedure | Test device first, approval for mass send |
| Unknown population quantified | Triage | Count and age of silent devices |
| Physical interventions listed | Triage | Devices needing dispatch, with location |

## 7. Failure handling

- **The control path itself is broken** → stop sending commands; fix the path with a lab device before touching the fleet.
- **A whole region goes silent** → check the carrier, the broker, and the DNS record before assuming device failure; carriers change NAT behaviour and IP ranges without notice.
- **Devices report but with wrong values** (stuck sensor, frozen clock) → treat as a correctness failure and add a plausibility check; a frozen clock often indicates a crashed watchdog.
- **Mass reboot does not restore reporting** → the failure is not transient; stop rebooting (it drains batteries and masks the pattern) and investigate the last known state per cohort.
- **A certificate expired** → this is a fleet-wide outage with a known fix; add expiry monitoring with a lead time longer than the update cycle.
- **Devices cannot be reached physically** → record them as lost, with the cost, and exclude them from compliance claims.
- **The count of silent devices grows after a firmware rollout** → treat as an OTA failure (`IOT-P01`) and halt the rollout before continuing triage.

## 8. Security and authorisation

Risk class B; mass commands are C and require approval. Remote commands must be authenticated per device and authorised per action — an unauthenticated command channel is both a safety hazard and a fleet-wide attack surface. Do not exfiltrate device identifiers or site locations into shared artefacts beyond what triage needs. Recovery actions that could disable a device (modem reset on a device with no fallback) are irreversible from your side; treat them as D.

## 9. Completion criteria

- [ ] Health expectations documented per device class.
- [ ] Heartbeat threshold and tolerance defined numerically.
- [ ] Baseline metrics captured (reporting rate, battery, reboot frequency).
- [ ] Silence classified by cohort with causes.
- [ ] Server-side causes checked and excluded.
- [ ] Correlated timestamps analysed.
- [ ] Recovery ladder defined with blast radius and success signals.
- [ ] Mass commands gated behind a test device and an approver.
- [ ] Unknown/silent population quantified with age distribution.
- [ ] Devices requiring physical intervention listed.

## 10. Deliverables and handover

Artifacts: `.fleet/HEALTH_MODEL.md`, `.fleet/TRIAGE.md`.

Handover: `IOT-P01` consumes the rollout failure signal; `04-process/observability-reliability/` P01 takes the heartbeat and certificate alerts into the standard alert set; field operations receives the dispatch list with device locations; a repeated cohort failure becomes a manufacturing or provisioning finding for the hardware owner.
