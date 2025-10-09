import csv
import dateparser
import os
import shutil

"""
Working from csv exports of this google sheet as source of truth:
https://docs.google.com/spreadsheets/d/1pcJOwIyaASjyX2Zh4pot0DhCWqQpv4GUZTulBY4hcyk/edit?gid=191252097#gid=191252097

ran :FixDoc over both csvs to fix smart quotes both single and double.
"""

def format_date(date_str):
    # Converts M/D/YYYY to YYYY-MM-DD
    try:
        return dateparser.parse(date_str).strftime("%B %Y")
    except ValueError:
        print(f"error parsing: {date_str}")
        return date_str  # Fallback if date is malformed


def main(data_file, match_file, template_file, output_file):
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
    rows = []
    for row in csv_rows:
        date = format_date(row['Date'])
        media = row['Category']
        title = row['Title'].strip()
        description = row['Description']
        url = match_dict.get(title)
        if not url:
            print(f"no file or link for {title}, skipping")
            continue

        if os.path.exists(url):
            key = title.lower().replace(':', '-') + ".pdf"
            shutil.copyfile(url, os.path.join(assets_destination, key))
            url = './assets/cqc/' + key

        rows.append(f"""
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
            <a href="{url}" target="_blank" class="underline hover:text-blue-600">{title.upper()}</a>
          </td>
          <td class="align-top px-4 py-2 w-[400px] text-[#58728d] text-sm font-normal leading-normal">
            {description}
          </td>
        </tr>
        """)

    # Output the combined HTML
    rows_html = "\n".join(rows)

    # Load template
    with open(template_file) as f:
        template = f.read()

    # Populate template
    template = template.replace('{rows}', rows_html)

    # Save result
    with open(output_file, 'w') as f:
        f.write(template)
        print(f"✅ HTML written to {output_file}")


if __name__ == '__main__':
    main('../data/cqc-reports.csv', '../data/cqc-reports-matching.csv', 'cqc-template.html', '../docs/cqc-reports.html')
