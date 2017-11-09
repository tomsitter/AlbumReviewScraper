""" Album Review Web Scraper in Python 3.6 with BeautifulSoup and Requests"""
import re

from bs4 import BeautifulSoup
from bs4.element import Comment
import requests
import dateparser

from Review import Review


def parse_album_review(text, site):
    """Return date, artist, album, and body of review for page"""
    soup = BeautifulSoup(text, "html.parser")

    if site == "exclaim":
        date = dateparser.parse(
            soup.find("div", {"class": "article-published"}).get_text()[10:]
        )
        author = soup.find("div", {"class": "article-author"}).get_text()[3:]
        try:  # Some reviews don't have ratings
            rating = soup.find("div", {"class": "article-rating"}).get_text()
        except AttributeError as err:
            rating = ''
        artist = soup.find("span", {"class": "article-title"}).get_text()
        album = soup.find("span", {"class": "article-subtitle"}).get_text()
        review = soup.find("div", {"class": "article"}).get_text()
        if rating != '':
            review = re.split('(\n[0-9]\n)', review)[2]
        review = re.split('(\([^()]+\)\n\n)', review)[0]

    elif site == "rollingstone":

        # date will need to be further processed
        date = dateparser.parse(
            soup.find("time", {"class": "content-published-date"}).get_text()
        )

        author = soup.find("a", {"class": "content-author"}).get_text()

        # title does not hold artist and album in structured way
        title = soup.find("h1", {"class": "content-title"}).get_text()

        # Work in progress -- use URL instead?
        # from urllib.parse imprt urlparse
        # url = soup.find('link', {'rel': 'canonical'}).get('href')
        # parsed_url = urlparse(url)
        # # get last part of URL, split it into words, and remove the last word which is some id
        # # should be left with
        # url_title = parsed_url.path.split("/")[-1].split("-")[:-1]
        # url_title = urltitle.split("-")

        if title.startswith("Review:"):
            title = title.lstrip("Review:")
        # if ":" in title:
        #     artist, album = title.strip().split(": ")
        # else:
        artist, album = title.strip(), ""

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
            review = ""

    return Review(date=date, author=author, rating=rating,
                  artist=artist, album=album, review=review)


def find_review_urls(url, site, page=1, max_pages=None):
    """Download URL and search it for album review urls based on the site"""
    text = requests.get(url).text
    # find all review URLs on this page
    for review_url in url_finder(text, site):
        yield review_url

    if max_pages is None or page < max_pages:
        yield from find_review_urls(next_page(url, site), site,
                                    page=page+1, max_pages=max_pages)


def url_finder(text, site):
    """Given the texts of a page listing album reviews,
       parse it with BeautifulSoup and return URLs to album reviews"""
    soup = BeautifulSoup(text, "html.parser")
    if site == 'exclaim':
        for article in soup.find_all("li", {"class": "streamSingle-item"}):
            yield 'https://exclaim.ca' + article.find("a").get("href")

    elif site == 'rollingstone':
        for article in soup.find_all("a", {"class": "content-card-link"}):
            yield article.get("href")

    else:
        raise ValueError("Unknown site: ", site)


def next_page(url, site):
    """Given a URL for a page of album reviews, return the next page"""
    if site == 'exclaim':
        current_page = re.search('page/(\d+)$', url)
        if not current_page:
            return url + '/page/2'
    elif site == 'rollingstone':
        current_page = re.search('page=(\d+)$', url)
        if not current_page:
            return url + '?page=2'
        page_number = current_page.groups()[0]
        page_digits = len(page_number)
        return url[:-page_digits] + str(int(page_number) + 1)
