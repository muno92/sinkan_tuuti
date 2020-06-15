# -*- coding: utf-8 -*-

import textwrap
from os import environ

import slackweb
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


class SlackPipeline(object):
    def process_item(self, item, spider):
        webhook_url = environ.get('SINKAN_TUUTI_SLACK_URL')
        if not webhook_url:
            raise DropItem('webhook url is not defined.')

        message = textwrap.dedent(f'''
        著者：{item['author']}
        タイトル：{item['title']}
        出版日：{item['publishing_date']}
        ''')

        slack = slackweb.Slack(webhook_url)
        slack.notify(text=message)
