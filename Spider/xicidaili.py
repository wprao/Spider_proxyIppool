from Spider.base import BaseSpider,ProxyItem
from lxml import etree

page = 10

class XiciSpider(BaseSpider):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.base_url = 'https://www.xicidaili.com/nn/{}'
        self.page = page

    def parse(self,response):
        html = etree.HTML(response)
        trs = html.xpath('.//table[@id="ip_list"]/tr')
        for tr in trs[1:]:
            item = ProxyItem()
            item['scheme'] = tr.xpath('./td[6]/text()')[0].lower()
            item['proxy'] = item['scheme'] + "://" + tr.xpath('./td[2]/text()')[0] + ":" + tr.xpath('./td[3]/text()')[0]
            self.count += 1
            yield item

if __name__ == '__main__':
    spider = XiciSpider()
    for item in spider.proxies:
        print(item)
    print(spider.count)
