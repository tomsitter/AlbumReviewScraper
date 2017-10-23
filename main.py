""" Album Review Web Scraper in Python 3.6 with BeautifulSoup and Requests"""

from bs4 import BeautifulSoup
import requests

urls = {
    "exclaim": "http://exclaim.ca/music/reviews",
    "rollingstone": "",
}

def main(site):
    """Main entry to script from command line"""
    url = urls[site]
    for review_url in find_review_urls(url, site):
        print(review_url)

class Review:
    """Holds review data and can be serialized to CSV row"""
    def __init__(self, date, artist, album, review):
        self.date = date or ""
        self.artist = artist or ""
        self.album = album or ""
        self.review = review or ""
        

def parse_album_review(url):
    r = requests.get(url)
    

def find_review_urls(url, site):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    for article in article_finder(soup, site):
        yield article.find("a").get("href")


def article_finder(soup, site):
    if site == 'exclaim':
        yield from soup.find_all("li", {"class" : "streamSingle-item"})
    elif site == 'rollingstone':
        raise NotImplementedError()
    else:
        raise ValueError("Unknown site: ", site)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", help="The site to scrape for reviews. Choices: exclaim, rollingstone")
    args = parser.parse_args()

    main(args.site)
