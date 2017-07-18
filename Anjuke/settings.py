# -*- coding: utf-8 -*-

# Scrapy settings for Anjuke project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'Anjuke'

SPIDER_MODULES = ['Anjuke.spiders']
NEWSPIDER_MODULE = 'Anjuke.spiders'
ITEM_PIPELINES = {
    'Anjuke.pipelines.AnjukePipeline': 300,
    'Anjuke.pipelines.MySQLStorePipeline': 300,
}
LOG_LEVEL = 'INFO'
COMMANDS_MODULE = 'Anjuke.commands'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Anjuke (+http://www.yourdomain.com)'
DOWNLOADER_MIDDLEWARES = {
#    'Anjuke.middlewares.MyCustomDownloaderMiddleware': 543,
    'Anjuke.middlewares.RandomUserAgent': 1, #随机user agent
   # 'Anjuke.middlewares.ProxyMiddleware': 1,
}
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
]

PROXIES = [
  {'ip_port': '60.212.197.120:8888', 'user_pass': ''},
  {'ip_port': '115.50.83.7:8888', 'user_pass': ''},
  {'ip_port': '222.84.66.99:8888', 'user_pass': ''},
  {'ip_port': '110.178.199.133:8888', 'user_pass': ''},
  {'ip_port': '183.95.122.143:8888', 'user_pass': ''},
  {'ip_port': '27.115.75.114:8080', 'user_pass': ''},
]