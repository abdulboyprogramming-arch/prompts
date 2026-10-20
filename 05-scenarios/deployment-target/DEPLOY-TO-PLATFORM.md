# Deploy to a Managed Platform

**Identifier:** DEPLOY-01
**System:** 05-scenarios/deployment-target
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** C — creates or reconfigures the system that serves production traffic
**Depends on:** none (release-engineering P01–P04 consumes this once the target exists)
**Produces:** `.deploy/TARGET_PROFILE.md`, a working deployment, `DEPLOY_NOTES.md`
**Inputs:** DEPLOY_PLATFORM, REPO_PATH, TARGET_ENV (optional: TARGET_SERVICE, DOMAIN_NAME, SPEND_LIMIT, APPROVER)
**Est. effort:** 45 min – 3 h for a first deployment

---

## 1. Role and mandate

You are putting an application onto a managed platform: Vercel, Netlify, Cloudflare, Render, Railway, Fly.io, Heroku, Cloud Run, App Service, or a plain VPS with Docker. The provider is a variable — **`{{DEPLOY_PLATFORM}}`** — and this prompt stays provider-agnostic. Platform-specific traps live in [`PLATFORM-PROFILES.md`](PLATFORM-PROFILES.md); read the profile for the chosen platform before step 2.

Managed platforms fail in ways a laptop never does: the build has a different clock, disk is ephemeral, functions time out, environment variables exist in three scopes, previews inherit production secrets, and the filesystem you wrote to yesterday is gone. Your job is to make those properties explicit **before** the first customer request.

## 2. Objective and scope

**Produce:** a documented target profile (runtime shape, build, config classes, limits, cost), a deployment that passes a real end-to-end check, and a rollback path that was exercised.

Out of scope: choosing the architecture (`02-engineering/from-scratch/`), release readiness and versioning (`04-process/release-engineering/` P01–P02), long-term observability (`04-process/observability-reliability/`), migrating an existing host (`05-scenarios/platform-migration/`).

## 3. Prerequisites and inputs

- `{{REPO_PATH}}` and `{{DEPLOY_PLATFORM}}` — the platform as it will actually be used (plan tier matters: free tiers change limits).
- `{{TARGET_ENV}}` — `preview`, `staging`, or `production`. The first deployment should not be production unless nothing else exists.
- `{{TARGET_SERVICE}}` if the repository is a monorepo or hosts several deployables; `{{DOMAIN_NAME}}` if a custom domain is required; `{{SPEND_LIMIT}}` — the monthly ceiling you must not exceed; `{{APPROVER}}` for anything that spends money or serves public traffic.

## 4. Workflow

1. **Classify the application shape**, because it decides almost everything else:

   | Shape | Needs | Typical failure on a managed platform |
   |-------|-------|---------------------------------------|
   | Static site / SPA | CDN, rewrite rules for client routing | Deep links 404 because no catch-all rewrite |
   | SSR (Next/Nuxt/SvelteKit/Remix) | build step, server runtime, ISR/cache | Build succeeds, runtime env vars missing or read at build time |
   | API / serverful | long-lived process, health check | Idle spin-down, cold start, request timeout on slow queries |
   | Background worker / cron | always-on process or schedule | Platform kills idle workers; cron runs in a different timezone |
   | Functions / edge | per-request invocation, cold start | Ephemeral filesystem, execution time limit, package size |
   | Database-backed | connection pooling | Connection exhaustion under serverless concurrency |

2. **Separate configuration into the three classes that platforms actually have**, and write down which variables belong to which. This is the single largest source of "works locally, broken deployed":
   - **Build-time** — inlined into the bundle (public prefixes, `NEXT_PUBLIC_*`, `VITE_*`). Secret here = leaked to every browser.
   - **Runtime** — read per request on the server. Must exist in the *runtime* scope of the target environment.
   - **Preview** — inherited by branch deploy previews. Production secrets must **not** be visible here.

3. **Map each secret to a store, never to a file.** Platform env-var settings or an external secret manager. Add a `.env.example` listing names only, and confirm `.env*` is git-ignored. Record where each value lives, who can rotate it, and what breaks if it leaks.

4. **Configure the build explicitly**: install command, build command, output directory, root directory (monorepos are the most common misconfiguration), Node/runtime version pinned, and lockfile respected. **Reproduce the build locally in a clean environment first** — a build that only works with your global cache will fail on the platform.

5. **Address the platform's physical constraints before deploying**, using its profile: ephemeral disk (uploads must go to object storage), request/execution timeout, memory, concurrency, region and data residency, outbound IP ranges (for allowlists at the database or a partner API), websocket support, file size limits, and idle behaviour.

6. **Set up the environment topology**: one project per long-lived environment (staging and production separate, not one project with a toggle), a preview policy per branch, and a rule that previews never point at the production database.

7. **Deploy to a non-production target first.** Follow the build log, not just the status: a green deploy can hide warnings that will bite (deprecations, oversized bundles, missing optional deps). Then run the end-to-end check: the primary user path through the deployed URL, not `GET /` returning 200.

8. **Configure the domain and TLS deliberately**: apex vs `www`, redirect direction (one canonical host), certificate issuance, HSTS only after every subdomain is HTTPS, and DNS TTL lowered *before* any future cutover rather than during it.

9. **Define health, logs, and alerting at the platform level**: a health endpoint that checks dependencies (not just process liveness), where logs go and how long they are retained, error tracking, uptime check on the real path, and an alert that reaches a named human.

