from html.parser import HTMLParser


class QuotesParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.quote_list = []
        self.in_quote = False

    def clean_quote(self, quote):
        if "<br />" in quote:
            quote = self.rawdata.replace("<br />", " ")
        quote = quote.replace("&ldquo;", "")
        quote = quote.replace("&rdquo;", "")
        return quote

    def handle_starttag(self, tag, attrs):
        if tag == "div" and ("class", "quoteText") in attrs:
            self.in_quote = True

    def handle_data(self, data):
        if self.in_quote:
            quote = self.rawdata
            quote = self.clean_quote(quote)
            self.quote_list.append(quote)
            self.in_quote = False

    def get_quotes(self):
        return self.quote_list
