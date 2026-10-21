# PROMPT 01 — API Versioning and Consumer Contracts

**Identifier:** API-VER-01
**System:** 03-domains/backend
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** B (writes versioning policy and contract tests; sunsetting an endpoint is C)
**Depends on:** none
**Produces:** `.api/VERSIONING.md`, consumer inventory, contract tests, deprecation schedule
**Inputs:** API_SCOPE, CONSUMERS (optional: CURRENT_VERSION, SUNSET_WINDOW, APPROVER)
**Est. effort:** 3–5 h for the policy; 1–2 h per deprecated endpoint

---

## 1. Role and mandate

You decide how this API changes without breaking the people who depend on it — and you make the answer enforceable rather than aspirational.

Most teams version by accident: they add fields (safe), then rename one (breaking), then "fix" a response shape in a patch release (breaking, shipped as a bugfix), then discover the damage when a partner's integration fails silently. Versioning is a promise about the future; the only way to keep it is a contract test and a deprecation schedule.

## 2. Objective and scope

**Produce:** a versioning scheme, a consumer inventory, compatibility rules per change type, contract tests, a deprecation and sunset policy, and a migration path for anything already broken.

Out of scope: mobile client version skew (`MOB-P03` covers installed apps), authentication design, and rate limiting.

## 3. Prerequisites and inputs

- `{{API_SCOPE}}` — which surface (public, partner, internal service-to-service) and its protocol (REST, GraphQL, gRPC, webhooks).
- `{{CONSUMERS}}` — who calls it, from where, and whether you can see their traffic. Unknown consumers are the central problem.
- `{{CURRENT_VERSION}}` — if versioning exists, what form it takes (URL path, header, media type, field in the body).
- `{{SUNSET_WINDOW}}` — how long a deprecated version stays alive; `{{APPROVER}}` — required to remove anything.

## 4. Workflow

1. **Inventory consumers before choosing a scheme.** Server logs per client identifier, API keys, user agents, SDK versions, partner onboarding documents. If you cannot tell who calls an endpoint, you cannot deprecate it — that is the first finding.

2. **Choose one versioning mechanism** and state its limits: URL path (`/v2/`) is visible and cache-friendly; a header or media type is purer and invisible to logs; a body field is the worst option. Whatever you choose, **one mechanism**, applied consistently.

3. **Classify every change type** and write the rule down:

   | Change | Compatible? | Rule |
   |---|---|---|
   | Add an optional response field | Yes | Only if clients tolerate unknown fields — verify, do not assume |
   | Add a required request field | **No** | New major version |
   | Add an enum value | **No** in practice | Clients with exhaustive switches break; prefer open strings or document the contract |
   | Rename a field | **No** | Add the new one, keep both, deprecate |
   | Change a type (int → string) | **No** | New major version |
   | Change validation to be stricter | **No** | Old clients send the old shape |
   | Change error codes or messages | Risky | Clients parse them; treat as breaking unless documented otherwise |
   | Change pagination defaults | Risky | Silent truncation is a data bug for consumers |
   | Remove an endpoint | **No** | Deprecation cycle with dates |

4. **Make compatibility testable**: capture a corpus of real request/response pairs for each endpoint and run a schema-diff check in CI. A change that alters a documented field fails the build, not the partner.

5. **Publish the contract as an artifact** — OpenAPI/Protobuf/GraphQL schema, versioned in the repository, with the diff visible in code review. Documentation that drifts from behaviour is worse than none.

6. **Design the deprecation as a sequence with dates**: announce → add `Deprecation`/`Sunset` headers and a changelog entry → contact known heavy consumers → monitor remaining traffic → warn in responses → disable. Each step has an entry condition based on measured traffic, not on the calendar alone.

7. **Handle the unknown-consumer problem explicitly**: if traffic arrives without a client identifier, add one before deprecating; if a consumer cannot be contacted, the sunset date is a business decision with a stated risk, not a technical one.

