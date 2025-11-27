"""
Document schema and utilities for the CJS archive site.

Provides a unified data model for all documents across different sections
and utilities for generating SEO-friendly URLs.
"""

import re
from dataclasses import dataclass
from typing import Optional


# Section definitions
SECTIONS = {
    'cqc-reports': {
        'name': 'CQC Reports',
        'path': 'cqc-reports.html'
    },
    'cqc-media': {
        'name': 'CQC Media Coverage',
        'path': 'cqc-media.html'
    },
    'cqc-publications': {
        'name': 'CQC Publications',
        'path': 'cqc-publications.html'
    },
    'savp': {
        'name': 'Special Advisor',
        'path': 'special-advisor.html'
    },
    'blackman': {
        'name': 'Blackman-Jones Court Monitor',
        'path': 'blackman.html'
    },
    'otoole': {
        'name': "O'Toole Court Monitor",
        'path': 'otoole.html'
    },
    'otoole-timeline': {
        'name': "O'Toole Timeline",
        'path': 'otoole-timeline.html'
    }
}


@dataclass
class Document:
    """Unified document model for all site content."""

    # Required fields
    title: str
    section: str  # Key from SECTIONS dict
    url: str      # URL to the resource (PDF or external link)

    # Common fields
    date: str = ""              # YYYY-MM-DD format
    description: str = ""       # Description or abstract
    category: str = ""          # Type/category (Investigation, Report, etc.)
    source: str = ""            # Publication source or media outlet

    # Generated fields
    slug: str = ""              # URL-friendly slug
    document_url: str = ""      # URL to landing page
    file_path: str = ""         # Relative path to PDF if local

    def __post_init__(self):
        """Generate slug and document URL after initialization."""
        if not self.slug:
            self.slug = generate_slug(self.title)
        if not self.document_url:
            self.document_url = get_document_url(self.section, self.slug)

    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            'title': self.title,
            'section': self.section,
            'section_name': SECTIONS[self.section]['name'],
            'section_path': SECTIONS[self.section]['path'],
            'url': self.url,
            'date': self.date,
            'description': self.description,
            'category': self.category,
            'source': self.source,
            'slug': self.slug,
            'document_url': self.document_url,
            'file_path': self.file_path
        }


def generate_slug(title: str) -> str:
    """
    Convert title to URL-friendly slug.

    Rules:
    - Lowercase
    - Remove special characters (keep alphanumeric and spaces)
    - Replace spaces with hyphens
    - Collapse multiple hyphens
    - Strip leading/trailing hyphens

    Examples:
        "A Review of Broome Developmental Services"
          → "a-review-of-broome-developmental-services"

        "In the Matter of R.H. - A Patient at Manhattan Psychiatric Center"
          → "in-the-matter-of-rh-a-patient-at-manhattan-psychiatric-center"

        "2024 Annual Report"
          → "2024-annual-report"
    """
    slug = title.lower()
    # Remove special characters, keep alphanumeric, spaces, and hyphens
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    # Replace spaces with hyphens
    slug = re.sub(r'\s+', '-', slug)
    # Collapse multiple hyphens
    slug = re.sub(r'-+', '-', slug)
    # Strip leading/trailing hyphens
    slug = slug.strip('-')
    return slug


def get_document_url(section: str, slug: str) -> str:
    """
    Generate the document landing page URL.

    Format: documents/{section}-{slug}.html

    Examples:
        get_document_url('cqc-reports', 'annual-report-1996-97')
          → 'documents/cqc-reports-annual-report-1996-97.html'
    """
    return f'documents/{section}-{slug}.html'


def ensure_unique_slug(slug: str, section: str, existing_slugs: set) -> str:
    """
    Ensure slug is unique by adding numeric suffix if needed.

    Args:
        slug: The proposed slug
        section: The section identifier
        existing_slugs: Set of already-used "{section}-{slug}" combinations

    Returns:
        Unique slug (may have suffix added)
    """
    full_slug = f"{section}-{slug}"
    if full_slug not in existing_slugs:
        return slug

    # Add numeric suffix
    original_slug = slug
    counter = 2
    while f"{section}-{slug}" in existing_slugs:
        slug = f"{original_slug}-{counter}"
        counter += 1

    return slug


# CSV Column Mapping Functions

def map_cqc_reports_row(row: dict, url: str, file_path: str = "") -> Document:
    """Map CQC Reports CSV row to Document."""
    return Document(
        title=row['Title'].strip(),
        section='cqc-reports',
        url=url,
        date=row['Date'],  # Will be formatted by caller
        description=row['Description'],
        category=row['Category'],
        file_path=file_path
    )


def map_savp_row(row: dict) -> Document:
    """Map SAVP CSV row to Document."""
    url = row['URL']
    file_path = ""

    # If URL is "PDF", it will be set by caller
    if url == 'PDF':
        file_path = f"assets/savp/{generate_slug(row['Title'])}.pdf"

    return Document(
        title=row['Title'],
        section='savp',
        url=url,
        date=row['Date'],  # Will be formatted by caller
        description=row['Description'],
        category=row['Type'],
        file_path=file_path
    )


def map_blackman_row(row: dict, url: str, file_path: str) -> Document:
    """Map Blackman CSV row to Document."""
    return Document(
        title=row['Document'].strip(),
        section='blackman',
        url=url,
        date=row['Date'],  # Will be formatted by caller
        description=row['Description'],
        category='Court Monitor Report',
        file_path=file_path
    )


def map_otoole_row(row: dict, url: str, file_path: str) -> Document:
    """Map O'Toole CSV row to Document."""
    return Document(
        title=row['Document'],
        section='otoole',
        url=url,
        date=row['Date'],  # Will be formatted by caller
        description=row['Description'],
        category='Court Monitor Report',
        file_path=file_path
    )


def map_otoole_timeline_row(row: dict) -> Document:
    """Map O'Toole Timeline CSV row to Document."""
    return Document(
        title=row['News Coverage'],
        section='otoole-timeline',
        url=row['URL'],
        date=row['DATE'],  # Will be formatted by caller
        description=row['ACTION'],
        category='Timeline Event'
    )


def map_cqc_media_row(row: dict) -> Document:
    """Map CQC Media Coverage CSV row to Document."""
    return Document(
        title=row['Title'],
        section='cqc-media',
        url=row['URL'],
        date=row['Date'],  # Will be formatted by caller
        description=row['Description'],
        category=row['Media'],
        source=row['Media']
    )


def map_cqc_publications_row(row: dict) -> Document:
    """Map CQC Publications CSV row to Document."""
    return Document(
        title=row['Title'],
        section='cqc-publications',
        url=row['URL'],
        date=row['Date'],  # Will be formatted by caller
        description='',  # No description in this CSV
        category='Publication',
        source=row['Publication']
    )
