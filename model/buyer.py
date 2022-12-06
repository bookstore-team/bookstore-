import sqlite3 as sqlite
import uuid
import json
import logging
from be.model import db_conn
from be.model import error
import time

class Buyer(db_conn.DBConn):
    def __init__(self):
        db_conn.DBConn.__init__(self)

    def new_order(self, user_id: str, store_id: str, id_and_count: [(str, int)]) -> (int, str, str):
        order_id = ""
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id) + (order_id, )
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id) + (order_id, )
            uid = "{}_{}_{}".format(user_id, store_id, str(uuid.uuid1()))
            
            t_price=0   ####

            for book_id, count in id_and_count:
                cursor = self.conn.execute(
                    "SELECT book_id, stock_level, book_info FROM store "
                    "WHERE store_id = ? AND book_id = ?;",
                    (store_id, book_id))
                row = cursor.fetchone()
                if row is None:
                    return error.error_non_exist_book_id(book_id) + (order_id, )

                stock_level = row[1]
                book_info = row[2]
                book_info_json = json.loads(book_info)
                price = book_info_json.get("price")
                t_price+=count*price  ####
                if stock_level < count:
                    return error.error_stock_level_low(book_id) + (order_id,)

                cursor = self.conn.execute(
                    "UPDATE store set stock_level = stock_level - ? "
                    "WHERE store_id = ? and book_id = ? and stock_level >= ?; ",
                    (count, store_id, book_id, count))
                if cursor.rowcount == 0:
                    return error.error_stock_level_low(book_id) + (order_id, )

                self.conn.execute(
                        "INSERT INTO new_order_detail(order_id, book_id, count, price) "
                        "VALUES(?, ?, ?, ?);",
                        (uid, book_id, count, price))

            self.conn.execute(
                "INSERT INTO new_order(order_id,user_id,store_id,order_status,total_price,time) "
                "VALUES(?,?,?,?,?,?);",
                (uid, user_id, store_id, 0,t_price,time.time()))
            self.conn.commit()
            order_id = uid
        except sqlite.Error as e:
            logging.info("528, {}".format(str(e)))
            return 528, "{}".format(str(e)), ""
        except BaseException as e:
            logging.info("530, {}".format(str(e)))
            return 530, "{}".format(str(e)), ""
        return 200, "ok", order_id

    def payment(self, user_id: str, password: str, order_id: str) -> (int, str):
        conn = self.conn
        try:
            cursor = conn.execute("SELECT order_id, user_id, store_id, order_status,total_price FROM new_order WHERE order_id = ?", (order_id,)) ####CBY
            row = cursor.fetchone()
            if row is None:
                return error.error_invalid_order_id(order_id)

            order_id = row[0]
            buyer_id = row[1]
            store_id = row[2]
            order_status=row[3] ####CBY
            total_price=row[4]  ####CBY

            if buyer_id != user_id:
                return error.error_authorization_fail()

            if order_status!=0: #若已经付过款返回错误####CBY 
               return error.error_invalid_order_id(order_id) 

            ##买家
            cursor = conn.execute("SELECT balance, password FROM user WHERE user_id = ?;", (buyer_id,))
            row = cursor.fetchone()
            if row is None:
                return error.error_non_exist_user_id(buyer_id)
            balance = row[0]
            if password != row[1]:
                return error.error_authorization_fail()

            #卖家
            cursor = conn.execute("SELECT store_id, user_id FROM user_store WHERE store_id = ?;", (store_id,))
            row = cursor.fetchone()
            if row is None:
                return error.error_non_exist_store_id(store_id)
            seller_id = row[1]
            if not self.user_id_exist(seller_id):
                return error.error_non_exist_user_id(seller_id)

            ####CBY 
            # cursor = conn.execute("SELECT book_id, count, price FROM new_order_detail WHERE order_id = ?;", (order_id,))
            # total_price = 0
            # for row in cursor:
            #     count = row[1]
            #     price = row[2]
            #     total_price = total_price + price * count

            if balance < total_price:   #钱不够
                return error.error_not_sufficient_funds(order_id)
            # 买家付钱，钱减少
            cursor = conn.execute("UPDATE user set balance = balance - ?"
                                  "WHERE user_id = ? AND balance >= ?",
                                  (total_price, buyer_id, total_price))
            if cursor.rowcount == 0:
                return error.error_not_sufficient_funds(order_id)
            # 卖家收钱，钱增多
            cursor = conn.execute("UPDATE user set balance = balance + ?"
                                  "WHERE user_id = ?",
                                  (total_price, seller_id))
            if cursor.rowcount == 0:
                return error.error_non_exist_user_id(seller_id)

            # 将记录的state改为1，表示已付款 ####CBY
            cursor = conn.execute("UPDATE new_order set order_status = ?"
                                  "WHERE order_id = ?",
                                  (1, order_id)) 
            # cursor = conn.execute("DELETE FROM new_order WHERE order_id = ?", (order_id, ))
            if cursor.rowcount == 0:
                return error.error_invalid_order_id(order_id)

            # cursor = conn.execute("DELETE FROM new_order_detail where order_id = ?", (order_id, ))
            # if cursor.rowcount == 0:
            #     return error.error_invalid_order_id(order_id)
            conn.commit()

        except sqlite.Error as e:
            return 528, "{}".format(str(e))

        except BaseException as e:
            return 530, "{}".format(str(e))

        return 200, "ok"

    def add_funds(self, user_id, password, add_value) -> (int, str):
        try:
            cursor = self.conn.execute("SELECT password  from user where user_id=?", (user_id,))
            row = cursor.fetchone()
            if row is None:
                return error.error_authorization_fail()

            if row[0] != password:
                return error.error_authorization_fail()

            cursor = self.conn.execute(
                "UPDATE user SET balance = balance + ? WHERE user_id = ?",
                (add_value, user_id))
            if cursor.rowcount == 0:
                return error.error_non_exist_user_id(user_id)

            self.conn.commit()
        except sqlite.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))

        return 200, "ok"

#买家确认收货   ####CBY
    def receive_stock(self, user_id: str, password: str, order_id: str):    # -> (int, str)
        try:
            #先验证用户密码
            cursor = self.conn.execute("SELECT password  from user where user_id=?", (user_id,))
            row = cursor.fetchone()
            if row is None:
                return error.error_authorization_fail()
            if row[0] != password:
                return error.error_authorization_fail()

            #查找订单状态
            cursor = self.conn.execute("SELECT order_status from new_order where order_id=?", (order_id,))
            row = cursor.fetchone()
            if row is None:
                return error.error_invalid_order_id(order_id)
            if row[0] != 2:
                return error.error_order_not_received(order_id)

            #更新订单状态为3 收货
            cursor = self.conn.execute("UPDATE new_order set order_status = ?"
                                  "WHERE order_id = ?",
                                  (3, order_id))            
            if cursor.rowcount == 0:
                return error.error_non_exist_user_id(user_id)

            self.conn.commit()
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"


   