""" Command-line entry to application """

import sys

import requests

from config import urls
from util import print_catalog, catalog_to_csv, FileStream, write_review_to_file
from scraper import find_review_urls, parse_album_review

if sys.version_info[0] < 3:
    raise Exception("Python 3 or a more recent version is required.")


def main(site, output=None, path="./", max_pages=None, 
         stream=None, separate_files=None):
    """Main entry to script from command line
    """
    url = urls[site]
    catalog = []
    file_stream = None

    print(f"Path is {path}")
    print(f"Output is {output} and stream is {stream}")
    if output and stream:
        try:
            file_stream = FileStream(filename=output, path=path, separate_files=separate_files)
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

    print('No more reviews found')

    if stream:
        print(f"Streamed {len(catalog)} reviews to {output}")
        return

    if catalog:
        print(f"Found {len(catalog)} reviews")
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


def ask_for_input(catalog):
    """Command line prompt if file fails"""
    choice = input("Type 'q' to quit, 'p' to print reviews to console, 'a' to write all reviews to individual files, or enter the filename to write all reviews to one file: ")
    if choice == 'q':
        sys.exit()
    elif choice == 'p':
        print_catalog(catalog)
    elif choice == 'a':
        for review in catalog:
            write_review_to_file(review)
    else:
        try:
            catalog_to_csv(catalog, output=choice)
            print(f'Wrote {len(catalog)} reviews to {choice}')
        except IOError as err:
            print(err)
    ask_for_input(catalog)



if __name__ == "__main__":
    """ Parse command line arguments and call main()"""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--site",
                        help="The site to scrape for reviews. Choices: exclaim, rollingstone",
                        required=True)
    parser.add_argument("-o", "--output",
                        help="The file to output CSV results to.")
    parser.add_argument("--path",
                        help="path to write files to")
    parser.add_argument("--pages",
                        help="The number of pages to scrape before quiting",
                        type=int)
    parser.add_argument("--stream",
                        help="Specify whether to stream output to file",
                        action='store_true')
    parser.add_argument("--sepfiles",
                        help="Specify whether to write reviews to individual files",
                        action='store_true')
    args = parser.parse_args()

    if args.site:
        main(args.site, 
             output=args.output,
             path=args.path,
             max_pages=args.pages,
             stream=args.stream,
             separate_files=args.sepfiles)
    else:
        raise ValueError("Missing site name for scraping")

