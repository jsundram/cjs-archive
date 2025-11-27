import csv
from datetime import datetime
from document_schema import Document, ensure_unique_slug

"""
Generates cqc-media.html from CQC-Coverage.csv
"""

def format_date(date_str):
    # Converts M/D/YYYY to YYYY-MM-DD
    try:
        return datetime.strptime(date_str, "%m/%d/%Y").strftime("%Y-%m-%d")
    except ValueError:
        return date_str  # Fallback if date is malformed


def main(data_file, content_file, output_file):
    """
    Generate HTML page from CSV and return Document objects.

    Args:
        data_file: Path to CSV file
        content_file: Path to content template HTML file
        output_file: Path to output HTML file

    Returns:
        list[Document]: List of all documents processed
    """
    documents = []
    html_rows = []
    existing_slugs = set()

    with open(data_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            date = format_date(row['Date'])
            media = row['Media']
            title = row['Title']
            description = row['Description']
            url = row['URL']

            # Create Document object
            doc = Document(
                title=title,
                section='cqc-media',
                url=url,
                date=date,
                description=description,
                category=media,
                source=media
            )

            # Ensure unique slug
            doc.slug = ensure_unique_slug(doc.slug, doc.section, existing_slugs)
            existing_slugs.add(f"{doc.section}-{doc.slug}")
            doc.document_url = f'documents/{doc.section}-{doc.slug}.html'

            documents.append(doc)

            # Generate HTML row
            row_html = f"""
            <tr class="border-t border-t-[#d3dbe4]">
              <td class="align-top px-4 py-2 w-[150px] text-[#58728d] text-sm font-normal leading-normal">
                {date}
              </td>
              <td class="align-top px-4 py-2 w-60 text-sm font-normal leading-normal">
                <button class="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-full h-8 px-4 bg-[#e9edf1] text-[#101419] text-sm font-medium leading-normal w-full">
                  <span class="truncate">{media}</span>
                </button>
              </td>
              <td class="align-top px-4 py-2 w-[200px] text-[#101419] text-sm font-normal leading-normal">
                <a href="./{doc.document_url}" class="underline hover:text-blue-600">{title.upper()}</a>
              </td>
              <td class="align-top px-4 py-2 w-[400px] text-[#58728d] text-sm font-normal leading-normal">
                {description}
              </td>
            </tr>
            """
            html_rows.append(row_html)

    # Output the combined HTML
    rows_html_str = "\n".join(html_rows)

    # Load content template
    with open(content_file) as f:
        content_template = f.read()

    # Populate content template with rows
    content = content_template.replace('{rows}', rows_html_str)

    # Load base template
    with open('base-template.html', encoding='utf-8') as f:
        template = f.read()

    # Populate template
    html = template.replace('{meta_title}', 'Commission on Quality of Care - Media Coverage')
    html = html.replace('{meta_description}', 'Media coverage and news articles about the work of the Commission on Quality of Care under Clarence J. Sundram.')
    html = html.replace('{canonical_url}', 'cqc-media.html')
    html = html.replace('{breadcrumb}', '')
    html = html.replace('{page_title}', 'Commission on Quality of Care - Media Coverage')
    html = html.replace('{content}', content)
    html = html.replace('{path_prefix}', './')

    # Save result
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
        print(f"✅ HTML written to {output_file}")

    # Return documents for registry
    return documents


if __name__ == '__main__':
    main('../data/CQC-Coverage.csv', 'cqc-media-content.html', '../docs/cqc-media.html')
