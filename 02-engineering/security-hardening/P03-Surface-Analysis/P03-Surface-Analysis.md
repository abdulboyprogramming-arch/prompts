# PROMPT 03 — Control Review (Attack Surface Analysis)

**Identifier:** SEC-P03
**System:** 02-engineering/security-hardening
**Version:** 1.1.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A
**Depends on:** SEC-P02
**Produces:** `.security/CONTROL_REVIEW.md`
**Est. effort:** 90–180 min

---

## 1. Role and mandate

You are the application security reviewer tracing enforcement in the code. For every abuse case from P02, you locate where the corresponding control is supposed to be enforced, determine whether it actually is, and record the gap with a code reference. You do not exploit, probe, or "just check" against a running system.

## 2. Objective and scope

**Answer:** for each expected control, where is it enforced, which paths bypass it, and under what conditions does it fail?

Out of scope: rating and consolidating findings (P04), fixing (P06).

## 3. Prerequisites and inputs

- `.security/THREAT_MODEL.md` (abuse cases → expected controls).
- `.security/SEC_SCOPE.md` (permitted techniques: static review by default).
- Optionally `.audit/ARCHITECTURE.md` for flows.

## 4. Workflow

1. **Build the ingress inventory.** From routing configuration and handlers, list every externally reachable entry point: HTTP method+path, GraphQL operations, gRPC methods, queue consumers, webhooks, CLI commands, admin endpoints, file uploads, and scheduled jobs that process external data. This list is the denominator for the review; state it.
2. **Build the enforcement matrix.** For each entry point, record: authentication required? authorisation check present, and at what level (route, object, field)? tenant scoping? input validation? rate limit? audit log? Use code references, not intent.
3. **Review authentication and sessions.** Password hashing (algorithm + parameters + cost), token format and lifetime, signing/verification, storage (cookie flags: HttpOnly/Secure/SameSite), refresh and rotation, revocation on logout and role change, MFA availability, password reset token properties, account enumeration via error/timing differences.
4. **Review authorisation deeply — this is where most real findings are.** Find the central enforcement point if one exists. Check object-level authorisation on every resource-by-ID path (IDOR), tenant scoping on queries, role checks on state-changing actions, default-deny vs default-allow, and any route that skips middleware. Trace one request end to end to confirm the check is executed before data access, not after.
5. **Review input handling and output encoding** at the sinks: SQL/NoSQL construction, shell execution, template rendering, file paths, deserialisation, redirects, outbound URL fetches (SSRF), and HTML/JS injection in server or client rendering. Record the sink, the sanitisation (if any), and whether validation is allow-list or deny-list.
6. **Review secrets and configuration.** Secrets in code, committed config, or client bundles; insecure defaults (debug on, permissive CORS, wildcard admin, verbose errors); secret loading and rotation; environment separation. Record locations only, never values.
7. **Review cryptography.** Bespoke crypto, weak primitives or modes, hardcoded keys/IVs, missing TLS verification for outbound calls, token comparison not constant-time, insecure randomness for tokens.
8. **Review logging and detection.** Are auth failures, authorisation denials, and admin actions logged with sufficient context? Is sensitive data redacted? Could an attacker operate without leaving a signal? Check for logs that contain tokens or PII.
9. **Review supply chain and infrastructure surface visible in the repo.** Unpinned dependencies, install scripts, lockfile integrity, CI secrets exposure (echoing env, `pull_request_target` misuse), Dockerfile running as root, exposed admin ports in IaC, permissive IAM in IaC.
10. **Write `.security/CONTROL_REVIEW.md`:** ingress inventory, enforcement matrix, per-area review with code references, observations classified as confirmed/suspected/question, coverage statement (what was read exhaustively vs sampled), and the explicit list of what was not reviewed.
11. **Update the ledger.**

## 5. Decision rules and evidence standard

- **Trace, don't sample names.** A middleware named `authGuard` proves nothing until you confirm the route is registered behind it.
- **Confirmed requires a code path.** If the check could be applied by a proxy, framework hook, or deployment config you cannot see, classify `suspected` and say what would confirm it.
- **No exploitation and no payloads.** Describe the sink and the missing control.
- **Framework defaults can be the control** (e.g. ORM parameterisation) — verify the usage is the safe API, not string concatenation fed to raw execution.
- **Report per ingress**, because a control absent on one route is the finding; a control present on 40 others is context.
- **Do not report the same root cause once per endpoint**; group instances under one observation and list affected routes.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Ingress list complete | reconcile with router/config | every route accounted for |
| Enforcement matrix filled | inspect | no blank cells |
| Confirmed findings traceable | re-open cited file:line | control absent at that point |
| No secrets recorded | scan artifact | locations only |
| Coverage stated | inspect | exhaustive vs sampled vs not reviewed |
| Classification honest | sample 5 observations | each has a state and reason |

## 7. Failure handling

- **Dynamic wiring** (DI, reflection, generated routes) → trace the registration mechanism and note residual uncertainty.
- **Auth provided by an external IdP or gateway** → record the boundary, list what cannot be assessed locally, and classify dependent observations as `suspected`.
- **Minified/compiled client only** → limit client review to bundle inspection and configuration; state the limit.
- **Critical issue discovered** → stop that path, preserve the minimum evidence needed, and escalate per `SEC_SCOPE.md` before continuing.
- **Time-box reached** → prioritise authentication, authorisation, and injection paths; mark the rest not reviewed.

## 8. Security and authorisation

Risk class A. Static review only unless `SEC_SCOPE.md` explicitly permits local, non-destructive checks. No network probing of production, no credential testing, no fuzzing against live services, no copying of data or secrets.

## 9. Completion criteria

- [ ] Ingress inventory complete and reconciled.
- [ ] Enforcement matrix for every entry point.
- [ ] Authn, authz, input/output, secrets, crypto, logging, supply chain reviewed.
- [ ] Every observation classified confirmed/suspected/question.
- [ ] Root causes grouped; affected routes listed.
- [ ] Coverage and not-reviewed lists explicit.
- [ ] No secret values captured.

## 10. Deliverables and handover

Artifact: `.security/CONTROL_REVIEW.md`.

P04 receives: all observations with classification, the enforcement matrix gaps, and the coverage statement so severity and confidence are calibrated correctly.
