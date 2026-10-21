# Environment Parity: why it works here and not there

**Identifier:** ENVPARITY-01
**System:** 05-scenarios/environment-parity
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** audit-remediation
**Risk class:** A for comparison; B for configuration and CI changes; **C** for changes to a shared staging or production environment
**Depends on:** none
**Produces:** `.env/PARITY_REPORT.md`, a divergence diff, config contract, CI parity job
**Inputs:** TARGET_ENV (optional: SOURCE_ENV, APPROVER, TIME_BUDGET)
**Gallery:** "It works locally", staging behaves differently from production, or a bug reproduces on one machine and not another — find the difference that matters instead of the dozens that do not.

---

## 1. Role and mandate

You find the difference between two environments that explains a behaviour difference: local versus CI, CI versus staging, staging versus production, one developer's machine versus another's.

Environments diverge in thousands of ways and almost all of them are harmless. The skill is not listing differences; it is **ranking them by whether they can change behaviour** and proving which one does. A different node patch version is noise. A different database isolation level is not.

The most expensive class of divergence is the one that hides a defect until production: a feature flag that is on in staging, a queue with no consumer in dev, a clock that is UTC everywhere except your laptop, and a validation rule applied by an API gateway nobody configured locally.

## 2. Objective and scope

**Produce:** a behaviour-relevant divergence inventory between the named environments, the specific differences that can change behaviour, evidence for the one causing the reported symptom, and controls that keep the parity gap from silently growing.

Out of scope: building a new environment, redesigning the deployment topology, and application performance differences that are purely capacity (that is `05-scenarios/capacity-planning/`).

## 3. Prerequisites and inputs

- `{{TARGET_ENV}}` — the environment that behaves unexpectedly, and the symptom: what differs from the other environment, in observable terms.
- `{{SOURCE_ENV}}` — the environment where it works (default: local development).
- `{{APPROVER}}` — for changes to shared environments.
- `{{TIME_BUDGET}}` — how deep the comparison goes; the ranking below makes a two-hour pass useful.

## 4. Workflow

1. **State the symptom as an observation, not a diagnosis.** "The list endpoint returns 12 items in staging and 240 locally" is a fact; "the cache is different" is a guess. Every later step is a test of a hypothesis against this observation.

2. **Enumerate the layers that can actually change behaviour**, in this order — it is roughly the order of how often each is the cause:

   | Layer | What to compare |
   |---|---|
   | Configuration and feature flags | Every env var and flag: present/absent, value, default when missing |
   | Data | Row counts, tenancy, seed versus real data, deleted rows, character sets, timezone of stored timestamps |
   | Dependencies' versions | Runtime, package lockfile, database engine and extension versions, OS libraries |
   | Services and architecture | Which processes exist: cache, queue worker, search, reverse proxy, gateway |
   | Network and routing | DNS, TLS termination, redirects, CORS, load balancer timeouts, egress rules |
   | Resource limits | CPU/memory limits, connection pool size, timeouts, body size limits, rate limits |
   | Permissions and identity | Roles, scopes, credentials used by the app, service accounts |
   | Time and locale | System timezone, locale, ICU data, DST handling |
   | Build | Minified versus dev build, source maps, env-var inlining, NODE_ENV effects, tree-shaking |

3. **Diff the configuration mechanically, not from memory**, and include what is *missing*. A variable absent in one environment falls back to a code default, and the default is where the surprise lives. Produce a three-way table: name, value in A, value in B, and the code default.

4. **Check the defaults and the branches that only exist in one mode.** Production builds often enable different code paths: assertions compiled out, dev-only error overlays, strict-mode differences, `NODE_ENV`-gated caching, and client-side libraries that behave differently when minified. A bug that only exists in the minified build is a real class, not a myth.

5. **Compare the data shapes, not just the row counts.** Staging with 12 rows never exercises pagination, the query planner chooses a different plan at 240,000 rows, and a unique constraint never fires because the fixture has no duplicates. For each environment record: row counts per table, the largest string, the distribution of one key column, and whether soft-deleted rows exist.

6. **Find the silent service gaps.** A queue with no consumer means jobs appear to succeed and never run; a cache with no eviction means memory grows until the first eviction; a search index that is never rebuilt means search returns nothing and the UI shows an empty state rather than an error. List which services run in one environment and not the other.

7. **Prove the cause with an experiment, not a description.** Change one variable between environments (or reproduce the target configuration in the source environment) and show the symptom follows it. If flipping the candidate does not move the symptom, it was not the cause — keep the list and continue. Record each experiment and its result; a parity report full of "likely" is a guess with formatting.

