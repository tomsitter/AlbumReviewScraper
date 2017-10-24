""" Album Review Web Scraper in Python 3.6 with BeautifulSoup and Requests"""

from bs4 import BeautifulSoup
import requests
import sys

if sys.version_info[0] < 3:
    raise Exception("Python 3 or a more recent version is required.")

urls = {
    "exclaim": "http://exclaim.ca/music/reviews",
    "rollingstone": "http://www.rollingstone.com/music/albumreviews",
}

def main(site, output=None):
    """Main entry to script from command line"""
    url = urls[site]
    for review_url in find_review_urls(url, site):
        print(review_url)
        r = requests.get(review_url)
        date, artist, album, review = parse_album_review(r.content, site)
        print(review)


class Review:
    """Holds review data and can be serialized to CSV row"""
    def __init__(self, date, artist, album, review):
        self.date = date or ""
        self.artist = artist or ""
        self.album = album or ""
        self.review = review or ""
        

def parse_album_review(content, site):
    """Return date, artist, album, and body of review for page"""
    soup = BeautifulSoup(content, "html.parser")
    if site == "exclaim":
        # artist = article-title
        # album = article-subtitle
        # date = article-published "Published Oct 23, 2017"
        # body = *not wrapped in anything*
        date, artist, album, review = "Ex", "cl", "a", "im"
    elif site == "rollingstone":
        date = soup.find("time", {"class": "content-published-date"}).get_text()
        title = soup.find("h1", {"class": "content-title"}).get_text()
        if title:
            print("Title: ", title)
            artist, album = title.split(": ")
        else:
            artist, album = "None found", "None found"
        review = soup.find("div", {"class": "article-content"})
        import pdb
        pdb.set_trace()
        if not review:
            review = "None found"

    return date, artist, album, review
        
        
def find_review_urls(url, site):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    for review_url in url_finder(soup, site):
        yield review_url


def url_finder(soup, site):
    if site == 'exclaim':
        for article in soup.find_all("li", {"class" : "streamSingle-item"}):
            yield article.find("a").get("href")
    elif site == 'rollingstone':
        for article in soup.find_all("a", {"class": "content-card-link"}):
            yield article.get("href")
    else:
        raise ValueError("Unknown site: ", site)
        

if __name__ == "__main__":
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
