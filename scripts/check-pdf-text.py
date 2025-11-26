#!/usr/bin/env python3
"""
Check which PDFs have searchable text content
Requires: pdftotext (from poppler-utils)
Install on macOS: brew install poppler
"""
import subprocess
import sys
from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent / "docs"
MIN_TEXT_LENGTH = 100  # Minimum characters to consider PDF as having text


def check_pdftotext_installed():
    """Check if pdftotext is available"""
    try:
        result = subprocess.run(['which', 'pdftotext'],
                              capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False


def extract_text(pdf_path):
    """Extract text from PDF using pdftotext"""
    try:
        result = subprocess.run(
            ['pdftotext', str(pdf_path), '-'],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return result.stdout
        return None
    except subprocess.TimeoutExpired:
        return None
    except Exception as e:
        print(f"Error processing {pdf_path.name}: {e}")
        return None


def check_pdfs():
    """Check all PDFs for searchable text"""

    # Check if pdftotext is installed
    if not check_pdftotext_installed():
        print("❌ ERROR: pdftotext not found!")
        print("\nTo install on macOS:")
        print("  brew install poppler")
        print("\nTo install on Ubuntu/Debian:")
        print("  sudo apt-get install poppler-utils")
        sys.exit(1)

    print("Checking PDFs for searchable text...\n")

    # Collect all PDFs
    pdfs = list(DOCS_DIR.glob("assets/**/*.pdf"))
    total = len(pdfs)

    results = {
        'has_text': [],
        'no_text': [],
        'errors': []
    }

    for i, pdf_path in enumerate(sorted(pdfs), 1):
        rel_path = pdf_path.relative_to(DOCS_DIR)
        print(f"[{i}/{total}] Checking: {rel_path.parent.name}/{pdf_path.name[:60]}...")

        text = extract_text(pdf_path)

        if text is None:
            results['errors'].append(rel_path)
        elif len(text.strip()) < MIN_TEXT_LENGTH:
            results['no_text'].append(rel_path)
        else:
            results['has_text'].append(rel_path)

    # Print summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"\n✅ PDFs with searchable text: {len(results['has_text'])}/{total}")

    if results['no_text']:
        print(f"\n⚠️  PDFs with little/no text ({len(results['no_text'])}):")
        print("   (These may be scanned images and need OCR)")
        for pdf in results['no_text']:
            print(f"   - {pdf}")

    if results['errors']:
        print(f"\n❌ Errors processing ({len(results['errors'])}):")
        for pdf in results['errors']:
            print(f"   - {pdf}")

    # Final recommendation
    print("\n" + "="*80)
    if results['no_text']:
        print("⚠️  RECOMMENDATION: PDFs listed above may need OCR processing")
        print("   to be fully searchable by Google.")
    else:
        print("✅ All PDFs appear to have searchable text content!")
    print("="*80)

    return len(results['no_text']) == 0 and len(results['errors']) == 0


if __name__ == "__main__":
    success = check_pdfs()
    sys.exit(0 if success else 1)
