# PROMPT 01 — Time and Date Correctness Audit

**Identifier:** TIME-01
**System:** 02-engineering/time-correctness
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A (read-only audit; corrections are separate changes)
**Depends on:** none
**Produces:** `TIME_AUDIT.md`, a defect register, boundary tests
**Inputs:** REPO_PATH, PRODUCT_TIME_ZONES (optional: DATABASE, SCHEDULER, TARGET_ENV, REPORTING_PERIODS)
**Est. effort:** 2–5 h

---

## 1. Role and mandate

You find the places where this system is wrong about time — and every system is wrong about time somewhere.

The defects are quiet and expensive: a report that is off by one day at month-end, a subscription that renews an hour early after a DST change, a "last 30 days" filter that returns 31, a scheduled job that runs twice or never on the transition day, a timestamp stored without an offset that means three different instants depending on who reads it.

None of these throw. All of them produce a number that looks plausible and is wrong.

## 2. Objective and scope

**Produce:** an inventory of time-bearing data and logic, a defect register with reproductions, boundary tests at DST and month-end, and a rule set for the codebase.

Out of scope: timezone database updates (an ops concern), and calendar/holiday business rules owned by the product.

## 3. Prerequisites and inputs

- `{{REPO_PATH}}` with schema, API handlers, scheduled jobs, and reporting queries.
- `{{PRODUCT_TIME_ZONES}}` — where users are, and whether they have a "local day" concept (billing dates, streaks, daily digests). A "local day" is where most bugs live.
- `{{DATABASE}}` — the column types actually in use (`timestamp`, `timestamptz`, `datetime`, epoch integers, strings).
- `{{SCHEDULER}}` — cron/timezone settings; `{{REPORTING_PERIODS}}` — the periods that must be exact (month, fiscal quarter, week starting on which day).
- `{{TARGET_ENV}}` — audit and test in a copy; do not create test data in production.

## 4. Workflow

1. **Inventory the three representations** and how they convert: storage (UTC instant, local wall-clock, date-only), transport (ISO 8601 with offset, epoch, string), and display (user timezone, locale format). A bug exists wherever the conversion is implicit.

2. **Classify each column and field**:
   - **instants** (a moment in time) → must be stored as UTC with an offset type (`timestamptz`, `TIMESTAMP WITH TIME ZONE`) or epoch;
   - **wall-clock events** (a meeting at 09:00 local) → store the local time **and** the zone, not an instant;
   - **dates without time** (a birthday, an invoice date) → store `date`, never a midnight timestamp, or it will shift a day in another zone.

   Mixing these three is the root cause of most defects.

3. **Search for the specific anti-patterns**:
   - naive timestamps compared against zoned ones (often an implicit server-timezone conversion);
   - `now()` used inside pure functions, making results unreproducible;
   - arithmetic on dates using seconds (`+ 86400`) instead of calendar arithmetic, which breaks across DST;
   - `BETWEEN` on timestamps for date ranges, which excludes the last day's final instant;
   - "last N days" computed as `now - N*24h` when the product means N calendar days;
   - formatting with the server's locale and timezone for a user somewhere else;
   - month arithmetic using `setMonth()`-style logic that overflows (31 Jan + 1 month);
   - sorting or grouping by a formatted string.

4. **Test the boundaries explicitly**, because normal dates never fail: 23:30 and 00:30 around a DST spring-forward and fall-back; the transition hour itself (02:30 on the spring-forward day does not exist; 01:30 on the fall-back day happens twice); month-end (31st), leap day, year boundary, and the ISO week boundary; a user in UTC+14 and one in UTC-11 looking at the same report.

5. **Check the scheduler separately** (`JOBS-01` covers mechanics): a job pinned to 02:30 local time skips or doubles at DST; a "daily" job without an explicit zone fires per server default. Verify the next five run times in the target zone, including the transition.

6. **Check the API contract**: are timestamps returned with an offset? Does the client assume UTC? Does an "updated_at" that is a naive string get parsed as local by a browser? A contract without an offset forces every consumer to guess.

