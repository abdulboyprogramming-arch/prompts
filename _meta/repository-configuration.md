<!-- not-a-prompt -->

# Repository Configuration — what to set, where, and why

The files in this repository are the content. This page is the metadata around it: the fields GitHub asks for, what to put in each, and the commands that apply them. Everything here is copy-paste ready, and everything here is a decision recorded so it is not re-litigated later.

**Date:** 2026-10-22 · **Status:** ready to apply · **Backlog:** #100 (visibility), publication checklist §4

---

## 1. Identity fields

| Field | Value | Why this, and not something else |
|---|---|---|
| **Repository name** | `prompts` | It is what the thing is. A clever name costs the repository its only free signal: someone searching "engineering prompts" |
| **Display title** | `Engineering Prompt Library` | The name field in the social preview and the page `<title>` is derived from the repository name; set the *About* description to carry the words |
| **Description** | `364 engineering prompts with evidence rules, failure handling, and a definition of done — for humans and coding agents. Audited by a repo, not a vibe.` | 158 characters. Names the count, the differentiator (evidence rules), the audience, and the posture. No "supercharge", no "10x" |
| **Website** | leave empty until there is a hosted index | A dead link is worse than none |
| **Topics** | see below | Each topic is a search surface; ten is the maximum GitHub shows |

**Description, shorter variant** (if the field truncates): `364 engineering procedures for humans and coding agents — evidence rules, failure handling, a defined finish.`

## 2. Topics

GitHub allows up to twenty; it displays the first few. Set these ten, in this order:

```
prompts  prompt-engineering  ai-agents  llm  engineering  code-review
incident-response  software-engineering  developer-tools  playbook
```

Rejected on purpose: `chatgpt`, `claude`, `gpt` (vendor terms date; the library is model-agnostic and says so), `awesome-list` (it is not a list of links, and the label invites low-effort PRs), `templates` (implies fill-in-the-blank, which is the opposite of the evidence rules).

## 3. Social preview

GitHub's preview images are 1280 × 640. There is no image in this repository by design — the library argues against decoration — so the honest options are, in order:

1. **Generate one** from the repository itself: the README's first paragraph, the count, and the phrase *"operational means structurally reviewed, not proven"*. That sentence is the project's actual position, and a preview built from it cannot overclaim.
2. **Skip it.** The default preview renders as a repository card on most surfaces. Leaving it is defensible; a stock photo is not.

If you generate one, the acceptance test is: *does the image make a claim the README would also make?* If not, it is a launch asset rather than a description, and it belongs in a blog post.

## 4. Repository settings

| Setting | Value | Reason |
|---|---|---|
| Visibility | **Public** | The point. Do it after branch protection and the CI billing fix |
| Social preview | as above | — |
| Features → Discussions | **On** | The best place for "is there a prompt for X" without an issue; also gives the routing conversation a home |
| Features → Wiki | Off | Documentation belongs in the repository, versioned with the prompts |
| Features → Projects | Off | One maintainer; a project board is overhead |
| Issues | **On**, with the three templates already in `.github/ISSUE_TEMPLATE/` | — |
| Merge options | **Squash only**, auto-delete head branches | A prompt library wants one commit per change and one branch per idea |
| Require linear history | On | Follows from squash-only |
| Default branch | `main` | — |
| Branch protection on `main` | Require `validate` to pass; no force pushes; no deletions; admins included | The validator is the only thing standing between a careless edit and a broken library |
| Dependabot alerts + security updates | **On** | Nine scripts, no dependencies today — which is exactly when this is cheap to enable |
| Secret scanning + push protection | **On** (public) | The library contains prompts about secrets; someone will paste one |
| CodeQL | **On** for Python | The scripts are the only executable surface |
| Private vulnerability reporting | **On** | Matches `.github/SECURITY.md` |

## 4a. What actually exists on `main` — measured 2026-10-22

A ruleset named **"Protect default branch"** (id `25579218`) is active on the default branch. It is
not the configuration §4 recommends, and it changed what "merge yourself" can mean here.

| Rule | Setting | Consequence for a solo maintainer |
|---|---|---|
| `deletion` | blocks branch deletion | fine |
| `non_fast_forward` | blocks force-push | fine, and matches the intent |
| `required_linear_history` | on | fine — the workflow is squash-only |
| `pull_request` | **1 approving review required**, thread resolution required, squash only | **blocking**: GitHub refuses an approval on your own pull request (`422`), so with one identity and `bypass_actors: []` (`current_user_can_bypass: never`) nothing can be merged |
| `required_status_checks` | `validate` | now satisfiable — run `39846014231` was green |

**Measured effect:** PR #34 was blocked at merge with *"At least 1 approving review is required by
reviewers with write access"*, and `--admin` does not help because no bypass actor is configured.
The ruleset predates the publication, but earlier merges today succeeded, so something about it
became enforceable during the session; the state above is what the API reports now.

