# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import random

import scrapy
from scrapy.pipelines.files import FilesPipeline

from NetflavScrapy.items import DownloadVideoItem
from NetflavScrapy.util.user_agent_custom import x_forwarded_for


class DownloadVideoPipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        if isinstance(item, DownloadVideoItem):
            info.spider.logger.warn('接到下载任务，文件名：{0}\n地址：{1}\n'.format(item['file_name'] + '.mp4', item['file_urls']))
            customer_headers = {
                'User-Agent': random.choice(info.spider.settings.get('USER_AGENT')),
                'X-Forwarded-For': x_forwarded_for()
            }
            return scrapy.Request(url=item['file_urls'], meta=item, headers=customer_headers)

    def file_path(self, request, response=None, info=None):
        down_name = request.meta['file_name'] + '.mp4'
        return down_name
