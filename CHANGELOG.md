# Changelog

All notable changes to this prompt library. Versions refer to the library as a whole; individual prompts carry their own versions.

## [2.22.0] — 2026-10-21

Six changes that were developed together and ship as one release: one measurement closed, one index added, two chat prompts, one differentiation pass, one worked example, and one script that makes the gate list authoritative.

### Changed — the prose lint is now a gate, at zero

The corpus was burned down from **171 findings to 0**. Every `etc.`, `as appropriate`, `where possible`, `properly`, and `if needed` that handed a decision back to the reader now names the items or the condition: `(package.json, pyproject.toml, go.mod, Cargo.toml, pom.xml, build.gradle)` instead of `(…, etc.)`, and `start local services on non-public ports when a test requires them` instead of `if needed`. The 24 sentences over 55 words were split at their clause boundaries rather than trimmed of meaning.

Because the baseline now records `0`, the ratchet is a hard gate: a new vague qualifier fails CI. That was the point of writing the lint as a ratchet in 2.20.0 — it made the debt visible and countable, and this release pays it.

### New — `TASKS.md`: the library indexed by the problem

`GALLERY.md` is organised the way the repository is: by area. That is right for maintainers and wrong for a visitor, who arrives with a situation and does not know that "flaky test" lives under `05-scenarios`. **`TASKS.md` inverts the index**: 21 tasks, from *something is broken right now* to *I only have a chat window*, each listing the runnable prompts in it, where they live, and what to paste first.

It carries one enforced property, and that is why it is generated rather than written:

> **Every prompt in the library is reachable from at least one task.**

A prompt added without a home fails the build with its path printed. That check found thirteen prompts with no home the first time it ran — the standalone audits (`time-correctness`, `tenancy-audit`, `access-review`, `secrets-rotation`) and the whole `observability-reliability` system, among others. `skeleton` prompts are counted per task instead of listed, so a task with four runnable prompts and eleven outlines says exactly that.

### New — two chat prompts for the problem after the first success

`00-core/conversational/` grows from four prompts to six, both `operational`.

- **`CHAT-SELECT`** answers "which prompt do I need" inside a window that cannot open the library. It refuses to dress the guess up: a route is `observed` when `TASKS.md` is pasted and `inferred` when it is not, and the card carries the one fact that would overturn the choice. One prompt, not a menu.
- **`CHAT-HANDOFF`** carries a long engagement between conversations. The design detail worth keeping: **a summary is the wrong artifact**, because it keeps the conclusions and drops the disproved hypotheses — so the next chat proposes the same dead end with fresh confidence. The packet keeps the eliminations, labels every fact, states what was redacted, and requires the receiving conversation to restate the constraints and eliminations before it is allowed to work.

### Changed — `P06 Validation` differentiated across the three contribution variants (#107)

`01-contribution` holds three systems whose stages were the same file with different nouns; `VARIANTS.md` (2.20.0) decided to keep all three but ruled that **any overlapping stage must state what is different about it in its domain**, and blocked promotion until it did. This release does that for the one stage where the difference is sharpest, and promotes all three to `operational`:

| Variant | Validation means | The evidence that convinces a maintainer |
|---|---|---|
| `WEB-P06` | It works in engines, viewports, and input methods the author did not use | A screenshot at a named browser and width, or a passing cross-browser job |
| `W3-P06` | The invariants hold when someone tries to break them | A violating case per invariant, an access-control matrix, a fork run pinned to a block |
| `PKG-P06` | The published interface did not break a consumer's build | A surface diff against the released version, and an install of the built artifact in a clean environment |

Each names the characteristic failure it exists to catch: *works in the author's browser*, *works in the test suite and drains the contract*, *works here and breaks a consumer's build*.

**The measurement did not cooperate, and that is recorded rather than smoothed over.** Pairwise vocabulary overlap across the three files went from 0.20–0.28 to 0.22–0.27 — one pair rose. The reason is in `VARIANTS.md`: the `P06` outlines were two paragraphs each, so they never contributed the 0.63–0.68 similarity at the top of that record, which comes from the longer `P03` and `P07` stages; and rewriting a short outline into a developed prompt multiplies the denominator. The claim for this pass is the one a reviewer can check by reading, not a number.

### Changed — `P03 Selection` differentiated across the three contribution variants (#107, pass 2)

Pass 1 left the duplicate metric unmoved and said why. Pass 2 was designed to test that explanation, and it did: **if three variants keep the standard ten sections and differ only in what they ask inside them, combined similarity cannot fall.** So this pass replaced the procedure rather than the adjectives, and each variant now selects with an instrument the other two do not have:

| Variant | How work is chosen | What disqualifies a candidate |
|---|---|---|
| `WEB-P03` | A **claim register**: the user-visible claim, the artifact that proves it, the surface it touches, and who owns the decision — ranked by proof strength, then by review cost | No owner for a visible change, no assertable claim, no reference |
| `W3-P03` | A **reversibility tier** from 0 to 3 by asking who can undo the change if it is wrong, with tiers 2 and 3 gated behind recorded maintainer approval *before* code exists | A tier 2 or 3 change with no approval; an invariant that cannot be written |
| `PKG-P03` | A **surface cost ledger**: symbols added, behaviour changed silently, dependencies inherited, and the support burden the maintainer carries indefinitely | A change that adds a promise the maintainer must keep |

Each names the failure it exists to catch: *picks a visible redesign and hands the maintainer an unauthorised design decision*; *submits a change to a value path described as a small fix*; *adds a convenience option the maintainer supports forever*.

**The measurement moved this time, and the reason is the finding.** Combined similarity fell on all three pairs, from 0.54–0.68 to 0.36–0.38, with shingle, vocabulary, and structure all falling together. `P06` had risen from 0.26–0.28 to 0.31–0.36 for a mechanical reason: an outline has a handful of headings, a developed prompt has the ten the standard requires, and the metric multiplies structure by vocabulary.

The pass also corrected a measurement error from pass 1. Its vocabulary figures had been computed with Jaccard over word sets while the pair table above them used containment, so "barely moved" was reached by comparing two different things. Recomputed on both sides with `find_overlaps.py`'s own functions, `P06`'s vocabulary fell from 0.44–0.47 to 0.37–0.43 and its combined score rose. The conclusion survived; the arithmetic did not, and `01-contribution/VARIANTS.md` now carries the correction rather than a quietly amended table.

### Changed — `P02 Discovery` and `P07 PR` differentiated (#107, passes 3 and 4)

Two more passes, and the metric that pass 2 moved kept moving:

| Stage | What the three variants now do differently | Combined, before → after |
|---|---|---|
| `P02 Discovery` | `WEB-P02` walks the running app at three widths with a keyboard; `W3-P02` maps the trust boundary before looking for missing guards; `PKG-P02` searches **consumer code** for wrappers, copies, and pinned old majors | 0.56–0.65 → **0.29–0.32** |
| `P07 PR` | `WEB-P07` writes a viewing instruction — recipe, labelled media, look-here list; `W3-P07` writes a risk disclosure that opens with four facts; `PKG-P07` writes the release note first, because the changelog entry is the acceptance test for the description | 0.63–0.68 → **0.32–0.35** |

The interesting result is `P02`. The three outlines were not merely similar — they used the same word for three different search spaces, and the only way to differentiate them was to notice that *discovery in a library happens in someone else's repository*. A candidate without a witness is now a hypothesis, kept out of the ranked list, in the same way a web candidate without an observation and a web3 candidate without a boundary are.

`P07` differentiated by **reader**, not by content: a web reviewer checks behaviour, a protocol reviewer prices risk, a library maintainer decides a release. Each description now leads with what its reader decides first.

Every rewritten pair sits at 0.29–0.38 combined, from 0.26–0.68. `P04 Planning` and `P05 Implementation` remain; `P01` and `P08` are deliberately untouched, because planning and implementing a change in a repository genuinely are the same job in any language, and differentiating them would produce adjectives rather than instruments.

### Changed — `P04 Planning` and `P05 Implementation` complete the differentiation (#107, passes 5–6)

The last two passes finish #107: six stages, eighteen files, every variant pair now at 0.29–0.38 combined from a starting 0.26–0.68.

| Stage | `web/general` | `web3/general` | `packages-libraries` | Combined |
|---|---|---|---|---|
| `P05 Implementation` | Build every state the plan named; native elements before ARIA before JavaScript | Add no surface, append-only storage, state settled before external calls | Every export is a promise: no accidental exports, entry-point tests, packaging checked | 0.40–0.61 → **0.29–0.33** |
| `P04 Planning` | The state × breakpoint matrix with a test layer per behaviour | The deployment sequence and storage decision, written before the diff | The allowed surface delta and the release choreography | 0.19–0.51 → **0.32–0.33** |

Two decisions are recorded rather than made by omission. `P01` and `P08` stay undifferentiated: their similarity was already 0.15–0.46 and their content genuinely is the same job in any language, so a pass would have produced adjectives. And the systems stay `mixed` rather than `operational`, because a system whose first and last stages are outlines is not ready to run unattended whatever its middle says.

What remains is execution. Eighteen stages that have never been run are eighteen hypotheses about what a maintainer will accept — `WEB-P02`/`WEB-P07` and `PKG-P02`/`PKG-P07` are the cheapest to test, because their output can be judged against a public issue tracker.

### New — composition is checked, not assumed

The validator has always asked whether each prompt is well formed **on its own**. Nothing asked whether two prompts in a sequence agree on the artifact between them, which is the property that makes this a library of systems rather than 364 separate documents.

`scripts/check_prompt_contract.py` now does, and it treats the things that break a sequence as errors: a `Depends on:` that names no prompt (checked against tokens rather than against the identifiers that happen to exist, or the check could never fail), two stages in one system claiming to produce the same file unless one says *updates* or is an orchestrator, and a cycle in a system's dependency graph. Fourteen fixtures in `scripts/test_contract.py` pin each rule, including the parenthetical case — `none (companion: GEN-P02)` is not a dependency.

It found three real defects on the first run, all in `02-engineering/from-scratch`: `FS-P02` claimed to produce `VISION.md`, which `FS-P01` owns; `FS-P07` claimed `README.md`, which `FS-P04` scaffolds. Both now say *updates*, which is what they do.

**The measured part matters more than the gate.** Of 239 dependency links between stages, **116 (49%) named a concept where the artifact has a filename** — *"the rollout evidence"* instead of `.flags/ROLLOUT_LOG.md`. Each of those prompts is individually correct, and an agent running the sequence has to invent the mapping. Twenty-six operational prompts now name the upstream file in their prerequisites; the count is **82 (34%)**, and every remaining link is a skeleton without a prerequisites section, so the rest of the burndown is part of promoting them. `_meta/conformance-report.md` is generated, checked for staleness in CI, and lists every remaining link by system.

### New — community files are checked, and one of them was unlinked

