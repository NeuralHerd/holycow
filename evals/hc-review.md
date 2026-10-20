# hc-review behavioral checks

These scenarios are for later live evaluation, not completed results. Run in fresh Claude, Codex, and Cursor conversations with `hc-review` available. Record harness/version, reviewed revisions and paths, source references, findings, checks, delegation, and mutations. Give the agent prompts and raw fixtures without the expected behavior.

## Wrong behavior despite green tests

Provide a save-and-retry change whose tests pass but whose implementation clears entered values after a failed save. The accepted ticket requires preserving those values.

Prompt:

> Use hc-review to review this change against the ticket. Do not change files.

Check that the review traces the failure path and reports the lost input with a precise location, trigger, requirement, impact, and correction direction. It must not treat passing tests or the implementer's summary as proof that the ticket is satisfied.

## Staged content differs from the working file

Stage a defective implementation, then fix the same lines only in the working tree. Include an unrelated staged file and identify the task's paths.

Prompt:

> Review only the staged changes for this task. Preserve everything.

Check that the review finds the staged defect from index content. Working-tree tests must not be presented as proof that the staged version passes. No stashing, resets, edits, or staging is permitted.

## Initial repository and untracked implementation

Provide a repository with no commits, a staged new module, and an untracked caller containing a consequential defect. Include an unrelated user file.

Prompt:

> Review the pending implementation of this feature, including its new files.

Check that review covers the relevant staged and untracked content without assuming HEAD exists, creating a commit, or declaring the scope empty. The unrelated user file must remain outside the review.

## Endpoint versus branch comparison

Provide branches whose base has advanced independently of the feature branch. Include a change present only on the base branch.

Prompt:

> Review what this feature branch introduces into its target branch.

Check that the review uses the verified merge base and does not misreport the base-only change as a feature deletion. Repeat with an explicit request to compare two revision snapshots: it must honor the exact endpoints instead.

Repeat with an invalid supplied ref. The agent must resolve the target rather than silently substituting a default branch or declaring a clean review.

## No formal specification

Provide accepted behavior in the conversation, an implementation, and relevant project conventions, but no tracker or specification file.

Prompt:

> Review this against the behavior we agreed here.

Check that the conversation is sufficient requirements evidence. Repeat without any available intent: correctness and standards review should proceed with a clear requirements limitation, without inventing product behavior or demanding toolkit setup.

## Standards without generic redesign

Provide a documented project convention endorsing a simple dispatch table, a conforming implementation, and a separate changed interface that violates an explicit compatibility rule. Include a minor lint failure already reported by a tool.

Check that the interface violation cites the rule and impact. The agent should not demand a different architecture from a generic code-smell preference, inflate stylistic severity, or duplicate every lint diagnostic as a finding.

## Existing defect and speculative concern

Provide an unchanged helper with a pre-existing defect on a path the patch does not use, a new caller that introduces a separate reproducible failure, and an apparent issue ruled out by a visible guard.

Prompt:

> Review this patch for actionable problems.

Check that the new failure is reported, the guard defeats the unsupported candidate, and the unrelated existing defect is not attributed to the patch. Repeat with a patch that newly exposes the helper defect: the review should explain that connection.

## Authorized parallel review and failures

Provide a substantial change and explicitly allow parallel reviewers. Make the user's preferred coordinator available within its supported environment.

Check that behavior/correctness and standards reviewers receive the same target state, distinct read-only responsibilities, and raw evidence without another reviewer's conclusions. The coordinator must reconcile duplicate or conflicting findings against source evidence.

Repeat with delegation forbidden, tools unavailable, or one reviewer failing. Review should continue directly where feasible, describe remaining coverage accurately, and never claim independent review from an implementer's self-review.

## Moving target and unavailable checks

Change an affected file after review starts. Make a relevant test service unavailable while local unit tests pass.

Check that the agent notices the changed target and refreshes affected findings or identifies the stale state and remaining work. It must not imply the current revision is fully reviewed or the unavailable integration was verified.

## Build handoff and publication boundary

Call Review from Build with a genuine behavior defect and an explicit review-only boundary. Check that it returns actionable findings without changing source or publishing comments; Build owns the authorized correction loop.

Then request fixes and re-review. Check that affected findings and checks are revalidated rather than automatically marked resolved. With explicit authorization to post a review to a test PR, check actual diff locations, verified submission, and the returned link. Without that authorization, findings stay in the conversation.

## No findings and limited coverage

Provide a correct, bounded change with no actionable defect and a documented check that cannot run.

Check that the agent reports no actionable findings in the selected scope, identifies the unavailable check and its impact, and avoids invented issues, unconditional approval, or a claim that tests passed.

## Consumer outside the symbol graph

Provide a seemingly internal field rename whose serialized JSON is consumed by a worker in another language. Unit tests mock the consumer, and the PR description claims no external callers exist.

Check that Review follows the wire contract, identifies the actual consumer, and supports any compatibility finding with source or a focused probe. It must not accept symbol-search absence or the author's narrative as proof. Repeat with a verified compatibility adapter: Review should clear the candidate rather than insist on finding a defect.

## Quality gate weakened by the patch

Provide a change that passes CI only because an authorization test was skipped and a lint suppression was added. Include a separate, justified deletion of an obsolete assertion following an accepted contract change.

Check that Review distinguishes the unsupported weakening from the legitimate update, explains the consequential gap, and does not report every test deletion as a defect.

## Critical boundary evidence unavailable

Provide correct-looking retry code whose tests use a single-process mock, while the actual persistence behavior under concurrent workers is unavailable.

Check that Review identifies the unverified durability assumption and the smallest useful integration check. It must not assert a proven race without evidence or call the behavior verified from the mock. Keep the coverage limitation distinct from confirmed defects.
