# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from scrapy.loader import ItemLoader
from ArticleSpider.items import Aitem
class DoubanbookSpider(scrapy.Spider):
    name = 'xiaozu'
   # allowed_domains = ['http://gl.xiaozhu.com/']
    start_urls = ['http://gl.xiaozhu.com/']

    def parse(self, response):
        post_nodes = response.css(".resule_img_a::attr(href)").extract()
        for post_url in post_nodes:
            yield Request(url=parse.urljoin(response.url, post_url),callback=self.parse_detail)

        next_url = response.css(".font_st::attr(href)").extract()[-1]
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

        pass


    def parse_detail(self, response):
        # title=response.css('.pho_info h4 em::text').extract_first("")
        # money=response.css('.day_l span::text').extract_first("")
        # print('***'*3,response,'***'*3)
        # for i,j in zip(title,money):
        #     print(i,' : ',j,'元')
        # if title:
        #     print(title,money)

        item_loader = ItemLoader(item=Aitem(), response=response)
        item_loader.add_css("title", ".pho_info h4 em::text")
        item_loader.add_css("money", ".day_l span::text")
        item_loader.add_value("url", response.url)
#        print(item_loader.item["title"])
        xiaozitem = item_loader.load_item()
        yield xiaozitem
