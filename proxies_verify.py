"""验证代理IP的有效性"""
from gevent import pool,monkey
monkey.patch_all()
import requests
import time
from fake_useragent import UserAgent
from proxies_client import ProxiesClient
from queue import Queue
from requests.exceptions import RequestException
import logging

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(threadName)s %(levelname)s : %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S')

class ProxiesVerify(object):
    def __init__(self):
        self.client = ProxiesClient()
        self.user_agent = UserAgent()
        self.base_url = '{}://www.baidu.com/'
        self.proxies_queue = Queue()
        self.pool = pool.Pool()

    def _send_response(self):
        time.sleep(1)
        proxy = self.proxies_queue.get()
        scheme = proxy.split(':',1)[0]
        proxies = {
            scheme : proxy
        }
        test_url = self.base_url.format(scheme)
        headers = {'User_Agent':self.user_agent.random}
        try:
            response = requests.get(test_url,headers=headers,proxies=proxies,timeout=5)
            if response.status_code == 200:
                self.client.max_score(scheme,proxy)
            else:
                self.client.reduce_score(scheme,proxy)
                logging.info('【请求异常】：异常原因【请求代码异常】')
        except RequestException as e:
            msg = '【请求异常】，异常原因【{}】'.format(e.args[0])
            logging.info(msg)
            self.client.reduce_score(scheme,proxy)
        finally:
            self.proxies_queue.task_done()

    def _proxies_queue(self):
        for proxy in self.client.all_proxies:
            self.proxies_queue.put(proxy)

    def verify(self):
        self.pool.apply_async(self._proxies_queue)
        time.sleep(3)
        for i in range(20):
            self.pool.apply_async(self._send_response,callback=self._test_task)
        self.proxies_queue.join()

    def _test_task(self,item):
        self.pool.apply_async(self._send_response,callback=self._test_task)

if __name__ == '__main__':
    verify = ProxiesVerify()
    verify.verify()
