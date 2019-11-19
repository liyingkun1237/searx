# --*-- coding: utf-8 _*_
# @Author   :liyingkun
# @time     :2019/11/14 2:23 下午
# @File     :ixigua.py
# @Software :PyCharm

from functools import reduce
from json import loads

from searx.engines.contactTool import myextractor
from searx.engines.xpath import extract_text
from searx.engines.youtubeUser import youtubeUser
from searx.utils import list_get
from searx.url_utils import quote_plus

# engine dependent config
categories = ['videos']
paging = True
language_support = False
time_range_support = True

# search-url
base_url = 'https://www.ixigua.com/search/'
search_url = base_url + '{query}'

embedded_url = '<iframe width="540" height="304" ' + \
               'data-src="{url}" ' + \
               'frameborder="0" allowfullscreen></iframe>'


# do search-request
def request(query, params):
    pageno = params['pageno']
    start_index = (int(pageno) - 1) * 10
    params['url'] = search_url.format(query=quote_plus(query),
                                      start_index=start_index)
    # if params['time_range'] in time_range_dict:
    #     params['url'] += time_range_url.format(time_range=time_range_dict[params['time_range']])

    return params


# 通过接口直接查询出粉丝数和被关注数
import requests


def follow(authorId):
    url = "https://www.ixigua.com/api/userv2/follow/list"

    querystring = {"_signature": "sNwNEAAgEAZo-GZiN0tr87DcDQAAO0g", "authorId": "{}".format(authorId)}

    headers = {
        'User-Agent': "PostmanRuntime/7.19.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "0b04bb90-0012-4c66-bb47-49da23822006,621c78e2-ab27-4ac9-b934-d2a2606a5c2c",
        'Host': "www.ixigua.com",
        'Accept-Encoding': "gzip, deflate",
        'Cookie': "xiguavideopcwebid=6759069506889647629; xiguavideopcwebid.sig=T8UvzRS99ES_b7eXYmowh_JO3N8",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    # todo 加代理
    response = requests.request("GET", url, headers=headers, params=querystring)

    # print(response.text)
    if response.status_code == 200:
        result_json = loads(response.text)
        sections = result_json.get('data', {}).get('data', [])
        results = {'follow': result_json.get('data').get('total_number'), 'followDetail': sections}

    else:
        pass
        # todo 重试机制
    return results


def fans(authorId):
    url = "https://www.ixigua.com/api/userv2/fans/list"

    querystring = {"_signature": "6f1kSgAgEAcx2Q84dh.ktun9ZFAALQ-", "authorId": "{}".format(authorId)}

    headers = {
        'User-Agent': "PostmanRuntime/7.19.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "dc28d6f2-5f8e-469c-af77-3fccfa9236df,7b7b4d46-eeba-478b-a7c6-cf628c093453",
        'Host': "www.ixigua.com",
        'Accept-Encoding': "gzip, deflate",
        'Cookie': "xiguavideopcwebid=6759069506889647629; xiguavideopcwebid.sig=T8UvzRS99ES_b7eXYmowh_JO3N8",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    def trans_int(x):
        try:
            if '万' in x:
                x = x.replace('.', '').replace('万', '')
                return int(x) * 10000
            else:
                return int(x)
        except Exception as e:
            print(str(e))
            return 0

    response = requests.request("GET", url, headers=headers, params=querystring)
    # print(response.text)
    if response.status_code == 200:
        result_json = loads(response.text)
        sections = result_json.get('data', {}).get('fan_nums', [])
        fans = sum([trans_int(section.get('fans_count')) for section in sections])
        results = {'fans': fans, 'fansDetail': sections}
    else:
        pass
        # todo 重试机制
    return results


# get response from search-request
def response(resp):
    results = []

    results_data = resp.text[resp.text.find('<script type="application/json" id="SSR_HYDRATED_DATA">'):]
    results_json = loads(results_data[results_data.find('{'):results_data.find('}</') + 1])
    # print(results_json)

    sections = results_json.get('complexSearch', {}).get('res', '').get('data', [])
    if sections:
        for section in sections:
            if section.get('cell_type') == 51:
                url = 'https://www.ixigua.com/i{}/'.format(section.get('group_id', ''))
                # 获取粉丝数和观看量
                authorId = section.get('user_info', {}).get('user_id')
                follow_ = follow(authorId)
                fans_ = fans(authorId)
                snippet = {"title": section.get('user_info').get('name'), "publishedAt": "", "country": "CN",
                           "thumbnails": {"high": {"url": section.get('user_info').get('avatar_url')}}}
                statistics = {'viewCount': -1, 'commentCount': 0,
                              'subscriberCount': fans_.get('fans'), 'videoCount': -1,
                              'follow': follow_.get('follow')}

                userItems = {"snippet": snippet, "statistics": statistics}
                results.append({'url': url,
                                'title': section.get('title', ''),
                                'content': section.get('title', ''),
                                'template': 'videos.html',
                                'embedded': embedded_url.format(url=url),
                                'thumbnail': section.get('video_detail_info', {}).get('detail_video_large_image',
                                                                                      {}).get('url', ''),
                                'channelId': authorId,
                                'userItems': userItems,
                                "statistics": {'fansDetail': fans_.get('fansDetail'),
                                               'followDetail': follow_.get('followDetail')}
                                })


            else:
                print(section.get('cell_type'))
    return results
