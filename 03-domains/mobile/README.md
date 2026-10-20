# Mobile Applications

**Maturity: operational (v1.0.0).** Three stages for software that ships to devices you do not control, through a reviewer who is not on your team, with no rollback.

**Entry point:** [`P01-Release/P01-Store-Release.md`](P01-Release/P01-Store-Release.md)
**Execution mode:** implementation
**Per stage:** implementation (P01), diagnostic (P02), planning (P03)
**Risk class:** C (store submission) → A (crash analysis) → B (compatibility)
**Identifiers:** `MOB-P01..P03`

## Why this system exists

Mobile has three constraints that no web-shaped process models correctly:

1. **The client cannot be rolled back.** A staged rollout can be halted and a server can be patched, but the build on a user's phone is permanent.
2. **A third party gates your release.** Review queues, policy changes, and rejections are part of the release process, not interruptions to it.
3. **The fleet is a long tail.** Users run versions from two years ago; the backend must serve all of them or the team must deliberately stop serving the old ones.

The library previously had **no mobile system at all** — store release, symbolication, and version skew were unrepresented.

## Stages

| ID | Stage | Purpose | Produces |
|----|-------|---------|----------|
| MOB-P01 | [Store release & phased rollout](P01-Release/P01-Store-Release.md) | Build identity, halt criterion before rollout, levers that actually exist, post-release journeys | `.release/RELEASE_PLAN.md`, `ROLLOUT_LOG.md` |
| MOB-P02 | [Crash triage & symbolication](P02-Crashes/P02-Crash-Triage.md) | Symbolicated clusters, segmentation, classification, ranking by consequence | `.crashes/TRIAGE.md` |
| MOB-P03 | [Client compatibility](P03-Compatibility/P03-Client-Compatibility.md) | Version matrix, compatibility contract, deprecation schedule, forced-upgrade paths | `.compat/CLIENT_MATRIX.md` |

## The rules

1. **No halt criterion, no rollout.**
2. **You cannot unpublish** — every rollback is a halt plus a server-side lever, or a forward fix.
3. **Symbolicated or not analysed.**
4. **Rank crashes by affected users and critical path**, not raw count.
5. **The client cannot be rolled back; make the server tolerant.**
6. **Every supported version is a test obligation.**
7. **Measure the new version, not the fleet.**
8. **Privacy declarations describe what the app actually collects.**

## Proportionality

| Situation | Run |
|-----------|-----|
| Shipping a build | P01 |
| Crash rate spike | P02, then P01 if a release is implicated |
| Changing an API the app calls | P03 before the change |
| Raising the minimum supported version | P03, with an approver |
| First release of a new app | P01 (signing, metadata, rollout), P02 baseline after |

## Boundaries

- Backend API design and implementation: `03-domains/backend/`.
- Payments inside the app: `03-domains/payments/`.
- General release engineering (versioning, changelogs, CI): `04-process/release-engineering/`.
- Accessibility of the interface: `03-domains/frontend/` (skeleton) and the accessibility audit in the backlog.

## What this system will not do

- Guarantee store approval.
- Replace device-farm testing.
- Advise on store policy disputes — it tells you which lever you have and what it costs.
