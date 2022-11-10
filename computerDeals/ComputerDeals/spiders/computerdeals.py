import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector

class ComputerdealsSpider(scrapy.Spider):
    name = 'computerdeals'
    
    def remove_characters(self,value):
        return value.strip(' w/ ')


    def start_requests(self):
        yield SeleniumRequest(
            url='https://slickdeals.net/computer-deals',
            wait_time=3,
            callback=self.parse
        )


    def parse(self, response):
        products = response.xpath("//ul[@class='dealTiles categoryGridDeals blueprint']/li")
        for product in products:
                name=self.remove_characters(product.xpath("normalize-space(.//a[@class='itemTitle bp-p-dealLink bp-c-link']/text())").get())
                link=product.xpath(".//a/@href").get()
                store_name=product.xpath("normalize-space(.//button[@class='itemStore bp-p-storeLink bp-c-linkableButton  bp-c-button js-button bp-c-button--link']/text())").get()
                price=product.xpath("normalize-space(.//div[@class='itemPrice  wide ']/text())").get()

                #on the land page extract possible datas and send with META tag
                #follow through that item -> parse_comment() and extract more specific details
                #link = {f/16089061-asrock-b550-phantom-gaming...} ----> with follow METHOD it refers "slickdeals.net/f/16089061-asrock-b550-phantom-gaming..."
                yield response.follow(url=link,callback=self.parse_comment,meta={
                    'name':name,
                    'store_name':store_name,
                    'price':price
                })

            

        #if finised one page next another one till the end
        nextPage = response.xpath("//a[@data-role='next-page']/@href").get()
        if nextPage:
            absoluteURL = f"https://slickdeals.net{nextPage}"
            yield SeleniumRequest(
                url=absoluteURL,
                wait_time=3,
                callback=self.parse
            )


    def parse_comment(self,response):
        name = response.request.meta['name']
        store_name = response.request.meta['store_name']
        price = response.request.meta['price']

        comments = response.xpath("//div[@class='viewsAndComments']")
        for comment in comments:
                comment_count  = comment.xpath(".//div[2]/a/label/text()").get()
                view_count  = comment.xpath(".//div[@id='dealViews']/span[2]/text()").get()
                yield{
                    'name':name,
                    'store_name':store_name,
                    'price':price,
                    'comment_count:': comment_count,
                    'view_count':view_count
                }
