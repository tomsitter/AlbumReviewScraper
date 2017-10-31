A webscraper for album reviews written in Python

Installation:
- git clone https://github.com/tomsitter/AlbumReviewScraper.git
- cd AlbumReviewScraper
- pip install --editable .

Running:

```
usage: main.py [-h] -s SITE [-o OUTPUT] [-p PATH] [--pages PAGES] [--stream]
               [--sepfiles] [-t TIMEOUT]

optional arguments:
  -h, --help            show this help message and exit
  -s SITE, --site SITE  The site to scrape for reviews. Choices: exclaim,
                        rollingstone
  -o OUTPUT, --output OUTPUT
                        The file to output CSV results to.
  -p PATH, --path PATH  path to write files to
  --pages PAGES         The number of pages to scrape before quiting
  --stream              Specify whether to stream output to file rather than
                        allocate in memory until end
  --sepfiles            Specify whether to write reviews to individual files
  -t TIMEOUT, --timeout TIMEOUT
                        Specify time between page visits in ms, default is
                        100ms
```
