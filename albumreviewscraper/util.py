"""Utility functions for printing reviews and writing them to files"""

import csv
import os
import re


class FileStream:
    def __init__(self, 
                 filename=None,
                 separate_files=False,
                 path="./", 
                 mode="w", 
                 delimiter="\t"):
        self.separate_files = separate_files
        self.path = path
        self.filename=filename
        if filename:
            filepath = os.path.join("./", path, filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            self.output = open(filepath, mode, encoding="utf-8", newline='')
            self.writer = csv.writer(self.output, delimiter=delimiter)
        else:
            self.output = None
            self.writer = None
        self.wrote_header = False


    def write_review(self, review):
        """Writes a review to the given filename, and to a seperate file if 
        separate_files is True"""
        if self.writer:
            if not self.wrote_header:
                self.writer.writerow(review.keys())
                self.wrote_header = True
            self.writer.writerow(review.as_list())

        if self.separate_files:
            write_review_to_file(review, path=self.path)

    def __del__(self):
        if self.output:
            self.output.close()


def catalog_to_csv(catalog, output=None, mode="w", delimiter="\t"):
    """Export a list of reviews to a CSV file"""
    try:
        if catalog:
            with open(output, mode, encoding='utf-8', newline='') as out:
                writer = csv.writer(out, delimiter=delimiter)
                writer.writerow(catalog[0].keys())
                for review in catalog:
                    writer.writerow(review.as_list())
    except IOError as err:
        print(err)


def write_review_to_file(review, mode="w", path="./"):
    """Given a Review object, write the body of the 
    review to a file: date_artist_album.txt
    """
    filename = "_".join([review.date,
                         review.artist,
                         review.album]).strip("_") + ".txt"
    # sanitize
    filename = re.sub('[^\w\-_\. ]', '_', filename)
    try:
        filepath = os.path.join("./", path, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, mode, encoding="utf-8", newline='') as out:
            out.write(review.review)
    except IOError as err:
        print(err)
    else:
        print(f'Wrote review to {filename}')


def print_catalog(catalog):
    """Print a list of reviews to the terminal"""
    if catalog:
        header = catalog[0].keys()
        print(", ".join(header))
        for review in catalog:
            print(", ".join(review.as_list()))
    else:
        print("Catalog is empty")