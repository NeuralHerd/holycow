# Running HolyCow evaluations

Draft, 27 November 2026. Turns the scenarios in [`evals/`](../../evals/) into repeatable runs that compare each agent with and without HolyCow.

## Goal

For every skill and every supported agent, publish how often the agent meets the scenario's expectations with HolyCow installed versus without it, plus tokens and time. Results must come from recorded runs, not from reading the skills.

Constraints:

- Any agent with a headless mode can be added through one adapter; no agent's own eval format is canonical.
- Each run starts from a fresh workspace and sees only the skill revision under test. Globally installed skills, user instructions and memory must not leak into either arm.
- The executing agent never sees the expected behavior or the graders.

## Running

```sh
python3 evals/run.py --list
python3 evals/run.py invocation/ordinary-request --agent claude --arm both
python3 evals/run.py invocation --agent codex --runs 3
```

Models come from [`evals/agents.json`](../../evals/agents.json); `--model` and `--judge-model` override them. The runner refuses to start without a pinned agent model unless `--allow-default-model` is passed for a quick check. Each run writes `result.json`, the raw events, stderr, the final reply and `diff.patch` under `.local/evals/` (ignored). `--keep-workspace` keeps the workspace for inspection.

The runner's own tests need no agent: `python3 -m unittest discover -s evals`.

## A case

`evals/cases/<group>/<slug>/` holds:

- `case.json`: the scenario it implements (`evals/<file>.md#<heading-anchor>`), its steps, graders and an optional `timeout_seconds` (default 900).
- One prompt file per step, holding the user's message without invocation syntax. A step's `invoke` names the skill to invoke; the runner adds `/skill` or `$skill` in the with-skill arm and leaves the message bare in the without-skill arm. Each step is a separate agent session in the same workspace.
- `fixture/`: files copied into the workspace and committed as the starting state.

The site renders only top-level `evals/*.md`, so cases under `evals/cases/` do not become pages. The Markdown scenario files stay the human-readable source.

## A run

1. Copy the fixture into a temporary directory, `git init`, and commit.
2. With-skill arm: copy every skill into the agent's project-level skill folder, hidden from `git status` through `.git/info/exclude`. Without-skill arm: install nothing.
3. Run each step headless, in its own process group, with the case's time limit. Writes are allowed only inside the workspace.
4. Keep the raw event stream, final reply, a diff against the fixture, duration and reported usage.
5. Grade, then write the result.

After a step the agent controls the workspace, including `.git/config` and `.gitattributes`, which can make git run commands. So the runner measures changes in Python against the original fixture (committed changes count; symlinks are recorded, never followed) and runs no git command there except a commit count with hooks and fsmonitor off. Check commands run code the agent wrote, so they run under macOS `sandbox-exec` with no network, writes limited to the workspace and temp folder, and only `PATH`, `HOME`, `TMPDIR`, `LANG` and `PYTHONDONTWRITEBYTECODE` in the environment. Without `sandbox-exec`, a check runs unsandboxed and its result says so.

The agents themselves run inside their own sandboxes with your environment, minus `CLAUDE_*` and `ANTHROPIC_*` variables. Claude Code creates an empty `~/.claude/projects/<workspace>/memory/` folder even with `--no-session-persistence`; the runner removes it after the run.

## Agent adapters (observed 27 November 2026)

| Agent | Version | Headless command | Isolation from global skills |
| --- | --- | --- | --- |
| Claude Code | 2.1.332 | `claude -p "<prompt>" --output-format stream-json --verbose --no-session-persistence --setting-sources project,local --strict-mcp-config --permission-mode acceptEdits --settings '{"sandbox":{"enabled":true,"autoAllowBashIfSandboxed":true}}'` | Works with the existing login. User-level skills dropped from 10 HolyCow entries to 0, and a workspace `.claude/skills` copy loaded. Organization-managed plugins still load. The `init` event lists loaded skills, so each run verifies its arm. |
| Codex | 0.172.0 | `codex exec --json --ephemeral -s workspace-write -c features.memories=false -C <workspace> "<prompt>" < /dev/null` | Works with the eval HOME below. With the daily HOME, an explicit `$holycow-guide` loaded the global `~/.agents/skills` copy with and without `--ignore-user-config`. With the eval HOME it reported the skill as not loaded, and it loaded a copy in the test folder's `.agents/skills`. The `memories` feature is off by default and the runner keeps it off. Without `< /dev/null`, `codex exec` waits for stdin indefinitely. |
| Cursor | 2026.11.22 | `cursor-agent -p "<prompt>" --output-format stream-json --trust --force --sandbox enabled --workspace <workspace> < /dev/null` | Works with the eval HOME and API key below, but shows a keychain dialog (see below). With the daily HOME, an explicit `/holycow-guide` loaded a global copy from `~/.claude/skills` or `~/.agents/skills`. With the eval HOME and `CURSOR_API_KEY`, it reported the skill as not loaded, and it loaded a copy in the test folder's `.cursor/skills`. The default model was "Grok 4.7 256K High Fast" with the daily login and "Auto" with the API key. |

