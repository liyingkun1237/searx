# --*-- coding: utf-8 _*_
# @Author   :liyingkun
# @time     :2019/11/14 4:04 下午
# @File     :toutiaosearch.py
# @Software :PyCharm
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
base_url = 'https://m.toutiao.com/search/?pd=video&source=search_subtab_switch&format=json&count=10&offset=20&from=video&'
search_url = base_url + 'keyword={query}&start_index={start_index}'

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


# get response from search-request
def response(resp):
    results = []

    results_json = loads(resp.text).get('scripts')
    print(results_json)
    results_json = loads(results_json[results_json.find('{'):results_json.find('</s')])
    results.append({'url': results_json.get('url', ''),
                    'title': results_json.get('title', ''),
                    'content': results_json.get('display', {}).get('emphasized', {}).get('summary', ''),
                    'template': 'videos.html',
                    'embedded': embedded_url.format(url=results_json.get('url', '')),
                    'thumbnail': results_json.get('display', {}).get('info', {}).get('images', [''])[0],
                    'channelId': results_json.get('user_id', '')})

    return results
