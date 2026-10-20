# Embedded & IoT

**Maturity: operational (v1.0.0).** Two stages for software whose failure mode is a device you cannot reach.

**Entry point:** [`P01-OTA/P01-Firmware-OTA.md`](P01-OTA/P01-Firmware-OTA.md)
**Execution mode:** implementation
**Per stage:** implementation (P01, class D), diagnostic (P02, class B)
**Identifiers:** `IOT-P01..P02`

## Why this system exists

Embedded engineering differs from server engineering in ways that change the whole process:

1. **Recovery is physical.** A bricked server is a redeploy; a bricked sensor is a ladder, a technician, and a shipping label.
2. **Power is a correctness constraint.** An update that drains the battery or loses power mid-write is a failure, not an inconvenience.
3. **Silence is the dominant signal.** Devices that stop reporting are the normal symptom of every failure class at once.
4. **There is no in-place edit.** The image is the deployment; atomicity is designed into the bootloader or it does not exist.

The library previously had no embedded coverage at all — `firmware` appeared only in a backlog row.

## Stages

| ID | Stage | Purpose | Produces |
|----|-------|---------|----------|
| IOT-P01 | [Firmware OTA with rollback](P01-OTA/P01-Firmware-OTA.md) | Signed image, atomic slot switch, trial boot, automatic rollback, cohort rollout, recovery cost | `.ota/OTA_PLAN.md` |
| IOT-P02 | [Fleet health & remote recovery](P02-Fleet/P02-Fleet-Health.md) | Health expectations, silence classification, bounded escalation ladder | `.fleet/HEALTH_MODEL.md`, `TRIAGE.md` |

## The rules

1. **No tested rollback, no fleet rollout.**
2. **Never overwrite the running image.**
3. **Power loss is the default test case.**
4. **The bootloader verifies signatures before execution.**
5. **A device that stops reporting has failed**, whatever its last message said.
6. **Check the server before the device.**
7. **Mass commands are gated behind a single device that proves the path works.**
8. **Unknown device state is reported, never assumed healthy.**

## Proportionality

| Situation | Run |
|-----------|-----|
| First OTA capability | P01 — including the bootloader work |
| Pushing a firmware update | P01 rollout stages |
| Devices stopped reporting | P02 triage before any command |
| After a failed rollout | P01 halt → P02 cohort analysis |
| New device class | P02 health model first, then P01 |

## Boundaries

- Server-side reliability and alerting: `04-process/observability-reliability/`.
- Device-cloud API design: `03-domains/backend/`.
- Supply-chain and firmware signing compromise: `05-scenarios/security-incident/`, `03-domains/web3/` P02 for key custody patterns.
- Hardware design, EMC, certification: outside this library.

## What this system will not do

- Make an unrecoverable device recoverable.
- Replace hardware-in-the-loop testing or a bench rig — it tells you what to test on it.
- Certify safety-critical compliance (ISO 26262, IEC 62304); those require domain-specific processes this system does not claim.
