| **课程名称**：当代数据管理系统 | **年级**：2020 级           | **上机实践成绩**：           |
| ------------------------------ | --------------------------- | ---------------------------- |
| **指导教师**：周煊             | **上机实践名称**：bookstore | **上机实践日期**：2022.12.10 |

---

组员：陈柏延（10205501441）、李思琪（10205501412）、严寒（10205501435）

> - 实现一个提供网上购书功能的网站后端。
> - 网站支持书商在上面开商店，购买者可以通过网站购买。
> - 买家和卖家都可以注册自己的账号。
> - 一个卖家可以开一个或多个网上商店，
> - 买家可以为自已的账户充值，在任意商店购买图书。
> - 支持 下单->付款->发货->收货 流程。

**各成员工作**

## 一、关系数据库设计

### 概念设计

考虑实验功能实现要求进行概念设计，在原框架的基础上优化数据库结构。

### ER 图

### 关系模式

Table user:

## 二、连接 postgreSQL 数据库使用 ORM

### 连接

### 通过测试用例结果

## 三、功能实现逻辑

三部分的测试接口及测试用例说明分别在 doc.auth.md，doc.buyer.md，doc.seller.md 中编写，导出为 pdf 格式 auth.pdf、buyer.pdf、seller.pdf。

### author

1. 注册

   ```python
   @bp_auth.route("/register", methods=["POST"])
   def register():
       user_id = request.json.get("user_id", "")
       password = request.json.get("password", "")
       u = user.User()
       code, message = u.register(user_id=user_id, password=password)
       return jsonify({"message": message}), code
   ```

   我们从路由前台得到 user_id 与 password 后，调用 be.model 中 user 里的 User 类，调用后端 User 类中的方法 register 如下，进行异常测试。

   ```python
   def register(self, user_id: str, password: str):
           try:
               terminal = "terminal_{}".format(str(time.time()))
               token = jwt_encode(user_id, terminal)
      					new_user=Users(user_id=user_id,password=password,balance=0,token=token,terminal=terminal)
               DbSession.add(new_user)
               DbSession.commit()
           except BaseException as e:
               logging.info("530, {}".format(str(e)))
               return 530, "{}".format(str(e))
           return 200, "ok"
   ```

   后端逻辑中，每次注册根据得到的 str 类型 user_id 与 password、新生成的 terminal 与 token，向 User 表内新插入一条数据。

2. 注销

   ```python
   @bp_auth.route("/unregister", methods=["POST"])
   def unregister():
       user_id = request.json.get("user_id", "")
       password = request.json.get("password", "")
       u = user.User()
       code, message = u.unregister(user_id=user_id, password=password)
       return jsonify({"message": message}), code
   ```

   从路由前台得到 user_id、password 后，调用 be.model.user 里 User 类，调用后端 User 类中的方法 unregister 如下，进行异常测试。

   ```python
    def unregister(self, user_id: str, password: str):      # -> (int, str)
           try:
               code, message = self.check_password(user_id, password)
               if code != 200:
                   return code, message
               cursor=DbSession.query(Users).filter_by(user_id==user_id).delete()
               cnt=0
               for i in cursor:
                   cnt+=1
               if cnt==1:
                   DbSession.commit()
               else:
                   return error.error_authorization_fail()
           except BaseException as e:
               return 530, "{}".format(str(e))
           return 200, "ok"
   ```

   后端逻辑：每次登录根据得到的 str 类型 user_id、password，先调用类中的 check_password 方法验证密码正确（check_password 函数在第 6 点中，根据 User 中主键 user_id 查询相应密码，如遇传入的 password 相符，返回 200），如验证失败，则返回 check_password 相应报错信息；之后按照 User 中主键 user_id 查询结果，删除 User 表中该条数据；cnt 记录 query 这条语句查询到数据数量，若 cnt=1，该会话 commit 执行，若成功返回 200；若 cnt=0，说明 Users 中没有这条 user_id，报错返回错误码：401。

