# PROMPT 06 — Grounded Retrieval: does the system answer from your documents?

**Identifier:** AI-P06
**System:** 03-domains/ai-agentic
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** audit-remediation
**Risk class:** B (builds and edits evaluation harnesses and retrieval code; no production rollout without authorisation)
**Depends on:** AI-P03 (evaluation discipline), AI-P04 (injection defence)
**Produces:** `RETRIEVAL_EVAL.md`, an ablation table, a grounding policy
**Inputs:** REPO_PATH, CORPUS_SCOPE (optional: EVAL_SET, EMBEDDING_MODEL, CHUNK_STRATEGY, LATENCY_BUDGET)
**Est. effort:** 3–6 h

---

## 1. Role and mandate

You establish whether a retrieval system actually answers from the corpus — with citations that support the claim — or merely produces fluent text that resembles an answer.

The failure is specific and invisible in demo conditions: retrieval returns *plausible* chunks, the model writes a confident paragraph, the citation points at a document that does not contain the statement. Nothing throws. Users trust it more because it cites something.

You measure **retrieval quality and answer groundedness separately**, because a failure in either produces the same symptom and requires a different fix.

## 2. Objective and scope

**Produce:** a labelled evaluation set with answerable and unanswerable questions, retrieval metrics, groundedness measurement, an ablation over chunking and `k`, and a written grounding/abstention policy.