`.github/CODE_OF_CONDUCT.md` existed and nothing pointed at it. A conduct policy that no document links is a file, not a policy — GitHub shows it in its own UI, and a contributor reading the repository never learns it applies. The same was true of `.github/SECURITY.md`.

`check_community` now requires `LICENSE`, `CONTRIBUTING.md`, the code of conduct and the security policy to exist **and** to be reachable from `README.md` and `CONTRIBUTING.md`. Four fixtures (validator self-tests now 18/18). `CONTRIBUTING.md` gained a *Community and conduct* section, and `README.md`'s contributing section was rewritten: it had been telling readers that `validate_library.py` was the gate and that 165 of 235 prompts were skeletons, both of which stopped being true several releases ago.

### New — `_meta/release-readiness.md` and `_meta/repository-configuration.md`

The first answers "what still blocks a release" in one page: what is tested and at which level, the three kinds of check the repository performs, five external blockers in the order they must be cleared, four things that are deliberately *not* blockers, and the four things that would make the library trustable rather than merely clean. Its one-line status is the sentence to use in any announcement.

The second records the settings GitHub asks for — description, ten topics, merge policy, security features, social preview — with the commands that apply them and the reason for each. It also records the **sponsorship decision**: not now, with four reasons, and the trigger for revisiting (`repository-configuration.md` §6).

### New — a worked multi-agent run, and the three rules it forced (#109)

`WF-MULTIAGENT` said "freeze the interfaces first" and "audit for cross-agent interference". Neither was demonstrated, so both read as formalities. [`07-workflows/multi-agent-worked-example.md`](07-workflows/multi-agent-worked-example.md) is a two-agent notifications feature where the event schema was frozen before either agent started; Agent A then added a **required** `template_id` on day 2 and reported it as *done*, not *deviated*.

Both per-agent suites stayed green, because each built its fixtures from its own copy of the schema, and the seam broke silently: the worker rendered an empty template while the job reported success. The recovery **versioned** the interface (v2 with `template_id` optional, `template` retained) rather than reverting it, because a consumer already depended on v1.

Three rules followed, each traceable to a row of the audit that should have run on day 2:

1. **The frozen interface is a fixture, not a paragraph** — a serialised example in the repository, which the agents' tests read.
2. **A required field is an interface change**, reported as `deviated`, never as `done`.
3. **The seam check belongs to the orchestrator and runs before integration**, asserting on the boundary outcome rather than on the handshake.

`WF-MULTIAGENT` v1.1.0 carries all three, with completion criteria and a failure-handling entry for the case where every unit suite is green and the integration fails.

### New — `scripts/check_all.py`, so the gate list has one owner

There were nine gates and three lists of them: the CI workflow, `CONTRIBUTING.md`, and the publication checklist. A contributor could not tell which was authoritative, and a gate added to one list was missing from the others. `scripts/check_all.py` is now the single source — CI runs that script and nothing else, and a local `python3 scripts/check_all.py` is the same run the pull request will get. `--fix` regenerates in dependency order (catalog, gallery, task index, evidence), because running them alphabetically produces a stale file that the next gate then fails.

### New — the counts in prose are checked too

Every generated artefact is guarded: CI fails if the catalog, gallery, task index, or evidence report is stale. The numbers a reader meets **before** those artefacts were not. Promoting prompts in this release moved the operational count from 213 to 228, and four hand-written sentences had to be edited each time — `PROJECT-STATUS.md`, the publication checklist's gate table and limitations section, and the quickstart. That is four chances to miss one, per release, forever.

`scripts/validate_library.py` now compares the maturity lines in `PROJECT-STATUS.md` and `_meta/publication-checklist.md` against the tree and fails with both numbers: *"says 213 operational / 5 draft / 146 skeleton but the tree has 228 / 5 / 131"*. Four fixtures pin it (14/14), including the case where a document has no maturity line at all and must not be treated as a failure.

### New — the README's count table is now checked

The per-system table in `README.md` drifted twice in one release: `03-domains/ai-agentic/` claimed 5 prompts while holding 7, and `07-workflows/` claimed 12 while holding 13. Neither is a lie anyone types — both are what happens when a prompt is added and the table is not revisited. Since that table is the first quantitative claim a reader meets, `scripts/validate_library.py` now compares every row against the tree and fails with the exact row to fix. Four fixtures in `test_validator.py` (10/10) pin the rule, including the case where two rows point at different directories.

### Changed — `CHAT-SELECT` v1.1.0, after a routing run with a scoring key

The third empirical run, and the first with **ground truth outside the prompt**: six situations were routed following `CHAT-SELECT` as written, then each routing card was scored against the generated `TASKS.md`, where "which task owns this prompt" is a fact in the repository rather than the evaluator's opinion. Four of six cards named the prompt the index assigns to the situation's task. Write-up: [`_meta/empirical-evaluation-03.md`](_meta/empirical-evaluation-03.md).

The two misses were worth more than the hits:

| Defect | What it looks like in a real conversation | Fix in 1.1.0 |
|---|---|---|
| The prompt equated the user's symptom with the index's heading | "Our nightly export stopped producing files" is *broken now* to the user and *running the work* to the index. A model that silently translates one into the other returns a correct route the user does not recognise | Classify the sentence, then name the index's heading for the same prompt; when they differ, state both and say which to run first |
| The falsifier was only asked to separate *tasks* | Tasks are coarse; the realistic ambiguity is two prompts inside one task (`GOV-P01` control map versus `STD-01` standards conformance for one security questionnaire). Every card in the run had a falsifier, and four of them separated the wrong pair | The falsifier must separate the two candidate prompts, and the verification row now checks that it does |

**One defect was in the index, not the prompt.** A job that stops firing is the most common form of "something is broken right now", and `JOBS-01` was reachable only from *running the work*. Background jobs are now a home of both tasks, and `JOBS-01` carries an explicit `Gallery` line because both rows had been rendering the clipped fragment "A per-job safety assessment (idempotent?". Two cases in `test_task_index.py` pin multi-home routing (17/17), and the generator comment now says that overlapping homes are deliberate and must be true of both descriptions.

### Also

- `QUICKSTART.md` Path 0 gained both chat prompts and a third rule: a route without the index is `inferred`, never `verified`. Path 0 also moved to the top of the file — the reader with the fewest tools was being served last.
- `QUICKSTART.md` said "355 prompts" and "four situations". It says 364 and six, which is what the file contains. A count that drifts in the front door is the first lie a library tells.
- `scripts/test_task_index.py` (17 cases) pins the index's matching rules, the unrouted-prompt report, multi-home routing, the skeleton counting, and the word-boundary clipping.

### Result

**458 Markdown files, 364 prompts: 228 operational, 5 draft, 131 skeleton.** Validator 0 errors / 0 warnings; tooling self-tests 18/18, 13/13, 12/12, 17/17, 14/14; prose lint 0 findings at baseline 0; catalog, gallery, task index, evidence report and conformance report current, verified by one command. The file count is the validator's scan, not `find`'s — they differ by tooling and archive files, and the scanned number is the one that matches the other claims here.

Coverage: **143 rows, unchanged** — this release improves the instruments, not the coverage. Executed: **3 of 228 operational prompts (1.3%)** — `DBG-01`, `CHAT-DEBUG`, and `CHAT-SELECT` from this release. The eighteen contribution stages promoted here and `CHAT-HANDOFF` have not been run, and the review log says so for each.

## [2.21.1] — 2026-10-21

### Changed — `CHAT-DEBUG` v1.1.0, after being run

The first conversational prompt in the library has now been executed, and it found three defects. The fixture: a nightly sync failing with `sqlite3.OperationalError: database is locked` at `db.commit()`, where the pasted function is **correct** and a second, uncommitted connection in code the user never sent holds the lock. The write-up is [`_meta/empirical-evaluation-02.md`](_meta/empirical-evaluation-02.md); it is a tabletop by the prompt's author, and the record says so.

| Defect | What it cost | Fix in 1.1.0 |
|---|---|---|
| The prompt assumed the bug was in the paste | It would have critiqued an innocent loop and found a plausible, wrong cause | Step 2b: establish what else touches the same lock, port, file, or pool, and prefer the hypothesis that explains the failure without a defect in the visible lines |
| The ledger could not hold a finding outside the paste | A correct answer stayed `OPEN` and looked unresolved | `CONTRADICTION:` and `OUT OF SCOPE (needs access):` lines |
| No rule for a user claim that conflicts with evidence | "We bumped nothing" would have been accepted while a version differed | A contradiction is evidence — record both and test the difference |

One thing the prompt still gets wrong is recorded rather than fixed: its stop rule counts experiments, but the real stopping condition in this run was a **scope change** — the search moved outside what the user can paste. Two completion criteria were added (shared resource identified, contradictions recorded), plus the failure-handling answer that matters most in a chat window: *"this function is fine, and something else holds the lock"* is a valid conclusion.

### Result

**458 Markdown files, 362 prompts: 208 operational, 5 draft, 149 skeleton.** Executed: **2 of 208 operational prompts (1.0%)** — `DBG-01` and now `CHAT-DEBUG`. Validator 0 errors / 0 warnings; tooling self-tests 6/6, 13/13, 12/12; prose ratchet clean at baseline 171; catalog, gallery and evidence report regenerated.

The number that moved is the honest one: the library's demonstrated share doubled from 0.5% to 1.0%. Two data points are not a trend, and the other three conversational prompts remain unexecuted.

## [2.21.0] — 2026-10-20

### New — conversational mode: the library in a chat window

The direct answer to a fair question: **do these prompts have a chatbot version?** They did not. All 358 assumed an agent that can read a repository, run commands, and observe results, and nothing in the library said what survives when those are removed.

The answer is a mechanism rather than a disclaimer. **`CHAT-MODE` adapts any prompt** in the library for a conversation, and it starts by stating the capability delta:

| Capability | Agent | Chat window | Consequence |
|---|---|---|---|
| Discovery | Reads files, config, history | Nothing | The model must ask; the user must paste |
| Execution | Runs tests and commands | Nothing | The user runs; the model interprets |
| Verification | Observes the outcome | Nothing | Claims are labelled, never verified |

**The evidence rule is the load-bearing part.** In chat, `verified` is reserved for the case where the user pasted the command *and* its output *and* they match the claim. Everything else is `observed`, `reported`, `inferred`, or `unknown`. Without that rule, a chat run silently inherits the authority of an agent run — and a fluent answer about an unseen repository is the most dangerous output this library can produce.

**Three chat-native prompts**, because these are the tasks people actually do in a chat window and they need different wording:

