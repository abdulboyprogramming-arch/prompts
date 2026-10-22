<!-- not-a-prompt -->

# A Worked Multi-Agent Run — two agents, one frozen interface, and the drift that unit tests cannot see

**Status:** teaching document · **Date:** 2026-10-21 · **Backlog:** #109
**Companions:** [`multi-agent-orchestration.md`](multi-agent-orchestration.md) defines the rules; this file shows one run where a rule was missing.

---

## Why this file exists

`WF-MULTIAGENT` states that interfaces must be frozen before parallel work and that cross-agent interference must be audited afterwards. Both statements were assertions. Nothing in the repository showed what interface drift looks like when it happens, how it is detected, or what the recovery costs — so "freeze the interface" read as a formality rather than the whole point.

This is a constructed run, assembled to be representative rather than observed in one company. It is labelled that way in the same spirit as `failure-examples.md`: the failure modes come from the orchestration prompt's own pathology list, not from a single incident report.

---

## The task, and the decomposition

A notifications feature. Two agents, one week:

| | Agent A | Agent B |
|---|---|---|
| Objective | Produce the API endpoint that records a notification and emits an event | Build the worker that consumes the event and sends the email |
| Owned paths | `src/api/notifications/` | `src/workers/email/` |
| Forbidden paths | `src/workers/`, manifests, migrations | `src/api/`, manifests, migrations |
| Verification | `pytest tests/api/notifications` | `pytest tests/workers/email` |
| Deliverable | endpoint plus tests | worker plus tests |

**The frozen interface** — committed to `ORCHESTRATION_PLAN.md` before either agent started:

```
event: notification.created  (v1)
fields:
  id            string, uuid
  recipient     string, email
  template      string, one of: welcome, reset, receipt
  created_at    string, RFC 3339
```

Both agents were given the same block. Neither was allowed to change it; changes went through the orchestrator and the decision log.

## What actually happened

| Day | Agent | Action | Evidence in the run log |
|---|---|---|---|
| 1 | A | Builds the endpoint, emits `notification.created` with `template` | unit tests green |
| 1 | B | Builds the worker, reads `payload["template"]`, renders it | unit tests green, fixtures built from the frozen block |
| 2 | A | Finds `template` insufficient — product wants per-notification overrides — and adds **`template_id`** as a *required* field | "added template_id for override support", reported as **done**, not as *deviated* |
| 3 | B | Runs its own suite against its own fixtures: green | green |
| 3 | Orchestrator | Integrates both branches | integration test **fails** |

**The drift was three inches wide and invisible from both sides.** A's suite asserted that `template_id` was present. B's suite asserted that a payload built from the frozen block rendered. Neither suite ever saw the other's payload, so each was correct and the system was broken.

## How it surfaced, and how nearly it did not

The integration test caught it because it asserted on the **rendered email body**, not on the event. Had it asserted that an event arrived, the run would have shipped a worker that sends an empty template — a silent failure that appears in production as blank emails with a successful job status.

That is the specific lesson this example exists to teach: **the drift between two agents is detected by a check that neither agent owns.** Every per-agent verification can pass while the seam is broken, so the integration check has to assert on the *outcome at the seam*, not on the handshake.

## Recovery, in the order performed

1. **Stop dependent work.** The email worker's follow-on task (bounce handling) was cancelled before it started against the broken contract.
2. **Attribute from the artifacts, not from reports.** The decision log had no entry for `template_id`; A's diff did. Attribution took one `git log` and one read of the plan, because both agents had written to paths they owned.
3. **Decide the interface centrally, and write it down.** Two options were on the table: revert A's field, or keep it and teach B to read it. The orchestrator chose a **v2 event with `template_id` optional and `template` retained**, so an old consumer keeps working while the new one gains the field. That is a versioned interface, not a fixed one, and it cost ten minutes.
4. **Have one agent rework, not both.** B added the fallback (`template_id` if present, else `template`) and a test built from **A's serialised payload**, not from the frozen block. A did not touch the worker.
5. **Re-run the seam check first, then both suites.** The seam test passed at 14:20; both per-agent suites passed afterwards. Neither was run before the seam test, because a green unit suite after a contract change is the least informative evidence available.

## The audit that should have run on day 2

The orchestration prompt requires a cross-agent interference audit after integration. Run on the branch history, it would have shown, in twelve minutes:

| Check | Result |
|---|---|
| Files changed outside owned paths | none — the ownership rule held |
| Duplicated helpers | none |
| `ORCHESTRATION_PLAN.md` matches the committed interface | **no — `template_id` is absent from the plan** |
| Any required field added without a decision-log entry | **yes — one** |
| Lockfile or manifest touched by both agents | no |

One row was a violation and it was cheap to find. **The audit was defined and not run**, which is the honest account of this run: the rules existed, the check was skipped because both agents reported done.

## What changed in the workflow as a result

Three rules were added to `WF-MULTIAGENT` after this example, each traceable to a row above:

1. **The frozen interface is a fixture, not a paragraph.** The plan must contain a serialised example payload, and each agent's tests must build their input from *that file*, not from a copy of the schema. A copy is where the drift lives.
2. **A required field is an interface change**, whatever the reason. Adding one is not an implementation detail, and "done" is not an acceptable report for it.
3. **The seam check runs before integration, not after.** It asserts on the outcome at the boundary — the rendered email, the persisted row, the response body — and it belongs to the orchestrator, not to either agent.

## Cost, recorded honestly

| Item | Cost |
|---|---|
| Rework (worker fallback plus test) | ~2 hours |
| Event v2, plan and decision log | ~1 hour |
| Integration debugging | ~40 minutes |
| Work that could have shipped wrong | blank emails with a green dashboard |

The rework was cheap because the seam test existed. A team without it would have paid the same two hours and shipped the defect.

## What this example does not show

- **Three or more agents.** Pairwise drift is the easy case; three agents can produce an interface that is inconsistent in a way no pair reveals, which is why the orchestration prompt forbids direct negotiation between them.
- **A correct run.** This is the failure path. A clean two-agent run is shorter and teaches less.
- **Human gates.** No irreversible action was involved; the same run with a migration would have needed an approval that neither agent could grant.
