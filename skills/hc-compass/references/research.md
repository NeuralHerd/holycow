# Research coordination

Parallelism is for independent fact-finding that benefits from separate attention. Do not fan out speculative questions, duplicate work already done, or ask multiple agents to interview the user. Respect explicit limits on delegation and cost. Existing authorization remains valid; do not request approval for each researcher.

## Choose the available mechanism

1. Use the user's preferred coordinator when available. For Herdr, follow its installed skill and current CLI guidance; control it only inside a managed pane (`HERDR_ENV=1`). Do not control a focused Herdr session from outside it.
2. Otherwise use the harness's available native subagent tools. Report when a preferred coordinator is unavailable and identify the fallback. If the user required that coordinator exclusively, explain the limitation instead of substituting another.
3. If no permitted agent mechanism is available, say so and research sequentially. Do not install tools, create new user-facing chats, or launch extra harness processes as an automatic workaround.

This skill defines the coordination behavior, not a new agent runtime. Use the tools actually exposed in the session; do not assume equivalent commands across harnesses.

## Dispatch a bounded batch

Start with a small batch, normally two researchers, within the user's budget and available capacity. Send only ready, unclaimed questions without dependencies on each other's findings. Keep independent discussion moving if the user is available.

Record which question each researcher owns and its returned agent or pane identity. Give each researcher:

- The precise question and relevant accepted context.
- The sources or repositories to inspect and the boundary of the investigation.
- A read-only assignment: return evidence; do not change product files, the tracker, or the shared map.
- A request for concise findings, source references, uncertainty, and any newly exposed questions.

Do not pass the whole conversation or spawn additional agents recursively by default. The coordinating agent owns map and tracker updates.

## Collect and reconcile

Use the mechanism's status and wait tools to collect actual results. A successful launch or an idle pane does not establish that the research finished. On timeout or failure, inspect the existing worker before retrying so the same assignment is not launched twice.

Inspect decisive evidence, reconcile conflicting findings, and separate observations from recommendations. Missing access or failed research leaves a question waiting; successful independent results can still be recorded. Research cannot substitute for the user's product decisions.

Before marking a question resolved, verify that its answer still applies to the current assumptions and dependencies. If the user changes direction, revise or stop research you launched that is no longer relevant. Preserve pending worker identities and questions in checkpoints so resumed sessions do not duplicate running work.
