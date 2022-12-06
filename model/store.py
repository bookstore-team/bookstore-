import sqlite3 as sqlite
import pandas as pd
# import jieba
import logging
import os
import numpy as np
import psycopg2
import datetime, time

class Store:
    database: str
    # def __init__(self):
    #     self.host = 'dase-cdms-2022-pub.pg.rds.aliyuncs.com'
    # self.port = '5432'
    # self.user = 'stu10205501435'
    # self.password = 'Stu10205501435'
    # self.database = 'stu10205501435'
    # self.init_tables()
    
    # def fetch_all_db(self):
    #     conn = self.get_db_conn()
    # sql = 'select current_database();'
    # # 执行SQL
    # conn.execute(sql)
    # # SQL执行后，会将结果以元组的形式缓存在cursor中，使用下述语句输出
    # for tuple in conn.fetchall():
    #     print(tuple)
        
        
    def __init__(self, db_path):
        self.database = os.path.join(db_path, "be.db")
        self.init_tables()

    def init_tables(self):
        try:
            conn = self.get_db_conn()
            conn.execute(
                "CREATE TABLE IF NOT EXISTS user ("
                "user_id TEXT PRIMARY KEY, password TEXT NOT NULL, "
                "balance INTEGER NOT NULL, token TEXT, terminal TEXT);"
            )

            conn.execute(
                "CREATE TABLE IF NOT EXISTS user_store("
                "user_id TEXT, store_id TEXT, PRIMARY KEY(user_id, store_id));"
            )

            conn.execute(
                "CREATE TABLE IF NOT EXISTS store( "
                "store_id TEXT, book_id TEXT, book_info TEXT, stock_level INTEGER,title TEXT,tag TEXT,author TEXT,content TEXT,book_price INTEGER NOT NULL,"
                " PRIMARY KEY(store_id, book_id))"
            )
 # status 0:未付款 1:已付款 2：已发货 3：已收货
            conn.execute(
                "CREATE TABLE IF NOT EXISTS new_order( "
                "order_id TEXT PRIMARY KEY, user_id TEXT, store_id TEXT, order_status INTEGER, total_price INTEGER,time INTEGER)"
            )

            conn.execute(
                "CREATE TABLE IF NOT EXISTS new_order_detail( "
                "order_id TEXT, book_id TEXT, count INTEGER NOT NULL, price INTEGER NOT NULL, "
                "PRIMARY KEY(order_id, book_id))"
            )
            
            
            conn.commit()
            
# ——————————————————————————————————————————————————————————————————————————————————
            # sql = "select * from Book"
            # conn.execute(sql)
            # if not conn.fetchall():
            #     f = open("../fe/data/book.csv", encoding="utf-8")
            #     values = pd.read_csv(f)
            #     f.close()
            #     s_content = values.iloc[:, 14]
            #     v_content = []
            #     for i in range(len(s_content)):
            #         vector = ''
            #         seg_list = jieba.cut(str(s_content[i]))
            #         for s in seg_list:
            #             vector += s
            #             vector += ' '
                #     v_content.append(vector)
                # v_content = np.array(v_content)
                # values['v_content'] = v_content
                # values = values.values
                # sql = "insert into Book(book_id, title, author, publisher, original_title, translator, pub_year , " \
                #       "pages, price ," \
                #       "currency_unit ,binding,isbn ,author_intro,book_intro ,content ,tags, picture, v_content) values (%s,%s, %s, %s, " \
                #       "%s, %s,%s, %s, %s, " \
                #       "%s, %s,%s, %s, %s, %s, %s, %s, %s) "
                # conn.executemany(sql, values)
                # conn.execute("alter table Book add column tscontent tsvector;")
                # conn.execute("update Book set tscontent=to_tsvector('simple', v_content);")
                
# ——————————————————————————————————————————————————————————————————————————————————

        except sqlite.Error as e:
            logging.error(e)
            conn.rollback()

    def get_db_conn(self) -> sqlite.Connection: 
        return sqlite.connect(self.database)


database_instance: Store = None


def init_database(db_path):
    global database_instance
    database_instance = Store(db_path)


def get_db_conn():
    global database_instance
    return database_instance.get_db_conn()

