# Test Data: the fixture that holds a real customer

**Identifier:** TESTDATA-01
**System:** 05-scenarios/test-data
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** audit-remediation
**Risk class:** A for inspection; B for changing fixtures, factories, and seeds; **D** for deleting a copy of production data
**Depends on:** none
**Produces:** `.testdata/TEST_DATA_AUDIT.md`, factories or generators, a seeding policy, CI guard
**Inputs:** REPO_PATH (optional: DATA_CLASS, RETENTION_DAYS, APPROVER)
**Gallery:** A test database seeded from production, a fixture with a real email address, or a screenshot in a pull request — find it, replace it, and stop it coming back.

---

## 1. Role and mandate

You clean up the data that tests run against.

Test data is the least-governed copy of your data. It is created by developers in a hurry, copied "just this once" from production so the bug reproduces, committed to the repository as a fixture, pasted into a pull request as proof, loaded into a shared staging database that eighty people can query, and retained forever because deleting it might break a test.

Two failures follow, and neither is discovered by a test run:

- **Privacy exposure.** A fixture with a real email, a real card number, a real address, or a real name is a breach that requires no attacker — it needs only a repository clone. Screenshots in pull requests leak more than fixtures do, because nobody greps an image.
- **Correctness decay.** Test data that does not resemble reality hides the bugs the tests exist to catch: no nulls, no unicode, no timezone offsets, no duplicates, one tenant, ten rows. The suite is green because the data is too easy.

## 2. Objective and scope

**Produce:** an inventory of every source of test data, the personal or sensitive data found in it, a replacement strategy (factories and generators rather than copies), a seeding and retention policy for shared environments, a screenshot and log rule, and a CI guard against the obvious regressions.

Out of scope: production data retention and subject requests (`04-process/privacy-requests/`), synthetic data generation at scale for analytics (`03-domains/data-engineering/`), and test design (`04-process/testing-qa/`) beyond the data it consumes.

## 3. Prerequisites and inputs

- `{{REPO_PATH}}` — the repository, its test directories, and the tooling that seeds local and shared environments.
- `{{DATA_CLASS}}` — what the application handles: contact details, financial records, health data, credentials, user content. This sets the severity.
- `{{RETENTION_DAYS}}` — how long a non-production copy may exist before it must be destroyed.
- `{{APPROVER}}` — required before deleting a shared dataset, because somebody's test will fail and they will notice at the worst time.

## 4. Workflow

1. **Inventory every place test data lives**, because they have different owners and different escape routes:
   - fixture files in the repository (JSON, CSV, SQL dumps, YAML, binary)
   - factory and builder definitions, and their default values
   - seed scripts and migration seeds
   - a shared staging or development database
   - snapshot dumps stored in object storage or on a laptop
   - recorded HTTP fixtures (VCR/cassettes) that contain real request bodies
   - container images or database backups used for local development
   - screenshots, videos, and logs attached to pull requests and CI artifacts

2. **Search for personal and sensitive data with patterns, then read what the patterns flag.** Email addresses, phone numbers in national formats, names paired with addresses, payment card patterns, national ID formats, IP addresses, bearer tokens, cookies, and keys. Do not rely on one regex: run several, then open the matches. A synthetic-looking `test@example.com` is fine; `firstname.lastname@gmail.com` in a fixture is not, and only reading tells you which.

3. **Look in the places a grep misses.** Base64-encoded blobs inside fixtures, JSON embedded as a string in another JSON file, `.sql` dumps where the data is the insert statements, binary fixtures, recorded cassettes with `Authorization` headers, and images. For each, record where it came from and when, because provenance decides whether it is a real copy.

4. **Establish, for each dataset, which of the four states it is in** — and label it, because the remediation differs:

   | State | What it means | Remediation |
   |---|---|---|
   | **Synthetic** | Generated, no real individual | Keep; check it is not *too* clean |
   | **Anonymised** | Derived from real data, identifiers replaced | Verify the replacement is irreversible and re-identification needs are unmet |
   | **Pseudonymised** | Derived from real data, mapping retained | Treat as production data: access control, retention, deletion |
   | **Real copy** | Production data, unchanged | Highest severity: destroy or replace, with evidence |

5. **Check whether "anonymised" is true.** Removing names while keeping date of birth, postcode, and gender is not anonymisation; it is a re-identification exercise. Hash a field and keep the salt in the repository and it is not anonymisation either. Where the data must remain realistic, generate it from distributions rather than transforming real records, or keep a mapping under production controls and treat the dataset as pseudonymised.

6. **Replace real data with factories that produce *awkward* data**, not tidy data. A generator that only emits `"Alice"` and `"Smith"` reproduces none of the bugs the suite exists to find. Require variety: unicode and right-to-left scripts, maximum-length strings, nulls where nullable, timezone offsets and DST boundaries, duplicate names and near-duplicate records, one and many tenants, and at least one record that violates an assumption.

7. **Make isolation a property of the fixture, not of discipline.** Each test creates its own data and cleans up; shared mutable fixtures are the source of both flakiness and cross-contamination. State the boundary: per-test transaction rollback, unique namespace per test, or a fresh schema. If tests share a dataset, that dataset is production-like and needs the controls of one.

