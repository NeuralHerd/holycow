# Decision map storage

Use the user's chosen tracker or planning location. Keep one canonical map; do not maintain a competing local and remote copy.

## Configured tracker

Use available connected tools or the tracker CLI. Inspect the project's existing issue types, hierarchy, relationships, and workflow before writing; do not assume Jira, GitHub, Linear, or another tracker exposes identical capabilities.

Represent the effort with a parent or overview issue and link the question issues using the project's supported hierarchy. Store status, ownership, and blocking dependencies in native tracker fields where supported. Query those fields to find ready questions; the overview links decisions and artifacts without duplicating mutable status tables.

If native dependencies are unavailable, use explicit linked blocker lists following the project's convention and check them before selecting work. Map semantic states such as deferred or excluded to the existing workflow with a clear reason; a closed issue is not automatically a resolved prerequisite.

Record outcomes on the canonical question issue using the project's convention, then update its status and the overview. Verify tracker writes through returned IDs or a follow-up read. Report failed writes without claiming the tracker is updated.

If the selected tracker is unavailable, explain the limitation. Keep a clearly marked pending checkpoint if useful; do not silently switch the source of truth or claim synchronization.

## Local Markdown

Use this when requested or no tracker is configured. Prefer the project's existing planning folder; otherwise use `.hc/compass/<effort>/map.md` in the working directory, with a `questions/` folder beside it. This works without Git. Create only records currently needed; saving a local map does not require initializing Git, publishing issues, or committing.

The map holds status and dependency metadata; linked records hold each question's context and answer.

## Shared conventions

Keep one canonical record for each question. Existing glossary entries or ADRs remain canonical for decisions already recorded there: link them instead of maintaining competing copies.

## Map contents

- **Outcome:** The agreed result and what evidence makes the direction actionable.
- **Scope:** Included work and constraints.
- **Questions:** A tracker query or local table with stable ID, linked question name, method, status, dependencies, and owner when shared work is in progress.
- **Decisions so far:** One-line results with links to their canonical records.
- **Not yet clear:** In-scope uncertainties that cannot yet be phrased as precise questions.
- **Out of scope:** Excluded work and reasons.
- **Next step:** The recommended ready question or the blocker to resolve.

Use `open`, `in-progress`, `waiting`, `resolved`, `deferred`, and `excluded` as statuses when no project convention exists. Dependencies reference stable question IDs. A question is ready only when its prerequisites are resolved and it is unclaimed. Preserve IDs across title changes. Investigate missing or circular dependencies rather than inferring readiness.

## Question record

Use a descriptive title with the tracker issue's stable identity or a stable local filename, such as `questions/q1-export-timing.md`.

Capture the question, why it matters, and what would resolve it. Add relevant evidence links as they become available. On resolution, record the accepted answer or verified finding, rationale, alternatives where consequential, and limitations. Preserve dated corrections when later evidence changes the answer.

Link prototypes, research, and accepted decision records; do not embed entire transcripts or duplicate their contents. On resume, read the map and selected records, not every historical answer.
