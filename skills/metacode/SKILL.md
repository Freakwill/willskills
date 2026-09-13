---
name: metacode
description: A meta-programming skill that automatically configures and manages Agent software such as OpenCode through natural-language prompts. Covers the full lifecycle — initial configuration, skill/plugin/MCP creation, update diagnostics, and self-evolution. Users complete all operations through conversation without memorizing any CLI commands.
category: devops
author: William
tags: [atomcode, meta, automation, self-evolving, mcp]
version: 0.1.0
---

# Metacode — Drive Agent Software by Talking

## Positioning

Metacode is the "administrator mode" for Agent software (OpenCode, OpenClaw, etc.).
An ordinary skill helps you write business code; Metacode helps you manage AtomCode itself:
installing plugins, creating skills, configuring MCP, diagnosing failures, performing upgrades — and even letting it improve itself.

## Capabilities

### 1. Initialization & Basic Configuration
- One-click detection of installation status and environment
- Automatically recommend and write `config.yaml` based on the user's tech stack (frontend / backend / algorithms / full-stack)
- CRUD management of model providers, API keys, and default models
- Configuration backup and rollback

### 2. Skill Lifecycle Management
- Generate a complete `SKILL.md` from a conversational description (including YAML frontmatter + operational steps)
- Automatically write to `~/.config/<agent>/skills/` or the project-level `.<agent>/skills/`
- Support enabling, disabling, version iteration, and batch updates of skills
- Provide skill quality self-checks (frontmatter completeness, step executability)

### 3. Plugin / MCP Management
- Parse community plugin/MCP repositories; install, configure, and uninstall with one click
- Automatically handle `stdio` / `sse` connection parameters for MCP servers
- Monitor plugin load status; automatically degrade or warn on conflicts

### 4. Updates & Diagnostics
- Detect updates for the software itself, skills, and plugins
- Perform safe upgrades (back up first, then replace)
- Collect runtime logs and environment info to locate common failures (network, permissions, missing dependencies)
- Generate diagnostic reports with repair suggestions

### 5. Self-Evolving
- **Skill introspection**: analyze the Agent's performance in the current conversation to identify recurring errors and inefficient patterns
- **Automatic patching**: write fixes into the corresponding skill's pitfalls section or add new operational steps
- **Skill merging**: detect skills with overlapping functionality, propose a merge plan, and execute it
- **Meta-log**: record the change points of each self-evolution, supporting human review and rollback

## Usage Examples

### Scenario A: Onboarding a newcomer
> User: I just installed OpenCode. I mainly write Python backends — set up my environment.
>
> Opencode:
> 1. Detect installation path and version
> 2. Write recommended configuration (model: qwen-coder; default shell: zsh; Python toolset fully enabled)
> 3. Install the `python-expert` and `git-workflow` skills
> 4. Verify the configuration takes effect

### Scenario B: Creating a custom skill
> User: I need a skill to convert design mockups into Tailwind CSS.
>
> Metacode:
> 1. Ask follow-up details (input format, output spec, whether screenshot analysis is needed)
> 2. Generate `design-to-tailwind/SKILL.md`
> 3. Register it in the skill directory
> 4. Test one case on the spot to confirm it works

### Scenario C: Troubleshooting
> User: OpenCode suddenly stopped responding to my MCP tools.
>
> Metacode:
> 1. Read the last 50 lines of the log
> 2. Check whether the MCP server process is alive
> 3. Validate the `mcp_servers` configuration format in `config.yaml`
> 4. Find a JSON syntax error, fix it automatically, and restart the service

### Scenario D: Triggering self-evolution
> User: (encounters similar errors on the same skill three times in a row)
>
> Metacode (in the background):
> 1. Identify the recurring failure pattern
> 2. Append an avoidance strategy to the original skill's pitfalls section
> 3. Report to the user: "I've optimized the XX skill for you — you won't fall into this trap again."

## Design Principles

1. **Conversation as interface**: all operations are done through natural language, with zero command-memorization burden
2. **Safety first**: automatically back up before modifying configs, require confirmation for critical operations, support undo
3. **Transparent & auditable**: every change records its reason, diff, and timestamp, viewable by the user at any time
4. **Progressive enhancement**: basic features work out of the box; advanced capabilities such as self-evolution are disabled by default and require user authorization

## Roadmap

- [x] v0.1 Basic configuration + skill creation
- [ ] v0.2 Plugin / MCP automated management
- [ ] v0.3 Diagnostics center + one-click repair
- [ ] v0.4 Self-evolution engine (skill introspection & automatic patching)
- [ ] v0.5 Community skill marketplace integration (one-click install of metacode packages shared by others)
