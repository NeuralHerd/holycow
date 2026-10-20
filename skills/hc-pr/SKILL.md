---
name: hc-pr
description: Use when writing or updating a pull request description from the actual changes, verification evidence, and merge risks.
license: MIT
disable-model-invocation: true
---

# hc-pr

Help a reviewer understand what changes, why it matters, what establishes that it works, and what merging could affect. Keep the description proportional to the change.

In a repository, use the HolyCow context linked by its instructions, or `docs/agents/holycow.md` when present. Read only relevant sections and reuse context already loaded. Continue without it; recorded capabilities may need rechecking in this session.

## Ground the description

Identify the requested PR or proposed change and its baseline and target. Read the relevant diff, surrounding code, accepted requirements, and verification results. For an existing PR, use its actual revisions rather than assuming the local checkout matches.

Separate pending local work from changes already included in the PR. Evidence from Build can be reused when it still applies to the selected version. If the user wants a draft before implementation, label it provisional and distinguish intended behavior from completed work.

Read the applicable repository instructions, PR template, and existing description. Preserve relevant human-authored context and reconcile outdated claims. Use established domain language and real issue or dependency links; do not invent identifiers or add closing keywords without the intended workflow supporting closure.

## Explain the change

Follow the repository template and fit the following concepts into its existing sections. Without a template, use **Summary**, **Evidence**, and **Merge risk**. A small change needs only brief entries.

Lead with the concrete problem and resulting behavior. Describe the final scope for a reviewer who has not seen the conversation. Include rationale or alternatives only when they explain a material decision. If a title is requested, make it describe the same outcome.

Use the smallest representation that makes the change clear:

- Brief prose for a straightforward change.
- A focused before/after sketch or pseudocode for changed logic.
- A call, component, or file tree when ownership or structure matters.
- Mermaid when relationships or sequence are easier to understand visually.

Keep visuals consistent with the implementation and supported by the destination. Put them beside the explanation they support. Do not turn a small PR into an architecture document or present illustrative pseudocode as an executed test.

## Show observed evidence

Use real before/after evidence when available: screenshots for visible behavior, or relevant test and execution results for functional changes. If the before state was not observed, say so or describe the previous behavior as an inference from code. Never invent a screenshot, failing run, command result, or successful check.

Identify what was checked, its outcome, and material limits. Keep passed, failed, skipped, and pending checks distinct. Evidence from an older revision must not silently certify newer changes; identify what remains unverified. Reuse applicable results rather than rerunning checks solely to populate the description.

Use links or attachments reviewers can access in the intended destination. A local filesystem path is not a published screenshot. Exclude sensitive data from evidence and keep private references within their intended audience. Report unavailable artifacts rather than pretending they are attached.

## Explain merge risk

Describe reversibility and affected scope in concrete terms. State whether reverting the code restores behavior and identify consequences it would not undo, such as deleted data, emitted events, or external side effects. Do not equate a reversible Git commit with a reversible system change.

Mention affected consumers, interfaces, data, or workflows where relevant. For migrations or changes across repositories, include known compatibility constraints, rollout order, and dependency links. Keep unverified assumptions visible rather than promising a safe rollback.

Scale this explanation to the change. A text correction can have a short risk statement; a destructive migration needs its actual recovery limitations.

## Return or publish the description

Return the requested title or body without a recap of how it was written. When called from Build, return the content for Build's delivery workflow. This skill does not replace implementation or code review.

Drafting alone does not imply publication. Follow existing authorization to create or update a PR without asking again. When publishing directly, verify the repository and PR target, re-read an existing body before replacing it to preserve concurrent edits, and verify the resulting content and link. If the write outcome is uncertain, inspect the target before retrying.

Report draft versus published status accurately. Writing a description does not establish that CI passed, review was approved, or the change was merged or deployed.
