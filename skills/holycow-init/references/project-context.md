# Project context

Keep the context small enough to navigate. It records where authoritative information lives and how this project works; it does not replace that information or grant execution permissions.

## Location and discovery

Use the context location already linked by applicable repository instructions. Otherwise use `docs/agents/holycow.md` under the selected project root. Do not create a second profile when an existing context or guide already serves this purpose.

Each HolyCow workflow skill reads the linked context, or the default path when present, and uses only relevant sections. Absence of the profile does not require initialization. Existing instructions and the user's current request still apply; surface material conflicts rather than silently promoting a profile value over them.

Prefer repository-relative references and meaningful links. Resolve Markdown links relative to the context file and verify their targets. For multiple repositories, identify logical names and documented relationships; put personal checkout paths in an existing private local record or the current session.

Reuse a short pointer in the actual instruction entry files used by the requested harnesses. The pointer should identify the context location and say to read relevant sections. Preserve existing scope and unrelated rules. Do not assume editing `CLAUDE.md` makes a pointer visible to Codex or Cursor; inspect their actual discovery path or rely on the shared default path used by HolyCow skills.

## Content to include when relevant

| Area | Useful information |
| --- | --- |
| Project boundaries | Components and repositories in scope, their responsibilities, and links to the existing architecture or workspace guide. |
| Work tracking | Selected tracker and project or repository identity, available access method, existing issue and dependency conventions, and canonical planning location. |
| Domain and decisions | Pointers to the existing knowledgebase, glossary, ADRs, standards, and relevant context indexes. Planned locations are labelled as planned. |
| Commands | Exact command, working directory, purpose, prerequisites, and source in project scripts or CI. Distinguish routine checks from operations with external effects. |
| Quality requirements | Links to the project's definition of done, CI gates, security and accessibility requirements, performance budgets, and documented exceptions where they exist. Distinguish enforced checks from aspirations. |
| Delivery | Existing branch, commit, PR, and issue-completion conventions; link templates and policy rather than duplicating them. |
| Coordination and expertise | Preferred coordinator, supported fallback, relevant technology skills, and when they are needed. Runtime availability and delegation authorization are checked in the active session. |

Omit irrelevant categories instead of creating empty sections. Record unresolved consequential choices as unresolved. A documentation-only project need not acquire a test framework, and a new project need not acquire a tracker.

Reuse existing quality requirements rather than creating a competing checklist or mandatory `CONSTRAINTS.md`. If a consequential requirement is missing, recommend a measurable check and where it belongs. A measured baseline is evidence for a proposed budget, not automatic agreement to enforce it. Do not import arbitrary coverage percentages, latency targets, or rollout thresholds.

## Tracker conventions

Existing tracking documentation is authoritative when still applicable. Identify the actual target before proposing operations. Record supported issue types, states, ownership, hierarchy, and blocking relationships only from reliable evidence or explicit user decisions.

Check connected-tool or CLI capabilities in the current environment; do not paste a generic provider command catalogue and assume it works. Native dependencies are preferable where supported. Explicit linked blocker lists can represent dependencies where native support is absent.

If no tracker is selected, reuse local planning conventions. With none, Compass and Plan already provide `.hc/compass/` and `.hc/plan/` defaults; link their intended roles without creating empty plans. Never treat unavailable remote access as permission to switch the canonical tracker.

Read-only setup can establish the target exists or a capability is advertised. Record write verification as outstanding unless an authorized operation actually demonstrates it. Do not create labels, sample tickets, or comments solely as a connectivity test.

## Shared facts and verification results

Keep durable conventions in the profile. Put transient facts such as a tool being unavailable in this session, an access failure, or a check result in the setup report with its scope.

Use precise descriptions such as “command located in the package scripts; not run,” “project metadata read successfully in this harness,” or “dependency writes unverified.” Avoid a blanket “configured” or “ready” label that hides missing capabilities.

Shared context must respect the repository's audience. Internal documentation and service identifiers do not belong in a public profile. If an excluded local location is used, verify the exclusion before placing private material there; otherwise keep it in the session until an appropriate location is established.
