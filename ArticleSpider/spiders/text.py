# -*- coding: utf-8 -*-
import base64
import hashlib
import hmac
from http import cookiejar
from io import BytesIO

import execjs
import scrapy
import json
import datetime
import requests
from PIL import Image

session = requests.session()
session.cookies = cookiejar.LWPCookieJar(filename='./cookies.txt')
try:
    import cookielib
except:
    import http.cookiejar as cookielib

class TextSpider(scrapy.Spider):
    name = 'text'
    # allowed_domains = ['www,zhihu,com']
    start_urls = ['https://www.zhihu.com/signin?next=%2F']

    login_url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
    captcha_url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'

    login_data = {
        'grant_type': 'password',  # 登录方式
        'source': 'com.zhihu.web',
        'username': '18894899674',
        'password': '666666666.',
        'captcha': '',  # 验证码
        'timestamp': '',
        'client_id':'c3cef7c66a1843f8b3a9e6a1e3160e20'
        # lang    cn

    }
    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhizhu.com",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
        'x-xsrftoken': '24f6yC6wyCU8LE0qnJy4xsSu94QLoo2t',
        'content-type': 'application/x-www-form-urlencoded',
        'x-zse-83': '3_2.0'
    }

    def __init__(self):
        self.session = requests.session()
        with open('C:/Users/23607/Desktop/py/ArticleSpider/ArticleSpider/spiders/get_formdata1.js', 'r', encoding='utf-8') as f:
            self.encry_js = f.read()

    def parse(self, response):
        pass

    def start_requests(self):
        yield scrapy.Request(url=self.captcha_url, headers=self.headers,callback=self.parse_get_captcha)

    def parse_get_captcha(self, response):
        print(response.text)
        is_captcha = json.loads(response.text).get("show_captcha")
        if is_captcha:
            print('有验证码!')
            yield scrapy.Request(url=self.captcha_url, method='PUT',headers=self.headers, callback=self.parse_image_url)

    def parse_image_url(self, response):
        print(response.text)
        img_url = json.loads(response.text).get("img_base64")
        # 对加密图片进行解密，获取原始地址
        img_data = base64.b64decode(img_url)
        # 根据得到的Bytes-like对象，创建一个字节码对象(bytes对象)
        img_real_url = BytesIO(img_data)
        # 利用Image去请求这个图片，获得图片对象
        img = Image.open(img_real_url)
        img.save('captcha.png')
        try:
            im = Image.open('captcha.png')
            im.show()
            im.close()
        except:
            print('没有图啊！')
        self.in_c=input('输入验证码或者数字')
        yield scrapy.FormRequest(
            url=self.captcha_url,
            callback=self.parse_post_captcha,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',},
            formdata={
                'input_text': self.in_c
            }
        )
    def parse_post_captcha(self,response):
        result = json.loads(response.text).get("success", '')
        print(response.text)
        if result:
            print('验证码输入正确')
            import time
            timestamp=str(int(time.time())*1000)
            post_data = {
                'timestamp': timestamp,
                'ref_source': 'homepage',
                'lang': 'en',
                'captcha': self.in_c,
                'signature': self._get_signature(timestamp),
            }
            self.login_data.update(post_data)

            print(self.login_data)

            encry= self.get_form_data(self.login_data['timestamp'], self.login_data['signature'], self.login_data['captcha'])
            print(encry)

            url = 'https://www.zhihu.com/api/v3/oauth/sign_in'

            self.session.post(url, headers=self.headers, data=encry)
            r = self.session.get('https://www.zhihu.com/notifications', headers=self.headers)
            print(r.text)

            if self.login_data['username'] in r.text:
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

            # yield scrapy.FormRequest(
            #     url=self.login_url,
            #     # formdata=self.login_data,
            #     # data=encry,
            #     formdata={encry},
            #     headers=self.headers,
            #     callback=self.parse_login
            # )

    def parse_login(self,response):

        return [scrapy.FormRequest(
            url=self.login_url,
            # formdata=self.login_data,
            headers=self.headers,
            callback=self.isLogin
        )]

    def check_login(self):
        resp = self.session.get(self.login_url, allow_redirects=False)
        if resp.status_code == 302:
            print('登录成功!!!!!!!!!')
            self.session.cookies.save()
            return True
        return False

    def isLogin(self):  # 通过查看用户个人信息来判断是否已经登录
        if self.check_login:
            url = "https://www.zhihu.com/settings/profile"
            login_code = session.get(url, headers=self.headers, allow_redirects=False).status_code
            if login_code == 200:
                print('成功!!!!!!!!!')
            else:
                print('失败!!!!!!!!!')

    def _get_signature(self,timestamp):

        ha = hmac.new(b'd1b964811afb40118a12068ff74a12f4', digestmod=hashlib.sha1)
        grant_type = self.login_data['grant_type']
        client_id = self.login_data['client_id']
        source = self.login_data['source']
        ha.update(bytes((grant_type + client_id + source + timestamp), 'utf-8'))
        return ha.hexdigest()

    def get_form_data(self, timestamp,signature, captcha):
        text1 = "client_id=c3cef7c66a1843f8b3a9e6a1e3160e20&grant_type=password&timestamp={0}&" \
               "source=com.zhihu.web&signature={1}&username=%2B86{2}&password={3}&" \
               "captcha={4}&lang=ene&utm_source=&ref_source=other_https%3A%2F%2Fwww.zhihu.com%2Fsignin%3Fnext%3D%252F".format(timestamp, signature, self.login_data['username'],
                                                                            self.login_data['password'], captcha)
        text='client_id=c3cef7c66a1843f8b3a9e6a1e3160e20&grant_type=password&timestamp={0}&source=com.zhihu.web&signature={1}&username=%2B86{2}&password={3}&captcha=%20{3}&lang=en&utm_source=&ref_source=other_https%3A%2F%2Fwww.zhihu.com%2Fsignin%3Fnext%3D%252F'.format(timestamp, signature, self.login_data['username'],
                                                                            self.login_data['password'], captcha)
        print(text)
        ctx = execjs.compile(self.encry_js)
        encry = ctx.call('b',text)
        return encry

        # with open('./encrypt.js') as f:
        #     js = execjs.compile(f.read())
        #     return js.call('Q', urlencode(form_data))