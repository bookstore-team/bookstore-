import jwt
import time
import logging
import psycopg2
import sqlite3 as sqlite
from be.model import error
from be.model import db_conn
from be.model import user
# encode a json string like:
# {
#       "user_id": [user name],
#       "terminal": [terminal code],
#       "timestamp": [ts] to a JWT
# }
# decode a JWT to a json string like:
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
            self.conn.execute(
                "INSERT into user(user_id, password, balance, token, terminal) "    #注册时插入数据
                "VALUES (?, ?, ?, ?, ?);",
                (user_id, password, 0, token, terminal), )
            self.conn.commit()
        except sqlite.Error:
            return error.error_exist_user_id(user_id)
        return 200, "ok"

    def check_token(self, user_id: str, token: str):    # -> (int, str)
        cursor = self.conn.execute("SELECT token from user where user_id=?", (user_id,))
        row = cursor.fetchone()
        if row is None:
            return error.error_authorization_fail()
        db_token = row[0]
        if not self.__check_token(user_id, db_token, token):
            return error.error_authorization_fail()
        return 200, "ok"

    def check_password(self, user_id: str, password: str):  # -> (int, str)当与查找的user_id密码相同时返回正确
        cursor = self.conn.execute("SELECT password from user where user_id=?", (user_id,))
        row = cursor.fetchone()
        if row is None:
            return error.error_authorization_fail()
        if password != row[0]:
            return error.error_authorization_fail()
        return 200, "ok"

    def login(self, user_id: str, password: str, terminal: str):    #-> (int, str, str)
        token = ""
        try:
            code, message = self.check_password(user_id, password)
            if code != 200:
                return code, message, ""
            token = jwt_encode(user_id, terminal)
            cursor = self.conn.execute(
                "UPDATE user set token= ? , terminal = ? where user_id = ?",
                (token, terminal, user_id), )
            if cursor.rowcount == 0:
                return error.error_authorization_fail() + ("", )
            self.conn.commit()
        except sqlite.Error as e:
            return 528, "{}".format(str(e)), ""
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
            cursor = self.conn.execute(
                "UPDATE user SET token = ?, terminal = ? WHERE user_id=?",
                (dummy_token, terminal, user_id), )
            if cursor.rowcount == 0:
                return error.error_authorization_fail()
            self.conn.commit()
        except sqlite.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def unregister(self, user_id: str, password: str):      # -> (int, str)
        try:
            code, message = self.check_password(user_id, password)
            if code != 200:
                return code, message
            cursor = self.conn.execute("DELETE from user where user_id=?", (user_id,))  #注销用户
            if cursor.rowcount == 1:
                self.conn.commit()
            else:
                return error.error_authorization_fail()
        except sqlite.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def change_password(self, user_id: str, old_password: str, new_password: str):  # -> bool
        try:
            code, message = self.check_password(user_id, old_password)
            if code != 200:
                return code, message
            terminal = "terminal_{}".format(str(time.time()))
            token = jwt_encode(user_id, terminal)
            cursor = self.conn.execute(
                "UPDATE user set password = ?, token= ? , terminal = ? where user_id = ?",      
                (new_password, token, terminal, user_id), )
            if cursor.rowcount == 0:
                return error.error_authorization_fail()
            self.conn.commit()
        except sqlite.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"
    
    # yh
    # 模糊查询
    def params_search(self, title: str, author: str, tag: str, store_id: str):
        flag = (title is None) & (author is None) & (tag is None) & (store_id is None)
        have_restrict = 0
        try:
            values = []
            if flag == 1:
                sql = "select title from store"
            else:
                sql = "select title from store where"

            if store_id is not None:
                sql += " book_id in (select book_id from store where store_id = ?)"
                values.append(store_id)
                have_restrict = 1

            if title is not None:
                if have_restrict == 0:
                    sql += " title = ?"
                else:
                    sql += " and title = ?"
                values.append(title)
                have_restrict = 1

            if author is not None:
                if have_restrict == 0:
                    sql += " author = ?"
                else:
                    sql += " and author = ?"
                values.append(author)
                have_restrict = 1

            if tag is not None:
                if have_restrict == 0:
                    sql += " tag like ?"
                else:
                    sql += " and tag like ?"
                values.append("%" + tag + "%")

            if store_id is not None:
                if not self.store_id_exist(store_id):
                    return error.error_non_exist_store_id(store_id)
                else:
                    self.conn.execute(sql, values)
            else:
                self.conn.execute(sql, values)
        except sqlite.Error as e:
            print(sql)
            print(e)
            return 528, "{}".format(str(e))
        except BaseException as e:
            print(e)
            return 530, "{}".format(str(e))
        return 200, "ok"

    # def whole_content_search(self, content: str, store_id=None):
    #     try:
    #         if store_id is None:
    #             self.conn.execute("select book_id from store where tscontent @@ to_tsquery('%s');"%content)
    #         else:
    #             if not self.store_id_exist(store_id):
    #                 return error.error_non_exist_store_id(store_id)
    #             else:
    #                 sql = "select book_id from store where tscontent @@ to_tsquery('simple', ?) and book_id in (select book_id from store where store_id = ?);"
    #                 self.conn.execute(sql, (content, store_id))
    #     except sqlite.Error as e:
    #         return 528, "{}".format(str(e))
    #     except BaseException as e:
    #         print(e)
    #         return 530, "{}".format(str(e))
    #     return 200, "ok"