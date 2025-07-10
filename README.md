# cjs-archive

##  TODO
- [x] github repository
- [x] copy stitchwithgoogle code from https://stitch.withgoogle.com/projects/7798201880332395140?pli=1
- [x] autogenerate pages with tables for sheets 3 and 4.
- [x] deploy to github pages and send dad a link
- [x] point domain to github pages
- [x] favicon
- [ ] fix tailwind css console error (https://tailwindcss.com/docs/installation/play-cdn)
- [ ] figure out how to templatize this nicely instead of cut-and-paste monstrosity
- [ ] copy header from index.html for other files
- [ ] nicer previews for social (fb/x/iMessage)
- [ ] Match CQC revision of CQC citations with CQC reports sheet 1.
- [ ] Make sure mobile styling looks good


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
    * create blackman page
        * create template
        * parse csv
* CQC update (for later)
    * NB Reports page doesn't exist yet

