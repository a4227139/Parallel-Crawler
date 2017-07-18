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
class OldSpider(CrawlSpider):
  #定义爬虫的名称
  name = "OldSpider"
  g_queue_urls = Queue.Queue(100000)#全局变量，保存在售的url
  g_container_urls = {""}#
  #定义允许抓取的域名,如果不是在此列表的域名则放弃抓取
  allowed_domains = ["anjuke.com"]
  #定义抓取的入口url
  start_urls = [
    "http://nanning.anjuke.com/sale/p1"
  ]
  # 定义爬取URL的规则，并指定回调函数为parse_item
  rules = [#http://nn.fang.anjuke.com/loupan/            http://nn.fang.anjuke.com/loupan/xingning/s?p=2
    Rule(sle(allow=("/sale/p\d{1,}")),
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
    Houses = sel.css('ul.house-list li')#<div class="day">中的<div class="postTitle">标签，返回的是SelectorList对象
    #print "=============length======="
    #Info = sel.css('div.item-mod div.infos')
    #标题、url和描述的结构是一个松散的结构，后期可以改进
    #print'len(Pos):',len(Houses)
    #print'base_url:',base_url
    for index in range(len(Houses)):
        item=OldItem()
        infos=Houses[index].css('div.house-details div')
        item['link']=infos[0].xpath('a/@href').extract()[0]
        #print item['link']
        info= infos[1].xpath('span')
        item['acreage']= info[0].xpath('text()').extract()[0]
        item['type']= info[1].xpath('text()').extract()[0]
        item['unit_price']= info[2].xpath('text()').extract()[0]
        try:
            item['build_in']=info[4].xpath('text()').extract()[0][:4]
        except:
            item['build_in']=''
        location= infos[2].xpath('span/text()').extract()[0].strip()
        item['name']=location.split('[')[0]
        item['area']=location.split('[')[1].split('-')[0]
        try:
            item['addr']=location.split('[')[1].split('-')[1].split(']')[0]
        except:
            item['addr']=''
        item['total_price']=Houses[index].css('div.pro-price').xpath('span/strong/text()').extract()[0]+'0000'
        #print item['total_price']
        items.append(item)
    return items