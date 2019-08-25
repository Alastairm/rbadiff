import datetime
import re
import string

from urllib import request
from urllib import error


class MediaRelease(object):
    """RBA Media Release class"""

    def __init__(self, year, n):
        self.mr_year = year
        self.mr_n = n
        self.title_delim = ('<span class="rss-mr-title" itemprop="headline">','</span>')
        self.date_delim = ('<time class="rss-mr-date" datetime="','" itemprop="d')
        self.content_delim = ('<div class="rss-mr-content" itemprop="text">','</div>')

        self.page_text = self.get_mr()

        self.title = self.page_text.split(self.title_delim[0])[1].split(self.title_delim[1])[0]
        
        self.interest_rate_decision = self.title[-24:] == 'Monetary Policy Decision'

        # Fetch 'yyyy-mm-dd' str from time element and convert to date.
        _date = self.page_text.split(self.date_delim[0])[1].split(self.date_delim[1])[0]
        _date = _date.split('-')
        self.date = datetime.date(int(_date[0]), int(_date[1]), int(_date[2]))

        _content = self.page_text.split(self.content_delim[0])[1].split(self.content_delim[1])[0]
        _content = _content.replace('<p>','').replace('</p>', '\n \n')
        self.release_content = _content


    def get_mr(self):
        """ Get the nth RBA media relase of year.

        :returns: (str) media release page html
        """
        year = str(self.mr_year)
        n = self.mr_n

        base_url = "https://rba.gov.au/media-releases"
        if n < 1 or n > 99:
            raise ValueError('n must be 1-99')

        url = f"{base_url}/{year}/mr-{year[-2:]}-{n:02d}.html"
        print(f"GET: {url}")
        page = request.urlopen(url)

        page_str = ''
        for line in page.readlines():
            page_str += line.decode('utf-8')
        
        page_str = re.sub('\s+', ' ', page_str)
        return page_str


def get_year_mrs(year):
    mrs = []
    n = 0
    while True:
        n += 1
        try:
            mrs.append(MediaRelease(year, n))
        except error.HTTPError:
            return mrs


def get_most_recent_mpd_mr(year):
    mrs = get_year_mrs(year)
    for mr in mrs[::-1]:
        if mr.interest_rate_decision:
            return mr


if __name__ == "__main__":
    year = datetime.date.today().year
    print(get_most_recent_mpd_mr(year).release_content)
