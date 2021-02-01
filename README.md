# qa-defect-tracker-cli

A lightweight command-line tool for logging, tracking, and reporting QA defects during manual testing cycles. Built for QA engineers who work without a full bug tracking system or need a fast local tracker during sprint cycles.

## Tech Stack

- Python 3.6
- stdlib only (`argparse`, `json`, `csv`, `uuid`, `datetime`)
- JSON flat-file storage

## Features

- Log defects with title, module, severity, steps to reproduce
- Update defect status with audit history
- Filter defects by status, severity, or module
- Generate text or CSV summary reports
- Highlights open critical defects in report

## Usage

```bash
# Log a new defect
python main.py log --title "Login fails on Safari" \
                   --module "Auth" \
                   --severity "high" \
                   --steps "Open Safari, go to /login, enter valid credentials" \
                   --expected "Redirect to dashboard" \
                   --actual "Page reloads with blank form"

# Update status
python main.py update --id DEF-0001 --status in_progress --comment "Dev picked up"

# List all open defects
python main.py list --status open

# List by module
python main.py list --module Auth

# Show full defect detail
python main.py show --id DEF-0001

# Generate summary report
python main.py report

# Export to CSV
python main.py report --format csv > defects_export.csv
```

## Defect Statuses

`open` → `in_progress` → `resolved` → `closed` | `reopened`

## Severity Levels

`low` | `medium` | `high` | `critical`

## Data Storage

Defects are saved in `data/defects.json`. Each defect includes a full status history with timestamps.
# readme
