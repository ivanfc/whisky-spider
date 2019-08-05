# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WhiskyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    attributes = scrapy.Field()
    description = scrapy.Field()
    amount = scrapy.Field()
    alcohol = scrapy.Field()
    price = scrapy.Field()
    dilivery = scrapy.Field()
    stock = scrapy.Field()
    company = scrapy.Field()
    image_src = scrapy.Field()
