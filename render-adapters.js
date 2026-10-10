#!/usr/bin/env node
// Render per-harness adapters from this repo's harness-neutral sources
// (docs/adr/0003). Called by install.sh after skills are copied.
//
//   node render-adapters.js <repo-dir> <claude-dir> <opencode-dir|"">
//
// - {{SPEC_DRIVEN_DIR}} in installed skills and agents becomes the installed
//   spec-driven skill path.
// - agents/<name>.md -> <claude-dir>/agents/<name>.md (Claude Code; omp reads it too)
//                    -> <opencode-dir>/agents/<name>.md (mode: subagent, hidden)
// - COMMAND_SKILLS are human-only triggers (`disable-model-invocation: true`).
//   opencode ignores that key, so they become opencode commands and
//   opencode.json denies the model loading them as skills. Only skills whose
//   body is self-contained belong here: a command has no skill directory to
//   resolve relative files against.
// An empty <opencode-dir> skips everything opencode.

const fs = require('fs');
const path = require('path');

const [repoDir, claudeDir, opencodeDir] = process.argv.slice(2);
if (!repoDir || !claudeDir) {
  console.error('usage: render-adapters.js <repo-dir> <claude-dir> [opencode-dir]');
  process.exit(2);
}
const TOKEN = /\{\{SPEC_DRIVEN_DIR\}\}/g;
const COMMAND_SKILLS = ['spec-review', 'code-review'];
const specDriven = path.join(claudeDir, 'skills', 'spec-driven');

function split(text) {
  const m = text.match(/^---\n([\s\S]*?)\n---\n?([\s\S]*)$/);
  if (!m) return { meta: {}, body: text };
  const meta = {};
  for (const line of m[1].split('\n')) {
    const kv = line.match(/^([\w-]+):\s*(.*)$/);
    if (kv) meta[kv[1]] = kv[2].replace(/^["']|["']$/g, '');
  }
  return { meta, body: m[2] };
}

const frontmatter = (pairs) =>
  '---\n' + pairs.map(([k, v]) => `${k}: ${typeof v === 'string' ? JSON.stringify(v) : v}`).join('\n') + '\n---\n';

function write(file, text) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, text);
}

function walk(dir) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((e) =>
    e.isDirectory() ? walk(path.join(dir, e.name)) : [path.join(dir, e.name)]);
}

// 1. Placeholders inside installed skills.
for (const file of walk(path.join(claudeDir, 'skills'))) {
  if (!/\.(md|ya?ml|txt)$/.test(file)) continue;
  const text = fs.readFileSync(file, 'utf8');
  if (text.search(TOKEN) !== -1) fs.writeFileSync(file, text.replace(TOKEN, specDriven));
}

// 2. Agents.
const agentsDir = path.join(repoDir, 'agents');
for (const f of fs.existsSync(agentsDir) ? fs.readdirSync(agentsDir).filter((x) => x.endsWith('.md')) : []) {
  const { meta, body } = split(fs.readFileSync(path.join(agentsDir, f), 'utf8'));
  const name = meta.name || f.replace(/\.md$/, '');
  const text = body.replace(TOKEN, specDriven);
  write(path.join(claudeDir, 'agents', `${name}.md`),
    frontmatter([['name', name], ['description', meta.description]]) + text);
  if (opencodeDir) {
    write(path.join(opencodeDir, 'agents', `${name}.md`),
      frontmatter([['description', meta.description], ['mode', 'subagent'], ['hidden', true]]) + text);
  }
  console.log(`  agent ${name}`);
}

// 3. Human-only skills -> opencode commands + skill deny.
const humanOnly = [];
for (const name of COMMAND_SKILLS) {
  const file = path.join(repoDir, 'skills', name, 'SKILL.md');
  if (!fs.existsSync(file)) continue;
  const { meta, body } = split(fs.readFileSync(file, 'utf8'));
  if (meta['disable-model-invocation'] !== 'true') {
    console.log(`  NOTE: ${name} lacks disable-model-invocation: true; not rendered as a command.`);
    continue;
  }
  humanOnly.push(name);
  if (opencodeDir) {
    write(path.join(opencodeDir, 'commands', `${name}.md`),
      frontmatter([['description', meta.description]]) +
      body.replace(TOKEN, specDriven).trimEnd() + '\n\nArguments: $ARGUMENTS\n');
    console.log(`  opencode command /${name}`);
  }
}

if (!opencodeDir) {
  console.log('  opencode not found; skipped opencode agents and commands.');
  process.exit(0);
}
if (!humanOnly.length) process.exit(0);

const cfgPath = path.join(opencodeDir, 'opencode.json');
let cfg = { $schema: 'https://opencode.ai/config.json' };
if (fs.existsSync(cfgPath)) {
  try {
    cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
  } catch (e) {
    console.log(`  NOTE: ${cfgPath} is not plain JSON; deny skills ${humanOnly.join(', ')} under permission.skill by hand.`);
    process.exit(0);
  }
}
if (cfg.permission !== undefined && (typeof cfg.permission !== 'object' || cfg.permission === null)) {
  console.log(`  NOTE: opencode.json "permission" is not an object; deny skills ${humanOnly.join(', ')} by hand.`);
  process.exit(0);
}
cfg.permission = cfg.permission || {};
let skill = cfg.permission.skill;
if (typeof skill === 'string') skill = { '*': skill };
skill = skill || {};
let changed = false;
for (const n of humanOnly) {
  if (skill[n] !== 'deny') {
    skill[n] = 'deny';
    changed = true;
  }
}
cfg.permission.skill = skill;
if (changed) {
  write(cfgPath, JSON.stringify(cfg, null, 2) + '\n');
  console.log(`  opencode.json: model may not load ${humanOnly.join(', ')} (human-only commands)`);
} else {
  console.log('  opencode.json skill permissions already present.');
}
