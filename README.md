# CJS Archive

A static website archive of professional work by Clarence J. Sundram, documenting his career as:
- Chairman of the New York State Commission on Quality of Care for the Mentally Disabled
- Special Advisor to the Governor on the Mentally Disabled
- Court-appointed Monitor in landmark civil rights cases

**Live site**: [clarencesundram.org](https://clarencesundram.org)

## Overview

This is a Python-based static site generator that transforms CSV data exports into a searchable archive with 337+ documents, SEO-optimized landing pages, and client-side search functionality.

## Architecture

### Data Flow

```
Google Sheets (source of truth)
    ↓ (manual export)
CSV files (./data/)
    ↓ (Python scripts)
HTML pages + Search Index + Sitemap
    ↓ (git commit)
GitHub Pages (clarencesundram.org)
```

### Content Pipeline

1. **Source Data**: Google Sheets maintained in Dropbox
   - [CQC Spreadsheet](https://docs.google.com/spreadsheets/d/1FEB-TLPxuc_buzlWEIJzNzch9QWkWWil/edit?gid=1637828733#gid=1637828733) - Reports, media coverage, publications
   - Additional spreadsheets for Special Advisor work and Court Monitor cases

2. **CSV Exports**: Exported to `./data/` directory
   - `cqc-reports.csv` - CQC reports with file matching logic
   - `cqc-reports-matching.csv` - Maps titles to PDF files/URLs
   - `CQC-Coverage.csv` - Media coverage
   - `CQC-Publications.csv` - Publications
   - `savp.csv` - Special Advisor publications
   - `blackman.csv` - Blackman v. Rowland court monitor reports
   - `otoole.csv` - O'Toole v. Cuomo court monitor reports
   - `otoole-timeline.csv` - Timeline of O'Toole case events

3. **PDF Assets**: Stored in Dropbox, copied during build
   - Source: `/Users/jsundram/Dropbox/Archive of CJS/`
   - Destination: `./docs/assets/[section]/`
   - **Note**: Update the `assets_origin` paths in Python scripts for your local system

4. **Generated Output**: Static HTML in `./docs/` (GitHub Pages root)
   - 10 main pages (index, section pages, 404)
   - 337+ document landing pages
   - Search index (`search-index.json`)
   - XML sitemap (455+ URLs)

### Template System

The site uses a DRY template composition approach:

- **Base Template** (`base-template.html`): Master template with navigation, search bar, fonts, and scripts
- **Content Templates** (`*-content.html`): Page-specific HTML with `{rows}` placeholders
- **Python Scripts**: Combine content + base template, populate with CSV data

All pages include:
- Tailwind CSS (CDN)
- MiniSearch for client-side search
- Responsive design
- SEO metadata

## Setup

### Prerequisites

- Python 3.7+
- Access to Dropbox folder with PDF assets (for building from source)

### Installation

```bash
# Clone the repository
git clone https://github.com/jsundram/cjs-archive.git
cd cjs-archive

# Install dependencies
cd scripts
pip install -r requirements.txt
```

## Build Process

### Full Site Build

```bash
cd scripts
python3 build-site.py
```

This orchestrates the complete build:

1. **Static Pages** - Generates index, CQC overview, Court Monitor overview, 404
2. **CSV-to-Table Pages** - Processes 7 CSV files to create table-based pages
3. **Document Landing Pages** - Creates 337+ individual document pages
4. **Search Index** - Builds searchable JSON index
5. **Sitemap** - Generates XML sitemap with all URLs

### Individual Script Execution

For development or debugging, run individual generators:

```bash
# Generate specific pages
python3 cqc-reports.py
python3 savp-csv-to-table.py
python3 blackman-csv-to-table.py
python3 otoole-csv-to-table.py

# Generate static pages
python3 generate-static-pages.py

# Generate document landing pages
python3 generate-document-pages.py

# Build search index
python3 build-search-index.py

# Generate sitemap
python3 generate-sitemap.py
```

### Build Output

```
docs/
├── index.html                    # Biography/about page
├── cqc.html                      # CQC overview
├── cqc-reports.html             # CQC reports table
├── cqc-media.html               # CQC media coverage table
├── cqc-publications.html        # CQC publications table
├── special-advisor.html         # Special Advisor publications
├── court-monitor.html           # Court Monitor overview
├── otoole.html                  # O'Toole case reports
├── otoole-timeline.html         # O'Toole timeline
├── blackman.html                # Blackman case reports
├── 404.html                     # Error page
├── sitemap.xml                  # XML sitemap
├── search-index.json            # Search index
├── documents/                   # 337+ document landing pages
│   ├── cqc-reports-*.html
│   ├── savp-*.html
│   ├── blackman-*.html
│   └── otoole-*.html
└── assets/                      # PDF files
    ├── cqc/
    ├── savp/
    ├── blackman/
    └── otoole/
```

## Key Scripts

| Script | Purpose |
|--------|---------|
| `build-site.py` | Master build orchestrator |
| `generate-static-pages.py` | Generates static pages from content templates |
| `cqc-reports.py` | Generates CQC reports page with file matching logic |
| `cqc-media-csv-to-table.py` | Generates CQC media coverage page |
| `cqc-publications-csv-to-table.py` | Generates CQC publications page |
| `savp-csv-to-table.py` | Generates Special Advisor page |
| `blackman-csv-to-table.py` | Generates Blackman v. Rowland page |
| `otoole-csv-to-table.py` | Generates O'Toole v. Cuomo page |
| `otoole-timeline-csv-to-table.py` | Generates O'Toole timeline page |
| `generate-document-pages.py` | Generates individual document landing pages |
| `build-search-index.py` | Creates MiniSearch index |
| `generate-sitemap.py` | Generates XML sitemap |
| `document_schema.py` | Document data model and slug generation |
| `check-pdf-text.py` | Utility to verify PDFs have searchable text |

## Updating Content

1. **Edit Google Sheets** - Update source data in Google Sheets
2. **Export to CSV** - Download sheets as CSV to `./data/` directory
3. **Clean CSV** - Fix smart quotes, date formats (see CLAUDE.md)
4. **Run Build** - Execute `python3 build-site.py`
5. **Review Changes** - Check generated HTML in `./docs/`
6. **Commit & Push** - Git commit and push to deploy via GitHub Pages

## Deployment

The site is deployed via GitHub Pages:
- **Source**: `docs/` folder in `main` branch
- **Domain**: clarencesundram.org (configured via CNAME)
- **Automatic**: Pushes to `main` deploy automatically

## Features

- **Search**: Client-side full-text search across all 337+ documents
- **SEO**: Individual landing pages for each document with metadata
- **Sitemap**: Comprehensive XML sitemap for search engines
- **Responsive**: Mobile-friendly design using Tailwind CSS
- **Accessible**: Semantic HTML with proper heading structure
- **Fast**: Static HTML with no server-side processing

## File Matching Logic (CQC Reports)

CQC reports use a two-stage file matching process:

1. **Explicit Matching**: Look up title in `cqc-reports-matching.csv`
   - Contains manual mappings of titles → filenames or URLs
   - Handles special cases and external links

2. **Automatic Matching**: Case-insensitive filename search in Dropbox
   - Normalizes filenames (lowercase, replace `:` with `-`)
   - Searches for `[title].pdf` in Dropbox folder

3. **Fallback**: Skip entries without matches (prints warning)

## Document Schema

Each document in the registry includes:
- `title` - Document title
- `section` - Category (cqc-reports, savp, blackman, otoole, etc.)
- `url` - Link to PDF or external resource
- `date` - Publication/event date
- `description` - Document description
- `category` - Document type
- `slug` - URL-safe identifier (auto-generated, unique per section)
- `document_url` - Path to generated landing page
- `file_path` - Local path to PDF asset (if applicable)
- `source` - Source publication (for media/publications)

Registry saved to `data/document-registry.json` during build.

## Contributing

For detailed development guidance, see [CLAUDE.md](./CLAUDE.md).

## License

Content © Clarence J. Sundram. All rights reserved.
