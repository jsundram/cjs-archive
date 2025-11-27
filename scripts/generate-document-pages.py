#!/usr/bin/env python3
"""
Generate individual landing pages for each document from the document registry.
"""

import json
import os
from pathlib import Path


# Map section IDs to their display names and page URLs
SECTION_CONFIG = {
    'cqc-reports': {
        'name': 'CQC Reports',
        'page': 'cqc-reports.html'
    },
    'cqc-media': {
        'name': 'CQC Media Coverage',
        'page': 'cqc-media.html'
    },
    'cqc-publications': {
        'name': 'CQC Publications',
        'page': 'cqc-publications.html'
    },
    'savp': {
        'name': 'Special Advisor to the Governor',
        'page': 'special-advisor.html'
    },
    'blackman': {
        'name': 'Blackman v. Rowland',
        'page': 'blackman.html'
    },
    'otoole': {
        'name': "O'Toole v. Cuomo",
        'page': 'otoole.html'
    },
    'otoole-timeline': {
        'name': "O'Toole v. Cuomo Timeline",
        'page': 'otoole-timeline.html'
    }
}


def truncate_description(text, max_length=155):
    """Truncate description for meta tag (Google shows ~155-160 characters)."""
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(' ', 1)[0] + '...'


def generate_document_page(doc, template):
    """Generate HTML for a single document page."""

    section_info = SECTION_CONFIG.get(doc['section'], {
        'name': doc['section'].title(),
        'page': f"{doc['section']}.html"
    })

    # Build metadata display
    metadata_items = []
    if doc.get('date'):
        metadata_items.append(f'''
                <div class="flex items-center gap-2">
                  <p class="text-[#58728d] text-sm font-medium">Date:</p>
                  <p class="text-[#101419] text-sm">{doc['date']}</p>
                </div>''')

    if doc.get('category'):
        metadata_items.append(f'''
                <div class="flex items-center gap-2">
                  <p class="text-[#58728d] text-sm font-medium">Category:</p>
                  <button class="flex min-w-[84px] cursor-pointer items-center justify-center overflow-hidden rounded-full h-8 px-4 bg-[#e9edf1] text-[#101419] text-sm font-medium leading-normal">
                    <span class="truncate">{doc['category']}</span>
                  </button>
                </div>''')

    if doc.get('source'):
        metadata_items.append(f'''
                <div class="flex items-center gap-2">
                  <p class="text-[#58728d] text-sm font-medium">Source:</p>
                  <p class="text-[#101419] text-sm">{doc['source']}</p>
                </div>''')

    metadata_html = '\n'.join(metadata_items)

    description_html = ''
    if doc.get('description'):
        description_html = f'''
              <div class="flex flex-col gap-2">
                <p class="text-[#58728d] text-sm font-medium">Description</p>
                <p class="text-[#101419] text-base leading-relaxed">{doc['description']}</p>
              </div>'''

    # Build breadcrumb
    breadcrumb = f'''
        <div class="bg-white border-b border-solid border-b-[#e9edf1] px-10 py-3">
          <div class="flex items-center gap-2 text-sm">
            <a href="../{section_info['page']}" class="text-[#58728d] hover:text-[#0066cc]">{section_info['name']}</a>
            <span class="text-[#58728d]">/</span>
            <span class="text-[#101419]">Document</span>
          </div>
        </div>'''

    # Build content
    content = f'''
        <div class="px-40 flex flex-1 justify-center py-5">
          <div class="layout-content-container flex flex-col max-w-[960px] flex-1">
            <div class="flex flex-col gap-6 px-4 py-6">
              <h1 class="text-[#101419] text-4xl font-bold leading-tight tracking-[-0.015em]">{doc['title']}</h1>
              <div class="flex flex-wrap gap-4">
                {metadata_html}
              </div>
              {description_html}
              <div class="flex gap-3 flex-wrap">
                <a href="{doc['url']}" target="_blank"
                   class="flex min-w-[200px] max-w-[400px] cursor-pointer items-center justify-center overflow-hidden rounded-full h-12 px-6 bg-[#1971c2] text-white text-base font-bold leading-normal tracking-[0.015em] hover:bg-[#1864ab] transition-colors">
                  <span class="truncate">View Document</span>
                </a>
                <a href="../{section_info['page']}"
                   class="flex min-w-[200px] max-w-[400px] cursor-pointer items-center justify-center overflow-hidden rounded-full h-12 px-6 bg-[#e9edf1] text-[#101419] text-base font-bold leading-normal tracking-[0.015em] hover:bg-[#d3dbe4] transition-colors">
                  <span class="truncate">Back to {section_info['name']}</span>
                </a>
              </div>
            </div>
          </div>
        </div>'''

    # Create meta description
    meta_description = doc.get('description', doc['title'])
    meta_description = truncate_description(meta_description)

    # Populate base template
    html = template.replace('{meta_title}', doc['title'])
    html = html.replace('{meta_description}', meta_description)
    html = html.replace('{canonical_url}', doc['document_url'])
    html = html.replace('{breadcrumb}', breadcrumb)
    html = html.replace('{page_title}', '')  # No duplicate page title for document pages
    html = html.replace('{content}', content)
    html = html.replace('{path_prefix}', '../')

    return html


def main():
    """Generate all document landing pages."""

    # Load document registry
    registry_path = Path('../data/document-registry.json')
    with open(registry_path, 'r', encoding='utf-8') as f:
        documents = json.load(f)

    # Load base template
    template_path = Path('base-template.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    # Create output directory
    output_dir = Path('../docs/documents')
    output_dir.mkdir(exist_ok=True)

    print(f"Generating document landing pages...\n")

    # Track by section for summary
    section_counts = {}

    for doc in documents:
        # Generate HTML
        html = generate_document_page(doc, template)

        # Write to file
        output_path = output_dir / doc['document_url'].split('/')[-1]
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        # Track counts
        section = doc['section']
        section_counts[section] = section_counts.get(section, 0) + 1

    print(f"{'='*60}")
    print(f"Document pages generated!")
    print(f"{'='*60}")
    print(f"Total pages: {len(documents)}")
    print(f"Output directory: {output_dir}")

    print(f"\nPages by section:")
    for section, count in sorted(section_counts.items()):
        section_name = SECTION_CONFIG.get(section, {}).get('name', section)
        print(f"  {section_name}: {count}")


if __name__ == '__main__':
    main()
