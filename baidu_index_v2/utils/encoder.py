# -*- coding: utf-8 -*-
"""
create on 2019-05-19 下午9:44

author @heyao
"""


def urlencode(query):
    """查询字符串编码
    与 `urllib.urlencode` 不同的是，如果传入的值是None，或key是空字符串、None，不会编码"="
    :param query: dict.
    :return: str
    >>> urlencode({"a": None, "b": ""})
    <<< "a&b="
    >>> urlencode({"": "abc", "b": ""})
    <<< "abc&b="
    """

    def encode(key, val):
        """编码单个键值对"""
        if val is None or not key:
            return val
        return '%s=%s' % (key, val)

    result = [encode(key, val) for key, val in query.items()]
    return '&'.join(result)
