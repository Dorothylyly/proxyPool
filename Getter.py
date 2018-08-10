from RedisClient import RedisClient
from Crawler import Crawler



POOL_UPPER_THRESHOLD = 10000
"""
    定义一个Getter类,用来动态地调用所有以crawl开头的方法
"""


class Getter(object):
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):
        """
            判断是否达到了代理池的限制
        """
        if self.redis.count() > POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        print("获取器开始执行")
        # 如果代理池中的代理数量没有达到最大限制
        if not self.is_over_threshold():
            # 向代理池中添加代理
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                proxies = self.crawler.get_proxies(callback)
                for proxy in proxies:
                    self.redis.add(proxy)





