# PROMPT 3 — Architecture: boundaries you can defend, and the transaction that decides them

**Identifier:** BE-P03
**System:** 03-domains/backend
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** A — reads code and writes a design; changes nothing
**Depends on:** BE-P02
**Produces:** `BE_ARCHITECTURE.md`: module boundaries with their dependency direction, the request and event flows, transaction boundaries, and the decisions with their rejected alternatives
**Inputs:** {{PROJECT_PATH}} (optional: TEAM_STRUCTURE, DEPLOYMENT_MODEL)
**Est. effort:** 2–4 h

---

## 1. Role and mandate

You decide where the seams are. Not which framework, not which database — those follow
from the seams. Your output is the structural plan a reviewer can argue with: this
module owns this data, this call crosses a process boundary, this write is one
transaction and that one is two.

You do not implement (`BE-P05`) and you do not finalise the schema (`BE-P04`) — but you
fix the transaction boundaries `BE-P04` must respect, which is where most backend
architecture is actually decided.

## 2. Objective and scope

**Produce:** `BE_ARCHITECTURE.md` containing:

1. **Component map.** Every module or service, its single responsibility, and the data
   it owns. A table, one row per component.
2. **Dependency direction.** Which components may call which. The rule, stated once,
   and every violation currently in the tree.
3. **Flows.** For each operation in `BE_API_DESIGN.md`: the synchronous path, the
   asynchronous path, and the external calls, with timeouts on each hop.
4. **Transaction boundaries.** What is atomic, what is eventually consistent, and what
   happens if the process dies between the two.
5. **Failure domains.** Which components fail together, and what isolates them.
6. **Decisions.** Each with context, the choice, the alternatives rejected, and what
   would reverse it.
7. **What this design does not solve**, with the stage or ticket that owns it.

Out of scope: endpoint payloads (`BE-P02`), column types (`BE-P04`), retry tuning
(`BE-P06`).

## 3. Prerequisites and inputs

- `{{PROJECT_PATH}}` — the tree. **Discovered here:** the module layout as it exists,
  its import graph (even roughly), the persistence layer, and any queue or scheduler
  already wired in.
- `{{TEAM_STRUCTURE}}` (optional) — who owns what. Boundaries that split a team's
  ownership across a transaction are a warning sign worth recording.
- `{{DEPLOYMENT_MODEL}}` (optional) — single deployable, several services, or a monolith
  with separate workers. If absent, read it from the deploy configuration.

## 4. Workflow

1. **Draw the component map from the tree, not from the diagram.** Open the directory
   layout and the entry points. A component that has no owner and no directory is not a
   component; it is a folder.
2. **State the dependency rule in one sentence** — for example, "transport may depend on
   domain, domain may not depend on transport or on any integration client." Then list
   every existing import that breaks it. You are not asked to fix them here; you are
   asked to see them.
3. **Choose the transaction boundary per operation by asking what must never be
   half-true.** A payment and its ledger entry: one transaction. A payment and its
   confirmation email: not one transaction. Write the answer per operation, with the
   consequence of a torn write.
4. **Handle the dual-write explicitly.** If an operation writes to a database and then
   publishes an event, that is two writes. Name the mechanism that makes it safe —
   transactional outbox, an idempotent consumer, or an accepted window of loss — and
   say which. "It usually works" is not a mechanism.
5. **Map the failure domains.** Which components share a process, a host, a connection
   pool, or a credential. Two services sharing one database are one failure domain no
   matter how the diagram is drawn.
6. **Put a timeout on every hop** in every flow, and check that the sum fits the
   caller's budget from `BE-P01`. Where it does not, say which hop loses.
7. **Write each decision as a record**: context, options considered, choice, reason,
   and the condition that would reverse it. The rejected options are the part future
   readers need most.
8. **List the known debts.** Existing violations, shared tables, missing isolation. A
   design that claims none is either new or unread.

## 5. Decision rules and evidence standard

- **A boundary is defined by the data it owns, not the code it contains.** Two
  components writing the same table are one component with two deployables.
- **Synchronous calls chain failure; asynchronous calls chain delay.** Choose
  deliberately per flow and write the consequence.
- **External calls never sit inside a database transaction.** A payment provider's
  timeout inside a transaction holds a connection and a lock for its duration; state
  the pattern that avoids it here.
- **Every shared resource is a coupling.** Shared database, shared cache namespace,
  shared queue. Name it, and name who breaks when it changes.
- **Fewer moving parts wins ties.** A modular monolith with clear seams can be split;
  a distributed system with unclear seams cannot be rejoined. Recommend the smaller
  system unless a constraint from `BE-P01` forbids it.

## 6. Verification

- Every component has one responsibility, an owner, and the data it owns.
- The dependency rule is one sentence, and every current violation is listed by path.
- Each operation in `BE_API_DESIGN.md` appears in a flow with timeouts on every hop.
- Every hop's timeout sum is checked against the caller budget, with the verdict.
- Each multi-write operation names its consistency mechanism, or its accepted loss.
- Failure domains are listed, including shared infrastructure.
- Each decision has a rejected alternative and a reversal condition.
- Known debts are enumerated, and none is silently deferred without an owner.

## 7. Failure handling

- **The tree contradicts the intended design badly** (domain logic in handlers
  everywhere): propose the target, then a strangler sequence of small reversible steps.
  Do not propose a rewrite in one branch; that design will not survive review and should
  not.
- **Two components already share a database.** Record it as a failure domain and as a
  coupling, and specify the extraction path — but do not fake independence in the
  diagram.
- **A required external dependency has no timeout or no idempotency** (a legacy partner
  API): record it as an unbounded failure, specify the wrapper the service will use
  (timeout, circuit breaker, dedupe key), and hand the residual risk to `BE-P06`.
- **The chosen boundary splits a single transaction that cannot be split** (financial
  invariants across tables): keep one component over that data and say why. Distributed
  purity is worth less than a ledger that balances.
- **Scope grows during the design** (someone asks for a new capability): record it as
  out of scope with the stage that would own it; do not absorb it into this plan.

## 8. Security and authorisation

Risk class A: read-only. Record the trust boundaries — where a request crosses from
untrusted to trusted, where a credential is held, and which component enforces
authorisation. A design that leaves authorisation to "the gateway" must name the gateway
configuration that does it, by path, or mark it `unverified`.

## 9. Completion criteria

- [ ] Component map with responsibility, owner and owned data.
- [ ] Dependency rule stated, with existing violations listed by path.
- [ ] A flow per operation, with a timeout on every hop and the budget verdict.
- [ ] Transaction boundary per operation, with the torn-write consequence.
- [ ] Dual writes named with their consistency mechanism.
- [ ] Failure domains including shared infrastructure.
- [ ] Decision records with rejected alternatives and reversal conditions.
- [ ] Known debts enumerated with owners.

## 10. Deliverables and handover

`BE_ARCHITECTURE.md` at the service root. `BE-P04` needs the transaction boundaries and
the ownership map — it may not create a cross-component write. `BE-P05` needs the module
layout and the dependency rule. `BE-P06` needs the failure domains, the dual-write
mechanisms and the external calls with no idempotency. `BE-P07` needs the flows to test
end to end.
