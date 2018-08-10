
import redis
# 生成随机数
from random import choice
"""
    操作缓存数据库的有序集合,实现分数的设置，代理的获取
    检测代理
"""
# 最大分数 100分为高可用
MAX_SCORE = 100
# 最低分数 一旦低于0分 立即剔除
MIN_SCORE = 0
# 刚爬取到的代理的初始化分数
INITIAL_SCORE = 10
#
# #LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
# DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"


REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PASSWORD = "123456"
REDIS_KEY = "proxies"
from loggingCustom import log as logging

class RedisClient(object):

    # logging.basicConfig(filename='RedisClient.#log', level=logging.DEBUG, format=#LOG_FORMAT, datefmt=DATE_FORMAT)

    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化
        :param host: 地址
        :param port: 端口
        :param password: 密码
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加代理，设置分数为最高
        :param proxy:
        :param score:
        :return:
        """

        # 如果redis里面没有 这个proxy 就将代理添加进redis
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, score, proxy)

    def random(self):
        """
         随机获取有效代理，首先尝试获取最高代理分数，如果最高分数不存在，则按排名获取，否则异常
         :return: 随机代理
        """
        # result 返回score等于100的所有代理列表  大于等于MAX_SCORE小于等于MAX_SCORE
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            # 在result列表中 随机选择一个，实现负载均衡
            return choice(result)
        # 如果不存在100分的代理
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 100)
            # 当result不为空时
            if len(result):
                return choice(result)
            else:
                logging().warning("raise PoolEmptyError")
                raise TimeoutError

    def decrease(self, proxy):
        """
        代理值减一分，分数小于最小值，则代理删除
        :param proxy: 代理
        :return: 修改后的代理的分数
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            logging().info("proxy{}score{} - 1".format(proxy, score))
            print("proxy", proxy, "score", score, "-1")
            return self.db.zincrby(REDIS_KEY, proxy, -1)
        else:
            print("proxy", proxy, "score too low,out")
            return self.db.zrem(REDIS_KEY, proxy)

    def exits(self,proxy):
        """
        判断代理是否存在
        :param proxy: 代理
        :return: 是否存在
        """
        return not self.db.zscore(REDIS_KEY, proxy) is None

    def max(self, proxy):
        """
        将代理设置为 MAX_SCORE
        :param proxy: 代理
        :return:
        """

        logging().info("proxy{}ok,set score {}".format(proxy, MAX_SCORE))

        print("proxy", proxy, "ok,set score", MAX_SCORE)
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

    def count(self):
        """
        获取代理数量
        :return: 代理数量
        """
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """
        获取全部代理列表
        :return:
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)



