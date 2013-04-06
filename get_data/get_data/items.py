# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class GetDataItem(Item):
    
	#meme type - SAP, sudden clarity clarence, etc
	meme_type = Field ()
	
	#the top and bottom lines of text  from the meme
	top_line = Field ()
	bottom_line = Field ()
	
	
	
    pass