7. **Check the stored data for evidence of past bugs**: timestamps at exactly midnight UTC for date-only fields, clustered at 00:00 or 23:59, monotonic gaps of exactly one hour on DST days, and records whose created/updated ordering is impossible.

8. **Write tests that would have caught each defect**, using frozen clocks (inject the clock rather than reading the system one) so the test is deterministic.

9. **Write the rule set in one page**: store instants in UTC with a zone-aware type; store wall-clock and date-only distinctly; convert only at the boundary; inject the clock; do calendar arithmetic with a library, not with seconds; always format with an explicit zone and locale.

10. **Write `TIME_AUDIT.md`**: inventory, defect register with reproduction and user impact, the boundary test suite, and the rules adopted.

## 5. Decision rules and evidence standard

- **An instant is not a date, and a wall-clock event is not an instant.** Classify before fixing.
- **Store UTC, convert at the edges**, and only once.
- **Calendar arithmetic is not second arithmetic.**
- **Every test freezes the clock**; a test that reads `now()` is not reproducible.
- **Dates in ranges are half-open**: `>= start AND < next_day_start`.
- **The database type is the enforcement mechanism**; application discipline is not.
- **A defect needs a reproduction on a boundary date**, or it is a suspicion.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Inventory complete | Schema + code search | Every time column classified |
| Type audit | Schema inspection | Instants zoned, dates typed as date |
| Anti-pattern search | Grep + review | Each of the eight patterns checked |
| DST boundaries | Test at spring-forward and fall-back | No double-run, no skip, no wrong day |
| Month-end / leap day | Test | No overflow, no off-by-one |
| Timezone extremes | UTC+14 and UTC-11 | Same instant renders the intended local time |
| Scheduler verified | Next-run computation | Correct across the transition |
| API contract | Response inspection | Offsets present, no naive strings |
| Historical anomalies | Data query | Clusters and one-hour gaps reviewed |
| Clock injection | Code review | No direct `now()` in business logic |
| Rules documented | Document | One page, adopted |

## 7. Failure handling

- **The database stores naive timestamps and cannot be migrated now** → document the implicit assumption (server timezone), enforce it explicitly at the boundary, and add the migration to the backlog with its risk; do not leave it implicit.
- **A bug affects stored data** (dates shifted by an hour) → a correction is a data change: `03-domains/database/` P02 with a snapshot and reconciliation.
- **The product defines "day" differently per feature** → write it down per feature; inconsistent definitions are a product decision, not a bug to guess at.
- **A third-party API returns local times without a zone** → record the assumption, pin the offset in code, and alert on drift.
- **The timezone database is outdated** (a country changed its rules) → update it and re-run the boundary tests; historical timestamps are unaffected, but future scheduling is.
- **A test fails only in one timezone** → the test environment is part of the bug; set `TZ` explicitly in CI to expose it.

## 8. Security and authorisation

Risk class A: read-only audit. Test data must be synthetic; querying production for anomalies must be read-only and must not export personal records. Do not change system clocks in a shared environment — freeze the clock in the application instead.

## 9. Completion criteria

- [ ] All time-bearing columns and fields classified as instant, wall-clock, or date.
- [ ] Eight anti-patterns checked with file references.
- [ ] Boundary tests written and passing at DST, month-end, leap day, and year boundary.
- [ ] Timezone extremes verified (UTC+14, UTC-11).
- [ ] Scheduler next-run times verified across a transition.
- [ ] API responses carry offsets; no naive timestamp strings.
- [ ] Historical anomalies reviewed and explained.
- [ ] Clock injection used in business logic.
- [ ] One-page rules document adopted.
- [ ] Defect register written with impact and reproductions.

## 10. Deliverables and handover

Artifacts: `TIME_AUDIT.md`, boundary test suite, rules document.

Handover: defects route to the owning system (billing → `03-domains/payments/`, reporting → `03-domains/data-engineering/`, scheduling → `05-scenarios/background-jobs/`); the rules join the coding standards referenced by `04-process/code-review/`; the boundary tests go into CI with an explicitly set timezone, because a suite that passes only in the author's zone is not a suite.
