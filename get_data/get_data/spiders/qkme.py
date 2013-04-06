#spider for crawling quickmeme
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request


# Class: QkmeSpider
# -----------------
# spider to crawl through quickmeme and scrape text from advice animals.
# currently only scrapes meme types that are hard-coded in.
class QkmeSpider (BaseSpider):
    name = "qkme"
    allowed_domains = ["quickmeme.com"]
    start_urls = ["http://www.quickmeme.com/Socially-Awkward-Penguin/"]
    
    def __init__ (self):

        #list to contain the absolute links to each instance page
        self.instance_page_hrefs = []

        pass
    
    
    def print_status (self, status_string):
        print "##### Status: " + status_string + "#####"
    
    # Function: parse
    # ---------------
    # this function will parse a hard-coded meme-type's page and extract
    # links to each individual meme instance's page.
    def parse (self, response):
        self.print_status("Scanning meme-type page")
        
        hxs = HtmlXPathSelector(response)
        
        #xpath expression to extract the links to each meme instance page
        instance_page_hrefs_xpath = '//div[@class="memeThumb"]/a/@href'
        
        #xpath for the 'next page' href
        next_page_hrefs_xpath = '//a[@class="next"]/@href'
        
        instance_page_hrefs = hxs.select(instance_page_hrefs_xpath).extract ()
        next_page_hrefs = hxs.select (next_page_hrefs_xpath).extract ()


        BaseURL = 'http://www.quickmeme.com'
        
        #Get the links to instance pages, store them in self.instance_page_hrefs
        for link in instance_page_hrefs:
            self.instance_page_hrefs.append(BaseURL + link)


        requests = []
        #Get link to the next page of this meme-type
        for link in next_page_hrefs:
            next_page_href = BaseURL + link
            requests.append (Request (next_page_href, callback=self.parse))
            print next_page_href

        #case - still more meme-type pages to go through.
        # return a request object for the next page
        if len(requests) > 0:
            return requests

        #case - no more meme-type pages left
        # return a list of requests for the meme instance pages from links stored in self.instance_page_hrefs
        else:
            self.print_status("Finished scanning meme-type pages")
            for href in self.instance_page_hrefs:
                print href
                requests.append (Request (href, callback=self.parse_instance_page))
            self.print_status("Beginning to scan meme-instance pages")
            return requests




    def parse_instance_page (self, response):
        self.print_status("Scanning meme instance page")
        
        return
                


    









