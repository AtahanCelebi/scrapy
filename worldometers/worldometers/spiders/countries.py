import scrapy


class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']
    # start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    headers = {"user_agent":"Mozilla/5.0 (X11; CrOS x86_64 14943.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}

    def start_requests(self):
        yield scrapy.Request(url='https://www.worldometers.info/world-population/population-by-country/',callback=self.parse,headers=self.headers)

    def parse(self, response):
        countries = response.xpath("//td/a")
        for c in countries:
            name = c.xpath(".//text()").get()
            link = c.xpath(".//@href").get()


            yield response.follow(url=link, callback=self.parse_country,meta={'country_name':name}) #follow the links


            # absolute_url = f"https://www.worldometers.info{link}"
            # yield scrapy.Request(url=absolute_url)


            # yield{
            #     'title':name,
            #     'country_link':link
            # }

    def parse_country(self,response):
            name = response.request.meta['country_name']
            rows = response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr[1]")
            for row in rows:
                year = row.xpath(".//td[1]/text()").get()
                population = row.xpath(".//td[2]/strong/text()").get()

                yield{
                    "Country":name,
                    "year":year,
                    "population":population
                }

