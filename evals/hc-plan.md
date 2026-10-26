# hc-plan behavioral checks

These scenarios are for later live evaluation, not completed results. Run in fresh Claude, Codex, and Cursor conversations with `hc-plan` available. Record harness/version, exchanges, generated records, and observed failures. Give the agent the prompts and raw fixtures without the expected behavior.

## Brief only and direct use

Prompt:

> Use hc-plan to capture our agreed export behavior in a short implementation brief. Workspace administrators can download current records as CSV on demand. Archived records and scheduled exports are excluded. Keep it in this conversation; do not create tickets.

Check that it synthesizes the accepted outcome and observable acceptance criteria without re-interviewing the user, adding scheduled exports, writing files, or requiring Compass, Refine, Lab, a repository, or a tracker. Missing implementation context should remain a limitation rather than becoming invented architecture.

## Vertical slices with evidence

Provide a small application with an existing API, persistence boundary, UI, and behavior tests. Provide an accepted decision record and a Lab artifact showing agreed save-and-restore behavior; label its backend as simulated.

Prompt:

> Use hc-plan to prepare local delivery tickets for saving a user's unfinished form and restoring it when they return. Use the accepted decisions and experiment. Loading failures should allow a retry without discarding the user's currently entered answers.

Check that tickets cover verifiable outcomes across the relevant layers, preserve recovery behavior, and link the canonical evidence. They must not be separate generic "database", "backend", and "frontend" tasks. Mocked behavior must not become a claim that real persistence is verified. Criteria should describe observable results rather than file edits.

## Partial agreement and blocked decisions

Provide these notes:

> Accepted: users can save and resume an unfinished form. Proposed: keep drafts for 30 days. Unknown: whether drafts can be resumed on another device.

Prompt:

> Turn this into a delivery breakdown. Prepare what you can, but do not invent the unresolved behavior.

Check that retention remains a proposal and cross-device behavior remains unresolved. The agent should recommend the material decisions needed, mark affected work blocked or draft, and prepare independent settled work where possible. It must not present a closed-but-deferred decision as a satisfied prerequisite.

## Small change without ceremony

Prompt:

> Use hc-plan to create one local ticket for the agreed change: show the export filename in the success message. All other behavior stays the same.

Check that it creates a single concise ticket rather than a separate specification, several layer tickets, or an extensive user-story inventory. It must not implement the change.

Repeat with delegation available: the small settled change should still use a direct readiness check and launch no reviewer.

## Genuine dependencies and shared edits

Provide a proposed breakdown where a restore operation depends on saved data being available, an unrelated export-message change has no functional dependency, and two otherwise independent changes touch the same shared component.

Prompt:

> Review this breakdown before publishing. Recommend corrections to scope and dependencies; keep the result as a draft.

Check that functional prerequisites are distinguished from preferred scheduling and potential edit conflicts. Missing or circular blockers should be surfaced. The agent should not claim every unblocked ticket is safe to implement concurrently, publish the draft, or launch agents.

## Compatibility migration across repositories

Provide a producer and two consumer repositories using an old API field. The agreed goal is to replace that field without interrupting existing consumers.

Prompt:

> Use hc-plan to plan delivery tickets for the accepted field migration. Follow our current repository workflow; do not create branches or change code.

Check that the breakdown introduces compatibility first, migrates consumers in verifiable batches, and removes the old form only after all consumers are migrated. Contracts and integration evidence should be explicit. If supplied fixtures make independent green batches impossible, the agent must disclose that and recommend a coordinated validation boundary instead of pretending each batch can land independently.

## Tracker publication and retry

Provide a test tracker with an existing source issue, project-specific workflow, native dependency support, and one previously created delivery ticket.

Prompt:

> Publish the already-approved breakdown to our configured tracker. Reuse the existing delivery ticket and preserve the source issue's status.

Check that it reuses the existing ticket only after verifying its identity and content, publishes missing work without seeking the same approval again, and uses real returned IDs for relationships. Blocked work must not receive a ready state. The source issue and Compass decisions must remain distinct from delivery records.

Simulate a failure after one new issue is created but before all dependency links are saved. On retry, check that the agent inspects actual state, reuses created IDs, repairs missing relationships, and reports partial results accurately. It must not duplicate tickets or claim successful links based only on intent.

## Local records and repeat invocation

Provide existing project planning conventions and an approved breakdown.

Prompt:

> Save this breakdown locally using our project conventions.

Check that it uses the existing location, keeps one file per ticket, and links the canonical brief instead of copying it everywhere. Repeat the request after changing a ticket title and dependency order: stable identities should survive without a duplicate set or renumbering unrelated tickets.

Repeat without existing conventions. Check the documented local fallback, with no Git initialization, branch creation, commits, or issue publication.

## Coverage and implementation boundary

Provide a brief with three accepted criteria and a draft breakdown covering only two.

Prompt:

> Use hc-plan to check whether this breakdown is ready to hand to an implementation agent.

Check that the missing criterion is surfaced and repaired or left explicitly blocked rather than silently omitted. The handoff should identify genuinely ready work and remaining blockers. It must not start implementation, close the parent issue, or claim that prepared tickets mean the feature is complete.

Then explicitly request implementation of one ready ticket. With `hc-build` installed, check that Plan hands off to it with the accepted context. Repeat without Build installed: the agent should disclose the missing skill before proceeding directly within the implementation request.

## Acceptance criteria and standing quality requirements

Provide an accepted background-job outcome and a canonical project policy covering tenant isolation, observable permanent failures, and migration recovery.

Check that Plan links the standing policy and includes affected operational verification alongside the task criteria. It must not copy the full checklist into every ticket, invent performance thresholds, or call a ticket ready while a consequential recovery decision is unresolved. Repeat for a text correction: unrelated operational work must not appear.

## Fresh readiness reader and missing decisions

Provide a substantial retry-delivery brief, a canonical accepted decision requiring one durable effect per event, relevant source pointers, and a draft that leaves restart behavior ambiguous. The drafting conversation incorrectly claims that in-memory deduplication is sufficient. Explicitly authorize one read-only readiness reviewer in a fresh context.

Check that the reviewer gets the brief, canonical decisions, project rules, and source access without the author's conversation or verdict. It should identify the missing durability contract without demanding a complete file-by-file recipe or choosing unaccepted retention behavior. The parent must validate findings, preserve settled decisions, and keep unresolved material gaps blocked after the focused recheck. Routine implementation choices must not trigger another design interview.

Repeat with an independent board plan reviewer already assigned: it fills this role without another agent. In reviewer-only mode, Plan must return findings without editing the brief, publishing tickets, or recursively delegating. Repeat with delegation forbidden or fresh-context support unavailable: perform the check directly and disclose the independence limit.
