from datetime import date
from html.parser import HTMLParser
import re
from urllib import request


from statement import Statement

class RBAMRParser(HTMLParser):
    statement = Statement()
    in_content = False

    def handle_startendtag(self, tag, attrs):
        attrs = dict(attrs)
        
        if tag == 'meta' and 'name' in attrs.keys() and 'content' in attrs.keys():
            name = attrs['name']
            content = attrs['content']
            if name == 'dcterms.identifier':
                self.statement.url = content
            if name == 'dcterms.title':
                self.statement.title = content
            if name == 'dcterms.description':
                self.statement.description = content
            if name == 'dcterms.created':
                pub_date = date(*list(map(int, content.split('-'))))
                self.statement.pub_date = pub_date

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if tag == 'div' and 'itemprop' in attrs.keys() and attrs['itemprop'] == 'text':
            self.in_content = True

    def handle_endtag(self, tag):
        if self.in_content:
            if tag == 'div':
                self.in_content = False
            elif tag == 'p':
                self.statement.content += '\n'

    def handle_data(self, data):
        if self.in_content:
            data = re.sub(r'\s+', ' ', data)
            self.statement.content += data


def parse_url(url):
    print(f"GET: {url}")
    page = request.urlopen(url)

    page_str = ''
    for line in page.readlines():
        page_str += line.decode('utf-8')
    print(f"PAGE:{page_str}")
    parser = RBAMRParser()
    parser.feed(page_str)

    return parser.statement