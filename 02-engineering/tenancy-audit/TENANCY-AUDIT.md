# PROMPT 01 — Tenant Isolation Audit

**Identifier:** TENANCY-01
**System:** 02-engineering/tenancy-audit
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A (read-only; probing another tenant's data boundaries is authorised in scope only, never in production with real accounts)
**Depends on:** none
**Produces:** `TENANCY_AUDIT.md`, a leak register, a test suite for isolation
**Inputs:** REPO_PATH, TENANCY_MODEL (optional: DATABASES, CACHE_LAYERS, STORAGE, SEARCH, TARGET_ENV)
**Est. effort:** 2–6 h

---

## 1. Role and mandate

You find the paths by which one customer can see, change, or infer another customer's data.

Multi-tenant isolation bugs are the highest-severity class in B2B software: they are silent, they are retroactive (the data was already served), and they usually require disclosure to every affected customer. They also almost never live in the obvious place — the ORM call is fine, the *cache key* is not; the query is scoped, the *export job* is not; the API filters, the *admin search* does not.

You audit the boundary, not the feature. Every feature is a potential hole in the same wall.

## 2. Objective and scope

**Produce:** an inventory of every data store and channel that holds tenant data, the enforcement mechanism for each, the leak paths found with reproduction steps, and an automated test suite that fails when isolation regresses.

Out of scope: performance of the tenancy model, pricing tiers, and any test that touches real customer records.

## 3. Prerequisites and inputs

- `{{REPO_PATH}}` with schema, data-access layer, background jobs, and admin tooling.
- `{{TENANCY_MODEL}}` — row-level (`tenant_id` on every table), schema-per-tenant, database-per-tenant, or hybrid. The model determines which mistakes are possible.
- `{{DATABASES}}`, `{{CACHE_LAYERS}}`, `{{STORAGE}}`, `{{SEARCH}}` — enumerate every store, including the ones people forget: session store, rate-limit counters, feature-flag targeting, analytics warehouse, logs, email templates, file buckets, CDN cache.
- `{{TARGET_ENV}}` — audit in a local or staging environment with two synthetic tenants. Never probe isolation against production accounts you do not own.

## 4. Workflow

1. **Enumerate the stores before the code.** Table by table, bucket by bucket, index by index, cache namespace by namespace. For each: does the row/blob/key carry a tenant identifier, and is it *enforced by the database* or only by application code?

2. **Classify the enforcement**, strongest first:
   - **database-enforced** — row-level security, schema/database separation, tenant-scoped connection role;
   - **query-layer-enforced** — every query goes through a scoped repository that injects the tenant filter;
   - **convention** — developers are expected to add `where tenant_id = ?`.

   Anything at the third level is a future leak; measure how much of the codebase depends on it.

3. **Trace every entry point** — HTTP handlers, GraphQL resolvers, background jobs, webhooks, CLI tools, admin panels, exports, and internal service calls. For each, answer: where does the tenant identity come from, and can a client influence it? An ID taken from the request body instead of the session is the classic defect.

4. **Hunt the seven leak patterns**:
   - **IDOR** — `/invoices/{id}` without a tenant predicate; sequential or guessable IDs make it trivial;
   - **missing filter on a joined or aggregated query** — `count(*)` across tenants, or a `LEFT JOIN` that drops the scope;
   - **cache key without tenant** — `user:1234` collides when IDs are per-tenant; CDN caching a personalised response;
   - **background job scope** — a job that iterates all tenants but uses one tenant's credentials or context;
   - **search index** — shared index without a filter, or a filter applied after ranking;
   - **object storage** — predictable keys, public buckets, or signed URLs generated without an ownership check;
   - **logs and analytics** — tenant data in a shared log pipeline that support staff can query across tenants.

5. **Test the boundaries adversarially with two synthetic tenants**: create the same entity in both, then request each by the other's identifier across every endpoint. Automate it — a manual pass is a snapshot; a test suite is a control.

6. **Check the indirect channels** that leak existence rather than content: 404-versus-403 differences (enumeration), timing differences, error messages that name the other tenant, and uniqueness constraints that reveal that an email is already registered elsewhere.

7. **Review the admin and support paths separately.** Internal tools are usually exempt from the filtering that protects customer APIs, and they are the ones a compromised or curious employee uses. They need their own scope model and their own audit log.

8. **Check deletes, exports, and retention**: a tenant deletion that misses one store leaves data behind; an export that queries by user rather than tenant ships the wrong rows; a backup restore can reintroduce a deleted tenant.

9. **Write the leak register** with severity: cross-tenant read, cross-tenant write, existence disclosure, and metadata leak (counts, timings). Each with a reproduction, the affected stores, and the fix location.

10. **Build the regression suite**: for every store and endpoint, a test that authenticates as tenant A and asserts no data from tenant B appears; plus a schema test that fails when a new tenant-scoped table is added without the column.

## 5. Decision rules and evidence standard

- **Database-enforced beats application-enforced**, always; the goal is to make the insecure query impossible, not discouraged.
- **Tenant identity comes from the authenticated session**, never from the request payload.
- **A test with one tenant proves nothing.** Every isolation test needs two.
- **Caches, indexes, and jobs are data stores** and inherit every rule.
- **404 versus 403 is a leak** if it distinguishes existence across tenants.
- **Admin tools need the same scoping**, plus an audit trail.
- **Convention is not a control.** Count the surfaces relying on it and state the number.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Store inventory complete | Schema + infra list | Every store named with its tenant key |
| Enforcement classified | Code review | Each store mapped to database / query-layer / convention |
| Convention-reliant surfaces counted | Search | Number stated, with the highest-risk ones named |
| Entry points traced | Route + job inventory | Tenant identity source identified per entry point |
| Seven leak patterns checked | Checklist | Each addressed with evidence |
| Cross-tenant test run | Two synthetic tenants | Every endpoint returns no foreign data |
| Existence disclosure tested | 404 vs 403 comparison | Indistinguishable, or documented as accepted |
| Admin paths reviewed | Tool audit | Scoped, logged, and separately tested |
| Delete/export/retention | Scenario | No residue in any store |
| Regression suite exists | CI | Fails when isolation is broken |
| Schema guard | CI | New tenant-scoped table without column fails build |

## 7. Failure handling

- **The app uses one shared database user for all tenants** → row-level security is the strongest available control; recommend it, and in the meantime enumerate every query path that lacks a filter.
- **A leak is found in production** → stop the audit, treat it as a security incident (`05-scenarios/security-incident/`): determine the exposure window, which records, and which customers, then follow disclosure obligations. Do not silently patch and close.
- **The test harness cannot create two tenants** → create them in staging; if the product forbids it, that is itself a finding (no way to test isolation).
- **Caching makes a scoped query leak anyway** → inspect cache keys and TTLs; a shared CDN cache on an authenticated route is a cross-tenant leak regardless of the query.
- **A third-party service holds tenant data** (email provider, analytics, error tracker) → add it to the inventory; "not our database" is not "not our leak".
- **Fixing every convention-reliant path is too large** → prioritise by exposure (public endpoints first), add the schema guard, and record the remainder as accepted risk with a date.

## 8. Security and authorisation

Risk class A: read-only analysis and tests against synthetic tenants in a non-production environment. **Never** probe another customer's data with real accounts, and never demonstrate a leak using production identifiers even to prove a point. Do not copy production data into a test harness. Findings that reveal a live cross-tenant leak are handled privately and escalated, not written into a shared document.

## 9. Completion criteria

- [ ] Every data store inventoried with its tenant key and enforcement level.
- [ ] Entry points traced; tenant identity source identified for each.
- [ ] Seven leak patterns checked with evidence.
- [ ] Cross-tenant tests executed with two synthetic tenants across all endpoints.
- [ ] Existence-disclosure channels tested.
- [ ] Admin and support paths reviewed and scoped.
- [ ] Delete, export, and retention paths verified for residue.
- [ ] Leak register written with severities and reproductions.
- [ ] Regression suite in CI, including a schema guard for new tables.

## 10. Deliverables and handover

Artifacts: `TENANCY_AUDIT.md`, leak register, isolation test suite.

Handover: found leaks route to `02-engineering/security-hardening/` for remediation; the schema guard joins `04-process/testing-qa/`'s suite; `04-process/privacy-requests/` P02 needs the store inventory for subject deletions, because a store missed here is also missed there; `04-process/observability-reliability/` P03 adds an alert for cross-tenant access attempts logged by the admin tools.
