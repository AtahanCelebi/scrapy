import scrapy


class Debt22Spider(scrapy.Spider):
    name = 'debt22'
    # allowed_domains = ['worldpopulationreview.com']
    # start_urls = ['http://worldpopulationreview.com/countries/countries-by-national-debt']

    headers = {"user_agent":"Mozilla/5.0 (X11; CrOS x86_64 14943.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}

    def start_requests(self):
        yield scrapy.Request(url='https://web.archive.org/web/20180224034716/http://worldpopulationreview.com',callback=self.parse,headers=self.headers)


    def parse(self, response):
        print("**************************************************************")
        row1 = response.xpath("//table/tbody/tr/td/a/text()")
        row2 = response.xpath("//table/tbody/tr/td[3]")
        
           
        for i in range(len(row1)):
            yield{
                "country":row1[i].get(),
                "den":row2[i].get()
            }
