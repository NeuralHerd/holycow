---
name: holycow-init
description: Use when the user wants to initialize, inspect, or refresh a repository's HolyCow workflow configuration, including tracking, project guidance, checks, and available tools.
license: MIT
disable-model-invocation: true
---

# holycow-init

Prepare a repository for the HolyCow workflow by discovering its conventions, filling relevant gaps, and verifying what is usable. Work with new or existing projects. Setup remains optional for the other skills.

## Show the Init identity

Start an Init run with the Cyber Halo Cow: a gold halo, cyan-to-violet mechanical cow, and HolyCow wordmark. Use the bundled [terminal renderer](scripts/banner.py) rather than recreating the artwork. Follow [terminal presentation](references/terminal.md) to choose visible terminal output or a plain chat fallback, and show the identity once per run. Omit decoration for quiet or machine-readable requests.

During setup, give brief updates at meaningful transitions: discovery, configuration, and verification. Report actual outcomes, including unresolved choices and unavailable checks; do not simulate progress percentages or announce readiness before verification. The banner makes no connection claims. An audit uses the same identity but does not imply configuration was applied.

## Inspect the existing project

Establish the requested repository or workspace boundary and whether the user wants an audit, a proposed configuration, or applied setup. A request to initialize or refresh authorizes the relevant local setup edits; reuse preferences already established.

Check current working changes and applicable instructions before editing. Use safe repository metadata, manifests, scripts, CI configuration, relevant agent instructions, planning records, and documentation pointers. Avoid broad source scans or reading entire global configurations when targeted inspection is sufficient.

Identify existing tracker choices, glossary and decision locations, check commands and working directories, standing quality requirements, repository relationships, and workflow constraints. A GitHub remote identifies code hosting, not necessarily the issue tracker. A monorepo does not by itself require multiple glossaries.

Inspect any existing HolyCow context first. Read [project context](references/project-context.md) before creating or updating it. Reuse canonical documents and link to them rather than copying their contents into another configuration.

## Resolve material gaps

Briefly show what is established, what is missing, and the intended edits. Ask only about choices the evidence cannot settle, such as conflicting trackers, a new source of truth, or whether internal context belongs in shared documentation. Give a recommendation, reason, and material trade-off; follow the user's preferred question format.

Keep unresolved choices explicit while completing independent setup. Do not invent issue types, states, labels, test commands, stack choices, or domain definitions. Use local planning when chosen or no tracker is configured; an unavailable selected tracker remains selected and unavailable.

For a new project with little evidence, record only settled conventions and useful next steps. Do not manufacture a full development environment, initialize Git, or create empty glossary, ADR, and ticket scaffolding merely to make setup look complete.

## Configure the smallest useful context

Keep one canonical project context at the existing documented location. Without one, use `docs/agents/holycow.md`. This is ordinary Markdown with stable project facts, relevant conventions, and pointers, not a new configuration runtime.

Capture only what future work needs: repository scope, work tracking, canonical project documentation, meaningful commands, delivery conventions, and coordination preferences. Separate shared project facts from personal paths and machine-specific availability. Keep private material within its intended audience and never store credentials in the profile.

Where the repository has applicable agent instructions, add or update a short context pointer without replacing unrelated content. Respect directory scope and each requested harness's actual instruction-loading mechanism. Do not assume that one harness reads another harness's entry file, or duplicate the full context across them. Verify unfamiliar mechanisms against current documentation.

When there are no existing instruction entry files, the default context path is sufficient for HolyCow's consumers; creating additional entry files is only necessary when the requested workflow needs them. If a custom context location is chosen, ensure the relevant consumers can discover its pointer.

Do not install or remove skills, plugins, hooks, dependencies, or global configuration as an automatic setup step. Likewise, tracker mutations, cloud provisioning, credential changes, and deployment require corresponding scope in the user's request. Perform such already-authorized work without requesting the same permission again.

## Check the capabilities that matter

Inspect available tools for the requested workflow and harnesses. A CLI on disk, an installed skill, and an authenticated project connection are different capabilities. Use focused read-only probes against the intended project where available. A successful read does not prove write access or support for hierarchy and dependency operations.

Check command provenance before running anything. Prefer appropriate low-impact checks within the setup scope. Report a command found in a manifest separately from one successfully executed; do not run migrations, deployments, or scripts with unreviewed side effects to fill a checklist.

For Herdr, follow its installed guidance and control it only within a supported managed environment. If the preferred coordinator is unavailable, report the limitation and a permitted native-agent or sequential fallback. Do not launch workers or extra harness processes merely to test setup. Availability does not authorize delegation.

Report capability checks with the harness or environment where observed. Do not claim Claude, Codex, and Cursor are all verified from one successful session. Keep transient access results in the setup report or an existing private local record rather than treating them as permanent shared project facts.

## Reconcile and finish

On a rerun, update only changed facts or broken pointers, preserve human edits, and avoid duplicate configuration or instruction sections. Re-read affected files before writing if other work may have changed them. An unchanged setup should need no file edits.

Verify written content, links, command locations, and discovery from the requested consumers. Check that recorded conventions still match their canonical sources. Do not create test issues or publish changes merely to prove connectivity.

Return the actual context location and changed files, what was verified and where, what remains untested or unavailable, and the next useful action. Describe partial setup accurately and preserve completed work if a later operation fails. Reconcile existing results before retrying.

Setup alone does not launch a feature workflow. Recommend a next step appropriate to the user's task; a clear implementation request can go directly to Build without repeating planning.
