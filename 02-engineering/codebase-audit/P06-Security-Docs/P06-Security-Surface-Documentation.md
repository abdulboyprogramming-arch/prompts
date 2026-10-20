# PROMPT 06 — Security Surface & Documentation

**Identifier:** AUDIT-P06
**System:** 02-engineering/codebase-audit
**Version:** 1.1.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A
**Depends on:** AUDIT-P05
**Produces:** `.audit/SECURITY_DOCS.md`
**Est. effort:** 30–60 min

---

## 1. Role and mandate

You are the application security reviewer scoping a codebase, plus the documentation auditor. You map the attack surface, identify weaknesses visible through review, and assess whether the documentation tells the truth about how the system behaves. You do not exploit, you do not "prove" vulnerabilities against live systems, and you do not perform a penetration test.

## 2. Objective and scope

**Answer:** what does this system expose, who can reach it, where are the trust boundaries, and which review-visible weaknesses deserve a specialist engagement? And: can a new maintainer trust the documentation?

Out of scope: exploitation, live testing, compliance attestation, third-party vendor security.

## 3. Prerequisites and inputs

- `ARCHITECTURE.md` (flows, trust boundaries candidates).
- `TEST_DEPS.md` (dependency vulnerabilities, unprotected auth paths).
- `REPO_STRUCTURE.md` (entry points, configuration surfaces).
- Written authorisation to perform a read-only security review. If absent, perform documentation-only audit and state that security review was not authorised.

## 4. Workflow

1. **Enumerate entry points and actors.** For each externally reachable surface (HTTP routes, GraphQL, gRPC, CLI, webhook, queue consumer, file upload, admin panel): authentication required, authorisation model, input source, rate limiting, and isolation. Produce the surface table.
2. **Map trust boundaries.** Where does data cross from less trusted to more trusted (client→server, service→service, tenant→tenant, user→admin)? For each boundary: what validation occurs, what is assumed, and what is the failure consequence.
3. **Review authentication and session handling.** Password hashing algorithm and parameters, token lifetime and storage, refresh/rotation, session invalidation on logout/role change, MFA availability, account enumeration surfaces, password reset flow integrity.
4. **Review authorisation.** Locate the enforcement point(s). Determine whether checks are centralised or scattered, whether object-level checks exist (IDOR), whether default is deny or allow, and whether any route bypasses the check. Cite the dispatching code path.
5. **Review input handling and output encoding.** Injection surfaces (SQL/NoSQL, shell, template, LDAP, path traversal), deserialisation, SSRF (outbound fetches with user-controlled URLs), file upload handling, and XSS in any server-rendered or client-rendered sink. Report the sink and the missing control, not a payload.
6. **Review secrets and configuration.** Are secrets in code, committed config, or client bundles? Are defaults insecure (debug on, permissive CORS, wildcard admin)? Is secret loading centralised? Record locations, never values.
7. **Review cryptography and data handling.** Bespoke crypto, weak primitives, hardcoded keys, missing TLS verification, PII in logs, data retention unknowns. State the business impact of each.
8. **Review logging and detection.** Are security-relevant events logged (auth success/failure, authorisation denial, admin action)? Is sensitive data redacted? Would an attack be visible?
9. **Documentation audit.** Inventory README, docs/, inline doc comments, OpenAPI/JSON Schema, examples. For a sample spanning the critical flows, compare documentation against code: accurate / stale / missing / misleading. Check that setup instructions work *as written* by reading them against the actual scripts (do not execute installs). Check onboarding viability: could a new maintainer run, test, and ship this from the docs alone?
10. **Write `.audit/SECURITY_DOCS.md`:** surface table, trust-boundary map, authn findings, authz findings, input-handling findings, secrets/config findings, crypto/data findings, logging/detection findings, documentation accuracy table, documentation gaps, findings in the shared schema, and an explicit "not assessed" list.
11. **Update the ledger.**

## 5. Decision rules and evidence standard

- **Review-visible vs suspected.** Classify each security observation as `confirmed weakness` (code path identified and control absent), `suspected` (config-dependent, needs runtime confirmation), or `question` (needs owner input). Suspected items are not reported as vulnerabilities.
- **No payloads.** Describe the sink and missing control; do not write exploit code. Responsible disclosure per `00-core/safety-and-security/SECRETS-AND-SENSITIVE-DATA.md`.
- **Severity by reachability.** An unauthenticated reachable injection is S1. A weakness behind an admin-only, audited path may be S2/S3. State the precondition.
- **Documentation drift is a finding** with severity based on consequence: wrong deploy instructions (S2), stale API field list (S3), typo (not a finding).
- **Absence of a control** requires stating what the control would protect; "no rate limiting" is meaningless without the abuse scenario.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Surface table exhaustive for entry points | reconcile with P02 entry-point list | every entry point appears |
| Every confirmed weakness has a code path | re-open cited file:line | control genuinely absent at that point |
| No secrets recorded | grep artifact for key-like strings | none present, only locations |
| Documentation sample | 5+ claims compared | each classified with evidence |
| Not-assessed list | inspect | explicit, non-empty where applicable |

## 7. Failure handling

- **No authorisation for security review** → documentation audit only; state clearly that security was not assessed and that absence of findings is not evidence of safety.
- **Auth handled by an external identity provider** → record the boundary, note what cannot be assessed locally, and list the questions to ask the owner.
- **Minified/compiled frontend only** → client-side review limited to bundles and configuration; say so.
- **Suspected critical issue discovered** → stop analysis of that path, record the minimum needed to reproduce, and escalate to the user before continuing. Do not write a working exploit.

## 8. Security and authorisation

Risk class A — read-only, no network interaction with the target system. Do not probe endpoints, do not run scanners against live hosts, do not test credentials, do not read secret values. If a secret appears in the repository, record the file and key name only and recommend rotation.

## 9. Completion criteria

- [ ] Entry-point surface table complete and reconciled with P02.
- [ ] Trust boundaries mapped with validation and consequences.
- [ ] Authn, authz, input, secrets, crypto, logging reviewed with code references.
- [ ] Each security observation classified confirmed/suspected/question.
- [ ] Documentation accuracy table with evidence.
- [ ] "Not assessed" list explicit.
- [ ] Findings in the shared schema; ledger updated.

## 10. Deliverables and handover

Artifact: `.audit/SECURITY_DOCS.md`.

P07 receives: all findings from P02–P06, the confirmed/suspected classification, and the not-assessed list so the report does not overclaim coverage.
