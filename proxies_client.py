'''代理IP出库和入库的规则(Redis)'''
from redis import StrictRedis
from setting import REDIS_DB, REDIS_HOST, REDIS_PORT
import logging
import random

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(threadName)s %(levelname)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S')

# 分数规则设置
max_score = 100
initial_score = 10
min_score = 0

class EmptyPool(Exception):
    pass

class ProxiesClient(object):
    def __init__(self):
        self.client = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

    def add_new(self, key, proxy):
        '''
        将爬取的代理IP入库。若添加成功返回True，如代理IP已经存在，则返回False
        key: http或https，将不同协议的地址存入到数据库不同的键中
        proxy: 待添加的代理IP
        '''
        key = key.lower()
        if not self.client.zscore(key, proxy):
            self.client.zadd(key,{proxy: initial_score})
            msg = "【新增IP】：IP地址为【{}】,并将score初始化为【{}】".format(proxy,initial_score)
            logging.info(msg)
            return True
        else:
            return False

    def max_score(self, key, proxy):
        '''
        当代理IP访问成功时，将score设置为最大值。
        '''
        key = key.lower()
        self.client.zadd(key,{proxy:max_score})
        msg = "【有效IP】：代理IP【{}】访问成功，将score设置为【{}】".format(proxy,max_score)
        logging.info(msg)

    def reduce_score(self, key, proxy):
        '''
        当代理IP访问不成功时，将score在原基础上减1
        '''
        key = key.lower()
        new_score = self.client.zincrby(key,-1,proxy)
        if new_score >=0:
            msg = "【失效IP】：代理IP【{}】访问失败，score从【{}】减为【{}】".format(proxy,new_score+1,new_score)
        else:
            self.client.zrem(key,proxy)
            msg = "【失效IP】：代理IP【{}】访问失败，score减为【{}】，从数据库中移除".format(proxy,min_score)
        logging.info(msg)

    def random_proxy(self, key):
        '''
        从数据库中随机获取一个代理IP地址。
        规则：先取出分数为100的代理IP，如果不存在，则从分数排名前20的序列中随机返回一个
        '''
        target_list = self.client.zrangebyscore(key,max_score,max_score)
        if not target_list:
            target_list = self.client.zrevrange(key,0,20)
        if not target_list:
            raise EmptyPool('pool is empty')
        return random.choice(target_list)

    def get_score(self, proxy):
        '''获取proxy的分数'''
        key = proxy.split(':',1)[0].lower()
        score = self.client.zscore(key,proxy)
        return score

    @property
    def http_proxies(self):
        '''
        获取全部http协议的代理IP
        '''
        if self.http_count:
            return self.client.zrange('http',0,-1)
        else:
            raise EmptyPool('当前数据库没有http代理IP')

    @property
    def https_proxies(self):
        '''
        获取全部https协议的代理IP
        '''
        if self.https_count:
            return self.client.zrange('https', 0, -1)
        else:
            raise EmptyPool('当前数据库没有https代理IP')

    @property
    def all_proxies(self):
        '''
        获取全部代理IP
        '''
        if self.all_count:
            proxies = self.client.zrange('http',0,-1) + self.client.zrange('https',0,-1)
            return proxies
        else:
            raise EmptyPool('当前数据库没有代理IP')

    @property
    def http_count(self):
        '''获取http代理IP的个数'''
        number = self.client.zcard('http')
        return number

    @property
    def https_count(self):
        '''获取https代理IP的个数'''
        number = self.client.zcard('https')
        return number

    @property
    def all_count(self):
        '''获取代理IP的个数'''
        return self.http_count+self.https_count

if __name__  ==  '__main__':
    client = ProxiesClient()
    print(client.all_proxies)
