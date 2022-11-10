import scrapy
import json

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    # Under the Network > Heades --> get REQUEST URL 
    start_urls = ['https://quotes.toscrape.com/api/quotes?page=1']

    def parse(self, response):
        resp = json.loads(response.body)

        # Network> Fetch/XHR > Preview --> there is a key called "quotes" //we want that
        quotes = resp.get('quotes')
        #print(quotes)
        for quote in quotes:
            yield{
                'author': quote.get('author').get('name'),
                'tags': quote.get('tags'),
                'text': quote.get('text')
            }

        has_next = resp.get("has_next") # returns boolean variable
        if has_next: 
            next_page = int(resp.get("page"))+1
            
            yield scrapy.Request(
                url=f'https://quotes.toscrape.com/api/quotes?page={next_page}',
                callback=self.parse 
            )
