# PROMPT 02 — Crash Triage and Symbolication

**Identifier:** MOB-P02
**System:** 03-domains/mobile
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A (reads crash data and build artefacts; no store actions)
**Depends on:** none
**Produces:** `.crashes/TRIAGE.md`, a ranked fix list, a symbolication check
**Inputs:** APP_ID, PLATFORM (optional: RELEASE_VERSION, CRASH_SOURCE, SAMPLE_SIZE, TARGET_ENV)
**Est. effort:** 1–3 h per triage cycle

---

## 1. Role and mandate

You turn a pile of crash reports into a ranked, evidenced list of defects and a decision about whether to roll back, hotfix, or wait.

Mobile crash data is uniquely hostile to analysis: symbolication fails silently, the dominant crash is often a third-party SDK, one device model can dominate the count, and the version that crashes may be three releases old because most users never update. Treating the top line of a dashboard as "the bug" produces fixes that change nothing.

## 2. Objective and scope

**Produce:** a symbolicated, deduplicated crash inventory; a ranking by affected users and business impact (not raw count); a classification of each cluster (our bug / dependency / OS / device-specific / data corruption); and a recommendation.

Out of scope: implementing the fix, store submission (`MOB-P01`), performance work.

## 3. Prerequisites and inputs

- `{{APP_ID}}`, `{{PLATFORM}}`, `{{RELEASE_VERSION}}` — and deliberately compare against the **previous** version.
- `{{CRASH_SOURCE}}` — Crashlytics / Sentry / Play vitals / Xcode organiser / App Store Connect; each aggregates and samples differently.
- `{{SAMPLE_SIZE}}` — how many reports you actually have, so a 3-crash cluster is not mistaken for a trend.
- `{{TARGET_ENV}}` — production, beta, or internal track.
- **dSYM / mapping files** for the exact build under analysis. Without them, the stack trace is addresses and the triage is a guess.

## 4. Workflow

1. **Verify symbolication before interpreting anything.** If frames show raw addresses or `???`, fix the symbol upload first. A triage built on unsymbolicated data is fiction with numbers attached.

2. **Establish the denominator.** Crash-free *sessions* and crash-free *users*, per version, for the same window. A crash affecting 40 users once can outrank one affecting 4,000 sessions if sessions per user differ; state which metric you are ranking by.

3. **Deduplicate into clusters** by (exception type + top application frame + version + OS major + device class). Then check whether the largest cluster is actually one bug or five with the same signature — common in generic `NullPointerException`/`EXC_BAD_ACCESS` crashes.

4. **Segment before concluding**: version, OS version, device model, app state (foreground/background/cold start), network conditions, locale, and whether it happens on first launch. A crash concentrated in one OS version is an OS-compatibility bug; spread evenly across devices, it is usually logic.

5. **Classify each cluster**:
   - **our code** — fix in a release;
   - **dependency** — check the SDK's issue tracker and version; upgrading a dependency is a different project than fixing yours;
   - **OS/framework regression** — document, work around, report;
   - **device-specific** (memory pressure, GPU, OEM ROM) — quantify the affected population before spending effort;
   - **data corruption** — escalate immediately: it can persist after the fix and affect users who never see a crash.

6. **Read the stack, then read the *context*.** The frame that throws is rarely the frame that is wrong. Reconstruct the user journey from breadcrumbs, not from the exception message. Ask what precondition the code assumed and which one failed.

7. **Check for a shared trigger** across apparently unrelated clusters — the same null session, the same failed migration, the same offline start. One root cause often presents as five symptoms.

8. **Rank by consequence**: users affected × session-ending × path criticality (login, payment, checkout, save-game) × whether it is new in this release. A crash in the payment flow at 0.2% outranks a background crash at 3%.

9. **Decide and state the option set**: hotfix now, server-side mitigation, roll back the staged rollout (`MOB-P01`), or accept with a monitoring threshold. Each option needs a cost and a time-to-user.

10. **Write `.crashes/TRIAGE.md`**: clusters with counts, segments, classification, root-cause hypothesis with the evidence, ranked actions, and what data would change the conclusion.

## 5. Decision rules and evidence standard

- **Symbolicated or not analysed.**
- **Rank by affected users and critical path**, never by raw crash count.
- **Segment before concluding**; an aggregate hides the population that matters.
- **A hypothesis needs a reproduction or a breadcrumb trail**, not just a plausible frame.
- **Dependency crashes are still your crashes** to the user; the classification affects the fix, not the priority.
- **New-in-release regressions outrank long-standing noise**, because they indicate a change you just made.
- **Small samples are reported as small**, not smoothed into a percentage.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Symbolication complete | Stack frames | Named functions and lines, no raw addresses |
| Denominator stated | Metrics | Sessions and users per version, window defined |
| Clusters deduplicated | Grouping method | Signature + version + OS + device |
| Segmentation done | Table | No conclusion drawn from aggregate alone |
| Each cluster classified | Table | One of the five categories |
| Root cause evidenced | Breadcrumb or repro | Hypothesis tied to data |
| Shared triggers checked | Cross-cluster note | Stated whether one cause explains several |
| Ranking justified | Table | Consequence model applied |
| Options costed | Section | Time-to-user and risk per option |
| Fix verification plan | Section | Crash-free rate target and observation window |

## 7. Failure handling

- **No dSYM/mapping for the build** → obtainable for iOS from Xcode archives; if genuinely lost, triage by breadcrumb and device data only, and mark stack-level conclusions as unavailable. Add symbol-upload verification to CI.
- **The top crash is in a third-party SDK** → reproduce with the SDK's latest version, check its changelog for a known issue, and evaluate removal or replacement; do not patch around it blindly.
- **The crash is not reproducible in-house** → gather device model, OS build, locale, and free storage from reports; attempt a device farm run before declaring it unreproducible.
- **Crash rate rises immediately after a release** → treat as a rollout halt decision first (`MOB-P01`), analysis second.
- **The reports are sampled or throttled** (common on iOS) → state that the absolute rate is approximate and use relative comparison between versions.
- **A crash correlates with data corruption** → stop triage, protect user data: disable the affected feature server-side and design the repair path before the fix.
- **The same cluster reappears after a fix shipped** → check version adoption: the users may simply not have updated. Distinguish "not fixed" from "not adopted".

## 8. Security and authorisation

Risk class A. Crash payloads can contain user data, URLs with tokens, and device identifiers — extract only what the analysis needs and never paste raw payloads into public artefacts. Redact before sharing. Do not use production crash data to reproduce issues on live accounts; use a synthetic account and a staging build.

## 9. Completion criteria

- [ ] Symbolication verified with dSYM/mapping for the exact build.
- [ ] Crash-free sessions and users per version recorded with the window.
- [ ] Clusters deduplicated by the stated signature.
- [ ] Segmentation across version, OS, device, and app state.
- [ ] Each cluster classified into one of five categories.
- [ ] Root-cause hypothesis supported by breadcrumbs or a reproduction.
- [ ] Shared across-cluster triggers checked.
- [ ] Ranking by consequence with the model stated.
- [ ] Options costed with time-to-user.
- [ ] Fix verification target and observation window defined.

## 10. Deliverables and handover

Artifacts: `.crashes/TRIAGE.md`, ranked fix list, symbol-upload gap record if found.

Handover: fixes go to an implementation step with a regression test where the platform allows it; `MOB-P01` owns the rollout decision if a release is implicated; `04-process/observability-reliability/` P03 adds the alert that would have caught this earlier than a user report; a symbolication failure becomes a CI check, not a note.
