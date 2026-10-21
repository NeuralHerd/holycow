# Terminal presentation

The renderer uses Python 3's standard library and bundled ASCII assets. Resolve its location relative to the installed skill, not the project being initialized:

```sh
python3 "<installed-skill-directory>/scripts/banner.py"
```

It only writes to stdout. It does not initialize a repository, connect agents, alter terminal settings, clear the screen, animate, or install dependencies. The colors use Eden's cyan, blue, violet, and gold; the terminal's background stays unchanged. Soft glow is not part of ANSI text rendering.

## Choose the output surface

- In an established user-visible shell, run the renderer once. It detects width and selects full artwork with a speech box, stacked branding, a compact cow, or a text label.
- In a harness that captures or collapses tool output, use the command below, then reproduce the returned artwork in a visible response as a monospace block before inspecting the repository. Use 80 columns unless a known narrower pane requires less. Respect required response prefixes. A tool-created PTY does not prove the user can see its colors; do not put escape sequences into assistant prose or bypass capture by writing to `/dev/tty`.
- If Python is unavailable, read the [full cow](../assets/cyber-cow.txt) or [compact cow](../assets/cyber-cow-compact.txt), add `HOLYCOW / INIT` beneath it, and show plain text. Use just the label when the pane is too narrow. Do not install a runtime just for decoration.

Captured-output command (use the installed skill's path even when the coordinator starts outside the target repository):

```sh
python3 "<installed-skill-directory>/scripts/banner.py" --color never --width 80
```

Run it separately from discovery commands so its output can be reproduced without unrelated logs. `--help` prints usage, not the banner. Successful execution alone is insufficient when the user sees only a collapsed tool summary.

Herdr hosts the terminal, while the foreground agent controls its own presentation. Do not infer color support from the names Claude, Codex, or Cursor, or from Herdr being installed. Follow the installed Herdr guidance; do not create panes, interrupt an agent, or start processes in another pane just to display the banner. Use an already-authorized visible shell when one is available. Otherwise use the chat fallback.

## Color controls

Automatic mode emits color only to a terminal with a usable `TERM` and no nonempty `NO_COLOR`. It uses RGB when advertised by `COLORTERM` or a direct-color `TERM`, then 256 or 16 colors according to the terminal declaration. Piped output is plain.

For an explicit visual check in a compatible terminal:

```sh
python3 "<installed-skill-directory>/scripts/banner.py" --color truecolor --width 100
```

`--color truecolor|256|16|never` explicitly overrides detection, including `NO_COLOR`; use it only when requested or the output capability is known. `--width` overrides layout width. `--quiet` prints nothing. Do not repeatedly force color to compensate for a harness stripping it.

If the user requests the colors while using a capturing harness, explain the presentation limit and give the command above with the actual installed path for their ordinary shell. Keep the plain cow visible in the agent response; do not claim the colored terminal version appeared there.

Keep status reporting outside the renderer and tied to real setup results. A successful banner run proves rendering output was produced, not that any agent, tracker, or project is ready.
