import json

from pyquery import PyQuery as pq
from get_page import get_page
from loggingCustom import log as logging


# LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
# DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
# #logging.basicConfig(filename='proxyPool.log', level=#logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)
# 创建元类 用这个类去创建别的类 继承type

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Referer': 'http://www.goubanjia.com/buy/dynamic.html'
}


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        # 相当于在类中定义了一个 CrawlFunc 变量
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'Craw_' in k:

                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)

# 继承object类 元类是 ProxyMetaclass


class Crawler(object, metaclass=ProxyMetaclass):
    # #logging.basicConfig(filename='proxyPool.log', level=#logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)

    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print("success get proxy", proxy)
            proxies.append(proxy)
        return proxies

    def Craw_daili66(self, page_count=4):
        """
        获取代理66
        :param page_count: 页码
        :return: 代理
        """

        # 使用占位符
        start_url = "http://www.66ip.cn/{}.html"
        # 将 page 添加到 start_url中
        urls = [start_url.format(page) for page in range(1, page_count+1)]
        for url in urls:
            print("Crawling", url)
            html = get_page(url)
            if html:
                doc = pq(html)
                # 选择大于0 索引的行
                try:
                    trs = doc('.containerbox table tr:gt(0)').items()
                    for tr in trs:
                        ip = tr.find("td:nth-child(1)").text()
                        port = tr.find("td:nth-child(2)").text()
                        logging().info("Spider get proxy{}:{}".format(ip, port))
                        yield ":".join([ip, port])
                except RuntimeError as e:
                   print(e.args)


    def crawl_goubanjia(self):
        """
        获取 Goubanjia
        :return: 代理
        """
        start_url = "http://www.goubanjia.com"
        html = get_page(start_url)
        if html:

            doc = pq(html)
            print(doc)
            trs = doc(".table > tbody:nth-child(2)").items()
            for tr in trs:
                tr.find("p").remove()
                ip_port = tr.find("td.ip").text().replace("\n", "")
                logging().info("Spider get proxy", ip_port)
                yield ip_port







