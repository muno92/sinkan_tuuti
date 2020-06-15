# -*- coding: utf-8 -*-

from os import environ

from scrapy.exceptions import DropItem


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class SearchPipeline(object):
    def process_item(self, item, spider):
        author_search_keywords = environ.get("AUTHOR_SEARCH_KEYWORDS", "") \
            .split()

        for author_search_keyword in author_search_keywords:
            if author_search_keyword in item['author']:
                return item
        raise DropItem('Not Match Author')
