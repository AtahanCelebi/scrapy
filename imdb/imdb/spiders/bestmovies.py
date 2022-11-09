import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestmoviesSpider(CrawlSpider):
    name = 'bestmovies'
    allowed_domains = ['web.archive.org']
    # start_urls = ['https://web.archive.org/web/20200715000935/https://www.imdb.com/search/title/?groups=top_250&sort=user_rating']
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    def start_requests(self):
        yield scrapy.Request(url="https://web.archive.org/web/20200715000935/https://www.imdb.com/search/title/?groups=top_250&sort=user_rating",
        headers={'User-Agent':self.user_agent}
        )
    
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"), callback='parse_item', follow=True,process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="//a[@class='lister-page-next next-page'][1]"),process_request='set_user_agent')
    )

    

    def set_user_agent(self,request,spider):
        request.headers['User-Agent']=self.user_agent
        return request

    def parse_item(self, response):
        yield{
            'title':response.xpath("(//h1/text())[1]").get(),
            'year':response.xpath("//span[@id='titleYear']/a/text()").get(),
            'duration':response.xpath("normalize-space((//time)[1]/text())").get(),
            'genre':response.xpath("(//div[@class='subtext']//a)[1]/text()").get(),
            'rating':response.xpath("//div[@class='ratingValue']/strong/span/text()").get(),
            'movie_url':response.url
        }
