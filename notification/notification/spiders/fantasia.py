import re

import scrapy
from bs4 import BeautifulSoup

from notification.items import Book


class FantasiaSpider(scrapy.Spider):
    name = 'fantasia'
    allowed_domains = ['fantasiabunko.jp']
    start_urls = ['http://fantasiabunko.jp/product/']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        books = []
        pattern = re.compile(r'\d{4}年\d{1,2}月\d{1,2}日')
        for li in soup.select('.booksSingleList > li'):
            book = Book()

            book['isbn'] = li["data-isbn"]
            book['title'] = li["data-title"]
            book['author'] = li.select_one('.author > li:first-child a').text
            book['publishing_date'] = pattern.search(
                li.select_one('.release').text
            ).group()

            books.append(book)
        print(books)
