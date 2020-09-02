# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader.processors import MapCompose, TakeFirst, Join


def get_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums


def getfirst(value):
    return value[0].strip()


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Aitem(scrapy.Item):
    title = scrapy.Field()
    money = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    url = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = "INSERT INTO xiaozhu VALUES (%s, %s, %s)"
        title = self['title'][0].strip()
        url = self['url'][0].strip()
        params = (title, self['money'], url)
        return insert_sql, params


class Bitem(scrapy.Item):
    title = scrapy.Field(
        # input_processor=MapCompose(getfirst)
        output_processor=Join("-")
    )
    money = scrapy.Field(

        # input_processor=MapCompose(getfirst)
        # output_processor=Join(" ")
    )
    condition = scrapy.Field(
        # input_processor=MapCompose(getfirst),
        output_processor = Join("   ")
    )
