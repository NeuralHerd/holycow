# Behavior experiments

Choose the execution environment according to the evidence needed.

## Exploring a model

For state transitions, business rules, or data relationships, prefer a small interactive simulation. A standalone HTML file is useful for non-developers; a terminal interface can fit technical users. Use the existing project environment when that makes the experiment more faithful or easier to run.

Keep the logic separate from presentation without adding a generic framework. Show relevant state after each action, what changed, and why a requested action is allowed or rejected. Use domain language, with technical details available only when they help the question.

Provide free exploration, a reset, and a few repeatable scenarios: the ordinary path, a consequential edge case, and an invalid action when relevant. Start guided scenarios from known state. Simulate time, retries, or failures explicitly so the user can reproduce them without waiting or guessing.

A simulation explores the proposed rules. It does not prove that a database, queue, network, or third-party service behaves that way.

## Testing a real capability

When the question depends on an API contract, runtime, persistence, or concurrency guarantee, use the relevant implementation in an authorized test environment. Keep the exercise narrow, record the version and configuration that affect the finding, and capture actual observations.

If the required environment or access is unavailable, report the unanswered question. A fixture can still illustrate an idea, but cannot replace the missing verification.

## Validate the evidence

Exercise the decisive scenarios, including failure or recovery when that is the uncertainty. Focused automated checks are appropriate when they make a claimed invariant reproducible; avoid a broad production test suite for an isolated demo unless the project requires it.

Distinguish an execution error in the experiment from a failure of the proposed model. Fix the former before interpreting the latter. Present observed behavior and a recommendation, then let the user judge whether the behavior meets their needs.
