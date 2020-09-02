# -*- coding: utf-8 -*-
import execjs
import scrapy
from scrapy.http import Request
import json
import base64
import hashlib
import hmac

try:
    import cookielib
except:
    import http.cookiejar as cookielib

import requests
session = requests.session()

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    # allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/signin?next=%2F']
    agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'

    login_url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhizhu.com",
        'User-Agent': agent
    }

    def __init__(self):
        self.session = requests.session()
        with open('C:/Users/23607/Desktop/py/ArticleSpider/ArticleSpider/spiders/get_formdata1.js', 'r', encoding='utf-8') as f:
            self.encry_js = f.read()

    def parse(self, response):
        pass

    def start_requests(self):

        return [scrapy.Request('https://www.zhihu.com/signin?next=%2F', headers=self.headers, callback=self.login)]
        # yield scrapy.Request(url=self.captcha_url, callback=self.parse_get_captcha)
        # return [scrapy.FormRequest(
        #
        # )]
    def login(self, response):
        import time
        self.t = str(int(time.time() * 1000))
        captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(self.t)
        yield scrapy.Request(captcha_url, headers=self.headers,callback=self.get_captcha)

    def get_captcha(self, response):
        with open("captcha.jpg", "wb") as f:
            f.write(response.body)
            f.close()

        from PIL import Image
        try:
            im = Image.open('captcha.jpg')
            im.show()
            im.close()
        except:
            print('错误！！！')
        captcha = input("输入验证码\n>")

        encry = self.get_form_data(self.t,self._get_signature(self.t),captcha)
        print(encry)

        url = 'https://www.zhihu.com/api/v3/oauth/sign_in'

        self.session.post(url, headers=self.headers, data=encry)
        r = self.session.get('https://www.zhihu.com/notifications', headers=self.headers)
        print(r.text)

        if '18894899674' in r.text:
            print('登陆成功')
        else:
            print('登陆失败')

        resp = self.session.get(self.login_url, allow_redirects=False)
        if resp.status_code == 302:
            print('登录成功!!!!!!!!!')
            self.session.cookies.save()

        url = "https://www.zhihu.com/settings/profile"
        login_code = session.get(url, headers=self.headers, allow_redirects=False).status_code
        if login_code == 200:
            print('成功!!!!!!!!!')
        else:
            print('失败!!!!!!!!!')



    def _get_signature(self,timestamp):

        ha = hmac.new(b'd1b964811afb40118a12068ff74a12f4', digestmod=hashlib.sha1)
        grant_type = 'password'
        client_id = 'c3cef7c66a1843f8b3a9e6a1e3160e20'
        source = 'com.zhihu.web'
        ha.update(bytes((grant_type + client_id + source + timestamp), 'utf-8'))
        return ha.hexdigest()

    def get_form_data(self, timestamp,signature, captcha):
        text = "client_id=c3cef7c66a1843f8b3a9e6a1e3160e20&grant_type=password&timestamp={0}&" \
               "source=com.zhihu.web&signature={1}&username=%2B86{2}&password={3}&" \
               "captcha={4}&lang=en&utm_source=&ref_source=other_https%3A%2F%2Fwww.zhihu.com%2Fsignin%3Fnext%3D%252F".format(timestamp, signature, '18894899674',
                                                                            '18894899674.', captcha)
        print(text)
        ctx = execjs.compile(self.encry_js)
        encry = ctx.call('b',text)
        return encry