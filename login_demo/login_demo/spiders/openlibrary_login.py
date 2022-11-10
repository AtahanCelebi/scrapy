import scrapy
from scrapy import FormRequest

class OpenlibraryLoginSpider(scrapy.Spider):
    name = 'openlibrary_login'
    allowed_domains = ['openlibrary.org']
    start_urls = ['https://openlibrary.org/account/login']

    def parse(self, response):
        yield FormRequest.from_response(
            response,
            formid = 'register',
            formdata={                        #formdata under network after login process which we have fetch it
                'username':'atahancelebi98@gmail.com',
                'password': 'de7a7838',
                'redirect':'',
                'debug_token': '',
                'login': 'Log In'
            },
            callback = self.after_login
        )

    def after_login(self,response):
        print("********************Log In")