3. 登录

   ```python
   @bp_auth.route("/login", methods=["POST"])
   def login():
       user_id = request.json.get("user_id", "")
       password = request.json.get("password", "")
       terminal = request.json.get("terminal", "")
       u = user.User()
       code, message, token = u.login(user_id=user_id, password=password, terminal=terminal)
       return jsonify({"message": message, "token": token}), code

   ```

   我们从路由前台得到 user_id、password、terminal 后，调用 be.model 中 user 里的 User 类，调用后端 User 类中的方法 login 如下，进行异常测试。

   ```python
       def login(self, user_id: str, password: str, terminal: str):    #-> (int, str, str)
           token = ""
           try:
               code, message = self.check_password(user_id, password)
               if code != 200:
                   return code, message, ""
               token = jwt_encode(user_id, terminal)
               cursor=DbSession.query(Users).filter_by(user_id=user_id).update({'token':token,'terminal':terminal})
               if cursor==0:
                   return error.error_authorization_fail() + ("", )
               DbSession.commit()
           except BaseException as e:
               return 530, "{}".format(str(e)), ""
           return 200, "ok", token

   ```

   后端逻辑中，每次登录根据得到的 str 类型 user_id、password、terminal，先调用类中的 check_password 方法验证密码正确（check_password 函数在第 6 点中，根据 User 中主键 user_id 查询相应密码，如与传入的 password 相符，返回 200），如验证失败，则返回 check_password 相应报错信息；之后根据该登录时间，按照 User 中主键 user_id 查询结果，更新这条数据中的 token 和 terminal，该会话 commit 执行，若成功返回 200，否则报错。

4. 登出

   ```python
   @bp_auth.route("/logout", methods=["POST"])
   def logout():
       user_id: str = request.json.get("user_id")
       token: str = request.headers.get("token")
       u = user.User()
       code, message = u.logout(user_id=user_id, token=token)
       return jsonify({"message": message}), code

   ```

   我们从路由前台得到 user_id、tocken 后，调用 be.model 中 user 里的 User 类，调用后端 User 类中的方法 logout 如下，进行异常测试。

   ```python
   def logout(self, user_id: str, token: str) -> bool:
       try:
           code, message = self.check_token(user_id, token)
           if code != 200:
               return code, message
           terminal = "terminal_{}".format(str(time.time())) #登出时更新该用户的terminal和token
           dummy_token = jwt_encode(user_id, terminal)
       cursor=DbSession.query(Users).filter_by(user_id=user_id).update({'token':dummy_token,'terminal':terminal})
           if cursor==0:
               return error.error_authorization_fail()
           DbSession.commit()
       except BaseException as e:
           return 530, "{}".format(str(e))
       return 200, "ok"

   ```

   后端逻辑中，每次登录根据得到的 str 类型 user_id、token，先调用类中的 check_tocken 方法验证 tocken 合理（check_tocken 函数在第 6 点中，根据 User 中主键 user_id 查询相应 token，根据当前时间与 token 中记录的登录时间计算得 lifetime，若大于 0 正确，返回 200），如验证失败，则返回 check_token 相应报错信息；之后根据该登出时间，按照 User 中主键 user_id 查询结果，更新这条数据中的 token 和 terminal，该会话 commit 执行，若成功返回 200，否则报错（未找到这条 user_id，返回 401 错误码）。

5. 修改密码

   ```python
   @bp_auth.route("/password", methods=["POST"])
   def change_password():
       user_id = request.json.get("user_id", "")
       old_password = request.json.get("oldPassword", "")
       new_password = request.json.get("newPassword", "")
       u = user.User()
       code, message = u.change_password(user_id=user_id, old_password=old_password, new_password=new_password)
       return jsonify({"message": message}), code

   ```

   我们从路由前台得到 user_id、old_password、new_password 后，调用 be.model 中 user 里的 User 类，调用后端 User 类中的方法 change_password 如下，进行异常测试。

   ```python
       def change_password(self, user_id: str, old_password: str, new_password: str):  # -> bool
           try:
               code, message = self.check_password(user_id, old_password)
               if code != 200:
                   return code, message
               terminal = "terminal_{}".format(str(time.time()))
               token = jwt_encode(user_id, terminal)
             cursor=DbSession.query(Users).filter_by(user_id=user_id).update({'password':new_password,'token':token})
               cnt=0
               for i in cursor:
                   cnt+=1
               if cnt==0:
                   return error.error_authorization_fail()
               DbSession.commit()
           except BaseException as e:
               return 530, "{}".format(str(e))
           return 200, "ok"

   ```

   后端逻辑中，每次登录根据得到的 str 类型 user_id、old_password、new_password，先调用类中的 check_password 方法验证旧密码正确（check_password 函数在第 6 点中，根据 User 中主键 user_id 查询相应密码，如与传入的 password 相符，返回 200），如验证失败，则返回 check_password 相应报错信息；之后根按照 User 中主键 user_id 查询结果，将这条数据中 password 更新为 new_password，该会话 commit 执行，若成功返回 200，否则报错（未找到这条 user_id，返回 401 错误码）。

