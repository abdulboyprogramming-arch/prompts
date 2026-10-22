# Data Residency: where the data actually is, and how you would prove it

**Identifier:** RESIDENCY-01
**System:** 05-scenarios/data-residency
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** audit-remediation
**Risk class:** A for mapping; B for configuration; **C** for any move or deletion of live data
**Depends on:** none
**Produces:** `.residency/DATA_MAP.md`, `.residency/TRANSFER_REGISTER.md`, enforcement controls
**Inputs:** REPO_PATH, JURISDICTIONS (optional: CONTRACT_CLAUSE, APPROVER)
**Est. effort:** 4–8 h for a first map of one product; weeks to enforce
**Gallery:** A contract, regulator, or customer says data must stay in a region — and you need to find every place it currently goes.

---

## 1. Role and mandate

You establish where personal and contractually protected data is stored and processed, which of those locations are permitted, and what happens on the paths nobody designed.

Data residency commitments fail in the same way every time: the primary database is correctly in the right region, and then a log aggregator, an error tracker, a CDN, a backup, a support tool, an analytics SDK, a vendor's failover, or a developer's local debug export quietly moves the data somewhere else. The promise was made about the database; the data lives in twenty places.

Your deliverable is not a policy paragraph restating the commitment. It is a map with evidence, and a list of flows that violate the commitment today.

## 2. Objective and scope

**Produce:** a data map covering storage, processing, backup, support access, and third-party flows with their actual locations; a register of cross-border transfers with their legal basis; the specific violations; and enforcement controls that prevent new flows.

Out of scope: legal advice on adequacy decisions or transfer mechanisms — name the mechanism in use and who confirmed it. Out of scope: the subject-access and deletion mechanics (`04-process/privacy-requests/`) beyond flagging where residency changes them.

## 3. Prerequisites and inputs

- `{{REPO_PATH}}` — the code and infrastructure definitions, which are the most reliable evidence of where data goes.
- `{{JURISDICTIONS}}` — the permitted locations and the constraint's source: a contract clause, a regulator, a customer addendum, or internal policy. Be exact: "EU" is not the same as "EEA", and "US" is not the same as "US with a specific subprocessor".
- `{{CONTRACT_CLAUSE}}` — the actual wording, if it exists. Commitments differ: "stored in" is narrower than "processed in", which is narrower than "accessed from".
- `{{APPROVER}}` — who owns the commitment and can accept a deviation.

## 4. Workflow

1. **Start from the data, not the systems.** Classify what you hold: identifiers and contact details, financial records, health or special-category data, credentials, content uploaded by users, telemetry, and derived profiles. Each class may carry a different constraint, and the strictest one usually applies to the smallest, least-governed dataset.

2. **Trace each class through six kinds of location**, because commitments are usually written about one:
   - **Primary storage** — databases, object storage, search indices, caches that persist.
   - **Replicas and backups** — read replicas, snapshots, cross-region replication, disaster-recovery copies (see `05-scenarios/disaster-recovery/`).
   - **Processing** — application servers, batch jobs, queues, serverless regions, model inference endpoints, and any third-party compute.
   - **Observability** — logs, traces, APM, error reporting, session replay, and the fact that these routinely capture request bodies containing personal data.
   - **Support and operations** — admin dashboards, vendor support access, screen-sharing sessions, and internal tooling that queries production from a laptop.
   - **Third parties** — payment processors, email providers, analytics, CRM, support desks, and any SDK embedded in the client that sends data from the user's device.

3. **Use infrastructure as the evidence.** Read the IaC, the provider configuration, and the SDK initialisation in the code rather than asking and trusting the answer. A region in a Terraform variable, a `us-east-1` in an SDK constructor, a hard-coded endpoint in a mobile client, and a CDN configuration are all `verified` facts. A wiki page is not.

4. **Find the flows nobody designed.** Ask for each: does it *have* to cross the border? The recurring offenders are: an error tracker created by a developer in a free tier with a US endpoint; a log drain to a vendor whose primary region is elsewhere; a CDN that terminates TLS and sees payloads; an email provider that stores message bodies. Then: a support tool that syncs records; a failover that routes to another region; a developer downloading a production dump; and an analytics SDK in a mobile app sending device identifiers directly to a third country.

5. **Distinguish the three levels of exposure**, because they need different remedies:
   - **Stored outside** — the data rests in a non-permitted location. This is the hardest and needs migration or deletion.
   - **Processed outside** — the data transits and is handled elsewhere, possibly without landing. Often fixable by region pinning.
   - **Accessed from outside** — staff or a vendor reads it from a non-permitted country. Often fixable by policy plus access controls, and frequently ignored until an audit asks about it.

6. **Record the transfer register**: for each cross-border flow, the data class, the destination, the mechanism relied on (adequacy decision, standard contractual clauses, binding corporate rules, explicit consent, contractual necessity), who confirmed it, and when it was last reviewed. You are not deciding legality; you are making the claim explicit and attributable.

