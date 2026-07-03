import csv
import re
from pathlib import Path

src = Path("/home/lee/projects/ado-ready/test/input/scheduledTasksForFeatures-ado-automation-2026-06-01_2026-06-02.md")
dst = Path("/home/lee/projects/ado-ready/test/out/work-items.csv")

text = src.read_text(encoding="utf-8")

m = re.search(r"<!--\s*WORKITEMS:START\s*-->(.*?)<!--\s*WORKITEMS:END\s*-->", text, re.S)
if not m:
    raise SystemExit("Could not find Work Items table between markers")

table = m.group(1).strip()
lines = [ln for ln in table.splitlines() if ln.strip().startswith("|")]

def parse_row(line):
    # strip leading/trailing pipe, split on pipe, strip whitespace
    parts = line.strip().strip("|").split("|")
    return [p.strip() for p in parts]

rows = [parse_row(ln) for ln in lines]
header = rows[0]
data = [r for r in rows[1:] if not all(set(c) <= set("-: ") for c in r)]

dst.parent.mkdir(parents=True, exist_ok=True)
with dst.open("w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, quoting=csv.QUOTE_MINIMAL, lineterminator="\r\n")
    w.writerow(header)
    w.writerows(data)

print(f"Wrote {len(data)} data rows + header to {dst}")
print(f"Columns: {header}")