10. **Bound the cost.** Record the plan, the included limits, what triggers overage (bandwidth, invocations, build minutes, egress, function GB-seconds), the budget alert, and the `{{SPEND_LIMIT}}`. A traffic spike on a metered platform is a financial incident, not just a performance one.

11. **Prove the rollback.** Promote a previous deployment, or redeploy a known-good commit, and record the time it took. A platform whose rollback you have never used is a platform with an untested recovery path.

12. **Keep an exit route.** Identify what is platform-specific (config format, storage API, cron syntax, edge runtime) and record how it would move. Do not adopt a proprietary feature you cannot replace without noting it.

13. **Write `.deploy/TARGET_PROFILE.md`** (shape, platform, plan, regions, config classes, limits, cost model, domains) and **`DEPLOY_NOTES.md`** (commands used, what was verified, what was not, rollback procedure, and the next operator's first three actions).

## 5. Decision rules and evidence standard

- **The platform is a variable; the guarantees are not.** Anything provider-specific belongs in `TARGET_PROFILE.md`, not hardcoded in the prompt or the code.
- **A deploy is not done when the build turns green.** It is done when the primary user path works on the deployed URL.
- **Secrets have three scopes; a secret in the wrong one is a breach.** Build-time secrets are public by definition.
- **Previews are public.** Assume every preview URL is indexable and reachable; never attach production data or secrets to one.
- **Assume the filesystem is temporary.** Uploads, caches, and generated files go to object storage or a database.
- **Timeout and cold start are product decisions.** A 10-second function limit changes what features are possible; state it rather than discovering it at scale.
- **Cost is a correctness property.** Record the metered units and the alert threshold before the traffic arrives.
- **Rollback is verified or it does not exist.**

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| App shape classified | profile doc | one shape, with its constraint list |
| Config split into build/runtime/preview | table | every variable assigned a class |
| Secrets in a store | repo scan + platform check | no secret in code, `.env*` ignored |
| Build reproduced clean | local clean build or container | same result as the platform |
| Monorepo root/output correct | deploy log | correct artefact served |
| Platform limits documented | profile | timeout, memory, disk, region recorded |
| Non-production deploy first | deploy log | target env stated |
| End-to-end path verified | real request through the app | primary flow works |
| Domain + TLS correct | DNS and certificate check | one canonical host, valid cert |
| Health and alerts | alert test fires | named recipient |
| Cost bound | budget alert set | limit and trigger recorded |
| Rollback exercised | promoted previous version | time recorded |
| Exit route noted | profile | platform-specific items listed |

## 7. Failure handling

- **The build fails only on the platform** → compare runtime version, lockfile handling, native dependencies, and case-sensitivity of paths (Linux is case-sensitive; macOS is not). Reproduce in a container with the platform's image.
- **The app builds but 500s at runtime** → check runtime-scope variables first, then the entry point/output path, then the port binding (`0.0.0.0` and `$PORT`, not `localhost:3000`).
- **Deep links 404** → add the SPA/SSR rewrite or catch-all route; this is a configuration defect, not a bug in the app.
- **Cold starts hurt the user path** → measure them, then either keep a minimum instance, move the slow dependency to a warm path, or change the product's expectation. Do not hide it with a spinner and call it solved.
- **Database connections exhaust** → introduce pooling (platform-provided or external); record the maximum concurrency the tier allows.
- **Cost spikes** → check for a crawler loop, a retry storm, or an unauthenticated endpoint; set the alert before re-enabling traffic, and record the incident.
- **Rollback fails** → stop, restore service by redeploying a known commit manually, and treat the platform's rollback as broken until proven otherwise; note it in `DEPLOY_NOTES.md`.

## 8. Security and authorisation

Risk class C: this changes what serves production traffic. Do not deploy to production without `{{APPROVER}}` and a stated window. Never commit credentials; never put a production secret in a build-time or preview scope; never disable authentication, rate limiting, or TLS verification to make a deployment work. Restrict preview deployments to the team where the platform allows it, and confirm the deployment is not publicly indexable before it carries real data. Platform accounts and billing are ownership-bearing: record who owns them, because that is what `04-process/handover/` P03 will have to transfer.

## 9. Completion criteria

- [ ] Application shape classified with its constraint list.
- [ ] Every configuration variable assigned to build, runtime, or preview scope.
- [ ] Secrets in a store; `.env*` ignored; `.env.example` lists names only.
- [ ] Build reproduced in a clean environment.
- [ ] Platform limits documented (timeout, memory, disk, region, cold start).
- [ ] Non-production deployment verified end to end.
- [ ] Domain canonical, TLS valid, redirects defined.
- [ ] Health endpoint, logs, error tracking, and an alert that reaches a human.
- [ ] Cost model recorded with a budget alert at or below `{{SPEND_LIMIT}}`.
- [ ] Rollback exercised and timed.
- [ ] Exit route and platform-specific dependencies noted.
- [ ] `TARGET_PROFILE.md` and `DEPLOY_NOTES.md` written.

## 10. Deliverables and handover

Artifacts: `.deploy/TARGET_PROFILE.md`, `DEPLOY_NOTES.md`, the deployment itself.

Handover: `04-process/release-engineering/` P01–P04 takes over for subsequent releases, using the target profile as the environment truth; `04-process/observability-reliability/` P01 receives the logs, metrics, and health endpoints as its starting inventory; `04-process/handover/` P03 receives the platform account ownership as an access item.
