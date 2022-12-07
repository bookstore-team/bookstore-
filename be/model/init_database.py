import sqlalchemy
import psycopg2
from sqlalchemy import create_engine, Column, Text, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, scoped_session  # 创建会话
from sqlalchemy.ext.declarative import declarative_base  # 创建表
import time
# 创建引擎,初始化数据库连接:
#url = 'postgresql://{}:{}@{}:{}/{}'
#url = url.format(user, password, host, port, db)
engine=create_engine("postgresql://postgres:lisiqi20020521@localhost:5432/bookstore")
# 用户名:密码@localhost:端口/数据库名
#engine = create_engine('postgresql://postgres:mbyc020905@localhost:5432/books')
# # 创建session
# Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# # 默认session进行查询之前会自动把当前累计的修改发送到数据库且默认自动commit；此处为了事务处理，将其改为false
# DbSession = scoped_session(Session)
# session = DbSession()

# 创建对象的基类:
Base = declarative_base()

#user表
class User(Base):
    #表名
    __tablename__="user"

    #表的结构
    user_id= Column(Text,primary_key=True,unique=True,nullable=False)
    password=Column(Text,nullable=False)
    balance=Column(Integer,nullable=False)
    token=Column(Text,nullable=False)
    terminal=Column(Text,nullable=False)


#store表
class Store(Base):
    #表名
    __tablename__="store"

    #表的结构
    store_id=Column(Text, primary_key=True,nullable=False)
    book_id=Column(Text, primary_key=True,nullable=False)
    book_info=Column(Text)
    stock_level=Column(Integer,nullable=False)
    title=Column(Text)
    tag=Column(Text)
    author=Column(Text)
    content=Column(Text)
    book_price=Column(Integer)

#user_store表
class User_store(Base):
    __tablename__="user_store"

    user_id=Column(Text, primary_key=True)
    store_id=Column(Text, primary_key=True)

#new_order表
class New_order(Base):
    __tablename__="new_order"

    order_id=Column(Text,primary_key=True,nullable=False)
    user_id=Column(Text,nullable=False)
    store_id=Column(Text,nullable=False)
    order_status=Column(Integer,nullable=False)
    total_price=Column(Integer)
    time=Column(Integer,nullable=False)

#new_order_detail表
class New_order_detail(Base):
    __tablename__="new_order_detail"

    order_id=Column(Text,primary_key=True,nullable=False)
    book_id=Column(Text,primary_key=True,nullable=False)
    count=Column(Integer,nullable=False)
    price=Column(Integer)

if __name__ == "__main__":
    # 删除表
    Base.metadata.drop_all(engine)
    # 创建表
    Base.metadata.create_all(engine)
