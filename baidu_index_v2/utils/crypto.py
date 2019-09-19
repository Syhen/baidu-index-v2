# -*- coding: utf-8 -*-
"""
create on 2019-05-19 下午9:43

author @heyao
"""


def decrypt(key, data):
    n = list(key)
    i = list(data)
    a = {}
    r = []
    for o in range(int(len(n) / 2)):
        a[n[o]] = n[int(len(n) / 2) + o]
    for s in range(len(data)):
        r.append(a[i[s]])
    return "".join(r)
