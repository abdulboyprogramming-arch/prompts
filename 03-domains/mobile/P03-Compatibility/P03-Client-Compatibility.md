# PROMPT 03 — API Compatibility with Shipped Clients

**Identifier:** MOB-P03
**System:** 03-domains/mobile
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** B (plans and edits server-side compatibility; breaking a shipped client is a user-facing outage)
**Depends on:** none
**Produces:** `.compat/CLIENT_MATRIX.md`, a deprecation schedule, a forced-upgrade plan
**Inputs:** TARGET_SERVICE, MIN_SUPPORTED_VERSION (optional: CLIENT_VERSIONS, DEPRECATION_WINDOW, APPROVER)
**Est. effort:** 2–4 h

---

## 1. Role and mandate

You keep the backend working for app versions that users still have installed — including versions shipped two years ago that nobody in the team has run recently.

This is the defining constraint of mobile engineering: **the client is a distributed system you cannot upgrade.** A web app is always the latest version; a mobile fleet is a long tail. A backend change that is trivially safe on the web can break 30% of your users, silently, with no rollback available for the client.

## 2. Objective and scope

**Produce:** a client-version matrix (which versions exist, in what proportion), the compatibility contract for each supported version, a deprecation schedule, and a forced-upgrade mechanism with its failure modes.

Out of scope: shipping the app (`MOB-P01`), writing the API (a backend task), app-store policy on forced updates.

## 3. Prerequisites and inputs

- `{{TARGET_SERVICE}}` — the API or backend surface in question.
- `{{MIN_SUPPORTED_VERSION}}` — the oldest version the team intends to support (a business decision with a cost: every supported version is a code path you must test).
- `{{CLIENT_VERSIONS}}` — actual adoption distribution from store analytics, not from assumption; `{{DEPRECATION_WINDOW}}` — how long a deprecation announcement runs before enforcement.
- `{{APPROVER}}` — for raising the minimum supported version.

## 4. Workflow

1. **Build the version matrix from real data**: version → share of active users → platform → OS range → date shipped. Include the fraction that never updates (often 5–15%) and users on versions older than your minimum.

2. **Write the compatibility contract per version**, explicitly: which endpoints, fields, and behaviours each supported version depends on. Anything not listed is not guaranteed, but find out what they actually call before claiming that — clients call undocumented endpoints.

3. **Classify every change** you intend to make:
   - **additive** (new optional field, new endpoint) — safe for old clients if they ignore unknown fields; verify they do;
   - **behavioural** (same field, new semantics) — dangerous; old clients interpret it their way;
   - **removal** (field, endpoint, enum value) — breaking;
   - **tightening** (new validation, new required parameter) — breaking for old clients that omit it.

   Additive is only safe if old clients are tolerant: a client that fails on an unknown enum value makes "additive" a breaking change.

3. **Version the API in a way that supports the tail**: additive changes within a version, breaking changes behind a new major version, and a routing rule that maps client version ranges to behaviour. Do not use "latest" as an implicit contract.

5. **Plan the deprecation as a sequence, not an event**: instrument usage per version → announce in-app and in release notes → provide an upgrade path → monitor adoption → enforce → remove. Each step has a date and a success condition. Skipping instrumentation is how you discover the impact after enforcement.

6. **Design forced upgrade honestly**: a server response that blocks usage below a version, with an in-app message and a store link. Specify what happens when the store is unreachable, when the user cannot update (old OS, no storage), and for users in regions where the store is unavailable. A hard block with no escape hatch strands users; no block at all leaves you supporting a version you cannot secure.

7. **Handle the offline and retry cases**: old clients retry with exponential backoff (or not at all), cache responses, and may run for days without connectivity. A breaking change reaches them not at deploy time but whenever they next wake up — so monitor for a week, not an hour.

8. **Test the contract, not just the current build**: keep a small set of frozen client versions (simulators, device farm images, or recorded request fixtures) and run them against the API in CI. Recorded fixtures from real old clients are cheap and catch most regressions.

