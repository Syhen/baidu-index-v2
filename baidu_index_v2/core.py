# -*- coding: utf-8 -*-
"""
create on 2019-05-16 下午12:36

author @heyao
"""
from datetime import timedelta
import json

from baidu_index_v2 import apis
from baidu_index_v2.utils.crypto import decrypt
from baidu_index_v2.utils.date import str2date, date2str
from baidu_index_v2.utils.web import make_response


def mean(x):
    x = [i if i else 0 for i in x]
    if not len(x):
        return 0
    return sum(x) / len(x)


class BaiduIndexCrawler(object):
    SINGLE_INDEX_MAX_DURATION = 365
    HEADERS = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"

    def __init__(self, cookies, headers=None):
        self.cookies = self._format_cookies(cookies)
        self.headers = headers or {
            "User-Agent": self.HEADERS,
            "X-Requested-With": "XMLHttpRequest",
            "Host": "index.baidu.com",
            "Referer": "http://index.baidu.com/v2/main/index.html",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7"
        }

    def _format_cookies(self, cookies):
        if not isinstance(cookies, str):
            return cookies
        return {i.split('=', 1)[0]: i.split('=', 1)[1] for i in cookies.split('; ')}

    def set_cookies(self, cookies):
        self.cookies = cookies

    def get_decrypt_key(self, uniqid):
        response = make_response(apis.API_DECRYPT_KEY, cookies=self.cookies, headers=self.headers, uniqid=uniqid)
        return response.json()['data']

    def _make_data(self, indexes, ratios, decrypt_key, key):
        result = {
            'data': [int(i) if i else None for i in decrypt(decrypt_key, indexes[key]['data']).split(',')],
            'end_date': indexes[key]['endDate'],
            'start_date': indexes[key]['startDate'],
            'avg': ratios[key]['avg']
        }
        return result

    def fetch_index(self, word, days=30):
        response = make_response(apis.API_SEARCH_INDEX, cookies=self.cookies, headers=self.headers, word=word,
                                 days=days)
        index_data = json.loads(response.content)
        if not index_data['data']:
            return {key: {} for key in ('all', 'wise', 'pc')}
        uniqid = index_data['data']['uniqid']
        indexes = index_data['data']['userIndexes'][0]
        ratios = index_data['data']['generalRatio'][0]
        decrypt_key = self.get_decrypt_key(uniqid)
        indexes = {key: self._make_data(indexes, ratios, decrypt_key, key) for key in ('all', 'wise', 'pc')}
        return indexes

    def _fetch_index_from_date_range(self, word, start_date, end_date):
        response = make_response(apis.API_SEARCH_INDEX_RANGE, cookies=self.cookies, headers=self.headers, word=word,
                                 start_date=start_date, end_date=end_date)
        index_data = json.loads(response.content)
        if not index_data['data']:
            return {key: {} for key in ('all', 'wise', 'pc')}
        uniqid = index_data['data']['uniqid']
        indexes = index_data['data']['userIndexes'][0]
        ratios = index_data['data']['generalRatio'][0]
        decrypt_key = self.get_decrypt_key(uniqid)
        indexes = {key: self._make_data(indexes, ratios, decrypt_key, key) for key in ('all', 'wise', 'pc')}
        return indexes

    def fetch_index_from_date_range(self, word, start_date, end_date):
        _start_date = str2date(start_date)
        _end_date = str2date(end_date)
        if (_end_date - _start_date).days <= self.SINGLE_INDEX_MAX_DURATION:
            return self._fetch_index_from_date_range(word, start_date, end_date)
        indexes = []
        days = (_end_date - _start_date).days
        # 根据每365天获取指数
        while days * 1. / self.SINGLE_INDEX_MAX_DURATION > 0:
            local_start_date = date2str(_start_date)
            add_days = self.SINGLE_INDEX_MAX_DURATION - 1 if days > self.SINGLE_INDEX_MAX_DURATION else days
            local_end_date = date2str(_start_date + timedelta(days=add_days))
            _start_date = _start_date + timedelta(days=add_days + 1)
            days = (_end_date - _start_date).days
            indexes.append(self._fetch_index_from_date_range(word, local_start_date, local_end_date))
        # 初始化对象
        result = {key: {'data': [], 'end_date': end_date, 'start_date': start_date, 'avg': 0} for key in
                  ('all', 'wise', 'pc')}
        # 将所有指数拼接起来
        for index in indexes:
            for platform, data in index.items():
                if 'data' not in data:
                    break
                result[platform]['data'].extend(data['data'])
        # 求平均值
        for platform, data in result.items():
            if 'data' not in data:
                break
            result[platform]['avg'] = mean(data['data'])
        return result


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    cookies = ''
    baidu_index_crawler = BaiduIndexCrawler(cookies)
    indexes = baidu_index_crawler.fetch_index_from_date_range("拍拍贷", start_date="2014-4-12", end_date="2016-4-13")
    print(indexes)
    for key in indexes:
        plt.plot(indexes[key]['data'], label=key)
    plt.legend()
    plt.show()