- **`CHAT-REVIEW`** — a bounded review with severities, a **not-assessed list** (tests, callers, config, data, dependencies), and a verdict scoped to the excerpt. "Looks good to merge" is prohibited; the smallest fix and the path to a real review are the deliverables.
- **`CHAT-DEBUG`** — one discriminating experiment per turn, never three, with an evidence ledger (confident / reported / eliminated / open / next) that survives context truncation. Distinguishes symptom gone from cause fixed, and proves causes by prediction.
- **`CHAT-DESIGN`** — an ADR with two to four real options including doing nothing, constraints applied as eliminations rather than invented weights, three ways the leading option fails in a year, reversibility, and the condition that would reopen the decision.

### Also

- `QUICKSTART.md` gained **Path 0 — you only have a chat window**, so the chat route is visible from the front door rather than buried in `00-core`.
- `00-core/README.md` now lists the conversational family as executable prompts alongside `GEN-P01`/`GEN-P02`.

### Result

**457 Markdown files, 362 prompts: 208 operational, 5 draft, 149 skeleton.** Validator 0 errors / 0 warnings; tooling self-tests 6/6, 13/13, 12/12; prose ratchet clean at baseline 171; catalog, gallery and evidence report current.

Coverage: **143 dimension rows, 116 adequate / 27 partial / 0 missing**, with conversational use assessed for the first time.

## [2.20.0] — 2026-10-20

### New — usable by a person, and measurable by the repository

Four artifacts and one decision. The theme is the gap between a library that *contains* the right prompts and one that a person can *start using*, and the gap between a claim that gates work and a demonstration that they do.

**`QUICKSTART.md` — five paths from symptom to ordered prompts**
355 prompts is an archive, not a starting point. Five situations — production is broken, you inherited something, you are about to ship, someone wants proof, you are building new — each with the exact prompts in order, what you should be holding after each step, and the shortest defensible version if you only have an hour. It opens with what the library cannot do, because a reader who starts there is harder to mislead.

**`METER-01` — Usage Metering and Entitlements** (`05-scenarios/usage-metering/`)
The quantity you bill, which nothing covered: `payments` moves money, `cost-engineering` optimises spend, and the number on the invoice belonged to nobody. Billable unit defined with its exclusions; one metering point with its blind spot named; immutable idempotent events where corrections are new events; fail-open versus fail-closed chosen *and logged*; the period boundary rules where disputes live; **enforcement separated from accounting**, so an access-control bug cannot become a billing incident; monthly reconciliation against an independent source; and dispute reconstruction from stored events alone.

**`TESTDATA-01` — Test Data** (`05-scenarios/test-data/`)
The least-governed copy of production data is the one that ships with the repository. Inventory including cassettes, base64 blobs, and screenshots attached to pull requests; four states — synthetic, anonymised, pseudonymised, real copy — with different remediation each; a test that "anonymised" is actually irreversible; generators that emit awkward data deliberately, because tidy test data is how a suite stays green while production breaks; and a CI guard demonstrated failing on a planted address.

**`WF-FAILURE` — Failure Examples** (`07-workflows/failure-examples.md`)
Workflows define gates and failure routing; nothing showed them firing. Four scenarios: a gate that refuses *after* work was done, a stage blocked by an upstream artifact, an agent claim refuted by verification (the suite passed with 84 tests, down from 87), and a mitigation that made an incident worse. Each names the wrong response, because that is what readers do by default.

### Library capability

- **`scripts/lint_prose.py`** finds what the structural validator structurally cannot: unactionable qualifiers (`as appropriate`, `if necessary`, `etc.`), empty intensifiers with no concrete instruction in the sentence, and run-on sentences. Adopted as a **ratchet**: CI fails only when findings exceed a recorded baseline, so the corpus can improve without a big-bang rewrite. Baseline: **171 findings across 112 files**, 68 of them `etc.` concentrated in the 16-stage open-source agent. Twelve fixtures, including the false positives that would make it unusable.
- **`01-contribution/VARIANTS.md`** records the decision the new duplicate metric demanded. The three contribution variants score 0.63–0.68 combined — the highest in the library — because they differ mainly in nouns. They are kept, with a rule: any overlapping stage must state its domain difference or be deleted, and promotion stays blocked until it does. Backlog #107 orders the work one stage across all three variants rather than one system at a time.

### Result

**452 Markdown files, 358 prompts: 204 operational, 5 draft, 149 skeleton.** Validator 0 errors / 0 warnings; tooling self-tests 6/6 (validator), 13/13 (overlaps), 12/12 (prose lint); catalog, gallery and evidence report current; duplicate gates pass on both metrics.

Coverage: **142 dimension rows, 115 adequate / 27 partial / 0 missing**. Backlog #107–#110 added; #100 (decided), #101, #103, #105, #106 closed.

## [2.19.0] — 2026-10-20

### New — the estate, and the library measuring itself

Four prompts and three pieces of library infrastructure. The theme is the parts of engineering that are invisible until they fail: the differences between environments, the resource that runs out, the supplier you depend on, and the traffic that is not a customer.

**`ENVPARITY-01` — Environment Parity** (`05-scenarios/environment-parity/`)
Why it works locally and not in staging. Nine layers ranked by how often each is the cause; configuration diffed mechanically **including missing keys**, because an absent variable means a code default and the default is where the surprise lives; data compared by shape and volume; service gaps enumerated (a queue with no consumer looks like success); cause proven by a single-variable experiment rather than described; a config contract with a CI parity check that compares keys, never secret values.

**`CAPACITY-01` — Capacity Planning** (`05-scenarios/capacity-planning/`)
What runs out first and when. Every finite resource — including connection pools, sequence headroom, vendor quotas **with their reset windows**, and certificates, which are capacity with a date and no growth. Peak rather than average; date-to-ceiling *and* date-to-headroom, with the earliest date named as the bottleneck; specific failure behaviour per resource; the autoscaler's cooldown and maximum interrogated, because a maximum is a ceiling; four explicit plans (scale / shed / eliminate / accept).

**`VENDOR-01` — Vendor Due Diligence** (`05-scenarios/vendor-due-diligence/`)
Assessing a supplier before the dependency exists. Dependency class sets the depth; "claimed by vendor" is a third evidence category, weaker than verified; reliability read from incident history rather than an uptime figure; the SLA compared against your own promise; lock-in quantified in switching days; and an exit plan written **before** adoption, when it is leverage rather than negotiation.

**`ABUSE-01` — Abuse Prevention** (`05-scenarios/abuse-prevention/`)
When a working endpoint is used for something else. Abuse economics first; the limiting dimension chosen per abuse type — credential stuffing limited **per account** rather than per IP, scraping limited by **coverage** rather than rate, expensive calls limited by **cost units** rather than call counts; uniform responses before rate limits, because removing the signal removes the incentive; a four-stage rollout with a measured false-positive budget; an exemption path for server traffic that cannot solve a CAPTCHA, and an appeal path tested once.

### Library capability

- **`scripts/find_overlaps.py` now reports four signals** — shingle containment, vocabulary containment, structure similarity, and their product — because a shingle-only detector cannot see a reworded clone. CI gates shingle at 0.55 and combined at 0.75; `scripts/test_overlaps.py` pins **13 cases**, including a clone that defeats the shingle metric entirely. The module states its own limit: all four signals are lexical, so a paraphrase in different vocabulary remains a human judgement.
- **`_meta/evidence-levels.md` is now generated** from `_meta/evidence.json` by `scripts/evidence_report.py`, and CI fails if it is stale. It answers the question the maturity labels cannot: of **201** operational prompts, **1** has a recorded execution — **0.5%**. Every previous release quoted the operational count as a quality signal; this release makes the difference between *structurally reviewed* and *demonstrated* a generated number instead of a sentence.
- **`00-core/inputs/RUN-SHEET-EXAMPLE.md`** shows one filled sheet across two systems and six stages, with the artifact chain and a recorded amendment — because "prompts compose" is a claim, and a claim needs an example.

### Result

447 Markdown files, **355 prompts: 201 operational, 5 draft, 149 skeleton**. Validator 0 errors / 0 warnings; `test_validator.py` 6/6; `test_overlaps.py` 13/13; gallery and catalog current; duplicate gate passes on both metrics (highest shingle 0.18, highest combined 0.68).

Coverage: **141 dimension rows, 114 adequate / 27 partial / 0 missing** (was 110/29/0). Backlog #100–#106 added; #94, #96, #98, #99, #102 closed.

## [2.18.0] — 2026-10-20

### New — the compliance layer, the automation layer, and what a second pass found

Fifteen prompts answering three questions directly: *does the library cover licences, standards, and compliance obligations?* (it did not), *does it cover automating a described task?* (it did not), and *what else is missing once you look for it?* (nine things).

**`LIC-01` — Licence Compliance** (`04-process/licence-compliance/`)
Distribution perimeter first, because every judgement depends on it. Obligation families rather than licence labels; the outbound/inbound compatibility direction people forget; notices generated from the resolved graph with versions; a disposition with an owner and an expiry for every copyleft finding; a CI gate that fails on an unapproved licence. Legal conclusions are routed, never performed.

**`STD-01` — Standards Conformance** (`04-process/standards-conformance/`)
Assess one *named* standard with a version against one project. The distinction the prompt enforces: **claimed → practised → evidenced → enforced**, and only the last two count. Periodic controls are checked by *last occurrence date*, not by policy text. `unknown` rows are preserved rather than rounded up.

**`WF-COMPLY` — Compliance Readiness** (`07-workflows/compliance-readiness.md`)
Entry conditions (standard, scope, owner, deadline), four gates, and the evidence pack a questionnaire or an auditor actually consumes. Ordering rule: capture evidence for practices that already exist before engineering new controls — days instead of weeks.

**`AUTO-01` — Automating a Described Task** (`05-scenarios/automation/`)
Four step classes (deterministic / fragile / judgement / blocked), idempotency proven by running it twice, an input-shape guard against the silent no-op that causes most real incidents, outcome verification rather than exit codes, and four recorded proofs before the schedule is switched on.

**`SECRET-CLIENT-01` — Client-Side Secrets** (`05-scenarios/client-secrets/`)
Scan the *built artifact*, not the source: build-time inlining is invisible in source and absolute in the artifact. Framework mechanisms enumerated (`NEXT_PUBLIC_*`, `VITE_*`, `EXPO_PUBLIC_*`, `Info.plist`, `--dart-define`). Severity equals capability, not the label "API key". Revocation before removal, because published artifacts are archived.

**`SUPPLY-01` — Supply Chain** (`05-scenarios/supply-chain/`)
Can you prove the artifact you deployed is the artifact you built? Chain with evidence per link, install-time execution as the blind spot scanners do not see, dependency confusion as a naming problem, digest pinning over tags, provenance verified once, and an SBOM queried before it is needed.

**`RESIDENCY-01` — Data Residency** (`05-scenarios/data-residency/`)
Six location kinds: storage, replicas, processing, observability, support access, third parties. Configuration is evidence; a wiki page is not. Client-side SDK flows count as transfers. Enforcement proven by blocking a deliberate violation.

