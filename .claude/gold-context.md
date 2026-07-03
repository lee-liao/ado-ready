This is the ado-ready workspace for Azure DevOps integration testing.

The workspace is a git repo at /opt/data/projects/ado-ready. An Azure DevOps
MCP server (name: azure-devops, package: @tiberriver256/mcp-server-azure-devops)
is registered in .mcp.json and exposes tools for reading work items, repositories,
pipelines, and pull requests from the cubeforest3003 organization (project
powerBI-demo).

The AZURE_DEVOPS_PAT and AZURE_DEVOPS_ORG_URL environment variables are available
to Bash commands; use them for direct REST API calls (e.g. downloading work item
attachments via curl) since the MCP server has no attachment-download tool.

A PreToolUse hook (.claude/confine_writes.py) confines all Write/Edit/MultiEdit
calls to the current task's GS_RUN_DIR. Always write under $GS_RUN_DIR.
