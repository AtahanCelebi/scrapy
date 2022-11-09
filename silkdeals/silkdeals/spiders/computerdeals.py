import scrapy
from scrapy_selenium import SeleniumRequest

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
            yield{
                'name':self.remove_characters(product.xpath("normalize-space(.//a[@class='itemTitle bp-p-dealLink bp-c-link']/text())").get()),
                'link':product.xpath(".//a/@href").get(),
                'store_name':product.xpath("normalize-space(.//button[@class='itemStore bp-p-storeLink bp-c-linkableButton  bp-c-button js-button bp-c-button--link']/text())").get(),
                'price':product.xpath("normalize-space(.//div[@class='itemPrice  wide ']/text())").get()
            }


        nextPage = response.xpath("//a[@data-role='next-page']/@href").get()
        if nextPage:
            absoluteURL = f"https://slickdeals.net{nextPage}"
            yield SeleniumRequest(
                url=absoluteURL,
                wait_time=3,
                callback=self.parse
            )
