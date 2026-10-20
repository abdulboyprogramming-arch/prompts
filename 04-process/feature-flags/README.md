# Feature Flags

**Maturity: operational (v1.0.0).** Five stages that treat runtime switches as production controls with a lifecycle, not as a permissive hack that never gets cleaned up.

**Entry point:** [`P01-Inventory/P01-Flag-Inventory-Risk.md`](P01-Inventory/P01-Flag-Inventory-Risk.md) to see what you have; [`P02-Design/P02-Flag-Design-Defaults.md`](P02-Design/P02-Flag-Design-Defaults.md) to add one properly.
**Execution mode:** diagnostic  
**Per stage:** diagnostic (P01), planning (P02), implementation (P03, P05), specialised (P04)
**Risk class:** A → B → C — P01 is read-only; P03 and P04 change production behaviour

## Why this system exists

A feature flag is a branch that bypasses code review, deployment approval, and version control. It is enormously useful and it rots silently:

- **Flags outlive their purpose.** The release flag from two quarters ago is still there, still read, and the losing branch is code nobody has executed since.
- **Kill-switches are never tested.** The control you plan to use at 3 a.m. has never been flipped, and its off-path no longer builds the current product shape.
- **Defaults are unsafe.** The provider is unreachable during an outage — which is exactly when flags are evaluated — and the default turns the risky path *on*.
- **Permissions hide in the flag service.** A boolean that gates a paid capability is an authorisation decision editable by whoever has console access, with no review and no audit.
- **Rollouts measure noise.** Percentage ladders that last an hour on a service doing a hundred requests a day, thresholds chosen after looking at the graph.

This system makes the set visible, the defaults safe, the rollout measurable, the switch usable, and the removal routine.

## Stages

| ID | Stage | Purpose | Produces |
|----|-------|---------|----------|
| FF-P01 | [Inventory & risk](P01-Inventory/P01-Flag-Inventory-Risk.md) | Reconcile code, provider, and config; classify by purpose; audit kill-switches; rank by consequence | `.flags/FLAG_INVENTORY.md` |
| FF-P02 | [Design & defaults](P02-Design/P02-Flag-Design-Defaults.md) | Justify the flag, type it, make the default safe, name an owner and an expiry | `.flags/FLAG_DESIGN.md` |
| FF-P03 | [Progressive rollout](P03-Rollout/P03-Progressive-Rollout.md) | Pre-declared thresholds, cohort ladder, sample-size reasoning, tested reversal | `.flags/ROLLOUT_LOG.md` |
| FF-P04 | [Kill-switch use](P04-Kill-Switch/P04-Kill-Switch-Use.md) | Flip under pressure: prediction, one flip, measured effect, recorded residual state | `.flags/SWITCH_LOG.md` |
| FF-P05 | [Retirement](P05-Retirement/P05-Flag-Retirement.md) | Prove the winning state, delete the branch, config, tests, and docs; prevent recurrence | `.flags/RETIREMENT.md` |

## The rules

1. **A flag without an owner and an expiry is permanent behaviour with nobody accountable.**
2. **Default off for risky behaviour; default on only for a kill-switch whose job is to survive a provider outage.** Never a default that enables data-destructive or money-moving paths.
3. **Never gate authorisation with a flag.** Entitlements belong in the policy layer, with review and audit.
4. **Thresholds before data.** A limit chosen after seeing the graph is not a control.
5. **A kill-switch is exercised, not assumed.** Its off-path is the least-tested code in the system, and it is the code you will run during an incident.
6. **Removal deletes the branch, not just the switch.** A leftover conditional on a removed flag silently changes behaviour.
7. **Both states are tested, including the default path.**

## Proportionality

| Situation | Run |
|-----------|-----|
| "Why does production behave differently from staging?" | P01 inventory, then re-check the flags in the diff |
| Shipping a class C/D change behind a switch | P02 design, P03 rollout, P04 as the control, P05 at the end |
| Incident where a flag is the suspected cause or the mitigation | P04, with `05-scenarios/incident-response/` |
| Flag debt review (quarterly) | P01, then a P05 batch prioritised by consequence |
| A permission gate discovered in the flag service | P01 finding → route to the authorisation system; **do not** "retire" it |

## Boundaries

- Deploy, versioning, and post-release verification: `04-process/release-engineering/`.
- The incident itself (command, communications, postmortem): `05-scenarios/incident-response/` and `04-process/observability-reliability/` P05.
- Removing a whole service or asset: `04-process/decommissioning/`.
- Schema or data changes hidden behind a flag: still `03-domains/database/`. A flag does not make an unsafe migration safe.

## What this system will not do

- Give you a flag service. It assumes one exists and that its evaluation semantics matter.
- Decide product entitlement. P01 will find permission gates in the wrong place and route them; it will not design your authorisation model.
- Make a rollout safe that has no reversible state. If the change writes data the old code cannot read, the honest answer is "this is a migration", and the system will say so.
