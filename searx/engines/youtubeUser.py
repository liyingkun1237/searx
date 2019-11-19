# --*-- coding: utf-8 _*_
# @Author   :liyingkun
# @time     :2019/11/13 4:55 下午
# @File     :youtubeUser.py
# @Software :PyCharm

import requests
import json

url = "https://www.googleapis.com/youtube/v3/channels"
api_key = 'AIzaSyBc3xAnnqvIEh3pbdBQTm97Lpm7Ae29EEk'


def youtubeUser(ids):
    querystring = {"part": "snippet,contentDetails,statistics", "id": "{}".format(ids),
                   "key": "AIzaSyBc3xAnnqvIEh3pbdBQTm97Lpm7Ae29EEk", "maxResults": "50"}

    headers = {
        'User-Agent': "PostmanRuntime/7.19.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "a7402d47-7d9a-48d3-8334-690fcabccbfe,ad2c58e2-1b41-4d15-a55d-10a4eab2491a",
        'Host': "www.googleapis.com",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        print('请求youtubeuser出错', ids, '错误码：', response.status_code)
        return {}
