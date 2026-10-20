# UI experiments

Put the experiment in realistic context. In an existing app, use its relevant page or flow, components, layout, and representative data. Preserve authentication and data-loading behavior. Keep the original rendering as the default; expose variants through the project's local preview mechanism or an explicit development-only switch. Do not make experiments reachable in production.

If there is no suitable host, use a clearly marked experiment route following the project's conventions. For a new idea without an app, a small standalone page can be sufficient.

When comparing alternatives, start with two or three meaningfully different structures or interactions. Use the same content, tasks, and comparable starting state so cosmetic differences do not obscure the actual choice. Add variants only when they answer another unresolved question.

Provide a simple, labelled switcher. A query parameter can make variants easy to revisit where the router supports it; preserve unrelated parameters. Keep experiment controls visually separate from the design being judged. Do not intercept typing or normal keyboard navigation.

Make the relevant interactions work. Use representative long, empty, or dense content when it could change the decision, and check the viewport sizes relevant to the request. Stub mutations and label behavior the experiment does not implement.

Open and exercise the actual preview using available browser tools. If those tools are unavailable, disclose what could be checked and give the user precise manual steps.

Ask for feedback on the question, not just which screen looks nicest. A combined variant may incorporate parts of several options. Preserve the accepted rationale and show the revised result before calling the choice settled.
