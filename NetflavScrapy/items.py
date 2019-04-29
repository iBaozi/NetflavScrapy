# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DownloadVideoItem(scrapy.Item):
    file_urls = scrapy.Field()
    file_name = scrapy.Field()
    files = scrapy.Field()
