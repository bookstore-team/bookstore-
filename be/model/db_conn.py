from be.model import store
from be.model.init_database import User
from be.model.init_database import User_store
from be.model.init_database import Store 
import sqlalchemy
import psycopg2
from sqlalchemy import create_engine, Column, Text, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker # 创建会话
from sqlalchemy import and_,or_
from sqlalchemy.ext.declarative import declarative_base  # 创建表
# from be.model.init_database import DbSession 


class DBConn:
    def __init__(self):
        #engine = create_engine('postgresql://postgres:mbyc020905@localhost:5432/books')
        engine=create_engine("postgresql://postgres:lisiqi20020521@localhost:5432/bookstore")
        # 创建session
        DbSession = sessionmaker(bind=engine)
        self.conn = DbSession()

    def user_id_exist(self, user_id):
        # cursor = self.conn.execute("SELECT user_id FROM user WHERE user_id = ?;", (user_id,))
        # row = cursor.fetchone()
        row = self.conn.query(User).filter(User.user_id == user_id).first()
        if row is None:
            return False
        else:
            return True

    def book_id_exist(self, store_id, book_id):
        # cursor = self.conn.execute("SELECT book_id FROM store WHERE store_id = ? AND book_id = ?;", (store_id, book_id))
        # row = cursor.fetchone()
        row = self.conn.query(Store).filter(Store.store_id == store_id, Store.book_id == book_id).first()
        if row is None:
            return False
        else:
            return True

    def store_id_exist(self, store_id):
        # cursor = self.conn.execute("SELECT store_id FROM user_store WHERE store_id = ?;", (store_id,))
        # row = cursor.fetchone()
        row = self.conn.query(User_store).filter(User_store.store_id == store_id).first()
        if row is None:
            return False
        else:
            return True
