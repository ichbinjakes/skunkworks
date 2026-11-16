Zellij organizes your terminal into **Sessions** (persistent workspaces), **Tabs** (separate contexts within a session), and **Panes** (splits or floating windows within a tab). Because it displays an interactive shortcut bar at the bottom of the screen, you do not need to memorize every command upfront.

### 1. Starting & Managing Sessions

Use named sessions for different projects so you can close your terminal and pick up right where you left off.

* **Start or attach to a named session:** `zellij attach -c my-project` (creates `my-project` if it doesn't exist, or attaches if it does)
* **List active/exited sessions:** `zellij list-sessions`
* **Detach (keep running in background):** `Ctrl + o`, then `d`
* **Open the interactive Session Manager:** `Ctrl + o`, then `w` (lets you switch sessions, preview them, or resurrect exited ones)

---

### 2. Core Modal Keybindings

Zellij uses **modes** to prevent shortcut conflicts with programs like Vim or your shell. Press a mode trigger, run your action, and press `Enter` or `Esc` to return to normal typing.

| Mode | Trigger | Common Actions |
| --- | --- | --- |
| **Pane** | `Ctrl + p` | `n` (new pane), `d` (split down), `r` (split right), `x` (close), `w` (toggle floating pane), `f` (fullscreen), `h/j/k/l` or arrows (move focus) |
| **Tab** | `Ctrl + t` | `n` (new tab), `x` (close tab), `r` (rename tab), `h/l` or `←/→` (switch tabs), `1-9` (jump to tab) |
| **Resize** | `Ctrl + n` | `h/j/k/l` or arrows to grow/shrink the focused pane |
| **Scroll** | `Ctrl + s` | `j/k` or arrows to scroll history; `e` to open the pane's scrollback directly in your `$EDITOR` |
| **Lock** | `Ctrl + g` | Passes all keystrokes directly to the active app (useful if Zellij shortcuts clash with Neovim/Emacs). Press `Ctrl + g` again to unlock. |

*(Tip: You can also use `Alt + n` for a quick new pane, `Alt + f` to toggle floating panes, and `Alt + h/j/k/l` to move between panes without entering a mode.)*

---

### 3. Typical Daily Coding Workflow

1. **Spin up a project workspace:** Run `zellij attach -c api-service` inside your repository.
2. **Set up Tab 1 (Coding):** Open your editor (`nvim` or `helix`), then press `Ctrl + p` -> `r` to open a narrow terminal pane on the right for running tests or git commands.
3. **Run quick tasks in a floating pane:** Press `Alt + f` to pop up a floating terminal, run a one-off script or database CLI, and press `Alt + f` again to hide it while it keeps running in the background.
4. **Separate concerns with tabs:** Press `Ctrl + t` -> `n` to open a second tab dedicated to running background services (Docker, dev servers, log tails) so they don't clutter your editor view.
5. **Wrap up:** Press `Ctrl + o` -> `d` to detach. The next day, reattach to the exact same layout and running processes.

---

### 4. Next-Level Quality of Life

* **Layouts (`.kdl`):** Once you find a pane/tab setup you repeat daily, save it as a KDL layout file and launch it with `zellij --layout my-layout.kdl` to boot your editor, servers, and logs in one command.
* **Interactive Settings:** Press `Ctrl + o`, then `c` to tweak themes, keybinding presets, or mouse behavior directly in the UI without manually editing config files.
