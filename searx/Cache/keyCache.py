# --*-- coding: utf-8 _*_
# @Author   :liyingkun
# @time     :2019/11/18 5:50 下午
# @File     :keyCache.py
# @Software :PyCharm

import redis

REDIS_HOST = '192.168.1.27'
REDIS_PORT = 6379


class keyRedis(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, decode_responses=True):
        pool = redis.ConnectionPool(host=host, port=port, decode_responses=decode_responses)
        r = redis.Redis(connection_pool=pool)
        self.r = r

    def keyNum(self, keyword):
        """ 对关键词累加1"""
        self.r.hincrby("kool:keywords", keyword, amount=1)

    def getAllkeyNum(self):
        return self.r.hgetall('kool:keywords')

    def getAllkeyNumbyscan(self):
        return self.r.hscan('kool:keywords')

    def saveResult(self, formDict, result):
        self.r.hset("kool:result", formDict, result)

    def getResult(self, formDict):
        return self.r.hget("kool:result", formDict)

    def existsForm(self, formDict):
        return self.r.hexists("kool:result", formDict)


if __name__ == "__main__":
    kr = keyRedis()
    kr.keyNum('mirror')
    print(kr.getAllkeyNum())
    print(kr.getAllkeyNumbyscan())
    kr.saveResult('123', '{"json":"json"}')
    print(kr.getResult('123'))
    print(kr.r.hexists('kool:result', '123'))
    print(kr.r.hexists('kool:result', '1123'))
