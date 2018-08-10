from loggingCustom import log as logging
from tester import Tester
from Getter import Getter
import time

# 多线程模块
from multiprocessing import Process
from flaskWeb import app

API_ENABLE = True
TESTER_CYCLE = 20
GETTER_CYCLE = 20
TESTER_ENABLED = True
GETTER_ENABLE = True





class Scheduler():

    def schedule_tester(self, cycle=TESTER_CYCLE):
        """
        定时检测代理
        :param cycle:
        :return:
        """
        tester = Tester()
        while True:
            logging().info("测试器开始运行")
            print("测试器开始运行")
            tester.run()
            time.sleep(cycle)

    def schedule_getter(self, cycle=GETTER_CYCLE):
        getter = Getter()
        while True:
            logging().info("开始抓取代理")
            print("开始抓取代理")
            # 抓取器开始运行
            getter.run()
            time.sleep(cycle)

    def schedule_api(self):
        """
        开启api
        :return:
        """
        app.run()

    def run(self):
        logging().info("代理池开始运行")
        print("代理池开始运行")
         # 以主线程为父线程 创建子线程
        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()
        if GETTER_ENABLE:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()
        if API_ENABLE:
            api_process = Process(target=self.schedule_api)
            api_process.start()


if __name__=="__main__":
    Scheduler().run()



