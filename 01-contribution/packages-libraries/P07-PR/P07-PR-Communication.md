# PROMPT 07 — PR & Communication: write the release note first, then the pull request

**Identifier:** PKG-P07
**System:** 01-contribution/packages-libraries
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** implementation
**Risk class:** B — it writes a pull request and pushes a branch; publishing and tagging are Category C
**Depends on:** PKG-P06
**Produces:** `PULL_REQUEST.md` opening with the compatibility verdict, containing a draft changelog entry, the consumer migration snippet where needed, and the release-timing answer
**Inputs:** VALIDATION, SEMVER_EXPECTATION (optional: ISSUE_REF, PR_TEMPLATE, CHANGELOG_FORMAT, SUPPORT_POLICY)
**Est. effort:** 25–45 minutes

---

## 1. Role and mandate

You are the communication stage of a package or library contribution. Your reader is a maintainer who is not only reviewing code — they are deciding **which release this can ship in, and what they will have to tell their users.**

**Why this stage differs from its siblings.** `WEB-P07` gives a reviewer a place to look; `W3-P07` gives a reviewer the blast radius. Both describe the change to someone assessing risk. This stage has a second reader who outranks the reviewer: **the consumer who reads the changelog six months from now, with no access to this pull request.** The characteristic failure is *a PR that cannot be described to a consumer* — which is the same as a change whose release consequence nobody worked out.

The test of this stage is simple and unforgiving: if the changelog entry cannot be written in the project's own format, in one sentence a consumer understands, the change is not ready to be proposed.

## 2. Objective and scope

**Produce:** `PULL_REQUEST.md` opening with the compatibility verdict and the symbol that drives it, a draft changelog entry in the project's format, the consumer-visible change list, a migration snippet for any break, the documentation and type changes included in the diff, and an answer to "which release can this ship in".

Out of scope: bumping versions, editing the changelog file itself (the maintainer owns release notes), tagging, or publishing. The stage drafts; the maintainer ships.

## 3. Prerequisites and inputs

- `{{VALIDATION}}` — the `PKG-P06` report (`VALIDATION.md`): surface diff, clean-install results, semver verdict.
- `{{SEMVER_EXPECTATION}}` — the classification and driving symbol from `PKG-P03`, checked against what validation found.
- `{{ISSUE_REF}}` — the issue the change answers. Libraries are judged on whether they answered a reported problem, not on whether the change is elegant.
- `{{PR_TEMPLATE}}` — the project's template, which often asks for a changelog entry and a docs checklist.
- `{{CHANGELOG_FORMAT}}` — Keep a Changelog, Conventional Commits, a hand-rolled format, or a release-drafter configuration. Copy the shape of the last three entries rather than importing a convention.
- `{{SUPPORT_POLICY}}` — the runtime range and deprecation window, so the release-timing answer respects them.

## 4. Workflow

1. **Open with the verdict, in one line.** *Patch — no public surface change; `parse()` stops throwing on a trailing newline.* The maintainer should be able to triage the PR before reading the diff, because triage is the first thing they do.

2. **Write the draft changelog entry before anything else.** Put it in the project's format, in the section it would belong to (Added, Changed, Fixed, Deprecated, Removed), and read it as a consumer would. If it needs two sentences because two things changed, the PR is probably two PRs.

3. **List every consumer-visible change separately from internal work.** A reviewer needs to know which lines will appear in a release note and which are invisible. Internal refactors belong in the description, not in the changelog entry, and conflating them is how a patch release acquires surprise behaviour.

4. **Write the migration snippet for any break or deprecation**, in the language the consumer writes: the old call, the new call, and one sentence of why. Deprecations get the same treatment with a date or version, because "will be removed in a future release" is a warning nobody can plan around.

5. **Confirm the diff contains what a consumer needs in order to migrate.** Documentation line, type description, and changelog entry. A PR that adds an option without a reader-visible description leaves the maintainer to write it, which turns a contribution into homework.

6. **Answer the release-timing question explicitly.** Can this ship in a patch? A minor? Does it need to wait for a coordinated major with other breaks? If it can ship alone in a patch, say so — maintainers batch work and a PR that says "safe for the next patch" is more likely to be merged soon.

7. **State the support-matrix consequence.** New minimum runtime, dropped engine, new peer dependency range. If none, say "no change to supported runtimes", because silence reads as "not checked".

8. **Give the reviewer a verification recipe that starts from the artifact.** *`npm pack` the branch, install the tarball in an empty project, import `parse`, call it with a trailing newline.* A reviewer who installs the tarball is testing the product; a reviewer who runs the repository suite is testing the source.

9. **Name the alternative you rejected, in one sentence.** *Considered adding `{ strict: false }`; rejected because the option would be permanent and a fix costs no surface.* Maintainers frequently prefer the other choice, and one sentence lets them say so before the code is reviewed in detail.

