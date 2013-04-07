#spider for crawling quickmeme
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from selenium import selenium
import time
import csv

# Class: QkmeSpider
# -----------------
# spider to crawl through quickmeme and scrape text from advice animals.
# currently only scrapes meme types that are hard-coded in.
class QkmeSpider (BaseSpider):
    name = "qkme"
    allowed_domains = ["quickmeme.com"]
    start_urls = ["http://www.quickmeme.com/Socially-Awkward-Penguin/"]
    
    def __init__ (self, meme_name="Socially-Awkward-Penguin"):

        #list to contain the absolute links to each instance page
        self.instance_page_urls = []
        self.baseURL = 'http://www.quickmeme.com'
        self.selenium = selenium("localhost", 4444, "*chrome", "http://www.quickmeme.com")
        self.selenium.start ()
        
        self.start_urls[0] = "http://www.quickmeme.com/" + meme_name + "/"
        
        self.datafile_name = meme_name + " data.txt"
        self.datafile = open(self.datafile_name, 'w')
        
        pass
    
    
    def print_status (self, status_string, level=0):
        print "     "*level,
        print "##### Status: " + status_string + "#####"
    
    # Function: parse
    # ---------------
    # this function will parse a hard-coded meme-type's page and extract
    # links to each individual meme instance's page.
    def parse (self, response):
        self.print_status("Scanning meme-type page")
        
        hxs = HtmlXPathSelector(response)
        
        #xpath expression to extract the links to each meme instance page
        instance_page_urls_xpath = '//div[@class="memeThumb"]/a/@href'
        
        #xpath for the 'next page' url
        next_page_urls_xpath = '//a[@class="next"]/@href'
        
        instance_page_urls = hxs.select(instance_page_urls_xpath).extract ()
        next_page_urls = hxs.select (next_page_urls_xpath).extract ()

        
        #Get the links to instance pages, store them in self.instance_page_urls
        for link in instance_page_urls:
            self.instance_page_urls.append(self.baseURL + link)


        requests = []
        #Get link to the next page of this meme-type
        for link in next_page_urls:
            next_page_url = self.baseURL + link
            requests.append (Request (next_page_url, callback=self.parse))
            print next_page_url

        #case - still more meme-type pages to go through.
        # return a request object for the next page
        if len(requests) > 0:
            return requests

        #case - no more meme-type pages left
        # return a list of requests for the meme instance pages from links stored in self.instance_page_urls
        else:
            self.print_status("Finished scanning meme-type pages")
            for url in self.instance_page_urls:
                print url
                requests.append (Request (url, callback=self.parse_instance_page))
            self.print_status("Beginning to scan meme-instance pages")
            return requests




    # Function: parse_instance_page
    # -----------------------------
    # Function to parse the instance page - should extract a link to the 'add your own caption' page
    def parse_instance_page (self, response):
        self.print_status("Scanning meme instance page", 1)
        hxs = HtmlXPathSelector(response)
        
        #Url for "add your own caption" - the caption page
        add_caption_xpath = '//a[@id="editurl"]/@href'
        
        requests = []
        add_caption_url = hxs.select(add_caption_xpath).extract()
        for url in add_caption_url:
        
            sel = self.selenium
            sel.open(self.baseURL + url)
            time.sleep(2)
            
            meme_type_xpath = '//a[@id="meme_name"]/text()'
            top_text_xpath = '//textarea[@tabindex="1"]/text()'
            bottom_text_xpath = '//textarea[@tabindex="2"]/text()'
            
            meme_type = hxs.select(meme_type_xpath).extract ()[0]
            top_text = sel.get_text(top_text_xpath)
            bottom_text = sel.get_text(bottom_text_xpath)
            
            self.store_in_file (meme_type, top_text, bottom_text)

        

    # Function: write_to_file
    # -----------------------
    # will write a meme (top_text, bottom_text) to a file
    def store_in_file (self, meme_type, top_text, bottom_text):
        
        self.datafile.write("%s | %s | %s\n" % (meme_type, top_text, bottom_text) )
        
        
        pass









