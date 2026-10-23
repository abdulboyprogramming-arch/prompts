# Author's notes for the change (the input given to the prompt, unedited)

- Promoted the onboarding prompt. It was a 55-line skeleton, "join an unfamiliar codebase". I built a
  takeover fixture (11 files) with real traps, ran the old prompt against it: 0 of 9. Rewrote it to
  v1.0.0, ran again: 9 of 9.
- Fixture is in _meta/fixtures/takeover-scenario/, both runs are stored verbatim in runs/.
- The rewrite adds an 11-step procedure and a verdict with conditions C1–C7.
- Counts moved: skeleton 74 → 73, operational 287. Evidence 39 of 287 (13.6%).
- check_all passes. Everything regenerated and committed.
- Also fixed a stale line in PROJECT-STATUS that still listed four 06-interactive stages as skeleton
  (they've been operational since 2.28.6).
- Not sure how much the six-file fixture proves. It's small. I ran it, that's all I can say.
- No UI.
