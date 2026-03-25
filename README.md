# agent-skills

Reusable agent skills collected in one repo.

This repository is the source for the skills under [`skills/`](./skills). It is intentionally lightweight: the repo mainly contains skill folders with `SKILL.md` instructions plus any supporting scripts, references, or templates each skill needs.

## What This Repo Contains

- Custom and adapted skills for coding, ops, writing, review, debugging, and workflow automation
- Supporting assets that live next to a skill, such as Python helpers, shell scripts, templates, and reference notes
- A local install/source lock file in [`.skill-lock.json`](./.skill-lock.json) showing where some imported skills came from

## Layout

```text
.
├── skills/
│   ├── <skill-name>/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   ├── references/
│   │   └── templates/
└── .skill-lock.json
```

Each skill is self-contained. The contract is simple: if a tool or agent knows how to discover `SKILL.md` files, it can use this repo as a skill source.

## Notable Skill

[`skills/retro`](./skills/retro) provides a retrospective workflow for reviewing recent coding sessions and improving skills, agents, and workflows. Its helper script, [`skills/retro/retro_extract.py`](./skills/retro/retro_extract.py), currently parses Claude Code-style `.jsonl` session transcripts from `~/.claude/projects`.

That is narrower than Angie’s version in `angie/agentic-setup`, which has expanded `retro_extract.py` support for multiple backends and a vendoring/install layer around it. This repo is the upstream skill source; Angie’s repo is a broader personal agent environment that consumes repos like this one.

## Using This Repo

How you install these skills depends on the agent framework you use, but the common pattern is:

1. Clone this repo somewhere your agent tooling can read.
2. Point your tool at the [`skills/`](./skills) directory, or copy/link individual skill folders into its skill search path.
3. Keep third-party provenance in sync if you import or update external skills.

This repo does not currently include a universal installer or manifest of its own.

## Related Repos

- [`angie/agentic-setup`](https://github.com/angie/agentic-setup): a full personal agent environment with vendoring, manifest-driven sync, and personal overrides; it explicitly vendors `damacus/agent-skills` as an opt-in upstream for `retro`
- [`citypaul/.dotfiles`](https://github.com/citypaul/.dotfiles): a major upstream in Angie’s setup for `CLAUDE.md`, skills, commands, and agents
- [`mintuz/claude-plugins`](https://github.com/mintuz/claude-plugins): another upstream in Angie’s setup for skills, commands, and agents

## Provenance

Several skills in this repo were imported or adapted from other public repositories. The current local lockfile references these sources:

- [`anthropics/skills`](https://github.com/anthropics/skills)
- [`vercel-labs/skills`](https://github.com/vercel-labs/skills)
- [`microsoft/playwright-cli`](https://github.com/microsoft/playwright-cli)
- [`addyosmani/web-quality-skills`](https://github.com/addyosmani/web-quality-skills)
- [`odyssey4me/agent-skills`](https://github.com/odyssey4me/agent-skills)
- [`nicolaischmid/agent-skills`](https://github.com/nicolaischmid/agent-skills)
- [`markpitt/claude-skills`](https://github.com/markpitt/claude-skills)
- [`jeffallan/claude-skills`](https://github.com/jeffallan/claude-skills)

If you want stricter attribution, the next useful step would be adding per-skill provenance metadata or a small generated table from [`.skill-lock.json`](./.skill-lock.json).
