
"""
create on 2019-05-16 上午11:29

author @heyao
"""

API_DECRYPT_KEY = {
    'host': 'http://index.baidu.com',
    'method': 'GET',
    'mark': '?',
    'query': {'uniqid': '{uniqid}'},
    'path': '/Interface/ptbk'
}
API_SEARCH_INDEX = {
    'host': 'http://index.baidu.com',
    'method': 'GET',
    'mark': '?',
    'query': {
        'word': '{word}',
        'area': '0',
        'days': '{days}'
    },
    'path': '/api/SearchApi/index'
}
API_SEARCH_INDEX_RANGE = {
    'host': 'http://index.baidu.com',
    'path': '/api/SearchApi/index',
    'mark': '?',
    'method': 'GET',
    'query': {
        'area': '0',
        'word': '{word}',
        'startDate': '{start_date}',
        'endDate': '{end_date}'}
}
