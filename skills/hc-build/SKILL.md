---
name: hc-build
description: Use when the user asks to implement agreed work, diagnose or fix a bug or performance regression, and verify the resulting outcome.
license: MIT
disable-model-invocation: true
---

# hc-build

Implement or investigate the requested outcome and produce supporting evidence. Use the accepted requirements and the project's conventions, keeping diagnosis, implementation, verification, and delivery status distinct.

In a repository, use the HolyCow context linked by its instructions, or `docs/agents/holycow.md` when present. Read only relevant sections and reuse context already loaded. Continue without it; recorded capabilities may need rechecking in this session.

## Load the applicable guidance

Whether invoked by name or read directly, load the applicable references before the steps below. Resolve their paths from this skill's directory. Reuse complete, unchanged guidance already read in this session; retrieve needed sections omitted by truncated tool output.

| When to read | Required guidance |
| --- | --- |
| Before choosing checks for an implementation or verification task | [Verification](references/verification.md) |
| Before designing or changing trust boundaries, persistent or shared state, service reliability, or infrastructure | [Production concerns](references/production.md), limited to the affected concerns |
| Before investigating a reported bug, performance regression, or unexplained failure | [Debugging](references/debugging.md) |

If a condition arises later, load its guidance then. Include the applicable guidance in the implementation and verification approach. Disclose unavailable guidance and its practical limits; reading this entrypoint alone does not establish that the complete workflow was followed.

## Establish the work

Read the supplied ticket or brief, relevant updates, acceptance criteria, dependencies, and linked decisions or experiments. State the ticket's name when working from a tracker. A clear direct request is also sufficient; do not require a specification, tracker, or another HolyCow skill.

Verify that prerequisites are actually available. A ready label or closed blocker is not proof that a needed contract, migration, or capability exists. Surface contradictions or missing decisions that affect implementation, with a recommendation and trade-off. Continue independent authorized work without inventing product behavior.

Implement the selected work or explicitly requested batch; do not consume an entire backlog by implication. For substantial changes, state a short implementation and verification approach grounded in the acceptance criteria. Reuse established decisions without requesting approval again.

## Inspect before editing

Check the current checkout, branch where applicable, and existing changes. Follow the user's repository workflow; do not create another checkout as an automatic prerequisite. Preserve unrelated edits and distinguish them from this task's changes.

Read relevant instructions, domain terms, decisions, immediate callers, exports, shared utilities, and existing tests before changing an interface. Inspect actual source after using navigation tools. For new work, use the established stack and conventions rather than introducing speculative structure.

Load technology-specific skills only where the affected work needs them or project instructions require them. Verify uncertain API or platform behavior against authoritative documentation. Prototype code is evidence for intent, not automatically production-ready implementation.

For stateful logic or an interface change, identify the caller's use, state ownership, and invariants before adding branches or layers. Prefer a data shape that expresses those rules without unnecessary machinery. Simplify within scope only after establishing why existing behavior exists; repeated workarounds may signal a mistaken model rather than another missing guard.

## Choose the smallest complete solution

Prefer the first option that satisfies the accepted behavior and project conventions:

1. Reuse an existing project helper, component, service, or pattern after checking its actual contract.
2. Use a standard-library or native platform capability when it fits; preserve established project components and their required behavior.
3. Use an appropriate installed dependency before adding another. Justify a new dependency by the capability needed, not convenience alone.
4. Write focused new code where those options fall short. Add wrappers, abstractions, configuration, and extension points only for a present requirement.

Optimize for a readable, complete change rather than a line-count target. Include affected callers, exports, configuration, and tests; a smaller patch that leaves them broken is incomplete. Preserve required validation, authorization, data integrity, accessibility, compatibility, and error handling when simplifying. An accepted requirement cannot be silently dropped to take a shorter route.

## Investigate failures when needed

Establish a signal for the reported symptom, distinguish plausible causes with evidence, and avoid repeated speculative patches. Feature work without such a failure does not need the debugging reference.

Honor diagnosis-only and no-edit boundaries. A diagnosis-only request does not authorize applying a fix. Report the supported cause or remaining uncertainty and the next useful action; implementation, change review, and delivery steps apply only to authorized changes.

## Implement in small verified steps

