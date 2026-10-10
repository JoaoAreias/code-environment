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
# Skills this repo used to ship under another name; removed on install.
RETIRED_SKILLS="tlc-spec-driven"

if ! command -v node >/dev/null 2>&1; then
  echo "ERROR: 'node' is required (renders agents and merges hook config into settings.json)."
  exit 1
fi

mkdir -p "$CLAUDE_DIR/skills" "$CLAUDE_DIR/hooks" "$CLAUDE_DIR/agents"

# 1. Skills — copy every skills/<name>/ folder that has a SKILL.md
echo "Installing skills..."
for name in $RETIRED_SKILLS; do
  if [ -d "$CLAUDE_DIR/skills/$name" ]; then
    rm -rf "$CLAUDE_DIR/skills/$name"
    echo "  removed retired skill $name"
  fi
done
for dir in "$SCRIPT_DIR"/skills/*/; do
  name="$(basename "$dir")"
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

# 4. Hooks — copy flat (caveman-config.js locates SKILL.md via
#    ../skills/caveman/SKILL.md relative to this directory, so hooks and
#    skills must stay siblings)
echo "Installing hooks..."
for f in "$SCRIPT_DIR"/hooks/*; do
  cp -f "$f" "$CLAUDE_DIR/hooks/$(basename "$f")"
done
chmod +x "$CLAUDE_DIR/hooks/caveman-statusline.sh"
echo "  $(ls "$SCRIPT_DIR"/hooks | wc -l | tr -d ' ') files"

# 5. settings.json — wire SessionStart, UserPromptSubmit, statusLine
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
