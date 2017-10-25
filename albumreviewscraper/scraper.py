""" Album Review Web Scraper in Python 3.6 with BeautifulSoup and Requests"""

from bs4 import BeautifulSoup
import requests
import dateparser

import re

from Review import Review

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
        # if ":" in title:
        #     artist, album = title.strip().split(": ")
        # else:
        artist, album = title, "parse error"

        # Reviews are nested <p> in the article-content <div>
        # I want to join contents of all <p>s, unescape the HTML, and remove newlines and tabs 
        review = " ".join([
            p.get_text() for p in 
            soup.find("div", {"class": "article-content"}).find_all("p")
        ])

        rating = len(soup.select("span.percentage.full"))
        if len(soup.select("span.percentage.half")) == 1:
            rating += 0.5
        
        if not review:
            review = "None found"

    return Review(date, artist, album, review, rating)
        
        
def find_review_urls(url, site):
    """Download URL and search it for album review urls based on the site"""
    text = requests.get(url).text
    # find all review URLs on this page
    for review_url in url_finder(text, site):
        yield review_url

    yield find_review_urls(next_page(url), site)

    # find next page



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


def next_page(url, site):
    """Given a URL for a page of album reviews, return the next page"""
    if site == 'exclaim':
        raise NotImplementedError()
    elif site == 'rollingstone':
        current_page = re.search('page=(\d+)$', url)
        if not current_page:
            return url + '?page=2'
        else:
            page_number = current_page.groups()[0]
            page_digits = len(page_number)
            return url[:-page_digits] + str(int(page_number) + 1)