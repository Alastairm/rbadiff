import datetime
import string
from urllib import request





class MediaRelease(object):
    """RBA Media Release class"""

    def __init__(self, year, n):
        self.title_delim = ('<span class="rss-mr-title" itemprop="headline">','</span>')
        self.date_delim = ('<span class="value"><time class="rss-mr-date" datetime="','" itemprop="datePublished">')
        self.content_delim = ('<div class="rss-mr-content" itemprop="text">','</div>')

        self.page_text = self.get_mr(year, n)

        self.title = self.page_text.split(self.title_delim[0])[1].split(self.title_delim[1])[0]
    
    def is_interest_rate_decision(self):
        pass


    def get_mr(self, year: int, n: int):
        """ Get the nth RBA media release of year.
        
        :param year: year of media release.
        :param n: nth media release of year.
    
        """
        base_url = "https://rba.gov.au/media-releases"
        if n < 1 or n > 99:
            raise Exception('n must be 1-99')
        year = str(year)
        url = f"{base_url}/{year}/mr-{year[-2:]}-{n:02d}.html"
        print(url)
        page = request.urlopen(url)

        page_str = ''
        for line in page.readlines():
            page_str += line.decode('utf-8')
        return page_str


if __name__ == "__main__":
    a = MediaRelease(2019, 20)