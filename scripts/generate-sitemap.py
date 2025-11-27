#!/usr/bin/env python3
"""
Generate comprehensive sitemap including HTML pages, document landing pages, and PDFs
"""
import os
import json
from datetime import datetime
from pathlib import Path
from html import escape

# Base configuration
SITE_URL = "https://clarencesundram.org"
DOCS_DIR = Path(__file__).parent.parent / "docs"
DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUT_FILE = DOCS_DIR / "sitemap.xml"

# Main HTML pages with their priorities
HTML_PAGES = [
    ("index.html", 1.0, "monthly"),
    ("cqc.html", 0.9, "monthly"),
    ("cqc-reports.html", 0.8, "monthly"),
    ("cqc-media.html", 0.8, "monthly"),
    ("cqc-publications.html", 0.8, "monthly"),
    ("special-advisor.html", 0.9, "monthly"),
    ("court-monitor.html", 0.9, "monthly"),
    ("otoole.html", 0.8, "monthly"),
    ("otoole-timeline.html", 0.7, "monthly"),
    ("blackman.html", 0.8, "monthly"),
]


def get_file_date(filepath):
    """Get file modification date in YYYY-MM-DD format"""
    timestamp = os.path.getmtime(filepath)
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")


def generate_sitemap():
    """Generate complete sitemap with HTML pages, document landing pages, and PDFs"""

    urls = []

    # Add main HTML pages
    print("Adding main HTML pages...")
    for page, priority, changefreq in HTML_PAGES:
        filepath = DOCS_DIR / page
        if filepath.exists():
            lastmod = get_file_date(filepath)
            urls.append({
                'loc': f"{SITE_URL}/{page}",
                'lastmod': lastmod,
                'priority': priority,
                'changefreq': changefreq
            })
            print(f"  ✓ {page}")

    # Add document landing pages from registry
    print("\nAdding document landing pages...")
    registry_path = DATA_DIR / "document-registry.json"
    doc_count = 0
    if registry_path.exists():
        with open(registry_path, 'r', encoding='utf-8') as f:
            documents = json.load(f)

        for doc in documents:
            doc_url = doc['document_url']
            filepath = DOCS_DIR / doc_url
            if filepath.exists():
                lastmod = get_file_date(filepath)
                urls.append({
                    'loc': f"{SITE_URL}/{doc_url}",
                    'lastmod': lastmod,
                    'priority': 0.7,
                    'changefreq': 'monthly'
                })
                doc_count += 1

        print(f"  ✓ Added {doc_count} document pages")
    else:
        print(f"  ⚠ Document registry not found at {registry_path}")

    # Add PDFs
    print("\nAdding PDF files...")
    pdf_count = 0
    for pdf_path in sorted(DOCS_DIR.glob("assets/**/*.pdf")):
        # Get relative path from docs directory
        rel_path = pdf_path.relative_to(DOCS_DIR)
        # Convert to URL path
        url_path = str(rel_path).replace(" ", "%20")

        lastmod = get_file_date(pdf_path)
        urls.append({
            'loc': f"{SITE_URL}/{url_path}",
            'lastmod': lastmod,
            'priority': 0.6,
            'changefreq': 'yearly'
        })
        pdf_count += 1

    print(f"  ✓ Added {pdf_count} PDFs")

    # Generate XML
    print("\nGenerating sitemap XML...")
    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for url in urls:
        xml_lines.append('  <url>')
        xml_lines.append(f'    <loc>{escape(url["loc"])}</loc>')
        xml_lines.append(f'    <lastmod>{url["lastmod"]}</lastmod>')
        xml_lines.append(f'    <changefreq>{url["changefreq"]}</changefreq>')
        xml_lines.append(f'    <priority>{url["priority"]}</priority>')
        xml_lines.append('  </url>')

    xml_lines.append('</urlset>')

    # Write to file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml_lines))

    print(f"\n✅ Sitemap generated: {OUTPUT_FILE}")
    print(f"   Total URLs: {len(urls)}")
    print(f"   - Main pages: {len(HTML_PAGES)}")
    print(f"   - Document pages: {doc_count}")
    print(f"   - PDFs: {pdf_count}")


if __name__ == "__main__":
    generate_sitemap()
