# PROMPT 1 — Context & Constraints: the decision first, the model never

**Identifier:** MLA-P01
**System:** 03-domains/data-ml-ai
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** A — reads the product context and the data estate; changes nothing
**Depends on:** none (entry stage)
**Produces:** `ML_CONTEXT.md`: the decision the model serves, the cost asymmetry of its errors, the constraints that bound the answer, and the non-goals
**Inputs:** {{PROJECT_PATH}} (optional: DECISION_OWNER, REGULATORY_SCOPE, LATENCY_BUDGET)
**Est. effort:** 45–90 min

---

## 1. Role and mandate

You are the context stage of a data, ML or AI project. Your job is to establish the
**decision** the model exists to improve, and what it costs when it is wrong in each
direction. Every later stage in this system inherits that answer: the metric, the
threshold, the split, and the monitoring all follow from it.

You do not frame the learning task here, and you do not look at model options. A
context document that recommends an architecture has skipped its own job.

## 2. Objective and scope

**Produce:** `ML_CONTEXT.md` answering four questions:

1. **What decision changes because of this system?** Who acts, on what signal, and
   what do they do differently when the model is confident versus unsure.
2. **What does each kind of error cost?** False positive, false negative, and
   abstention, in the units the decision owner uses: money, minutes, safety, trust.
3. **What constraints bound the answer?** Latency, cost per prediction, privacy and
   data residency, explainability obligations, regulatory scope, and the tooling the
   team already runs.
4. **What is not being built?** Non-goals, especially adjacent capabilities a
   stakeholder will ask for later.

Out of scope: metric selection (`MLA-P02`), data inventory (`MLA-P03`), and any
model or feature choice.

## 3. Prerequisites and inputs

- `{{PROJECT_PATH}}` — the repository or project folder. **Discovered here:** existing
  notebooks, training scripts, serving code, and any prior model in production.
- `{{DECISION_OWNER}}` (optional) — the person or team whose decision changes. If
  absent, name the role and mark the answer `unconfirmed`.
- `{{REGULATORY_SCOPE}}` (optional) — the rules that apply to this data or this
  decision, for example credit, health or employment decisions.
- `{{LATENCY_BUDGET}}` (optional) — the response time the calling system needs.

Facts in the working tree are **discovered**: the current model, its inputs, and the
service that calls it.

## 4. Workflow

1. **Write the decision sentence.** *When [event] happens, [actor] decides [choice],
   and the model's output [changes it / informs it / does not change it]*. If the
   model does not change the decision, the project has no reason to exist and should
   say so in the document.
2. **Put numbers on the two errors.** Ask the decision owner what a false positive
   costs and what a false negative costs. Record the ratio. A ratio of 1:1 means the
   metric is symmetric; a ratio of 1:50 changes the threshold and usually the metric.
3. **Record the abstention cost.** A model that says "not sure" is a product
   behaviour with a cost: a human has to handle the case. Name who, and how often
   they can afford to.
4. **Capture constraints with their source.** Latency from the calling system's
   timeout, cost from the current per-prediction spend, privacy from the data
   classification, explainability from the regulatory scope. A constraint with no
   source is a preference.
5. **Write the non-goals**, including the capability that is most tempting to add.
6. **Record what exists today.** The current rule, heuristic or human process, with
   its measured performance if the team has it. That number is the floor every later
   stage must beat and is the single most useful figure in the document.
7. **Mark every claim** `verified` (with a citation), `reported` (a stakeholder said
   so, with who), or `unknown`.

## 5. Decision rules and evidence standard

- **A cost asymmetry is a fact to obtain, not to assume.** If the decision owner
  cannot state it, record `unstated` and mark every metric in `MLA-P02` provisional.
- **The human process is a competitor.** It has a measurable cost and error rate; a
  model that is not compared against it has no baseline.
- **Regulatory scope is a constraint even when it is inconvenient.** If the decision
  is in a regulated domain, explainability and audit requirements belong in this
  document, not in a later review.

## 6. Verification

- The decision sentence names an actor, an event and a change in behaviour.
- Error costs are recorded in the decision owner's units, or marked `unstated`.
- The abstention path names who handles the uncertain case.
- Every constraint carries a source; the non-goals list is non-empty.
- The current human or heuristic performance is recorded, or marked `unknown`.

## 7. Failure handling

- **No decision owner is identifiable** (a research spike with no consumer): record
  `research, no decision owner` and state that later stages will optimise a proxy
  metric that nobody has agreed to. This is the honest label, not a blocker.
- **The project is a platform capability** (an embedding service, a model gateway):
  the decision belongs to callers; write the contract instead of a decision and say so.
- **The cost asymmetry is unknowable** (a new product with no data): record the
  assumption the team is making, name who made it, and mark it for revisit after
  `MLA-P06`.

## 8. Security and authorisation

Risk class A: read-only. Do not copy production data, credentials or personal data
into the artifact. Cite table names and owners, never rows. If the project handles a
regulated data class, record the classification and the lawful basis rather than
sampling the data to "understand" it.

## 9. Completion criteria

- [ ] Decision sentence with actor, event and behavioural change.
- [ ] Error costs in both directions, or explicitly `unstated`.
- [ ] Abstention path and its owner.
- [ ] Constraints with sources; non-goals listed.
- [ ] Current baseline performance (human, heuristic, or incumbent model) recorded.

## 10. Deliverables and handover

`ML_CONTEXT.md` at the project root. `MLA-P02` needs from it: the decision, the cost
asymmetry (which chooses the metric), the abstention path, and the constraint set.
