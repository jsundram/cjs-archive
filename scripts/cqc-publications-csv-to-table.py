import csv
from datetime import datetime

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


def format_row(date, title, publication, url):
    return f"""
    <tr class="border-t border-t-[#d3dbe4]">
      <td class="align-top px-4 py-2 w-[150px] text-[#58728d] text-sm font-normal leading-normal">
        {format_date(date)}
      </td>
      <td class="align-top px-4 py-2 w-[400px] text-[#101419] text-sm font-normal leading-normal">
        <a href="{url}" target="_blank" class="underline hover:text-blue-600">{title}</a>
      </td>
      <td class="align-top px-4 py-2 w-[400px] text-[#58728d] text-sm font-normal leading-normal">
        {publication}
      </td>
    </tr>
    """


def main(data_file, template_file, output_file):
    html_rows = "\n".join([format_row(**r) for r in read_csv(data_file)])

    # Load template
    with open(template_file, encoding='utf-8') as f:
        template = f.read()

    # Populate template
    html_output = template.replace('{rows}', html_rows)

    # Save result
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_output)
        print(f"✅ HTML written to {output_file}")


if __name__ == '__main__':
    main('../data/CQC-Publications.csv', 'cqc-publications-template.html', '../docs/cqc-publications.html')
