import logging
import os
import jieba
import numpy as np
import sqlite3 as sqlite


class Store:
    database: str

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
            # search
            conn.execute(
                "CREATE TABLE IF NOT EXISTS new_search( "
                "user_id TEXT, store_id TEXT, book_id TEXT, count INTEGER NOT NULL, price INTEGER NOT NULL, "
                "PRIMARY KEY(order_id, book_id))"
            )
            
            conn.commit()

        except sqlite.Error as e:
            logging.error(e)
            conn.rollback()

    def get_db_conn(self) -> sqlite.Connection: #该函数返回的值为sqlite.Connection
        return sqlite.connect(self.database)


database_instance: Store = None


def init_database(db_path):
    global database_instance
    database_instance = Store(db_path)


def get_db_conn():
    global database_instance
    return database_instance.get_db_conn()

# 不知道是不是还要加一段