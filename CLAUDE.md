# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Static website archive for Clarence J. Sundram, displaying his professional work across multiple roles:
- **CQC** (Commission on Quality of Care): Reports, media coverage, and publications
- **Special Advisor**: Various advisory work and publications
- **Court Monitor**: Documents for O'Toole and Blackman-Jones cases

The site is deployed to GitHub Pages at clarencesundram.org.

## Architecture

### Content Pipeline

Data flows from Google Sheets → CSV exports → Python scripts → HTML pages:

1. **Source**: Google Sheets maintained in Dropbox (see README.md for links)
2. **Data**: CSV files exported to `./data/`
3. **Scripts**: Python generators in `./scripts/` combine CSV data with HTML templates
4. **Output**: Static HTML pages in `./docs/` (GitHub Pages root)

### Key Scripts

All scripts follow the same pattern: read CSV + template → generate HTML + copy assets

- `cqc-reports.py`: Generates `cqc-reports.html` from CQC Reports CSV
  - Matches titles to PDF files using `CQC-Reports-matching.csv`
  - Copies PDFs from Dropbox to `docs/assets/cqc/`
  - Handles both local files and external URLs

- `savp-csv-to-table.py`: Generates `special-advisor.html` from SAVP CSV
  - Copies PDFs from Dropbox to `docs/assets/savp/`

- `blackman-csv-to-table.py`: Generates `blackman.html` from Blackman CSV
  - Copies PDFs from Dropbox to `docs/assets/blackman/`

- `otoole-csv-to-table.py`: Generates `otoole.html` from O'Toole CSV
  - Similar structure to Blackman script

### File Matching Logic (CQC Reports)

The CQC reports script uses a two-stage matching process:
1. Look up title in `CQC-Reports-matching.csv` for explicit filename/URL mapping
2. Fallback to case-insensitive filename search in Dropbox folder
3. Skip entries without matches

### Template System

HTML templates in `./scripts/` contain `{rows}` placeholder that gets replaced with generated table rows. Templates use:
- Tailwind CSS (loaded via CDN)
- Custom fonts from Google Fonts
- Consistent styling across all pages

## Common Commands

### Generate HTML Pages

Run from `./scripts/` directory:

```bash
cd scripts
python cqc-reports.py
python savp-csv-to-table.py
python blackman-csv-to-table.py
python otoole-csv-to-table.py
```

Each script:
- Reads CSV from `../data/`
- Reads template from `./scripts/`
- Writes HTML to `../docs/`
- Copies referenced PDFs to `../docs/assets/[section]/`

### Dependencies

Python scripts require:
- `dateparser` library for parsing various date formats
- Standard library: `csv`, `os`, `shutil`

## Important Notes

### Asset Paths

Scripts reference hardcoded Dropbox paths:
- CQC: `/Users/jsundram/Dropbox/Archive of CJS/CQC Reports/`
- SAVP: `/Users/jsundram/Dropbox/Archive of CJS/Special Advisor/`
- Court Monitor: `/Users/jsundram/Dropbox/Archive of CJS/Court Monitor/`

These paths must exist on the system running the scripts.

### CSV Preprocessing

CSVs often need manual cleanup before processing:
- Fix smart quotes (single and double) to regular quotes
- Fix date formatting inconsistencies
- Some CSVs have header rows that must be skipped (see script comments)

### Date Formatting

- CQC reports: Displays as "Month Year" (e.g., "January 2020")
- Other pages: Displays as "YYYY-MM-DD"

### File Naming Conventions

PDF filenames are normalized:
- Lowercased
- Colons replaced with hyphens
- `.pdf` extension added
