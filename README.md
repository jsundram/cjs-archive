# cjs-archive

##  TODO
- [x] github repository
- [x] copy stitchwithgoogle code from https://stitch.withgoogle.com/projects/7798201880332395140?pli=1
- [x] autogenerate pages with tables for sheets 3 and 4.
- [x] deploy to github pages and send dad a link
- [x] point domain to github pages
- [x] favicon
- [x] Add the files “timeline””CJS Statement”  and “Final Order of Dismissal”
    * manually add final order of dismissal to existing otoole.csv
    * rerun otoole-csv.py
    * this means looking at the "timeline of case.xlsx" document in the Dropbox Folder
    * converted to google sheet and edited [here](https://docs.google.com/spreadsheets/d/1HQzrmKri9cTj_yOy0aHg_-KALvczY-R3qNk_T8ibdA8/edit?gid=282188553#gid=282188553)
    * then exported to csv in data/otoole-timeline.csv
- [ ] change row alignment so text is at the top, not vertically centered

---
- [ ] fix tailwind css console error (https://tailwindcss.com/docs/installation/play-cdn)
- [ ] figure out how to templatize this nicely instead of cut-and-paste monstrosity
- [ ] copy header from index.html for other files
- [ ] nicer previews for social (fb/x/iMessage)
- [ ] Match CQC revision of CQC citations with CQC reports sheet 1.
- [ ] Make sure mobile styling looks good
- [ ] Create landing pages for all external links with descriptions for better SEO?


## Description
idea is that excel spreadsheets have the content, pull the data into csvs, use python to generate html.
use about.html as the template file for the repository.

##  Resources
bio: https://docs.google.com/document/d/12xP_eeYnS0Oy7feqvtC87xZ03IaSeLu2/edit
CQC: https://docs.google.com/spreadsheets/d/1FEB-TLPxuc_buzlWEIJzNzch9QWkWWil/edit?gid=1637828733#gid=1637828733

## history
* Email: CQC spreadsheet [https://mail.google.com/mail/u/0/#search/from%3Acjsundram%40gmail.com/FMfcgzQbfVDcqKvnQsHHtZdVLfvChmJF]
    * sheet 1: reports
    * sheet 2: merged into publications
    * sheet 3: media coverage
    * sheet 4: publications
    * merged into CQC spreadsheet on google drive (above)
* Email: bio  -> google drive (see above) [https://mail.google.com/mail/u/0/#search/from%3Acjsundram%40gmail.com/FMfcgzQbfVDczRsXcbQWBpZQGFbcJCQW]
* headshot (https://mail.google.com/mail/u/0/#search/from%3Acjsundram%40gmail.com/FMfcgzQbfVDczVHgdkQPxLRCFjDFJJfm)
* [CQC Description Email](https://mail.google.com/mail/u/0/#search/from%3Acjsundram%40gmail.com/FMfcgzQbfVDdJnHVjJlnhZqGXmjCKQzk)
* Email SAVP.xlsx [https://mail.google.com/mail/u/0/#search/from%3Acjsundram%40gmail.com/FMfcgzQbffbFFXVSWjkCVpGcBxHcsKtC]
    * Several questions on this
* Adding "Website SVAP.xlsx" to the site (copy in drobpox folder)
    * Sheet 1: Special Advisor
        * Columns should be: Date, Type, Title, Publication, URL.
        * Move podcast episodes FROM CQC page to be here, so DELETE CQC podcast rows.
        * Made edits to this file in a .numbers file in my Downloads folder...
    * Sheets 2 and 3 should be sub-pages of a main "Court Monitor" page
        * Landing Page (will need a blurb)
        * Sheet 2: Court Monitor - O'Toole
            * seems ok except some date formatting issues
        * Sheet 3: Court Monitor - Blackman
            * seems ok except some date formatting issues
            * TODO: clean up some file names?
* Sheet 1
    * Edit and export.
    * 1. create template for SAVP
        * base on about page (index.html)
        * modify to have a table like cqc-media.html
    * 2. python script to read csv and populate template
    * 3. git commit
* Court Monitor page
    * received blurb for landing page via [email](https://mail.google.com/mail/u/0/#inbox/FMfcgzQbgJGVVhZqVtDxnswKfmnNmPML) and copied it to ./data/court-monitor.md
    * create otoole page
        * create template
        * parse csv
        * git commit
        * TODO: files need to be moved
    * create blackman page
        * create template
        * parse csv
        * move files
        * git commit
* CQC update (for later)
Input Files
The Spreadsheet of CQC Reports has four tabs:
1. Reports
2. Publications (these were merged with the publications on sheet 4 for the website)
3. Media Coverage
4. Publications (merged with 2, as noted above).

The CQC Citation and file matching file has 2 tabs:
1. missing citation - these were files that you had saved in dropbox which were missing any mention in the CQC spreadsheet above. The first column contains the filename in the dropbox folder CQC Reports. The second column contains the Title which is used in tab 1 of the Spreadsheet of CQC Reports. You've updated the Spreadsheet of CQC reports tab 1 to cite these files.
2. matches - column 1 contains the Title in tab 1 of the Spreadsheet of CQC reports. column 2 contains one of the following:
a. a URL to the file
b. a filename
c. a notation indicating that there isn't a file -- this means that the report with this Title will not be shown on the website.

Procedure
tab 1 ("Reports") of Spreadsheet of CQC Reports will be used to create "cqc-reports.html", a web page containing a table with the following columns: Date, Category, Title, Description.

Export tab 1 (reports) to csv ("./data/CQC-Reports.csv")

Each row in Tab 1 will correspond to a row in that webpage table:
1. The title will be used to search for a file in the Dropbox "CQC Reports" folder.
2. If the file is found, it will be copied to the website
3. If the file is not found, I'll look at "CQC citation and file matching" tab 2, and find a row with the same title.
4. If I can't find that row, something is broken. That row won't be added.
5. If I can find that row, it will contain either a URL or a filename, or a notation that there is a file missing.
6. If the file is missing, that row won't be added
7. If there is a url or filename, that row will be added and the file will be linked.

Output
will be written to https://clarencesundram.org/cqc-reports.html (currently 404) which is linked from https://clarencesundram.org/cqc.html.


