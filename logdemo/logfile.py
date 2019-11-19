# --*-- coding: utf-8 _*_
# @Author   :liyingkun
# @time     :2019/11/18 2:49 下午
# @File     :logfile.py
# @Software :PyCharm

import sys

from loguru import logger

# 日志相关的配置参数
LOG_ENABLED = True  # 是否开启日志
LOG_TO_CONSOLE = True  # 是否输出到控制台
LOG_TO_FILE = True  # 是否输出到文件
LOG_TO_ES = True  # 是否输出到 Elasticsearch

import requests
import json


def send_dingding_func(message):
    """参考链接 https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq"""
    baseUrl = "https://oapi.dingtalk.com/robot/send?access_token=87094fd19f145edece814053f1342e5633bffe0a648bd438290e5cc5398f8337"

    # please set charset= utf-8
    HEADERS = {
        "Content-Type": "application/json ;charset=utf-8 "
    }

    # 这里的message是你想要推送的文字消息
    # message = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    # stringBody = {
    #     "msgtype": "text",
    #     "text": {"content": message},
    #     # "at": {
    #     #     "atMobiles": ["1825718XXXX"],
    #     #        "isAtAll": True   #@所有人 时为true，上面的atMobiles就失效了
    #     # }
    # }
    # print(message)
    message_dict = json.loads(message)
    text_dict = {"time": message_dict.get('record').get('time').get('repr'),
                 "module": message_dict.get('record').get('module'),
                 "name": message_dict.get('record').get('name'),
                 "level": message_dict.get('record').get('level').get('name'),
                 "exception": message_dict.get('record').get('exception'),
                 "line": message_dict.get('record').get('line'),
                 "text": message_dict.get('text')
                 }
    stringBody = {
        "msgtype": "markdown",
        "markdown": {
            "title": "{module}.py出错了,@18910785537速去查探！！".format(module=text_dict.get('module')),
            "text": "####  time:{time}\n #### module:{module}.{name}\n  #### level:{level}\n\n  #### exception:__{exception}__\n  #### line:{line}\n ".format(
                **text_dict)
        },
        "at": {
            "atMobiles": [
                "18910785537"
            ],
            "isAtAll": False
        }
    }
    MessageBody = json.dumps(stringBody)
    result = requests.post(url=baseUrl, data=MessageBody, headers=HEADERS)
    print(result.text)


def get_logger(name=None):
    if not name:
        name = __name__
    # 输出到控制台
    if LOG_ENABLED and LOG_TO_CONSOLE:
        logger.add(sys.stderr, format="{time} {level} {message}", filter="", level="INFO")

    # 输出到文件
    if LOG_ENABLED and LOG_TO_FILE:
        # 如果路径不存在，创建日志文件文件夹
        logger.add("file.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")

    # 输出到 dingding
    if LOG_ENABLED and LOG_TO_ES:
        # 添加
        logger.add(send_dingding_func, serialize=True)

    # logger['name'] = name
    return logger


if __name__ == '__main__':
    # send_dingding_func('lyk test')
    logger_ = get_logger()


    # logger_.debug('this is debug')

    @logger_.catch
    def my_function(x, y, z):
        # An error? It's caught anyway!
        return 1 / (x + y + z)


    my_function(0, 0, 0)
    print(' ')