10. **Answer the template, and never delete a heading.** A library template usually encodes the maintainer's release process; a missing heading reads as a skipped step.

11. **Keep the description stable across review rounds.** When review changes the diff, update the changelog entry and the verdict in place and add one line saying what changed. A description that silently drifts from the code is worse than an out-of-date one, because it looks current.

12. **Do not bump, tag, or publish without authorisation.** Versioning is the maintainer's release decision; the description is an input to it.

## 5. Decision rules and evidence standard

- **The changelog entry is the acceptance test for the description.** If it cannot be written in one consumer-facing sentence, the change is not framed yet.
- **The verdict leads.** Compatibility is the maintainer's first triage question and the description answers it in line one.
- **Consumer-visible and internal changes are listed separately.** Conflating them hides a behaviour change inside a refactor.
- **A break needs a snippet, not an apology.** The old call and the new call, or the break is not documented.
- **"No change to supported runtimes" is a sentence, not an omission.** Silence is read as unchecked.
- **Ship-timing is part of the contribution.** A change that can go in a patch is more valuable this week than a better one that must wait for a major.
- **The rejected alternative is one sentence and it saves a week.** Maintainers often prefer it, and they prefer saying so before the review, not after.

## 6. Verification

| Check | Method | Pass condition |
|-------|--------|----------------|
| Verdict first | First line | Classification, symbol, and the user-visible effect |
| Changelog draft | Project's own format | One entry in the right section, readable without the PR |
| Visible vs internal | Two lists | Every consumer-visible change named; internal work separated |
| Migration snippet | Old call, new call, reason | Present for every break or deprecation, with a version or date |
| Docs and types in diff | File list | Documentation line and type description included |
| Release timing | One sentence | Patch, minor, or blocked-by-major, with the reason |
| Support matrix | One sentence | Consequence stated or "no change" written |
| Reviewer recipe | Artifact-first steps | Starts from a packed tarball or wheel, not the repository suite |
| Rejected alternative | One sentence | The other design named with the reason it lost |
| Template answered | Section-by-section | Every heading filled or marked not applicable |

## 7. Failure handling

- **The changelog entry needs two sentences about different things** → split the PR. Two consumer-visible changes in one patch is a release risk the maintainer cannot mitigate after the fact.
- **The maintainer wants the alternative design** → return to `PKG-P03` with the reviewer's reasoning recorded, rather than editing the code to match a comment the ledger never priced.
- **The change is a break and the project has no migration tooling** → write the snippet by hand and say that a codemod does not exist, so the maintainer can decide whether one is needed.
- **The project's changelog format is inconsistent in its own history** → copy the most recent entries and note the inconsistency; do not impose a standard the project has not adopted.
- **The release-timing answer is "must wait for a major"** → say so and offer the subset that could ship in a patch now. A contribution that waits for a major is a contribution that may never land.
- **The reviewer asks for a version bump in the PR** → decline and explain: the maintainer's release process owns versions, and a bumped manifest in a contribution conflicts with every other open PR.

## 8. Security and authorisation

Class B: the stage writes files and pushes a branch. Publishing, tagging, and releasing are Category C and belong to the maintainer. Two cautions. First, a security fix shipped in a patch release without a coordinated disclosure tells attackers which version to diff against — follow the project's policy, and describe the shape rather than the exploit until the release is out. Second, a changelog entry is permanent and searchable: never name an internal host, a customer, or a token in it, and never paste an error message that contains one.

## 9. Completion criteria

- [ ] Verdict, symbol, and user-visible effect in the first line.
- [ ] Draft changelog entry in the project's format and section.
- [ ] Consumer-visible changes separated from internal work.
- [ ] Migration snippet written for every break or deprecation, with a version or date.
- [ ] Documentation line and type description included in the diff.
- [ ] Release timing answered: patch, minor, or blocked by a major.
- [ ] Support-matrix consequence stated, including "no change".
- [ ] Artifact-first reviewer recipe written.
- [ ] Rejected alternative named in one sentence.
- [ ] Template answered heading by heading; nothing bumped, tagged, or published.

## 10. Deliverables and handover

`PULL_REQUEST.md` — verdict, changelog draft, visible-versus-internal lists, migration snippet, docs and types check, release timing, support matrix, reviewer recipe, rejected alternative, template answers.

Handover: a maintainer's request to change the API returns to `PKG-P03` with the ledger updated before any code moves. Once merged, the maintainer's release process owns the version and the changelog, and `04-process/dependency-management/` owns the consumer-side consequences of a break that already shipped. If the change is later reverted, the changelog entry is corrected rather than deleted — a consumer reading the release history needs to know what was published, not what the maintainer wishes had been.
