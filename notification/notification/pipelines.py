# -*- coding: utf-8 -*-

import textwrap
import traceback
from os import environ

import psycopg2
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


class DbPipeline(object):
    def process_item(self, item, spider):
        try:
            if self.is_notified(item):
                raise DropItem(f'{item["title"]} is notified.')
            self.save_notification_log(item)
            return item
        except Exception:
            webhook_url = environ.get('SINKAN_TUUTI_SLACK_URL')
            if webhook_url:
                message = 'title: ' + item["title"] + '\n'
                message += traceback.format_exc()

                slack = slackweb.Slack(webhook_url)
                slack.notify(text=message)
            raise DropItem('DB Error.')

    def get_connection(self):
        return psycopg2.connect(
            host=environ.get('DB_HOST'),
            port=int(environ.get('DB_PORT')),
            user=environ.get('DB_NAME'),
            password=environ.get('DB_USER'),
            database=environ.get('DB_PASSWORD'),
            sslmode='require'
        )

    def is_notified(self, item):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                sql = 'SELECT COUNT(*) FROM notification_logs WHERE isbn = %s'
                cur.execute(sql, (item['isbn'],))
                (count,) = cur.fetchone()

                return count == 1

    def save_notification_log(self, item):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                sql = '''
                INSERT INTO notification_logs
                    (isbn, author, title, publishing_date)
                    VALUES (%s, %s, %s, %s)
                '''

                cur.execute(sql, (
                    item['isbn'],
                    item['author'],
                    item['title'],
                    item['publishing_date']
                ))

                conn.commit()


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
