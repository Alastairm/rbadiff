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

        title_delim = ('<span class="rss-mr-title" itemprop="headline">','</span>')
        date_delim = ('<time class="rss-mr-date" datetime="','" itemprop="d')
        content_delim = ('<div class="rss-mr-content" itemprop="text">','</div>')

        self.page_text = self.get_mr()
        self.title = self.page_text.split(title_delim[0])[1].split(title_delim[1])[0]
        self.is_mpd = self.title[-24:] == 'Monetary Policy Decision'

        # Fetch 'yyyy-mm-dd' str from time element and convert to date.
        date = self.page_text.split(date_delim[0])[1].split(date_delim[1])[0].split('-')
        self.date = datetime.date(int(date[0]), int(date[1]), int(date[2]))

        content = self.page_text.split(content_delim[0])[1].split(content_delim[1])[0]
        self.release_content = content.replace('<p>','').replace('</p>', '\n \n')


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
        
        page_str = re.sub(r'\s+', ' ', page_str)
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


def get_most_recent_mpd_mr():
    year = datetime.date.today().year
    mrs = get_year_mrs(year)
    for mr in mrs[::-1]:
        if mr.is_mpd:
            return mr


if __name__ == "__main__":
    print(get_most_recent_mpd_mr().release_content)
