
from RedisClient import RedisClient
import aiohttp
import asyncio
import time
# 定义合法的状态码
VALID_STATUS_CODE = [200]

TEST_URL = "http://desk.zol.com.cn/fengjing/"
# 定义一次最多验证多少个代理IP
BATCH_TEST_SIZE = 100

# aiohttp 其实表示协程


class Tester(object):
    def __init__(self):
        self.redis = RedisClient()

    # 异步的方法
    async def test_single_proxy(self, proxy):
        """
        方法用于检测一个代理是否合法
        :param proxy: 需要检测的代理
        :return:
        """

        # 用来设置一次最大连接数量 参数用来防止ssl报错
        conn = aiohttp.TCPConnector(verify_ssl=False)
        # 用来创建一个Session连接
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                # 检测proxy是否为bytes类型
                if isinstance(proxy,bytes):
                    # 如果是的话 用utf-8进行proxy编码
                    proxy = proxy.decode('utf-8')
                real_proxy="http://"+proxy
                print("testing...", proxy)
                # 发起get请求
                async with session.get(TEST_URL, proxy=real_proxy, timeout=15) as response:
                    # 如果响应状态码是200
                    if response.status in VALID_STATUS_CODE:
                        # 将proxy的分数设置为 100
                        self.redis.max(proxy)
                        print("proxy ok", proxy)
                    else:
                        # 将代理分数减一
                        self.redis.decrease(proxy)
                        print("return code is illegal", proxy)
            except (aiohttp.ClientError, aiohttp.ClientConnectorError, TimeoutError,AttributeError):
                self.redis.decrease(proxy)
                print("proxy request fail", proxy)

    def run(self):
        """
        测试主函数
        :return:
        """
        print("测试器开始运行")
        try:
            proxies = self.redis.all()
            # 创建消息循环队列
            loop = asyncio.get_event_loop()
            # 进行批量测试
            for i in range(0, len(proxies), BATCH_TEST_SIZE):
                # 一次测试 100 个代理
                test_proxies = proxies[i:i+BATCH_TEST_SIZE]
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except Exception as e:

            print("error", e.args)







