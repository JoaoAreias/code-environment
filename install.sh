#!/bin/bash
# Install this repo's skills, agents and caveman hooks into Claude Code, and
# render the matching agents and commands for opencode (omp reads the Claude
# files). Safe to re-run after every `git pull` — always overwrites the copied
# files, only adds to settings.json / opencode.json what isn't already there.
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
OPENCODE_DIR="${OPENCODE_CONFIG_DIR:-$HOME/.config/opencode}"
SETTINGS="$CLAUDE_DIR/settings.json"
# Skills this repo no longer ships, one per line as `name|phrase`. The phrase is
# text from the SKILL.md this repo shipped under that name (for tlc-spec-driven,
# the upstream Tech Lead's Club copy that spec-driven replaced). The skills folder is
# shared with other sources, so an installed folder is removed only when it is a
# real folder (not a symlink) whose SKILL.md contains the phrase.
RETIRED_SKILLS="tlc-spec-driven|Tech Lead's Club - Spec-Driven Development
ask-matt|A router over the skills in this repo.
implement|Use /tdd where possible, at pre-agreed seams.
to-spec|Do NOT interview the user; just synthesize what you already know.
to-tickets|tracer-bullet vertical slices, each declaring the tickets that
triage|through a small state machine of triage roles.
wayfinder|Wayfinding is about finding that way, not charging at the destination.
wizard|walks a human, step by step, through a manual procedure
setup-matt-pocock-skills|Scaffold the per-repo configuration that the engineering skills assume"

is_retired() {
  printf '%s\n' "$RETIRED_SKILLS" | grep -q "^$1|"
}

if ! command -v node >/dev/null 2>&1; then
  echo "ERROR: 'node' is required (renders agents and merges hook config into settings.json)."
  exit 1
fi

mkdir -p "$CLAUDE_DIR/skills" "$CLAUDE_DIR/hooks" "$CLAUDE_DIR/agents"

# 1. Skills — copy every skills/<name>/ folder that has a SKILL.md
echo "Installing skills..."
while IFS='|' read -r name phrase; do
  dest="$CLAUDE_DIR/skills/$name"
  if [ ! -e "$dest" ] && [ ! -L "$dest" ]; then
    continue
  fi
  if [ ! -L "$dest" ] && [ -f "$dest/SKILL.md" ] && grep -qF -- "$phrase" "$dest/SKILL.md"; then
    rm -rf "$dest"
    echo "  removed retired skill $name"
  else
    echo "  skipped $name: not installed by this repo"
  fi
done <<RETIRED
$RETIRED_SKILLS
RETIRED
for dir in "$SCRIPT_DIR"/skills/*/; do
  name="$(basename "$dir")"
  if is_retired "$name"; then
    continue
  fi
  if [ -f "$dir/SKILL.md" ]; then
    rm -rf "$CLAUDE_DIR/skills/$name"
    cp -r "$dir" "$CLAUDE_DIR/skills/$name"
    echo "  $name"
  fi
done

# 2. Agents and opencode adapters — one harness-neutral source per agent in
#    agents/, rendered per harness (docs/adr/0003-*). opencode is rendered only
#    when it is installed or its config dir exists.
echo "Rendering agents and commands..."
OPENCODE_TARGET=""
if command -v opencode >/dev/null 2>&1 || [ -d "$OPENCODE_DIR" ]; then
  OPENCODE_TARGET="$OPENCODE_DIR"
fi
node "$SCRIPT_DIR/render-adapters.js" "$SCRIPT_DIR" "$CLAUDE_DIR" "$OPENCODE_TARGET"

# 3. graphify — the code graph spec-driven and both reviewers search with
if command -v graphify >/dev/null 2>&1; then
  echo "graphify: $(command -v graphify)"
elif command -v uv >/dev/null 2>&1; then
  echo "Installing graphify (uv tool install graphifyy)..."
  uv tool install graphifyy
else
  echo "WARNING: graphify not found and uv unavailable. Install it (pipx install graphifyy) before /spec-review or /code-review."
fi

# 4. fd — spec-driven lists decision records and other flows' plans with it
if ! command -v fd >/dev/null 2>&1; then
  echo "WARNING: fd not found. spec-driven needs it to find decisions and plans in a repo; install fd (https://github.com/sharkdp/fd) before the next Specify."
fi

# 5. Hooks — copy flat (caveman-config.js locates SKILL.md via
#    ../skills/caveman/SKILL.md relative to this directory, so hooks and
#    skills must stay siblings)
echo "Installing hooks..."
for f in "$SCRIPT_DIR"/hooks/*; do
  cp -f "$f" "$CLAUDE_DIR/hooks/$(basename "$f")"
done
chmod +x "$CLAUDE_DIR/hooks/caveman-statusline.sh"
echo "  $(ls "$SCRIPT_DIR"/hooks | wc -l | tr -d ' ') files"

# 6. settings.json — wire SessionStart, UserPromptSubmit, statusLine
echo "Wiring settings.json..."
if [ ! -f "$SETTINGS" ]; then
  echo '{}' > "$SETTINGS"
fi
if [ ! -f "$SETTINGS.bak" ]; then
  cp "$SETTINGS" "$SETTINGS.bak"
fi

CAVEMAN_SETTINGS="$SETTINGS" CAVEMAN_HOOKS_DIR="$CLAUDE_DIR/hooks" node -e "
  const fs = require('fs');
  const settingsPath = process.env.CAVEMAN_SETTINGS;
  const hooksDir = process.env.CAVEMAN_HOOKS_DIR;
  const statusLinePath = hooksDir + '/caveman-statusline.sh';
  const settings = JSON.parse(fs.readFileSync(settingsPath, 'utf8'));
  if (!settings.hooks) settings.hooks = {};

  const hasHook = (event, script) =>
    Array.isArray(settings.hooks[event]) &&
    settings.hooks[event].some(e =>
      e.hooks && e.hooks.some(h => h.command && h.command.includes(script))
    );

  if (!settings.hooks.SessionStart) settings.hooks.SessionStart = [];
  if (!hasHook('SessionStart', 'caveman-activate.js')) {
    settings.hooks.SessionStart.push({
      hooks: [{
        type: 'command',
        command: 'node \"' + hooksDir + '/caveman-activate.js\"',
        timeout: 30,
        statusMessage: 'Loading caveman mode...'
      }]
    });
    console.log('  Added SessionStart hook.');
  } else {
    console.log('  SessionStart hook already present.');
  }

  if (!settings.hooks.UserPromptSubmit) settings.hooks.UserPromptSubmit = [];
  if (!hasHook('UserPromptSubmit', 'caveman-mode-tracker.js')) {
    settings.hooks.UserPromptSubmit.push({
      hooks: [{
        type: 'command',
        command: 'node \"' + hooksDir + '/caveman-mode-tracker.js\"',
        timeout: 30,
        statusMessage: 'Tracking caveman mode...'
      }]
    });
    console.log('  Added UserPromptSubmit hook.');
  } else {
    console.log('  UserPromptSubmit hook already present.');
  }

  if (!settings.statusLine) {
    settings.statusLine = { type: 'command', command: 'bash \"' + statusLinePath + '\"' };
    console.log('  Configured statusLine.');
  } else if (typeof settings.statusLine === 'object' && settings.statusLine.command && settings.statusLine.command.includes(statusLinePath)) {
    console.log('  statusLine already configured.');
  } else {
    console.log('  NOTE: existing statusLine detected — left untouched.');
  }

  fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2) + '\n');
"

echo ""
echo "Done. Restart Claude Code and opencode so they pick up new skills, agents, commands and hooks."
