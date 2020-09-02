import random

import requests
from scrapy.selector import Selector
import pymssql

conn=pymssql.connect("192.168.174.1","system_dbm","123456", "my_spider")
cursor = conn.cursor() # 获取光标
# cursor.execute(
#             """IF OBJECT_ID('ip_proxy','U')IS NOT NULL
#             DROP TABLE ip_proxy
#             CREATE TABLE ip_proxy
#                 ( ip VARCHAR(20) NOT NULL,
#                   port VARCHAR(20) NOT NULL,
#                   speed float,
#                   ip_type VARCHAR(10),
#                 )  """)
def crawl_ips():
    #爬取西刺的免费ip代理
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362"}

    for i in range(10):
        import time
        time.sleep(1)
        print(i,'运行中...')
        re = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers=headers,)

        selector = Selector(text=re.text)
        all_trs = selector.css("#ip_list tr")


        ip_list = []
        for tr in all_trs[1:]:
            speed_str = tr.css(".bar::attr(title)").extract()[0]
            if speed_str:
                speed = float(speed_str.split("秒")[0])
            all_texts = tr.css("td::text").extract()

            ip = all_texts[0]
            port = all_texts[1]
            proxy_type = all_texts[5]

            ip_list.append((ip, port, proxy_type, speed))

        for ip_info in ip_list:
            cursor.execute(
                "insert into ip_proxy(ip, port, speed, ip_type) VALUES('{0}', '{1}', {2}, 'HTTP')".format(
                    ip_info[0], ip_info[1], ip_info[3]
                )
            )

            conn.commit()


class GetIP(object):
    def delete_ip(self, ip):
        #从数据库中删除无效的ip
        delete_sql = """
            delete from [my_spider].[dbo].[ip_proxy] where ip='{0}'
        """.format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def judge_ip(self, ip, port):
        #判断ip是否可用
        http_url = "http://www.baidu.com"
        proxy_url = "http://{0}:{1}".format(ip, port)
        try:
            proxy_dict = {
                "http":proxy_url,
            }
            response = requests.get(http_url, proxies=proxy_dict)
        except Exception as e:
            print ("错误错误！invalid ip and port",ip)
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 300:
                print ("有用!effective ip")
                return True
            else:
                print  ("假的假的！invalid ip and port",ip)
                self.delete_ip(ip)
                return False


    def get_random_ip(self):
        #从数据库中随机获取一个可用的ip
        random_sql = """
             SELECT TOP 1 [ip]
		                ,[port]
             FROM [my_spider].[dbo].[ip_proxy]
             ORDER BY newid()
            """
        result = cursor.execute(random_sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]

            judge_re = self.judge_ip(ip, port)
            if judge_re:
                print("***************http://{0}:{1}".format(ip, port),'**************')
                return "http://{0}:{1}".format(ip, port)
            else:
                return self.get_random_ip()
if 1:
    a=GetIP()
    print(a.get_random_ip())

# crawl_ips()


# for i in range(10):
#     print(random_ip[random.randint(0,4)])
# random_ip.pop()
#
# randomip= random.choice(random_ip)
# print(randomip)