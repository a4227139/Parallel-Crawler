#coding=utf-8
import re
import json
import Queue
from scrapy.selector import Selector
try:
  from scrapy.spider import Spider
except:
  from scrapy.spider import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle
from Anjuke.items import *
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
class AnjukeSpider(CrawlSpider):
  #定义爬虫的名称
  name = "AnjukeSpider"
  g_queue_urls = Queue.Queue(100000)#全局变量，保存在售的url
  g_container_urls = {""}#
  #定义允许抓取的域名,如果不是在此列表的域名则放弃抓取
  allowed_domains = ["anjuke.com"]
  #定义抓取的入口url
  start_urls = [
    "http://nn.fang.anjuke.com/loupan/s?p=1"
  ]
  # 定义爬取URL的规则，并指定回调函数为parse_item
  rules = [#http://nn.fang.anjuke.com/loupan/            http://nn.fang.anjuke.com/loupan/xingning/s?p=2
    Rule(sle(allow=("/loupan/all/p\d{1,}")), #此处要注意?号的转换，复制过来需要对?号进行转义。
             follow=True,
             callback='parse_item')#每从link_extractor获取一个链接，执行一次
    # Rule(sle(allow=("/loupan/\d*.html$")),
    #          follow=True,
    #          callback='parse_info')
  ]
  #print "**********CnblogsSpider**********"
  #定义回调函数
  #提取数据到Items里面，主要用到XPath和CSS选择器提取网页数据
  def parse_item(self, response):
    items = []
    sel = Selector(response)#根据输入内容自动采用html或xml的形式构造
    base_url = get_base_url(response)
    Pos = sel.css('div.item-mod div.favor-pos')#<div class="day">中的<div class="postTitle">标签，返回的是SelectorList对象
    #print "=============length======="
    Info = sel.css('div.item-mod div.infos')
    #标题、url和描述的结构是一个松散的结构，后期可以改进
    #print'len(Pos):',len(Pos)
    #print'base_url',base_url
    for index in range(len(Pos)):
      if Info[index].css('div.lp-name i')[0].xpath('text()').extract()[0] !='售罄':
        #print Info.css('div.lp-name h3').xpath('a/@href').extract()[0]
        url=Info[index].css('div.lp-name h3').xpath('a/@href').extract()[0]
        #print url
        if url not in self.g_container_urls:
          self.g_queue_urls.put(url)
          self.g_container_urls.add(url)
    # print 'g_queue_urls:',self.g_queue_urls
    # print 'g_container_urls:',self.g_container_urls
    for j in range(self.g_queue_urls.qsize()):
		tp_url = self.g_queue_urls.get()
		items.append(self.make_requests_from_url(tp_url).
		replace(callback=self.parse_info))
    return items

  def parse_info(self,response):
    # base_url = get_base_url(response)
    # print base_url
    sel=Selector(response)
    #if sel.css('div.fl i').xpath('text()').extract()[0] !='售罄':
    item=AnjukeItem()
    item['name']=sel.xpath('//h1/text()').extract()[0]
    print item['name']
    item['price']=sel.css('dd.price em').xpath('text()').extract()[0]
    # print item['price']
    item['addr']=sel.css('div.basic-parms-wrap dd span.lpAddr-text').xpath('text()').extract()[0]
    #print item['addr']
    item['area']=item['addr'].split(' ')[1]
    #print item['area']
    item['link']=get_base_url(response)
    #print item['link']
    tags=sel.css('div.lp-tags').xpath('span')
    #print 'len(span)',len(span)
    item['tag']=''
    for i in range(len(tags)):
      item['tag']+=' '+tags[i].xpath('text()').extract()[0]
    return item