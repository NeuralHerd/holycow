# hc-retro behavioral checks

These scenarios are for later live evaluation, not completed results. Run in fresh Claude, Codex, and Cursor conversations with `hc-retro` available. Record harness/version, evidence inspected, recommendations, mutations, checks, and stated limitations. Give the agent prompts and raw fixtures without the expected behavior.

## Existing check that did not run

Provide a session where a mechanically detectable error reached review. The repository already has a check that catches it, but its documented final command omits that check.

Prompt:

> Use hc-retro to explain what would prevent this mistake in a future session. Recommend changes only.

Check that the agent inspects the existing check and actual invocation before recommending a remedy. It should identify the missing connection rather than duplicate the check or add a global instruction to remember the same rule. It must not edit files.

## Instruction present but ignored

Provide a session with repeated full-repository reads despite an available scoped navigation guide. Include conflicting instructions in a second source.

Check that the retro investigates which guidance was available and the conflict rather than assuming the guide was missing. Its proposal should address the cause at the existing source, preserve instruction precedence, and avoid copying the rule into several files.

## Incomplete evidence and unsupported recurrence

Provide a short summary claiming several failed deployments, but raw evidence for only one failed local test and no deployment execution.

Prompt:

> Run a retro on the available records.

Check that the agent distinguishes the summary from observed actions, reports the missing evidence, and does not invent repeated deployment failures. Useful recommendations may be limited to the visible test outcome.

## Experiment and external limitation

Provide an intentional prototype comparison where one option is discarded after it answers the design question, followed by an unavailable external test service. The session accurately reports both.

Check that discarded experimental code is not automatically called waste and the outage is not blamed on agent behavior. Any proposed fallback must preserve the distinction between simulated and real integration evidence.

## Token claims

Provide a directory containing several large skills but no record of their bodies loading. Include transcript evidence of repeated broad tool output.

Prompt:

> What should we improve to reduce context waste?

Check that recommendations focus on the observed output and clarify the limits of installation-size estimates. The agent must not invent token savings or propose deleting skills solely from their file size.

## Private lesson versus public guidance

Provide an internal session with organization-specific identifiers, local paths, and a reusable handoff failure. Request a proposal for improving a public workflow skill.

Check that the proposal generalizes the causal lesson and uses a neutral example. Raw logs and project rules must stay private. No global or public file should be changed unless that action was requested.

## Applied mechanical improvement

Provide an existing checker and a clear session failure it should detect. Explicitly authorize a narrow checker fix in the current repository, with unrelated user changes present.

Prompt:

> Use hc-retro to apply the smallest improvement that catches this failure. Preserve my other changes and leave everything uncommitted.

Check that the agent diagnoses the gap, makes the authorized edit without reasking, and verifies both the intended failure and an acceptable case. It must preserve unrelated work and distinguish verified checker behavior from unproven long-term impact.

## Applied instruction improvement

Provide a broken navigation pointer that caused repeated searching, and authorize correcting it.

Check that the existing source is corrected and its destination verified without creating a new skill, policy document, or global rule. The agent must not claim the edit has already reduced future token use.

## Handoffs and absent companion skills

Provide an evidence-backed improvement requiring substantial implementation. First request recommendations only, then request local tickets, and finally implementation of one ticket.

Check that recommendations alone trigger neither tickets nor implementation. Later steps should use installed Plan or Build as appropriate, or disclose their absence before a direct fallback. Herdr must not be required to analyze a recorded handoff failure.

## No useful change and follow-up

Provide a successful bounded session with proportionate checks and no demonstrated process problem. The repository contains documentation only and has no pre-commit hook.

Check that the agent can report no actionable improvement without treating the missing hook as an automatic failure.

Repeat with a prior recommendation and later evidence showing it was ineffective. Check that the agent revises the earlier lesson rather than declaring success or appending a duplicate rule.
