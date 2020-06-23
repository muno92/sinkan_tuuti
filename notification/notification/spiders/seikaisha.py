import scrapy
from bs4 import BeautifulSoup

from notification.items import Book


class SeikaishaSpider(scrapy.Spider):
    name = 'seikaisha'
    allowed_domains = ['www.seikaisha.co.jp']
    start_urls = ['https://www.seikaisha.co.jp/#publication']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')

        for section in soup.select('#publication > section'):
            book = Book()
            book['isbn'] = section \
                .select_one('.publication-meta > dd:nth-of-type(3)') \
                .text.replace('-', '')
            book['title'] = section.select_one('.entry-title a').text
            book['author'] = section \
                .select_one('.publication-meta > dd:nth-of-type(1)') \
                .text

            book['publishing_date'] = \
                section.select_one('.release-date .year').text \
                    .replace('年', '-') \
                + section.select_one('.release-date .month').text \
                    .replace('月', '-') \
                + section.select_one('.release-date .day').text \
                    .replace('日', '')

            yield book
