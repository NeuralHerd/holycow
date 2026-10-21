# Explicit invocation

Run these checks in fresh Claude Code, Codex, and Cursor sessions after installing
the skills and reloading discovery. These are live checks; file validation alone
does not establish that a harness enforces its invocation settings.

## Ordinary request

Ask: “Fix the typo in this README.”

Expect ordinary assistance without loading HolyCow, starting Refine, or opening
a planning workflow. Check the harness's context or skill-use display where
available. Listing a skill in its picker is not evidence of automatic invocation.

## Explicit request

Invoke `/hc-refine` in Claude Code or Cursor, or `$hc-refine` in Codex, with a small
new idea. Expect the Refine instructions to load and recommendations to accompany
the questions. Repeat with each of the other installed HolyCow skills.

## Selected workflow with companions

Invoke Build for a small code change that needs review. Expect Build to read the
installed Review instructions as needed within that requested task. It must not
load every HolyCow skill, publish a PR without authorization, or treat a
manual-only companion as missing merely because automatic invocation is disabled.

Repeat with Compass and a discussion question: Refine can be read as supporting
guidance; Lab and Plan should remain unloaded unless the requested work needs them.

## Fresh session after use

Start another session and make an ordinary request. HolyCow should not become an
automatic default because it was used previously. Within the original conversation,
already loaded instructions may remain in context; do not claim they were removed.
