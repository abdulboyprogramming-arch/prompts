# PROMPT 01 — Store Release and Phased Rollout

**Identifier:** MOB-P01
**System:** 03-domains/mobile
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** C — publishes to a store; a bad build reaches real users and cannot be recalled
**Depends on:** none
**Produces:** `.release/RELEASE_PLAN.md`, `.release/ROLLOUT_LOG.md`
**Inputs:** APP_ID, PLATFORM, TARGET_VERSION (optional: TRACK, ROLLOUT_PERCENT, MIN_SUPPORTED_VERSION, APPROVER)
**Est. effort:** 1–3 h plus review-queue waiting time

---

## 1. Role and mandate

You ship a mobile release that reaches users in an environment you cannot roll back.

A web deploy is undone in seconds. A mobile release is reviewed by a third party, downloaded by devices you do not control, and — once users update — the old build is gone. Google Play's staged rollout can halt; the App Store cannot, at all. Every decision here is shaped by that asymmetry.

## 2. Objective and scope

**Produce:** a release plan with a signed build, store metadata, a staged rollout, a halt criterion defined *before* the rollout starts, and a post-release verification.

Out of scope: writing features, app design, marketing copy, and any change to store agreements.

## 3. Prerequisites and inputs

- `{{APP_ID}}`, `{{PLATFORM}}` (iOS / Android / both), `{{TARGET_VERSION}}` (semantic or build number — state the scheme).
- `{{TRACK}}` — internal, TestFlight, closed, open, production; `{{ROLLOUT_PERCENT}}` — staged percentage schedule.
- `{{MIN_SUPPORTED_VERSION}}` — the oldest client version the backend still supports; this constrains everything about migration.
- `{{APPROVER}}` — required; a store submission is an outward-facing action.
- Signing material available in CI (never in the repository), store credentials present, and a changelog in the users' language.

## 4. Workflow

1. **Verify the build before the store sees it**: version and build number incremented (iOS build numbers must be monotonic and unique per upload; Android `versionCode` likewise), release signing (not debug), R8/ProGuard or bitcode settings as intended, and no debug endpoints, logging of PII, or test API keys compiled in.

2. **Check the compatibility surface** that this release changes: minimum OS version, removed permissions, new required permissions (each needs a store justification string), changed URL schemes and universal links, and any migration of local data. A local database migration that fails on upgrade is the classic mobile-only outage.

3. **Write the rollout in stages with a defined halt condition before starting**:
   - internal → 5% → 20% → 50% → 100% (Android), or TestFlight → phased release over 7 days (iOS);
   - **halt criterion**: crash-free sessions below X%, a specific fatal in the new build, or a payment/login failure above baseline. Numeric, with the measurement source named.

4. **Prepare the rollback that actually exists**: you cannot unpublish. The available levers are **halt the staged rollout**, **server-side kill switch for the new feature**, **remote config to disable the code path**, and **a forward fix in the next build**. List which levers this release has, and test them before submitting — a feature flag you cannot flip remotely is not a lever.

5. **Prepare store metadata**: release notes in each supported language, screenshots if the UI changed, privacy manifest / data-safety declaration updated for any new data collection, and age rating if content changed. A missing data-safety declaration is a rejection, not a warning.

6. **Submit and record**: submission timestamp, review status, reviewer notes if asked, and the exact build number under review. Never upload a second build during review without cancelling the first — the store may accept the wrong one.

7. **On approval, start the lowest stage** and watch for the declared window before widening. Read the *new-version-specific* crash rate, not the aggregate — a 0.3% aggregate can hide a 12% crash rate in the new build.

8. **Verify the things that only break after release**: login on a fresh install and on an upgrade from the previous version, push notification delivery, deep links from an external app, in-app purchases in the sandbox and production, and background sync after the app is killed.

9. **Handle the review outcomes as first-class paths**: rejection for metadata, for privacy, for a guideline violation, for a crash on the reviewer's device (which you may be unable to reproduce). Each has a different response; a rejection is not a bug report.

