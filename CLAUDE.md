# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository status

Newly initialized repo. Only `README.md` is tracked. No build, lint, or test commands exist yet — there is no source code to run.

## Azure DevOps MCP integration

`.mcp.json` registers a stdio MCP server named `azure-devops` using `@tiberriver256/mcp-server-azure-devops`, pointed at the Azure DevOps organization `cubeforest3003`. 

## Security note

`settings.local.json` holds a PAT in plaintext. It is **not** git-tracked. Add a `.gitignore` before running `git add .`.
