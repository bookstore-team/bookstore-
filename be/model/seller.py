import sqlite3 as sqlite
from be.model import error
from be.model import db_conn


class Seller(db_conn.DBConn):

    def __init__(self):
        db_conn.DBConn.__init__(self)

    def add_book(self, user_id: str, store_id: str, book_id: str, book_json_str: str, stock_level: int, title: str,
                 author: str, content: str, tag: str,book_price:int):#向store中添加书
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if self.book_id_exist(store_id, book_id):
                return error.error_exist_book_id(book_id)

            self.conn.execute("INSERT into store(store_id, book_id, book_info, stock_level,title,tag,author,content,book_price)"
                              "VALUES (?,?,?,?,?,?,?,?,?)", (store_id, book_id, book_json_str, stock_level,title,tag,author,content,book_price))
            self.conn.commit()
        except sqlite.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def add_stock_level(self, user_id: str, store_id: str, book_id: str, add_stock_level: int):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if not self.book_id_exist(store_id, book_id):
                return error.error_non_exist_book_id(book_id)

            self.conn.execute("UPDATE store SET stock_level = stock_level + ? "
                              "WHERE store_id = ? AND book_id = ?", (add_stock_level, store_id, book_id))
            self.conn.commit()
        except sqlite.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def create_store(self, user_id: str, store_id: str):       #-> (int, str)
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if self.store_id_exist(store_id):
                return error.error_exist_store_id(store_id)
            self.conn.execute("INSERT into user_store(store_id, user_id)"
                              "VALUES (?, ?)", (store_id, user_id))
            self.conn.commit()
        except sqlite.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def send_stock(self, user_id: str, order_id: str):  # -> (int, str) #发货#####CBY
        try:
            #先验证订单存在、用户存在
            cursor = self.conn.execute("SELECT user_id,order_id  from new_order where order_id=?", (order_id,))
            row = cursor.fetchone()
            if row is None:
                return error.error_invalid_order_id()

            #查找订单状态
            cursor = self.conn.execute("SELECT order_status from new_order where order_id=?", (order_id,))
            row = cursor.fetchone()
            if row is None:
                return error.error_invalid_order_id(order_id)
            if row[0] != 1:
                return error.error_order_not_dispatched(order_id)
            
            #更新订单状态为2 发货
            cursor = self.conn.execute("UPDATE new_order set order_status = ?"
                                  "WHERE order_id = ?",
                                  (2, order_id))            
            if cursor.rowcount == 0:
                return error.error_non_exist_user_id(user_id)
                
            self.conn.commit()
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"