10. **Write `.release/RELEASE_PLAN.md`** (build identity, compatibility surface, stage schedule, halt criterion, levers, metadata) and **`.release/ROLLOUT_LOG.md`** (stage timestamps, crash-free rate per stage, halts, decisions, final state).

## 5. Decision rules and evidence standard

- **No halt criterion, no rollout.** Deciding the threshold during an incident is deciding it under pressure.
- **Measure the new version, not the fleet.**
- **A staged rollout is a test with users; treat the first stage as a canary.**
- **You cannot unpublish** — every rollback plan is a halt plus a server-side lever, or a forward fix.
- **Data-safety and privacy declarations are part of the release**, not paperwork to fix later.
- **One build in review at a time.**
- **Minimum supported version is a product decision with a support cost**, not a technical detail.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Build identity | Store console | Version/build monotonic, matches the tag |
| Release signing | Build inspection | Release key, not debug |
| No debug artefacts | Search build | No test endpoints, keys, or verbose PII logs |
| Local migration tested | Upgrade install | Data intact from the previous release |
| Halt criterion recorded | Plan | Numeric, with measurement source |
| Levers tested | Flag/remote config check | Each lever exercised before submission |
| Metadata complete | Store listing | Notes, privacy manifest, screenshots current |
| One build in review | Console | No competing submission |
| Stage 1 observed | Dashboard | New-version crash rate within threshold |
| Post-release journeys | Device tests | Login, push, deep link, purchase, background sync |
| Rollout log current | Artifact | Every stage timestamped |

## 7. Failure handling

- **Crash rate in the new version exceeds the halt criterion** → halt the staged rollout immediately; do not "wait for more data". Then decide: server-side disable or forward fix.
- **Rejected by review** → read the guideline cited, fix the specific issue, and resubmit with a note; do not resubmit unchanged and hope for a different reviewer.
- **The app crashes on the reviewer's device but not yours** → check the reviewer's OS version and locale; if unreproducible, ship a defensive fix or ask for a call through the resolution centre.
- **Apple has no staged rollout below 100% for a critical fix** → use the expedited review request only for a genuine critical issue, and say in the request what breaks without it.
- **The backend must change for the new client** → version the API and keep the old path until `{{MIN_SUPPORTED_VERSION}}` rises (`MOB-P03`). A backend that assumes the new client breaks every user who has not updated.
- **Signing keys are unavailable or compromised** → stop; key rotation and app transfer are their own procedures with store-specific lead times.
- **The rollout log shows an anomaly you cannot explain** → halt first, investigate second.

## 8. Security and authorisation

Risk class C. Store credentials, signing keys, and provisioning profiles never appear in the repository, the session, or a log; they live in CI's secret store. Requires `{{APPROVER}}` before any production submission. Privacy declarations must reflect what the app actually collects — an inaccurate declaration is a regulatory exposure, not a store technicality. Do not enable debug or test backdoors in a production build to "help support".

## 9. Completion criteria

- [ ] Version and build number incremented and monotonic.
- [ ] Release signing verified; no debug artefacts or test keys in the build.
- [ ] Local data migration tested from the previous release.
- [ ] Compatibility surface documented (OS version, permissions, schemes, API min version).
- [ ] Halt criterion written before the rollout starts, with numbers and source.
- [ ] Rollback levers enumerated and each tested.
- [ ] Store metadata and privacy declarations current.
- [ ] Single build in review, recorded.
- [ ] Rollout executed in stages with per-stage crash-free rate.
- [ ] Post-release journeys verified on a real device.
- [ ] Rollout log complete, including any halt and its resolution.

## 10. Deliverables and handover

Artifacts: `.release/RELEASE_PLAN.md`, `.release/ROLLOUT_LOG.md`, the signed build reference.

Handover: `MOB-P02` takes the new version's crash signature baseline; `MOB-P03` maintains the server-side compatibility window this release depends on; `04-process/release-engineering/` holds the versioning and changelog conventions; the support team receives the user-facing notes and the known-issues list at the same time as the store.
