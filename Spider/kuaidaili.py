from Spider.base import BaseSpider,ProxyItem
from lxml import etree

page = 100


class KuaiSpider(BaseSpider):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.base_url = 'https://www.kuaidaili.com/free/inha/{}/'
        self.page = page

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
    spider = KuaiSpider()
    num = 0
    for item in spider.proxies:
        print(item)
    print(num)
