# Production concerns

Use only the sections relevant to the affected behavior. Follow the project's accepted requirements and service-specific guidance; do not add a new platform, telemetry stack, or release process to satisfy this reference.

## Access and data boundaries

Identify the acting user or service, the protected resource, and where externally controlled data enters. Consider the relevant misuse alongside the intended flow: another tenant's identifier, a forged callback, or an untrusted value reaching a privileged operation. Verify authorization at the resource boundary, not merely that the caller is signed in.

Use the project's validation and secret-handling mechanisms. Check that errors, responses, fixtures, logs, and traces do not expose protected data. Exercise a relevant rejection case as well as authorized behavior. Do not assume a successful happy path establishes isolation.

## Retries and partial failure

For commands, webhooks, queues, or background work, identify what happens after duplicate delivery, timeout, partial persistence, or process restart where applicable. State the invariant, who owns durable state, and which operation makes an external effect safe to repeat.

Test the consequential interruption or replay at the actual boundary. A unique key in a mock or an in-memory flag does not establish durable idempotency across concurrent workers or restarts. Distinguish the model a test explores from the service guarantees verified.

## Operational evidence

Name the operator question that matters, such as how to distinguish a delayed job from a permanently failed one. Reuse appropriate logs, metrics, or traces and existing correlation conventions. Verify that the relevant success or failure produces the expected signal; adding a logging call alone does not establish visibility.

Keep fields safe and metric labels bounded. Use accepted service objectives or measured baselines for performance claims, and state the measurement conditions. Do not invent numerical release gates.

## Compatibility and recovery

For deployments, configuration, or migrations, identify affected consumers, required ordering, and the recovery action. Explain effects a code revert cannot undo, including persisted data changes or external messages. Check old/new compatibility when versions can coexist.

Use the project's rollout and recovery conventions. If a feature flag is warranted, verify the relevant states and record ownership and removal conditions. Do not introduce a flag or staged rollout for every change.

Validate infrastructure through the project's appropriate static checks, synthesis, or plan where available. Label exactly what that establishes; a plan is not an applied deployment or a recovery rehearsal. Deployment, data changes, and live recovery exercises require corresponding authorization.