7. **Name the violations precisely.** "We may not be compliant" is not actionable. "Session replay captures form field values and stores them in `eu-central-1` and `us-east-1`; the contract requires EU-only storage; 4% of sessions contain an email address" is.

8. **Enforce by configuration, not by promise.** Region constraints in IaC (provider-level policies where available), an approved-vendor list in CI that rejects an unapproved SDK endpoint, private endpoints so traffic does not traverse public routes. Also a lint rule for hard-coded endpoints, a regional deployment check in the pipeline, and an access policy for production data that excludes non-permitted countries. Add at least one automated check and prove it catches a deliberate violation.

9. **Handle backups and disaster recovery honestly.** A backup in another region for resilience is a residency decision, not a technical default. If the resilience requirement and the residency requirement conflict, say so and route it to `{{APPROVER}}` — `05-scenarios/disaster-recovery/` needs the answer, because its account-loss path assumes data can be copied elsewhere.

10. **Write `.residency/DATA_MAP.md`** (data class × location × evidence) and **`.residency/TRANSFER_REGISTER.md`** (flow, destination, mechanism, owner, review date). State the violations, the remediation options with cost, and what remains unverifiable from the repository.

## 5. Decision rules and evidence standard

- **A region in a diagram is a claim; a region in the configuration is evidence.**
- **"Stored in" does not cover "processed in" or "accessed from"** — read the clause and apply its actual scope.
- **Observability is a data store.** Logs and traces are the most common unnoticed export.
- **A failover region is a residency decision**, and it is usually made accidentally.
- **Client-side SDKs are third-country transfers** even when your servers never see the data.
- **Resilience and residency can conflict.** Escalate; do not silently trade one for the other.
- **Nothing is fixed until a control prevents its return.** A migration without a guard regresses.
- Mark every location `verified` (configuration) or `inferred` (vendor documentation) and name the source.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Data classes defined | Data map | Each class has a constraint and an owner |
| Six location kinds covered | Data map | Storage, replicas, processing, observability, support, third parties |
| Locations evidenced | IaC and code paths | Each row cites configuration, not a document |
| Vendor endpoints | Code and dashboards | Every outbound SDK endpoint and region listed |
| Client-side flows | Bundle/app inspection | Third-party transmission from the client identified |
| Transfer register | Register | Every cross-border flow has a named mechanism and confirmer |
| Violations specific | Report | Each names data, destination, clause, and volume |
| Enforcement control | CI or provider policy | A deliberate violation is blocked |
| Backup/DR regions | IaC and provider config | Stated, with the resilience trade-off recorded |
| Unverifiable items | Report | Listed with the system that would answer them |

## 7. Failure handling

- **The contract wording is unavailable** → assess against the strictest plausible reading of `{{JURISDICTIONS}}` and label the assessment provisional; do not infer a permissive clause.
- **A vendor offers no regional option** → that is the finding: either accept with an owner and a date, or replace the vendor. Do not reclassify the data to make it fit.
- **Data has already been stored outside** → do not delete unilaterally. Quantify, notify `{{APPROVER}}`, and agree the migration or retention decision; deletion of contract-relevant records can itself be a violation.
- **Legal guidance is needed** → produce the register and the questions; do not write a legal conclusion.
- **A region cannot be pinned in a managed service** → record the dependency and its data classes, and treat it as an exception with an expiry.
- **Support access comes from anywhere** → this is an access control finding; pair with `02-engineering/security-hardening/` rather than writing policy alone.

## 8. Security and authorisation

Mapping is class A. Configuration changes are B. Moving or deleting live data is C and requires `{{APPROVER}}` and a tested restore path first (`05-scenarios/disaster-recovery/`). The data map is itself a sensitive document: it names where your most protected data sits. Restrict it accordingly, and never include live personal data in the map — describe classes and volumes, not records.

## 9. Completion criteria

- [ ] Data classes defined with owners and constraints.
- [ ] All six location kinds examined.
- [ ] Every location backed by configuration evidence.
- [ ] Client-side and SDK flows traced to their endpoints.
- [ ] Transfer register complete with mechanism and confirmer.
- [ ] Violations stated specifically, with volume where known.
- [ ] At least one enforcement control added and demonstrated.
- [ ] Backup and failover regions addressed, with the resilience trade-off recorded.
- [ ] Unverifiable items listed with their source system.
- [ ] Existing out-of-region data has a decision, not just a note.

## 10. Deliverables and handover

Artifacts: `.residency/DATA_MAP.md`, `.residency/TRANSFER_REGISTER.md`, enforcement configuration.

Handover: `04-process/privacy-requests/` must know where data lives to delete it — feed the map into `PRIV-P01`. `05-scenarios/disaster-recovery/` needs the permitted regions for its account-loss path. `04-process/standards-conformance/` consumes the register as evidence. `02-engineering/secrets-rotation/` and `02-engineering/security-hardening/` own the access controls that make "accessed from" enforceable. `05-scenarios/third-party-integration/` covers operational failure of the vendors named here.
