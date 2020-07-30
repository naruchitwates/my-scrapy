import scrapy
from scrapy.http import Request
import json

class QoutesapiSpider(scrapy.Spider):
    name = 'QoutesAPI'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/scroll/']

    def start_requests(self):
        yield Request(url="http://quotes.toscrape.com/api/quotes?page=1",
                      callback=self.parse
                          )

    def parse(self, response):

        # self.logger.info(response.body)
        data = json.loads(response.body)
        has_next = data.get('has_next')
        at_page = data.get('page')
        quotes = data.get('quotes')

        for quote in quotes:
                yield {
                    'name': quote.get('author').get('name'),
                    'goodreads_link': quote.get('author').get('goodreads_link'),
                    'slug': quote.get('author').get('slug'),
                    'tags': quote.get('tags'),
                    'text': quote.get('text'),
                    'page': at_page,
                    'url':  response.request.url
                }


        if has_next:
            yield Request(url=f"http://quotes.toscrape.com/api/quotes?page={at_page+1}",
                          callback=self.parse
                          )
