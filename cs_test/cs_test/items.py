# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CsTestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ArticleItem(scrapy.item):
    title_name = scrapy.Field()
    creat_time = scrapy.Field()
    author = scrapy.Field()
    target = scrapy.Field()
    read_num = scrapy.Field()
    raise_num = scrapy.Field()
    comment_num =scrapy.Field()
    burry_num = scrapy.Field()
    from_image_url =scrapy.Field()
