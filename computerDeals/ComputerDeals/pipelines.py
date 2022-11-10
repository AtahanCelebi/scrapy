# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
import logging

class MongodbPipeline(object):
    collection_name = "all_deals" # under the database it refes collection name

        

    def open_spider(self,spider):
        """
        Go <Database Access> click "ADD NEW DATABASE USER"
        it includes your userName and password
        PS: Do not forget select "Built-in Role" --> Atlas admin or Read and write to any database authentication
        Go <Network Access> click "ADD IP ADRESS" button
        0.0.0.0/0   
        """
        self.client = pymongo.MongoClient("mongodb+srv://ata:ata@cluster0.3lic3mt.mongodb.net/?retryWrites=true&w=majority") #port of the database
        self.db = self.client["ComputerDeals"] #database name

    def close_spider(self,spider):
        self.client.close()

    def process_item(self,item,spider):
        self.db[self.collection_name].insert(item)
        return item