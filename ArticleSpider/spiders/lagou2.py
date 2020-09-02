# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from scrapy.loader import ItemLoader
from ArticleSpider.items import Bitem
from selenium import webdriver
from scrapy.signalmanager import SignalManager
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

class Lagou2Spider(scrapy.Spider):
    name = 'lagou2'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/zhaopin/Python/?labelWords=label']

    def __init__(self):
        self.browser = webdriver.Chrome(executable_path='C:\\Users\\23607\\Desktop\\py\\chromedriver.exe')
        super(Lagou2Spider,self).__init__()
        SignalManager(dispatcher.Any).connect(self.spider_closed, signal=signals.spider_closed)

    def spider_closed(self,spider):
        print('spider close!')
        self.browser.quit()

    def parse(self, response):
        post_nodes = response.css(".position_link::attr(href)").extract()
        post_nodes.pop()   #去掉最后一个元素
        for post_url in post_nodes[0:6]:
            yield Request(url=parse.urljoin(response.url, post_url),callback=self.parse_detail)

        # next_url = response.css(".page_no::attr(href)").extract()[-1]
        # if next_url:
        #     yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)
        pass

    def parse_detail(self, response):

        item_loader = ItemLoader(item=Bitem(), response=response)
        item_loader.add_css("title", ".name::text")
        item_loader.add_css("money", ".salary::text")
        item_loader.add_css("condition", ".job-detail ::text")

        job_detail = item_loader.load_item()

        yield job_detail