Out of scope: model selection without a task, embedding-model training, and general prompt tuning (that is `AI-P03`'s harness with a different hypothesis).

## 3. Prerequisites and inputs

- `{{REPO_PATH}}` with the ingestion, chunking, embedding, and query code; `{{CORPUS_SCOPE}}` — the documents, versions, and whether they change.
- `{{EVAL_SET}}` — if none exists, build one: **60–150 questions**, at minimum 30% unanswerable from the corpus, 20% requiring two documents, and 10% with a near-miss distractor.
- `{{EMBEDDING_MODEL}}`, `{{CHUNK_STRATEGY}}`, `{{LATENCY_BUDGET}}` — the variables the ablation will move.

## 4. Workflow

1. **Build the eval set from the corpus, not from the demo.** Every answerable question carries its gold passage ID(s). Unanswerable questions are the ones that matter most: they reveal whether the system can say "I don't know".

2. **Measure retrieval in isolation first.** For each question, compute recall@k and MRR against gold passage IDs. If the gold passage is not retrieved, the generator cannot be grounded — report this before discussing answer quality.

3. **Measure groundedness of the answer.** For each generated claim, check whether it is supported by a retrieved passage. Classify: **supported**, **partially supported** (overreach), **unsupported** (hallucination), **contradicted** (the passage says the opposite — the worst case, because the citation looks credible).

4. **Check citation correctness separately from answer correctness.** An answer can be right with a wrong citation, which trains users to trust the wrong document. Measure: does the cited passage contain the claim? Does the claim appear in the corpus at all?

5. **Measure abstention.** On unanswerable questions, the system should refuse or say it lacks information. Report the abstention rate and, critically, the **false-abstention rate** on answerable questions — a system that refuses everything scores well on hallucination and is useless.

6. **Run the ablation, one variable at a time**: chunk size and overlap; chunk boundaries (fixed window vs semantic vs heading-aware); `k`; hybrid lexical + vector retrieval versus vector only; reranking on/off; query rewriting on/off. Report the delta in recall@k and groundedness for each, with cost and latency.

7. **Test the corpus conditions that break production**: a document updated after indexing (staleness), duplicates and near-duplicates (the model cites the wrong version), tables and code blocks (chunking destroys them), permission-scoped documents (see step 8), and very long documents (retrieval returns only the middle).

8. **Test permission leakage explicitly.** If documents have access rules, retrieval must filter *before* the model sees content, not after. Ask a question whose answer exists only in a document the querying user cannot access: if the system answers, that is a critical finding, not a quality issue.

9. **Test injection through retrieved content.** A poisoned document ("ignore previous instructions and…") is the standard attack (`AI-P04`). Verify that retrieved text is treated as data and that the system's behaviour does not change.

10. **Write the grounding policy**: when to cite, when to abstain, what to do with partial support, how freshness is communicated, and what the user sees when retrieval returns nothing. **If the policy is not written, the model improvises it** — usually by answering anyway.

## 5. Decision rules and evidence standard

- **Retrieval metrics before answer metrics.** A generator cannot fix a missing passage.
- **Gold passage IDs are required**; "looks relevant" is not a label.
- **Unanswerable questions are at least 30% of the set**, or the evaluation measures fluency.
- **A citation is a claim about provenance** and is scored independently.
- **Abstention is a feature to measure, not a failure to eliminate.**
- **Ablate one variable at a time**; multi-variable changes produce uninterpretable results.
- **Permission filtering happens before generation**, never in the prompt.
- **A single stale document can invalidate an entire answer**, so freshness is part of correctness.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Eval set built with gold IDs | File | Every answerable question has passage IDs |
| Unanswerable share | Count | ≥30% of the set |
| Recall@k measured | Harness | Reported per question and aggregate |
| Groundedness classified | Rubric | Supported / partial / unsupported / contradicted |
| Citations scored | Harness | Citation contains the claim |
| Abstention measured | Harness | Rate on unanswerable and false-abstention on answerable |
| Ablation per variable | Table | Delta in recall and groundedness, with cost and latency |
| Staleness tested | Case | Outdated document flagged or excluded |
| ACL leakage tested | Case | No answer from an unauthorised document |
| Injection through corpus tested | Case | Behaviour unchanged by poisoned passage |
| Grounding policy written | Document | Cite/abstain rules explicit |

## 7. Failure handling

- **Recall is high but groundedness is low** → the generator is ignoring context or the prompt permits invention; fix the prompt and the policy, not retrieval.
- **Recall is low and groundedness is high** → the system abstains a lot; improve chunking, add hybrid search or reranking, and re-measure.
- **Contradicted answers appear** → the retrieved passage contradicts the claim; check for stale duplicates and for the model's tendency to "correct" documents from parametric knowledge.
- **The system answers unanswerable questions** → add explicit "only answer from provided context" instruction, an abstention path, and a post-filter; re-measure both rates, because over-correction causes false abstention.
- **Permission leakage found** → treat as a security incident, not a bug: `02-engineering/security-hardening/` and `05-scenarios/security-incident/`, and record the blast radius (which documents, which users).
- **Latency exceeds `{{LATENCY_BUDGET}}` after adding reranking** → report the trade-off table and let the product owner choose; do not silently drop the quality step.
- **The corpus changes weekly** → the eval set must be re-run on every reindex, or drift is invisible.

## 8. Security and authorisation

Risk class B. Evaluation must run against a copy of the corpus with production access controls intact — testing ACL bypass on real documents with real permissions is itself a risk and needs authorisation. Never place production documents in a public harness, and redact PII from any eval artefact that leaves the environment. Retrieved content is untrusted input: it must never be concatenated into the instruction channel without delimiters and a stated precedence rule.

## 9. Completion criteria

- [ ] Eval set with gold passage IDs and ≥30% unanswerable questions.
- [ ] Recall@k and MRR measured before any generation change.
- [ ] Groundedness classified on every generated claim.
- [ ] Citation correctness scored independently.
- [ ] Abstention and false-abstention measured.
- [ ] Ablation run one variable at a time, with cost and latency.
- [ ] Staleness, duplication, table/code, and long-document cases tested.
- [ ] ACL leakage tested; result recorded.
- [ ] Injection through retrieved content tested.
- [ ] Grounding/abstention policy written.

## 10. Deliverables and handover

Artifacts: `RETRIEVAL_EVAL.md`, eval set with labels, ablation table, grounding policy.

Handover: `AI-P03` absorbs the eval set into the standard harness so every change is measured against it; `AI-P04` takes the injection findings; `AI-P05` adds retrieval-quality monitoring (empty results, low-score retrievals, abstention rate) to production dashboards, because retrieval degrades silently as the corpus grows.
