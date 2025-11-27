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

### Template System

The site uses a DRY template composition system:

- **`base-template.html`**: Master template with navigation, header, search bar, and scripts
- **Content templates**: Separate HTML files containing page-specific content with `{rows}` placeholders
  - Static pages: `index-content.html`, `cqc-content.html`, `court-monitor-content.html`, `404-content.html`
  - Table pages: `cqc-reports-content.html`, `savp-content.html`, `blackman-content.html`, etc.
- **Python scripts**: Load content template + base template, populate with data, generate final HTML

All pages use:
- Tailwind CSS (loaded via CDN)
- Custom fonts from Google Fonts
- MiniSearch for client-side search functionality
- Consistent navigation and styling

### Build Process

**Main build script**: `build-site.py` orchestrates the entire build:

1. **Generate static pages** (`generate-static-pages.py`)
   - Combines content templates with base template
   - Creates: index.html, cqc.html, court-monitor.html, 404.html

2. **Generate table-based pages** (CSV-to-table scripts)
   - Read CSV data
   - Generate HTML table rows
   - Combine with content templates and base template
   - Copy PDF assets from Dropbox to `docs/assets/`

3. **Generate document landing pages** (`generate-document-pages.py`)
   - Creates 337+ individual landing pages for each document
   - Uses base template with programmatic content
   - Provides metadata, description, and direct links

4. **Build search index** (`build-search-index.py`)
   - Creates `search-index.json` for MiniSearch
   - Indexes all 337+ documents with metadata

5. **Generate sitemap** (`generate-sitemap.py`)
   - Creates `sitemap.xml` with 455+ URLs
   - Includes main pages, document pages, and PDF files

### Key Scripts

#### Static Page Generator
- **`generate-static-pages.py`**: Generates static pages from content templates

#### CSV-to-Table Generators
All follow the same pattern: read CSV + content template → generate HTML + copy assets

- **`cqc-reports.py`**: Generates `cqc-reports.html` from CQC Reports CSV
  - Matches titles to PDF files using `cqc-reports-matching.csv`
  - Copies PDFs from Dropbox to `docs/assets/cqc/`
  - Handles both local files and external URLs

- **`savp-csv-to-table.py`**: Generates `special-advisor.html` from SAVP CSV
  - Copies PDFs from Dropbox to `docs/assets/savp/`

- **`blackman-csv-to-table.py`**: Generates `blackman.html` from Blackman CSV
  - Copies PDFs from Dropbox to `docs/assets/blackman/`

- **`otoole-csv-to-table.py`**: Generates `otoole.html` from O'Toole CSV

- **`otoole-timeline-csv-to-table.py`**: Generates `otoole-timeline.html`

- **`cqc-media-csv-to-table.py`**: Generates `cqc-media.html`

- **`cqc-publications-csv-to-table.py`**: Generates `cqc-publications.html`

#### Support Scripts
- **`document_schema.py`**: Defines Document dataclass and slug generation
- **`check-pdf-text.py`**: Utility to verify PDFs have searchable text (for SEO)

### File Matching Logic (CQC Reports)

The CQC reports script uses a two-stage matching process:
1. Look up title in `cqc-reports-matching.csv` for explicit filename/URL mapping
2. Fallback to case-insensitive filename search in Dropbox folder
3. Skip entries without matches (prints warning)

## Common Commands

### Full Site Build

Run from `./scripts/` directory:

```bash
cd scripts
python3 build-site.py
```

This runs all generators in the correct order and produces:
- 10 main HTML pages
- 337+ document landing pages
- Search index
- Sitemap

### Individual Page Generation

For development/debugging, you can run individual generators:

```bash
cd scripts
python3 cqc-reports.py
python3 savp-csv-to-table.py
# etc.
```

### Dependencies

Install required Python packages:

```bash
cd scripts
pip install -r requirements.txt
```

Required packages:
- `dateparser` - For parsing various date formats from CSVs

Standard library dependencies: `csv`, `os`, `shutil`, `json`, `pathlib`, `datetime`

## Important Notes

### Asset Paths

Scripts reference hardcoded Dropbox paths for PDF assets:
- CQC: `/Users/jsundram/Dropbox/Archive of CJS/CQC Reports/`
- SAVP: `/Users/jsundram/Dropbox/Archive of CJS/Special Advisor/`
- Court Monitor Blackman: `/Users/jsundram/Dropbox/Archive of CJS/Court Monitor/Blackman Jones/`
- Court Monitor O'Toole: `/Users/jsundram/Dropbox/Archive of CJS/Court Monitor/O'Toole v. Cuomo/`

**These paths must exist on the system running the scripts.** Update the `assets_origin` variable in each script for your local environment.

### CSV Preprocessing

CSVs often need manual cleanup before processing:
- Fix smart quotes (single and double) to regular quotes
- Fix date formatting inconsistencies
- Some CSVs have header rows that must be skipped (see script comments)

Use vim commands like `:FixDoc` to clean up smart quotes.

### Date Formatting

- CQC reports: Displays as "Month Year" (e.g., "January 2020")
- Other pages: Displays as "YYYY-MM-DD"

### File Naming Conventions

PDF filenames are normalized:
- Lowercased
- Colons replaced with hyphens
- `.pdf` extension added

### Search Functionality

- Client-side search using MiniSearch library
- Search bar in navigation (base template)
- Searches across all 337+ documents
- Indexes: title, description, category, section

### Document Schema

All documents follow a standard schema defined in `document_schema.py`:
- `title`: Document title
- `section`: Which section (cqc-reports, savp, blackman, otoole, etc.)
- `url`: Link to PDF or external resource
- `date`: Publication/creation date
- `description`: Document description
- `category`: Document type/category
- `slug`: URL-safe identifier (auto-generated, unique per section)
- `document_url`: Path to generated landing page
- `file_path`: Local path to PDF asset (if applicable)
- `source`: Source publication (for media/publications)

Documents are saved to `data/document-registry.json` during build.
