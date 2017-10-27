""" Review class holds formatted data from scraped album reviews.
"""
import datetime
import html

class Review:
    """Holds review data.
    Can be serialized to list and has .keys() method to get a header for export to tabular data
    Dates must be datetime.date objects and are serialized to yyyy-mm-dd when queried
    reviews are automatically sanitized of newlines and tabs
    """
    def __init__(self, date=None, artist=None, album=None, review=None, rating=None):
        self._date = date
        self.artist = artist
        self.album = album
        self.review = review
        self._rating = rating

    @staticmethod
    def sanitize(review):
        return html.unescape(review).replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').strip()

    def keys(self):
        return [key.lstrip("_") 
                for key in vars(self).keys()]

    def as_list(self):
        # returns the items as a list
        return [self.__getattribute__(key) for key in self.keys()]

    @property
    def date(self):
        date_format = "%Y-%m-%d"
        if self._date:
            return self._date.strftime(date_format)
        else:
            return self._date

    @date.deleter
    def date(self):
        del self._date

    @date.setter
    def date(self, value):
        if value and isinstance(value, datetime.date):
            self._date = value
        else:
            self._date = None
            raise ValueError("Date must be of type datetime.date")

    @property
    def review(self):
        return self._review

    @review.deleter
    def review(self):
        del self._review
    
    @review.setter
    def review(self, value):
        self._review = self.sanitize(value)

    @property
    def rating(self):
        return str(self._rating)