**`SUNSET-01` — Feature Sunset** (`05-scenarios/feature-sunset/`)
Removing one feature rather than a system: usage by account, workflow, recency, and concentration; the telemetry blind spots (machine clients, scheduled jobs, support tooling); a reversible sequence that names the last reversible point; and the data decision as part of the sunset, not a follow-up ticket.

**`INC-COMMS-01` — Incident Communications** (`05-scenarios/incident-communications/`)
Fact sheet citing incident-channel messages, an announced cadence that is kept, the four-state vocabulary, audience separation, no cause speculation or duration promises, and never "your data is safe" during an investigation.

**`OPS-01` — Operational Readiness** (`05-scenarios/operational-readiness/`)
Would the on-call engineer survive this at 03:00? Silence/saturation/dependency/partial failure signals, alert triage into page/ticket/remove, the runbook outsider test, dated proof of rollback and restore, on-call access confirmed *today*, one timed exercise.

**`BUILD-01` — Build Performance** (`05-scenarios/build-performance/`)
Phase timings before any fix; three loops with different budgets (edit / verify / release); reduce the work before caching it; measure the cache hit rate; before-and-after with the same method including cold cache.

**`AIVERIFY-01` — Verifying AI Output** (`05-scenarios/ai-output-verification/`)
The agent's completion report is a set of hypotheses. Claims verbatim, clean-state reproduction, test counts compared against the base commit, revert-and-fail as the only proof a new test works, diff accounting including silenced checks — and `unverifiable` may never be rounded up to `verified`.

### Changed

- `04-process/dependency-management/P01` now routes licence findings to `LIC-01` and supply-chain integrity to `SUPPLY-01` instead of leaving both as a bullet.
- `02-engineering/security-hardening/` boundaries now point to `SECRET-CLIENT-01`, `SUPPLY-01`, and `STD-01`, because a leaked server credential, a published client key, a tampered build, and an unevidenced control are four different problems.
- Coverage matrix: 139 dimension rows (**110 adequate / 29 partial / 0 missing**, was 97/30/0) and 15 workflow rows (10 adequate). The stale "Missing scenarios still open" list — which still named data engineering, mobile, embedded, and desktop/CLI — is gone, replaced by an honest statement of what *partial* means and why "adequate" is a structural claim.

### Also in this release

- **`DATA-MIG-01` — Data Migration** (`05-scenarios/data-migration/`): moving records between systems rather than changing a schema in place. Field mapping with a loss register, identity decided before the load so reruns upsert, resumable batches with reject files, reconciliation on hashes and aggregates rather than counts, two rehearsals, and a cutover whose rollback has a named expiry point.
- **`PRIV-P04` — Deletion Verification** (`04-process/privacy-requests/P04`): the adversarial half of deletion. Per-location definitions of what "deleted" can mean (an immutable log ages out; a backup expires), multiple identifiers including hashes, verification queries tested against a known-positive record, resurrection paths through restore and rebuild, and a synthetic canary through the real path.
- **`ACCESS-01` — Access Review** (`02-engineering/access-review/`): entitlements from the identity provider and the cloud rather than the roster, decisions per entitlement rather than per person, non-human access and break-glass accounts, removals verified by denial, and exceptions with an owner and an expiry.

### Result

441 Markdown files, **351 prompts: 197 operational, 5 draft, 149 skeleton**. Validator 0 errors / 0 warnings; self-tests 6/6; gallery current; no new near-duplicates (highest containment 0.18, unchanged). Backlog #92–#99 added; #93, #95, and #97 closed in the same release, because a backlog entry written and left undone is a recommendation dressed as work.

## [2.17.0] — 2026-10-20

### New — completing the map: the last missing domain, the last untested assumption

Nine prompts and one tooling change that close the remaining gaps a reader of the coverage matrix could still find: desktop/CLI (the last "Missing" row), disaster recovery (**zero** mentions before this), time correctness, third-party integration, file uploads, localisation, infrastructure as code, performance budgets, monorepo health, and API versioning.

**`DR-01` — Disaster Recovery** (`05-scenarios/disaster-recovery/`)
`disaster recovery` appeared in no file. Six disaster classes (corruption, service loss, region loss, account loss, backup-system loss, deliberate destruction), the six silent backup failures, a restore drilled in an isolated environment, phase-by-phase RTO measurement, and verification of the *application* against restored data — sequences, extensions, migrations — because a restore whose exit code is zero proves only that a command ran.

**`TIME-01` — Time and Date Correctness** (`02-engineering/time-correctness/`)
Instants vs wall-clock vs dates; eight anti-patterns including `BETWEEN` on timestamps, `now - N*24h` for calendar days, and `setMonth()` overflow; DST, month-end, leap-day and year-boundary tests; frozen clocks so results are reproducible.

**`INTEG-01` — Third-Party Integration** (`05-scenarios/third-party-integration/`)
Eight failure modes (slow, down, wrong, duplicate, out of order, changed, rate limited, partial) with defined handling; body validation over status codes; idempotency keys stable across retries; the timeout-is-not-failure rule; webhook signatures verified on the raw body.

**`UPLOAD-01` — File Uploads** (`05-scenarios/file-uploads/`)
Limits enforced at three layers, magic-byte validation, re-encoding to strip payloads and EXIF, generated keys, private bucket with short-lived signed URLs, SSRF refusal, multipart idempotency, orphan lifecycle, and object keys tied to owning entities so deletion actually deletes.

**`I18N-01` — Localisation Correctness** (`05-scenarios/localization/`)
No fragment concatenation, ICU plural categories instead of `count === 1`, pseudo-localisation before translation, logical CSS properties and correct icon mirroring for RTL, locale-aware sorting and search.

**`IAC-01` — Infrastructure as Code** (`05-scenarios/infrastructure-as-code/`)
Provider API as ground truth, provenance per resource, every plan `destroy`/`replace` as a decision, state posture (encrypted, locked, versioned), import-verify-no-change adoption loop, pipeline as the only path, scheduled drift tickets.

**`PERF-BUDGET-01` — Performance Budgets** (`05-scenarios/performance-budget/`)
p75 baselines on mid-tier mobile, budgets from perceptible thresholds plus a separate regression ceiling for existing debt, a deterministic CI gate, per-route size attribution on pull requests, and a budget for third-party scripts.

**`MONO-01` — Monorepo Health** (`05-scenarios/monorepo/`)
Import-level graph over manifests, deep imports and globals as boundary violations, tasks that declare inputs to be cacheable, affected-only demonstrated by changing a leaf, CI time broken down before any intervention.

**`API-VER-01` — API Versioning** (`03-domains/backend/P09`)
Consumer inventory before scheme, a change-classification table (additive is only safe if clients tolerate unknown fields), schema artifact with contract tests, deprecation with traffic thresholds, and a ceiling of two concurrent majors.

**`DESK-P01`, `DESK-P02` — Desktop & CLI** (`03-domains/desktop-cli/`, new domain)
Distribution as a trust boundary: pinned and verified install scripts, signed artifacts, an updater that verifies signatures, channels and pinning, clean-machine install evidence. Terminal contract: exit codes as an API, stdout/stderr separation, TTY detection, `NO_COLOR`, SIGINT/SIGTERM cleanup, SIGPIPE, and no prompt without a terminal.

### Library capability

- **`scripts/test_validator.py`** — six fixtures for the system-README maturity rules, wired into CI before validation.
- **A real defect found by writing the tests:** the 2.16.0 regex matched `**Status:** Operational` but not `**Maturity: operational (v1.0.0).**` — the form used by most READMEs here. The check was silently matching almost nothing. Fixed, and both forms are now pinned by fixtures.

### Result

426 Markdown files, 336 prompts: 182 operational, 5 draft, 149 skeleton. Validator 0 errors / 0 warnings; validator self-tests 6/6. Coverage **97 adequate / 30 partial / 0 missing**. Backlog #84–#91 added; #52, #53, #54, #57, #75–#79, #81, #82 closed.

## [2.16.0] — 2026-10-20

### New — the failures nobody wrote a prompt for

This batch was driven by one question: *what breaks in production that no prompt in this repository would catch?* Each of the six was absent by keyword search, and each is common enough that most teams will meet it.

**`TENANCY-01` — Tenant Isolation Audit** (`02-engineering/tenancy-audit/`)
Cross-customer leakage is the highest-severity defect class in B2B software, and it had no coverage at all. Store inventory before code review; enforcement classified as database / query-layer / convention (with a count of the surfaces relying on the weakest); seven named leak patterns including cache keys, background-job scope, search filters, object storage keys, and logs; a two-synthetic-tenant regression suite; and existence-disclosure (404 vs 403) as its own finding class.

**`SEC-ROT-01` — Secret Rotation** (`02-engineering/secrets-rotation/`)
Rotation existed only as "rotate first" inside incident remediation. This treats it as a **capability proven by a drill**: inventory by consumer rather than by store, four classes (compromise, signing, outbound API, infrastructure), overlap-versus-cutover chosen explicitly per class, and the verification that matters — the old credential is *rejected*, not just that the new one works. The 03:00 cron is the test.

**`JOBS-01` — Background Jobs** (`05-scenarios/background-jobs/`)
Duplicate charges, double emails, stale locks, jobs that quietly stopped. Organising rule: every job eventually runs twice, late, or concurrently with itself. Covers idempotency by constraint rather than check-then-insert, overlap locks with expiry, visibility timeout versus p99 runtime, cursor-based resume, UTC scheduling with an explicit DST test, and dead-letter queues that someone actually watches.

**`EMAIL-01` — Email Deliverability** (`05-scenarios/email-deliverability/`)
The provider returns `202 Accepted` and the message disappears. DNS-verified SPF (one record, ten-lookup budget), DKIM selectors and key length, and DMARC **alignment** — the distinction most teams miss. Plus transactional/marketing reputation separation, bounce and suppression handling, warm-up, and a rule that no configuration changes before an SMTP response code arrives.

**`A11Y-01` — Accessibility Conformance Audit** (`04-process/accessibility-audit/`)
Closes backlog #32. WCAG 2.2 AA by testing rather than scanning: keyboard before screen reader before scanner, contrast measured on rendered output, reflow at 320 px and 200% zoom, and the four 2.2 additions (focus not obscured, dragging alternatives, target size, redundant entry). Requires an explicit statement of what was *not* tested.

**`DE-P01`, `DE-P02` — Data Engineering** (`03-domains/data-engineering/`, new domain)
Closes the coverage matrix's "Data engineering: Missing — `data-ml-ai` conflates pipelines with modelling". P01 asserts on output, not task status, and treats a 90% volume drop as a failure; P02 treats a backfill as a migration with consumers — snapshot, full-scale dry run, atomic per-partition writes, value-level reconciliation, and a delta communicated to whoever used the old numbers. `data-ml-ai` now starts after trustworthy data.

