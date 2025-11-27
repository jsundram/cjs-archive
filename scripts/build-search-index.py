#!/usr/bin/env python3
"""
Build search index from document registry for MiniSearch.

This script creates a JSON file optimized for client-side search using MiniSearch.
"""

import json
from pathlib import Path


def main():
    """Build search index from document registry."""

    # Load document registry
    registry_path = Path('../data/document-registry.json')
    with open(registry_path, 'r', encoding='utf-8') as f:
        documents = json.load(f)

    # Build search index
    search_index = []

    for doc in documents:
        # Create search document
        # MiniSearch will search title, description, and category by default
        search_doc = {
            'id': f"{doc['section']}-{doc['slug']}",
            'title': doc['title'],
            'description': doc.get('description', ''),
            'category': doc.get('category', ''),
            'date': doc.get('date', ''),
            'section': doc['section'],
            'source': doc.get('source', ''),
            'url': doc['document_url']  # URL to the landing page
        }

        search_index.append(search_doc)

    # Save search index
    output_path = Path('../docs/search-index.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(search_index, f, indent=2, ensure_ascii=False)

    print(f"{'='*60}")
    print(f"Search index created!")
    print(f"{'='*60}")
    print(f"Total searchable documents: {len(search_index)}")
    print(f"Index saved to: {output_path}")

    # Show breakdown by section
    sections = {}
    for doc in search_index:
        sections[doc['section']] = sections.get(doc['section'], 0) + 1

    print(f"\nDocuments by section:")
    for section, count in sorted(sections.items()):
        print(f"  {section}: {count}")


if __name__ == '__main__':
    main()