**Two ways out, both owner-only:**

1. **Recommended:** Settings → Rules → *Protect default branch* → add **Repository admin** as a
   bypass actor. The protection stays on for everyone else; the single maintainer keeps the ability
   to merge their own reviewed-by-CI pull requests. This is how a one-person repository gets the
   benefit of the rule without being locked out by it.
2. Set *Required approvals* to **0** and rely on `validate` plus linear history. Weaker, but honest
   about the fact that there is no second reviewer to require.

Recording a rule that nobody can satisfy is the same defect class as a check that cannot fail: it
looks like governance and functions as a stop.

## 5. The commands

Run in this order. Each is idempotent.

```bash
# 1. Identity
gh repo edit abdulboyprogramming-arch/prompts \
  --description "364 engineering prompts with evidence rules, failure handling, and a definition of done — for humans and coding agents. Audited by a repo, not a vibe."

gh repo edit abdulboyprogramming-arch/prompts \
  --add-topic prompts --add-topic prompt-engineering --add-topic ai-agents \
  --add-topic llm --add-topic engineering --add-topic code-review \
  --add-topic incident-response --add-topic software-engineering \
  --add-topic developer-tools --add-topic playbook

# 2. Discussions on, wiki off
gh api -X PATCH repos/abdulboyprogramming-arch/prompts \
  -f has_discussions=true -F has_wiki=false

# 3. Squash-only, auto-delete, linear history
gh api -X PATCH repos/abdulboyprogramming-arch/prompts \
  -f allow_merge_commit=false -f allow_rebase_merge=false -f allow_squash_merge=true \
  -f delete_branch_on_merge=true

# 4. Branch protection (after the first green CI run)
gh api -X PUT repos/abdulboyprogramming-arch/prompts/branches/main/protection \
  --input - <<'EOF'
{
  "required_status_checks": {"strict": true, "contexts": ["validate"]},
  "enforce_admins": true,
  "required_pull_request_reviews": null,
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "required_linear_history": true
}
EOF

# 5. Security features (public, or after making public)
gh api -X PUT repos/abdulboyprogramming-arch/prompts/vulnerability-alerts
gh api -X PUT repos/abdulboyprogramming-arch/prompts/automated-security-fixes
gh api -X PATCH repos/abdulboyprogramming-arch/prompts \
  -F security_and_analysis[secret_scanning][status]=enabled \
  -F security_and_analysis[secret_scanning_push_protection][status]=enabled
```

`gh api` field syntax matters: `-f` sends a string, `-F` sends a typed value. Boolean flags need `-F`.

## 6. Sponsorship — the decision, not the button

**Recommendation: do not enable sponsorship, and do not add a `FUNDING.yml`.**

Four reasons, in order of weight:

1. **The work is not funding-shaped yet.** Sponsorship pays for sustained maintenance. This repository has one author, three executed prompts, and a release cadence measured in days. Money would introduce an obligation (responsiveness, a roadmap) that the project cannot honestly meet, and the library's entire posture is that claims should match evidence.
2. **A sponsorship button changes what a reader expects.** "Give me money" on a page that also says *"operational means structurally reviewed, not proven"* invites the reader to ask what they are paying for. The honest answer today is "a well-organised library with self-reviewed prompts", which is a good thing to give away and a bad thing to sell.
3. **It creates a second audience.** Sponsors read updates; contributors read the changelog. One maintainer serving two audiences splits attention away from execution, which is the actual bottleneck (37 of 285).
4. **It is trivially reversible.** Adding `FUNDING.yml` later takes one commit. Leaving it out now costs nothing.

**What to do instead, if someone offers money:** a single line in the README pointing at the backlog's *empirical test harness* item — "the most useful contribution is a run of any prompt against a real repository, written up in `_meta/empirical-evaluation-NN.md`". That converts enthusiasm into the thing that is actually missing.

**When to revisit:** more than one regular contributor, or a first external execution record. At that point sponsorship is a reasonable acknowledgement of maintenance rather than a claim about the product.

## 7. What not to add

| Item | Why not |
|---|---|
| A Discord or Slack | An empty chat is worse than no chat; Discussions covers it until there is volume |
| A "star history" badge | A metric that goes up without the library improving |
| Coverage badges | There are no tests of the prompts, only of the scripts, and a percentage would imply otherwise |
| A "used by" list | Nobody is using it yet in a way that can be cited |
| An LLM-generated logo | The project's argument is that decoration without evidence is the failure mode |

## Related

- [`publication-checklist.md`](publication-checklist.md) — the gates and the order.
- [`../AGENTS.md`](../AGENTS.md) — what an agent may change without asking.
