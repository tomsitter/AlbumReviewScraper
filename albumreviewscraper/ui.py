"""Functions used for command line interface
Can print a list of Review objects to the terminal or to a CSV file
Simply pass a list of Review objects to ask_for_input() 

reviews = [review1, review2, ...]
ask_for_input(reviews)

"""

import csv
import sys


def ask_for_input(catalog):
    """Command line prompt if file fails"""
    choice = input("Type 'q' to quit, 'p' to print reviews to console, or enter the filename to write to: ")
    if choice == 'q':
        sys.exit()
    elif choice == 'p':
        print_catalog(catalog)
    else:
        try:
            catalog_to_csv(catalog, output=choice)
            print('Wrote {} reviews to {}'.format(len(catalog), choice))
        except IOError as err:
            print(err)
    ask_for_input(catalog)


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


class FileStream:
    def __init__(self, filename, mode="w", delimiter="\t"):
        self.output = open(filename, mode, encoding="utf-8", newline='')
        self.writer = csv.writer(self.output, delimiter=delimiter)
        self.wrote_header = False

    def write_review(self, review):
        if not self.wrote_header:
            self.writer.writerow(review.keys())
            self.wrote_header = True
        self.writer.writerow(review.as_list())

    def __del__(self):
        self.output.close()

def print_catalog(catalog):
    """Print a list of reviews to the terminal"""
    if catalog:
        header = catalog[0].keys()
        print(", ".join(header))
        for review in catalog:
            print(", ".join(review.as_list()))
    else:
        print("Catalog is empty")
