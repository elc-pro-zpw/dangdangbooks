# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from dangdang.settings import *
import logging

logger = logging.getLogger(__name__)

class DangdangPipeline(object):
    def __init__(self,sql_uri,user,password,db,port):
        self.sql_uri = sql_uri
        self.user = user
        self.password = password
        self.db = db
        self.port = port

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
                sql_uri=crawler.settings.get('SQL_URI'),
                user=crawler.settings.get('USER'),
                password=crawler.settings.get('PASSWORD'),  #setttings中所以得参数变量都必须要大写，不然不生效
                db=crawler.settings.get('DB'),
                port=crawler.settings.get('PORT')
                )

    def open_spider(self,spider):
        self.conn = pymysql.connect(host=self.sql_uri,port=self.port,user=self.user,password=self.password,db=self.db,charset='utf8')
        self.cursor = self.conn.cursor()
        self.sql = 'insert into books(name,link,comment,price,satisfaction,kind) values(%s,%s,%s,%s,%s,%s)'

    def process_item(self, item, spider):
        price = float(item['price'].replace('¥',''))
        satisfaction = item['satisfaction'].replace('推荐','')
        comment = int(item['comment'].replace('条评论',''))
        values = [item['name'],item['link'],comment,price,satisfaction,item['kind']]
        try:
            self.cursor.execute(self.sql,values)
        except Exception as er: 
            self.conn.rollback()
            logger.error(er)
        else:
            self.conn.commit()
        return item

    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()


