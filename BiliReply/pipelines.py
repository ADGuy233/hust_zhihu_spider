# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

DB_FILE = r'C:/Users/ti/Desktop/av412935552.db'

import sqlite3
from BiliReply import items

class BilireplyPipeline:
    def __init__(self):
        self.pool_Reply = []
        # 创建连接数据库的成员
        self.conn = None  # type: sqlite3.Connection
        self.cursor = None  # type: sqlite3.Cursor
        # 创建将Items写入数据库的成员
        self.sql_insert_Reply = '''INSERT OR IGNORE INTO Reply VALUES (:1, :2, :3, :4, :5, :6, :7, :8) '''
        self.sql_create_Reply = '''
            CREATE TABLE IF NOT EXISTS "Reply"(
            "rpid" INTEGER NOT NULL,
            "aid" INTEGER NOT NULL,
            "mid" INTEGER NOT NULL,
            "root" INTEGER,
            "reply_ctime" INTEGER,
            "reply_count" INTEGER,
            "reply_like" INTEGER,
            "content" TEXT,
            PRIMARY KEY ("rpid")
            );
            '''

    def open_spider(self, spider):
            try:
                self.conn = sqlite3.connect(DB_FILE)
                self.cursor = self.conn.cursor()
                self.cursor.execute(self.sql_create_Reply)
                print('db opened')
            except:
                print('[E] error open db')

    def close_spider(self, spider):

            if len(self.pool_Reply):
                try:
                    self.cursor.executemany(self.sql_insert_Reply, self.pool_Reply)
                    self.conn.commit()
                except Exception as e:
                    self.conn.rollback()
                    print(e)
                self.pool_Reply.clear()

    def process_item(self, item, spider):
            if isinstance(item, items.Reply):
                if 'rpid' not in item:
                    print('a blank Item')
                    return item
                else:
                    self.pool_Reply.append((
                        item['rpid'], item['aid'], item['mid'], item['root'], item['reply_ctime'], item['reply_count'],
                        item['reply_like'], item['content']
                    ))
                    if len(self.pool_Reply) < 10:
                        return item

                    try:
                        self.cursor.executemany(self.sql_insert_Reply, self.pool_Reply)
                        self.conn.commit()
                    except Exception as e:
                        self.conn.rollback()
                        print(e)
                    self.pool_Reply.clear()