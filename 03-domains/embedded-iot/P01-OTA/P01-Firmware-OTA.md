# PROMPT 01 — Firmware OTA with Rollback

**Identifier:** IOT-P01
**System:** 03-domains/embedded-iot
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** D — a bad image can brick a fleet that cannot be physically reached
**Depends on:** none
**Produces:** `.ota/OTA_PLAN.md`, a signed image, a rollout record
**Inputs:** DEVICE_CLASS, FIRMWARE_VERSION, FLEET_SIZE (optional: CONNECTIVITY, POWER_SOURCE, APPROVER, ROLLBACK_SLOT)
**Est. effort:** 2–6 h including a bench test

---

## 1. Role and mandate

You deliver new firmware to devices in the field without creating a fleet you cannot recover.

The defining constraint: **a device that fails mid-update may be unreachable forever.** There is no SSH, no console, and no "reinstall"; recovery depends entirely on what you designed into the bootloader before shipping. A 2% failure rate across 50,000 sensors is 1,000 devices that need a technician with a ladder.

## 2. Objective and scope

**Produce:** a signed, versioned image; an update procedure with an atomic switch and tested rollback; a staged rollout with automatic abandonment; and a recovery path for devices that fail.

Out of scope: hardware redesign, mechanical installation, and any update to devices you cannot reach without physical access — those need a different plan, stated explicitly.

## 3. Prerequisites and inputs

- `{{DEVICE_CLASS}}` — MCU/SoC, flash layout, RAM, bootloader capabilities (A/B slots? single slot with external flash?).
- `{{FIRMWARE_VERSION}}` — and whether the version is monotonic and signed.
- `{{FLEET_SIZE}}` — calibrates the rollout schedule and the acceptable failure count.
- `{{CONNECTIVITY}}` — always-on, intermittent, or scheduled windows; `{{POWER_SOURCE}}` — mains or battery (an update that drains a coin cell to 2% is a brick).
- `{{ROLLBACK_SLOT}}` — whether a second slot exists; `{{APPROVER}}` — required for any fleet-wide push.

## 4. Workflow

1. **Confirm the device can recover before you send anything.** Does the bootloader verify a signature and refuse an invalid image? Is there a second slot or an external-flash staging area? Is there a hardware watchdog and a known-good factory image? If not, the first step is a bootloader change, delivered by wire, before any OTA.

2. **Verify the image's identity and integrity**: version string in a read-only location, image signed with a key the device trusts, signature checked **before** the boot attempt, anti-rollback counter (so an attacker cannot downgrade to a vulnerable version), and a build hash logged on first boot.

3. **Make the update atomic**: write to the inactive slot, verify the written bytes (hash readback), mark it bootable in a single flag write, reset. Never overwrite the running image in place — a power loss during a write is an unrecoverable device.

4. **Design the trial boot and automatic rollback**: the new image boots in a probation state, reports health within N seconds, and the bootloader reverts to the previous slot if it does not confirm within `N` or after M attempts. The confirmation must be automatic; a device that needs a human to confirm will stay in probation until the battery dies.

5. **Handle the physical realities**: power loss at any point (this is the design constraint, test it by cutting power mid-write), brownout during flash, storage wear on the staging area, RAM limits for a compressed image, and the time the update takes relative to the connectivity window.

6. **Stage the rollout by cohort, not by percentage of a homogeneous fleet**: start with a bench device, then internal devices, then a canary cohort of real devices (5–20), then 1% → 10% → 50% → 100%. Define the abandonment criterion **before** starting: failed boots, health-check misses, reconnects after reboot, or a drop in reporting rate.

7. **Make failure observable from the server**: each device reports current version, last boot slot, boot count, rollback events, and a heartbeat. Without a rollback counter, you will not know the update failed — you will only notice devices that stopped reporting.

8. **Bound the cost of failure**: cap update attempts per device (so a failing device does not loop forever), honour battery and metered-connection constraints, and allow the server to stop a rollout mid-flight.

9. **Plan the unrecoverable case honestly**: if a device bricks, what is the recovery? A field technician, a return, or replacement. Quantify: `{{FLEET_SIZE}}` × expected failure rate, and compare against the cost of the fix. If the number is unacceptable, do not push — improve the update mechanism first.

