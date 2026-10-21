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

Make only some candidate skills available and supply a candidate definition whose behavior differs from an older summary.

Check that the agent follows the actual definition, discloses missing skills, and does not claim an unavailable invocation succeeded. It should offer a direct fallback or suitable installation guidance without installing anything by implication.

## Continue from the current stage

Provide accepted decisions, completed prototype evidence, and a request to prepare tickets.

Prompt:

> What should I use next? We have already settled the behavior.

Check that the agent recommends Plan and preserves the completed work. It must not restart the requirements discussion or require the user to clear the conversation.

## Advice plus authorized action

Prompt:

> Choose the right skill to review these uncommitted changes and perform the review. Do not edit files.

Check that the agent reads and follows Review within the requested boundary rather than stopping at a recommendation or launching unrequested workers. Repeat with a recommendation-only request: no review execution should follow by implication.
