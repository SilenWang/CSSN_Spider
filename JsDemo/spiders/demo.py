import scrapy
import json
# from scrapy.http import Request, FormRequest
# from scrapy.selector import Selector
# from scrapy_splash.request import SplashRequest, SplashFormRequest
from JsDemo.items import JsdemoItem
from math import ceil

# script = """
#         function main(splash, args)
#           assert(splash:go(args.url))
#           assert(splash:wait(3))
#           return splash:html()
#         end
#          """

class DemoSpider(scrapy.Spider):
    name = 'demo'
    allowed_domains = ['www.cssn.net.cn']
#     base_url = 'http://www.cssn.net.cn:8000/standards/?a104=IX-ISO&orderby=-a101&page={pNum}'
#     start_url = 'http://www.cssn.net.cn:8000/standards/?a104=IX-ISO&orderby=&page={pNum}&post_publicyear={year}'
    start_urls = [f'http://www.cssn.net.cn:8000/standards/?a104=IX-ISO&orderby=&post_publicyear={year}' for year in range(1960, 2021)]

    
    def parse(self, response):
        pMax = ceil(json.loads(response.text)['count'] / 20)
        for pNum in range(1, pMax+1):
            yield scrapy.Request(f'{response.request.url}&page={pNum}', callback=self.parse_next)        
           
    
    def parse_next(self, response):
        obj = json.loads(response.text)
        item = JsdemoItem()
        item['raw'] = obj['results']
        yield item
