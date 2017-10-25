""" Command-line entry to application """

import sys

import requests

from config import urls
from ui import ask_for_input, catalog_to_csv, FileStream
from scraper import find_review_urls, parse_album_review

if sys.version_info[0] < 3:
    raise Exception("Python 3 or a more recent version is required.")


def main(site, output=None, max_pages=None, stream=None):
    """Main entry to script from command line
    """
    url = urls[site]
    catalog = []
    file_stream = None

    if output and stream:
        try:
            file_stream = FileStream(filename=output)
        except IOError as err:
            print(err)
            output = None

    for review_url in find_review_urls(url, site, max_pages=max_pages):
        print(review_url)
        text = requests.get(review_url).text
        review = parse_album_review(text, site)
        if file_stream:
            file_stream.write_review(review)
            catalog.append(1)
        else:
            catalog.append(review)

    if stream:
        print("Streamed %d reviews to %s" % len(catalog), output)
        return

    if catalog:
        print("Found %d reviews" % len(catalog))
        if output:
            try:
                catalog_to_csv(catalog, output=output)
            except IOError as err:
                print(err)
                ask_for_input(catalog)
        else:
            ask_for_input(catalog)
    else:
        print("No reviews found.")


if __name__ == "__main__":
    """ Parse command line arguments and call main()"""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--site",
                        help="The site to scrape for reviews. Choices: exclaim, rollingstone",
                        required=True)
    parser.add_argument("-o", "--output",
                        help="The file to output CSV results to.")
    parser.add_argument("--pages",
                        help="The number of pages to scrape before quiting",
                        type=int)
    parser.add_argument("--stream",
                        help="Specify whether to stream output to file")
    args = parser.parse_args()

    if args.site:
        main(args.site, 
             output=args.output, 
             max_pages=args.pages,
             stream=args.stream)
    else:
        raise ValueError("Missing site name for scraping")

