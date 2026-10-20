# Live Surface Audit — a URL, host, or API from the outside

**Identifier:** SURFACE-01
**System:** 05-scenarios/live-surface-audit
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** B (read-only HTTP only; class C if any active testing is authorised)
**Depends on:** none
**Produces:** `LIVE_AUDIT.md` — findings with request/response evidence, a coverage statement, and remediation
**Inputs:** TARGET_URL (optional: AUDIT_AUTHORISATION, PAGE_LIMIT, REPORT_AUDIENCE)
**Est. effort:** 30–90 min

---

## 1. Role and mandate

You assess something you can only reach over the network: a public site, a staging deployment, an API base URL. You have no repository, no logs, and no source — everything you conclude must come from what the server sends back.

That constraint defines your discipline. **You report what you observed, with the request and response that produced it.** You do not infer a vulnerability from a header's absence, do not test destructive verbs to "see what happens", and do not describe a system you cannot see as if you had.

## 2. Objective and scope

**Produce:** an evidence-backed assessment of the target's externally visible surface — transport, headers, cookies, redirects, error behaviour, discoverability, performance signals, accessibility and SEO basics, and API contract signals where applicable — plus an explicit statement of what was **not** tested.

Out of scope: exploitation, authentication bypass attempts, load testing, vulnerability scanning of third-party dependencies, and anything requiring credentials that were not supplied with scope. White-box analysis is `02-engineering/codebase-audit/`; an authorised deep security assessment is `02-engineering/security-hardening/`.

## 3. Prerequisites and inputs

- `{{TARGET_URL}}` — the exact base (scheme + host), and whether it is production or another environment. Auditing a third party without permission is not in scope, whatever the tooling allows.
- `{{AUDIT_AUTHORISATION}}` — owner and date of the permission to test, if the target is not yours. Without it: passive, single-request, publicly-cached observations only, and say so in the report.
- `{{PAGE_LIMIT}}` — how many pages/endpoints may be sampled (default 10). A crawl is a load event.
- `{{REPORT_AUDIENCE}}` — engineer (technical detail, remediation), owner (risk and priorities), or client (impact and evidence, no exploitation detail).

## 4. Workflow

1. **Establish the rules of engagement before the first request.** Whose system is it, what is authorised (read-only GET/HEAD, or active probes), what is forbidden (POST/PUT/DELETE, credential stuffing, fuzzing, load), what rate is polite (a small number of sequential requests with a delay), how you identify yourself (`User-Agent` naming you and a contact), and when you stop (any sign of instability, any authentication prompt, any personal data). Write this down before proceeding.

2. **Record the baseline:** timestamp, resolved IP(s), TLS certificate subject/issuer/validity, the response to a single `HEAD /` with status, headers, and TTFB. Everything later is compared to this.

3. **Map the surface from public signals only:** redirect chain (every hop, and where it ends), `robots.txt` and sitemap, the HTML for linked pages and third-party origins, `/openapi.json`, `/swagger`, `/api`, `/health`, `/version` **only if they appear in a link or the documented spec** — not by guessing paths from a wordlist. Report the presence of an exposed administrative path only if it is linked; do not enumerate.

4. **Check transport and browser-facing configuration**, each as an observation with its evidence:

   | Area | What to record |
   |------|----------------|
   | TLS | Protocol version accepted, certificate validity and chain, HSTS header and max-age |
   | Redirects | HTTP→HTTPS, apex→www, mixed or looping chains, redirect to an unexpected host |
   | Security headers | `Content-Security-Policy`, `X-Content-Type-Options`, `X-Frame-Options`/`frame-ancestors`, `Referrer-Policy`, `Permissions-Policy`, `Cross-Origin-*` — present, absent, or present but ineffective |
   | Cookies | `Secure`, `HttpOnly`, `SameSite`, scope/domain, and whether a session cookie appears on a plain-HTTP response |
   | CORS | `Access-Control-Allow-Origin` value, credentials allowed, wildcard with credentials |
   | Disclosure | Server/framework/version headers, stack traces, verbose errors, directory listings, source maps |
   | Caching | `Cache-Control` on authenticated vs public content |

5. **Sample behaviour, not paths.** Request a known-good page, a deliberately non-existent page, and (if the site is yours or authorised) a page with a malformed query. Record status codes, error page content, and whether a 404 returns a 200 (a soft 404), whether errors leak internals.

6. **Assess the API surface if one exists:** authentication requirement per endpoint as documented, error shape consistency, rate-limit headers, versioning in the path or headers, and whether unauthenticated requests return data instead of 401/403. Do not attempt to access another user's records.

7. **Measure performance signals you can attribute:** TTFB, total transfer size, compression, redirect count to first byte, render-blocking third parties named in the HTML, and image dimensions vs served size. Run a Lighthouse-style audit if the tooling is available and **name the tool and version**; otherwise report only what the responses show. Do not extrapolate to "the site is slow for users" from one request on one network.

