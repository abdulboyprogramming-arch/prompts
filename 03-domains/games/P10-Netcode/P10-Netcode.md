# PROMPT 10 — Multiplayer Netcode and Determinism

**Identifier:** GD-P10
**System:** 03-domains/games
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** B (simulation, instrumentation, and local network emulation; live-server changes are C)
**Depends on:** none
**Produces:** `.netcode/DIAGNOSIS.md`, a latency budget, a determinism report
**Inputs:** TARGET_MODE, ENGINE (optional: TICK_RATE, PLAYER_COUNT, REGIONS, REPRO_NOTES)
**Est. effort:** 3–6 h

---

## 1. Role and mandate

You diagnose why a multiplayer game feels wrong — rubber-banding, desyncs, "I shot first and died", abilities that fire twice — and you fix the cause rather than the symptom.

Netcode bugs are unique in that the **evidence is a disagreement between machines**, and every participant experiences a different truth. A replay from one client cannot establish what happened; you need server state, client state, and input timestamps side by side, aligned to a common clock.

## 2. Objective and scope

**Produce:** a diagnosis with measured numbers (latency, jitter, tick alignment, rollback depth), a corrected simulation or replication design where the bug is structural, and a determinism report.

Out of scope: matchmaking, anti-cheat policy, and live server capacity planning (infrastructure belongs to `04-process/observability-reliability/`).

## 3. Prerequisites and inputs

- `{{TARGET_MODE}}` — peer-to-peer, client-server authoritative, listen server, or rollback/rollback-netcode style.
- `{{ENGINE}}` — engine version matters; netcode behaviour changes between engine releases.
- `{{TICK_RATE}}`, `{{PLAYER_COUNT}}`, `{{REGIONS}}` — the conditions under which it fails; `{{REPRO_NOTES}}` — what players report, in their words, which is usually a symptom not a cause.

## 4. Workflow

1. **Reproduce with instrumented latency, not on a LAN.** A LAN test cannot reproduce netcode bugs. Simulate at minimum 80 ms RTT with 20 ms jitter and 1% loss, then 150 ms / 50 ms / 3%: if the bug only appears at the second profile, it is latency-dependent, which narrows the cause immediately.

2. **Record the three clocks**: server tick, client tick, and the input timestamp, on the same timeline. Most "I shot first" disputes are a missing or mismatched timestamp convention, not unfair damage.

3. **Classify the symptom correctly**:
   - **rubber-banding** — client prediction corrected too aggressively, or reconciliation applied to the wrong state;
   - **desync** — two simulations diverge: float determinism, unordered iteration, unseeded RNG, physics stepping;
   - **double-fire** — input replay without idempotency, or an ability applied on both prediction and server confirmation;
   - **phantom hits** — server-side hit validation differing from client-side hit prediction (usually a lag-compensation window);
   - **teleporting players** — snapshot interpolation buffer too small, or delta compression dropping a correction.

4. **Measure the budget**: input-to-photon latency, snapshot interval, interpolation delay, rollback depth (frames), bandwidth per player per second, and CPU time for the simulation tick. State which one exceeds its target before changing code.

5. **Check determinism if the model requires it**: fixed-point or integer maths for simulation state, deterministic iteration order (no hash-map ordering), seeded and synchronised RNG, fixed timestep independent of frame rate, and no wall-clock time inside the simulation. Run the same input log twice and diff the state — a single differing bit is the finding.

6. **Check idempotency of inputs and abilities**: every input carries a monotonic sequence number; replaying a packet must not double-apply; ability activation must be authoritative on one side only, with the other side predicting and reconciling.

7. **Test the adversarial conditions players actually have**: packet reordering, a client pausing and resuming, a host migration or server tick hitch, a player joining mid-match, and a client with a clock that is minutes off (many are).

8. **Fix the cause, not the feel**: increasing the interpolation buffer hides jitter and adds input lag; reducing rollback depth hides desync and causes rubber-banding. Every mitigation trades one symptom for another — state the trade explicitly.

9. **Add the instrumentation that makes the next bug diagnosable**: per-frame network stats overlay, state hash per tick, a recorded input+state log for repro, and a desync dump that includes both sides' state for the same tick.

10. **Write `.netcode/DIAGNOSIS.md`**: reproduction profile, measurements against budget, symptom classification, root cause with evidence, the fix and its trade-off, determinism results, and the regression test that would catch it again.

## 5. Decision rules and evidence standard

- **LAN tests are not evidence.**
- **Three clocks on one timeline** — server, client, and input timestamp.
- **Measure against a budget**; "feels laggy" is a report, not a finding.
- **Determinism requires integer/fixed maths and ordered iteration**; floats across platforms are not deterministic in practice.
- **Every mitigation states what it costs** (input lag, bandwidth, CPU).
- **A desync without a state hash is unfalsifiable**; add the hash first.
- **Fix the structure, not the setting**, when the setting exists only to hide the structure.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Latency profiles reproduced | Emulated network | Bug reproduced at a stated profile |
| Three clocks aligned | Instrumentation | Same-tick comparison possible |
| Symptom classified | Diagnosis | One of the five classes |
| Budget measured | Numbers | Each metric against target |
| Determinism tested | Replay diff | Identical state hashes, or the first divergence located |
| Input idempotency | Replayed packet | No double-apply |
| Adversarial conditions | Test matrix | Reorder, pause, hitch, join, skewed clock |
| Mitigation trade stated | Diagnosis | Cost named |
| Instrumentation added | Build | Overlay, hashes, input log, desync dump |
| Regression test | Automated | Fails on the old build, passes on the new |

## 7. Failure handling

- **The bug cannot be reproduced** → gather player-reported conditions (region, ISP, tick rate, player count), then emulate the worst profile; if still unreproducible, ship instrumentation and wait for a capture rather than guessing.
- **Desync only on one platform** → suspect float behaviour, physics stepping, or thread ordering; compare state hashes at the first divergent tick, not at the end.
- **Latency is fine but players report unfairness** → check lag-compensation windows and server hit validation tolerance; the simulation is correct but the *perceived* fairness is not.
- **The fix increases bandwidth beyond budget** → reduce update size (delta compression, relevance filtering) rather than raising the rate.
- **Rollback depth grows with player count** → the simulation step is too heavy; measure tick CPU before adding more rollback.
- **Host migration loses state** → snapshot the authoritative state at a known tick and resume from it; do not attempt to reconstruct from clients.

## 8. Security and authorisation

Risk class B. Emulated-latency tests run on your own build; never test against live production servers without authorisation. Client-side claims are untrusted by definition — do not trust a client-reported tick, position, or hit for anything authoritative. If instrumentation records player identifiers, treat the logs as personal data and redact before sharing.

## 9. Completion criteria

- [ ] Bug reproduced under a stated latency/jitter/loss profile.
- [ ] Server, client, and input timestamps aligned on one timeline.
- [ ] Symptom classified into one of the five categories.
- [ ] Budget metrics measured against targets.
- [ ] Determinism verified by replay, with first divergence located if any.
- [ ] Input and ability idempotency verified.
- [ ] Adversarial conditions tested.
- [ ] Fix targets the cause; trade-off stated.
- [ ] Instrumentation added for future diagnosis.
- [ ] Regression test demonstrates the fix.

## 10. Deliverables and handover

Artifacts: `.netcode/DIAGNOSIS.md`, instrumentation, regression test, state-hash tooling.

Handover: `04-process/observability-reliability/` P03 adds server-side netcode metrics (tick time, dropped packets, desync count) to alerts; `04-process/testing-qa/` absorbs the replay test into the suite; `GD-P09` is consulted if the fix changes save or session state.
