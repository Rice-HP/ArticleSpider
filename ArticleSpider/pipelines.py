# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sys
import io
import json
import pymssql

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030') # 改变标准输出的默认编码

class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item

class WritePipeline(object):
    def __init__(self):
        self.file=open('C:\\Users\\23607\\Desktop\\lagoupython.txt', 'w')

    def process_item(self, item, spider):

        try:
            print(item['title'], item['money'], item['condition'])
            text = "◆         职位名称 : " + item['title'].strip() +'\t￥ '+item['money'][0] +'\n◇'+item['condition'] +'\n\n'
            self.file.write(text.replace(u'\xa0', u' '))
            # self.file.write("    职位名称 : " + item['title'].strip().replace(u'\xa0', u' '))
            # self.file.write('\t￥ '+item['money'][0].replace(u'\xa0', u' '))
            # self.file.write('\n'+item['condition'].replace(u'\xa0', u' ')+'\n\n')
        except:
            print('文件写入错误（编码错误）！')
        #self.file.write(json.dumps(dict(item), ensure_ascii=False))
        return item

    def close_spider(self, spider):
        self.file.close()

class MssqlPipeline(object):
    server = "192.168.174.1"  # 连接服务器地址
    user = "system_dbm"            # 连接帐号
    password = "123456"        # 连接密码

    def __init__(self):
        self.conn=pymssql.connect(MssqlPipeline.server,MssqlPipeline.user, MssqlPipeline.password, "my_spider")
        self.cursor = self.conn.cursor() # 获取光标
        self.cursor.execute(
            """IF OBJECT_ID('xiaozhu','U')IS NOT NULL 
            DROP TABLE xiaozhu 
            CREATE TABLE xiaozhu 
                ( title VARCHAR(max) NOT NULL, 
                  money INT NOT NULL,
                  Url VARCHAR(max),
                )  """)

    def process_item(self, item, spider):

#        self.cursor.execute("INSERT INTO xiaozhu VALUES (%s, %s, %s)",(item['title'][0],item['money'][0],item['url'][0]))
        insert_sql, params = item.get_insert_sql()
        print (insert_sql, params)
        self.cursor.execute(insert_sql, params)
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.conn.close()