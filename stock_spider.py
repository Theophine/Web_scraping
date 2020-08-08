# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from ..items import StockChartItem


class StockSpiderSpider(scrapy.Spider):
    name = 'stock_spider'
    allowed_domains = ['www.barchart.com']
    #start_urls = ['https://www.barchart.com/stocks/quotes/$MMTH/overview/']
    
    custom_settings = {
        'FEED_URI': 'document/stock_file.csv', 
        'FEED_FORMAT': 'csv'
    }
    
    script = '''
    function main(splash, args)
  --[[Disable splash incognito mode]]--
  splash.private_mode_enabled = false
  
  --[[Set the user Agent]]--
  header = {
    ['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
  }
  splash:set_custom_headers(header)
  
  --[[Access the website]]--
  url = args.url
  assert(splash:go(url))
  assert(splash:wait(4))
    
  splash:set_viewport_full()
  return {
    splash:png(),
    splash:html()
  }
end
    '''

   
    def start_requests(self):
        yield SplashRequest(url = 'https://www.barchart.com/stocks/quotes/$MMTH/overview/', callback = self.parse, endpoint = 'execute', args = {'wait': 10, 'lua_source': self.script})
        
    
    def parse(self, response):
        
        item = StockChartItem()
        
        price_change = response.xpath("//div[contains(@class,'pricechangerow')]//span[contains(@class,'up')]/span[1]/text()").extract()
        percent_change = response.xpath("//div[contains(@class,'pricechangerow')]//span[contains(@class,'up')]//span[2][contains(@class,'last-change')]/span/text()").extract()
        day_high = response.xpath("//div[contains(@class,'bc-quote-row-chart')]//div[2][contains(@class,'small-6')]/div[3]/text()").extract()
        day_low = response.xpath("//div[contains(@class,'bc-quote-row-chart')]//div[1][contains(@class,'small-6')]/div[3]/text()").extract()
        
        
       
        item['price_change'] = price_change
        item['percent_change']= percent_change
        item['day_high'] = day_high 
        item['day_low'] = day_low
        
        
        yield item