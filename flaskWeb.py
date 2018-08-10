from flask import Flask,g
from RedisClient import RedisClient

__all__ = ['app']
app = Flask(__name__)


def get_conn():
    # 检查g中是否存在redis属性
    if not hasattr(g, 'redis'):
        # 如果没有
        g.redis = RedisClient()
    return g.redis


# 进行路径映射
@app.route('/')
def index():
    return '<h2>Welcome to Proxy Pool System</h2>'


@app.route('/random')
def get_proxy():
    """
    随机获取可用代理
    :return: 随机代理
    """
    conn = get_conn()
    # 调用方法随即返回一个proxy
    return conn.random()


@app.route("/count")
def get_counts():
    """
    获取代理池总量
    :return: 代理总数
    """
    conn = get_conn()
    return str(conn.count())


if __name__ == "__main__":
    app.run()

