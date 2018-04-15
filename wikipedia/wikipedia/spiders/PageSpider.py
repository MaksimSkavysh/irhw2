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
        "https://en.wikipedia.org/wiki/Java",
        "https://en.wikipedia.org/wiki/Metallica",
        "https://en.wikipedia.org/wiki/River",
        "https://en.wikipedia.org/wiki/United_Nations",
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
                           ],
                           restrict_xpaths="//div[@id='mw-content-text']//a[@href][position() < 100]",
                           ),
             callback='parse_wikipedia_page'),
    )
    #
    NUMBER_OF_URLS = 12000

    def parse_wikipedia_page(self, response):
        self.NUMBER_OF_URLS = self.NUMBER_OF_URLS - 1

        if self.NUMBER_OF_URLS < 1:
            raise CloseSpider('bandwidth_exceeded')

        item = WikipediaItem()
        soup = BeautifulSoup(response.body)

        item['url'] = response.url
        item['name'] = soup.find("h1", {"id": "firstHeading"}).string
        content = soup.find("div", {"id": "mw-content-text"})
        description = content.find("div", {"class": "mw-parser-output"})
        description = description.find('p').get_text()

        outgoing_urls = []
        for link in content.find_all('a', href=True):
            # print(link.get('href'))
            href = link.get('href')
            if '/wiki/' in href \
                    and '/wiki/Main_Page' not in href \
                    and '/File:' not in href \
                    and '/Category:' not in href \
                    and '/Template:' not in href \
                    and '/Wikipedia:' not in href \
                    and '/Portal:' not in href \
                    and 'https://www.wikidata.org/wiki/' not in href \
                    and href not in outgoing_urls:
                outgoing_urls.append(href)

        # description = soup.find("div", {"id": "mw-content-text"})
        # get the first tag
        # description = string_from_listing(description.find('p'))

        item['description'] = description
        item['outgoing_urls'] = outgoing_urls

        return item
