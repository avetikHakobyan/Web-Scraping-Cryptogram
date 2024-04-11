import unittest
import urllib.request as req
from QuotesParser import *


class QuotesParserTests(unittest.TestCase):

    def __init__(self, method_name: str = "runTest") -> None:
        super().__init__(method_name)
        self.test_valid_urls = {"https://www.goodreads.com/quotes": 30, "https://www.goodreads.com/quotes?page=2": 30,
                                "https://www.goodreads.com/quotes?page=3": 30}
        self.test_invalid_url = {"https://www.goodreads.com/about/us": 0}

    def test_valid_get_quotes(self):
        for url, expected in self.test_valid_urls.items():
            with req.urlopen(url) as f:
                lines = list(line.decode("utf-8").strip() for line in f.readlines())

            test_parser = QuotesParser()

            for line in lines:
                test_parser.feed(line)
            self.assertEqual(len(test_parser.get_quotes()), expected)

    def test_invalid_get_quotes(self):
        for url, expected in self.test_invalid_url.items():
            with req.urlopen(url) as f:
                lines = list(line.decode("utf-8").strip() for line in f.readlines())

            test_parser = QuotesParser()

            for line in lines:
                test_parser.feed(line)
            self.assertEqual(len(test_parser.get_quotes()), expected)


if __name__ == '__main__':
    unittest.main(verbosity=2)
