# -*- coding: utf-8 -*-
"""
create on 2019-05-19 下午9:55

author @heyao
"""

from datetime import datetime


def str2date(s):
    y, m, d = s.split('-')
    return datetime(int(y), int(m), int(d), 0, 0, 0)


def date2str(d):
    return '%s-%s-%s' % (d.year, d.month, d.day)
