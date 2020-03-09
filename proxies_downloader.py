"""实现代理IP的下载及入库功能"""
from setting import SPIDER_LIST
import importlib
from proxies_client import ProxiesClient
from threading import Thread,Lock

class ProxiesDownloader(object):
    def __init__(self):
        self.client = ProxiesClient()
        self._original_proxy_num = self.client.all_count
        self._count = 0
        self._lock = Lock()

    @property
    def _spiders(self):
        spider_list = []
        for spider_name in SPIDER_LIST:
            module_name = spider_name.rsplit(".", 1)[0]
            class_name = spider_name.rsplit('.', 1)[1]
            module = importlib.import_module(module_name)
            spider = getattr(module, class_name)
            spider_list.append(spider())
        return spider_list

    def download(self):
        th_list = []
        for spider in self._spiders:
            th = Thread(target=self._download,args=(spider,))
            th_list.append(th)
            th.setDaemon(True)
            th.start()
        for th in th_list:
            th.join()

    def _download(self,spider):
        try:
            for item in spider.proxies:
                self.client.add_new(key=item['scheme'], proxy=item['proxy'])
                self._lock.acquire()
                self._count += 1
                self._lock.release()
        except Exception as e:
            print(e)

    @property
    def download_count(self):
        return self._count

    @property
    def new_add_count(self):
        return self.client.all_count-self._original_proxy_num

if __name__ == '__main__':
    downloader = ProxiesDownloader()
    downloader.download()
    print('*'*100)
    print('下载完毕')
    print('共爬取了【{}】个代理IP'.format(downloader.download_count))
    print('新入库了【{}】个代理IP'.format(downloader.new_add_count))
