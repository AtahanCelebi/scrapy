import scrapy
from scrapy.loader import ItemLoader
from ..items import SteamItem
from w3lib.html import remove_tags

class BestSellingSpider(scrapy.Spider):
    name = 'best_selling'
    allowed_domains = ['store.steampowered.com']
    start_urls = ['https://store.steampowered.com/search/?filter=topsellers']


    def get_platforms(self,classes):
        platforms = list()
        for item in classes:
            platform = item.split(' ')[-1]

            if platform == 'win':
                platforms.append('Windows')
            if platform == 'mac':
                platforms.append('Mac os')
            if platform == 'linux':
                platforms.append('Linux')
            if platform == 'vr_required':
                platforms.append('VR REQUIRED')    
            if platform == 'vr_supported':
                platforms.append('VR SUPPORTED')    

        return platforms


    def remove_html(self,review):
        cleaned = ""
        try:
            cleaned = remove_tags(review)
        except TypeError:
            cleaned = 'No reviews'
        
        return cleaned

    def remove_minus(self,item):
        if item: # if it is not None
            return item.lstrip('-')
        return item

    def get_original_price(self,selector_obj):
        original_price = ''
        div_with_discount = selector_obj.xpath(".//div[contains(@class,'search_price discounted')]") #it returns list if it exsist (searching discounted)
        if len(div_with_discount)> 0:
            original_price = div_with_discount.xpath(".//span/strike/text()").get()
        else:
            original_price = selector_obj.xpath("normalize-space(.//div[contains(@class,'search_price')]/text())").get()
        return original_price

    
    def parse(self, response):
        steam_item = SteamItem()
        games = response.xpath("//div[@id='search_resultsRows']/a")
        for game in games:
            loader = ItemLoader(item=SteamItem(),selector=game,response=response)
            loader.add_xpath("game_url",".//@href")
            loader.add_xpath("img_url",".//div[@class='col search_capsule']/img/@src")
            loader.add_xpath("game_name",".//span[@class='title']/text()")
            loader.add_xpath("release_date",".//div[@class='col search_released responsive_secondrow']/text()")

            loader.add_xpath("platforms",".//span[contains(@class,'platform_img win') or @class='vr_supported' or @class='vr_required']/@class")
            loader.add_xpath("reviews","//span[contains(@class,'search_review_summary')]/@data-tooltip-html")
            loader.add_xpath("discounted_rate",".//div[@class='col search_discount responsive_secondrow']/span/text()")
            loader.add_xpath("original_price",".//div[contains(@class,'search_price_discount_combined')]")

            yield loader.load_item()



            # steam_item['game_url'] = game.xpath(".//@href").get()            
            # steam_item['img_url'] = game.xpath("//div[@class='col search_capsule']/img/@src").get()            
            # steam_item['game_name'] = game.xpath(".//span[@class='title']/text()").get()       
            # steam_item['release_date'] = game.xpath(".//div[@class='col search_released responsive_secondrow']/text()").get()     
            #      
            # steam_item['platforms'] = self.get_platforms(game.xpath(".//span[contains(@class,'platform_img win') or @class='vr_supported' or @class='vr_required']/@class").getall()) 
            # steam_item['reviews'] = self.remove_html(game.xpath(".//span[contains(@class,'search_review_summary')]/@data-tooltip-html").get())
            # steam_item['discounted_rate'] = self.remove_minus(game.xpath(".//div[@class='col search_discount responsive_secondrow']/span/text()").get())
            # steam_item['original_price'] =  self.get_original_price(game.xpath(".//div[contains(@class,'search_price_discount_combined')]"))

            #yield steam_item     

            # next_page =  response.xpath(".//a[@class='pagebtn' and text()='>']/@href").get()
            # if next_page:
            #     yield scrapy.Request(
            #         url=next_page,
            #         callback=self.parse
            #     )  
                       