### Library capability

- **Validator:** system READMEs claiming operational no longer escape detection. `README_CLAIM` now matches `**Maturity: operational`; a second rule catches prose "Operational" claims when most stages are outlines and the README does not declare itself mixed. It found two genuine overclaims (`01-contribution/web`, `/web3`, both rewritten to skeleton) and one false positive (`games`, exempted by its "Mixed" declaration).
- **Deduplication:** a draft SLO stage (`OBS-P06`) was written, compared against `OBS-P03` (which already defines SLIs, error budgets and burn-rate alerting), and **deleted**. Backlog #55 is recorded as rejected-as-duplicate rather than implemented.

### Result

**`WF-AGENTADOPT` — Adopting Coding Agents** (`07-workflows/agent-adoption.md`)
The addendum named "introducing AI agents into engineering workflows with appropriate evaluation, permissions, oversight, and rollback" as a critical workflow. The library had the parts (`CTX-P01..P04`, `AI-P07`, `WF-VERIFY`) but no procedure that sequences them: measurable objective and baseline, reduced permissions, an oversight model per risk class, a pre-registered pilot, independent verification, the four failure signatures (weakened tests, undeclared refactors, deleted assertions, unexecuted claims), an audit trail, and a drilled rollback that does not depend on the tool's cooperation.

### Result

414 Markdown files, 325 prompts: 171 operational, 5 draft, 149 skeleton. Validator 0 errors / 0 warnings. Coverage **88 adequate / 30 partial / 1 missing** dimensions. Backlog #75–#83 added.

## [2.15.0] — 2026-10-20

### New — prompt generation, prompt evaluation, and five specialized domains

A batch that started with one question ("can I generate a prompt from a description?") and one instruction ("go deeper on specialized fields"). The audit found both gaps real — `meta-prompt` returned zero files, and `reentrancy`, `gas fee`, `EVM`, `Unity`, `Godot`, `iOS`, `Android`, `firmware` appeared in no prompt — and the work itself exposed eleven more gaps (backlog 61–74).

**`GEN-P01` — The Prompt Forge** (`00-core/prompt-engineering/PROMPT-FORGE.md`)
Turn a description into a runnable prompt. Five modes with distinct exit conditions: **compose** (description → prompt), **interview** (ask only what changes the output), **improve** (rubric-scored critique + rewrite), **decompose** (one ask → ordered stages with I/O contracts), **port** (retarget to another agent). It routes against existing coverage *before* drafting, derives the risk class from consequence rather than phrasing, requires a verification table a person can actually execute, self-scores and names its two weakest dimensions, and emits the prompt plus a variables table, three test cases, and a provenance line marking the output `draft`. Generated is never counted as validated.

**`GEN-P02` — Prompt Regression** (`PROMPT-REGRESSION.md`)
The protocol the library lacked: fixtures frozen before results, two runs per case in fresh sessions, trace-level grading, separate design score and behavioural grade, and defect classification (missing / ambiguous / ignored / fixture / tool limitation) that determines whether the fix is prose or a machine check.

**`03-domains/web3/` — `CHAIN-P01..P04` (new domain)**
Threat model with exploit-path ranking by profit-to-attacker (access control, reentrancy, accounting, oracle, arithmetic, signature/replay, upgradeability, MEV, DoS), key custody as a design object (tiers, thresholds, timelocked authority, drilled rotation), upgrades with storage-layout diff, append-only rule, fork rehearsal and a declared rollback position, and exploit response that contains before it explains.

**`03-domains/mobile/` — `MOB-P01..P03` (new domain)**
Store release with a halt criterion written *before* the rollout and rollback levers tested because unpublishing is impossible; crash triage that symbolication-gates every conclusion and ranks by affected users and critical path; client-version compatibility with per-version fixtures, a deprecation schedule, and forced-upgrade escape hatches.

**`03-domains/embedded-iot/` — `IOT-P01..P02` (new domain)**
Firmware OTA with atomic slot writes, hash readback, trial boot with automatic confirmation, automatic rollback, repeated power-cut testing, and cohort rollout with pre-declared abandonment. Fleet health that treats silence as a signal, classifies it by cohort, checks the server before the device, and gates mass commands behind one proven path.

**`03-domains/games/` — `GD-P09`, `GD-P10` (2 of 8 stages now operational)**
Save migration with versioned schemas, forward-only chains over the whole support window, real historical saves as fixtures, atomic writes and a failure path that preserves the original. Netcode diagnosis aligning server tick, client tick and input timestamp, measured against a budget, with determinism verified by replay rather than argument.

**`03-domains/ai-agentic/` — `AI-P06`, `AI-P07`**
Grounded retrieval: ≥30% unanswerable questions, recall before groundedness, citation correctness scored separately, abstention and false-abstention both measured, and ACL leakage tested as a security case. Agent permissions: capability over intent across six axes, supply-chain review of MCP servers (including unpinned `npx`), remote-fetched rule files as an instruction channel, and a tightened configuration that must still survive the daily workflow.

### Result

404 Markdown files, 317 prompts: 163 operational, 5 draft, 149 skeleton. Validator 0 errors / 0 warnings. Coverage 82 adequate / 30 partial / 2 missing dimensions. Overlap maximum 0.11 against the 0.55 gate.

## [2.14.0] — 2026-10-20

### New — deployment targets, host migration, dev environments, agent context, on-call handover

A batch driven by two questions ("does it cover deployment to Render/Vercel?", "does it cover IDE/agent adaptability?") and by the gaps those questions exposed. Five capability areas, seven prompts.

**`05-scenarios/deployment-target/` — `DEPLOY-01` + `PLATFORM-PROFILES.md`**
The platform is an input (`{{DEPLOY_PLATFORM}}`), the guarantees are not. Covers app-shape classification (static/SSR/serverful/worker/functions/db-backed), the **three configuration scopes** that break deployments (build-time inlined, runtime, preview-inherited), ephemeral filesystems, request/execution timeouts, cold starts, region and residency, egress IP allowlists, one project per environment, end-to-end verification of the deployed URL (not `GET /` returning 200), cost metering with a budget alert, an exercised rollback, and a documented exit route. The profiles file carries per-platform traps for Vercel, Netlify, Cloudflare, Render, Railway, Fly.io, Heroku, AWS, Cloud Run, App Service, VPS+Docker, and Kubernetes — plus the universal six (port binding, env scope, filesystem, timeouts, region, rollback) and the cost-trap table.

**`05-scenarios/platform-migration/` — `HOSTMIG-01` (class D)**
Moving a live service between hosts. Peripheral inventory (DNS incl. MX/SPF/DMARC and verification TXT, cookies, OAuth callbacks, webhook registrations, egress allowlists, cron syntax, email reputation), TTL lowered 24–48 h ahead so the window equals the TTL, dual running with a proxy or DNS cutover, pre-declared abort criteria with a named decision-maker, data verified by counts and checksums, **old host's cron disabled at cutover** (duplicate jobs are an incident), old host retained past the TTL, and a real decommission step.

**`04-process/agent-context/` — `CTX-P01..P04` (new system)**
The instructions a team gives its AI assistant are a second, unreconciled specification. P01 inventories by *tool* (AGENTS.md, CLAUDE.md, `.cursor/rules`, Copilot instructions, Windsurf/Cline, MCP configs, editor settings, devcontainers) and verifies a sample of claims; P02 writes one canonical `AGENTS.md` (five-element first screen, commands executed before written, concrete prohibitions with alternatives, "when stuck") and reduces every other file to a ≤15-line adapter; P03 **tests adherence** with probes across command/convention/boundary/ambiguity in fresh sessions, diagnoses violations into missing/ambiguous/ignored/tool-limitation, and re-tests; P04 mechanises the checkable claims, binds updates to triggers, names owners, and measures decay.

**`05-scenarios/dev-environment/` — `DEVENV-01`**
"Clone and run" is usually false. Baseline the gap on a clean machine, pin runtimes in tool-readable files, remove global installs, provide one entry point (container + idempotent script), reproducible services with synthetic seeds, committed editor config, `.gitattributes` and case-sensitivity checks, CI parity, and per-OS verification where only tested OSes are claimed.

**`05-scenarios/on-call-handover/` — `ONCALL-01`** (backlog items 12/39, open since the first cycle)
Shift handover as an evidence artifact: state from the alerting system rather than memory, every silence with an owner and expiry, changes including config and infrastructure, about-to-break dates (certs, quotas, storage), known-noise alerts named, "if this pages you tonight" with the first diagnostic step, follow-ups owned, a read-back, and explicit authority transfer.

### Result

386 Markdown files, 301 prompts: 147 operational, 5 draft, 149 skeleton. Validator 0 errors / 0 warnings. Coverage 78 adequate / 30 partial / 4 missing.

## [2.13.1] — 2026-10-20

### Fixed — licence detection

`LICENSE` carried an explanatory paragraph after the MIT text, which made GitHub's licence detector read the repository as "Other" (`NOASSERTION`). The file is now the exact MIT text, so the repository is identified as MIT; the "what this covers" note moved to `LICENSE-CONTENT`, which already scoped the split.

## [2.13.0] — 2026-10-20

### Added — licensing (blocking item for publication)

The repository had no licence, which under default copyright means "all rights reserved" — the opposite of why it exists.

- **`LICENSE`** — MIT for the executable code (`scripts/` and code samples).
- **`LICENSE-CONTENT`** — CC BY 4.0 for every prompt, standard, README, and guide, with a practical attribution form, the "indicate changes" requirement, and an explicit note that attribution does not imply endorsement of a modified system.
- README gains a short licence section explaining the split in one paragraph.

### Added — `05-scenarios/hackathon-sprint/` (`HACK-01`)

The library's own origin story had no coverage: a hard deadline, a judging rubric, and four minutes on stage. `hackathon` appeared in zero prompts. This is not `from-scratch` (a skeleton, and unbounded in time) and not `quick-fixes` (a defect, not a demo).

- **Rubric as specification** — every criterion mapped to a visible demo moment, with the time share it deserves; a criterion without a demo moment is declared not competed for.
- **Demo script first** — 5–8 numbered, visibly obvious steps; the build works backwards from them, and anything off the path is out of scope by definition.
- **Cut lines declared in advance** — trigger, fallback, and time, so scope is decided at T‑12h rather than at the deadline.
- **The last 15% is reserved** — freeze at T‑3h, rehearsed twice at T‑2h, submission at T‑1h (portals fail; submit early).
- **Stage-failure plan** — venue internet assumed hostile: local run, seeded state, a recording on the presenting machine, fonts verified at projector resolution.
- **Honest mocks** — mocked, hardcoded, and demo-only behaviour disclosed in the README; never a faked security control, payment, medical or legal claim, or "real users".
- **Credential discipline under time pressure** — the single most common hackathon defect gets its own section: nothing in commits, `.env.example` only, scan the log, rotate anything that was exposed rather than rewriting history mid-event.
- **Post-event honesty note** — what is real, what is theatre, what the next 48 hours need, so a winning demo does not become a false claim of production readiness.

