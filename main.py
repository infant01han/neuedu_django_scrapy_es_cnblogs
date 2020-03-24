# -*- coding: utf-8 -*-
# @Time    : 2020/3/23 0023 23:31
# @Author  : Han lei
# @Email   : hanlei5012@163.com
# @File    : main.py
# @Software: PyCharm
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
process.crawl('cnblog')
process.start()