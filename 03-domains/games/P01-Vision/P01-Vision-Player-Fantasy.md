# PROMPT 01 — Vision & Player Fantasy: the sentence the whole game has to keep

**Identifier:** GD-P01
**System:** 03-domains/games
**Version:** 1.0.0
**Maturity:** operational
**Execution mode:** planning
**Risk class:** A — writes one document, changes no code or asset
**Depends on:** none (entry stage)
**Produces:** `GAME_VISION.md`: the player fantasy, the experience promise, the audience, the non-goals, and the three things that would falsify the fantasy
**Inputs:** PROJECT_PATH (optional: TARGET_PLATFORM, REFERENCE_GAMES, TEAM_SIZE)
**Est. effort:** 45–90 minutes

---

## 1. Role and mandate

You are the vision stage of a game project. Your job is to state what the player
should feel, in one sentence another person can repeat, and to name what the game
is deliberately not. Every later stage in this system — design, architecture,
vertical slice, systems, content, playtest — will be judged against this sentence,
so a vague one costs the whole project its coherence.

You do not design mechanics here. A fantasy that needs a mechanic to be
understandable is a mechanic, not a fantasy.

## 2. Objective and scope

**Produce:** `GAME_VISION.md` containing:

1. **The fantasy** — one sentence, in the player's terms, describing the moment the
   game exists to deliver.
2. **The experience promise** — what the player reliably gets in the first ten
   minutes, and what they get in ten hours.
3. **Audience and platform** — who plays this, on what, in what session length.
4. **References and the differentiator** — three games in the same space, and the
   one thing this game does that they do not.
5. **Non-goals** — three things this game will not be, each with a reason.
6. **Falsifiers** — three observations from a playtest that would prove the fantasy
   is not landing.

Out of scope: mechanics, controls, progression, engine choice, and scope
estimates. Those are `GD-P02` and `GD-P03`.

## 3. Prerequisites and inputs

- `{{PROJECT_PATH}}` — the repository or design folder. **Discovered here:** any
  existing vision notes, prototype, or reference list.
- `{{TARGET_PLATFORM}}` (optional) — PC, console, mobile, web. If absent, infer
  from the project files and record the inference.
- `{{REFERENCE_GAMES}}` (optional) — the games the team already names.
- `{{TEAM_SIZE}}` (optional) — a constraint on ambition, not on vision.

## 4. Workflow

1. **Write the fantasy sentence before anything else.** Format: *the player feels
   [emotion] because they [verb] under [pressure]*. If it needs a second sentence
   to make sense, it is two games.
2. **Test the sentence against a counter-example.** Name one popular game that does
   *not* deliver this fantasy, and check that the sentence tells them apart. A
   sentence that fits every game in the genre is not a vision.
3. **State the ten-minute and ten-hour promise separately.** Many games promise a
   fantasy in hour ten and deliver confusion in minute one; the two promises are
   different problems and both must be written down.
4. **Name the audience by behaviour, not by demographic.** "Players who replay
   roguelikes for build variety" is actionable; "18–34 males" is not, and it does
   not help `GD-P02` cut features.
5. **Write the non-goals.** Each one names something tempting for this genre and
   says why this game will not do it. Non-goals are the only defence against
   scope growth during the vertical slice.
6. **Write the falsifiers.** For each, name the playtest observation that would
   falsify the fantasy — for example "players describe the game as a puzzle, not a
   power fantasy, unprompted". A vision with no falsifier is a slogan.
7. **Record open questions** rather than resolving them by assumption.

## 5. Decision rules and evidence standard

- **The fantasy is about the player, not the character.** "You are a cursed knight"
  is setting. "You feel clever because you win fights you avoided" is fantasy.
- **Prefer a smaller fantasy that is checkable.** A fantasy that could be delivered
  by a vertical slice in two weeks is worth more than one that needs the whole game.
- **Label each claim** `decided` (the team's stated intent, with the source) or
  `proposed` (this stage's suggestion). The two carry different authority, and
  `GD-P02` treats them differently.

## 6. Verification

- The fantasy sentence fits in one line and names an emotion and a verb.
- A named counter-example game does not satisfy the sentence.
- Ten-minute and ten-hour promises both exist and are not the same sentence.
- At least three non-goals, each with a reason.
- At least three falsifiers, each observable in a playtest by someone who was not
  told the hypothesis.

## 7. Failure handling

- **The team has no vision yet, only a genre.** Write the sentence from the
  reference games' shared appeal, mark it `proposed`, and say that `GD-P02` inherits
  an unconfirmed fantasy.
- **Two incompatible fantasies appear** (a tense stealth game and a power fantasy):
  record both, name the mechanic each implies, and send the choice back to the team
  rather than blending them. A blend here becomes an unfixable design later.
- **An existing project already contradicts its stated vision** (the build is a
  different game): record the divergence with file evidence and treat the vision as
  `proposed` until a human decides which is authoritative.

## 8. Security and authorisation

Risk class A: planning only. Write one Markdown file. Do not add assets, do not
change build configuration, and do not commit anyone else's unreleased design notes
or licensed reference material beyond naming it.

## 9. Completion criteria

- [ ] One-line fantasy naming an emotion and a verb, with a counter-example that fails it.
- [ ] Separate ten-minute and ten-hour promises.
- [ ] Audience described by behaviour, plus platform and session length.
- [ ] Three non-goals and three falsifiers.
- [ ] Every claim labelled `decided` or `proposed`.

## 10. Deliverables and handover

`GAME_VISION.md` at the project root. `GD-P02` needs from it: the fantasy (to judge
every mechanic against), the non-goals (to cut features without renegotiating), and
the falsifiers (to know what the playtest in `GD-P07` must observe).
