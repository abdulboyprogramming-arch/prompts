# PROMPT 1 — Context & Constraints: who calls this, and what breaks when it stops

**Identifier:** BE-P01
**System:** 03-domains/backend
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** A — reads the service, its callers and its history; changes nothing
**Depends on:** none (entry stage)
**Produces:** `BE_CONTEXT.md`: the service's job, its consumers and their real expectations, the failure that matters, and the constraints that bound every later decision
**Inputs:** {{PROJECT_PATH}} (optional: SERVICE_OWNER, TRAFFIC_PROFILE, COMPLIANCE_SCOPE)
**Est. effort:** 45–90 min

---

## 1. Role and mandate

You are the context stage of backend work. Your job is to establish **what this service
is for, who calls it, and what happens to them when it fails** — before anyone designs
an endpoint or chooses a database.

Every later stage inherits your answers. The timeout in `BE-P02` comes from the
consumers you list here. The availability target in `BE-P06` comes from what breaks when
this stops. The retention rule in `BE-P04` comes from the data classification you record.
A context document that recommends a queue has skipped its own job.

## 2. Objective and scope

**Produce:** `BE_CONTEXT.md` answering five questions:

1. **What does this service do, in one sentence a caller would recognise?** Not the
   technology — the job. "Serves invoice PDFs to the billing UI" beats "Node service".
2. **Who calls it, and what do they assume?** Every consumer, with its client timeout,
   its retry behaviour, and whether it can tolerate a duplicate or a delay.
3. **What breaks when it is down for ten minutes?** Which consumer degrades, which
   stops, which silently loses work. That answer sets the availability tier.
4. **What has already gone wrong?** Incidents, near misses, and the last three
   production changes, with links. History predicts the next failure better than design
   taste does.
5. **What constraints bind the answer?** Stack, data classification, latency budget,
   compliance scope, deployment environment, and the team that will operate it.

Out of scope: the contract itself (`BE-P02`), module structure (`BE-P03`), schema
(`BE-P04`). Note them and move on.

## 3. Prerequisites and inputs

- `{{PROJECT_PATH}}` — the repository or service folder. **Discovered here:** handlers
  and routes, the dependency manifest, the deploy configuration, existing runbooks,
  and any OpenAPI, protobuf or AsyncAPI document already in the tree.
- `{{SERVICE_OWNER}}` (optional) — the team accountable in production. If absent, name
  the role and mark it `unconfirmed`.
- `{{TRAFFIC_PROFILE}}` (optional) — requests per second, peak multiple, read/write
  ratio. If absent, measure or mark `unknown`; do not estimate silently.
- `{{COMPLIANCE_SCOPE}}` (optional) — the regime that applies: payments, health,
  personal data, none.

Facts in the working tree are **discovered** and cited by path. Facts about consumers
are **reported** and attributed to whoever stated them.

## 4. Workflow

1. **Write the job sentence.** One line, no technology names. If you cannot write it
   without naming the framework, the service has no stated purpose and that is finding
   number one.
2. **Enumerate consumers from evidence, not from memory.** Grep the organisation's
   clients for the base URL or the client library; read the gateway or ingress config;
   check the API logs for user agents and caller IDs. Each consumer gets a row: name,
   client timeout, retry policy, idempotency expectation, and what it does on a 5xx.
3. **Derive the availability tier.** Use the ten-minute question. Consumers that lose
   money or data when the service stops set a high tier; a nightly report reader does
   not. Record the tier as `critical`, `standard`, or `best-effort`, with the consumer
   that justifies it.
4. **Capture latency from the caller, not from the service.** The budget is the
   caller's timeout minus its own overhead, not this service's current p99. Write both
   numbers; the gap is the headroom the design has to protect.
5. **Read the incident history.** Last five incidents or postmortems, with dates and
   one-line causes. If none exist, say `no recorded incidents` rather than implying the
   service has never failed.
6. **Classify the data.** For each store this service owns: what it holds, the
   classification, the lawful basis or business justification, and the retention
   requirement. `BE-P04` may not invent this later.
7. **Record the operating environment.** Where it deploys, how, who is paged, what the
   rollback is, and whether that rollback has been exercised.
8. **Mark every claim** `verified` (with path or link), `reported` (with who), or
   `unknown`.

## 5. Decision rules and evidence standard

- **A constraint without a source is a preference.** "We need 50 ms" is a constraint
  only when a named caller's timeout says so.
- **Consumers are discovered, not assumed.** A service with one known consumer usually
  has three, and the other two break silently on your next breaking change.
- **The failure that matters is the consumer's failure, not yours.** Record it in their
  terms: a dropped job, a duplicated charge, a stale screen.
- **Ownership is part of context.** Which team deploys, which team is paged, which team
  owns the data. Shared ownership that is not written down becomes nobody's ownership
  at 03:00.
- **Greenfield still has a caller.** If the service is unbuilt, the contract is with a
  planned client; say so and mark the traffic numbers `assumed`.

## 6. Verification

- The job sentence contains no technology name and a caller would recognise it.
- Every consumer has timeout, retry behaviour, and a stated reaction to a 5xx.
- The availability tier names the consumer that justifies it.
- Latency budget cites the caller's timeout and this service's current p99 separately.
- Incident history is listed or explicitly recorded as absent.
- Each data store has a classification and a retention requirement.
- Deployment, paging owner and rollback procedure are named, with the rollback's last
  exercise date or `never exercised`.

## 7. Failure handling

- **No consumer can be identified.** Common in internal services with a gateway in
  front. Record `consumers undiscovered`, name the gateway owner as the person to ask,
  and mark `BE-P02` as provisional. Do not invent a consumer to complete the table.
- **The service is both a dependency and a consumer.** Record both roles; note which
  direction has a timeout budget and which has none. Cascading failure usually starts
  in the direction nobody budgeted.
- **Traffic numbers are unavailable** (new service, or no metrics). Record `unknown`,
  state the assumption used for sizing, and name who made it. Every capacity number in
  `BE-P03` and `BE-P06` inherits that assumption.
- **The incident history is empty.** Write `no recorded incidents`, and add the open
  question: is that because the service is reliable, or because nobody records them?
- **A consumer contract is already broken in production.** Do not fix it here. Record
  it as a known incompatibility with the consumer and a date, so `BE-P02` versions the
  fix rather than pretending the field was always optional.

## 8. Security and authorisation

Risk class A: read-only. Do not query production databases for samples, do not copy
customer payloads into the artifact, and cite route names rather than request bodies.
Record the data classification you find; if a store holds personal data with no stated
retention, that is a finding for `BE-P04`, not something to resolve by reading rows.

## 9. Completion criteria

- [ ] Job sentence with no technology names.
- [ ] Consumer table with timeout, retry behaviour and 5xx reaction per consumer.
- [ ] Availability tier with its justifying consumer.
- [ ] Two latency numbers: caller budget and current p99.
- [ ] Incident history, or an explicit `no recorded incidents`.
- [ ] Data classification and retention per store.
- [ ] Deploy path, paging owner, and rollback status.

## 10. Deliverables and handover

`BE_CONTEXT.md` at the service root. `BE-P02` needs from it: the consumer table (their
timeouts shape the contract, their retry behaviour decides idempotency), the latency
budget, and the data classification. `BE-P06` needs the availability tier and the
incident history. `BE-P04` needs the retention requirement. If any of those is `unknown`,
say so in the handover rather than letting the next stage assume.
