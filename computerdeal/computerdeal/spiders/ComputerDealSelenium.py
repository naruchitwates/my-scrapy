import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest

class ComputerdealseleniumSpider(scrapy.Spider):
    name = 'ComputerDealSelenium'
    # allowed_domains = ['slickdeals.net']
    # start_urls = ['https://slickdeals.net/computer-deals/']


    def start_requests(self):
            yield SeleniumRequest(
                url='https://slickdeals.net/computer-deals/'
                ,wait_time=3
                ,callback=self.parse
            )


    def parse(self, response):

        # No modify on request
        # driver = response.meta['driver']
        # html = driver.page_source
        # driver.save_screenshot("output.png")
        #
        #
        # response_obj = Selector(text=html)

        items = response.xpath('//ul[@class="dealTiles categoryGridDeals"]/li[starts-with(@class,"fpGridBox")]')

        for item in items:
            yield {
                'page': response.url,
                'product_page': "https://slickdeals.net{}".format(item.xpath('.//div[@class="itemImageLink"]//a[starts-with(@class,"itemTitle")]/@href').get()),
                'product_img': item.xpath('.//div[@class="itemImageLink"]//img/@data-original').get(),
                'product_title': item.xpath('.//div[@class="itemImageLink"]//a[starts-with(@class,"itemTitle")]/text()').get(),
                'product_price': item.xpath('normalize-space(.//div[@class="priceLine"]/div[starts-with(@class,"itemPrice")]/text())').get(),
                'product_store': item.xpath('.//div[@class="itemImageLink"]//span[@class="blueprint"]/button/text()').get()

            }


        next_page = response.xpath('//div[@class="pagination buttongroup"]/a[@data-role="next-page"]/@href').get()
        if next_page:
            abs_url = f"https://slickdeals.net{next_page}"
            yield SeleniumRequest(
                url=abs_url,
                wait_time=3,
                callback=self.parse
            )




