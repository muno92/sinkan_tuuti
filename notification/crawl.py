from scrapy.crawler import CrawlerProcess

from notification.spiders.fantasia import FantasiaSpider
from notification.spiders.gagaga import GagagaSpider
from notification.spiders.seikaisha import SeikaishaSpider

process = CrawlerProcess()
process.crawl(FantasiaSpider)
process.crawl(GagagaSpider)
process.crawl(SeikaishaSpider)
process.start()
