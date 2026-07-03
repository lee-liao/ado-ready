# Report — Work Item 237

## Source work item

- **ADO ID:** 237 (Task, project `pbipExercise1`)
- **Title / Description:** please extract the "Work Item" table in the attached markdown file to csv file
- **Parent:** 19
- **Attachment:** `scheduledTasksForFeatures-ado-automation-2026-06-01_2026-06-02.md` (5896 bytes), downloaded to `test/input/`.

## What was done

1. Read work item 237 via the Azure DevOps MCP tools and pulled its single attachment.
2. Downloaded the attachment to `test/input/scheduledTasksForFeatures-ado-automation-2026-06-01_2026-06-02.md` (verified size 5896 bytes against the work item's `resourceSize`).
3. The markdown contains exactly one table — the "Work Items" table — bounded by `<!-- WORKITEMS:START -->` / `<!-- WORKITEMS:END -->` markers under the `## Work Items` heading. That is the table the Description refers to.
4. Parsed the table and wrote it to `test/out/work-items.csv` using Python's `csv` module with `QUOTE_MINIMAL`, so any field containing a comma, double-quote, or line break is RFC 4180-quoted (CRLF line terminator).

## Output

- **`test/out/work-items.csv`** — 1 header row + 16 data rows, 10 columns.

### Columns

`Date`, `Type`, `Title`, `Description`, `Assigned To`, `State`, `ID`, `Parent ID`, `Closing Note`, `Artifact`

### Row distribution

- By type: User Story ×2, Task ×9, Bug ×5
- By date: 2026-06-01 ×8, 2026-06-02 ×8

### Notes on the source data

- The source table's header has 10 columns, but only `Date`, `Type`, `Title`, `Description`, `Assigned To`, and (sometimes) `Parent ID` / `Closing Note` are populated. `State`, `ID`, and `Artifact` are empty in every row — the planner reserves them for the routine to fill in. Those empty fields are preserved as empty CSV cells so the column structure matches the source.
- One Title contains a literal double-quoted phrase (`"Closed by daily routine on ..."`); it is escaped per RFC 4180 by doubling the quotes inside a quoted field.
- The em-dash (—) and en-dash (–) characters in some Bug rows are preserved as-is in UTF-8.

## Files written

```
test/input/scheduledTasksForFeatures-ado-automation-2026-06-01_2026-06-02.md   (downloaded attachment)
test/out/work-items.csv                                                         (extracted table)
test/out/report.md                                                              (this report)
```
