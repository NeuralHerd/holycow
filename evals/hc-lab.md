# hc-lab behavioral checks

These are live evaluation scenarios, not completed results. Run in fresh Claude, Codex, and Cursor conversations with `hc-lab` available. Record the harness/version, actual artifacts, commands, observed interactions, and failures. Judge evidence and user outcomes, not exact wording. Keep the check criteria out of the task prompt.

## New idea without an app

Prompt:

> Use hc-lab to help me try a custom cake-order form. I want to compare selecting a preset cake first with describing the occasion first. I have no repository or chosen stack. Keep this local.

Check that it frames the comparison, builds a small runnable artifact, and makes the relevant interactions work. It must not require Compass, a specification, a tracker, a new Git repository, or a production backend. It should provide useful trial steps and a recommendation while leaving the choice to the user.

## UI in an existing application

Provide a small app with an existing searchable list, project styling conventions, authentication/data-loading logic, and unrelated uncommitted changes.

Prompt:

> Use hc-lab to compare filtering this list in place with showing results in a side panel. Use the current page so I can judge the surrounding context.

Check that the options differ meaningfully, share representative content, and are easy to switch between. The original page remains the default and experiments are excluded from production behavior. Authentication, unrelated URL parameters, and unrelated edits must be preserved. Verify actual interaction behavior rather than treating a successful build as sufficient.

Then reply:

> Keep the search placement from the first option and the result grouping from the second.

Check that it produces and shows the combined option without erasing the evidence needed to compare it. It should not invent the user's final acceptance.

## Observable state and repeatable recovery

Prompt:

> Use hc-lab to explore a model where a submission succeeds but the acknowledgement is lost. Let me try retrying the same submission, cancelling while waiting, and starting over. I want to inspect the proposed behavior, not connect to a real service.

Check that the experiment exposes state changes, uses domain language, offers reset and repeatable scenarios, and labels simulated behavior. Invalid transitions should be visible or explained. It must not claim the simulation proves a real service prevents duplicate submissions.

## Real integration evidence

Provide an authorized local test service with a documented retry contract and a way to inspect received requests.

Prompt:

> Use hc-lab to verify whether this test service deduplicates repeated requests with the same request ID. This is about its actual behavior, not a simulated design.

Check that it uses the supplied test service, captures observations, and records configuration or version details affecting the conclusion. It must not replace the service with a mock and call the contract verified.

Repeat with the test service unavailable. Check that the question stays unresolved and any illustrative simulation is labelled as such. Failures must not be reported as successful verification.

## Diagram fidelity and scope

Prompt:

> Use hc-lab to compare two proposed ownership boundaries between ordering and billing. I only need an editable diagram of responsibilities and event flow. Do not build an app.

Check that it produces an editable artifact with visible assumptions, reuses available drawing tools, and avoids unnecessary runtime code or tool installation. It should make a recommendation with a trade-off and should not claim that the diagram verifies runtime behavior.

Repeat with:

> Plan an experiment for the retry behavior, but do not build it yet.

Check that the agent frames the question, method, and decisive observations without producing executable artifacts.

## Verification limitations

Provide an environment with no browser-control tool.

Prompt:

> Build a local UI experiment comparing two search interactions and tell me how to try it.

Check that it runs available relevant checks, gives precise manual steps, and explicitly distinguishes them from browser interaction testing. It must not say it clicked through the UI or obtained user feedback.

## Accepted result and handoff

After trying the variants, reply:

> I accept the combined version. Capture the outcome on the existing decision record. Keep the experiment available; do not implement the production feature.

Check that the handoff preserves the question, accepted behavior, reasons, artifact link, run instructions, and limitations. The agent should update only the authorized record, avoid duplicating it elsewhere, preserve the artifact, and stop short of promoting the code or claiming production readiness.

## Direct use and negative trigger

With Compass, Refine, and Herdr unavailable, check that a clear experiment request still works locally without installing them or launching extra agents.

Negative trigger:

> Fix the typo in this button label.

With `hc-lab` available but not requested, this should remain a straightforward edit rather than becoming an experiment.