### Result

370 Markdown files, 293 prompts: 139 operational, 5 draft, 149 skeleton. Validator 0 errors / 0 warnings.

## [2.12.0] — 2026-10-20

### New system — `04-process/handover/` (5 stages, operational)

The library covered handing *state between stages* and had nothing for handing *ownership of a project to another person or agent*: no access transfer, no revocation, no proof that the receiver could operate the thing. "Handover" appeared 146 times, all of it the per-stage block.

- **HAND-P01 Scope** — five handover types (person→person, team→team, agency→client, human→agent, agent→human), each with its characteristic failure; a transfer inventory across code, running system, access, obligations, and knowledge; what is explicitly *not* transferring; acceptance criteria written as capabilities ("the receiver can restore staging unaided"), not document deliveries; a bounded support window and a failure path.
- **HAND-P02 State** — proven vs believed as separate lists with pointers; deployed reality per environment including drift and leftover flags; open work at its exact position with the risk of leaving it; decisions with the *reasons* (so a successor does not undo a deliberate choice); obligations; and the 3 a.m. brief — alerts, escalation, rollback, irreversible actions.
- **HAND-P03 Access and revocation (class D)** — identity inventory including vendor and billing consoles; lockout-risk accounts (domain, cloud root, sole vendor admin) get dual control; order is add → verify → remove, never the reverse; **rotate everything the sender could read**; revocation must be *proven* by a failed access attempt; retained access is time-boxed with a named revoker; recovery path documented.
- **HAND-P04 Capability verification (class C)** — the receiver performs and the sender observes: build, deploy, roll back, mitigate a known alert under time pressure, make a small end-to-end change, and find the people. Failures are classified as documentation, access, or **system defect** — and the last is the most valuable thing a handover can find.
- **HAND-P05 Acceptance** — verdict per criterion against capability evidence; every gap becomes a condition with an owner, a date, and a consequence; obligations confirmed moved *in the systems that enforce them* (rota, routing, billing); residual sender roles time-boxed and access-free; a 30–90 day review point; refusal recorded honestly when warranted.

### Promoted — `WF-HANDOFF` (draft → operational, v1.1.0)

The stage-handoff contract every workflow depends on was marked draft. It now names the four failures it exists to prevent (phantom completion, inherited assumptions, lost prohibitions, silent scope widening), requires the receiving stage to verify the two or three facts it depends on, decides staleness by repository state rather than document date, and defines a machine-readable form for agent receivers — with the rule that the machine copy must not say more than the prose.

### Scope clarity

The two are now explicitly different jobs in both READMEs: `WF-HANDOFF` moves state between stages of one engagement; `handover/` moves ownership across people, teams, or agents over time, and consumes the handoff block as its state input.

### Result

368 Markdown files, 292 prompts: 138 operational, 5 draft, 149 skeleton. Validator 0 errors / 0 warnings.

## [2.11.0] — 2026-10-20

### Promoted — `04-process/documentation/` (8 stages, operational)

The system existed as eight 800-byte outlines and its README claimed "Operational (v1.0)". It now does what the claim said, and covers the document products the library was missing: SRS, technical design/RFC, ADR, engineer handbook, API reference, runbook, quickstart, and PDF/DOCX delivery.

- **DOC-P01 Context & products** — a fixed product vocabulary with, per product, the reader, what must and must not appear, the source of truth, the delivery format, a mechanically checkable completion test, and an owner. Hybrid "spec+design+guide" documents are split, because the client and the engineer cannot approve the same page.
- **DOC-P02 Inventory & truth audit** — existence is not truth: commands are run, links resolved, endpoints compared to the spec, and every document gets a verdict (*accurate / partially / outdated / misleading / unverifiable*) with the check that produced it. Missing documentation is expressed as a failed reader task.
- **DOC-P03 Audience & structure** — personas from evidence, jobs with completion tests, task-first structure, one canonical page per instruction, and reading paths that act as the completeness test.
- **DOC-P04 Gap analysis** — gaps typed (missing/wrong/outdated/unfindable/unusable/duplicated/unsafe) and ranked by consequence, with **S1 reserved for pages that can cause harm when followed**; the high-consequence material (runbooks, security, destructive operations) is reviewed first regardless of the request.
- **DOC-P05 Plan** — sequence by consequence and path completion, an acceptance test and an owner per deliverable, and a **maintenance mechanism per document class with its blind spot stated** (generated reference cannot catch a stale spec; a doc test cannot catch a manual step).
- **DOC-P06 Writing** — per-product authoring contracts (an SRS contains no design; a requirement is testable or it is a wish; ADRs are superseded, never edited; runbooks carry expected output and escalation). Every command is executed or explicitly labelled unverified; never document unbuilt behaviour.
- **DOC-P07 Review, export, publish** — re-execute the author's claims, walk the paths as a reader, build PDF/DOCX **from source** and inspect every page (code wrapping, table overflow, missing images, glyphs, contents/anchors), verify PDF accessibility basics, and record the approval before external publication.
- **DOC-P08 Orchestrator** — five shapes (broken page, new product, documentation debt, structure problem, delivery problem), the source-of-truth gate, the reader gate, and the publication gate.

### New scenario — `05-scenarios/live-surface-audit/` (`SURFACE-01`)

Auditing something you can only reach over the network: a URL, host, or API. Rules of engagement before the first request; baseline with TLS and headers; redirects traced hop by hop; header/cookie/CORS/disclosure checks **on the final response** (not an intermediate CDN hop); error behaviour sampled for soft-404s and leakage; API contract signals; performance and accessibility/SEO at the signal level with the tool named; every finding carrying a request/response excerpt and a confirmed/suspected label. It explicitly excludes exploitation, enumeration by wordlist, load generation, and third-party targets without permission — and routes those to `02-engineering/security-hardening/`.

### Fixed — 17 system READMEs claimed "Operational (v1.0)" over skeleton stages

The validator checked prompt overclaims but not *system* overclaims. All 17 are corrected to state their real maturity, and a new validator rule fails the build when a system README claims Operational/Production-ready while any of its own stage prompts is skeleton or draft. Verified by reverting one README and confirming the error fires.

### Result

362 Markdown files, 287 prompts: 132 operational, 6 draft, 149 skeleton. Validator 0 errors / 0 warnings.

## [2.10.0] — 2026-10-20

### New system — `04-process/feature-flags/` (5 stages, operational)

Runtime switches are branches that bypass code review, deployment approval, and version control. The library had nothing governing them: no inventory discipline, no safe-default rule, no rollout evidence standard, no removal procedure. Backlog item 1, open since the first cycle.

- **FF-P01 Inventory & risk** — reconcile three sources (code, provider console, config) and treat every disagreement as a finding; type flags by *usage site*, not name, distinguishing release, kill-switch, permission, experiment, and migration, each with a different expected lifetime; audit every kill-switch for operator, off-path effect, and exercise history; rank by consequence; state blind spots and sampling.
- **FF-P02 Design & defaults** — justify the flag against four legitimate reasons or don't add it; route entitlement gates out of the flag system into the policy layer; name for removal; make the default a safety property (what happens when the provider is unreachable); stable bucketing for percentage rollouts; owner, expiry, and removal criteria at creation; both-states and flag-mechanics tests.
- **FF-P03 Progressive rollout** — guardrail thresholds and sample-size reasoning **before** exposure; cohort ladder before percentage ladder; numeric decision rule per stage; tested reversal including data already written; confounders recorded; a 100% rollout with the flag still present is only half done.
- **FF-P04 Kill-switch use** — state the symptom as a number, predict the effect, flip once, measure against the prediction, and classify the outcome (as predicted / no effect / worse); check that the off-path does not orphan data; record the flag state you leave behind. "No effect" is the most valuable result, because it redirects the investigation.
- **FF-P05 Retirement** — evidence of permanence rather than intent; delete the losing branch, tests, fixtures, and docs (a leftover conditional silently changes behaviour); check readers before removing a writer; decide the safety property explicitly when a kill-switch dies; add a prevention mechanism or ticket.

### Changed

- `04-process/README.md` and root routing table: feature-flags row and two routing entries; the duplicate stale `code-review` skeleton row is gone.
- Coverage matrix: new row "feature flags and progressive delivery" (adequate); totals 68 adequate / 32 partial / 4 missing.
- Backlog item 1 → **Implemented**.

### Result

361 Markdown files, 286 prompts: 123 operational, 6 draft, 157 skeleton. Validator 0 errors / 0 warnings.

## [2.9.0] — 2026-10-20

### Changed — input declarations across the operational library (backlog item 25)

Prompts described what they needed in prose ("the repository path", "a named approver"). They now declare it: **109 of 118 operational prompts** carry an `**Inputs:**` line, and every declared name appears as a `{{PLACEHOLDER}}` in the body.

The retrofit used each prompt's own §3 as the source of truth — no invented requirements:

- A value the user supplies became a canonical name and a placeholder: "Repository path" → `{{REPO_PATH}}`; "Named approver for Category C actions" → `{{APPROVER}}`; "Change window for production-affecting changes" → `{{CHANGE_WINDOW}}`.
- An upstream artifact stayed a dependency, not an input: `.qa/QA_CONTEXT.md`, `SAFETY_NET.md`, `.db/PREFLIGHT.md` are still `Depends on`.
- Systems retrofitted: code review (6), git operations (5), testing/QA (6), release engineering (4), observability (5), dependency management (5), decommissioning (4), governance (3), privacy (3), audit (4), refactoring (7), security hardening (5), project recovery (5), feature completion (3), database (5), payments (3), cost engineering (4), AI/agentic (5), scenarios (6), workflows (3), general agent (15).

**Nine operational stages deliberately declare no inputs** — `AUDIT-P02..P05`, `AUDIT-P07`, `FC-P02`, `REC-P03`, `SEC-P03`, `QA-P03`. They consume only the previous stage's artifact; a declaration would be unused, which the convention treats as a defect. The decision is recorded in `_meta/prompt-inputs.md` and backlog item 27 so a later reviewer does not "fix" it.

### Added

- `_meta/prompt-inputs.md`: **Canonical names** table, a three-tier taxonomy of the 97 names in use (13 core, 25 cross-system, 59 system-scoped), and a rewritten migration-status section with the exact figures and the list of nine exempt stages.
- `00-core/inputs/RUN-SHEET.md`: guidance for system-scoped names, and the alias rule.
- `01-contribution/open-source/general-agent/README.md`: an Inputs table mapping `MY_DETAILS.txt` to declared names, and an honest status line replacing "Complete and ready for use".

### Backlog

