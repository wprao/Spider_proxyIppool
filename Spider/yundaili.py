from Spider.base import BaseSpider,ProxyItem
from lxml import etree

page = 20

class YunSpider(BaseSpider):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.base_url = 'http://www.ip3366.net/free/?stype=1&page={}'
        self.page = page
        self.encoding = 'gbk'

    def parse(self, response):
        html = etree.HTML(response)
        trs = html.xpath('.//*[@id="list"]/table/tbody/tr')
        for tr in trs:
            item = ProxyItem()
            item['scheme'] = tr.xpath('./td[4]/text()')[0].lower()
            item['proxy'] = item['scheme'] + "://" + tr.xpath('./td[1]/text()')[0] + ":" + \
                            tr.xpath('./td[2]/text()')[0]
            self.count += 1
            yield item

if __name__ == '__main__':
    spider = YunSpider()
    for item in spider.proxies:
        print(item)
    print(spider.count)
