import scrapy
from scrapy_splash.request import SplashRequest
from urllib.parse import urljoin

class QuotesplashSpider(scrapy.Spider):
    name = 'quotesplash'
    allowed_domains = ['quotes.toscrape.com']
    # start_urls = ['http://quotes.toscrape.com/js']


    script = """
    function main(splash, args)
    
          splash.private_mode_enabled = false
          assert(splash:go(args.url))
          assert(splash:wait(0.5))
          
          splash:set_viewport_full()
          
          return splash:html()
    end
    """

    def start_requests(self):
        yield SplashRequest(url='http://quotes.toscrape.com/js',
                            callback=self.parse,
                            endpoint="execute",
                            args={"lua_source": self.script})


    def parse(self, response):

        qoutes = response.xpath('//div[@class="quote"]')
        for qoute in qoutes:
            yield {
                "text": qoute.xpath('.//span[@class="text"]/text()').get(),
                "author": qoute.xpath('.//small[@class="author"]/text()').get(),
                "tags": ','.join( [i for i in qoute.xpath('.//a[@class="tag"]/text()').getall()] ).join(("[","]"))

            }


        next_page = response.xpath('(//ul[@class="pager"]/*/a/@href)[last()]').get()



        self.logger.info(urljoin('http://quotes.toscrape.com/js', next_page))
        self.logger.info(response.request.url)

        if next_page:
            yield SplashRequest(url=urljoin('http://quotes.toscrape.com/js', next_page),
                                callback=self.parse,
                                endpoint="execute",
                                args={"lua_source": self.script})
