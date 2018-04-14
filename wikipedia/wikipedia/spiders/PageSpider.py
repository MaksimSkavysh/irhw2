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
        "https://en.wikipedia.org/wiki/Mountain"
    ]

    rules = (
        Rule(LinkExtractor(allow="https://en\.wikipedia\.org/wiki/.+_.+",
                           deny=[
                               "https://en\.wikipedia\.org/wiki/Wikipedia.*",
                               "https://en\.wikipedia\.org/wiki/Main_Page",
                               "https://en\.wikipedia\.org/wiki/Free_Content",
                               "https://en\.wikipedia\.org/wiki/Talk.*",
                               "https://en\.wikipedia\.org/wiki/Portal.*",
                               "https://en\.wikipedia\.org/wiki/Special.*"
                               "https://en\.wikipedia\.org/wiki/File.*"
                               "https://en\.wikipedia\.org/wiki/Category.*"
                               "https://en\.wikipedia\.org/wiki/Template.*"
                           ]),
             callback='parse_wikipedia_page'),
    )

    NUMBER_OF_URLS = 2

    def parse_wikipedia_page(self, response):
        # self.NUMBER_OF_URLS = self.NUMBER_OF_URLS - 1
        #
        # if self.NUMBER_OF_URLS < 1:
        #     raise CloseSpider('bandwidth_exceeded')

        item = WikipediaItem()
        soup = BeautifulSoup(response.body)

        item['url'] = response.url
        item['name'] = soup.find("h1", {"id": "firstHeading"}).string

        description = soup.find("div", {"id": "mw-content-text"})
        description = description.find("div", {"class": "mw-parser-output"})
        description = description.find('p').get_text()

        # description = soup.find("div", {"id": "mw-content-text"})
        # get the first tag
        # description = string_from_listing(description.find('p'))

        item['description'] = description

        return item
