# ado-ready — a GOLD session workspace for Azure DevOps automation

This repo is **not an application you run directly.** It is the *workspace* that a
`golden_session` GOLD is primed on: the engine primes a GOLD session here **once**,
then **forks one child session per task** into this same directory to work Azure
DevOps work items headlessly (read the item, download attachments, produce
artifacts). It is a concrete, filled-in instance of the engine's
`examples/workspace-template/`.

- **Engine:** `golden_session` (the [sub-agents-on-hermes](../sub-agents-on-hermes/golden_session/README.md)
  repo) — the `prime once → fork per task → resume to recover` orchestrator.
- **This repo's role:** the GOLD's `cwd`. Everything here (MCP registration, the
  output-isolation hook, the task template, helper scripts, secrets split) is
  what a fork inherits when it runs.
- **Deployment path:** copied to `/opt/data/projects/ado-ready` on the Hermes
  bind mount; the GOLD is registered under the name **`ado-ready`**.

## How a run happens

The engine drives this workspace — you don't launch `claude` here by hand.

```bash
# Prime the GOLD once, on this workspace (stable context → gold-context.md)
golden_session prime --name ado-ready --cwd /opt/data/projects/ado-ready \
  --context-file /opt/data/projects/ado-ready/.claude/gold-context.md \
  --description "Azure DevOps work-item automation"

# Fork a task: read WI 238, download its attachment, emit artifacts — all under GS_RUN_DIR
golden_session run --name ado-ready \
  --run-dir /tmp/gs-runs/<id> \
  --task-template ado-workitem-task.md --param WORK_ITEM_ID=238
```

Each `run` forks a fresh child of the GOLD, so the GOLD stays pristine and tasks
never contaminate each other. `--run-dir` becomes `GS_RUN_DIR`, and a PreToolUse
hook (below) confines every write to it.

## Layout — what a fork inherits

| Path | Responsibility |
|---|---|
| `.claude/gold-context.md` | Stable priming context for `prime --context-file` (what this workspace is, which ADO org/project, where secrets live). |
| `.claude/settings.json` | Git-tracked config — the confine-writes hook, `permissions`, `enabledMcpjsonServers`. **No secrets.** |
| `.claude/settings.local.json` | Per-machine secrets — the `env` block only (`AZURE_DEVOPS_PAT`, org URL, project). Gitignored. |
| `.claude/confine_writes.py` | PreToolUse hook — blocks any `Write`/`Edit`/`MultiEdit` outside the task's `GS_RUN_DIR` (engine feature F12). Inherited by every fork; boundary is per-task. |
| `.claude/ado_download.py` | Authenticated attachment download — reads `AZURE_DEVOPS_PAT` from `os.environ` so no secret and no `$VAR` appears on a Bash line. |
| `.mcp.json` | Registers the `azure-devops` stdio MCP server (`@tiberriver256/mcp-server-azure-devops`) for reading work items, repos, pipelines, PRs. |
| `ado-workitem-task.md` | Parameterized task prompt (`${WORK_ITEM_ID}`) with the headless rules a fork must obey. |
| `src/`, `test/` | Sample extraction script and reference input/output artifacts from a prior run (illustrative, not part of the harness). |

## Why the output-isolation hook matters

Because the hook lives at the workspace `cwd`, **every** fork of the GOLD inherits
it — but the boundary it enforces (`GS_RUN_DIR`) is per-task. So one task's
downloaded CSVs and generated reports can never land in, or clobber, another's.
That turns output isolation from a prompt convention into an enforced guarantee.

Caveat: the hook guards the path-carrying edit tools only. A `Bash` command can
still write anywhere, so task prompts direct downloads at `GS_RUN_DIR` and the
GOLD keeps `Bash` out of `allowed_tools` when a hard boundary is required.

## Secrets architecture (where the PAT lives)

The PAT goes in **one** place: the `env` block of `.claude/settings.local.json`
(gitignored). It does **not** go in `.mcp.json`. Claude Code injects that `env`
block into its process; the MCP server inherits it as a child process, and the
fork's `python3`/Bash reads the same values via `os.environ`. Single source of
truth, never committed.

| File | Git-tracked? | Contents |
|------|:---:|----------|
| `.claude/settings.json` | **yes** | hooks, `permissions`, `enabledMcpjsonServers` — no secrets |
| `.claude/settings.local.json` | **no** | `env` block only: PAT, org URL, project |
| `.mcp.json` | **no** | server `command` + `args` only — no `env` block |

## Headless task-prompt rules

Forks run as headless `claude -p`, which has two behaviors that bite every
first-time task author — `ado-workitem-task.md` already encodes them:

1. **No `$VAR` in Bash commands.** Headless claude blocks any Bash line
   containing `$NAME` ("Contains simple_expansion"), regardless of the allow-list.
   Resolve env vars in Python instead:
   `python3 -c "import os; print(os.environ.get('GS_RUN_DIR'))"`.
2. **Authenticated network calls go in a helper.** Use `.claude/ado_download.py`
   (reads the PAT from `os.environ`) rather than an inline `curl -u ":$…"`, which
   would trip rule 1 and leak the secret.

See the engine's [`examples/workspace-template/README.md`](../sub-agents-on-hermes/examples/workspace-template/README.md)
for the full template rationale and the `docs/OUTPUT_ISOLATION.md` deep-dive.
