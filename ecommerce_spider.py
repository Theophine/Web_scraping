# -*- coding: utf-8 -*-
import scrapy
from ..items import BookStoreItem

class BookSpiderSpider(scrapy.Spider):
    name = 'books_spider'
    #allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']
    
    custom_settings = {
        'FEED_URI': 'pagination_doc/books.csv', 
        'FEED_FORMAT': 'csv'
    }
    
    page_two = 2
    

    #function for spider to enter website and scrape from home page
    def parse(self, response):
        container = response.xpath("//div/ol[@class='row']//article[contains(@class,'product_pod')]")
        
        
        for row in container: 
            link = row.xpath(".//div[@class='image_container']/a/@href").extract_first()
            
            new_url = response.urljoin(link)
            
            
            yield scrapy.Request(url = new_url, callback = self.parse_info)
            
            
        #code to scrape from page 2    
        next_link = 'http://books.toscrape.com/catalogue/page-' + str(BookSpiderSpider.page_two) + '.html'
        
        yield scrapy.Request(url = next_link, callback = self.next_page)
            
            
            
    #code to scrape from pages 2 upwards
    def next_page(self, response):
        container = response.xpath("//div/ol[@class='row']//article[contains(@class,'product_pod')]")
        
        
        for row in container: 
            link = row.xpath(".//div[@class='image_container']/a/@href").extract_first()
            
            new_url = 'http://books.toscrape.com/catalogue/' + link
            
            
            yield scrapy.Request(url = new_url, callback = self.parse_info)
            
            
        #code for pagination from page 3
        next_link = response.css(' li.next > a::attr(href)').extract_first()
        
        while next_link is not None:

            new_url = 'http://books.toscrape.com/catalogue/' + next_link

            yield scrapy.Request(url = new_url, callback = self.next_page)
        
        
        
    
    #function for spider to follow link from each article and scrape from within 
    def parse_info(self, response):
        item = BookStoreItem()
        
        title = response.xpath("//article[@class='product_page']//div[@class = 'col-sm-6 product_main']/h1/text()").extract()
        img_url = response.xpath("//article[@class='product_page']//div[@class='item active']/img/@src").extract_first().replace('../../', '')
        price = response.xpath("//article[@class='product_page']//div[@class = 'col-sm-6 product_main']/p[@class='price_color']/text()").extract()
        availability = response.xpath("//article[@class='product_page']//div[@class = 'col-sm-6 product_main']/p[@class='instock availability']/text()")[1].extract().split('\n')[2]
        rating = response.css(" div p.star-rating::attr(class)").extract()[0].split(' ')[1]
        product_description = response.css(" article.product_page div#product_description + p::text").extract()
        UPC = response.xpath("//article[@class='product_page']//table[@class='table table-striped']//tr[1]/td/text()").extract_first()
        price_excl_tax = response.xpath("//article[@class='product_page']//table[@class='table table-striped']//tr[3]/td/text()").extract_first()
        price_incl_tax = response.xpath("//article[@class='product_page']//table[@class='table table-striped']//tr[4]/td/text()").extract_first()
        tax = response.xpath("//article[@class='product_page']//table[@class='table table-striped']//tr[5]/td/text()").extract_first()
    
    
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
        
        
       