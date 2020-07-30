# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import logging
import pymongo
from computerdeal.settings import MONGO_URI

class ComputerdealMongoPipeline:

    collection_name = 'products'
    #
    # @classmethod
    # def from_crawler(cls, crawler):
    #     cls.uri = crawler.setting.get("MONGO_URI")


    def open_spider(self, spirder):
        logging.warning("SPIDER OPENED FROM PIPELINE")
        self.client = pymongo.MongoClient(MONGO_URI)
        self.db = self.client["slickdeals"]


    def close_spider(self, spider):
        logging.warning("SPIDER CLOS FROM PIPELINE")
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(item)
        return item
