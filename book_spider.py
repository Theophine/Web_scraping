# -*- coding: utf-8 -*-
import scrapy
from ..items import BooksItem

class BookSpiderSpider(scrapy.Spider):
    name = 'book_spider'
    #allowed_domains = ['http://books.toscrape.com/']
    start_urls = ['http://books.toscrape.com/']
    
    page_two = 2 
    next_page = 3
    catalogue = 'catalogue/'
    
    
    custom_settings = {
        'FEED_URI': 'scraped_books_link/books.csv', 
        'FEED_FORMAT': 'csv'
    }
    
    
    #NOTE: The major aim of this project is to follow the book url link and scrape all the items within
    def parse(self, response):
        
        all_books = response.css(' div.row li > article.product_pod') 
        
        for book in all_books: 
          
            book_url = self.start_urls[0] + book.css(' h3 > a::attr(href)').extract_first()
            
            
            yield response.follow(url = book_url, callback = self.parse_content)
        
        
        
        #Code to go to page 2.
        
        link = 'http://books.toscrape.com/catalogue/page-' + str(BookSpiderSpider.page_two) + '.html'
        
        yield response.follow(url = link, callback = self.parse_other_pages)
            
    
    
    def parse_other_pages(self, response):
        
        all_books = response.css(' div.row li > article.product_pod') 
        
        for book in all_books: 
          
            book_url = self.start_urls[0] +  self.catalogue  + book.css(' h3 > a::attr(href)').extract_first()
            
            
            yield response.follow(url = book_url, callback = self.parse_content)
    
       
        
        
        #Code to go to the next pages from page 2 using pagination and extract from those pages.
        
        next_page = 'http://books.toscrape.com/catalogue/page-' + str(BookSpiderSpider.next_page) + '.html'
        
        if BookSpiderSpider.next_page < 51:
            
            BookSpiderSpider.next_page += 1
            
            yield response.follow(url = next_page, callback = self.parse_other_pages)
        
    
    
    def parse_content(self, response): 
        item = BooksItem()
        
        title = response.css(' div.product_main > h1::text').extract_first()
        img_url = response.url + response.css(' div#product_gallery img::attr(src)').extract_first().replace('../../', '/')
        price = response.css(' div.product_main > p.price_color::text').extract_first()
        availability = response.css(' div.product_main p.instock::text').extract()[1].replace('\n', ' ').strip(' ')
        rating = response.css(' p.star-rating::attr(class)').extract_first().split(' ')[1]
        product_description = response.css(' article.product_page div#product_description + p::text').extract_first()
        UPC = response.css(' table.table tr > td::text').extract_first()
        price_excl_tax = response.css(' table.table tr > td::text').extract()[2]
        price_incl_tax = response.css(' table.table tr > td::text').extract()[3]
        tax = response.css(' table.table tr > td::text').extract()[4]
        
        
        item['title'] = title
        item['img_url'] = img_url
        item['price'] = price
        item['availability'] = availability
        item['rating'] = rating
        item['product_description'] = product_description
        item['UPC'] = UPC
        item['price_excl_tax'] = price_excl_tax
        item['price_incl_tax'] = price_incl_tax
        item['tax'] = tax
        
        
        yield item
        
        
      