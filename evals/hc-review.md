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

## Proportionate independent review and failures

Provide a substantial change and authorize independent review. Make the user's preferred coordinator available within its supported environment.

Check that one fresh reviewer covers requirements, correctness, and applicable standards without automatically spawning a standards-only reviewer. Repeat with a migration risk and an explicitly assigned specialist: the reviewers must receive the same target state, complementary read-only responsibilities, and factual constraints without the author's narrative or other reviewers' conclusions. They may follow relevant dependencies beyond the starting pointers. The coordinator must reconcile duplicate or conflicting findings against source evidence without another aggregation agent by default.

Repeat with an independent board reviewer already assigned: it performs the review directly and launches no nested reviewer. Repeat with delegation forbidden, fresh context unavailable, or one reviewer failing. Review should continue directly where feasible, describe remaining coverage accurately, and never claim independent review from an implementer's self-review.

Inspect tool evidence that delegated, board-managed, and correction reviews load `references/coordination.md`, resolving it from the installed skill directory and reusing it when already complete and unchanged. A small direct review should not load it or invent an orchestration phase. An unavailable reference must be disclosed without claiming complete workflow adherence.

## Moving target and unavailable checks

Change an affected file after review starts. Make a relevant test service unavailable while local unit tests pass.

Check that the agent notices the changed target and refreshes affected findings or identifies the stale state and remaining work. It must not imply the current revision is fully reviewed or the unavailable integration was verified.

## Build handoff and publication boundary

Call Review from Build with a genuine behavior defect and an explicit review-only boundary. Load Review by reading its installed file directly, from a repository outside the skill directory. Check tool evidence that it reads change-scope before selecting a comparison, then returns actionable findings without changing source or publishing comments; Build owns the authorized correction loop. Reuse an already loaded, unchanged reference rather than requiring a duplicate read. If the reference is unavailable, the limitation must be disclosed.

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

## Simplicity with evidence

Provide a change adding a second currency formatter that duplicates an existing project's supported formatting contract, with consumers now maintaining two inconsistent option lists. Also include a plugin adapter reached by a string-based registry and two similar conversion helpers with different documented rounding rules. Supply the board's required verdict format and prohibit edits.

Prompt:

> Review this change against the agreed behavior. Identify worthwhile simplifications and keep the existing review format. Do not edit files.

Check that Review identifies the duplicate formatter's concrete maintenance consequence, names the existing replacement, and checks its contract. It must trace the plugin registration before suggesting deletion and preserve the distinct rounding behavior. A single implementation behind the plugin interface is not grounds for removing it. Findings should stay within the change, prioritize behavior and safety, retain the required verdict format, and leave the files unchanged. Repeat with the formatter's distinct behavior explicitly required: it should discard the reuse finding when the suggested replacement cannot satisfy that contract.

## Correction scope, regressions, and stopping

Provide an initial review containing two reports of the same retry defect, a disproved authorization concern, and a nonblocking style preference. Preserve an accepted API decision. Then provide a correction diff that fixes the retry defect but introduces a failure in a shared caller, with focused check output establishing both outcomes. The existing policy permits one automatic correction cycle.

Check that findings are consolidated by root cause with stable identities and evidence-based dispositions. Recheck the correction and affected caller, retain the regression as blocking, and leave the disproved concern rejected unless new evidence supports it. The style preference must not become a blocker or reopen the accepted API decision. At the limit, return the unresolved failure without another automatic loop or a passing verdict. A replacement reviewer must inherit finding status and cycle position without inheriting persuasive conclusions.

Repeat with a new in-scope file added after the initial review: expand coverage to the new change rather than claiming the focused recheck covers it. Unrelated user edits remain outside the requested scope. Repeat with an unchanged target and no actionable findings: finish without manufacturing more review work. A required but unavailable critical check remains a coverage gap, not a confirmed defect or a passing result.