For behavior changes with meaningful automated coverage, use a focused red-green cycle: express the expected behavior at an agreed or established boundary, observe the relevant failure, then make the smallest change that satisfies it. Extend one behavior at a time. Respect project-specific testing requirements; do not create ceremonial tests for trivial reversible edits.

Tests should use independent expected outcomes and survive harmless internal refactoring. Prefer existing public boundaries and test conventions. Do not add an abstraction merely to make a test easy.

Keep changes within scope. Necessary preparatory changes should have a clear connection to the outcome; unrelated cleanup belongs elsewhere. Implement the real behavior required by the ticket, including consequential failure and recovery paths. Remove experiment-only shortcuts from any reused code.

For changes across repositories, honor interface compatibility and migration order, and verify the producer/consumer behavior at the relevant integration boundary. Do not substitute a mock result for a required real integration check.

Work directly unless delegation is requested or otherwise authorized by the user's workflow. Delegate only a bounded outcome that benefits from separate work; a small change needs no worker group. Use the chosen coordinator, including Herdr when available, within its execution constraints.

Give each worker the outcome and acceptance criteria, owned files or responsibilities, relevant source and skill references, current checkout state, dependencies, permitted actions, and stopping boundary. Carry accepted constraints and applicable project instructions without copying the whole conversation. Workers may inspect consequential dependencies beyond the supplied pointers. When sharing a checkout, tell workers to preserve others' changes and return shared-file conflicts to the coordinator. Further delegation needs explicit assignment.

Ask for a concise result with changed files, checks and outcomes, and unresolved limits. Reconcile returned work and verify affected integration boundaries before claiming completion. Reuse evidence for unchanged code; rerun checks invalidated by combined changes.

## Review and correct

Review the actual task changes, including staged, unstaged, and new files; do not rely on a commit-only diff that omits the work. Compare them with acceptance criteria, relevant repository standards, and the behavior of affected callers.

Read and follow the installed [hc-review instructions](../hc-review/SKILL.md), including its required supporting guidance, for this workflow. Self-review follows the same scope-selection guidance as a separate review. If unavailable, disclose that and perform a direct review; do not describe self-review as independent review.

Identify who owns the review-and-correction cycle: the existing board or coordinator, otherwise Build. Keep self-checks, but when that workflow already supplies independent review, hand off to it without launching another reviewer group. Follow Review's proportional coverage and correction boundary; workers and reviewers do not start their own retry loops. Honor existing review policy and do not silently change board settings.

Address substantiated blocking findings together within scope, investigate uncertain claims, and rerun checks affected by fixes. Apply the project's severity threshold; without one, distinguish required behavior and safety defects from optional suggestions. Do not change accepted behavior solely to satisfy a review suggestion. Pass the finding status, correction diff, and check results to the focused recheck. At the correction boundary, return unresolved blockers and the decision needed without claiming completion or starting another cycle.

## Verify and hand off

Before the final handoff, confirm that the applicable guidance above informed the checks, and address any missed verification. Confirm each acceptance criterion and applicable standing quality requirement using the appropriate evidence. Report failed, skipped, or unavailable checks explicitly and distinguish observed results from assumptions. Unverified critical behavior means the work remains incomplete or needs further validation.

Follow the user's existing authorization and repository policy for commits, pushes, pull requests, and other delivery actions. Stage only the task's changes and preserve unrelated work, including unrelated hunks in shared files. Ticket creation or a ready label alone does not authorize these actions.

When a PR is requested, read and follow the installed [hc-pr instructions](../hc-pr/SKILL.md) to prepare the description from the actual changes and verification evidence. If unavailable, disclose that and write the description directly using the repository's template, including the problem, resulting behavior, evidence limits, and merge risks. Build retains responsibility for authorized Git and PR delivery. Return the real PR link and actual check status. Do not treat queued CI as passing or local implementation as merged or deployed.

Update tracker state only within the authorized workflow and its definition of done. Verify writes and keep parent issues open unless their completion conditions are met and the update is authorized.

Finish with the outcome, relevant file or PR links, verification results, and any remaining blockers. For interrupted work, preserve the accepted scope, changed files and checkout state, exact checks and outcomes, active worker identities if any, and next unresolved action in the existing handoff location or conversation. On resume, reconcile that checkpoint with actual files and processes before continuing. Do not claim completion merely because code was written or one check passed.
