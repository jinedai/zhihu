# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from zhihu.myconfig import DbConfig

class UserPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(user = DbConfig['user'], passwd = DbConfig['passwd'], db = DbConfig['db'], host = DbConfig['host'], charset = 'utf8', use_unicode = True)
        self.cursor = self.conn.cursor()
        # self.cursor.execute('truncate table weather;')
        # self.conn.commit()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """INSERT IGNORE INTO user (url, name, location, gender, avatar, create_at)
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (
                    item['url'],
                    item['name'],
                    item['location'],
                    item['gender'],
                    item['avatar'],
                    item['timestamp']
                )
            )
            self.conn.commit()
            print 'bbbbbbbbbbbbbbbbb'
        except MySQLdb.Error, e:
            print 'Error %d %s' % (e.args[0], e.args[1])

        return item