All three report token usage in their final event; Claude Code also reports cost. Results keep each agent's usage as reported, because the agents count cached input differently.

None of the three logs an explicit `/skill` or `$skill` invocation as an event. A run proves its arm from what the runner installed, plus Claude Code's startup skill list. Skill use is graded from reads of, and commands against, `skills/<name>/` files and Claude Code's `Skill` tool calls; whether an invoked skill shaped the reply is graded by the judge.

### Eval logins

Codex and Cursor run with `HOME` set to a dedicated eval folder, `~/.holycow-evals/<agent>/`, so eval runs never read or change your daily settings or global skills. Claude Code keeps its normal login, because its flags already exclude user-level skills.

- **Codex** keeps its login in the eval folder. Sign in once from your own terminal; the same account as daily work is fine:

  ```sh
  HOME="$HOME/.holycow-evals/codex" codex login
  ```

- **Cursor** keeps its login in the macOS keychain, which a different `HOME` cannot reach: `cursor-agent login` under the eval folder fails with "couldn't save your login to the macOS keychain (security exit code 154)". Do not run the `security delete-generic-password` command that error suggests; it deletes your daily Cursor login. Evals use a Cursor API key instead, passed as `CURSOR_API_KEY`. Store it once under its own keychain name, entering the key at the prompt:

  ```sh
  security add-generic-password -s holycow-evals-cursor -a "$USER" -w
  ```

  The runner reads it at run time and passes it only to `cursor-agent`; it never prints or writes the key.

  Each Cursor run still tries to save a session login to the keychain. Under the eval HOME, macOS then shows "A keychain cannot be found to store "cursor-user"". Click **Cancel**; the run continues. Never choose **Reset To Defaults**, which replaces your login keychain. Until this is solved, the runner refuses Cursor runs unless `--allow-keychain-prompt` is passed.

Swap in API keys with spending caps for any agent when eval usage needs separating from daily work.

## Graders

| Type | Passes when |
| --- | --- |
| `skills_not_used` | The step touched none of the listed skills (`"*"` means every skill except the one invoked in that step). |
| `skills_used` | The step touched every listed skill. |
| `no_command` | No shell command in any step matches the patterns. |
| `diff_matches` | Every pattern matches the final diff. |
| `changed_files` | The changed, added and deleted files are exactly the list. |
| `check_command` | The command exits 0 in the final workspace, run sandboxed as described above. |
| `judge` | `claude -p` with the judge model reads the rubric, the task, the tool calls, the reply and the diff, and returns pass. It is not told the arm. |

Graders may be limited to one arm with `arms` and to one step with `step` (1-based; default the last). A grader that cannot decide reports `error`; a judge without a model reports `skipped`. A run's verdict is `invalid` if its arm proof fails, `error` if the agent failed or timed out, then `error`, `fail`, `incomplete` (something skipped) or `pass` from its graders.

## Tiers

- Smoke: one case per skill, one run, with-skill arm only. Confirms cases load and agents run.
- Full: every case, both arms, three runs each. About 188 cases once variants are included, so roughly 1,100 agent sessions per agent; run per release, not per change.

## First slice

The four [invocation scenarios](../../evals/invocation.md) are in `evals/cases/invocation/` and run on Claude Code and Codex. Cursor is wired in but held back by the keychain dialog.

Smoke check, 27 November 2026: one run each of ordinary request (both arms) and of the other three cases (with-skill arm), on Claude Code 2.1.332 and Codex 0.172.0 with their default models and `claude-sonnet-5-5` as judge. All ten runs passed. Claude Code reported `claude-opus-5-5`; Codex does not report its model, so only a pinned `--model` records it. These are single unpinned runs that show the runner works, not evaluation results.

## Open decisions

1. Which model each agent and the judge use. `evals/agents.json` is empty until decided.
2. Spending limits for full runs.
3. How Cursor avoids the keychain dialog.

Decided: Codex and Cursor use separate eval logins (27 November 2026), rather than reusing daily logins from a temporary HOME or running under a separate macOS user or VM.
