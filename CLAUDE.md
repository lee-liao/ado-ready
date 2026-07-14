# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

`ado-ready` is a **GOLD session workspace** for the `golden_session` engine, not a
standalone application. The engine primes a GOLD session on this directory once,
then forks one child session per task to work Azure DevOps work items headlessly.
See `README.md` for the full picture; it is a filled-in instance of the engine's
`examples/workspace-template/`.

When you run *inside a fork* (headless `claude -p`), obey the rules in
`ado-workitem-task.md`:

- **No `$VAR` in Bash commands** — headless claude blocks any line containing
  `$NAME` ("Contains simple_expansion"). Resolve env vars in Python:
  `python3 -c "import os; print(os.environ.get('GS_RUN_DIR'))"`.
- **All output goes under `GS_RUN_DIR`** — a PreToolUse hook
  (`.claude/confine_writes.py`) blocks writes outside it. Never hard-code a path.
- **Download attachments via `.claude/ado_download.py`**, never an inline
  `curl -u ":$AZURE_DEVOPS_PAT"` (trips the `$VAR` rule and leaks the secret).

## Azure DevOps MCP integration

`.mcp.json` registers a stdio MCP server named `ado` (`@azure-devops/mcp`, the
official Microsoft server) for the `cubeforest3003` organization (default
project `powerBI-demo`), exposing tools to read work items, repos, pipelines,
wikis, test plans, and pull requests. Attachment binaries are still fetched via
REST, not an MCP tool — that is why `.claude/ado_download.py` exists.

## Secrets

Two env vars carry the same raw PAT, for two different consumers, and both live
**only** in the `env` block of `.claude/settings.local.json` (gitignored via
`.gitignore` — already present):

- `AZURE_DEVOPS_PAT` — read by `.claude/ado_download.py` and any inline REST
  calls.
- `ADO_MCP_AUTH_TOKEN` — read by the `ado` MCP server (`--authentication
  envvar` in `.mcp.json`).

Never put either in `.mcp.json` or `.claude/settings.json` (git-tracked).
Claude Code injects the `env` block into its process; the MCP server and the
fork's `python3`/Bash inherit it.

## Layout

- `.claude/settings.json` — hook + `permissions` + `enabledMcpjsonServers` (tracked, no secrets)
- `.claude/confine_writes.py` — PreToolUse hook confining writes to `GS_RUN_DIR`
- `.claude/ado_download.py` — authenticated attachment download (reads PAT from env)
- `.claude/gold-context.md` — stable priming context for `prime --context-file`
- `ado-workitem-task.md` — parameterized `${WORK_ITEM_ID}` task prompt

## Build / test

There is no build, lint, or test step.