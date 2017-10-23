""" Album Review Web Scraper in Python 3.6 with BeautifulSoup and Requests"""

from bs4 import BeautifulSoup
import requests

def main(argv):
    """Main entry to script from command line"""
    pass

class Review:
    """Holds review data and can be serialized to CSV row"""
    def __init__(self, date, artist, album, review):
        self.date = date or ""
        self.artist = artist or ""
        self.album = album or ""
        self.review = review or ""

sites = [
    "http://exclaim.ca/music/reviews"
]

def parse_album_review(url):
    r = requests.get(url)
    

def find_review_urls(url, site_parser):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    for article in site_parser(soup):
        yield article.find("a").get("href")


def find_exclaim_review_urls(soup):
    """returns links to all Exclaim album reviews on review page"""
    yield soup.find_all("li", {"class" : "streamSingle-item"})


def find_rollingstone_review_urls(soup):
    """returns links to all Rolling Stone album reviews"""
    pass


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])