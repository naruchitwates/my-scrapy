import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys

from scrapy.selector import Selector

class DuckduckgoseleniumSpider(scrapy.Spider):
    name = 'duckduckgoselenium'
    allowed_domains = ['duckduckgo.com']
    #start_urls = ['http://duckduckgo.com/']


    def start_requests(self):
        yield SeleniumRequest(url='https://duckduckgo.com',
                              wait_time=3,
                              screenshot=True,
                              callback=self.parse)



    def parse(self, response):

         # img = response.meta['screenshot']
         #
         # with open('screenshot.png', 'wb') as f:
         #     f.write(img)



        driver = response.meta['driver']

        search_input = driver.find_element_by_xpath('//form/input[@id="search_form_input_homepage"]')
        search_input.send_keys('my user agent')

        search_input.send_keys(Keys.ENTER)

        driver.save_screenshot("output.png")

        #self.logger.info(response.text)

        html = driver.page_source
        self.logger.info(type(html))
        response_obj = Selector(text=html)

        links = response_obj.xpath('//div[@id="links"]//div[@class="result__extras__url"]/a')
        self.logger.info(type(links))

        for link in links:
                yield {
                    "url": link.xpath('.//@href').get()
                }




