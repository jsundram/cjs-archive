#!/usr/bin/env python3
"""
Master build script for CJS Archive site.

This script:
1. Runs all CSV-to-HTML conversion scripts
2. Collects Document objects from each script
3. Saves a master document registry as JSON
"""

import importlib.util
import json
from dataclasses import asdict
from pathlib import Path


def import_module(name, filepath):
    """Import a module from a file path (handles hyphenated filenames)."""
    spec = importlib.util.spec_from_file_location(name, filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    """Build entire site and generate document registry."""

    # List of all page generation scripts with their parameters
    scripts = [
        {
            'name': 'cqc-reports',
            'file': 'cqc-reports.py',
            'args': ['../data/cqc-reports.csv', '../data/cqc-reports-matching.csv',
                     'cqc-reports-content.html', '../docs/cqc-reports.html']
        },
        {
            'name': 'savp',
            'file': 'savp-csv-to-table.py',
            'args': ['../data/savp.csv', 'savp-content.html', '../docs/special-advisor.html']
        },
        {
            'name': 'blackman',
            'file': 'blackman-csv-to-table.py',
            'args': ['../data/blackman.csv', 'blackman-content.html', '../docs/blackman.html']
        },
        {
            'name': 'otoole',
            'file': 'otoole-csv-to-table.py',
            'args': ['../data/otoole.csv', 'otoole-content.html', '../docs/otoole.html']
        },
        {
            'name': 'otoole-timeline',
            'file': 'otoole-timeline-csv-to-table.py',
            'args': ['../data/otoole-timeline.csv', 'otoole-timeline-content.html',
                     '../docs/otoole-timeline.html']
        },
        {
            'name': 'cqc-media',
            'file': 'cqc-media-csv-to-table.py',
            'args': ['../data/CQC-Coverage.csv', 'cqc-media-content.html', '../docs/cqc-media.html']
        },
        {
            'name': 'cqc-publications',
            'file': 'cqc-publications-csv-to-table.py',
            'args': ['../data/CQC-Publications.csv', 'cqc-publications-content.html',
                     '../docs/cqc-publications.html']
        }
    ]

    all_documents = []

    print("Generating static pages...\n")

    # Generate static pages first (index, cqc, court-monitor)
    generate_static = import_module('generate_static_pages', 'generate-static-pages.py')
    generate_static.main()

    print("\nBuilding site pages and collecting documents...\n")

    for script_info in scripts:
        print(f"Running {script_info['name']}...")

        # Import the module
        module = import_module(script_info['name'], script_info['file'])

        # Call main() and collect documents
        documents = module.main(*script_info['args'])
        all_documents.extend(documents)

        print(f"  ✅ Generated {len(documents)} documents\n")

    # Save document registry as JSON
    registry_path = Path('../data/document-registry.json')

    # Convert Document objects to dictionaries for JSON serialization
    registry_data = [asdict(doc) for doc in all_documents]

    with open(registry_path, 'w', encoding='utf-8') as f:
        json.dump(registry_data, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"Generating document landing pages...")
    print(f"{'='*60}\n")

    # Generate document landing pages
    generate_pages = import_module('generate_document_pages', 'generate-document-pages.py')
    generate_pages.main()

    print(f"\n{'='*60}")
    print(f"Building search index...")
    print(f"{'='*60}\n")

    # Build search index
    build_search = import_module('build_search_index', 'build-search-index.py')
    build_search.main()

    print(f"\n{'='*60}")
    print(f"Generating sitemap...")
    print(f"{'='*60}\n")

    # Generate sitemap
    generate_sitemap = import_module('generate_sitemap', 'generate-sitemap.py')
    generate_sitemap.generate_sitemap()

    print(f"\n{'='*60}")
    print(f"Build complete!")
    print(f"{'='*60}")
    print(f"Total documents: {len(all_documents)}")
    print(f"Document registry saved to: {registry_path}")

    # Print breakdown by section
    sections = {}
    for doc in all_documents:
        sections[doc.section] = sections.get(doc.section, 0) + 1

    print(f"\nDocuments by section:")
    for section, count in sorted(sections.items()):
        print(f"  {section}: {count}")


if __name__ == '__main__':
    main()
