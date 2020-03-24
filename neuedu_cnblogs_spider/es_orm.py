# -*- coding: utf-8 -*-
# @Time    : 2020/3/23 0023 23:35
# @Author  : Han lei
# @Email   : hanlei5012@163.com
# @File    : es_orm.py
# @Software: PyCharm
from datetime import datetime

from elasticsearch_dsl import Document, connections, Text, Keyword, Date

connections.create_connection(hosts=['127.0.0.1'])
class cnblogsIndex(Document):
    title = Text(analyzer='ik_max_word')
    description = Text(analyzer='ik_max_word')
    url=Keyword()
    article_date=Date()

    class Index:
        name = 'cnblogs_new'
        settings={
            'number_of_shards':5
        }
if __name__ == '__main__':
    cnblogsIndex.init()

