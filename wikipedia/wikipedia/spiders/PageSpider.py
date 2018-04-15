from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider

from bs4 import BeautifulSoup
from wikipedia.items import WikipediaItem


class PagesSpider(CrawlSpider):
    """
    the Page Spider for wikipedia
    """
    name = "wikipedia_pages"
    allowed_domains = ["wikipedia.org"]

    start_urls = [
        "https://en.wikipedia.org/wiki/Internet",
        "https://en.wikipedia.org/wiki/Computer_program",
        "https://en.wikipedia.org/wiki/History",
        "https://en.wikipedia.org/wiki/Geography",
        "https://en.wikipedia.org/wiki/Mathematics",
        "https: // en.wikipedia.org / wiki / Music",
        "https: // en.wikipedia.org / wiki / Biology",
        "https: // en.wikipedia.org / wiki / History",
        "https: // en.wikipedia.org / wiki / Medicine",
        "https: // en.wikipedia.org / wiki / Nature",
    ]

    rules = (
        Rule(LinkExtractor(allow="https://en\.wikipedia\.org/wiki/.+_.+",
                           deny=[
                               "https://en\.wikipedia\.org/wiki/File.*"
                               "https://en\.wikipedia\.org/wiki/Wikipedia.*",
                               "https://en\.wikipedia\.org/wiki/Main_Page",
                               "https://en\.wikipedia\.org/wiki/Talk.*",
                               "https://en\.wikipedia\.org/wiki/Portal.*",
                               "https://en\.wikipedia\.org/wiki/Special.*"
                               "https://en\.wikipedia\.org/wiki/Category.*"
                               "https://en\.wikipedia\.org/wiki/Template.*"
                               "https://en\.wikipedia\.org/wiki/Help.*"
                               "https://en\.wikipedia\.org/wiki/Template_talk.*"
                               "https://en\.wikipedia\.org/wiki/User.*"
                               "https://en\.wikipedia\.org/wiki/User_talk.*"
                           ],
                           restrict_xpaths="//div[@id='mw-content-text']//a[@href][position() < 200]",
                           ),
             callback='parse_wikipedia_page'),
    )
    #
    NUMBER_OF_URLS = 12000

    def parse_wikipedia_page(self, response):
        self.NUMBER_OF_URLS = self.NUMBER_OF_URLS - 1
        print(self.NUMBER_OF_URLS)

        # if self.NUMBER_OF_URLS < 1:
        #     raise CloseSpider('bandwidth_exceeded')

        item = WikipediaItem()
        soup = BeautifulSoup(response.body)

        item['url'] = response.url
        item['name'] = soup.find("h1", {"id": "firstHeading"}).string
        content = soup.find("div", {"id": "mw-content-text"})
        description = content.find("div", {"class": "mw-parser-output"})
        description = description.find('p').get_text()

        outgoing_urls = []
        for link in content.find_all('a', href=True):
            href = link.get('href')
            if '/wiki/' in href \
                    and href.find("/wiki/User:") == -1 \
                    and href.find("/wiki/User_talk:") == -1 \
                    and href.find("/wiki/Main_Page:") == -1 \
                    and href.find("/wiki/File:") == -1 \
                    and href.find("/wiki/Wikipedia:") == -1 \
                    and href.find("/wiki/Main_Page:") == -1 \
                    and href.find("/wiki/Talk:") == -1 \
                    and href.find("/wiki/Portal:") == -1 \
                    and href.find("/wiki/Special:") == -1 \
                    and href.find("/wiki/Category:") == -1 \
                    and href.find("/wiki/Template:") == -1 \
                    and href.find("/wiki/Help:") == -1 \
                    and href.find("/wiki/Template_talk:") == -1 \
                    and href.find("/https://") == -1 \
                    and href not in outgoing_urls:
                outgoing_urls.append(href)

        # description = soup.find("div", {"id": "mw-content-text"})
        # get the first tag
        # description = string_from_listing(description.find('p'))

        item['description'] = description
        item['outgoing_urls'] = outgoing_urls

        return item
