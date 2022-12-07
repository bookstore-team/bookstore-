import jwt
import time
import logging
import sqlite3 as sqlite
from be.model import error
from be.model import db_conn
from be.model import store


#导入表信息
from be.model.init_database import User as Users
from be.model.init_database import User_store
from be.model.init_database import Store 
from be.model.init_database import New_order 
from be.model.init_database import New_order_detail 

# encode a json string like:
#   {
#       "user_id": [user name],
#       "terminal": [terminal code],
#       "timestamp": [ts]} to a JWT
#   }


def jwt_encode(user_id: str, terminal: str) -> str:
    encoded = jwt.encode(
        {"user_id": user_id, "terminal": terminal, "timestamp": time.time()},
        key=user_id,
        algorithm="HS256",
    )
    return encoded.encode("utf-8").decode("utf-8")


# decode a JWT to a json string like:
#   {
#       "user_id": [user name],
#       "terminal": [terminal code],
#       "timestamp": [ts]} to a JWT
#   }
def jwt_decode(encoded_token, user_id: str) -> str:
    decoded = jwt.decode(encoded_token, key=user_id, algorithms="HS256")
    return decoded


class User(db_conn.DBConn):
    token_lifetime: int = 3600  # 3600 second

    def __init__(self):
        db_conn.DBConn.__init__(self)

    def __check_token(self, user_id, db_token, token) -> bool:
        try:
            if db_token != token:
                return False
            jwt_text = jwt_decode(encoded_token=token, user_id=user_id)
            ts = jwt_text["timestamp"]
            if ts is not None:
                now = time.time()
                if self.token_lifetime > now - ts >= 0:
                    return True
        except jwt.exceptions.InvalidSignatureError as e:
            logging.error(str(e))
            return False

    def register(self, user_id: str, password: str):
        try:
            
            terminal = "terminal_{}".format(str(time.time()))
            token = jwt_encode(user_id, terminal)            
            #self.conn.execute(
            #    "INSERT into user(user_id, password, balance, token, terminal) "    #注册时插入数据
            #    "VALUES (?, ?, ?, ?, ?);",
            #    (user_id, password, 0, token, terminal), )
            #self.conn.commit()
        
            new_user=Users(user_id=user_id,password=password,balance=0,token=token,terminal=terminal)
            self.conn.add(new_user)
            self.conn.commit()
        
        #except sqlite.Error:
            #return error.error_exist_user_id(user_id)
        except BaseException as e:
            logging.info("530, {}".format(str(e)))
            return 530, "{}".format(str(e))
        return 200, "ok"

    def check_token(self, user_id: str, token: str):    # -> (int, str)
        #cursor = self.conn.execute("SELECT token from user where user_id=?", (user_id,))
        #row = cursor.fetchone()
        row=self.conn.query(Users.token).filter_by(user_id=user_id).first()
        if row is None:
            return error.error_authorization_fail()
        db_token = row.token
        if not self.__check_token(user_id, db_token, token):
            return error.error_authorization_fail()
        return 200, "ok"

    def check_password(self, user_id: str, password: str):  # -> (int, str)当与查找的user_id密码相同时返回正确
        #cursor = self.conn.execute("SELECT password from user where user_id=?", (user_id,))
        #row = cursor.fetchone()
        row=self.conn.query(Users.password).filter_by(user_id=user_id).first()
        if row is None:
            return error.error_authorization_fail()
        if password != row.password:
            return error.error_authorization_fail()
        return 200, "ok"

    def login(self, user_id: str, password: str, terminal: str):    #-> (int, str, str)
        token = ""
        try:
            code, message = self.check_password(user_id, password)
            if code != 200:
                return code, message, ""
            token = jwt_encode(user_id, terminal)
            #cursor = self.conn.execute(
            #    "UPDATE user set token= ? , terminal = ? where user_id = ?",
            #    (token, terminal, user_id), )
            cursor=self.conn.query(Users).filter_by(user_id=user_id).update({'token':token,'terminal':terminal})
            #if cursor.rowcount == 0:
            if cursor==0: 
                return error.error_authorization_fail() + ("", )
            #self.conn.commit()
            self.conn.commit()
        #except sqlite.Error as e:
        #    return 528, "{}".format(str(e)), ""
        except BaseException as e:
            return 530, "{}".format(str(e)), ""
        return 200, "ok", token

    def logout(self, user_id: str, token: str) -> bool:
        try:
            code, message = self.check_token(user_id, token)
            if code != 200:
                return code, message
            terminal = "terminal_{}".format(str(time.time())) #登出时更新该用户的terminal和token
            dummy_token = jwt_encode(user_id, terminal)
            #cursor = self.conn.execute(
            #    "UPDATE user SET token = ?, terminal = ? WHERE user_id=?",
            #    (dummy_token, terminal, user_id), )
            cursor=self.conn.query(Users).filter_by(user_id=user_id).update({'token':dummy_token,'terminal':terminal})
            #if cursor.rowcount == 0:
            if cursor==0:
                return error.error_authorization_fail()
            #self.conn.commit()
            self.conn.commit()
        #except sqlite.Error as e:
        #    return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def unregister(self, user_id: str, password: str):      # -> (int, str)
        try:
            code, message = self.check_password(user_id, password)
            if code != 200:
                return code, message
            #cursor = self.conn.execute("DELETE from user where user_id=?", (user_id,))  #注销用户
            #####
            cursor=self.conn.query(Users).filter_by(user_id=user_id).first()

            # #if cursor.rowcount == 1:
            # #    self.conn.commit()
            # else:
            #     return error.error_authorization_fail()
            if cursor is None:
                return error.error_authorization_fail()
            else:
                self.conn.delete(cursor)
                self.conn.commit()

        #except sqlite.Error as e:
        #    return 528, "{}".format(str(e))
        except BaseException as e:
            print(e)
            return 530, "{}".format(str(e))
        return 200, "ok"


    def change_password(self, user_id: str, old_password: str, new_password: str):  # -> bool
        try:
            code, message = self.check_password(user_id, old_password)
            if code != 200:
                return code, message
            terminal = "terminal_{}".format(str(time.time()))
            token = jwt_encode(user_id, terminal)
            #cursor = self.conn.execute(
            #    "UPDATE user set password = ?, token= ? , terminal = ? where user_id = ?",      
            #    (new_password, token, terminal, user_id), )
            
            # cursor=self.conn.query(Users).filter_by(user_id=user_id).update({'password':new_password,'token':token})
            # #if cursor.rowcount == 0:
            #     return error.error_authorization_fail()
            # self.conn.commit()
            cursor=self.conn.query(Users).filter_by(user_id=user_id).first()
            if cursor is None:
                return error.error_authorization_fail() 
            cursor=self.conn.query(Users).filter_by(user_id=user_id).update({'password':new_password,'token':token}) 
            self.conn.commit()
        #except sqlite.Error as e:
        #    return 528, "{}".format(str(e))
    
        except BaseException as e:
            print(e)
            return 530, "{}".format(str(e))
        return 200, "ok"

    ###lsq:精确搜索书名
    def search_title(self, search_key:str,store_id:str):
        try:
            #全站搜索
            if store_id is None:
                row=self.conn.query(Store).filter_by(title=search_key).all()
                if len(row)==0: #没有找到与输入的书名匹配的书籍
                    return error.error_non_exist_book(search_key) #524
                else:
                    result_store=[] #存储售卖该书的商店
                    for i in row:
                        result_store.append(i.store_id)
            #店铺内搜索
            else:
                row=self.conn.query(Store).filter_by(title=search_key,store_id=store_id).all()
                if len(row)==0: #没有找到与输入的书名匹配的书籍
                    return error.error_non_exist_book(search_key) #524
            self.conn.commit()
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    ###lsq:精确搜索作者
    def search_author(self, search_key:str, store_id:str):
        try:
            #全站搜索
            if store_id is None:
                row=self.conn.query(Store).filter_by(author=search_key).all()
                if len(row)==0: #没有找到输入的作者作品
                    return error.error_non_exist_author(search_key)
                else:
                    result_store=[] #存储售卖该作者作品的书店
                    for i in row:
                        result_store.append(i.store_id)
            #店铺内搜索
            else:
                row=self.conn.query(Store).filter_by(author=search_key,store_id=store_id).all()
                if len(row)==0: #没有找到输入的作者作品
                    return error.error_non_exist_author(search_key)
            self.conn.commit()
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"