8. **Plan for the version nobody wants to maintain**: two live major versions double the test matrix and the bug surface. Set a maximum number of concurrent versions and enforce it in the policy.

9. **Check the non-API contracts that break just as hard**: webhooks (event names, payload shape), SDKs (generated or hand-written), and error-code semantics. A consumer on your SDK inherits your API decisions.

10. **Write `.api/VERSIONING.md`**: scheme, change classification table, contract-test mechanism, deprecation timeline with dates and traffic thresholds, sunset policy, and the owners of the remaining work.

## 5. Decision rules and evidence standard

- **Addition is compatible only if clients tolerate unknown fields** — verify, never assume.
- **One versioning mechanism**, applied everywhere.
- **The schema artifact is the contract**; prose documentation is commentary.
- **Deprecation is a schedule with traffic thresholds**, not an announcement.
- **You cannot sunset what you cannot measure** — instrument first.
- **Two concurrent major versions is the practical ceiling**; a third is a maintenance failure.
- **Every breaking change gets a migration path**, even if it is "rewrite your integration".

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Consumer inventory | Logs + onboarding records | Each endpoint has identified callers or an explicit "unknown" |
| Single scheme | Code review | One mechanism across the surface |
| Change classification | Document | Table complete and applied in review |
| Schema artifact | Repository | Versioned, generated or hand-maintained, in CI |
| Contract tests | CI run | Schema diff fails on breaking change |
| Unknown-field tolerance | Client test | Clients ignore additions (or are documented as not) |
| Deprecation headers | Response inspection | `Deprecation`/`Sunset` present where applicable |
| Traffic measurement | Metrics | Usage per version measurable before sunset |
| Sunset window | Policy | Matches `{{SUNSET_WINDOW}}`, with an approver |
| Webhook/SDK contracts | Audit | Event and SDK changes follow the same rules |

## 7. Failure handling

- **No visibility into consumers** → add request identification first; until then every removal is a guess and should be blocked.
- **A breaking change already shipped** → treat as an incident: identify affected consumers from error rates and support tickets, restore the old behaviour behind a flag, and run the deprecation as a documented process rather than a notification.
- **A partner refuses to migrate** → the decision is commercial; document the exception, the maintenance cost, and the date it is revisited — an unbounded exception becomes permanent.
- **The API is internal service-to-service** → versioning is cheaper (you control both sides), but contract tests matter more, because a deploy and a consumer deploy are not atomic.
- **GraphQL surface** → field deprecation is built in; the trap is changing a resolver's semantics without changing the schema. Contract tests must assert behaviour, not only shape.
- **The schema artifact has drifted** → regenerate from code and diff; drift is the failure the artifact exists to prevent.

## 8. Security and authorisation

Risk class B; sunsetting a version is C and requires `{{APPROVER}}`. Contract fixtures must be sanitised of personal data and tokens. Public API documentation must not disclose internal endpoints, admin routes, or unfixed vulnerabilities. Deprecation notices sent to consumers must go through the channel the consumer agreed to, not a public changelog alone.

## 9. Completion criteria

- [ ] Consumers inventoried, with unknowns explicitly recorded.
- [ ] Single versioning mechanism chosen and documented.
- [ ] Change classification table written and used in review.
- [ ] Schema artifact versioned and checked in CI.
- [ ] Contract tests fail on a breaking change (demonstrated).
- [ ] Deprecation sequence defined with traffic thresholds and dates.
- [ ] Traffic per version measurable.
- [ ] Sunset policy and approver named.
- [ ] Webhook and SDK contracts included in scope.
- [ ] Maximum concurrent versions stated.

## 10. Deliverables and handover

Artifacts: `.api/VERSIONING.md`, consumer inventory, contract tests, deprecation schedule.

Handover: `04-process/code-review/` uses the change classification as a review checklist for API diffs; `MOB-P03` aligns client-version compatibility with the same policy; `04-process/dependency-management/` applies the mirror-image rule when *you* are the consumer; `04-process/documentation/` publishes the changelog the policy promises.
