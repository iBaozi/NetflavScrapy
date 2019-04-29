import scrapy
import json
from scrapy.http.response.html import HtmlResponse

from NetflavScrapy.items import DownloadVideoItem


class StartSpider(scrapy.Spider):
    name = 'All'

    def start_requests(self):
        start_url = 'https://api.netflav.com/video/getVideo'
        yield scrapy.Request(start_url)

    def parse(self, response: HtmlResponse):
        json_resp = json.loads(response.text)
        current_page = json_resp['result']['page']
        max_pages = json_resp['result']['pages']

        if current_page < max_pages:
            next_url_suffix = '?page={0}'.format(current_page + 1)
            next_url = response.urljoin(next_url_suffix)
            self.logger.warn('next url:{0}'.format(next_url))
            yield scrapy.Request(next_url)

        video_info_list = json_resp['result']['docs']
        self.logger.warn('第{0}页，有{1}视频'.format(current_page, len(video_info_list)))
        for info in video_info_list:
            title = info['title']
            video_id = info['videoId']
            splice_url = 'https://www.netflav.com/video?id={0}'.format(video_id)
            addition_meta = {'name': title}
            yield scrapy.Request(url=splice_url, callback=self.real_video_parse, meta=addition_meta)

    def real_video_parse(self, response: HtmlResponse):
        if 'netflav' in response.url:
            play_video_url = response.css('div.videoiframe_container').css('#iframe-block::attr(src)').extract_first()
            avple_id = play_video_url.split('/')[-1]
            post_url = 'https://www.avple.video/api/source/{0}'.format(avple_id)
            json_header = {'Content-Type': 'application/json'}
            post_body = {play_video_url: 'www.avple.video'}
            # self.logger.warn('组装请求:url={0} body={1} meta={2}'.format(post_url, json.dumps(post_body), response.meta))
            yield scrapy.Request(url=post_url, headers=json_header, body=json.dumps(post_body),
                                 meta=response.meta, method='POST', callback=self.real_video_parse)
        elif 'avple.video' in response.url:
            json_resp = json.loads(response.text)
            data = json_resp['data']
            # TODO 有一些返回的有多个清晰度，有一些只有一个
            for real_info in data:
                self.logger.warn(real_info['label'])
            # if len(data) > 1:
            #     a = max(data, key=lambda datum: int(datum.get("label", "0p")[:-1]))
            #     self.logger.warn(a['label'])
                # self.logger.warn('ddddddddd:{0}'.format(data))
            # if len(data) == 1:
            #     clarity = data['label']
            #     video_type = data['type']
            #     real_url = data['file']
            #     video_name = '{0}-{1}.{2}'.format(response.meta['name'], clarity, video_type)
            #     yield DownloadVideoItem(file_urls=real_url, file_name=video_name)
            # else:
            #     self.logger.warn('ddddddddd:{0}'.format(data))
        else:
            self.logger.warn('获取真实视频地址失败,url:{0}'.format(response.url))
