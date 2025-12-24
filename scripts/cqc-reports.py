import csv
import os
import shutil
import dateparser
from document_schema import Document, ensure_unique_slug
from date_utils import format_date_month_year

"""
Working from csv exports of this google sheet as source of truth:
https://docs.google.com/spreadsheets/d/1pcJOwIyaASjyX2Zh4pot0DhCWqQpv4GUZTulBY4hcyk/edit?gid=191252097#gid=191252097

ran :FixDoc over both csvs to fix smart quotes both single and double.
"""


def main(data_file, match_file, content_file, output_file):
    """
    Generate HTML page from CSV and return Document objects.

    Args:
        data_file: Path to CSV file
        match_file: Path to matching CSV file
        content_file: Path to content template HTML file
        output_file: Path to output HTML file

    Returns:
        list[Document]: List of all documents processed
    """
    # destination for copied files:
    assets_origin = '/Users/jsundram/Dropbox/Archive of CJS/CQC Reports/'
    pdf_files = {f.lower(): os.path.join(assets_origin, f) for f in os.listdir(assets_origin)}
    assets_destination = '../docs/assets/cqc/'
    os.makedirs(assets_destination, exist_ok=True)

    match_dict = {}
    recorded = set()
    with open(match_file) as f:
        for r in csv.DictReader(f):
            # either we have a url, a filename, or a notation
            title = r['title']
            filename = r['filename']
            key = filename.lower().replace(':', '-') + ".pdf"
            recorded.add(title)
            if filename.startswith('http'):
                match_dict[title] = filename
            elif key in pdf_files:
                match_dict[title] = pdf_files[key]
            else:
                #print(f"{filename}:\n\t{title}")
                pass


    with open(data_file, newline='', encoding='utf-8') as csvfile:
        csv_rows = sorted(csv.DictReader(csvfile), key=lambda r: dateparser.parse(r['Date']))

    clean = lambda s: s.lower().replace(':', '-').replace('"','') + ".pdf"
    for r in csv_rows:
        title = r['Title'].strip()
        if title not in match_dict:
            key = clean(title)
            match = pdf_files.get(key)
            if match is not None:
                match_dict[title] = match
            elif title not in recorded:
                print(title)

    documents = []
    html_rows = []
    existing_slugs = set()

    for row in csv_rows:
        date = format_date_month_year(row['Date'])
        media = row['Category']
        title = row['Title'].strip()
        description = row['Description']
        url = match_dict.get(title)
        if not url:
            print(f"no file or link for {title}, skipping")
            continue

        file_path = ""
        if os.path.exists(url):
            key = title.lower().replace(':', '-') + ".pdf"
            shutil.copyfile(url, os.path.join(assets_destination, key))
            file_path = f'assets/cqc/{key}'
            url = f'/{file_path}'

        # Create Document object
        doc = Document(
            title=title,
            section='cqc-reports',
            url=url,
            date=date,
            description=description,
            category=media,
            file_path=file_path
        )

        # Ensure unique slug
        doc.slug = ensure_unique_slug(doc.slug, doc.section, existing_slugs)
        existing_slugs.add(f"{doc.section}-{doc.slug}")
        doc.document_url = f'documents/{doc.section}-{doc.slug}.html'

        documents.append(doc)

        # Generate HTML row
        html_rows.append(f"""
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
        """)

    # Output the combined HTML
    rows_html = "\n".join(html_rows)

    # Load content template
    with open(content_file) as f:
        content_template = f.read()

    # Populate content template with rows
    content = content_template.replace('{rows}', rows_html)

    # Load base template
    with open('base-template.html') as f:
        template = f.read()

    # Populate template
    html = template.replace('{meta_title}', 'Commission on Quality of Care - Reports')
    html = html.replace('{meta_description}', 'Reports, investigations, and publications from Clarence J. Sundram\'s tenure as founding Chairman of the New York State Commission on Quality of Care for the Mentally Disabled.')
    html = html.replace('{canonical_url}', 'cqc-reports.html')
    html = html.replace('{breadcrumb}', '')  # No breadcrumb for list pages
    html = html.replace('{page_title}', 'Commission on Quality of Care - Reports')
    html = html.replace('{content}', content)
    html = html.replace('{path_prefix}', './')

    # Save result
    with open(output_file, 'w') as f:
        f.write(html)
        print(f"✅ HTML written to {output_file}")

    # Return documents for registry
    return documents


if __name__ == '__main__':
    main('../data/cqc-reports.csv', '../data/cqc-reports-matching.csv', 'cqc-reports-content.html', '../docs/cqc-reports.html')
