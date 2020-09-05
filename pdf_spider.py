# -*- coding: utf-8 -*-
import scrapy
from ..items import PdfFilesItem
from scrapy.loader import ItemLoader

class PdfSpiderSpider(scrapy.Spider):
    name = 'pdf_spider'
    allowed_domains = ['www.bitsavers.org']
    start_urls = ['http://www.bitsavers.org/pdf/sony/floppy/']

    def parse(self, response):
        
        #define the container of the elements 
        container = response.xpath("//following::tr[3]/td[1]/a[contains(@href,'.pdf')]")
        
        for row in container: 
            
            #instantiate the item loader 
            
            loader = ItemLoader(item = PdfFilesItem(), selector = row)
            
            relative_url = row.xpath('.//@href').extract_first()
            
            pdf_url = response.urljoin(relative_url)
            
            #pdf_name = row.xpath('.//text()').extract_first()
            
            
            loader.add_value('file_urls', pdf_url)
            loader.add_xpath('pdf_name', './/text()')
            
            yield loader.load_item()
            
