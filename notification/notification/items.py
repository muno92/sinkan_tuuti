# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Book(scrapy.Item):
    isbn = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    publishing_date = scrapy.Field()