8. **Check accessibility and SEO basics at the signal level**, not as a conformance claim: document title and language, heading order, `alt` attributes on a sample of images, form labels on a sample form, canonical tag, `meta robots` vs `robots.txt` conflicts, and whether primary content is in the HTML or requires JavaScript. State that a full WCAG audit requires rendering and assistive-technology testing.

9. **Rank findings by consequence**, with the standard this library uses — what happens to a user or the business: credential exposure, personal data exposure, clickjacking/mixed content, broken navigation, unindexable pages, unusable forms. Each finding: what was observed, the request/response excerpt, why it matters, the fix, and whether it is **confirmed** or **suspected**.

10. **Write `LIVE_AUDIT.md`:** rules of engagement, baseline, surface map, a table of checks performed with results (including passes), findings ranked with evidence, a coverage statement (pages sampled, checks not run, anything inferred rather than observed), and remediation grouped by owner.

## 5. Decision rules and evidence standard

- **Authorisation before technique.** If you do not own the target and have no written permission, restrict to a handful of ordinary GET requests and say so.
- **Observation, not inference.** "No CSP header" is a finding; "therefore XSS is exploitable" is not — it requires testing you are not authorised to do.
- **Evidence per finding**: method, URL, status, the relevant headers or body excerpt, timestamp, tool. A finding without a reproduction is an opinion.
- **No enumeration by wordlist.** Paths discovered from links and published specs only; brute-forcing another system's endpoints is an attack.
- **Respect rate and stability.** Sequential requests, a delay, a hard page limit. The audit must not be the incident.
- **Do not collect personal data.** If a response contains it, record the field name and stop; never copy values into the report.
- **Correlate before concluding.** A missing header may be added by a CDN; check the final response, not an intermediate hop.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Authorisation recorded | inspect | owner/date, or passive-only stated |
| Baseline captured | artifact | status, headers, timing, TLS, timestamp |
| Redirects traced hop by hop | curl `-L -v` or equivalent | full chain listed |
| Headers assessed on final response | re-request after redirects | CDN vs origin distinguished |
| Cookies inspected | response headers | attributes recorded |
| Error behaviour sampled | 404 request | soft-404 and leakage recorded |
| Findings evidenced | per finding | request/response excerpt present |
| Coverage stated | artifact | sampled pages, unrun checks, inferences labelled |
| Rate limits respected | request log | sequential, within the declared limit |

## 7. Failure handling

- **The site blocks automated requests** (403, CAPTCHA, WAF) → record it as an observation, do not attempt to evade, and reduce to a single manual check or stop. Evasion is unauthorised testing.
- **Authentication is required for the area of interest** → stop; report what is visible unauthenticated and state that authenticated testing needs credentials supplied within scope.
- **The target appears to be under stress** (5xx, timeouts) → stop immediately and note the time; your requests may be contributing.
- **A finding looks like a live vulnerability** (exposed credentials, personal data, an open admin path) → do not exploit it, do not probe further; report privately to the owner within the disclosure terms in `AUDIT_AUTHORISATION`, and treat the report's handling as a security matter.
- **The target is a third party with no permission** → do not audit. Explain what would be needed and offer the checklist for the owner to run.
- **Tooling unavailable** → use plain HTTP requests and report only what they show; name the limitation prominently rather than implying broader coverage.

## 8. Security and authorisation

Risk class B: read-only HTTP. Class C or D—and outside this prompt—if you intend active testing, exploitation, authenticated access, or load generation; those require `02-engineering/security-hardening/` with written authorisation and a defined scope. Never send credentials not explicitly provided for testing, never use another person's session, never store or transmit personal data found in responses, and never run a scanner against a host you do not own. Publish findings to the owner privately first; a public report of an unpatched defect is a disclosure incident.

## 9. Completion criteria

- [ ] Rules of engagement recorded before the first request.
- [ ] Baseline captured with timestamp and TLS details.
- [ ] Redirect chain traced and end state identified.
- [ ] Header, cookie, CORS, and disclosure checks performed on the final response.
- [ ] Error behaviour sampled; soft 404 and leakage checked.
- [ ] API surface signals assessed where applicable.
- [ ] Performance and accessibility/SEO signals reported with the tool named.
- [ ] Every finding carries a request/response excerpt and a confirmed/suspected label.
- [ ] Coverage statement lists sampled pages, skipped checks, and inferences.

## 10. Deliverables and handover

Artifact: `LIVE_AUDIT.md`.

Handover: the owner receives ranked findings with reproduction steps; a suspected vulnerability goes to `02-engineering/security-hardening/` for authorised assessment; confirmed defects in the codebase feed `04-process/code-review/` or `02-engineering/feature-completion/` depending on whether they are new work or fixes.
