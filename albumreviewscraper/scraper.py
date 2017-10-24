""" Album Review Web Scraper in Python 3.6 with BeautifulSoup and Requests"""

from bs4 import BeautifulSoup
import csv
import requests
import dateparser
import datetime
import re
import sys
import string
import html

if sys.version_info[0] < 3:
    raise Exception("Python 3 or a more recent version is required.")


def catalog_to_csv(catalog, out=None, mode="w", delimiter="\t"):
    try:
        if len(catalog) > 0:
            with open(out, mode, encoding='utf-8', newline='') as o:
                writer = csv.writer(o, delimiter=delimiter)
                writer.writerow(catalog[0].keys())
                for review in catalog:
                    writer.writerow(review.as_list())
    except IOError as err:
        print(err)


def print_catalog(catalog):
    if len(catalog) > 0:
        header = catalog[0].keys()
        print(", ".join(header))
        for review in catalog:
            print(", ".join(review.as_list()))
    else:
        print("Catalog is empty")


class Review():
    """Holds review data 
        Noy yet in use 
    """
    def __init__(self, date, artist, album, review):
        self._date = date or ""
        self.artist = artist or ""
        self.album = album or ""
        self.review = review or ""
    def as_list(self):
        # returns the items as a list
        return [self.date,
                self.artist,
                self.album,
                self.review]
    @staticmethod
    def sanitize(review):
        return html.unescape(review).replace('\n', '').replace('\t', '').replace('\r', '')
    def keys(self):
        return [key.lstrip("_") 
                for key in vars(self).keys()]
    @property
    def date(self):
        date_format = "%Y-%m-%d"
        if self._date:
            return self._date.strftime(date_format)
        else:
            return self._date
    @date.deleter
    def date(self):
        del self._date
    @date.setter
    def date(self, value):
        if value and isinstance(value, datetime.date):
            self._date = value
        else:
            self._date = None
            raise ValueError("Date must be of type datetime.date")
    @property
    def review(self):
        return self._review
    @review.deleter
    def review(self):
        del self._review
    @review.setter
    def review(self, value):
        self._review = self.sanitize(value)



urls = {
    "exclaim": "http://exclaim.ca/music/reviews",
    "rollingstone": "http://www.rollingstone.com/music/albumreviews",
}


def main(site, output=None):
    """Main entry to script from command line
    """
    url = urls[site]
    catalog = []

    for review_url in find_review_urls(url, site):
        print(review_url)
        review = requests.get(review_url).text
        date, artist, album, review = parse_album_review(review, site)
        # output review to file
        catalog.append(Review(date, artist, album, review))

    if len(catalog) > 0:
        print("Found %d reviews" % len(catalog))
        if output:
            try:
                catalog_to_csv(catalog, out=output)
            except IOError as err:
                print(err)
                ask_for_input(catalog)
        else:
            ask_for_input(catalog)
    else:
        print("No reviews found.")


def ask_for_input(catalog):
    """Command line prompt if file fails"""
    choice = input("Press enter to quit, 'p' to print to console, or type in the name of the file you want to write to: ")
    if not choice:
        sys.exit()
    elif choice == 'p':
        print_catalog(catalog)
    else:
        try:
            catalog_to_csv(catalog, out=choice)
            print('Wrote {} reviews to {}'.format(len(catalog), choice))
        except IOError as err:
            print(err)
    ask_for_input(catalog)


def parse_album_review(text, site):
    """Return date, artist, album, and body of review for page"""
    soup = BeautifulSoup(text, "html.parser")
    if site == "exclaim":
        # artist = article-title
        # album = article-subtitle
        # date = article-published "Published Oct 23, 2017"
        # body = *not wrapped in anything*
        date, artist, album, review = "", "", "", ""
        raise NotImplementedError("Exclaim! is not yet supported")
    elif site == "rollingstone":

        # date will need to be further processed
        date = dateparser.parse(
            soup.find("time", {"class": "content-published-date"}).get_text()
        )
        
        # title does not hold artist and album in structured way
        title = soup.find("h1", {"class": "content-title"}).get_text()

        if title.startswith("Review:"):
            title = title.lstrip("Review:")
        if ":" in title:
            artist, album = title.strip().split(": ")
        else:
            artist, album = title, "parse error"

        # Reviews are nested <p> in the article-content <div>
        # I want to join contents of all <p>s, unescape the HTML, and remove newlines and tabs 
        review = " ".join([
            p.get_text() for p in 
            soup.find("div", {"class": "article-content"}).find_all("p")
        ])
        
        if not review:
            review = "None found"

    return date, artist, album, review
        
        
def find_review_urls(url, site):
    """Download URL and search it for album review urls based on the site"""
    text = requests.get(url).text
    for review_url in url_finder(text, site):
        yield review_url


def url_finder(text, site):
    """Given the texts of a page listing album reviews, 
       parse it with BeautifulSoup and return URLs to album reviews"""
    soup = BeautifulSoup(text, "html.parser")
    if site == 'exclaim':
        for article in soup.find_all("li", {"class" : "streamSingle-item"}):
            yield article.find("a").get("href")

    elif site == 'rollingstone':
        for article in soup.find_all("a", {"class": "content-card-link"}):
            yield article.get("href")

    else:
        raise ValueError("Unknown site: ", site)
        
format_rollingstone_review(raw):
    

if __name__ == "__main__":
    """ Parse command line arguments and call main()"""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--site", 
                        help="The site to scrape for reviews. Choices: exclaim, rollingstone",
                        required=True)
    parser.add_argument("-o", "--output", 
                        help="The file to output CSV results to.")
    args = parser.parse_args()

    if args.site:
        main(args.site, args.output)
    else:
        raise ValueError("Missing site name for scraping")
