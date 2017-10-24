""" Album Review Web Scraper in Python 3.6 with BeautifulSoup and Requests"""

from bs4 import BeautifulSoup
import requests
import sys

if sys.version_info[0] < 3:
    raise Exception("Python 3 or a more recent version is required.")


class Review:
    """Holds review data 
        Noy yet in use 
    """
    def __init__(self, date, artist, album, review):
        self.date = date or ""
        self.artist = artist or ""
        self.album = album or ""
        self.review = review or ""


urls = {
    "exclaim": "http://exclaim.ca/music/reviews",
    "rollingstone": "http://www.rollingstone.com/music/albumreviews",
}


def main(site, output=None):
    """Main entry to script from command line
    """
    url = urls[site]

    for review_url in find_review_urls(url, site):
        print(review_url)
        review = requests.get(review_url).content
        date, artist, album, review = parse_album_review(review, site)
        # output review to file
        

def parse_album_review(content, site):
    """Return date, artist, album, and body of review for page"""
    soup = BeautifulSoup(content, "html.parser")
    if site == "exclaim":
        # artist = article-title
        # album = article-subtitle
        # date = article-published "Published Oct 23, 2017"
        # body = *not wrapped in anything*
        date, artist, album, review = "", "", "", ""
        raise NotImplementedError("Exclaim! is not yet supported")
    elif site == "rollingstone":

        # date will need to be further processed
        date = soup.find("time", {"class": "content-published-date"}).get_text()
        
        # title does not hold artist and album in structured way
        title = soup.find("h1", {"class": "content-title"}).get_text()
        if ":" in title:
            artist, album = title.split(": ")
        else:
            artist, album = title, "parse error"

        # Reviews are nested <p> in the article-content <div>
        review = "\n".join([p.get_text() 
                            for p in 
                            soup.find("div", {"class": "article-content"}).find_all("p")])
        if not review:
            review = "None found"

    return date, artist, album, review
        
        
def find_review_urls(url, site):
    """Download URL and search it for album review urls based on the site"""
    content = requests.get(url).content
    for review_url in url_finder(content, site):
        yield review_url


def url_finder(content, site):
    """Given the contents of a page listing album reviews, 
       parse it with BeautifulSoup and return URLs to album reviews"""
    soup = BeautifulSoup(content, "html.parser")
    if site == 'exclaim':
        for article in soup.find_all("li", {"class" : "streamSingle-item"}):
            yield article.find("a").get("href")

    elif site == 'rollingstone':
        for article in soup.find_all("a", {"class": "content-card-link"}):
            yield article.get("href")
            
    else:
        raise ValueError("Unknown site: ", site)
        

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
