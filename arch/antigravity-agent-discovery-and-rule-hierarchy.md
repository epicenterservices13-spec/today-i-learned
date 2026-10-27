# Antigravity Agent Discovery and Custom Rule Precedence

Differentiate between standalone skills and first-class CLI agents in Antigravity, while managing global persona overrides via AGENTS.md.

## Context

When invoking custom personas or slash commands (e.g. `/morpheus`), system abstractions can create confusion if:
1. An agent is defined only as a skill or markdown file without being registered in an enabled plugin's `agents/` manifest, preventing `agy agents` and CLI aliases from discovering it.
2. An active global rule (`~/.agents/AGENTS.md`) hardcodes persona and formatting behavior (such as Lord Vader constraints), which overrides subagent personalities.
3. Decoupled dotfile refactors leave broken symlinks across automation directories (`50_OPS/51_AUTOMATION/agents/`).

## Implementation / Code

### 1. Registering First-Class Agents via Plugins
To make an agent visible to `agy agents` and callable via `agy --agent <name>`, define it under an enabled plugin's `agents/` directory with frontmatter:

```markdown
---
name: morpheus
description: "Matrix Captain & Systemic Reality Guide."
tools:
  - view_file
  - list_dir
  - run_command
mainAgent: true
subagent: true
commandExecutionPolicy: auto
---

# Morpheus — System Prompt
...
```

Verify agent registration:
```bash
agy agents
```

### 2. Managing Rule Precedence via AGENTS.md
Antigravity automatically loads rule definitions from `~/.agents/AGENTS.md` and workspace roots. Keep persona directives aligned with user intent and preserve core engineering guardrails (such as single-file atomic commits).

### 3. Repairing Dotfile & Automation Symlinks
Audit broken relative symlinks created during dotfile reorganizations:
```bash
ln -sfn "$HOME/55_INFRA/dotfiles/agents/morpheus" "$HOME/50_OPS/51_AUTOMATION/agents/morpheus"
ln -sfn "$HOME/.agents/AGENTS.md" "$HOME/AGENTS.md"
```

## Takeaways

- `skills/` provide tool workflows; `agents/` define selectable personas and conversational runtimes.
- An unregistered agent cannot be launched via `agy --agent <name>`, even if an alias exists in `aliases.sh`.
- Rules in `AGENTS.md` strictly bind the model's tone and formatting across all turns until explicitly modified.
- Always verify symlink targets using `ls -l` when reorganizing dotfiles and agent hierarchies.
