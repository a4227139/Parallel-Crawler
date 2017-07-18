#-*- coding:utf-8 -*-
import random
import base64
from settings import PROXIES

class RandomUserAgent(object):
    """Randomly rotate user agents based on a list of predefined ones"""

    def __init__(self, agents):
        self.agents = agents

    #该方法通过Crawler的 scrapy.crawler.Crawler.settings 属性进行访问
    @classmethod
    def from_crawler(cls, crawler):
        #settings.getlist将某项配置的值以列表形式返回。如果配置值本来就是list则将返回其拷贝。 如果是字符串，则返回被 ”,” 分割后的列表。cls实例化。
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
	#print "**************************" + random.choice(self.agents)
        request.headers.setdefault('User-Agent', random.choice(self.agents))

class ProxyMiddleware(object):
  def process_request(self, request, spider):
    proxy = random.choice(PROXIES)
    if proxy['user_pass'] is not None:
      request.meta['proxy'] = "http://%s" % proxy['ip_port']
      encoded_user_pass = base64.encodestring(proxy['user_pass'])
      request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
      print "**************ProxyMiddleware have pass************" + proxy['ip_port']
    else:
      print "**************ProxyMiddleware no pass************" + proxy['ip_port']
      request.meta['proxy'] = "http://%s" % proxy['ip_port']