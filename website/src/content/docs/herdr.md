# Using HolyCow in Herdr

HolyCow works without Herdr. Herdr adds a place to coordinate agents; the skills provide guidance for the work those agents do.

## Explicit use is the default

Install the skills for each agent you use. Invoke a skill by name in its chat, or give a coordinator a clear handoff that names the skill and the task.

For example:

```text
Use hc-compass to map the open decisions for this feature.
The repository context is docs/agents/holycow.md.
Reuse the existing map and accepted decisions.
```

Installation alone does not enable automatic HolyCow selection. The package keeps implicit invocation disabled across supported agents.

## Opt in through Herdr role instructions

If you want automatic selection only inside Herdr, add that preference to your Herdr role instructions. Keep the installed skill definitions unchanged so the preference does not spread to unrelated agent sessions.

Adapt this starting point to your setup:

```text
For work coordinated through Herdr, select the smallest useful HolyCow skill.
Use holycow-guide when the next step is unclear.
Read the selected SKILL.md and its applicable references before the work
they govern. Resolve references relative to the installed skill directory.
Reuse complete, unchanged guidance already read in this session.
Report missing or truncated guidance and retrieve needed sections.
Respect the user's task scope, authorization, and repository instructions.
```

Use instructions appropriate to each role:

| Role | Useful guidance |
| --- | --- |
| Coordinator | Choose the workflow and include the selected skill, repository, context pointers, accepted decisions, and current stage in handoffs. |
| Research agent | Use Compass for a continuing decision map, Refine for discussion, and Lab for an authorized experiment. |
| Planning agent | Use Plan to turn accepted understanding into deliverable work. |
| Implementation agent | Use Build and its applicable verification, debugging, and production references. Follow Review for self-review. |
| Reviewer | Use Review for implementation changes; use Plan when evaluating a delivery plan. |

Managed role instructions may not reach an ordinary pane launched manually. Include the instructions in that pane's handoff and verify what the agent actually read.

## Check that it worked

Look for tool evidence that the agent read the selected skill and the references relevant to its task. Then compare its actions and result with that guidance. A mention of a skill name, an installed directory, or a statement that it was loaded is not proof of compliance.

For example, a Build session changing persistent state should read the applicable production guidance before designing the change, choose meaningful checks using the verification reference, and establish the actual scope when reviewing its work.

Use the [evaluation scenarios](../../../../evals/invocation.md) to make these checks repeatable. They describe expected behavior, not a claim that a particular session passed.

## Updating an ongoing session

An installation update changes files on disk. An agent may still have older instructions in its conversation. Ask it to re-read the changed skill and applicable references, or start a fresh session with a concise handoff.

See [installation and updates](../../../../README.md#update) for the package commands. Automatic selection does not itself authorize delegation, worktrees, tracker writes, commits, pushes, or deployment.
