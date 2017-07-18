# -*- coding: utf-8 -*-
# from scrapy import signals
# import json
# import codecs
# from scrapy.xlib.pydispatch import dispatcher
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
from scrapy import log
from scrapy.exceptions import DropItem

class AnjukePipeline(object):
    def process_item(self, item, spider):
        return item

class MySQLStorePipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                host='127.0.0.1',#别用localhost，只用127.0.0.1
                db = 'anjuke',
                user = 'root',
                passwd = 'root',
                cursorclass = MySQLdb.cursors.DictCursor,
                charset = 'utf8',
                use_unicode = True
        )

    def process_item(self, item, spider):
        # run db query in the thread pool
        query = self.dbpool.runInteraction(self._conditional_insert, item,spider)
        query.addErrback(self.handle_error)
        # at the end return the item in case of success or failure
        query.addBoth(lambda _: item)
        # return the deferred instead the item. This makes the engine to
        # process next item (according to CONCURRENT_ITEMS setting) after this
        # operation (deferred) has finished.
        return item

    def _conditional_insert(self, cursor, item,spider):
        #print 'title:',item.get('title')
        #print spider.name
        if spider.name=='AnjukeSpider':
            #print "insert into cnblogs values ('%s', '%s','%s', '%s')" %(item['title'],  item['link'], item['desc'],item['listUrl'])
            cursor.execute(
                "insert into newhouses values ('%s', '%s','%s', '%s','%s','%s') "
                %(item['name'],  item['area'], item['price'],item['addr'],item['link'],item['tag'])
            )
        elif spider.name=='OldSpider':
            cursor.execute(
                "insert into oldhouses values ('%s', '%s','%s', '%s','%s','%s','%s','%s','%s')"
                %(item['name'],  item['area'], item['total_price'],item['unit_price'],item['type'],item['acreage'],item['build_in'],item['addr'],item['link'])
            )
    def handle_error(self, e):
        pass
        #print e
        #log.err(e)
