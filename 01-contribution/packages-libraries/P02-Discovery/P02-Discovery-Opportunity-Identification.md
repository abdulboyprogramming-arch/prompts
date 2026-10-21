# PROMPT 02 — Discovery & Opportunity Identification: read the consumers, not just the code

**Identifier:** PKG-P02
**System:** 01-contribution/packages-libraries
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** diagnostic
**Risk class:** A — it reads the repository, its releases, and public consumer code
**Depends on:** PKG-P01
**Produces:** `OPPORTUNITIES.md` with a consumer-evidence table: each candidate shows who hit the problem, in what code, and what the fix would cost the public surface
**Inputs:** PROJECT_CONTEXT, ISSUE_TRACKER (optional: RELEASE_HISTORY, DOWNSTREAM_SEARCH, SEMVER_POLICY)
**Est. effort:** 60–120 minutes

---

## 1. Role and mandate

You are the discovery stage of a package or library contribution. Your job is to find friction that **someone outside this repository has already felt**, and to record the evidence that they felt it.

**Why this stage differs from its siblings.** `W3-P02` maps a trust boundary, because its defects are silent until exploited. `WEB-P02` walks a running application, because its defects are visible in a browser. A library has neither: it has **consumers**, and they are not in the repository. The characteristic failure is *a list of API improvements the maintainer would like, produced from reading the API, with no evidence that any user wanted them.*

The instrument is consumer evidence. A defect with three downstream workarounds is worth more than a design improvement with none, and the difference is visible only if you go and look at the code that imports this package. That is what makes this stage distinct: the search happens partly outside the repository being contributed to.

## 2. Objective and scope

**Produce:** `OPPORTUNITIES.md` where each candidate records the consumer evidence (issue, downstream workaround, error message in the wild), the friction it represents, the surface cost of fixing it, and whether a fix can be non-breaking.

Out of scope: designing the API, deciding the version, or proposing features the maintainer has not asked for. Discovery finds problems with witnesses; `PKG-P03` prices them.

## 3. Prerequisites and inputs

- `{{PROJECT_CONTEXT}}` — from `PKG-P01`: the public surface, the supported runtimes, the release history, and the contribution conventions.
- `{{ISSUE_TRACKER}}` — open and recently closed issues, sorted by reactions and by age. Reactions are the closest thing a library has to a vote.
- `{{RELEASE_HISTORY}}` — the changelog and the tags. Regressions cluster near recent releases, and a fix that was reverted is a candidate with its history already written.
- `{{DOWNSTREAM_SEARCH}}` — how to search code that depends on this package: a package registry's dependents page, a code-search engine, or a local clone of a well-known consumer.
- `{{SEMVER_POLICY}}` — the versioning rule, so a candidate can state whether its fix is shippable in a patch.

## 4. Workflow

1. **Read the public surface first and write it down.** Exported functions, types, options, errors, and the documented examples. Everything you find afterwards is judged against this list, because a fix that grows it costs more than one that does not.

2. **Mine the tracker for friction, not for wishes.** Sort by reactions and by duplicates: three separate issues about the same error message are one candidate with strong evidence. Record the exact error text users paste, because it is what a fix must change.

3. **Search downstream code for workarounds.** This is the step that distinguishes this stage. For each public function, look for consumers wrapping it, catching a specific error, re-implementing it, or pinning an old version. A wrapper in three repositories is stronger evidence than an issue with no reactions:

   | What you find downstream | What it means |
   |---|---|
   | The same try/catch around one call | The error is unactionable or too broad |
   | A local copy of the function | The public one lacks a needed option |
   | A pinned old major in a maintained project | A breaking change lost someone |
   | A documented workaround in a README | The library's own docs are the workaround |

4. **Check the release history for regressions and reverted fixes.** A regression introduced in a minor release and reported twice is a high-value candidate: the maintainer already knows the code, and the fix restores behaviour rather than adding it.

5. **Read the documentation as a defect surface.** Examples that no longer compile against the current version, an option documented but not implemented, types that contradict the prose. These are cheap, welcome, and require no API decision — a documentation PR from a stranger is one of the few that merges quickly.

6. **Check the edges of the support matrix.** A minimum runtime the package claims but no longer tests, a peer dependency range that excludes a widely used version, an ESM/CJS combination that fails in a clean install. These are found by installing the package, not by reading it, which is why they are usually unclaimed.

7. **Record every candidate with its evidence and its surface cost.** A row without a consumer witness is a hypothesis, and it belongs in a separate section:

   | # | Candidate | Consumer evidence | Surface cost | Ship window |
   |---|---|---|---|---|
   | 1 | `parse()` throws `Error` instead of a typed error on malformed input | 12 issues with the same message; 3 downstream `catch` blocks matching on the string | None — replaces an untyped throw | Patch, if the message is unchanged |
   | 2 | The documented `timeout` option is ignored by `fetchAll()` | 2 issues; 1 downstream wrapper implementing its own timeout | Fix only; no new option | Patch |
   | 3 | ESM import fails in a clean project under Node 20 | Reproduced by installing the tarball; 0 issues filed | Packaging fix | Patch, urgent |

