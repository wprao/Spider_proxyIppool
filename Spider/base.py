import requests
import scrapy
import logging
from requests.exceptions import HTTPError
import time

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(threadName)s %(levelname)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S')

class ProxyItem(scrapy.Item):
    scheme = scrapy.Field()
    proxy = scrapy.Field()

class BaseSpider(object):
    encoding = 'utf-8'
    base_url = ''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:25.0) Gecko/20100101 Firefox/25.0',
    }
    page = 1
    count = 0

    def __init__(self):
        msg = "【访问网页】 ：爬虫【{}】正在下载网页信息".format(self.__class__)
        logging.info(msg)

    @property
    def start_urls(self):
        for i in range(1,self.page+1):
            yield self.base_url.format(i)

    def get_response(self,url):
        time.sleep(0.5)
        response = requests.get(url,headers=self.headers)
        return response.content.decode(self.encoding)

    def parse(self,response):
        yield None

    @property
    def proxies(self):
        for url in self.start_urls:
            logging.info('【访问网页】 ： 正在从网页【{}】下载数据'.format(url))
            response = self.get_response(url)
            for item in self.parse(response):
                yield item
