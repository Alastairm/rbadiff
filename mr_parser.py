from datetime import date
from html.parser import HTMLParser
from urllib import request


from statement import Statement

class RBAMRParser(HTMLParser):
    statement = Statement()
    in_content = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if tag is 'div' and 'itemprop' in attrs.keys() and attrs['itemprop'] is 'text':
            self.in_content = True

    def handle_startendtag(self, tag, attrs):
        attrs = dict(attrs)
        
        if tag is 'meta' and 'name' in attrs.keys() and 'content' in attrs.keys():
            name = attrs['name']
            content = attrs['content']
            if name is 'dcterms.identifier':
                self.statement.url = content
            if name is 'dcterms.title':
                self.statement.title = content
            if name is 'dcterms.description':
                self.statement.description = content
            if name is 'dcterms.created':
                pub_date = date(*content.split('-'))
                self.statement.pub_date = pub_date



    def handle_endtag(self, tag):
        if self.in_content:
            if tag is 'div':
                self.in_content = False
            elif tag is 'p':
                self.statement.content += '\n'

    def handle_data(self, data):
        if self.in_content:
            self.statement.content += data

def parse_url(url):
    page = request.urlopen(url)

    page_str = ''
    for line in page.readlines():
        page_str += line.decode('utf-8')
    
    parser = RBAMRParser()
    parser.feed(page_str)

    return parser.statement