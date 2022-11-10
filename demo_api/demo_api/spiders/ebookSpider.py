import scrapy
import json
from scrapy.exceptions import CloseSpider

class EbookspiderSpider(scrapy.Spider):
    name = 'ebookSpider'
    allowed_domains = ['openlibrary.org']
    start_urls = ['https://openlibrary.org/subjects/picture_books.json?limit=12&offset=12']
    starter_offset = 0

    def parse(self, response):

        if response.status == 500:
            raise CloseSpider('Reached last page...')

        resp = json.loads(response.body)
        ebooks = resp.get('works')

        for ebook in ebooks:
            yield {
                'author': [value['name'] for value in ebook.get('authors')],
                'title': ebook.get('title'),
                'subject': ebook.get('subject')
            }

        self.starter_offset +=12
        yield scrapy.Request(
                url=f"https://openlibrary.org/subjects/picture_books.json?limit=12&offset={self.starter_offset}",
                callback=self.parse
            )