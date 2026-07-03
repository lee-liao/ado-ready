# Archived Work Items — ADO Pipeline Cron Automation (re-dated 2026-06-01 → 2026-06-02)

Archived from [`../scheduledTasksForFeatures.md`](../scheduledTasksForFeatures.md) on 2026-06-18.
These rows summarize the **ADO daily work-item routine automation** build (Feature
[`#180`](https://dev.azure.com/cubeforest3003/MDAI/_workitems/edit/180)) drawn from the
conversation log `output/setup-discord-bot/3026029b-…jsonl`. They were authored for reading
and understanding only — the dates were shifted to **2026-06-01 / 2026-06-02** so they never
collide with the live planner, and this file is **not** read by the routine.

The anchors are retained so the table renders as it did in the live planner.

## Work Items

<!-- WORKITEMS:START -->
| Date | Type | Title | Description | Assigned To | State | ID | Parent ID | Closing Note | Artifact |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-06-01 | User Story | Stand up the cross-project ADO daily work-item routine | As the modeling team, we need a scheduled routine that creates and closes ADO work items from a manually-edited markdown planner, so each day's work is tracked without manual ticket entry. | cubeforest3003@gmail.com |  |  | 180 |  |  |
| 2026-06-01 | Task | Scaffold the Python + thin-YAML routine for AM-create and PM-close | Build run_routine.py + ado_client (option 3 architecture): AM creates Story then Tasks/Bugs and sets them Active; PM closes them and commits the planner update | yuhuang.li.cloudalake@gmail.com |  |  |  |  |  |
| 2026-06-01 | Task | Run cross-project from the MDAI_POC pipeline targeting MDAI | Use pipeline definition id 2 in MDAI_POC to manage work items in project MDAI; add Phase (auto/am/pm) and Target-project parameters | cubeforest3003@gmail.com |  |  |  |  |  |
| 2026-06-01 | Task | Grant the build identity rights in MDAI and unlimit job-auth scope | Add MDAI_POC Build Service (cubeforest3003) to Contributors with work-item edit in project MDAI; turn off limit-job-authorization-scope-to-current-project | yuhuang.li.cloudalake@gmail.com |  |  |  |  |  |
| 2026-06-01 | Task | Design the manually-edited planner table | Rename amq4ScheduleTasks.md to docs/plans/scheduledTasksForFeatures.md; add a Feature-ID column and a git fetch + rebase before each commit | cubeforest3003@gmail.com |  |  |  |  |  |
| 2026-06-01 | Task | Design the artifact publishing flow + session summary | Files under docs/plans/artifact are copied into the MDAI repo on close (one commit); capture the session in docs/conversations-analysis ADO pipeline cron setup.html | yuhuang.li.cloudalake@gmail.com |  |  |  |  |  |
| 2026-06-01 | Bug | Push to MDAI repo rejected — TF401027 GenericContribute | Build identity lacked Git Contribute on the repo; 403 on git push | yuhuang.li.cloudalake@gmail.com |  |  |  | Resolved by setting Project Settings → MDAI → Repositories → Security → MDAI_POC Build Service (cubeforest3003) → Contribute = Allow. |  |
| 2026-06-01 | Bug | Pipeline General settings greyed out; job-auth scope limited to project | Cross-project work-item creation blocked because job authorization scope was confined to the current project | cubeforest3003@gmail.com |  |  |  | Turned off limit-job-authorization-scope-to-current-project for both non-release and release pipelines at the org/project level. |  |
| 2026-06-02 | User Story | Harden the routine and clean up mistaken work items | As the modeling team, we need the routine to stagger its operations, publish artifacts cross-project securely, and recover cleanly from mid-run failures, so daily runs are reliable and auditable. | yuhuang.li.cloudalake@gmail.com |  |  | 180 |  |  |
| 2026-06-02 | Task | Add random wait after kickoff and jitter between work-item operations | Items were all created at the same timestamp; add a post-trigger sleep plus a randomized gap between each create/close | cubeforest3003@gmail.com |  |  |  |  |  |
| 2026-06-02 | Task | Switch artifact publish auth to the MDAI_PAT secret | Add MDAI_PAT as a secret pipeline variable and authenticate the cross-project clone/push over HTTP Basic, since the build-service token lacks Read on the MDAI repo | yuhuang.li.cloudalake@gmail.com |  |  |  |  |  |
| 2026-06-02 | Task | Make the Closing Note optional and drop the auto-appended sentence | A blank Closing Note closes the item with no comment; remove the "Closed by daily routine on ..." sentence the routine had been adding | cubeforest3003@gmail.com |  |  |  |  |  |
| 2026-06-02 | Task | Append the day's events to the cron-setup analysis doc | Update docs/conversations-analysis ADO pipeline cron setup.html with the hardening and cleanup work | yuhuang.li.cloudalake@gmail.com |  |  |  |  |  |
| 2026-06-02 | Bug | PM run crashed — TF401019 MDAI repo not found during publish | publish_to_mdai failed to clone/push the MDAI repo with the build-service token | cubeforest3003@gmail.com |  |  |  | Build-service token lacks Read on the MDAI repo; switched publish auth to the MDAI_PAT secret over HTTP Basic. |  |
| 2026-06-02 | Bug | PM run crashed on git rebase — overlapping State=Closed conflict | The bot committed its State=Closed edit on a pre-edit snapshot, then rebase on origin/master hit a conflict on those same rows | yuhuang.li.cloudalake@gmail.com |  |  |  | Replaced the stale-snapshot commit with sync_planner_and_push: idempotently re-apply the routine's intent onto fresh origin so concurrent edits never conflict. |  |
| 2026-06-02 | Bug | Orphan and duplicate work items created by mistake | #156–#160 were created unlinked to a Feature; #166–#170 came from a stray GitHub workflow firing on the same scheduled items | cubeforest3003@gmail.com |  |  |  | Cleaned up #151–#160 (hard-deleted #160) and the #166–#170 set; disabled the duplicate GitHub workflow so a future push will not re-trigger it. |  |
<!-- WORKITEMS:END -->