6. check

   ```python
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

   def check_token(self, user_id: str, token: str):    # -> (int, str)
       row=DbSession.query(Users.token).filter_by(user_id=user_id).first()
       if row is None:
           return error.error_authorization_fail()
       db_token = row.token
       if not self.__check_token(user_id, db_token, token):
           return error.error_authorization_fail()
       return 200, "ok"

   def check_password(self, user_id: str, password: str):  # -> (int, str)当与查找的user_id密码相同时返回正确
       row=DbSession.query(Users.password).filter_by(user_id=user_id).first()
       if row is None:
           return error.error_authorization_fail()
       if password != row.password:
           return error.error_authorization_fail()
       return 200, "ok"

   ```

   check_token、check_password、**check_token 都是在后端 User 类中的方法，为了验证登录等情况下用户的密码是否正确、tocken 是否合理。check_password 函数根据 User 中主键 user_id 查询相应密码，如与传入的 password 相符，返回 200，如验证失败，则返回相应报错信息 401；check_tocken 方法验证 tocken 合理，根据 User 中主键 user_id 查询相应 token，调用**check_token 将 token 传入，具体实现为根据当前时间与 token 中记录的登录时间计算得 lifetime，若大于 0 正确，返回 200，如验证失败，则返回 check_token 相应报错信息，并记录错误信息。

### buyer

1. 下单

   ```python
   @bp_buyer.route("/new_order", methods=["POST"])
   def new_order():
       user_id: str = request.json.get("user_id")
       store_id: str = request.json.get("store_id")
       books: [] = request.json.get("books")
       id_and_count = []
       for book in books:
           book_id = book.get("id")
           count = book.get("count")
           id_and_count.append((book_id, count))

       b = Buyer()
       code, message, order_id = b.new_order(user_id, store_id, id_and_count)
       return jsonify({"message": message, "order_id": order_id}), code
   ```

   ```python

   ```

2. 付款

   ```python
   @bp_buyer.route("/payment", methods=["POST"])
   def payment():
       user_id: str = request.json.get("user_id")
       order_id: str = request.json.get("order_id")
       password: str = request.json.get("password")
       b = Buyer()
       code, message = b.payment(user_id, password, order_id)
       return jsonify({"message": message}), code
   ```

   ```python

   ```

3. 充值

   ```python
   @bp_buyer.route("/add_funds", methods=["POST"])
   def add_funds():
       user_id = request.json.get("user_id")
       password = request.json.get("password")
       add_value = request.json.get("add_value")
       b = Buyer()
       code, message = b.add_funds(user_id, password, add_value)
       return jsonify({"message": message}), code
   ```

   ```python

   ```

4. 收货

   ```python
   @bp_buyer.route("/receive_stock", methods=["POST"]) #买家收货####CBY
   def receive_stock():
       user_id = request.json.get("user_id")
       password = request.json.get("password")
       order_id = request.json.get("order_id")
       b = Buyer()
       code, message = b.receive_stock(user_id, password, order_id)
       return jsonify({"message": message}), code
   ```

   ```python

   ```

5. 查询历史订单

   ```python
   @bp_buyer.route("/search_orders", methods=["POST"]) #买家查询订单####CBY
   def search_orders():
       user_id = request.json.get("user_id")
       password = request.json.get("password")
       b = Buyer()
       code, message = b.search_orders(user_id, password)
       return jsonify({"message": message}), code
   ```

   ```python

   ```

6. 手动取消订单

   ```python
   @bp_buyer.route("/cancel_order", methods=["POST"])
   def cancel_order():
      user_id = request.json.get("user_id")
      password = request.json.get("password")
      order_id = request.json.get("order_id")
      b=Buyer()
      code, message=b.cancel_order(user_id, password, order_id)
      return jsonify({"message": message}), code
   ```

   ```python

   ```

### seller

1. 创建店铺

   ```python
   @bp_seller.route("/create_store", methods=["POST"])
   def seller_create_store():
       user_id: str = request.json.get("user_id")
       store_id: str = request.json.get("store_id")
       s = seller.Seller()
       code, message = s.create_store(user_id, store_id)
       return jsonify({"message": message}), code
   ```

   ```python

   ```

2. 图书上架

   ```python
   @bp_seller.route("/add_book", methods=["POST"])
   def seller_add_book():
       user_id: str = request.json.get("user_id")
       store_id: str = request.json.get("store_id")
       book_info: str = request.json.get("book_info")
       stock_level: str = request.json.get("stock_level", 0)
       title = book_info['title']      ####
       tag = str(book_info['tags'])    ####
       content = book_info['content']  ####
       author = book_info['author']    ####
       book_price=book_info['price']    ####
       s = seller.Seller()
       code, message = s.add_book(user_id=user_id, store_id=store_id, book_id=book_info.get("id"), book_json_str=json.dumps(book_info), stock_level=stock_level, title=title,
                                  tag=tag, content=content, author=author,book_price=book_price)  ####
       return jsonify({"message": message}), code
   ```

   ```python

   ```