9. **Plan the failure you cannot prevent**: if an old client breaks anyway, the levers are server-side feature flags keyed by client version, a compatibility shim, or an emergency forced upgrade. Name which lever exists before you need it.

10. **Write `.compat/CLIENT_MATRIX.md`**: versions and shares, contract per version, change classification, API versioning scheme, deprecation timeline with dates and conditions, forced-upgrade behaviour, and the test fixtures used.

## 5. Decision rules and evidence standard

- **The client cannot be rolled back; the server can. Prefer server-side tolerance.**
- **"Additive" is a claim about client behaviour**, to be verified, not assumed.
- **Every supported version is a test obligation**; if it is not tested, it is not supported — say so and raise the minimum.
- **Deprecation is a schedule with adoption criteria**, not an announcement.
- **Forced upgrade needs an escape hatch** for users who cannot update.
- **Monitor for the tail's timescale** — days, not minutes.
- **Adoption data beats intuition** about which versions matter.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Matrix from real data | Analytics export | Shares sum to the active fleet, dated |
| Contract per version | Document | Endpoints and fields enumerated |
| Change classified | Table | Additive / behavioural / removal / tightening |
| Additive safety tested | Old-client fixture run | Client tolerates unknown fields and enums |
| Versioning scheme defined | Document | Routing rule for version ranges |
| Deprecation steps dated | Schedule | Each step has a date and a success condition |
| Instrumentation exists | Analytics check | Usage per version measurable |
| Forced-upgrade paths | Document | Offline, old-OS, and store-unavailable cases described |
| Old clients in CI | Pipeline | At least one frozen version runs against the API |
| Monitoring window | Plan | At least one full tail period after deploy |

## 7. Failure handling

- **No usage data by version** → instrument first; until then, treat every version as in use and make only additive changes.
- **A breaking change is unavoidable** → release the new major version, keep the old one running for `{{DEPRECATION_WINDOW}}`, and route by client version.
- **An old client crashes because of a new enum value** → this is the classic additive failure; ship a compatibility shim mapping unknown values to a safe default, and record the client behaviour in the contract.
- **Users on unsupported OS versions cannot update** → the forced-upgrade block must offer a degraded read-only mode or a clear explanation; otherwise you have deleted the app for them.
- **The store review delays the client fix** → the server-side shim is the only timely lever; design for it.
- **Adoption does not rise after deprecation announcements** → investigate why (no auto-update, region, device) before enforcing; enforcement may strand a population you did not measure.
- **A third-party integration calls the API** (partner, kiosk, embedded) → it is a client too; add it to the matrix or it will break your deprecation.

## 8. Security and authorisation

Risk class B. Raising `{{MIN_SUPPORTED_VERSION}}` requires `{{APPROVER}}` because it removes access for real users. Forced-upgrade responses must not become a denial-of-service lever for an attacker who can spoof a version header — never trust a client-declared version for security decisions, only for compatibility routing. Do not log full client payloads to diagnose compatibility; they contain user data.

## 9. Completion criteria

- [ ] Version matrix built from analytics, dated, with shares summing to the active fleet.
- [ ] Compatibility contract written per supported version.
- [ ] Every planned change classified, with additive safety verified against a real old client.
- [ ] API versioning scheme and routing rule documented.
- [ ] Deprecation schedule with dates and adoption criteria.
- [ ] Forced-upgrade behaviour defined for offline, old-OS, and store-unavailable users.
- [ ] Frozen old-client fixtures running in CI.
- [ ] Monitoring window covers the update tail.
- [ ] Third-party API consumers included in the matrix.

## 10. Deliverables and handover

Artifacts: `.compat/CLIENT_MATRIX.md`, deprecation schedule, fixture set.

Handover: `MOB-P01` uses the deprecation window when planning releases; backend changes reference the matrix before altering a field; `04-process/observability-reliability/` P03 adds per-version error-rate alerts, because the first symptom of a compatibility break is a spike from one client version.