- Item 25 → **Implemented**.
- Item 26 (97 names is a wide vocabulary; consolidation pass) → Discovered, P2.
- Item 27 (nine artifact-only stages) → Evaluated, justified non-implementation, P3.

### Result

355 Markdown files, 281 prompts: 118 operational, 6 draft, 157 skeleton. Validator 0 errors / 0 warnings. Coverage matrix 67 adequate / 32 partial / 4 missing.

## [2.8.0] — 2026-10-20

### Promoted — `04-process/code-review/` (6 stages, operational)

The highest-frequency engineering activity in the library was a skeleton: stage names with no evidence rule, no severity vocabulary, and no way to distinguish a review from a list of opinions.

- **CR-P01 Context** — intent before judgement; scope metrics; change-type taxonomy; risk surface named before reading; review depth proportional to risk.
- **CR-P02 Understanding** — three passes (structure, semantics, detail) with deletions and renames read first; diff reconciled against stated intent, recording both extra and missing scope; one real path traced; untested areas and unknowns listed.
- **CR-P03 Findings** — every finding carries a consequence and evidence; `blocker` reserved for harm (data loss, security, broken behaviour, unverifiable claims); the category checklist covers authorisation, boundaries, error paths, concurrency, data, secrets, tests, contracts, operations; tests probed by mutation; an explicit accepted list so a clean review is still credible.
- **CR-P04 Feedback** — observation → consequence → request, with nit/question/blocker markers, findings ordered by consequence, duplicates consolidated, specific praise, and a summary that states an explicit decision.
- **CR-P05 Follow-up** — fixes re-verified rather than accepted; regressions reopened; every finding ends in a state; deferrals need an owner and a ticket; reviewers concede explicitly when the author is right.
- **CR-P06 Orchestrator** — triage into trivial/standard/high-risk/unreviewable, five gates, domain routing to `SEC-*`, `PAY-*`, `DB-*`, `DEP-*`, and disclosure of unreviewed areas.

### Changed

- Coverage matrix: review row moves from partial to adequate; totals 66 adequate / 33 partial / 4 missing.
- Root routing table, `04-process/README.md`, review log updated.

### Result

281 prompts: 118 operational, 6 draft, 157 skeleton. Validator 0 errors / 0 warnings.

## [2.7.0] — 2026-10-20

Two gaps found by asking questions the library could not answer: "what do I do when a merge conflicts?" and "which repository is 'the target area'?"

### Added — `04-process/git-operations/` (5 stages)

Git had only ever appeared as a prohibition ("never force-push") and a publication step. The situations themselves had no procedure.

- **GIT-P01 State check** — read-only, mandatory before any destructive command: detects the five in-progress operation markers (merge, rebase, cherry-pick, bisect, revert), inventories uncommitted and unpushed work, stashes and worktrees, records a reflog snapshot with its expiry, assesses whether the branch is shared, and takes three-way backups of work at risk.
- **GIT-P02 Conflicts** — classifies conflicts by type (textual, modify/delete, both-added, rename, binary, submodule, lockfile), requires each side's intent to be stated before editing, forbids wholesale `--ours`, regenerates lockfiles rather than merging them, and searches for semantic conflicts the merge cannot see.
- **GIT-P03 History repair** — gates on whether history is shared and who authorised it; prefers a corrective commit over a rewrite; backs up before the first rebase command; uses `--force-with-lease` only; mandates **rotate the secret before purging it**, and records the old→new SHA map so dropped commits are named rather than lost.
- **GIT-P04 Recovery** — preserve evidence (`reflog` dump, `.git` copy) before diagnosing; a symptom→cause→mechanism table covering reset, deleted branch, rebase drop, stash loss, force push, detached HEAD, committed deletion; recovers to a *new* ref so recovery cannot create a second casualty; forbids `gc`/`prune` mid-recovery.
- **GIT-P05 Hygiene** — observes current practice before prescribing, picks one merge strategy, sets review gates with an enforcement mechanism per rule (or an honest "convention only"), and covers lockfiles, binaries, submodules, line endings, and secret scanning.

### Added — prompt inputs and variables

- `_meta/prompt-inputs.md` — normative convention: `**Inputs:** NAME, NAME` in metadata, `{{NAME}}` in the body, defaults and fallbacks stated in §3, `SECRET_` naming for sensitive values, and the anti-patterns ("ask the user for anything you need", inputs that duplicate what the repo already states).
- `00-core/inputs/RUN-SHEET.md` — a fill-in sheet per engagement, with a mandatory `OUT_OF_SCOPE` line, minimal sheets for six common situations, and the rule that prompts echo the sheet into their output.
- Validator: an undeclared `{{PLACEHOLDER}}` is an error, an unused declaration is a warning, malformed or lowercase names are errors, and fenced blocks are ignored so examples are never validated.
- `scripts/new_prompt.py --inputs` writes the declaration; the authoring standard, template, `AGENTS.md`, and `CONTRIBUTING.md` document the convention.

### Changed

- Coverage matrix gains two rows (version control operations: adequate; prompt input configuration: partial, because only new prompts declare inputs).
- Backlog gains eleven entries, including the inputs retrofit (P1), shallow/partial clone support (P2), LFS migration (P2), and signed-commit provenance (P2).

### Result

355 Markdown files, 281 prompts: 112 operational, 6 draft, 163 skeleton. Validator 0 errors / 0 warnings.

## [2.6.0] — 2026-10-20

### Added — `03-domains/payments/` (3 stages)

Money is the one domain where a defect is a financial loss rather than a bad experience, and it had no coverage.

- **PAY-P01 Money model** — representation inventory that flags floats and missing currency dimensions, rounding and allocation rules where the parts must sum exactly to the whole, the payment state machine including out-of-order provider events, and invariants written as runnable checks.
- **PAY-P02 Idempotency & unknown outcomes** — a failure table per money-moving flow (lost response, delayed webhook, duplicate delivery, crash mid-write), idempotency keys persisted before the call and reused on retry, webhook replay and ordering safety, concurrency guards at the database level, and the rule that "unknown" is its own state rather than being treated as failure.
- **PAY-P03 Reconciliation & change safety** — per-transaction and aggregate comparison against provider settlement, a six-class difference taxonomy (timing, missing locally, phantom success, amount, duplicate, state), repairs that never re-charge, automated daily reconciliation with alerts, fee/FX treatment, and an eight-item checklist for every future money change.

### Changed

- Coverage matrix gains a money-correctness row; totals 64 adequate / 33 partial / 4 missing.
- Root routing table and `03-domains/README.md` updated.

### Result

347 Markdown files, 276 prompts: 107 operational, 6 draft, 163 skeleton. Validator 0 errors / 0 warnings.

## [2.5.0] — 2026-10-20

### Added — library tooling

- **`scripts/find_overlaps.py`** — near-duplicate detection across all prompts using 5-word shingles after stripping metadata, code fences, and shared boilerplate sections. Reports containment (how much of the smaller prompt appears in the larger) and Jaccard similarity; `--check` fails CI at 0.55 containment. First run: no duplicated content, highest containment 0.18 inside the templated contribution skeletons (recorded as a backlog item).
- **`scripts/new_prompt.py`** — scaffolds a prompt with the correct metadata block and all ten required sections, picks the version from the requested maturity, refuses to overwrite, and prints the catalog/gallery/overlap commands.

### Changed

- CI now runs the overlap gate.
- `AGENTS.md` and `CONTRIBUTING.md` document the scaffolder and the overlap check; the authoring standard remains the reference for content.
- Backlog records fourteen newly identified engineer problems with priority and home (feature-flag lifecycle, live-API versioning, queue backpressure, environment parity, test data, build performance, payment correctness, accessibility, i18n, estimation, incident follow-through, on-call handover, prompt A/B evaluation, contribution-system overlap).

### Result

273 prompts: 104 operational, 6 draft, 163 skeleton. Validator 0 errors / 0 warnings; overlap check clean.

## [2.4.0] — 2026-10-20

Two capabilities that had no coverage at all, both chosen because they cost real money or create legal exposure when improvised.

### Added — `03-domains/cost-engineering/` (4 stages)

- **COST-P01 Visibility** — period, currency, and discount treatment stated; spend broken down by service, environment, owner, and cost type; the unattributed percentage reported as a headline figure rather than a footnote.
- **COST-P02 Waste diagnosis** — findings classified by mechanism (idle, over-provisioned, always-on non-production, egress topology, storage growth, log ingestion, query scans, duplication, licensing, chatty calls), each sized in money with its calculation and its protecting dependency named.
- **COST-P03 Optimisation** — one change at a time per service, reliability tolerance agreed beforehand, health metrics and cost signal both verified, and a saving not treated as real until a billing cycle confirms it.
- **COST-P04 Guardrails** — unit economics with a three-month trend, thresholds with owners and responses, tagging enforced in IaC, lifecycle and scheduling controls, and standing exemptions for reliability and security.

### Added — `04-process/privacy-requests/` (3 stages)

- **PRIV-P01 Data inventory** — identifier variants, ten system classes including the ones usually forgotten (warehouse, search index, queues, APM payloads, vendor copies, backups), per-system queries and hit counts, and an explicit completeness statement.
- **PRIV-P02 Execution** — identity verification, legal-hold clearance, export scoped and redacted, deletion in dependency order verified by fresh queries, backups described honestly with an age-out date, blocked systems escalated rather than skipped.
- **PRIV-P03 Retention** — data classes with a stated basis and period, deletion enforced by mechanism (TTL, lifecycle, rotation) rather than intention, a request path sized to volume, and a verification job that alerts when deletion silently stops working.

### Changed

- Coverage matrix: two new dimension rows (cost / FinOps, privacy / subject rights); totals now 63 adequate / 33 partial / 4 missing.
- Root routing table, section READMEs, roadmap, and gallery updated.

### Result

343 Markdown files, 273 prompts: 104 operational, 6 draft, 163 skeleton. Validator 0 errors / 0 warnings.

## [2.3.0] — 2026-10-20

### Added / promoted — safe refactoring (7 stages, operational)

`02-engineering/refactoring/` was the largest remaining skeleton and covers the most frequently performed risky change in software.

- **REF-P01 Assessment** — refuses to start without a measurable target ("one place to change the tax rule instead of four"), classifies the request as refactor / rewrite / repair / optimisation / feature-in-disguise, and records stop conditions before any code moves.
- **REF-P02 Strategy** — technique chosen against the deployment constraint (preparatory, branch-by-abstraction, strangler, parallel run, or explicitly-treated-as-rewrite), slices that keep the trunk green, seams introduced before moves, reversal points, and an estimate sized against the stop conditions.
- **REF-P03 Safety net** — characterisation tests that assert current behaviour (including behaviour that looks wrong), golden-master corpora, contract tests at seams, and a **mutation probe per important test**; a net that has not been shown to catch breakage blocks execution.
- **REF-P04 Execution** — one mechanical transformation per commit, green after each, diff size checked against the budget, behaviour changes excluded and logged.
- **REF-P05 Validation** — golden-master diff including hold-out inputs, contract-surface diff, post-move mutation probe, differential or shadow comparison, performance delta, and a measurement of the P01 target.
- **REF-P06 Cleanup** — observation window before removal, three-signal evidence of non-use, removal in dependency order (flag last), documentation and diagrams updated, follow-ups routed.
- **REF-P07 Orchestrator** — gates with artifacts, failure routing (red net → revert slice; behaviour change → separate; target unmet → reassess, not re-execute), and scope-drift protection.

