import csv
from datetime import datetime
from document_schema import Document, ensure_unique_slug

"""
Generates cqc-publications.html from CQC-Publications.csv
"""

def format_date(date_str):
    # Converts datetime to YYYY-MM-DD
    try:
        return date_str.strftime("%Y-%m-%d")
    except (ValueError, AttributeError):
        return date_str  # Fallback if date is malformed


def read_csv(filename):
    rows = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        # Date, Title, Publication, URL
        for row in reader:
            rows.append(dict(
                date=datetime.strptime(row['Date'], "%m/%d/%Y"),
                title=row['Title'],
                publication=row['Publication'],
                url=row['URL'],
            ))
    return sorted(rows, key=lambda row: row['date'], reverse=False)


def format_row(date, title, publication, document_url):
    return f"""
    <tr class="border-t border-t-[#d3dbe4]">
      <td class="align-top px-4 py-2 w-[150px] text-[#58728d] text-sm font-normal leading-normal">
        {format_date(date)}
      </td>
      <td class="align-top px-4 py-2 w-[400px] text-[#101419] text-sm font-normal leading-normal">
        <a href="./{document_url}" class="underline hover:text-blue-600">{title}</a>
      </td>
      <td class="align-top px-4 py-2 w-[400px] text-[#58728d] text-sm font-normal leading-normal">
        {publication}
      </td>
    </tr>
    """


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
    html_rows_list = []
    existing_slugs = set()

    for r in read_csv(data_file):
        # Create Document object
        doc = Document(
            title=r['title'],
            section='cqc-publications',
            url=r['url'],
            date=format_date(r['date']),
            description='',  # No description in this CSV
            category='Publication',
            source=r['publication']
        )

        # Ensure unique slug
        doc.slug = ensure_unique_slug(doc.slug, doc.section, existing_slugs)
        existing_slugs.add(f"{doc.section}-{doc.slug}")
        doc.document_url = f'documents/{doc.section}-{doc.slug}.html'

        documents.append(doc)

        # Generate HTML row
        html_rows_list.append(format_row(r['date'], r['title'], r['publication'], doc.document_url))

    html_rows = "\n".join(html_rows_list)

    # Load content template
    with open(content_file) as f:
        content_template = f.read()

    # Populate content template with rows
    content = content_template.replace('{rows}', html_rows)

    # Load base template
    with open('base-template.html', encoding='utf-8') as f:
        template = f.read()

    # Populate template
    html = template.replace('{meta_title}', 'Commission on Quality of Care - Publications')
    html = html.replace('{meta_description}', 'Published articles and papers by Clarence J. Sundram about the Commission on Quality of Care.')
    html = html.replace('{canonical_url}', 'cqc-publications.html')
    html = html.replace('{breadcrumb}', '')
    html = html.replace('{page_title}', 'Commission on Quality of Care - Publications')
    html = html.replace('{content}', content)
    html = html.replace('{path_prefix}', './')

    # Save result
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
        print(f"✅ HTML written to {output_file}")

    # Return documents for registry
    return documents


if __name__ == '__main__':
    main('../data/CQC-Publications.csv', 'cqc-publications-content.html', '../docs/cqc-publications.html')