3. 增加库存

   ```python
   @bp_seller.route("/add_stock_level", methods=["POST"])
   def add_stock_level():
       user_id: str = request.json.get("user_id")
       store_id: str = request.json.get("store_id")
       book_id: str = request.json.get("book_id")
       add_num: str = request.json.get("add_stock_level", 0)
       s = seller.Seller()
       code, message = s.add_stock_level(user_id, store_id, book_id, add_num)
       return jsonify({"message": message}), code
   ```

   ```python

   ```

4. 发货

   ```python
   @bp_seller.route("/send_stock", methods=["POST"])
   def send_stock():
       user_id: str = request.json.get("user_id")
       order_id: str = request.json.get("order_id")
       s = seller.Seller()
       code, message = s.send_stock(user_id=user_id, order_id=order_id)
       return jsonify({"message": message}), code
   ```

   我们从路由前台得到 user_id 与 order_id 后，调用 be.model 中 seller 里的 Seller 类，调用后端 Seller 类中的方法 send_stock 如下，进行异常测试。

   ```python
   def send_stock(self, user_id: str, order_id: str):  # -> (int, str) #发货#####CBY
       try:
           #先验证订单存在、用户存在
           row = DbSession.query(New_order).filter_by(order_id=order_id).first()
           if row is None:
               return error.error_invalid_order_id()

           #查找订单状态
           if row.order_status != 1:
               return error.error_order_not_dispatched(order_id)
           #更新订单状态为2 发货
           cursor=DbSession.query(New_order).filter_by(order_id = order_id).update({"order_status": 2})
           if cursor == 0:
               return error.error_non_exist_user_id(user_id)
           DbSession.commit()
       except BaseException as e:
           return 530, "{}".format(str(e))
       return 200, "ok"
   ```

5. 卖家改价

   ```python
   @bp_seller.route("/set_book_price", methods=["POST"])
   def set_book_price():
       user_id: str = request.json.get("user_id")
       store_id: str = request.json.get("store_id")
       book_id: str = request.json.get("book_id")
       book_price: str = request.json.get("book_price")

       s=seller.Seller()
       code, message=s.set_book_price(user_id,store_id,book_id,book_price)
       return jsonify({"message":message}), code
   ```

   ```python

   ```

### 自动取消订单

```python
def auto_cancel(): #自动清除订单
    rows = DbSession.query(New_order).filter_by(order_status=0).all()
    for content in rows:
        end_time = time.time()
        if (end_time - content.time >= 300):  # 付款时间超过5分钟自动取消
  					DbSession.query(New_order).filter_by(order_id=content.order_id).update({"order_status": -1})
            rows_=DbSession.query(New_order_detail).filter_by(order_id=content.order_id).all()
            for order in rows_:
                  DbSession.query(Store).filter(\
                                                Store.store_id==content.store_id,\
                                                Store.book_id==order.book_id
                                               ).\
                update({Store.stock_level: Store.stock_level + order.count})
    DbSession.commit()
scheduler=BackgroundScheduler() #定义后台执行调度器
scheduler.add_job(func=auto_cancel, trigger="interval", seconds=5)
if __name__ == "__main__":
    scheduler.start()
    serve.be_run()
```

该函数写在 app.py 中，执行逻辑：为了顺应自动清除未付款订单的需求，后台每 5 秒钟搜索一遍距离下单时间超过 5 分钟的未付款订单，予以删除（为了查询历史订单，此处的删除在数据库中实际为更改订单 status）

实现方法：使用 flask 定时任务 flask-apscheduler，接着导入 BackgroundScheduler，APSchedule 使用 interval 间隔时间 5s 启动任务函数 auto_cancel。主函数中，scheduler.start 后进行 app.run()，成功实现 function 函数一直在后台的定时运行。

auto_cancel 中，先根据 order_status=0 的条件查询 table New_order 中符合条件的所有数据，记录此时的时刻 endtime；遍历每一条数据，比较 endtime 与 time 列的值（记录了下单时的时间），如果大于 5 分钟，根据 order_id 主键查找 New_order 中对应数据，将 order_status 置为-1，表示已经被取消；同时，由于订单已被取消，要将之前下单时从 store 中删去书籍库存加回，因此根据 order_id 主键查找 New_order_detail 中对应数据，继而由主键（store_id，book_id）更新 Store 表中的 stock_level 值。

## 四、优化数据库执行性能

## 五、git 版本管理

## 六、总结问题
