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

#买家查询订单信息   ####CBY
    def search_orders (self , user_id : str , password : str):  #-> (int,str)
        try:
            #先验证用户信息与密码
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            cursor = self.conn.execute("SELECT password from user where user_id=?", (user_id,))
            row = cursor.fetchone()
            if row is None:
                return error.error_authorization_fail()
            if row[0] != password:
                return error.error_authorization_fail()

            #根据user_id搜索订单
            cursor = self.conn.execute("SELECT order_id,order_status from new_order where user_id=?", (user_id,))
            rows = cursor.fetchall() #((order_id,order_status),(order_id,order_status),...(order_id,order_status))             
            if rows is None :#没有查询到任何订单，报错
                return error.error_non_exist_order_id(user_id)
            orders_0=[]#未付款订单
            orders_1=[]#已付款未发货订单  
            orders_2=[]#已发货未收货订单  
            orders_3=[]#已收货订单  
            orders_4=[]#取消过的订单   
            for orders in rows:  #遍历每一个(order_id,order_status)
                status=orders[1]
                cursor_ = self.conn.execute("SELECT book_id,count,price FROM new_order_detail WHERE order_id = ?", (orders[0],))
                row=cursor_.fetchall()   #((book_id,count,price),...(book_id,count,price))
                for goods in row:   #遍历每个(book_id,count,price)
                    if status==0:
                        orders_0.append({"user_id":user_id,"order_id":orders[0],"book_id":goods[0],"count":goods[1],"price":goods[2]})
                    elif status==1:
                        orders_1.append({"user_id":user_id,"order_id":orders[0],"book_id":goods[0],"count":goods[1],"price":goods[2]})
                    elif status==2:
                        orders_2.append({"user_id":user_id,"order_id":orders[0],"book_id":goods[0],"count":goods[1],"price":goods[2]})
                    elif status==3:
                        orders_3.append({"user_id":user_id,"order_id":orders[0],"book_id":goods[0],"count":goods[1],"price":goods[2]})
                    elif status==-1:
                        orders_4.append({"user_id":user_id,"order_id":orders[0],"book_id":goods[0],"count":goods[1],"price":goods[2]})
            self.conn.commit()
            list_orders=[orders_0,orders_1,orders_2,orders_3,orders_4]  #总订单
        except BaseException as e:
            print(e)
            return 530, "{}".format(str(e))
        return 200,list_orders  #传回

    ###lsq:新功能：买家付款后申请取消订单
    def cancel_order(self, user_id: str, password:str, order_id: str):
        try:
            #先验证用户密码
            cursor = self.conn.execute("SELECT password  from user where user_id=?", (user_id,))
            row = cursor.fetchone()
            if row is None:
                return error.error_authorization_fail()
            if row[0] != password:
                return error.error_authorization_fail()
            
            #验证订单和对应的买家用户存在
            cursor=self.conn.execute("SELECT order_id, user_id, store_id, order_status,total_price FROM new_order WHERE order_id = ?", (order_id,))
            row = cursor.fetchone()
            if row is None:
                return error.error_invalid_order_id(order_id)
            
            order_id = row[0]
            buyer_id = row[1]
            store_id = row[2]
            order_status=row[3] 
            total_price=row[4]

            if buyer_id != user_id:
                return error.error_authorization_fail()
            
            #找到对应的卖家用户
            cursor = self.conn.execute("SELECT store_id, user_id FROM user_store WHERE store_id = ?;", (store_id,))
            row = cursor.fetchone()
            if row is None:
                return error.error_non_exist_store_id(store_id)
            seller_id = row[1]
            if not self.user_id_exist(seller_id):
                return error.error_non_exist_user_id(seller_id)
            
            #查找订单状态
            #1.1 在发货前取消订单-> 可以取消订单,将status置为-1,需要seller退款给buyer，并将扣除的库存还给store
            if order_status==1:
                #seller退款给buyer
                #buyer收款
                cursor = self.conn.execute("UPDATE user set balance = balance + ?"
                                           "WHERE user_id = ?",
                                           (total_price, buyer_id))                         
                if cursor.rowcount==0:
                    return error.error_non_exist_user_id(buyer_id)
                #seller退款
                cursor = self.conn.execute("UPDATE user set balance = balance - ?"
                                           "WHERE user_id = ? AND balance >= ?",
                                           (total_price, seller_id, total_price))
                
                #将扣除的订单书籍cnt补回stock_level
                cursor=self.conn.execute("SELECT book_id, count FROM new_order_detail WHERE order_id=?;",(order_id,))
                row=cursor.fetchall()
                
                book_id_and_count=[] #记录用户订单中的book_id和count信息
                for i in row:
                    book_id_and_count.append((i[0],i[1]))
                
                for book_id,count in book_id_and_count:
                    cursor = self.conn.execute(
                        "UPDATE store set stock_level= stock_level + ? "
                        "WHERE store_id = ? AND book_id = ?;",
                        (count,store_id, book_id))   
                
                #取消订单，status置为-1
                cursor = self.conn.execute("UPDATE new_order set order_status = ? WHERE order_id = ?",(-1,order_id))
                if cursor.rowcount==0:
                    return error.error_invalid_order_id(order_id)   
                       
            #1.2 在发货后取消订单->不可以取消,error
            if order_status==2:
                return error.error_order_dispatched(order_id)
            
            #2. 未付款时buyer取消订单->不需要退款给buyer，但要将扣除的库存还给store
            if order_status==0:
                #将扣除的订单书籍cnt补回stock_level
                cursor=self.conn.execute("SELECT book_id, count FROM new_order_detail WHERE order_id=?;",(order_id,))
                row=cursor.fetchall()
                
                book_id_and_count=[] #记录用户订单中的book_id和count信息
                for i in row:
                    book_id_and_count.append((i[0],i[1]))
                
                for book_id,count in book_id_and_count:
                    cursor = self.conn.execute(
                        "UPDATE store set stock_level= stock_level + ? "
                        "WHERE store_id = ? AND book_id = ?;",
                        (count,store_id, book_id))
                
                #取消订单，status置为-1
                cursor = self.conn.execute("UPDATE new_order set order_status = ? WHERE order_id = ?",(-1,order_id))
                if cursor.rowcount==0:
                    return error.error_invalid_order_id(order_id)

            self.conn.commit()
        except sqlite.Error as e:
            return 528, "{}".format(str(e))

        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"





