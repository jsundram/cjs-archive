import csv
from datetime import datetime
"""
for CQC-Coverage.csv
"""
def format_date(date_str):
    # Converts M/D/YYYY to YYYY-MM-DD
    try:
        return datetime.strptime(date_str, "%m/%d/%Y").strftime("%Y-%m-%d")
    except ValueError:
        return date_str  # Fallback if date is malformed


def main(filename):
    rows_html = []

    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            date = format_date(row['Date'])
            media = row['Media']
            title = row['Title']
            description = row['Description']
            url = row['URL']

            row_html = f"""
            <tr class="border-t border-t-[#d3dbe4]">
              <td class="align-top px-4 py-2 w-[400px] text-[#58728d] text-sm font-normal leading-normal">
                {date}
              </td>
              <td class="align-top px-4 py-2 w-60 text-sm font-normal leading-normal">
                <button class="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-full h-8 px-4 bg-[#e9edf1] text-[#101419] text-sm font-medium leading-normal w-full">
                  <span class="truncate">{media}</span>
                </button>
              </td>
              <td class="align-top px-4 py-2 w-[400px] text-[#101419] text-sm font-normal leading-normal">
                <a href="{url}" target="_blank" class="underline hover:text-blue-600">{title.upper()}</a>
              </td>
              <td class="align-top px-4 py-2 w-[400px] text-[#58728d] text-sm font-normal leading-normal">
                {description}
              </td>
            </tr>
            """
            rows_html.append(row_html)

    # Output the combined HTML
    html_output = "\n".join(rows_html)

    with open('table_rows.html', 'w', encoding='utf-8') as f:
        f.write(html_output)

    print("✅ HTML table rows generated in table_rows.html")

if __name__ == '__main__':
    main('CQC-Coverage.csv')

