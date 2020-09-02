# -*- coding: utf-8 -*-
import requests
from scrapy.signalmanager import SignalManager
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals, crawler
from requests import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ArticleSpider.items import Bitem
from scrapy.loader import ItemLoader
from selenium import webdriver

class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/zhaopin/Python/?labelWords=label']

    # custom_settings = {"COOKIES_ENABLED": True, "DOWNLOAD_DELAY": 1,
    #                    'DEFAULT_REQUEST_HEADERS':
    #                        {'Accept': 'application/json, text/javascript, */*; q=0.01',
    #                         'Accept-Encoding': 'gzip, deflate, br',
    #                         'Accept-Language': 'zh-CN,zh;q=0.8', 'Connection': 'keep-alive',
    #                         'Cookie': 'JSESSIONID=ABAAABAABEEAAJAC2B50C10272B86D263D9811FA6F7F7A0; WEBTJ-ID=20190815135324-16c93d682ef316-03642fcecf1b0a-71415a3b-1713590-16c93d682f06a6; TG-TRACK-CODE=index_navigation; X_HTTP_TOKEN=f272c47386e539af90484856510a4f8e187c609bef; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1565766176,1565766201,1565785531,1565847076; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1565848409; _ga=GA1.2.242066954.1565848405; _gid=GA1.2.1744484875.1565848405; _gat=1; user_trace_token=20190815135325-ff311f35-bf20-11e9-89f4-525400f775ce; LGSID=20190815135325-ff31210c-bf20-11e9-89f4-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGRID=20190815135329-019e5bb0-bf21-11e9-89f4-525400f775ce; LGUID=20190815135325-ff312428-bf20-11e9-89f4-525400f775ce; index_location_city=%E5%B9%BF%E5%B7%9E',
    #                         'Host': 'www.lagou.com', 'Origin': 'https://www.lagou.com',
    #                         'Referer': 'https://www.lagou.com/',
    #                         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    #                         }
    #                    }

    rules = (
        # Rule(LinkExtractor(allow=('.*/zhaopin/Python/.*',), ),follow=True),
        # Rule(LinkExtractor(allow=('.*www.lagou.com/jobs/d+.*',)), callback='parse_job',follow=True),
        # Rule(LinkExtractor(allow=('.*www.lagou.com/utrack/trackMid.*Fjobs.*',)), callback='parse_job', follow=True),
        # Rule(LinkExtractor(allow=('.*www.lagou.com%2Fjobs.*',)), callback='parse_job', follow=True),
        # Rule(LinkExtractor(allow=('.*www.lagou.com%2Fzhaopin.*',)),  callback='parse_list', follow=True),
        Rule(LinkExtractor(allow=("zhaopin/Python/.*",)), follow=True),
        # Rule(LinkExtractor(allow=("gongsi/j\d+.html",)), follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),
        # Rule(LinkExtractor(allow=('.*www.lagou.com%2Fjobs.*',)), callback='parse_job', follow=True),
        # Rule(LinkExtractor(allow=('.*www.lagou.com%2Fzhaopin.*',)),  callback='parse_list', follow=True),

    )

    def __init__(self):
        self.browser = webdriver.Chrome(executable_path='C:\\Users\\23607\\Desktop\\py\\chromedriver.exe')
        super(LagouSpider,self).__init__()
        # dispatcher.connect(self.spider_closed(),signals.spider_closed)
        # crawler.signals.connect(self.spider_closed, signals.spider_closed)
        SignalManager(dispatcher.Any).connect(self.spider_closed, signal=signals.spider_closed)

    def spider_closed(self,spider):
        print('spider close!')
        self.browser.quit()

    def parse_job(self, response):
        self.session = requests.session()

        item_loader = ItemLoader(item=Bitem(), response=response)
        item_loader.add_css("title", ".name::text")
        item_loader.add_css("money", ".salary::text")
        item_loader.add_css("condition", ".job-detail p::text")

        job_detail = item_loader.load_item()
        if job_detail:
            yield job_detail
        else:
            print('值呢????')
            # r = self.session.get(response.url)
            # print(r.text)
            # yield Request(url=response.url, callback=self.parse_job)

    def parse_list(self, response):
        item_loader = ItemLoader(item=Bitem(), response=response)
        item_loader.add_xpath("title", "//*[@id='s_position_list']/ul/li[1]/div[1]/div[1]/div[1]/a/h3/text()")
        item_loader.add_css("money", "//*[@id='s_position_list']/ul/li[4]/div[1]/div[1]/div[2]/div/span/text()")
        item_loader.add_css("condition", "//*[@id='s_position_list']/ul/li[4]/div[1]/div[1]/div[2]/div/text()")

        job_list = item_loader.load_item()

        yield job_list