---
name: hc-review
description: Use when the user asks to review a pull request, branch, commit, or work-in-progress changes for correctness, agreed requirements, and project standards.
license: MIT
disable-model-invocation: true
---

# hc-review

Find actionable problems in the requested changes and explain the evidence and impact. Keep requirements, correctness, and project standards visible so success in one cannot conceal a problem in another.

In a repository, use the HolyCow context linked by its instructions, or `docs/agents/holycow.md` when present. Read only relevant sections and reuse context already loaded. Continue without it; recorded capabilities may need rechecking in this session.

## Establish the review scope

Identify the requested PR, revision range, staged changes, or local work. Before selecting a Git comparison, read [change scope](references/change-scope.md), resolving the path from this skill's directory. This applies equally to standalone review and Build's self-review, including when the skill is read directly. Reuse complete, unchanged guidance already read in this session; disclose an unavailable reference and the resulting scope-verification limits. Include relevant new files when reviewing work in progress; a commit-only diff is insufficient.

Batch applicable guidance with independent reads of the supplied contract, known source entry points, and checkout status. Once the comparison is established, gather the diff and known affected source together. Discover missing paths selectively; do not repeat repository orientation when the target is already known. Bound output and retrieve any omitted evidence before relying on it. Keep dependent decisions and checks sequential.

Record the baseline, target revision or local state, and included paths. Use the supplied target or reliably established workflow context; ask only when ambiguity materially changes the review. An invalid ref must be resolved before reviewing that comparison, not silently replaced.

Preserve existing changes and distinguish the task from unrelated edits. Read relevant surrounding code and affected callers, not just isolated diff hunks. Changes outside the selected scope may explain a defect but must not silently become the subject of the review.

Review alone does not authorize source edits, commits, tracker changes, or published comments. Follow any existing authorization for fixes or publication without asking again. When called from Build, return findings for its correction loop.

## Establish intent and standards

Use the user's accepted behavior, supplied ticket or brief, relevant issue updates, and linked decisions or experiments. Read source material rather than treating titles or an implementation summary as requirements. Resolve material contradictions with a recommendation; do not invent acceptance criteria or overrule an accepted decision with an older document.

A formal specification, tracker, and other HolyCow skills are optional. If intent is unavailable, continue correctness and standards review while reporting the requirements limitation. Do not call speculative product preferences missing requirements.

Read applicable repository and directory instructions, including relevant coding standards and contribution guidance. Follow documented project conventions over generic preferences. Load domain or technology guidance only for the affected work or when required by the project. Verify uncertain external contracts against authoritative sources.

## Examine the change

- **Requirements:** Check accepted outcomes, scope boundaries, and consequential failure or recovery behavior. Identify omissions, partial behavior, or changes that contradict the agreed outcome. Prototype shortcuts and simulated results do not establish production behavior.
- **Correctness:** Trace affected callers, state transitions, and error paths. Examine concurrency, authorization boundaries, compatibility, migrations, or resource handling where the change reaches them. Check whether tests assert meaningful outcomes and whether integration evidence covers the actual contract.
- **Project standards:** Cite the applicable rule for a violation. Distinguish documented requirements from design suggestions. A code smell alone is not an actionable defect; explain a concrete maintenance consequence before recommending a change.

Within the requested change, examine unused options, speculative extension points, wrappers that only forward calls, duplicated behavior, and dependencies whose job an existing project facility or platform capability already fulfills. Name the reusable implementation or simpler alternative and verify that it preserves the required contract. Before recommending deletion, check callers, tests, configuration, and runtime or string-based references; a symbol search alone cannot establish that code is unused.

Report unnecessary complexity only with a concrete maintenance or behavioral consequence. One implementation behind an interface, a longer function, or fewer lines in an alternative is not by itself a defect. Judge correctness, safety, and required behavior before size; keep accepted design decisions and the project's review format intact. Do not turn a focused review into a cleanup audit.

Inspect the implementation directly even when tests pass. Use existing tooling for mechanical checks rather than manually enumerating formatting or lint issues. Report a material failing check once, with its scope and result, without flooding the review with duplicate diagnostics.

Follow consequential dependencies beyond symbol callers: persisted or serialized data, runtime-loaded code, background jobs, configuration, and downstream consumers. Identify the pivotal assumption a safety claim relies on and seek a focused check against the real boundary and dependency version. Label source-only reasoning and unavailable runtime evidence accurately.

Where affected, check resource or tenant isolation, retry and interruption behavior, operator-visible failures, and migration recovery. For structural changes, verify behavior is preserved before recommending deletion or new abstractions. Keep concerns tied to a concrete path and consequence; do not expand every review into a system-wide audit.

Inspect changes to tests, check configuration, budgets, and suppressions. A removed assertion or relaxed gate needs an accepted behavior or policy reason; a green result after weakening the check does not establish the original requirement.

## Coordinate independent review and corrections

Keep small, clear changes direct while preserving required project reviews. For substantial work with authorized delegation, start with one independent reviewer covering requirements, correctness, and standards. Add specialists only for distinct consequential risks or an explicit request. An existing board reviewer counts; do not recursively delegate.

Before delegated review, board-managed handoffs, or review corrections, read [review coordination](references/coordination.md). Reuse complete, unchanged guidance already loaded; disclose an unavailable reference and the resulting limits. Simple direct reviews need no coordination workflow.

Without authorized delegation or fresh-context support, perform the perspectives directly and describe the limitation. Complete failed reviewer coverage directly when feasible. Do not describe self-review as independent review, or reviewer agreement as proof.

## Validate candidate findings

For each candidate, establish the trigger, affected behavior, and connection to the reviewed change. Inspect the actual code and relevant requirement or rule. Use focused checks or a reproducer when useful and available within the task's execution permissions; report what ran and what remains unverified.

Distinguish a newly introduced problem from an existing defect. For change reviews, include existing defects only when the change makes them consequential, explaining that connection. A separately requested broader audit may cover more.

Reconcile reviewer disagreements against evidence, deduplicate the same root cause, and discard unsupported claims. A test-coverage gap should name the important behavior left unverified; it is not proof that the implementation is broken. Keep unresolved questions separate from confirmed findings.

## Report and hand back

Lead with actionable findings, ordered by impact. For each, provide:

- A concise title and severity, using the project's scale or P0 urgent, P1 high, P2 normal, P3 low. Judge severity from demonstrated impact and realistic conditions.
- The affected file and narrow line location in the reviewed version, plus a requirement or rule reference when relevant.
- The trigger, consequence, evidence, and smallest useful correction direction. Label design suggestions and assumptions explicitly.

Preserve each finding's perspective when consolidating reports. Briefly state coverage of requirements, correctness, and standards; checks run; and material limitations. If there are no actionable findings, say so within the reviewed scope without implying that tests ran or the change is proven correct.

Recheck the target before handing off. When running final read-only checks, collect the post-check target identity in the same tool execution after the checks finish, including when a check fails; preserve each result separately. If the target changed, inspect affected changes and refresh findings or identify the older state and remaining review. After authorized fixes, revalidate affected findings and checks; changed code alone does not establish resolution.

Return findings to Build or the current conversation. If publication was requested, use the actual target and supported review format, verify submission, and link the result. Review completion is separate from CI, approval, merge, and deployment.
