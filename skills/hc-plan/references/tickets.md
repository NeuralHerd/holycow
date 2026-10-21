# Ticket design and storage

## A useful delivery ticket

Use the project's template. If none exists, include:

- **Outcome:** A descriptive title and the behavior or capability delivered.
- **Source:** The parent brief or issue and relevant decision or experiment links.
- **Acceptance:** Observable success criteria and the verification approach.
- **Scope:** Affected responsibilities or repositories, important contracts, and necessary exclusions.
- **Blocked by:** Actual prerequisites, with stable references.
- **State:** Ready, blocked, or draft, expressed through the project's workflow.

Include only fields that carry useful information. A single ticket can also serve as the brief for a small change. Do not invent assignees, estimates, deadlines, performance targets, or infrastructure choices.

## Slicing exceptions

For a broad rename, schema transition, or shared-contract migration, first introduce the compatible new form, then migrate consumers in manageable batches, and finally remove the old form. The final removal depends on every affected consumer having migrated. Describe the evidence that establishes compatibility at each stage.

Keep intermediate work verifiable where possible. If pieces cannot pass independently, disclose the coupled validation boundary and recommend a coordinated integration approach. Do not label those pieces independently ready or create an integration branch contrary to the user's repository workflow.

A genuine prerequisite can have a technical outcome: for example, a test environment becomes reachable or an API contract is exercised by both producer and consumer. It still needs acceptance criteria; "set up infrastructure" is not enough.

## Configured tracker

Use connected tools or the available CLI. Inspect the actual project hierarchy, issue types, workflow states, and dependency support. Do not assume fixed Jira, GitHub, Linear, or other tracker fields or labels.

Search for existing records tied to the source and verify that they represent the same work before creating or updating them. Preserve stable identities. Never deduplicate unrelated tickets merely because their titles match.

Create missing records in dependency order, capturing returned IDs. Use native blocking links and parent relationships where supported; otherwise use explicit linked references following project conventions. Keep unresolved or blocked work out of the project's ready state.

Verify bodies, relationships, and states through returned data or follow-up reads. If a write fails or its outcome is unknown, inspect existing state before retrying. Keep the mapping between proposed slices and actual issue IDs so a resumed session can finish without duplicate tickets. Report anything unsaved or unlinked; do not claim full publication.

Do not close the source issue or rewrite a Compass decision record as an implementation task. If tracker access is unavailable, report it and preserve a clearly marked pending draft without claiming synchronization or silently changing the canonical destination.

## Local Markdown

Follow the existing planning convention. With none, use `.hc/plan/<effort>/brief.md` when a separate brief is useful and one file per ticket in `tickets/`, such as `01-save-draft.md`.

Use stable ticket identities and descriptive links; do not renumber existing tickets when the sequence changes. Record blockers and state explicitly. Reuse existing files for the same work instead of creating a new set on every invocation.

Keep the brief and ticket evidence traceable to their sources. Saving these records does not require initializing Git, creating a branch, committing, or publishing.