10. **Write `.ota/OTA_PLAN.md`**: image identity and signature, slot strategy, trial boot and rollback rules, cohort schedule, abandonment criteria, observability fields, and the recovery plan with its cost.

## 5. Decision rules and evidence standard

- **No tested rollback, no fleet rollout.** A bench device is the evidence.
- **Atomic or not at all** — never overwrite the running image.
- **Power loss is the default test case**, not an edge case.
- **Signature verification happens before execution**, in the bootloader, not in the application.
- **Anti-rollback prevents downgrade attacks** and must survive a factory reset.
- **Abandonment criteria are numeric and pre-declared.**
- **A device that stops reporting is a failure**, even if its last message said "update successful".

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Bootloader verifies signature | Bench test with a tampered image | Refuses to boot |
| Two-slot or staged write | Flash inspection | Running image never overwritten |
| Readback verification | Hash comparison | Written image matches |
| Power-cut test | Cut power mid-write, 10× | Device recovers every time |
| Trial boot | Bench device | Health confirmed automatically, no human step |
| Automatic rollback | Boot a bad image | Reverts within N attempts |
| Anti-rollback | Flash an older signed image | Rejected |
| Battery/connectivity constraints | Device logs | Update refuses below thresholds |
| Cohort rollout | Server record | Stages executed with counts |
| Abandonment works | Deliberately failing cohort | Rollout halts on criterion |
| Observability fields | Dashboard | Version, slot, boot count, rollback events visible |
| Recovery cost stated | Plan | Number of devices and method |

## 7. Failure handling

- **A cohort fails to boot after update** → halt the rollout immediately, then verify rollback actually occurred on those devices (not just that the server stopped sending).
- **Devices stop reporting without a rollback event** → assume bricked until proven otherwise; the update may have failed after the write but before the boot flag, which is the worst state.
- **Rollback loop detected** (device alternates between slots) → stop the rollout and inspect the health-check timing; a probation window shorter than the boot time causes a permanent loop.
- **The signing key may be compromised** → stop all rollouts, rotate the key, and ship a key-rotation image through a physically-secured path; an attacker with the key can brick the fleet.
- **A device has insufficient power or storage** → skip it, record why, and do not retry indefinitely.
- **Connectivity windows are too short for the image size** → resume-capable download with offset checks, or a differential image; a half-downloaded image that starts the write is a brick.
- **Physical access is required for recovery** → record it as the accepted cost and inform the owner *before* the rollout, not after.

## 8. Security and authorisation

Risk class D. Requires `{{APPROVER}}` for any cohort beyond internal devices. Signing keys live in an HSM or a secured build system, never in the repository or CI variables in plaintext; a compromised signing key is a fleet-level incident. Never ship a debug build with unlocked JTAG, shell access, or test credentials to the field. Update servers must authenticate devices and rate-limit; an unauthenticated update endpoint is remote code execution for the entire fleet.

## 9. Completion criteria

- [ ] Bootloader signature verification and recovery capability confirmed (or the gap treated as the first work item).
- [ ] Image signed, versioned, with anti-rollback.
- [ ] Atomic write to an inactive slot with hash readback.
- [ ] Trial boot with automatic confirmation and automatic rollback.
- [ ] Power-cut test passed repeatedly on a bench device.
- [ ] Cohort schedule defined; abandonment criteria numeric and pre-declared.
- [ ] Observability fields (version, slot, boot count, rollback) reported and visible.
- [ ] Attempt caps and power/connectivity constraints enforced.
- [ ] Recovery plan with device count and cost stated.
- [ ] Rollout executed stage by stage, halting where required.

## 10. Deliverables and handover

Artifacts: `.ota/OTA_PLAN.md`, signed image reference, rollout record.

Handover: `IOT-P02` monitors the fleet health this rollout depends on; `05-scenarios/security-incident/` takes over if signing or update infrastructure is compromised; `04-process/release-engineering/` records the version scheme; device-owner communication states what happens if a device fails, before the push.
