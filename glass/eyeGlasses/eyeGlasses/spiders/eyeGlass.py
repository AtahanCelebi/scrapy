import scrapy


class EyeglassSpider(scrapy.Spider):
    name = 'eyeGlass'
    allowed_domains = ['www.glassesshop.com']
    start_urls = ['https://www.glassesshop.com/bestsellers']





    def parse(self, response):
        for product in response.xpath("//div[@id='product-lists']/div"):
            product_name = product.xpath("normalize-space(.//div[@class='p-title']/a[1]/text())").get()
            if product_name:
                image_url = product.xpath(
                    "//div[@id='product-lists']/div//div//img[@class='lazy w-100 product-img-second']/@data-src").get()
                product_url = product.xpath(
                    ".//div[@class='p-title']/a[1]/@href").get()
                product_price = product.xpath(
                    ".//div[@class='p-price']/div[1]/span[1]/text()").get()
    
                yield{
                    'Product_Name': product_name,
                    'Price': product_price,
                    'URL': product_url,
                    'Image_URL': image_url
                }

        nextPage = response.xpath("//a[@class='page-link']/@href").get()
        if nextPage:
            yield scrapy.Request(url=nextPage,callback=self.parse)
