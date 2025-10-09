import csv
from datetime import datetime
"""
for CQC-Articles.csv
"""
def format_date(date_str):
    # Converts M/D/YYYY to YYYY-MM-DD
    try:
        return date_str.strftime("%Y-%m-%d")
    except ValueError:
        return date_str  # Fallback if date is malformed


def read_csv(filename):
    rows = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        # Date	Title	Publication	URL
        for row in reader:
            rows.append(dict(
                date = datetime.strptime(row['Date'], "%m/%d/%Y"),
                title = row['Title'],
                publication = row['Publication'],
                url = row['URL'],
            ))
    return sorted(rows, key=lambda row: row['date'], reverse=False)


def format_row(date, title, publication, url):
    return  f"""
    <tr class="border-t border-t-[#d3dbe4]">
      <td class="align-top px-4 py-2 w-[200px] text-[#58728d] text-sm font-normal leading-normal">
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


def main(filename):
    html = "\n".join([format_row(**r) for r in read_csv(filename)])

    with open('table_rows.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("✅ HTML table rows generated in table_rows.html")


if __name__ == '__main__':
    main('CQC-Publications.csv')