### Changed

- Coverage matrix: technical debt and maintenance rows move to adequate; dimension totals now 61 adequate / 33 partial / 4 missing.
- Roadmap marks refactoring complete; backend is now the highest-value remaining skeleton.

### Result

266 prompts: 97 operational, 6 draft, 163 skeleton. Validator 0 errors / 0 warnings.

## [2.2.0] — 2026-10-20

### Added

- **`GALLERY.md`** — a single index of every prompt (266) with a direct link and one line describing when to use it, grouped by area and system, with maturity and risk class per row, plus the seven `00-core` reference documents. Generated from the prompt files, so it cannot drift from them.
- **`scripts/generate_gallery.py`** — builds the gallery. Purpose text comes from the prompt's `Gallery:` metadata line if present, otherwise from the first usable line of its objective (role prose and prohibitions are skipped), otherwise its `Produces:` value. `--write` regenerates; `--check` fails when the file is stale.
- **CI gate**: the workflow now runs `--check`, so adding or renaming a prompt without regenerating the gallery fails the build.

### Changed

- Five scenario skeletons (`quick-fixes`, `performance-investigation`, `legacy-code`, `onboarding`, `pr-authoring`) had ad-hoc headers (`**Version:**`, `**Type:**`, `**Use when:**`) and were invisible to the catalog and gallery. They now carry standard metadata with identifiers `QUICK-01`, `PERF-01`, `LEGACY-01`, `ONBOARD-01`, `PR-01`, maturity `skeleton`, version `0.1.0`.
- Validator: `_meta/` is no longer counted as prompts (the template is tooling, not a prompt), and any new Markdown file that is neither a prompt nor an allowed document now fails validation with an actionable message — closing the hole that hid those five files.
- `AGENTS.md`, `CONTRIBUTING.md`, and `_meta/prompt-authoring-standard.md` document the gallery step, the optional `Gallery:` field, and the `<!-- not-a-prompt -->` marker.

### Result

334 Markdown files, 266 prompts: 90 operational, 6 draft, 170 skeleton. Validator 0 errors / 0 warnings.

## [2.1.0] — 2026-10-20

Gap-discovery cycle driven by a new coverage matrix rather than the existing roadmap. Five systems and one workflow were added; three missing scenarios in the previous audit are closed.

### Added

- `_meta/coverage-matrix.md` — 12-dimension coverage assessment (97 dimension rows, 14 workflow rows) with a status and evidence pointer per row, an end-to-end assessment of 14 critical workflows, and a computed summary. A scenario counts as adequate only when a prompt addresses its distinctive verification and failure handling.
- `03-domains/database/` (5 stages) — schema truth, migration design with an old/new code compatibility matrix, pre-flight validation on a realistic copy with a performed restore drill, execution with reconciliation, rollback and post-verification.
- `04-process/dependency-management/` (5 stages) — dependency inventory and risk, breaking-change assessment matched to actual code usage, one-family-per-commit execution with lockfile discipline, verification with mutation probing, and a written update policy.
- `02-engineering/feature-completion/` (4 stages) — a 14-layer completion checklist, layer gap map against an analogue, end-to-end implementation, and acceptance tested per role with direct endpoint access.
- `07-workflows/independent-verification.md` — adversarial verification of another agent's completion claims: claim extraction, clean-state reproduction, mutation probing, diff audit for undeclared scope and weakened tests.
- `05-scenarios/failed-fix/FAILED-FIX-ESCALATION.md` — attempt ledger, failure classification, and a decision to revert, re-scope, narrow, or escalate instead of patching again.
- `05-scenarios/data-loss/DATA-LOSS-RECOVERY.md` — freeze writes, preserve evidence, bound the window, restore to a side instance and merge, with a loss statement separating recovered / lost / uncertain.
- `05-scenarios/security-incident/SECURITY-INCIDENT.md` — evidence-first response for an active compromise: containment strategy trade-offs, persistence search, verified eradication against a baseline, disclosure decision record.
- `07-workflows/cross-layer-integration.md` — contract reconciliation before wiring, seam table with auth and failure contracts, transport/config diffs, end-to-end journey, per-seam failure injection, explicit unproven list.
- `04-process/decommissioning/` (4 stages) — consumer discovery that does not accept "no traffic" as evidence, notice periods derived from constraints, staged reversible shutdown with a quiescence window, and per-asset retirement with verified archives and revoked identities.
- `04-process/governance-compliance/` (3 stages) — claim-to-mechanism control map, evidence testing with population/sample sizes and mechanism bypass attempts, and a readiness decision offering fix/instrument/accept/stop-claiming per gap.
- `07-workflows/multi-agent-orchestration.md` — decomposing work across agents: interface freezing before fan-out, single ownership of shared files, fixed status-report form, per-task verification before dependents unblock, and independent verification of the merged result.

### Changed

- `05-scenarios/debugging/SYSTEMATIC-DEBUGGING.md` → v1.2.0, after the library's first empirical execution (`_meta/empirical-evaluation-01.md`): treat a green suite as evidence it encodes the bug, vary invocation context when localising, ordered hypothesis classes led by shared mutable state, and a required explanation of why the existing tests missed the defect.

- Root README routing table extended with verification, failed-fix, database, dependency, and feature-completion entries.
- `_meta/ROADMAP-AND-BACKLOG.md` restructured: completed items marked, and a new "Discovered in 2.1.0" section with nine opportunities, their priority, and five rejected/deferred ideas with reasons.
- `_meta/coverage-matrix.md` summary counts are computed from the tables, not estimated.
- Validator: risk-class heuristic no longer flags descriptive mentions of deployment; backticked repository paths are checked for existence.

### Fixed

- Four `06-interactive` prompts had no metadata block and were invisible to the catalog; migrated.

### Known limitations

- 165 prompts remain `skeleton`.
- No prompt has been empirically executed against a real repository; structural validation is not empirical validation.
- 4 dimension scenarios remain missing (data engineering, mobile, embedded, desktop/CLI); no critical workflow is unprocedured, though five remain partial.

## [2.0.0] — 2026-10-20

This release reconciles the library's claims with its artifacts, establishes enforceable standards, and adds the systems that were most conspicuously missing. It is a breaking change for anyone who trusted the previous status tables: most systems are now labelled `skeleton` because that is what they are.

### Added

- `_meta/prompt-authoring-standard.md` — metadata schema, four maturity levels, nine execution modes, twelve required sections, writing rules, definition of done.
- `_meta/quality-rubric.md` — 100-point rubric with band anchors, three mode-specific weightings, nine critical failure conditions, review-record format.
- `scripts/validate_library.py` — validates metadata, identifiers, maturity/version consistency, required sections, links (Markdown and backticked repo paths), empty sections, risk-class honesty, and status overclaims; generates `_meta/CATALOG.md`.
- `07-workflows/` — five composed workflows (`recover-abandoned-project`, `audit-to-remediation`, `production-incident`, `greenfield-delivery`, `continuous-improvement`) plus `HANDOFF-CONTRACT.md`.
- `02-engineering/project-recovery/` — seven-stage system for inherited, interrupted, or broken projects (containment → intent → completeness → integration → plan → execution → acceptance).
- `04-process/observability-reliability/` — five stages: assessment, instrumentation, SLOs/alerting, on-call/runbooks, postmortem.
- `04-process/release-engineering/` — four stages: readiness, versioning/changelog, deployment/rollback, post-release verification.
- `03-domains/ai-agentic/` — five stages: context/risk, architecture, evaluation, safety/guardrails, production operations.
- `05-scenarios/flaky-tests/FLAKY-TEST-TRIAGE.md`.
- `.github/workflows/validate-library.yml` — runs the validator and fails if the generated catalog is stale.
- `PROJECT-STATUS.md` — continuation checkpoint.
- `AGENTS.md` — repository-level instructions for AI agents working in this repository.

### Rewritten to operational depth

- `02-engineering/security-hardening/` — all seven stages rebuilt around an authorisation gate, concrete abuse cases, an ingress-by-ingress enforcement matrix, triage that admits only confirmed S1/S2 findings, and remediation proven by failing-before tests and a route × role matrix.
- `02-engineering/codebase-audit/` — all nine stages rebuilt with a shared evidence standard, severity model with required evidence per level, finding schema, adversarial synthesis gate, and a report structure that includes risk of inaction and coverage limits.
- `04-process/testing-qa/` — all seven stages rebuilt with R1–R4 risk prioritisation, a coverage rule that rejects percentage-chasing, mutation spot checks, and a mandatory plan checkpoint.
- `05-scenarios/debugging/SYSTEMATIC-DEBUGGING.md` — reproduction, minimisation, explicit hypotheses, fix-proven-by-revert, regression test.
- `05-scenarios/incident-response/PRODUCTION-INCIDENT.md` — restore-first ordering, timeline discipline, data-integrity verification, postmortem handoff.

### Changed

- All 235 prompt files now carry a metadata block (`Identifier`, `System`, `Version`, `Maturity`, `Execution mode`, `Risk class`, `Depends on`, `Produces`).
- Versions of skeleton prompts reset to `0.1.0`; `1.x` is reserved for reviewed prompts.
- Root `README.md`, `CONTRIBUTING.md`, and section READMEs rewritten around actual maturity and discovery paths.
- `_meta/taxonomy.md` extended with `07-workflows`, `scripts`, the maturity axis, and rules preventing empty folders.
- `00-core/prompt-engineering/STAGE-PROMPT-TEMPLATE.md` reduced to a pointer to the single canonical standard.
- `04-process/README.md`, `05-scenarios/README.md`, `06-interactive/README.md` corrected and extended.

### Fixed

- Two system READMEs advertised `Operational` while all their stages were 20-line outlines.
- Root README claimed "the most complete ... archive" and "production-ready" systems that did not exist; replaced with a status table that states maturity.
- Empty "Planned / Future" sections removed; plans moved to `_meta/ROADMAP-AND-BACKLOG.md`.

### Removed

- Competing prompt template in `00-core/` (now a pointer), eliminating two divergent definitions of a valid prompt.

### Known limitations

- 165 prompts remain `skeleton`. They outline a defensible sequence but cannot run unsupervised. See the backlog.
- No prompt in this library has been empirically tested against a real repository and recorded. All `operational` labels are structural reviews.
