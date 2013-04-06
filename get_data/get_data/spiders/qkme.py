#spider for crawling quickmeme
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import os.*


class QkmeSpider(BaseSpider):
    
	def __init__ (self):
		self.name = "Qkme"
		self.allowed_domains = ["quickmeme.com"]
		self.start_urls = ["http://www.quickmeme.com/Socially-Awkward-Penguin/"]

    def parse (self, response):
	
		hxs = HtmlXPathSelector(response)
		test_text = hxs.select("//a[@href='/Actual-Advice-Mallard/']/text()").extract()
		print test_text