8. **Rank by evidence strength, then by surface cost, then by ship window.** Fifteen users hitting one error outranks a defensible improvement; a patch-shippable fix outranks a better one that waits for a major, because the second may never land.

9. **Say what the maintainer has already declined.** If the tracker contains a maintainer decision against a candidate, record it and drop the candidate. Re-proposing a rejected design is the fastest way to be ignored, and the record is publicly available.

10. **Mark unverified candidates separately.** A design concern you believe in, with no witness, is legitimate to note and must not be ranked alongside evidence.

## 5. Decision rules and evidence standard

- **A candidate needs a witness.** An issue, a downstream workaround, a reproduction from installing the package, or a documentation contradiction. Reading the API and imagining a user is not discovery.
- **The surface cost is part of the finding.** A fix that adds an option is a different proposal from a fix that changes none, and the difference decides whether it can ship in a patch.
- **Duplicates are a signal, not noise.** Three reports of one error message is the strongest evidence a library issue tracker produces.
- **A reverted fix is a candidate with a history.** Read why it was reverted before proposing it again.
- **Documentation defects are the cheapest wins available.** They need no API decision and they merge fast.
- **Never re-propose what the tracker shows was declined.** The maintainer's no is part of the context.
- **Ship window comes before elegance.** A patch-shippable fix that helps today beats a better fix in a major release that may not happen.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Surface listed first | Exported symbols and documented options | Written down before candidate hunting |
| Tracker mined | Reactions and duplicates | Duplicate clusters counted, exact error text recorded |
| Downstream searched | Code search or dependents | Each public function checked for wrappers and pins |
| Release history read | Changelog and tags | Regressions and reverts recorded as candidates |
| Docs tested | Examples run or read against the source | Contradictions recorded |
| Support matrix checked | Clean install per runtime | Failures recorded with the runtime named |
| Evidence recorded | Row template | Every candidate has a witness and a surface cost |
| Ship window stated | Patch, minor, major | Each candidate classified |
| Declined designs noted | Tracker decisions | Rejected candidates recorded and dropped |
| Unverified separated | Appendix | Witness-free ideas kept out of the ranked list |

## 7. Failure handling

- **Downstream code cannot be searched** (private consumers, no dependents index) → fall back to the tracker and the clean-install checks, and say that consumer evidence is limited to reported issues.
- **The tracker has hundreds of open issues** → cluster by error message and by module before reading individual reports; a sample of twenty clusters is more useful than two hundred rows.
- **A candidate requires a new option to fix** → record it anyway with its surface cost. It is `PKG-P03`'s decision whether the option is worth its permanence, not yours to suppress.
- **The package is pre-1.0 with no users** → consumer evidence will be thin; the productive candidates are documentation, packaging, and clean-install defects, and the document should say so rather than manufacturing demand.
- **A regression is live in the latest release** → this is the highest-priority candidate in the document; say so in the first line, because a broken latest release is the one thing a maintainer will stop and fix.
- **The maintainer has declined the whole category** (for example, no new options ever) → respect it and search what remains: fixes, types, docs, packaging.

## 8. Security and authorisation

Class A: the stage reads public code and writes one document. Three cautions. First, installing a package to test it runs its install scripts; use a disposable environment, not a workstation with credentials. Second, a security issue in the package is not a normal candidate: follow the project's disclosure policy, and do not open an issue describing the exploit. Third, downstream code you read may contain secrets committed by its authors; quote the workaround shape, never the file contents.

## 9. Completion criteria

- [ ] Public surface written down before discovery began.
- [ ] Tracker mined by reactions and duplicate clusters, with exact error text.
- [ ] Downstream workarounds searched and recorded.
- [ ] Release history checked for regressions and reverted fixes.
- [ ] Documentation contradictions tested against the source.
- [ ] Support matrix checked by clean install.
- [ ] Every candidate carries a witness and a surface cost.
- [ ] Ship window stated for each candidate.
- [ ] Designs the maintainer declined are recorded and excluded.
- [ ] Witness-free ideas kept in a separate appendix.

## 10. Deliverables and handover

`OPPORTUNITIES.md` — the surface list, the consumer-evidence table, the documentation and packaging findings, the declined-designs note, and the unverified appendix.

Handover: `PKG-P03` builds its surface cost ledger from the cost column here and will reject a candidate with no witness. A regression against the latest release goes to the front of the list and may justify skipping selection entirely: a broken release is the one case where the work chooses itself. Security findings leave this document for the project's disclosure channel, and the entry here records only that they were routed.
