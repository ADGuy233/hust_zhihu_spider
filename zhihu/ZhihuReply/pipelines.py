
import sqlite3
from ZhihuReply import items

file_path = r"C:\Users\ti\OneDrive\论文硕士\知乎豆瓣\Spiders\Data\Replies\ZhihuEssence.db"

class ZhihuPipeline:
    def __init__(self):
        # 创建内容池，临时储存待写入数据库的Items
        self.pool_Question = []
        self.pool_Answer = []
        self.pool_Comment = []
        self.pool_ChildComment = []
        self.pool_Topic = []
        # 创建连接数据库的连接与游标
        self.conn = None  # type: sqlite3.Connection
        self.cursor = None  # type: sqlite3.Cursor
        # 创建将Items写入数据库的sql
        self.sql_insert_Question = '''INSERT OR IGNORE INTO Question VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10)'''
        self.sql_insert_Answer = '''INSERT OR IGNORE INTO Answer VALUES (:1, :2, :3, :4, :5, :6, :7, :8)'''
        self.sql_insert_Comment = '''INSERT OR IGNORE INTO Comment VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)'''
        self.sql_insert_ChildComment = '''INSERT OR IGNORE INTO ChildComment VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)'''
        self.sql_insert_Topic = '''INSERT OR IGNORE INTO Topic VALUES (:1, :2, :3, :4, :5, :6)'''
        # 创建数据库各表
        self.sql_create_Question = '''
            CREATE TABLE IF NOT EXISTS "Question"(
            "qid" INTEGER NOT NULL,
            "title" TEXT,
            "author" TEXT,
            "name" TEXT,
            "created" INTEGER,
            "topic_list" TEXT,
            "follow" INTEGER,
            "view" INTEGER,
            "good_question" INTEGER,
            "comment" INTEGER,
            PRIMARY KEY ("qid")
            );
            '''
        self.sql_create_Answer = '''
            CREATE TABLE IF NOT EXISTS "Answer"(
            "aid" INTEGER NOT NULL,
            "qid" INTEGER,
            "updated_time" INTEGER,
            "author" TEXT,
            "name" TEXT,
            "content" TEXT,
            "voteup_count" INTEGER,
            "comment_count" INTEGER,
            PRIMARY KEY ("aid")
            );
            '''
        self.sql_create_Comment = '''
            CREATE TABLE IF NOT EXISTS "Comment"(
            "cid" INTEGER NOT NULL,
            "aid" INTEGER,
            "qid" INTEGER,
            "root_comment" INTEGER,
            "created_time" INTEGER,
            "author" TEXT,
            "name" TEXT,
            "content" TEXT,
            "voteup_count" INTEGER,
            "comment_count" INTEGER,
            "featured" INTEGER,
            PRIMARY KEY ("cid")
            );
            '''
        self.sql_create_ChildComment = '''
            CREATE TABLE IF NOT EXISTS "ChildComment"(
            "cid" INTEGER NOT NULL,
            "aid" INTEGER,
            "qid" INTEGER,
            "root_comment" INTEGER,
            "created_time" INTEGER,
            "author" TEXT,
            "name" TEXT,
            "content" TEXT,
            "voteup_count" INTEGER,
            "comment_count" INTEGER,
            "reply_to_author" TEXT,
            PRIMARY KEY ("cid")
            );
            '''
        self.sql_create_Topic = '''
            CREATE TABLE IF NOT EXISTS "Topic"(
            "tid" INTEGER NOT NULL,
            "name" TEXT,
            "questions_count" INTEGER,
            "introduction" TEXT,
            "followers_count" INTEGER,
            "best_answers_count" INTEGER,
            PRIMARY KEY ("tid")
            );
            '''
    def open_spider(self, spider):
        try:
            self.conn = sqlite3.connect(file_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute(self.sql_create_Question)
            self.cursor.execute(self.sql_create_Answer)
            self.cursor.execute(self.sql_create_Comment)
            self.cursor.execute(self.sql_create_ChildComment)
            self.cursor.execute(self.sql_create_Topic)
            print('db opened')
        except:
             print('[E] error open db')

    def close_spider(self, spider):
        if len(self.pool_Question):
            self.cursor.executemany(self.sql_insert_Question, self.pool_Question)
            self.conn.commit()
            self.pool_Question.clear()

        if len(self.pool_Answer):
            self.cursor.executemany(self.sql_insert_Answer, self.pool_Answer)
            self.conn.commit()
            self.pool_Answer.clear()

        if len(self.pool_Comment):
            self.cursor.executemany(self.sql_insert_Comment, self.pool_Comment)
            self.conn.commit()
            self.pool_Comment.clear()

        if len(self.pool_ChildComment):
            self.cursor.executemany(self.sql_insert_ChildComment, self.pool_ChildComment)
            self.conn.commit()
            self.pool_ChildComment.clear()

        if len(self.pool_Topic):
            self.cursor.executemany(self.sql_insert_Topic, self.pool_Topic)
            self.conn.commit()
            self.pool_Topic.clear()

    def process_item(self, item, spider):

        if isinstance(item, items.Question):
            if 'qid' not in item:
                print('a blank Item')
                return item
            else:
                self.pool_Question.append((
                    item['qid'], item['title'], item['author'], item['name'], item['created'], item['topic_list'],
                item['follow'], item['view'], item['good_question'], item['comment']
                ))
                if len(self.pool_Question) < 1:
                    return item
                self.cursor.executemany(self.sql_insert_Question, self.pool_Question)
                self.conn.commit()
                self.pool_Question.clear()

        if isinstance(item, items.Answer):
            if 'aid' not in item:
                print('a blank Item')
                return item
            else:
                self.pool_Answer.append((
                    item['aid'], item['qid'], item['updated_time'], item['author'], item['name'], item['content'],
                    item['voteup_count'], item['comment_count']
                ))
                if len(self.pool_Answer) < 10:
                    return item
                self.cursor.executemany(self.sql_insert_Answer, self.pool_Answer)
                self.conn.commit()
                self.pool_Answer.clear()

        if isinstance(item, items.Comment):
            if 'cid' not in item:
                print('a blank Item')
                return item
            else:
                self.pool_Comment.append((
                    item['cid'], item['aid'], item['qid'], item['root_comment'], item['created_time'], item['author'], item['name'],
                    item['content'], item['voteup_count'], item['comment_count'], item['featured']
                ))
                if len(self.pool_Comment) < 10:
                    return item
                self.cursor.executemany(self.sql_insert_Comment, self.pool_Comment)
                self.conn.commit()
                self.pool_Comment.clear()

        if isinstance(item, items.ChildComment):
            if 'cid' not in item:
                print('a blank Item')
                return item
            else:
                self.pool_ChildComment.append((
                    item['cid'], item['aid'], item['qid'], item['root_comment'], item['created_time'], item['author'], item['name'],
                    item['content'], item['voteup_count'], item['comment_count'], item['reply_to_author']
                ))
                if len(self.pool_ChildComment) < 10:
                    return item
                self.cursor.executemany(self.sql_insert_ChildComment, self.pool_ChildComment)
                self.conn.commit()
                self.pool_ChildComment.clear()

        if isinstance(item, items.Topic):
            if 'tid' not in item:
                print('a blank Item')
                return item
            else:
                self.pool_Topic.append((
                    item['tid'], item['name'], item['questions_count'], item['introduction'], item['followers_count'], item['best_answers_count']
                ))
                if len(self.pool_Topic) < 1:
                    return item
                self.cursor.executemany(self.sql_insert_Topic, self.pool_Topic)
                self.conn.commit()
                self.pool_Topic.clear()

        return item
        
        
