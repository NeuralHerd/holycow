---
name: hc-slice
description: Use when the user wants to turn agreed ideas, decisions, a plan, or prototype findings into an implementation brief or dependency-aware delivery tickets.
license: MIT
disable-model-invocation: true
---

# hc-slice

Turn accepted understanding into work another session can implement and verify. Preserve the decisions and evidence; do not invent the missing design.

In a repository, use the HolyCow context linked by its instructions, or `docs/agents/holycow.md` when present. Read only relevant sections and reuse context already loaded. Continue without it; recorded capabilities may need rechecking in this session.

## Gather the settled context

Use the conversation, provided plan, existing issue, Compass map, or Lab outcome. Read referenced source material and relevant updates, not just titles. For an existing system, inspect the affected responsibilities, interfaces, project instructions, glossary, decisions, and test conventions. Reuse context already gathered.

Separate accepted requirements, observed behavior, proposals, and unresolved questions. Resolve contradictions that affect the work before presenting it as ready. Preserve explicit exclusions and limitations of prototype evidence.

Do not repeat a full interview. Ask only about gaps that change scope, expected behavior, or verification, with a recommendation, reason, and trade-off. If further discussion or experimentation is needed, recommend `hc-grill` or `hc-lab` when available; do not require their installation. Keep affected work blocked while preparing independent settled work.

## Produce the right-sized brief

Honor the requested output: a brief, tickets, or both. A small change may need one ticket with its brief included. Reuse a suitable existing specification instead of rewriting it. A long user-story inventory or a separate specification document is not mandatory.

Capture only what an implementer needs:

- **Outcome and scope:** The problem, intended behavior, affected users or systems, and explicit exclusions.
- **Accepted decisions:** Relevant contracts, constraints, and links to canonical decisions or experiments. Preserve important failure and recovery behavior.
- **Acceptance criteria:** Observable results that establish success, including consequential edge cases. Do not invent thresholds or turn implementation steps into acceptance criteria.
- **Verification:** Where the behavior can be exercised and what evidence is required. Prefer existing test boundaries and behavior-level checks; identify materially new test boundaries as proposals. Link the project's standing quality requirements separately from task-specific acceptance criteria; both apply.
- **Dependencies and uncertainty:** Required capabilities, open decisions, and operational considerations that actually affect delivery, such as access boundaries, retry safety, observability, or migration recovery. Include only affected concerns and leave unagreed thresholds explicit.

Describe responsibilities and interfaces rather than prescribing an unverified file-by-file implementation. Verified code pointers may help navigation. Include a small accepted schema, type, or state-transition snippet when it expresses a decision more precisely than prose; link its source and preserve its limitations.

## Slice by verifiable outcomes

When tickets are requested, read [ticket design and storage](references/tickets.md).

Prefer narrow end-to-end increments through the layers actually affected. Each ticket should deliver behavior or evidence that can be demonstrated independently and fit a focused implementation session. Do not split mechanically into database, backend, and frontend tickets, or force a UI into backend-only work.

Put observable acceptance criteria on every ticket and link the brief and relevant decisions. Keep one canonical brief rather than copying it into every issue.

Infrastructure prerequisites, justified preparatory refactors, and migrations may be separate when independently verifiable and necessary. Explain what they enable. For broad compatibility changes, use an expand-migrate-contract sequence instead of forcing slices that cannot work independently.

For changes across repositories, identify participating repositories, interface contracts, compatibility requirements, and rollout dependencies. Keep the complete outcome and its integration verification explicit even when implementation must be split.

## Check scope and dependencies

Show the proposed ticket names, what each delivers, and what blocks it. Recommend a granularity and explain material trade-offs. Seek confirmation where the breakdown introduces an unsettled scope, sequencing, or delivery choice; reuse an already-approved breakdown and existing publication authorization.

Dependencies express genuine prerequisites, not a preferred work order. Check for missing blockers and cycles. No blockers does not establish that simultaneous edits are safe; identify shared-code or ownership conflicts separately.

Check that every in-scope acceptance criterion is covered and that no ticket adds unaccepted behavior. Mark tickets with unresolved decisions or unmet prerequisites as blocked or draft. A closed decision record or excluded ticket is not automatically a delivered prerequisite.

## Save and hand off

Use the destination and write authorization in the user's request. Reuse the configured tracker or project planning location; local Markdown is available when no tracker is configured or the user chooses it. A draft-only request stays draft.

Verify created records and dependency links. On retry, reconcile existing records instead of duplicating them. Report partial publication and outstanding work accurately.

Return the brief and ticket links, the ready work, and the blockers. Readiness requires settled behavior, usable acceptance criteria, available evidence, and satisfied prerequisites. Keep Compass decision records distinct from delivery tickets and preserve parent status unless the user asked to change it.

This skill prepares implementation; it does not launch agents, change product code, or infer that ticket creation authorizes execution.

For a separately requested implementation, hand off the ready work to `hc-build` when installed. If it is unavailable, disclose that before proceeding directly within the user's implementation request.
