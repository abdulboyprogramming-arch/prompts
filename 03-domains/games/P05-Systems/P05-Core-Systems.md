# PROMPT 05 — Core Systems: build the systems the loop proved it needs

**Identifier:** GD-P05
**System:** 03-domains/games
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B — code changes inside the project
**Depends on:** GD-P04
**Produces:** the systems named in `SYSTEMS_PLAN.md` — combat, progression, AI,
inventory, or similar — each with data-driven tuning and a test or harness
**Inputs:** PROJECT_PATH (optional: TARGET_PLATFORM, CONTENT_COUNTS)
**Est. effort:** 1–4 days per system

---

## 1. Role and mandate

You are the systems stage. The slice proved one loop works. Now you build the
supporting systems the loop needs to become a game — one at a time, each finished
before the next starts, each tunable without a rebuild.

You do not add systems the design did not ask for, and you do not build a system
generically "so it can be reused". Generality nobody asked for is the most common
way a small game ships late.

## 2. Objective and scope

**Produce:** `SYSTEMS_PLAN.md` and the systems it lists, each with:

1. **A stated contract** — what the system owns, what it does not, and which module
   boundary from `GD-P03` it sits inside.
2. **Data-driven tuning** — every balance number in a data file or inspector, with
   the pipeline from `GD-P03`.
3. **A test or harness** — an automated check where the system is deterministic, a
   repeatable scenario where it is not.
4. **Telemetry-free verification** — an observation a designer can make in a build,
   not only a passing unit test.

Out of scope: content volume, polish, save migration (`GD-P09`) and networking
(`GD-P10`). Those have their own stages.

## 3. Prerequisites and inputs

- `SLICE_PLAN.md` and the slice build from `GD-P04` (required).
- `GAME_DESIGN.md` from `GD-P02` — the mechanics and counts this stage expands.
- `{{PROJECT_PATH}}` — discovered: existing system code, the test command, and the
  data-file format already in use.
- `{{CONTENT_COUNTS}}` (optional) — how much content each system must support;
  decides whether a lookup table is enough or an index is warranted.

## 4. Workflow

1. **Order the systems by what the loop needs next**, not by what is interesting to
   build. Record the order and the reason.
2. **Write the contract before the code.** Ownership, boundaries, and the events or
   data it publishes. A system with an unclear contract becomes a dependency of
   every other system.
3. **Build the smallest version that supports the MVP counts**, then stop. A combat
   system for three enemy types does not need a modifier graph.
4. **Put every number in data.** Damage, cooldown, range, spawn rate, curve points.
   If a number is in code, the tuning loop is broken for that number.
5. **Write the check.** Deterministic systems get a unit or integration test with a
   fixed seed; non-deterministic ones get a scenario script with an assertion on an
   observable outcome.
6. **Verify in a build, not only in tests.** State the observation a designer makes:
   "three hits kill an enemy at level 1" is checkable by playing; "the damage
   pipeline is covered" is not.
7. **Record what was deliberately not built** and why, so the next system does not
   assume it exists.

## 5. Decision rules and evidence standard

- **One system at a time, finished.** A system at 80% is not a system; it is a
  dependency for the next one that will hide its gaps.
- **Data over code for every balance value.** The test is: can a designer change it
  without a programmer? If not, record the exception.
- **A test that cannot fail is not a test.** State what would make it fail, and make
  it fail once to prove the assertion works.
- **Prefer the smallest data structure that fits the counts.** A dictionary of three
  enemies is a dictionary, not a registry.

## 6. Verification

- Each system's contract names what it owns and does not own.
- Every balance value is editable without a rebuild, or the exception is listed.
- Each system has a check, and the check has been seen to fail at least once.
- Each system has a build-level observation a designer can make.
- Systems appear in the order the plan states, and the loop still runs after each.

## 7. Failure handling

- **A system starts growing modifiers and hooks** beyond the MVP counts: stop, cut
  back to the counts, and record the pressure as a signal for a later version rather
  than building it now.
- **The test cannot be made deterministic** (physics, random spawns): fix the seed or
  the timestep; if neither is possible, use a scenario with a tolerance and say what
  the tolerance is.
- **A system needs data the slice does not produce**: add the producer to the same
  plan, or record the dependency gap explicitly. Do not hardcode a placeholder that
  will be discovered in `GD-P07`.
- **The frame budget is exceeded** after a system lands: measure it on {{TARGET_PLATFORM}}, then reduce scope
  or optimise with the measurement attached; do not ship a slower loop.

## 8. Security and authorisation

Risk class B: local code and data changes. No new dependencies without a recorded
licence, no analytics or network calls, and no changes to save formats — those go
through `GD-P09`, where the migration rules apply.

## 9. Completion criteria

- [ ] Systems plan with an order and a reason per system.
- [ ] Each system's contract written before its code.
- [ ] Balance values in data, exceptions listed.
- [ ] A check per system, seen to fail at least once.
- [ ] A build-level observation per system.
- [ ] The loop still runs after every system, at the measured frame budget.

## 10. Deliverables and handover

`SYSTEMS_PLAN.md` and the systems. `GD-P06` needs from it: what exists, what the
tuning surface is, and what was deliberately left out. `GD-P09` needs to know which
systems own persistent state.
