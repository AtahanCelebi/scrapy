# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from shutil import which
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector

class ExampleSpider(scrapy.Spider):
    name = 'example'

    chrome_options = Options()
    # chrome_options.add_argument("--headless")

    chrome_path = which("chromedriver")

    driver = webdriver.Chrome(executable_path=chrome_path,options=chrome_options)
    
    def start_requests(self):
        yield SeleniumRequest(
            url='https://duckduckgo.com',
            wait_time=3,
            screenshot=True,
            callback=self.parse
        )

    def parse(self, response):
        # img = response.meta['screenshot']

        # with open('screenshot.png', 'wb') as f:
        #     f.write(img)

        driver = response.meta['driver']
        search_input = driver.find_element_by_xpath("//*[@id='search_form_input_homepage']")
        search_input.send_keys('Hello World')

        # driver.save_screenshot('after_filling_input.png') #after typing hello world takes screenshot

        search_input.send_keys(Keys.ENTER)
        # driver.save_screenshot('enter.png') #after typing Hello World takes screenshot

        html = driver.page_source #we changed our initial page from duckduckgo.com to
        response_obj = Selector(text=html) # duckduckgo.com/Hello-World. So thats why we use Selector for current page to 
                                            #extract datas with scrapy.


        links = response_obj.xpath("//div[@class='ikg2IXiCD14iVX7AdZo1']")

        for link in links:
            yield{
                'URL':link.xpath(".//a/@href").get(),
                'name':link.xpath("normalize-space(.//span/text())").get()
            }


      
