# -*- coding: utf-8 -*-
import scrapy
from ..items import BookImagesItem
from scrapy.loader import ItemLoader 

class BookImageSpiderSpider(scrapy.Spider):
    name = 'book_image_spider'
   # allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']
    
    page_number = 2

    def parse(self, response):
        
        container = response.xpath("//section//li/article[contains(@class, 'product_pod')]")
        
        for row in container:
            #instantiate the item loadder 
            
            loader = ItemLoader(item = BookImagesItem(), selector = row)
            
            relative_url = row.xpath('.//img/@src').extract_first()
            
            image_url = response.urljoin(relative_url)
            
            
            #time to load the image_url and the book name 
            
            loader.add_value('image_urls', image_url)
            loader.add_xpath('book_name', './/img/@alt')
            
            yield loader.load_item()
            
    
        #write a code for pagination to scrape from every page 
        next_url = 'http://books.toscrape.com/catalogue/page-' + str(self.page_number) + '.html'

        if self.page_number <= 50:
            self.page_number += 1

            yield scrapy.Request(url =  next_url,  callback = self.parse)
            

       