8. **Set a policy for shared non-production environments**: what may be loaded (generated only, or pseudonymised under controls), who may query it, how long it survives, and how it is destroyed. A staging database with a real customer copy needs the same access restrictions as production and a deletion date; without both, it is an unmanaged copy.

9. **Close the screenshot and log hole.** Pull requests that demonstrate a fix frequently include a screen with a real name, email, or order. Set the rule (use generated data for demonstrations; redact before attaching), add it to the pull request template, and put the redaction step where the evidence is produced rather than where it is reviewed.

10. **Add a guard and prove it.** A CI step that scans fixtures and cassettes for the patterns in step 2 with an allowlist of known-good generated values (`example.com`, `555-01xx`, sequential fake IDs). Demonstrate it failing on a deliberately planted address. Write `.testdata/TEST_DATA_AUDIT.md` with the inventory, the state per dataset, findings, remediation, policy, and the guard.

## 5. Decision rules and evidence standard

- **A fixture is code and ships to everyone who clones the repository.** Treat committed test data as public.
- **Pseudonymised is not anonymised.** If a mapping exists, it is production data with extra steps.
- **Do not transform real records into "safe" ones unless you can show the transform is irreversible** for the fields that matter.
- **Clean test data hides bugs.** Generate awkward data on purpose.
- **Shared mutable fixtures produce both flakiness and contamination**; prefer per-test isolation.
- **Screenshots and logs leak faster than fixtures**, because no grep finds them.
- **Every non-production copy has a destruction date**, or it is permanent.
- Mark each dataset `verified` (inspected and classified) or `inferred` (reported by someone else).

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Inventory complete | Repository and environment review | Fixtures, factories, seeds, shared DBs, cassettes, attachments listed |
| Pattern scan run | Several patterns | Every match opened and classified, not just counted |
| Embedded data found | Manual inspection | Base64, nested JSON, SQL dumps, binaries examined |
| State per dataset | Table | Synthetic / anonymised / pseudonymised / real copy |
| Anonymisation tested | Reasoning per field | Irreversibility stated for the identifying fields |
| Generators produce variety | Factory code | Unicode, nulls, boundaries, duplicates, multiple tenants |
| Isolation | Test setup | Per-test data creation; no shared mutable state, or documented |
| Shared environment policy | Written | Who may load and query, retention, destruction date |
| Screenshot rule | Template and process | Rule stated where evidence is produced |
| CI guard | Pipeline | Planted address fails the build |

## 7. Failure handling

- **A real copy exists in a shared database** → do not delete it unilaterally. Escalate to `{{APPROVER}}`, replace the tests that depend on it first, then destroy the copy with evidence; record the exposure window.
- **Tests fail when real data is removed** → the tests were asserting on data rather than behaviour. Fix the assertions; a suite that requires a production copy to pass is a suite you cannot run safely.
- **The team cannot generate realistic data** (a proprietary format, a complex graph) → reduce the domain to a small synthetic graph that preserves relationships, and document what is not represented.
- **A cassette contains an auth token** → treat it as a leaked credential (`02-engineering/secrets-rotation/`), rotate it, and scrub the cassette; check whether the recording ran against production.
- **A pull request already contains a screenshot with personal data** → have it removed and the history rewritten if the repository is public (`04-process/git-operations/` P03), and treat the exposure as an incident if the data was a customer's.
- **The guard is too noisy** → tighten to high-confidence patterns and an explicit allowlist; a guard people disable is worse than none.

## 8. Security and authorisation

Inspection is class A. Changing fixtures, factories, and seeds is B. Deleting a copy of production data is **D** and requires `{{APPROVER}}` and a check that nothing depends on it. Never copy production data into a lower environment without an approved, documented, time-limited process; never store credentials in fixtures (`02-engineering/secrets-rotation/`). Generating synthetic data from a real dataset means reading that dataset — do it in an environment with the same access controls.

## 9. Completion criteria

- [ ] Every source of test data inventoried, including cassettes and attached evidence.
- [ ] Patterns scanned and every match classified by reading it.
- [ ] Each dataset labelled synthetic / anonymised / pseudonymised / real copy.
- [ ] Any real copy has a remediation plan and an owner.
- [ ] Generators produce awkward data, not tidy data.
- [ ] Test isolation is structural, not conventional.
- [ ] Shared non-production environments have a policy and a destruction date.
- [ ] Screenshot and log rule written where evidence is produced.
- [ ] CI guard added and demonstrated failing.
- [ ] Audit written with the inventory and the residual risks.

## 10. Deliverables and handover

Artifacts: `.testdata/TEST_DATA_AUDIT.md`, factories or generators, seeding policy, CI guard.

Handover: `04-process/testing-qa/` P04 owns the test-data strategy this prompt implements, and `P05` writes the tests; this prompt removes the data risk from both. `04-process/privacy-requests/` handles the subject-level consequences when a real copy is found, and `PRIV-P04` verifies deletion. `02-engineering/secrets-rotation/` takes any credential discovered. `05-scenarios/environment-parity/` explains why a staging dataset that differs from production hides defects — the two prompts share the argument but not the work.