8. **Fix at the right layer.** In order of preference: make the behaviour explicit in code (no reliance on an implicit default); declare the variable in the config contract with a required/optional schema and no ambiguous defaults; generate environment files from one source; add the divergence to a CI parity check. Do not fix it by copying a value into the target environment and hoping nobody re-deploys from the template.

9. **Write the parity check** so the gap cannot grow silently: a job that compares the **keys** (not the secret values) of every environment's configuration against the contract, fails when a key is missing or has an incompatible type, and reports added keys as a warning. Secrets are compared by presence and format, never by value.

10. **Write `.env/PARITY_REPORT.md`**: symptom, environment matrix, ranked divergences with the behaviour each can change, experiments and results, the confirmed cause, the fix and its verification, and the residual differences that are accepted (with the reason they are safe).

## 5. Decision rules and evidence standard

- **Rank by behavioural consequence, not by novelty.** A version difference that cannot change the symptom is not the finding.
- **Missing is a value.** An absent variable means a code default, and defaults differ from what people believe.
- **Prove the cause by experiment.** Flipping the candidate must move the symptom.
- **Data volume is part of the environment.** Staging that cannot reproduce production's scale cannot reproduce production's bugs.
- **Service gaps are silent by design**; enumerate what runs where rather than assuming the stack is the same.
- **Fix the default, not the deployment.** Copying a value leaves the next deploy to reintroduce the divergence.
- **Secrets are compared by shape, never by value**, and never printed.
- Mark each claim `verified` (measured or executed) or `inferred`.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Symptom stated observably | Report | Fact with both environments' values |
| Config diff | Mechanical comparison | All keys, values, and defaults, including missing keys |
| Build-mode differences | Build config + artifacts | Dev-only paths enumerated |
| Data comparison | Queries | Counts, largest values, distributions, soft-deleted rows |
| Service inventory | Process/host list | Every service in each environment listed |
| Limits compared | Config | Pools, timeouts, body and rate limits |
| Time and locale | Runtime | Timezone and locale captured per environment |
| Cause proven | Experiment | One variable flipped; symptom follows |
| Fix verified | Re-run | Symptom gone in the fixed environment |
| Parity check | CI job | Missing or mistyped key fails the build |
| Accepted differences | Report | Each with a reason it cannot change behaviour |

## 7. Failure handling

- **The target environment cannot be inspected** (no access, no shell) → compare what is observable from outside: responses, headers, errors, timings; state the limits of the method.
- **Configuration differs by design** (staging talks to a sandbox vendor) → record it as accepted, and check whether the sandbox's different behaviour is itself the cause.
- **The symptom will not reproduce anywhere else** → that is a parity gap in the *other* direction: capture the failing environment's state (versions, config checksums, data snapshot metadata) before anything is redeployed, because the evidence disappears with the next deploy.
- **Two divergences are both plausible** → flip them one at a time; do not "fix everything and see".
- **Fixing parity would break the environment** (a local-only dependency) → introduce an explicit switch with a documented default rather than an implicit difference.
- **Someone wants to make staging identical to production** → that is usually impossible and not the goal; the goal is that no divergence changes behaviour silently.

## 8. Security and authorisation

Comparison is class A. Changing configuration in a shared environment is **C** and requires `{{APPROVER}}`; changing production is C or D by blast radius. Never copy production data into staging to reproduce a bug without a masking plan (`04-process/privacy-requests/`, `05-scenarios/data-residency/`). Configuration dumps contain secrets: compare hashes or presence, redact values in the report, and keep the report out of public repositories.

## 9. Completion criteria

- [ ] Symptom stated as an observation with both environments' values.
- [ ] Configuration diffed mechanically, including missing keys and defaults.
- [ ] Build-mode and runtime differences enumerated.
- [ ] Data compared by shape and volume, not only counts.
- [ ] Service inventory compared.
- [ ] Limits, timeouts, and pools compared.
- [ ] Cause proven by a single-variable experiment.
- [ ] Fix applied at the code or contract layer, verified.
- [ ] CI parity check added and shown failing on a missing key.
- [ ] Accepted divergences documented with a reason.

## 10. Deliverables and handover

Artifacts: `.env/PARITY_REPORT.md`, config contract, parity CI job, experiment log.

Handover: `05-scenarios/dev-environment/` owns making local setup reproducible; this prompt explains behaviour differences that survive a correct setup. `05-scenarios/deployment-target/` covers platform-specific configuration scopes. `05-scenarios/capacity-planning/` takes over when the difference is resource-driven rather than behavioural. `04-process/testing-qa/` should turn the confirmed cause into a regression test that runs in CI, because a parity gap that is only fixed in the deployment returns with the next one.
