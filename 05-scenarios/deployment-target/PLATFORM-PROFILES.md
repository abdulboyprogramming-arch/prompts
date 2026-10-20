<!-- not-a-prompt -->
# Platform Profiles

Reference for [`DEPLOY-TO-PLATFORM.md`](DEPLOY-TO-PLATFORM.md). The prompt is provider-agnostic; this file holds the provider-specific traps. Read the row for `{{DEPLOY_PLATFORM}}` before step 2 of the prompt.

**Status:** reference material, kept current by hand. Limits change without notice — verify against the provider's current documentation before relying on a number, and record the date you checked.

| Platform | Best for | Runtime model | Characteristic traps | Verify before shipping |
|----------|----------|---------------|----------------------|------------------------|
| **Vercel** | Next.js/Nuxt/SvelteKit, static+SSR, previews | Serverless functions + edge + CDN | Build-time inlining of `NEXT_PUBLIC_*`; function duration caps by plan; edge runtime lacks Node APIs; image optimisation billed; preview deployments are public by URL | Function duration, region, preview visibility, image/bandwidth usage |
| **Netlify** | Static, JAMstack, functions | CDN + Lambda-style functions | `_redirects`/`netlify.toml` ordering (first match wins); build minutes metered; functions have their own env scope; large forms/uploads need external storage | Redirect precedence, function timeout, form/upload path |
| **Cloudflare Pages / Workers** | Static + edge compute | V8 isolates, no full Node runtime | No filesystem, no native modules, CPU-time (not wall-clock) limits, `nodejs_compat` gaps, KV/R2/D1 instead of disk | Runtime compatibility, CPU limit, storage binding |
| **Render** | Web services, workers, cron, Postgres | Containers or native runtimes | Free tier spins down (cold start on first request); disk is ephemeral unless a paid disk is attached; cron runs in UTC | Spin-down behaviour, persistent disk, cron timezone |
| **Railway** | Full apps + managed DBs | Containers/Nixpacks | Usage-based billing is easy to exceed; services sleep on free credits; private networking is per-project | Plan limits, private networking, volume mounts |
| **Fly.io** | Global anycast, Docker-native | MicroVMs | `fly.toml` region/scale defaults; machines stop when idle unless configured; volumes are per-region; release commands vs app start | Machine autostop, volume region, health check path |
| **Heroku** | Classic PaaS, add-ons | Dynos | Ephemeral filesystem (resets daily), 30 s router timeout, dyno hours, `Procfile` process types, add-on billing | Dyno type, timeout, add-on ownership |
| **AWS (App Runner / ECS / Lambda / Amplify)** | Enterprise, VPC access, compliance | Varies by service | IAM roles are the real configuration; security groups and subnets silently block egress; Lambda package size and cold starts; Amplify build images differ from local | IAM role, VPC/egress, size limits, region |
| **GCP Cloud Run** | Containers, scale-to-zero | Knative containers | Container must listen on `$PORT` and `0.0.0.0`; concurrency default 80 per instance; min instances cost money; Cloud SQL needs the connector | Port binding, concurrency, min instances, connector |
| **Azure App Service** | .NET/Java/Node enterprise | App Service plans | Always On is a paid setting (otherwise idle unload); deployment slots for staging; app settings per slot | Always On, slot settings, plan tier |
| **VPS + Docker** | Full control, predictable cost | Your container, your OS | You own TLS renewal, log rotation, backups, OS patches, and the firewall; a single box is a single point of failure | Certbot renewal timer, backup job, firewall rules, restart policy |
| **Kubernetes** | Multi-service, teams with platform skills | Pods/Deployments/Ingress | Resource requests vs limits, readiness vs liveness probes (a wrong readiness probe removes all pods), PVC storage class, image pull secrets | Probes, resources, storage class, ingress TLS |

## Universal checks, independent of provider

Whatever the platform, these six are where deployments actually break:

1. **Port and host binding** — listen on `0.0.0.0` and the injected `$PORT`, never a hardcoded `localhost:3000`.
2. **Environment scope** — the same variable name exists in build, runtime, and preview scopes, and only one of them is populated.
3. **Filesystem** — anything written at runtime is lost; uploads, caches, and generated reports need object storage or a database.
4. **Timeouts** — the platform's request/execution limit is lower than your slowest legitimate query.
5. **Region and residency** — the data sits where the law and the latency require, and the database is in the same region as the compute.
6. **Rollback** — the previous deployment can be promoted in one step, and you have done it once.

## Cost traps by model

| Billing model | What spikes | Guard |
|---------------|-------------|-------|
| Bandwidth / egress | A viral page, an image-heavy page, a scraping loop | Compression, image sizing, CDN caching, budget alert |
| Invocations / requests | A retry storm, a polling client, a crawler | Rate limiting, cache headers, request budget |
| Build minutes | Frequent rebuilds, monorepo full builds | Path-filtered builds, dependency caching |
| Compute time (GB-seconds) | A slow endpoint called often | Query and connection pooling, timeout, caching |
| Idle instances | Minimum instances kept warm | Set from measured cold-start cost, not comfort |
| Managed database | Connection count, storage growth | Pooling, retention policy, storage alert |

## When the platform is the wrong answer

Recommend leaving the platform — and say so plainly — when any of these holds:

- The workload needs a persistent local filesystem, GPU, or a long-lived connection the platform caps (websockets with hours-long sessions, streaming jobs over the execution limit).
- Compliance requires a region, network isolation, or an audit trail the plan does not offer.
- The cost curve is dominated by egress or invocations and a fixed-cost host is materially cheaper.
- The team cannot operate the platform's failure modes (cold starts, ephemeral disk) and the product needs guarantees they cannot give.

In that case: [platform migration](../platform-migration/PLATFORM-MIGRATION.md) for the move, and record the reason in `TARGET_PROFILE.md` so the decision is not re-litigated from memory.
