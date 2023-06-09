from pathlib import Path
from urllib.parse import urlparse, urlunparse

import scrapy
import playwright

def custom_headers(browser_type, playwright_request, scrapy_headers) -> dict:
    url = playwright_request.url
    res = urlparse(url)
    loc = res.netloc
    host = urlunparse([res.scheme, res.netloc, '', '', '', ''])
    page_url = urlunparse([res.scheme, res.netloc, res.path, '', '', ''])
    return {
        'authority': loc,
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'origin': host,
        'referer': host,
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'x-referer-page': page_url,
        'x-rp-client': 'h5_1.0.0',
    }


class QuoteSpider(scrapy.Spider):
    name = 'quotes123'
    custom_settings = {"PLAYWRIGHT_PROCESS_REQUEST_HEADERS": custom_headers}

    def start_requests(self):
        urls = [
            "https://item.jd.com/7836786.html"
        ]
        for url in urls:
            yield scrapy.Request(url=url, meta={"playwright": True}, callback=self.parse)

    def parse(self, response, **kwargs):

        page = response.url.split('/')[-1]
        filename = f'17836786.html'
        Path(filename).write_bytes(response.body)
        self.log(f'Saved file {filename}')
'''
执行： 项目根目录执行 scrapy crawl quotes
'''