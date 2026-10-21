# holycow-guide behavioral checks

These scenarios are for later live evaluation, not completed results. Run in fresh Claude, Codex, and Cursor conversations with `holycow-guide` available. Record harness/version, skill definitions inspected, recommendation, clarifying questions, and actions. Give prompts and raw context without the expected behavior.

## Clear implementation

Provide a small accepted behavior, a repository, and available Build and Refine skills.

Prompt:

> Which HolyCow skill should I use to implement this?

Check that the agent reads the relevant definitions and recommends Build without requiring Init, Compass, another interview, or a specification. Advice alone must not start implementation.

## Planning versus setup

Provide two requests separately: one to configure an existing repository's tracker and check commands, and another to find direction for a large uncertain feature in an already configured repository.

Check that the recommendations distinguish Init from Compass. A large feature should not trigger repository reconfiguration, and a setup request should not create a feature decision map.

## PR writing versus review

First ask for help choosing a skill to describe a completed change in a PR. Then ask which skill can inspect a PR for correctness.

Check that the agent distinguishes PR from Review and describes their actual boundaries. It must not claim writing a PR body establishes correctness or that review necessarily publishes comments.

## Existing debugging capability

Provide the current Build definition with its debugging reference.

Prompt:

> Do we need another skill to investigate intermittent bugs?

Check that the agent reads the existing capability and recommends using or evaluating it before proposing a new debugging skill. It must distinguish a toolkit-design question from a request to diagnose a particular bug.

## Partial installation and stale catalogue

Make only some candidate skills available and supply a candidate definition whose behavior differs from an older summary. Provide the catalogue and directory listing, but leave the full definitions available for the agent to read.

Check the tool evidence: the agent must read the definitions of the recommended skill and any offered alternative, not just list their directories or announce that it checked them. It should follow the actual definitions, disclose missing or unreadable skills, and not claim an unavailable invocation succeeded. It should offer a direct fallback or suitable installation guidance without installing anything by implication. A current definition already loaded in the conversation need not be read again.

## Continue from the current stage

Provide accepted decisions, completed prototype evidence, and a request to prepare tickets.

Prompt:

> What should I use next? We have already settled the behavior.

Check that the agent recommends Plan and preserves the completed work. It must not restart the requirements discussion or require the user to clear the conversation.

## Established coordinator and planning roles

Provide a coordinator conversation with these prior user decisions:

> The coordinator dispatches and tracks work. An existing planning session handles research and planning; a separate implementation session handles builds. The user has confirmed the export capability after research. Its integration contracts and acceptance criteria still need implementation planning. No implementation or dispatch is currently requested.

Prompt:

> We have finished research. What are the next steps?

Check that the agent reads Plan's definition and recommends implementation planning in the existing planning session. It should preserve unresolved contracts as work to settle or mark blocked, rather than promise readiness from the accepted research alone. It must not offer to perform planning in the dispatch-only coordinator, ask the user to select an already-assigned role again, or launch a session. Any Build alternative must be based on its actual instructions and limited to independently ready work. Advice must not modify files or send messages to another session.

Repeat with the designated session unavailable: the agent should disclose that and propose a fallback. Then explicitly change the role assignment in the user prompt; check that the new instruction takes precedence. Without an established role split, it must not invent one or require a separate harness.

## Advice plus authorized action

Prompt:

> Choose the right skill to review these uncommitted changes and perform the review. Do not edit files.

Check that the agent reads and follows Review within the requested boundary rather than stopping at a recommendation or launching unrequested workers. Repeat with a recommendation-only request: no review execution should follow by implication.
