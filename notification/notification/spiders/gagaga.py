import datetime
import re

import scrapy
from bs4 import BeautifulSoup

from notification.items import Book


class GagagaSpider(scrapy.Spider):
    name = 'gagaga'
    allowed_domains = ['gagagabunko.jp']
    start_urls = ['https://gagagabunko.jp/release/index.html']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        books = []

        isbn_pattern = re.compile(r'\d[\d\-]+\d')
        author_pattern = re.compile(r'著：(.+)　イラスト')
        publishing_date = str(datetime.date.today().year) + '年' + \
                          re.search(
                              r'\d{1,2}月\d{1,2}日',
                              soup.select_one(
                                  '#contBg .headingReleasedate').text
                          ).group()

        for section in soup.select('#contBg > section'):
            title_text = section.select_one('#title').text
            book = Book()
            book['isbn'] = re.search(isbn_pattern, title_text) \
                .group().replace('-', '')
            book['title'] = section.select_one('h3').text
            book['author'] = re.search(author_pattern, title_text).group(1)
            book['publishing_date'] = publishing_date

            books.append(book)
        print(books)
