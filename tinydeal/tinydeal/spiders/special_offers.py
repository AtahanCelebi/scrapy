import scrapy


class SpecialOffersSpider(scrapy.Spider):
    name = 'special_offers'
    allowed_domains = ['web.archive.org']
    start_urls = ['https://web.archive.org/web/20180324020147/https://www.tinydeal.com/products_all.html']
    #scrapy crawl special_offers -o dataset.json
    def parse(self, response):
        rows = response.xpath("//ul[@class='productlisting-ul']/div/li")
        for product in rows:
            yield{
                'title': product.xpath(".//a[@class='p_box_title']/text()").get(),
                'link': response.urljoin(product.xpath(".//a[@class='p_box_title']/@href").get()),
                'discount_price': product.xpath(".//div[@class='p_box_price']/span[1]/text()").get(),
                'normal_price': product.xpath(".//div[@class='p_box_price']/span[2]/text()").get()
            }

        next_page = response.xpath("//a[@class='nextPage']/@href").get()
        if next_page: #if exsist
            yield scrapy.Request(url=next_page,callback=self.parse)