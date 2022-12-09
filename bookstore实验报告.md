| **课程名称**：当代数据管理系统  | **年级**：2020 级           | **上机实践成绩**：           |
| ------------------------------ | --------------------------- | ---------------------------- |
| **指导教师**：周煊             | **上机实践名称**：bookstore | **上机实践日期**：2022.12.10 |

---

组员：陈柏延（10205501441）、李思琪（10205501412）、严寒（10205501435）

## 一、项目要求

### 1. 功能

- 实现一个提供网上购书功能的网站后端。

- 网站支持书商在上面开商店，购买者可以通过网站购买。
- 买家和卖家都可以注册自己的账号。
- 一个卖家可以开一个或多个网上商店，
- 买家可以为自已的账户充值，在任意商店购买图书。
- 支持 下单->付款->发货->收货 流程。

1. 实现对应接口的功能，

​        其中包括：

​        1) 用户权限接口，如注册、登录、登出、注销 

​        2) 买家用户接口，如充值、下单、付款 

​        3) 卖家用户接口，如创建店铺、填加书籍信息及描述、增加库存 

​         通过对应的功能测试，所有test case都pass 

2. 为项目添加其它功能 ：（40%）

​        1) 实现后续的流程：发货 -> 收货

​        2) 搜索图书 

​          用户可以通过关键字搜索，参数化的搜索方式；
​          如搜索范围包括，题目，标签，目录，内容；全站搜索或是当前店铺搜索。
​          如果显示结果较大，需要分页
​          (使用全文索引优化查找)

        3) 订单状态，订单查询和取消定单 
           用户可以查自已的历史订单，用户也可以取消订单。
           取消定单可由买家主动地取消定单，或者买家下单后，经过一段时间超时仍未付款，定单也会自动取消。

### 2. 要求

1. bookstore文件夹是该项目的demo，采用flask后端框架与sqlite数据库，实现了前60%功能以及对应的测试用例代码。要求利用ORM使用postgreSQL数据库实现前60%功能，可以在demo的基础上进行修改，也可以采用其他后端框架重新实现。需要通过fe/test/下已有的全部测试用例。

2. 在完成前60%功能的基础上，继续实现后40%功能，要有接口、后端逻辑实现、数据库操作、代码测试。对所有接口都要写test case，通过测试并计算测试覆盖率（尽量提高测试覆盖率）。

3. 尽量使用索引、事务处理等关系数据库特性，对程序与数据库执行的性能有考量

4. 尽量使用git等版本管理工具

5. 不需要实现界面，通过代码测试体现功能与正确性

## 二、关系数据库设计

### 1. 概念设计

根据要实现的功能，设计“存什么数据”的问题。

要建立四个实体，分别是user, order, store和book，分别包括如下属性：

（1）book: book_id作为索引，book_title, book_author, book_tag, book_content作为查询搜索的范围。

（2）user: user_id作为索引，password, balance记录用户的账户余额。

（3）order: order_id作为索引，order_status区分订单的完成情况（已下单未支付、已支付未发货、已发货未收货、取消）

（4）store: store_id作为索引，可以建立一个store_name。

通过对功能实现上的分析，将几个实体之间构建联系，绘制出的ER图和数据库设计如下：

### 2. ER 图
![请添加图片描述](https://img-blog.csdnimg.cn/6150da3392fd47e8a20cf58f38bf3768.jpeg)

### 3. 关系模式

**说明：本次实验通过postgresql数据库和sqlite数据库实现，其中postgresql数据库用户、订单、商铺相关的数据，sqlite数据库存放书的信息数据。**

#### postgresql数据库:

通过绘制ER图以及后续分析实验要求的功能，我们建了五张表，分别是user、store、user_store、new_order、new_order_detail，具体如下：

**Table user:**
![请添加图片描述](https://img-blog.csdnimg.cn/1aeb0b28c7a54503b01db9216526df96.jpeg)


变量名 | 类型 | 含义 | 是否可为空
---|---|---|---
user_id | text | 用户ID（主键） | N
password | text | 用户密码 | N
balance | integer | 用户账户存款 | N
token | text | 访问token，用户登录后每个需要授权的请求应在headers中传入这个token | 成功时不为空
terminal | text | 终端代码 | N

**说明：**

1. user_id作为索引，不允许为空。
2. user表用于记录用户信息和登录判断的依据。

**Table user_store:**
![请添加图片描述](https://img-blog.csdnimg.cn/36399bf33b304f52b9154d6f9ae37b1b.jpeg)


变量名 | 类型 | 含义 | 是否可为空
---|---|---|---
user_id | text | 用户ID（主键） | N
store_id | text | 商店ID（主键）| N

**说明：**

1. user_store表记录商铺和店家的信息，user_id和store_id作为联合主键，不允许为空，store_id唯一，user_id允许重复，可以用来存储一个商家开n家或1家店铺的情况。

**Table store:**
![请添加图片描述](https://img-blog.csdnimg.cn/212fa4cccd534308a8eeff55ef333959.jpeg)

变量名 | 类型 | 含义 | 是否可为空
---|---|---|---
store_id | text | 商店ID（主键）| N
book_id | text | 图书ID（主键） | N
book_info | text | 图书内容 | Y
stock_level | integer | 图书库存 | N
title | text | 图书标题 | Y
tag | text | 图书标签 | Y
author| text | 图书作者 | Y
content | text | 图书目录 | Y
book_price | integer | 图书价格 | Y

**说明：**

1. store表用来存储店铺售卖的书籍信息，以(store_id， book_id)为联合主键。这里将book的信息(title、tag、author、content、book_price等)存储在store表中，便于在搜索中查找店铺中书籍的相关信息。

**Table new_order:**
![image-20221209064328792](C:\Users\huawei\AppData\Roaming\Typora\typora-user-images\image-20221209064328792.png)

变量名 | 类型 | 含义 | 是否可为空
---|---|---|---
order_id | text | 订单ID（主键）| N
user_id | text | 用户ID | N
store_id | text | 商店ID | N
order_status | integer | 订单状态 | N
total_price | integer | 订单总价 | N 
time | integer | 订单产生时间 | N

**说明：**

1. new_order表中存储用户的订单信息，除最初ER图的设计外，考虑到后续的订单收发功能、取消订单以及payment功能，添加了order_status属性和total_price属性，其中，order_status分为五种状态，状态0：已下单未支付，状态1：已支付未发货，状态2：已发货未收货，状态3：已收货，订单结束。状态-1：订单被取消。
2. time属性用来记录订单产生时间，作为超时未付款自动取消订单的依据。
3. 由于一个用户每次下单的id不同，即便是同一个用户在同一家店铺下单，每次的订单id也是不同的，所以这里new_order表只在order_id属性上建立索引即可。

**Table new_order_detail:**
![image-20221209065527679](C:\Users\huawei\AppData\Roaming\Typora\typora-user-images\image-20221209065527679.png)

变量名 | 类型 | 含义 | 是否可为空
---|---|---|---
order_id | text | 订单ID（主键）| N
book_id | text | 书本ID | N
count | integer | 书本数目 | N
price | integer | 价格 | N 

**说明：**

1. new_order_detail表用来存储用户订单的具体信息，分别记录了用户订单内的书籍(book_id)，订单内每本书的数目(count)和单价(price)。
2. 以order_id为索引，调用时利用order_id查询到订单详情。


#### sqlite数据库：

book.db:
![请添加图片描述](https://img-blog.csdnimg.cn/48185808d2064ba587fcd748057de92a.png)
![请添加图片描述](https://img-blog.csdnimg.cn/91680a5342fa487faacb74afc348998b.png)


变量名 | 类型 | 含义 | 是否可为空
---|---|---|---
id | string | 书籍ID  | N
title | string | 书籍题目  | N
author | string | 作者 | Y
publisher | string | 出版社 | N
original_title | string |原书题目 | Y
translater | string | 译者 | Y
pub_year | string | 出版年月 | N
pages | int | 页数 | N
price | int | 价格，以分为单位 | N
currency_unit | string | 币种 | N
binding | string | 装订方式 | N
isbn | string | 国际标准书号 | N
author_intro | string | 图书内容 | Y
book_intro | string | 书籍简介 | Y
content | string | 样章试读 | Y
tags | array | 标签 | N
picture | array | 封面照片 | N

**说明：**

1. book.db数据库中记录了100本书籍的信息。

## 三、连接 postgreSQL 数据库并使用 ORM

### 1. 建立连接

![请添加图片描述](https://img-blog.csdnimg.cn/560dcc29da1640a69a681ffdc857c3b3.png)


### 2. 创建表


```python
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
    total_price=Column(Integer,nullable=False)
    time=Column(Integer,nullable=False)

#new_order_detail表
class New_order_detail(Base):
    __tablename__="new_order_detail"

    order_id=Column(Text,primary_key=True,nullable=False)
    book_id=Column(Text,primary_key=True,nullable=False)
    count=Column(Integer,nullable=False)
    price=Column(Integer,nullable=False)
```
（in init_database.py）


### 3. ORM改写

**说明：**

1. 对于前60%的基础功能和40%的其它功能都实现了ORM和postgresql数据库的连接使用。

2. 在我们所有实现的功能中，最初是用sqlite数据库建表并且完成了前60%的功能和后40%除搜索之外的功能，在完成这些功能之后，又将数据库的操作改写为用ORM进行，使用postgresql数据库。所以在代码中修改了最初连接数据库的方式以及数据库的操作，最初sqlite数据库的直接操作仍保留在注释内容中。

3. 在db_conn.py中修改了连接数据库的方式，基于ORM和Postgresql数据库，每调用一个self.conn=db_conn.DBConn.\_\_init\_\_()会新建立一个会话，也就意味着每个功能的实现都会建立一个新的会话，每个功能作为一个事务，在一个功能的任务全部完成之后self.conn.commit()提交，保证功能实现上的原子性。

   ```python
   class DBConn:
       def __init__(self):
           #engine = create_engine('postgresql://postgres:mbyc020905@localhost:5432/books')
           engine=create_engine("postgresql://postgres:lisiqi20020521@localhost:5432/bookstore")
           # 创建session
           DbSession = sessionmaker(bind=engine)
           self.conn = DbSession()
   ```

4. 这里展示几个ORM改写的实现：

   **例如，增(add)操作：**
   
   ```python
               new_user=Users(user_id=user_id,password=password,balance=0,token=token,terminal=terminal)
               self.conn.add(new_user)
               self.conn.commit()
   ```
   
   **删(delete)操作：**
   
   ```python
               cursor=self.conn.query(Users).filter_by(user_id=user_id).first()
               if cursor is None:
                   return error.error_authorization_fail()
               else:
                   self.conn.delete(cursor)
                   self.conn.commit()
   ```
   
   **改(update)操作：**
   
   ```python
   cursor=self.conn.query(Users).filter_by(user_id=user_id).update({'password':new_password,'token':token}) 
   self.conn.commit()
   ```
   
   **查(query)操作：**
   
   ```python
   #数据量多需要分页
   total_result=[] #分别存储所有页数据的集合
   page_cnt=math.ceil(len(row)/page_limit)
   for i in range(page_cnt):
   	total_result.append([]) #分别存储每一页数据
       #先排序，按照顺序分页显示，分页显示用到的是limit限制一页的数据量，利用offset做偏移
        row=self.conn.query(Store).order_by(Store.book_id.asc()).filter(Store.tag.like('%'+search_key+'%'),
                                     Store.store_id==store_id).limit(page_limit).offset(i*page_cnt).all()
        for j in row:
        	total_result[i].append(j)
   ```

## 四、功能实现逻辑

**说明：**

1. 三部分的测试接口及测试用例的说明分别在 doc/auth.md，doc/buyer.md，doc/seller.md 中编写，导出为 pdf 格式 auth.pdf、buyer.pdf、seller.pdf，见项目报告文件夹（报告）内。
2. 以下说明功能实现的后端逻辑实现以及相应的数据库操作。

### 1. 基础功能（60%）

#### 1. 1 author

##### **1.1.1 注册**

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
```

后端逻辑中，每次注册根据得到的 str 类型 user_id 与 password、新生成的 terminal 与 token，**向 User 表内新插入一条数据**。

##### 1.1.2 注销

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
            #cursor = self.conn.execute("DELETE from user where user_id=?", (user_id,))  #注销用户
            #####
            cursor=self.conn.query(Users).filter_by(user_id=user_id)
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
```

后端逻辑：每次登录根据得到的 str 类型 user_id、password，先调用类中的 check_password 方法验证密码正确（check_password 函数在第 1.1.6 点中，**根据 User 中主键 user_id 查询相应密码**，如与传入的 password 相符，返回 200），如验证失败，则返回 check_password 相应报错信息；之后按照 User 中主键 user_id 查询结果，**删除 User 表中该条数据**；cnt 记录 query 这条语句查询到数据数量，若 cnt=1，该会话 commit 执行，若成功返回 200；若 cnt=0，说明 Users 中没有这条 user_id，报错返回错误码：401。

##### 1.1.3 登录

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
```

后端逻辑中，每次登录根据得到的 str 类型 user_id、password、terminal，先调用类中的 check_password 方法验证密码正确（check_password 函数在第 1.1.6 点中，**根据 User 中主键 user_id 查询相应密码**，如与传入的 password 相符，返回 200），如验证失败，则返回 check_password 相应报错信息；**之后根据该登录时间，按照 User 中主键 user_id 查询结果，更新这条数据中的 token 和 terminal**，该会话 commit 执行，若成功返回 200，否则报错。

##### 1.1.4 登出

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

后端逻辑中，每次登录根据得到的 str 类型 user_id、token，先调用类中的 check_tocken 方法验证 tocken 合理（check_tocken 函数在第1.1.6 点中，根据 User 中主键 user_id 查询相应 token，根据当前时间与 token 中记录的登录时间计算得 lifetime，若大于 0 正确，返回 200），如验证失败，则返回 check_token 相应报错信息；**之后根据该登出时间，按照 User 中主键 user_id 查询结果，更新这条数据中的 token 和 terminal**，该会话 commit 执行，若成功返回 200，否则报错（未找到这条 user_id，返回 401 错误码）。

##### 1.1.5 修改密码

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

后端逻辑中，每次登录根据得到的 str 类型 user_id、old_password、new_password，先调用类中的 check_password 方法验证旧密码正确（check_password 函数在第 1.1.6 点中，**根据 User 中主键 user_id 查询相应密码**，如与传入的 password 相符，返回 200），如验证失败，则返回 check_password 相应报错信息；**之后根按照 User 中主键 user_id 查询结果，将这条数据中 password 更新为 new_password**，该会话 commit 执行，若成功返回 200，否则报错（未找到这条 user_id，返回 401 错误码）。

##### 1.1.6 check_token

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
```

check_token、check_password、check_token 都是在后端 User 类中的方法，为了验证登录等情况下用户的密码是否正确、token 是否合理。**check_password 函数根据 User 中主键 user_id 查询相应密码**，如与传入的 password 相符，返回 200，如验证失败，则返回相应报错信息 401；check_token 方法验证 token 合理，**根据 User 中主键 user_id 查询相应 token**，调用check_token 将 token 传入，具体实现为根据当前时间与 token 中记录的登录时间计算得 lifetime，若大于 0 正确，返回 200，如验证失败，则返回 check_token 相应报错信息，并记录错误信息。

#### 1.2 buyer

##### 1.2.1 下单

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
路由前台记录用户下单的信息，将用户下单的books，拆解为(book_id, count)对，存入id_and_count列表中。

从路由前台得到 user_id ， store_id 和id_and_count；调用 be.model 中 buyer 里的 Buyer 类，调用后端 Buyer 类中的方法 new_order 如下，进行异常测试。


```python
def new_order(self, user_id: str, store_id: str, id_and_count: [(str, int)]) -> (int, str, str):
        order_id = ""
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id) + (order_id, )
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id) + (order_id, )
            uid = "{}_{}_{}".format(user_id, store_id, str(uuid.uuid1()))
            t_price=0####cby
            for book_id, count in id_and_count:
                row = self.conn.query(Store).filter_by(store_id=store_id, book_id=book_id).first()  ####
                if row is None:
                    return error.error_non_exist_book_id(book_id) + (order_id,)
                    
                stock_level = row.stock_level
                book_info = row.book_info
                #####cby
                book_info_json = json.loads(book_info)
                price = book_info_json.get("price")
                t_price+=count*price  ####cby

                if stock_level < count:
                    return error.error_stock_level_low(book_id) + (order_id,)
                
                row = self.conn.query(Store).filter_by(store_id=store_id, book_id=book_id, stock_level=stock_level).update(
                    {'stock_level': stock_level - count})
                # if cursor.rowcount == 0:
                if row==0:
                    return error.error_stock_level_low(book_id) + (order_id, )
               
                new_order_detail = New_order_detail(order_id=uid, book_id=book_id, count=count, price=price)
                self.conn.add(new_order_detail)
                new_order=New_order(order_id=uid,user_id=user_id,store_id=store_id,order_status=0,total_price=t_price,time=time.time())
            self.conn.add(new_order)
            order_id = uid
            self.conn.commit()
            
        except BaseException as e:
            print(e)
            logging.info("530, {}".format(str(e)))
            return 530, "{}".format(str(e)), ""
        return 200, "ok", order_id
```
后端逻辑：

每次下单根据得到的 str 类型 user_id、store_id、id_and_count，先判断 user_id和store_id是否存在，如果不存在分别返回error_non_exist_user_id(user_id)（错误码：511）和error_non_exist_store_id(store_id)（错误码：513）。

**对于new_order中的每一个(store_id, book_id)，在数据库store表中查询店铺中该书的库存stock_level**，若其下单的数量count>stock_level，则无法下单，返回库存不足（error_stock_level_low）错误(517)。**若能够正常下单，将下单的详细信息增加入new_order_detail表中，在store表中更新库存，在new_order表中增加订单信息，将订单状态(order_status)置为0（已下单未付款的状态），填入订单总价和下单时间。**

##### 1.2.2 付款

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

从路由前台得到 user_id ， order_id 和password；
调用 be.model 中 buyer 里的 Buyer 类，调用后端 Buyer 类中的方法 payment完成对应订单的付款。

```python
    def payment(self, user_id: str, password: str, order_id: str) -> (int, str):
        try:
            row = self.conn.query(New_order).filter_by(order_id=order_id).first()
            if row is None:
                return error.error_invalid_order_id(order_id)

            order_id=row.order_id
            buyer_id = row.user_id
            store_id = row.store_id
            order_status=row.order_status 
            total_price=row.total_price

            if buyer_id != user_id:
                return error.error_authorization_fail()

            if order_status!=0: #若已经付过款返回错误####CBY 
               return error.error_invalid_order_id(order_id) 

            row = self.conn.query(User).filter_by(user_id=buyer_id).first()
            if row is None:
                return error.error_non_exist_user_id(buyer_id)

            buyer_balance = row.balance
            if password !=  row.password:
                return error.error_authorization_fail()
     
            row=self.conn.query(User_store).filter_by(store_id=store_id).first()
            seller_id=row.user_id

            row = self.conn.query(User).filter_by(user_id=seller_id).first()

            if row is None:
                return error.error_non_exist_store_id(store_id)
            # seller_id = row[1]
            seller_balance=row.balance
            ####
            if not self.user_id_exist(seller_id):
                return error.error_non_exist_user_id(seller_id)

            if buyer_balance < total_price:   #钱不够
                return error.error_not_sufficient_funds(order_id)
            
            cursor = self.conn.query(User).filter(User.user_id == buyer_id and User.balance >= total_price).update({'balance': buyer_balance - total_price})
            if cursor == 0:
                return error.error_not_sufficient_funds(order_id)
            
            cursor = self.conn.query(User).filter_by(user_id=seller_id).update({'balance': seller_balance + total_price})
            #self.conn.commit()
            if cursor == 0:
                return error.error_non_exist_user_id(seller_id)
          
            cursor = self.conn.query(New_order).filter_by(order_id=order_id).update({"order_status": 1})
            if cursor == 0:
                return error.error_invalid_order_id(order_id)

            self.conn.commit()

        except BaseException as e:
            return 530, "{}".format(str(e))

        return 200, "ok"
```

后端逻辑：

**在new_order表中通过订单号(order_id)查询新订单是否存在**，如果订单不存在，返回error.error_invalid_order_id(order_id)，错误码518；如果可以查询到订单，获取订单的详细信息，包括buyer_id,store_id,order_status和total_price便于后续判断。判断订单购买者是否是用户本人，如果不是则返回错误error_authorization_fail()；判断订单状态order_status是否不等于0，即已经付完款的所有状态，如果是，则不能重复支付，返回错误error_invalid_order_id(order_id) 。**对于买家，在表user中查询订单信息中的购买者id，获取存款(buyer_balance)；对于卖家，在表User_store中通过店铺id查询订单信息中的user_id（记为seller_id），同样去获取其存款数目(记为seller_balance)。**对比买家存款和前一步“下单”中得到的total_price，如果买家存款少于总价，即钱不够，返回错误error_not_sufficient_funds(order_id)；如果买家存款充足，则买家付钱，**在user表中，其存款中减少对应数目，同时卖家存款中增加对应数目**。**在new_order表中，将记录订单状态的status更新为1，表示已付款。**

##### 1.2.3 充值

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

从路由前台得到 user_id ， password 和add_value；调用 be.model 中 buyer 里的 Buyer 类，调用后端 Buyer 类中的方法 add_funds增加用户账户中的⾦额。

```python
def add_funds(self, user_id, password, add_value) -> (int, str):
        try:
            # cursor = self.conn.execute("SELECT password  from user where user_id=?", (user_id,))
            # row = cursor.fetchone()
            row = self.conn.query(User).filter_by(user_id=user_id).first()

            if row is None:
                return error.error_authorization_fail()
            if row.password!= password:
                return error.error_authorization_fail()

            balance = row.balance
            # cursor = self.conn.execute(
            #     "UPDATE user SET balance = balance + ? WHERE user_id = ?",
            #     (add_value, user_id))
            # if cursor.rowcount == 0:
            #     return error.error_non_exist_user_id(user_id)
            cursor = self.conn.query(User).filter_by(user_id=user_id).update({"balance": balance + add_value})
            if cursor == 0:
                return error.error_non_exist_user_id(user_id)
                
            self.conn.commit()
        # except sqlite.Error as e:
        #     return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))

        return 200, "ok"
```
后端逻辑：
**在User表中查找用户ID，得到用户在user表中的password，即验证是否本人，并获取用户现在的余额(balance)信息。若为本人，update user表将其充值金额(add_value)加入。**


#### 1.3 seller

##### 1.3.1 创建店铺

```python
@bp_seller.route("/create_store", methods=["POST"])
def seller_create_store():
    user_id: str = request.json.get("user_id")
    store_id: str = request.json.get("store_id")
    s = seller.Seller()
    code, message = s.create_store(user_id, store_id)
    return jsonify({"message": message}), code
```
从路由前台得到 user_id和store_id ；调用 be.model 中 seller 里的 Seller 类中的方法 create_store ，进行异常测试。

```python
def create_store(self, user_id: str, store_id: str):       #-> (int, str)
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if self.store_id_exist(store_id):
                return error.error_exist_store_id(store_id)
            # self.conn.execute("INSERT into user_store(store_id, user_id)"
            #                   "VALUES (?, ?)", (store_id, user_id))
            # self.conn.commit()
            user_store = User_store(user_id=user_id, store_id=store_id)
            self.conn.add(user_store)
            self.conn.commit()
        # except sqlite.Error as e:
        #     return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"
```
后端逻辑：

先验证用户和店铺id，根据 User 中主键 user_id 查询该用户是否存在，若不存在返回错误码511；根据 User 中主键 store_id 查询该用户想要创建的店铺是否存在，若已经存在返回error_exist_store_id(store_id)（错误码514）。
**在User_store表中插入该用户的id和新建店铺id，执行提交更改。**该会话commit 执行，若成功返回 200，反之报错。


##### 1.3.2 填加书籍信息及描述

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

从路由前台得到 user_id ，store_id ，book_info 和stock_level，其中若不存在stock_level，初始化为0 ；调用 be.model 中 seller 里的 Seller 类中的add_book方法 ，进行异常测试。

```python
def add_book(self, user_id: str, store_id: str, book_id: str, book_json_str: str, stock_level: int, title: str,
                 author: str, content: str, tag: str,book_price:int):#向store中添加书
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if self.book_id_exist(store_id, book_id):
                return error.error_exist_book_id(book_id)

            # self.conn.execute("INSERT into store(store_id, book_id, book_info, stock_level,title,tag,author,content,book_price)"
            #                   "VALUES (?,?,?,?,?,?,?,?,?)", (store_id, book_id, book_json_str, stock_level,title,tag,author,content,book_price))
            # self.conn.commit()
            one_store = Store(store_id=store_id,book_id= book_id, book_info=book_json_str,stock_level= stock_level,title=title, tag=tag, author=author, content=content,
                              book_price=book_price)
            self.conn.add(one_store)
            self.conn.commit()
        # except sqlite.Error as e:
        #     return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"
```
后端逻辑：

先验证user_id，store_id是否存在，如果不存在分别返回错误码511和514，**根据 主键 store_id 和 book_id ，在store表中查询该店铺中是否存在该书籍，若不存在返回error_exist_book_id(book_id)（错误码516）；向 store表中插入新上架图书的包括图书id、内容、上架数目、标题、标签、作者、目录和店铺id的信息**，执行提交更改，若成功返回 200，反之报错。

##### 1.3.3 增加库存

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

从路由前台得到 user_id ，store_id ，book_info 和add_stock_level；调用 be.model 中 seller 里的 Seller 类中的方法add_stock_level ，进行异常测试。

```python
def add_stock_level(self, user_id: str, store_id: str, book_id: str, add_stock_level: int):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if not self.book_id_exist(store_id, book_id):
                return error.error_non_exist_book_id(book_id)

            # self.conn.execute("UPDATE store SET stock_level = stock_level + ? "
            #                   "WHERE store_id = ? AND book_id = ?", (add_stock_level, store_id, book_id))
            # self.conn.commit()
            self.conn.query(Store).filter(Store.store_id == store_id, Store.book_id == book_id).update({Store.stock_level: Store.stock_level + add_stock_level})
            self.conn.commit()
        # except sqlite.Error as e:
        #     return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"
```
后端逻辑：

先验证user_id，store_id是否存在，如果不存在分别返回错误码511和514，根据主键 store_id 和 book_id 查询该店铺中是否存在该书籍，若不存在返回error_exist_book_id(book_id)（错误码516）；**根据 Store 中主键 store_id 和 book_id 查询店铺内该图书库存，更新库存为原数目+进货数目（add_stock_level）**。执行提交更改，若成功返回 200，反之报错。




### 2. 其它功能（40%）


#### 2.1 自动取消订单


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

#### 2.2 买家手动取消订单

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

从路由前台得到 user_id ，password，order_id；调用 be.model 中 buyer里的 Buyer类中的方法cancel_order，进行异常测试。

```python
 ###lsq:新功能：买家付款后申请取消订单
    def cancel_order(self, user_id: str, password:str, order_id: str):
        try:
            #先验证用户密码
            #cursor = self.conn.execute("SELECT password  from user where user_id=?", (user_id,))
            #row = cursor.fetchone()
            row=self.conn.query(User).filter_by(user_id=user_id).first()

            if row is None:
                return error.error_authorization_fail()
            if row.password != password:
                return error.error_authorization_fail()
            
            #验证订单和对应的买家用户存在
            #cursor=self.conn.execute("SELECT order_id, user_id, store_id, order_status,total_price FROM new_order WHERE order_id = ?", (order_id,))
            #row = cursor.fetchone()
            row=self.conn.query(New_order.order_id,New_order.user_id,New_order.store_id,New_order.order_status,New_order.total_price).filter_by(order_id=order_id).first()
            
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
            #cursor = self.conn.execute("SELECT store_id, user_id FROM user_store WHERE store_id = ?;", (store_id,))
            #row = cursor.fetchone()

            row=self.conn.query(User_store.user_id).filter_by(store_id=store_id).first()
 
            if row is None:
                return error.error_non_exist_store_id(store_id)
            seller_id = row[0]
            if not self.user_id_exist(seller_id):
                return error.error_non_exist_user_id(seller_id)
            
            #查找订单状态
            #1.1 在发货前取消订单-> 可以取消订单,将status置为-1,需要seller退款给buyer，并将扣除的库存还给store
            if order_status==1:
                #seller退款给buyer
                #buyer收款
                #cursor = self.conn.execute("UPDATE user set balance = balance + ?"
                #                           "WHERE user_id = ?",
                #                           (total_price, buyer_id))   

                row=self.conn.query(User.balance).filter_by(user_id=buyer_id).first()
                buyer_balance=row[0]

                cursor=self.conn.query(User).filter_by(user_id=buyer_id).update({'balance':buyer_balance+total_price})  
                #self.conn.commit()
                
                #if cursor.rowcount==0:
                if cursor==0:
                    return error.error_non_exist_user_id(buyer_id)

                #seller退款
                row=self.conn.query(User.balance).filter_by(user_id=seller_id).first()
             
                seller_balance=row[0]
                #cursor = self.conn.execute("UPDATE user set balance = balance - ?"
                #                           "WHERE user_id = ? AND balance >= ?",
                #                           (total_price, seller_id, total_price))
                cursor=self.conn.query(User).filter(and_(User.user_id==seller_id,User.balance>=total_price)).update({'balance':seller_balance-total_price})
         
                #将扣除的订单书籍cnt补回stock_level
                #cursor=self.conn.execute("SELECT book_id, count FROM new_order_detail WHERE order_id=?;",(order_id,))
                #row=cursor.fetchall()
                row=self.conn.query(New_order_detail).filter_by(order_id=order_id).all()
                
                book_id_and_count=[] #记录用户订单中的book_id和count信息
                for i in row:
                    book_id_and_count.append((i.book_id,i.count))
                
                for book_id, count in book_id_and_count:
                    #cursor = self.conn.execute(
                    #    "UPDATE store set stock_level= stock_level + ? "
                    #    "WHERE store_id = ? AND book_id = ?;",
                    #    (count,store_id, book_id)) 
                    row=self.conn.query(Store.stock_level).filter_by(store_id=store_id,book_id=book_id).first()
                    book_stock_level=row[0]
                    cursor=self.conn.query(Store).filter_by(store_id=store_id,book_id=book_id).update({'stock_level':book_stock_level+count})
                    #self.conn.commit()
                
                #取消订单，status置为-1
                #cursor = self.conn.execute("UPDATE new_order set order_status = ? WHERE order_id = ?",(-1,order_id))
                cursor=self.conn.query(New_order).filter_by(order_id=order_id).update({'order_status':-1})
                #self.conn.commit()
                #if cursor.rowcount==0:
                if cursor==0:
                    return error.error_invalid_order_id(order_id)   
                       
            #1.2 在发货后取消订单->不可以取消,error
            if order_status==2:
                return error.error_order_dispatched(order_id)
            
            #2. 未付款时buyer取消订单->不需要退款给buyer，但要将扣除的库存还给store
            if order_status==0:
                #将扣除的订单书籍cnt补回stock_level
                #cursor=self.conn.execute("SELECT book_id, count FROM new_order_detail WHERE order_id=?;",(order_id,))
                #row=cursor.fetchall()
                row=self.conn.query(New_order_detail).filter_by(order_id=order_id).all()
                
                book_id_and_count=[] #记录用户订单中的book_id和count信息
                for i in row:
                    book_id_and_count.append((i.book_id,i.count))
                
                for book_id,count in book_id_and_count:
                    #cursor = self.conn.execute(
                    #    "UPDATE store set stock_level= stock_level + ? "
                    #    "WHERE store_id = ? AND book_id = ?;",
                    #    (count,store_id, book_id))
                    row=self.conn.query(Store.stock_level).filter_by(store_id=store_id,book_id=book_id).first()
                    book_stock_level=row[0]
                    cursor=self.conn.query(Store).filter_by(store_id=store_id,book_id=book_id).update({'stock_level':book_stock_level+count})
                    #self.conn.commit()
                
                #取消订单，status置为-1
                #cursor = self.conn.execute("UPDATE new_order set order_status = ? WHERE order_id = ?",(-1,order_id))
                cursor=self.conn.query(New_order).filter_by(order_id=order_id).update({'order_status':-1})
                #self.conn.commit()
                #if cursor.rowcount==0:
                if cursor==None:
                    return error.error_invalid_order_id(order_id)

            self.conn.commit()
        #except sqlite.Error as e:
        #    return 528, "{}".format(str(e))

        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"    

```

后端逻辑：

取消订单主要分为三种情况讨论，

1. 第一种(order_status=0)：买家还没有付款，此时申请取消订单，要将下单时商铺预留的库存还回去，同时订单取消，order_status置为-1。
2. 第二种(order_status=1)：买家已经付款但是没有发货，此时申请取消订单，要将下单时商铺预留的库存还回去，同时订单取消，卖家向买家退款，买家收钱，卖家退钱；同时订单取消，order_status置为-1。
3. 第三种(order_status=2)：卖家已经发货，此时申请取消订单，不允许取消。

**对于数据库主要执行改和查的操作。**

退款操作需对user表查到买家和卖家的余额（balance），update更新+/-total_price。

order_status置为-1：根据order_id查new_order表，将order_status属性置为-1。

将库存还到店铺：查new_order_detail表，记录用户订单的(book_id,count)对。在store表中根据索引（store_id，book_id）找到书的信息，并对stock_level将库存补回。


#### 2.3 卖家发货
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
            # cursor = self.conn.execute("SELECT user_id,order_id  from new_order where order_id=?", (order_id,))
            # row = cursor.fetchone()
            row = self.conn.query(New_order).filter_by(order_id=order_id).first()
            if row is None:
                return error.error_invalid_order_id()

            #查找订单状态
            # cursor = self.conn.execute("SELECT order_status from new_order where order_id=?", (order_id,))
            # row = cursor.fetchone()

            # if row is None:
            #     return error.error_invalid_order_id(order_id)
            # if row[0] != 1:
            #     return error.error_order_not_dispatched(order_id)
            if row.order_status != 1:
                return error.error_order_not_dispatched(order_id)
            #更新订单状态为2 发货
            # cursor = self.conn.execute("UPDATE new_order set order_status = ?"
            #                       "WHERE order_id = ?",
            #                       (2, order_id))     
            cursor=self.conn.query(New_order).filter_by(order_id = order_id).update({"order_status": 2})
            if cursor == 0:
                return error.error_non_exist_user_id(user_id)
                
            self.conn.commit()
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"
```
实现方法：
先通过 **row = self.conn.query(New_order).filter_by(order_id=order_id).first()**验证订单存在，如果不存在则返回错误码521；**如果订单存在（即订单状态为1）且订单对应用户存在，则将订单状态更改为2**，否则返回错误值error_non_exist_user_id(错误码511)。
send_stock 中，先根据 order_id的条件查询 table New_order 中是否存在目标订单和订单用户，如果订单不存在则返回错误码521，用户不存在返回错误码511。**如果订单存在（即订单状态为1）且订单对应用户存在，则将订单状态更改为2，代表订单已发货。**


#### 2.4 买家收货

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
从路由前台得到 user_id ， password 和add_value；调用 be.model 中 buyer 里的 Buyer 类，调用后端 Buyer 类中的方法 receive_stock 如下，进行异常测试。


```python
def receive_stock(self, user_id: str, password: str, order_id: str):    # -> (int, str)
        try:
            row = self.conn.query(User).filter_by(user_id=user_id).first()
            if row is None:
                return error.error_authorization_fail()
            if row.password != password:
                return error.error_authorization_fail()

            row = self.conn.query(New_order).filter_by(order_id=order_id).first()
            if row is None:
                return error.error_invalid_order_id(order_id)
            if row.order_status!= 2:
                return error.error_order_not_received(order_id)

          
            cursor = self.conn.query(New_order).filter_by(order_id=order_id).update({"order_status": 3})
            if cursor == 0:
                return error.error_invalid_order_id(order_id)
            self.conn.commit()
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"
```
该函数写于buyer.py中。
 后端逻辑：先验证用户密码，**根据 User 中主键 user_id 查询相应密码**，验证密码正确性（若密码错误返回错误码：401），**然后根据 New_order 中主键 order_id 查找对应的订单状态**。如果状态row.order_status不等于2（send_stock中实现的发货），返回报错信息error_order_not_received(order_id)（错误码：520）。**用户手动确认收货之后，将order_status更新为3，代表已收货**。
该会话commit 执行，若成功返回 200。


#### 2.5 订单查询

```python
@bp_buyer.route("/search_orders", methods=["POST"]) 
def search_orders():
    user_id = request.json.get("user_id")
    password = request.json.get("password")
    b = Buyer()
    code, message = b.search_orders(user_id, password)
    return jsonify({"message": message}), code
```

从路由前台得到 user_id和password；调用 be.model 中 buyer 里的 Buyer 类，调用后端 Buyer 类中的方法 search_orders 如下，进行异常测试。

```python
def search_orders (self , user_id : str , password : str):  #-> (int,str)
        try:
            row = self.conn.query(User).filter_by(user_id=user_id).first()
            if row is None:
                return error.error_authorization_fail()
            if row.password != password:
                return error.error_authorization_fail()
 
            rows=self.conn.query(New_order).filter_by(user_id=user_id).all()

            if rows is None :#没有查询到任何订单，报错
                return error.error_non_exist_order_id(user_id)
            
            orders_0=[]#未付款订单
            orders_1=[]#已付款未发货订单  
            orders_2=[]#已发货未收货订单  
            orders_3=[]#已收货订单  
            orders_4=[]#取消过的订单   

            for orders in rows:  #遍历每一个(order_id,order_status)
                status=orders.order_status
                
                row=self.conn.query(New_order_detail).filter_by(order_id=orders.order_id).all()
                for goods in row:   #遍历每个(book_id,count,price...)
                    if status==0:
                        orders_0.append({"user_id":user_id,"order_id":orders.order_id,"book_id":goods.book_id,"count":goods.count,"price":goods.price})
                    elif status==1:
                        orders_1.append({"user_id":user_id,"order_id":orders.order_id,"book_id":goods.book_id,"count":goods.count,"price":goods.price})
                    elif status==2:
                        orders_2.append({"user_id":user_id,"order_id":orders.order_id,"book_id":goods.book_id,"count":goods.count,"price":goods.price})
                    elif status==3:
                        orders_3.append({"user_id":user_id,"order_id":orders.order_id,"book_id":goods.book_id,"count":goods.count,"price":goods.price})
                    elif status==-1:
                        orders_4.append({"user_id":user_id,"order_id":orders.order_id,"book_id":goods.book_id,"count":goods.count,"price":goods.price})
            
            self.conn.commit()        
            list_orders=[orders_0,orders_1,orders_2,orders_3,orders_4]  #总订单
        except BaseException as e:
            print(e)
            return 530, "{}".format(str(e))
        return 200,list_orders  #传回
```
该函数写于buyer.py中。
 后端逻辑：

先验证用户信息与密码，**根据 User 中主键 user_id 验证用户是否存在，查询该user_id对应的密码，**密码为空或错误返回错误码：401。然后**根据 New_order 中主键 根据user_id搜索订单**。如果查询结果为空，返回错误码523。若能查询到对应订单，分别用orders_0代表未付款订单，用orders_1代表已付款未发货订单，用orders_2代表已发货未收货订单，用orders_3代表已收货订单 ，orders_4代表取消过的订单。遍历每一个订单id-订单状态，**对于每个订单id在表New_order_detail中的信息（包括user_id，order_id，book_id，count，price）进行查找并分类到不用的orders_x中**，将查找到的得到的5个orders汇总成一个list_orders，这就是当前用户名下的所有订单。传回list_orders。
该会话commit 执行，若成功返回 200，反之报错。

#### 2.6 卖家改价

```python
#### lsq:新功能：卖家改价
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
从路由前台得到 user_id，store_id，book_id和book_price；调用 be.model 中 seller 里的 Seller 类，调用后端 Seller 类中的方法 set_book_price 如下，进行异常测试。

```python
#### lsq:新功能：卖家改价
    def set_book_price(self, user_id: str,store_id: str,book_id:str,book_price:int): 
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if not self.book_id_exist(store_id, book_id):
                return error.error_non_exist_book_id(book_id)

            self.conn.query(Store).filter_by(store_id = store_id,book_id=book_id).update({"book_price": book_price})
            self.conn.commit()

        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"
```
该函数写于seller.py中。
 后端逻辑：验证用户id，店铺id和店铺中的书籍id参数是否存在，**根据 store表中 store_id 和book_id查找到对应店铺的对应书籍，通过update将书本的price更新到卖家所需要的新价格**。该会话commit 执行，若成功返回 200，反之报错。

#### 2.7 精确搜索图书【by 李思琪】

```python
###lsq:精确搜索书名
@bp_auth.route("/search_title", methods=["POST"])
def search_title():
    search_key=request.json.get("search_key")
    store_id=request.json.get("store_id")
    u=user.User()
    code, message = u.search_title(search_key=search_key,store_id=store_id)
    return jsonify({"message": message}), code
```

```python
###lsq:精确搜索作者名
@bp_auth.route("/search_author", methods=["POST"])
def search_author():
    search_key=request.json.get("search_key")
    store_id=request.json.get("store_id")
    u=user.User()
    code, message = u.search_author(search_key=search_key,store_id=store_id)
    return jsonify({"message": message}), code
```

从路由前台得到search_key和store_id；调用 be.model 中 user 里的 User 类，调用后端 User 类中的方法 search_title 和search_author如下，进行异常测试。

```python
    ###lsq:精确搜索书名
    def search_title(self, search_key:str,store_id:str):
        try:
            page_limit=20
            #全站搜索
            if store_id is None:
                row=self.conn.query(Store).filter_by(title=search_key).all()
                if len(row)==0: #没有找到与输入的书名匹配的书籍
                    return error.error_non_exist_book(search_key) #524
                else:
                    #数据量少则不需要分页
                    if(0<len(row)<=page_limit):
                        result_store=[] #存储售卖该书的商店
                        for i in row:
                            result_store.append(i.store_id)
                    else:
                        #数据量多需要分页
                        total_result=[] #分别存储所有页数据的集合
                        page_cnt=math.ceil(len(row)/page_limit)
                        for i in range(page_cnt):
                            total_result.append([]) #分别存储每一页数据
                            #先排序，按照顺序分页显示，分页显示用到的是limit限制一页的数据量，利用offset做偏移
                            row=self.conn.query(Store).order_by(Store.book_id.asc()).filter(Store.title==search_key).limit(page_limit).offset(i*page_cnt).all()
                            for j in row:
                                total_result[i].append(j)
            #店铺内搜索
            else:
                row=self.conn.query(Store).filter_by(title=search_key,store_id=store_id).all()
                if len(row)==0: #没有找到与输入的书名匹配的书籍
                    return error.error_non_exist_book(search_key) #524
            self.conn.commit()

        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"
```

```python
    ###lsq:精确搜索作者
    def search_author(self, search_key:str, store_id:str):
        try:
            page_limit=20
            #全站搜索
            if store_id is None:
                row=self.conn.query(Store).filter_by(author=search_key).all()
                if len(row)==0: #没有找到输入的作者作品
                    return error.error_non_exist_author(search_key)
                else:
                    #数据量少则不需要分页
                    if(0<len(row)<=page_limit):
                        result_store=[] #存储售卖该书的商店
                        for i in row:
                            result_store.append(i.store_id)
                    else:
                        #数据量多需要分页
                        total_result=[] #分别存储所有页数据的集合
                        page_cnt=math.ceil(len(row)/page_limit)
                        for i in range(page_cnt):
                            total_result.append([]) #分别存储每一页数据
                            #先排序，按照顺序分页显示，分页显示用到的是limit限制一页的数据量，利用offset做偏移
                            row=self.conn.query(Store).order_by(Store.book_id.asc()).filter(Store.author==search_key).limit(page_limit).offset(i*page_cnt).all()
                            for j in row:
                                total_result[i].append(j)
            #店铺内搜索
            else:
                row=self.conn.query(Store).filter_by(author=search_key,store_id=store_id).all()
                if len(row)==0: #没有找到输入的作者作品
                    return error.error_non_exist_author(search_key)
            self.conn.commit()
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"
```

这里，考虑到现实中搜索的应用，例如知网上的论文等等，都是可以分类进行查找的，待查的因素可以选择作者/书名，我写的功能是对书名和作者名进行精确搜索，store_id为空时，进行全局搜索，store_id不为空时，进行店内搜索。当数据量较多时，进行分页显示结果。

精确筛选，即输入是否完全等于用户输入的search_key。

**对数据库的操作：**

以搜书名为例，搜作者名的情况同理。

`row=self.conn.query(Store).filter_by(title=search_key).all()  `根据title=search_key作为筛选条件筛选出多组数据row，类型为list。len(row)计算结果中包含的数据条数，若大于page_limit，则进行分页显示。

```python
#数据量多需要分页
total_result=[] #分别存储所有页数据的集合
page_cnt=math.ceil(len(row)/page_limit)
for i in range(page_cnt):
	total_result.append([]) #分别存储每一页数据
#先排序，按照顺序分页显示，分页显示用到的是limit限制一页的数据量，利用offset做偏移
 	row=self.conn.query(Store).order_by(Store.book_id.asc())
        .filter(Store.author==search_key).limit(page_limit).offset(i*page_cnt).all()
    for j in row:
		total_result[i].append(j)
```

先排序，按照顺序分页显示，分页显示用到的是limit限制一页的数据量，利用offset做偏移。

在搜索中，若从前端路由接收到的store_id不为空，则可以进行店内搜索，若为空则进行全局搜索。

#### 2.8 模糊搜索图书【by 李思琪】

通过like+%的匹配方式，实现了一个简单的模糊搜索，其它与精确搜索的思路一致，前端路由代码如下：

在这里实现了对title、author、tag、content的模糊搜索：

```python
###lsq:模糊搜索title
@bp_auth.route("/search_title_inexact", methods=["POST"])
def search_title_inexact():
    search_key=request.json.get("search_key")
    store_id=request.json.get("store_id")
    u=user.User()
    code, message = u.search_title_inexact(search_key=search_key,store_id=store_id)
    return jsonify({"message": message}), code

###lsq:模糊搜索author
@bp_auth.route("/search_author_inexact", methods=["POST"])
def search_author_inexact():
    search_key=request.json.get("search_key")
    store_id=request.json.get("store_id")
    u=user.User()
    code, message = u.search_author_inexact(search_key=search_key,store_id=store_id)
    return jsonify({"message": message}), code

###lsq:模糊搜索tag
@bp_auth.route("/search_tag_inexact", methods=["POST"])
def search_tag_inexact():
    search_key=request.json.get("search_key")
    store_id=request.json.get("store_id")
    u=user.User()
    code, message = u.search_tag_inexact(search_key=search_key,store_id=store_id)
    return jsonify({"message": message}), code

###lsq:模糊搜索content
@bp_auth.route("/search_content_inexact", methods=["POST"])
def search_content_inexact():
    search_key=request.json.get("search_key")
    store_id=request.json.get("store_id")
    u=user.User()
    code, message = u.search_content_inexact(search_key=search_key,store_id=store_id)
    return jsonify({"message": message}), code
```

前端路由得到输入的关键字（search_key）和商铺ID（store_id）。

后端实现的四个函数为，除了使用like+%，进行数据的匹配之外，其它部分的思路与精确搜索的一致。

```python
###lsq:模糊搜索书名
    def search_title_inexact(self, search_key:str,store_id:str):
        #如果搜索得到的结果数据较多，则需要结果分页
        try:
            page_limit=20
            #全站搜索
            if store_id is None:
                row=self.conn.query(Store).filter(Store.title.like("%"+str(search_key)+"%")).all()
                if len(row)==0: #没有找到与输入的标题信息匹配的书籍
                    return error.error_non_exist_book(search_key) #524
                else:
                    #数据量少则不需要分页
                    if(0<len(row)<=page_limit):
                        result_store=[] #存储售卖该书的商店
                        for i in row:
                            result_store.append(i.store_id)
                    else:
                        #数据量多需要分页
                        total_result=[] #分别存储所有页数据的集合
                        page_cnt=math.ceil(len(row)/page_limit)
                        for i in range(page_cnt):
                            total_result.append([]) #分别存储每一页数据
                            #先排序，按照顺序分页显示，分页显示用到的是limit限制一页的数据量，利用offset做偏移
                            row=self.conn.query(Store).order_by(Store.book_id.asc()).filter(Store.title.like("%"+str(search_key)+"%")).limit(page_limit).offset(i*page_cnt).all()
                            for j in row:
                                total_result[i].append(j)
            #店铺内搜索
            else:
                row=self.conn.query(Store).filter(Store.title.like("%"+str(search_key)+"%"),Store.store_id==store_id).all()
                if len(row)==0: #没有找到与输入的信息匹配的书籍
                    return error.error_non_exist_book(search_key) #524
                else:
                    #数据量少则不需要分页
                    if(0<len(row)<=page_limit):
                        result_store=[] #存储售卖该书的商店
                        for i in row:
                            result_store.append(i.store_id)
                    else:
                        #数据量多需要分页
                        total_result=[] #分别存储所有页数据的集合
                        page_cnt=math.ceil(len(row)/page_limit)
                        for i in range(page_cnt):
                            total_result.append([]) #分别存储每一页数据
                            #先排序，按照顺序分页显示，分页显示用到的是limit限制一页的数据量，利用offset做偏移
                            row=self.conn.query(Store).order_by(Store.book_id.asc()).filter(Store.title.like("%"+str(search_key)+"%"),Store.store_id==store_id).limit(page_limit).offset(i*page_cnt).all()
                            for j in row:
                                total_result[i].append(j)
            self.conn.commit()
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"
```

```python
    ###lsq:模糊搜索作者
    def search_author_inexact(self, search_key:str,store_id:str):
        #如果搜索得到的结果数据较多，则需要结果分页
        try:
            page_limit=20
            #全站搜索
            if store_id is None:
                row=self.conn.query(Store).filter(Store.author.like('%'+search_key+'%')).all()
                if len(row)==0: #没有找到与输入的作者信息匹配的书籍
                    return error.error_non_exist_author(search_key) #525
                else:
                    #数据量少则不需要分页
                    if(0<len(row)<=page_limit):
                        result_store=[] #存储售卖该书的商店
                        for i in row:
                            result_store.append(i.store_id)
                    else:
                        #数据量多需要分页
                        total_result=[] #分别存储所有页数据的集合
                        page_cnt=math.ceil(len(row)/page_limit)
                        for i in range(page_cnt):
                            total_result.append([]) #分别存储每一页数据
                            #先排序，按照顺序分页显示，分页显示用到的是limit限制一页的数据量，利用offset做偏移
                            row=self.conn.query(Store).order_by(Store.book_id.asc()).filter(Store.author.like('%'+search_key+'%')).limit(page_limit).offset(i*page_cnt).all()
                            for j in row:
                                total_result[i].append(j)
                            
            #店铺内搜索
            else:
                row=self.conn.query(Store).filter(Store.author.like('%'+search_key+'%'),Store.store_id==store_id).all()
                if len(row)==0: #没有找到与输入的信息匹配的书籍
                    return error.error_non_exist_author(search_key) #525
                else:
                    #数据量少则不需要分页
                    if(0<len(row)<=page_limit):
                        result_store=[] #存储售卖该书的商店
                        for i in row:
                            result_store.append(i.store_id)
                    else:
                        #数据量多需要分页
                        total_result=[] #分别存储所有页数据的集合
                        page_cnt=math.ceil(len(row)/page_limit)
                        for i in range(page_cnt):
                            total_result.append([]) #分别存储每一页数据
                            #先排序，按照顺序分页显示，分页显示用到的是limit限制一页的数据量，利用offset做偏移
                            row=self.conn.query(Store).order_by(Store.book_id.asc()).filter(Store.author.like('%'+search_key+'%'),Store.store_id==store_id).limit(page_limit).offset(i*page_cnt).all()
                            for j in row:
                                total_result[i].append(j)
            self.conn.commit()
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"
```

```python
    ###lsq:模糊搜索tag
    def search_tag_inexact(self, search_key:str,store_id:str):
        #如果搜索得到的结果数据较多，则需要结果分页
        try:
            page_limit=20
            #全站搜索
            if store_id is None:
                row=self.conn.query(Store).filter(Store.tag.like('%'+search_key+'%')).all()
                if len(row)==0: #没有找到与输入的作者信息匹配的书籍
                    return error.error_non_exist_tag(search_key) #526
                else:
                    #数据量少则不需要分页
                    if(0<len(row)<=page_limit):
                        result_store=[] #存储售卖该书的商店
                        for i in row:
                            result_store.append(i.store_id)
                    else:
                        #数据量多需要分页
                        total_result=[] #分别存储所有页数据的集合
                        page_cnt=math.ceil(len(row)/page_limit)
                        for i in range(page_cnt):
                            total_result.append([]) #分别存储每一页数据
                            #先排序，按照顺序分页显示，分页显示用到的是limit限制一页的数据量，利用offset做偏移
                            row=self.conn.query(Store).order_by(Store.book_id.asc()).filter(Store.tag.like('%'+search_key+'%')).limit(page_limit).offset(i*page_cnt).all()
                            for j in row:
                                total_result[i].append(j)
                            
            #店铺内搜索
            else:
                row=self.conn.query(Store).filter(Store.tag.like('%'+search_key+'%'),Store.store_id==store_id).all()
                if len(row)==0: #没有找到与输入的信息匹配的书籍
                    return error.error_non_exist_tag(search_key) #526
                else:
                    #数据量少则不需要分页
                    if(0<len(row)<=page_limit):
                        result_store=[] #存储售卖该书的商店
                        for i in row:
                            result_store.append(i.store_id)
                    else:
                        #数据量多需要分页
                        total_result=[] #分别存储所有页数据的集合
                        page_cnt=math.ceil(len(row)/page_limit)
                        for i in range(page_cnt):
                            total_result.append([]) #分别存储每一页数据
                            #先排序，按照顺序分页显示，分页显示用到的是limit限制一页的数据量，利用offset做偏移
                            row=self.conn.query(Store).order_by(Store.book_id.asc()).filter(Store.tag.like('%'+search_key+'%'),Store.store_id==store_id).limit(page_limit).offset(i*page_cnt).all()
                            for j in row:
                                total_result[i].append(j)
            self.conn.commit()
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"
```

```python
    ###lsq:模糊搜索content
    def search_content_inexact(self, search_key:str,store_id:str):
        #如果搜索得到的结果数据较多，则需要结果分页
        try:
            page_limit=20
            #全站搜索
            if store_id is None:
                row=self.conn.query(Store).filter(Store.content.like('%'+search_key+'%')).all()
                if len(row)==0: #没有找到与输入的目录信息匹配的书籍
                    return error.error_non_exist_content(search_key) #527
                else:
                    #数据量少则不需要分页
                    if(0<len(row)<=page_limit):
                        result_store=[] #存储售卖该书的商店
                        for i in row:
                            result_store.append(i.store_id)
                    else:
                        #数据量多需要分页
                        total_result=[] #分别存储所有页数据的集合
                        page_cnt=math.ceil(len(row)/page_limit)
                        for i in range(page_cnt):
                            total_result.append([]) #分别存储每一页数据
                            #先排序，按照顺序分页显示，分页显示用到的是limit限制一页的数据量，利用offset做偏移
                            row=self.conn.query(Store).order_by(Store.book_id.asc()).filter(Store.content.like('%'+search_key+'%')).limit(page_limit).offset(i*page_cnt).all()
                            for j in row:
                                total_result[i].append(j)
                            
            #店铺内搜索
            else:
                row=self.conn.query(Store).filter(Store.content.like('%'+search_key+'%'),Store.store_id==store_id).all()
                if len(row)==0: #没有找到与输入的信息匹配的书籍
                    return error.error_non_exist_content(search_key) #527
                else:
                    #数据量少则不需要分页
                    if(0<len(row)<=page_limit):
                        result_store=[] #存储售卖该书的商店
                        for i in row:
                            result_store.append(i.store_id)
                    else:
                        #数据量多需要分页
                        total_result=[] #分别存储所有页数据的集合
                        page_cnt=math.ceil(len(row)/page_limit)
                        for i in range(page_cnt):
                            total_result.append([]) #分别存储每一页数据
                            #先排序，按照顺序分页显示，分页显示用到的是limit限制一页的数据量，利用offset做偏移
                            row=self.conn.query(Store).order_by(Store.book_id.asc()).filter(Store.content.like('%'+search_key+'%'),Store.store_id==store_id).limit(page_limit).offset(i*page_cnt).all()
                            for j in row:
                                total_result[i].append(j)
            self.conn.commit()
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"     

```



#### 2.9 搜索图书【by 严寒】

**由于最后运行的后端代码以及测试中，没有加入这部分内容，所以在此位置展示：**

用户可以通过关键字搜索到想要的图书，搜索范围包括题目，作者，标签，店铺名称；全站搜索和是当前店铺搜索。
**初步实现**：

```python
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
                    cursor = self.conn.execute("SELECT book_id from store where title=?", (title,))
                    row = cursor.fetchone()
                    if row is None:
                        return error.error_non_exist_title(title)
                    
                    sql += " title = ?"
                else:
                    sql += " and title = ?"
                values.append(title)
                have_restrict = 1

            if author is not None:
                if have_restrict == 0:
                    cursor = self.conn.execute("SELECT book_id from store where author=?", (author,))
                    row = cursor.fetchone()
                    if row is None:
                        return error.error_non_exist_auth(author)
                    sql += " author like ?"
                else:
                    sql += " and author like ?"
                values.append("%" + author + "%")
                have_restrict = 1

            if tag is not None:
                if have_restrict == 0:
                    cursor = self.conn.execute("SELECT book_id from store where tag=?", (tag,))
                    row = cursor.fetchone()
                    if row is None:
                        return error.error_non_exist_tag(tag)
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
# 如果指定了store_id就是店内搜索，没指定就是全场搜索。
```
搜索函数写在user.py中，
**执行逻辑**：
用户输入title（书名）：（）, author（作者）：（）, tag（标签）: （）, store_id（店铺ID）（）：，这些参数可以部分为空。通过搜索得到目标书籍的全部信息。
实现方法：用户输入参数后，首先判断用户的输入参数齐全，如果全部为有效输入，则直接通过title在指定店铺中查找书籍。当店铺ID输入为空时，搜索范围是全数据库；当店铺ID有正确输入时，搜索范围是指定的店铺。一旦输入参数有缺失，我们将分别通过title、author和tag进行搜索。以author为例，首先判断author不为空，这是执行后续的关键。接着判断thave_restrict，如果have_restrict == 1，说明在前一步我们已经得到有效的限制条件，have_restrict == 1，这时sql语句记录的就是" and author like XXX"，信息已经直接得到；而如果thave_restrict == 0，说明在前面的过程中我们没有得到可以约束的条件，author就是目前可以判断具体书籍的参数，我们需要从数据库里选出作者为输入的author的书籍。
在数据库中搜索判断要求是否存在，如果不存在，返回错误函数error_non_exist_author(author)，打印错误值522。这时thave_restrict依然为0，因为我们目前还没有得到可以查询到需求书籍的参数；如果存在，sql记录" author like ?"，用一个append把该属性填进去，将thave_restrict 更改为1。
上述的author关键字我们采用了模糊查询，即like+%模式。这里参考了一篇博文[like % %模糊查询](https://blog.csdn.net/qq_39207963/article/details/122110128?ops_request_misc=&request_id=&biz_id=102&utm_term=%E4%B8%8D%E7%A1%AE%E5%AE%9A%E5%80%BClike%E6%A8%A1%E7%B3%8A%E6%90%9C%E7%B4%A2&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduweb~default-0-122110128.142%5Ev68%5Epc_rank_34_queryrelevant25,201%5Ev4%5Eadd_ask,213%5Ev2%5Et3_control2&spm=1018.2226.3001.4187)。而对于title，我们采用的是精确查询。

**测试**：

**严寒这部分代码受be.db限制，若在助教老师本地运行，可能测试不了，会有报错。因为其查询的是be.db(sqlite数据库)中store表的数据，store表插入时，插入的书籍信息和store_id都是随机的。**

```python
import pytest
import time
from fe.access import search
from fe.access import book
from fe import conf

class TestSearch:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        # do before test
        # self.title = "这个测试到底能不能过了"
        # self.title = None
        # self.store_id = "store_s_1_1_360cf0ce-7459-11ed-8d67-acde48001122"
        # # self.author = "张乐平"
        # self.author = "朔间零"
        # self.tag = "儿童文学"
        # self.content = "彼得・潘出现了"
        
        self.title = "袁氏当国"
        # self.title = None
        self.store_id = "test_add_book_stock_level1_store_458e933c-756b-11ed-a55f-367dda5b2985"
        self.author = "[美] 唐德刚"
        self.tag = "近代史"
        self.content = "――民国开国史简论"

        self.mysearch = search.Search(conf.URL)
        yield
        # do after test

    # def test_param_ok(self):
    #     code = self.mysearch.param_search(title=self.title, author=self.author, tags=self.tags)
    #     assert code == 200

    #     code = self.mysearch.param_search(title=self.title, author=self.author, tags=self.tags, store_id=self.store_id)
    #     assert code == 200

    # def test_content_ok(self):
    #     code = self.mysearch.content_search(sub_content=self.subcontent)
    #     assert code == 200

    #     code = self.mysearch.content_search(sub_content=self.subcontent, store_id=self.store_id)
    #     assert code == 200
            
    def test_param_whole_ok(self):
        code = self.mysearch.param_search(self.title, self.author, self.tag)
        assert code == 200
    def test_param_instore_ok(self):
        code = self.mysearch.param_search(self.title, self.author, self.tag, self.store_id)
        assert code == 200
        
    # def test_content_ok(self):
    #     code = self.mysearch.content_search(self.content)
    #     assert code == 200

        # code = self.mysearch.content_search(self.content, self.store_id)
        # assert code == 200
```

1. 全部参数（title、author、tag、content、store_id）输入时：
   ![请添加图片描述](https://img-blog.csdnimg.cn/85a27f001ac143d3b3f67fbde05dd019.png)
   title精确查询测试成功。

2. 当我们指定图书但使title=None时，测试结果：

![请添加图片描述](https://img-blog.csdnimg.cn/fd9da0beb9c64e4b9e53296536a50b2e.png)

author模糊搜索成功。

3. 当title为不存在书名时，测试报错：
   ![请添加图片描述](https://img-blog.csdnimg.cn/f4e7b33aa5ed4502b47d70ad0883576d.png)
   逻辑完整。
   由此，精确查询和模糊查询都得到实现。

## 五、优化数据库执行性能分析

**在本次项目中，我们采用的优化数据库执行性能分析的手段如下：**

**1. 索引：利用索引进行搜索可以提高数据库查询的效率** 
在我们的项⽬中，具体的index建⽴如下： 
user 的user_id
user_store 的user_id , store_id
store 的store_id，book_id
new_order 的order_id
new_order_detail 的order_id，book_id

**2. 冗余但能提升效率的表的属性:**

new_order中的total_price属性：可以用new_order中的total_price+=count*price来作为替代，但是计算完total_price直接存入new_order表中，在涉及到退款等关系到订单总价的功能时，可以避免遍历new_order_detail中的大量数据，性能有所提高。

**3. 在事务处理方面：**

我们在对每一个功能的后端函数都新建了一个会话，并在函数结束时commit，以保证事务完成的原子性。也尝试过只建一个会话，但是事务处理的时间明显变长，代码测试卡住出不来，可能是由于数据的死锁占用了大量时间。



**了解到的在本项目中可以应用的提高性能的手段：**

**1. 多建表，存储的数据量没有变，但可以减少对一张表的遍历次数**

比如，对于查询历史订单这个功能，在实现上可以采取，从new_order中将已经结束的订单分离出来，单独建一张表，

finished_order(order_id,user_id,store_id,total_price,time) ，并且从new_order表中将历史订单，即order_status=3（买家已收货）的订单从new_order中delete。

**2. 查询功能的实现：建立全文索引**

全文索引，也即倒排表，原理是先根据现在的数据建立一个词库，然后在每篇文档中（在本次实验中就是content），计算每个词出现的频率，并记录位置，把频率和位置信息按照词库的顺序归纳，就对文档形成了一个以词库为目录的索引，这样查找一个词的时候就可以很快地找到位置。

在本次实验中，对于模糊搜索的应用，除了像我们采取的用like+%来搜索的方法之外，就可以利用倒排表进行索引，可以很大程度地提升效率。like+%的模糊搜索方法将导致进行全表扫描而放弃使用索引。

**3. 关于索引的更多了解**

建立索引与全表扫描相比，可以极大地提升搜索的效率，所以在实现功能的时候，应当考虑如何建立索引而避免全表扫描。了解到的可以采用的方法如下：

- 考虑在where以及order by涉及筛选的列上建立索引。
- 避免在where语句中对可为空的字段进行判断，这将导致引擎放弃使用索引而进行全表扫描。
- 在where语句中，慎用 != 或<或>操作符，避免条件or的连接，避免对字段进行表达式操作，慎用in或者not in 以及like+%的查询，以上都将导致引擎放弃使用索引而进行全表扫描。
- 在新建表时，如果一次性插入很大量的数据，可以使用select into代替create table，避免产生大量log。
- ....（更多可以参考http://blog.itpub.net/31555484/viewspace-2565387/）



## 六、git 版本管理

**说明：**

1. 代码仓库链接：https://github.com/bookstore-team/bookstore-
2. 由于陈柏延和严寒的github偶尔加载不出，所以部分代码由李思琪代为上传。
3. Github截图和commit记录截图（部分）如下：

![请添加图片描述](https://img-blog.csdnimg.cn/8dafd5c4784b4dc189838185fccf6a31.jpeg)

![请添加图片描述](https://img-blog.csdnimg.cn/b6a59979a7594265bcebe179d7883330.jpeg)



## 七、所有功能都实现后的测试结果和覆盖率测试

**说明：**

1. 总共设计了70个接口测试的情况，具体接口测试的说明分别在报告\auth.pdf，报告\buyer.pdf和报告\seller.pdf中展示。
2. 对于70个接口测试，全部passed，并且覆盖率达到91%。通过检查coverage生成的index.html文件(2022_CDMS_PJ2_第7组\报告\htmlcov\index.html)发现，没有覆盖的部分都是一些异常情况的return。

![image-20221209071824513](C:\Users\huawei\AppData\Roaming\Typora\typora-user-images\image-20221209071824513.png)

![image-20221209071854182](C:\Users\huawei\AppData\Roaming\Typora\typora-user-images\image-20221209071854182.png)
![image-20221209071928893](C:\Users\huawei\AppData\Roaming\Typora\typora-user-images\image-20221209071928893.png)

## 八、小组分工

陈柏延：ER图&数据库设计（40%）、前60%功能的ORM改写以及创建和连接postgresql数据库（75%）；超时自动取消订单、卖家发货、买家收货、不同类型的订单查询功能【用ORM】以及其对应的接口测试（100%）；报告中前60%的author基础功能、卖家发货、订单查询和自动取消订单功能的实现介绍以及接口介绍（20%）。

李思琪：ER图&数据库设计（60%）、前60%功能的ORM改写以及创建和连接postgresql数据库（25%）；买家手动取消订单、卖家改价、精确搜索图书、模糊搜索图书功能（包括全局搜索和店内搜索，以及分页）【用ORM】以及其对应的接口测试（100%）；报告细节的修改、搜索和取消订单的介绍、优化数据库性能分析、ORM（35%）。

严寒：全局搜索和店内搜索图书功能以及其对应的接口测试（通过）、报告seller和buyer前60%的实现介绍和买家发货、卖家改价的实现介绍（45%）

**最终的量化贡献率：陈柏延（40%），李思琪（40%），严寒（20%）**

**说明：**

**由于搜索功能最初分配是给严寒，其最终只实现了sqlite数据库的根据title的精确搜索和根据author和tag的模糊搜索，这几种参数搜索的全局搜索和店内搜索，以及其认为合理的接口测试。**

**李思琪最终独自实现了postgreSQL数据库的根据title、author的分类精确搜索，和根据title、author、tag、content的分类模糊搜索，实现了数据量较大时的分页。另外，也实现了这几种搜索的全局搜索和店内搜索，以及其认为合理的相应的测试接口。**

## 九、总结

1. 李思琪: 通过这次bookstore项目所有功能的实现，锻炼了我使用ORM连接到数据库进行数据库的操作的能力，我们在完成项目的过程中，先做了sqlite数据库的尝试，然后又改写为ORM操作和Postgresql的方式。对于表索引和选择有意义的数据冗余有了更深的了解，也学习了优化数据库执行性能能力的方法，包括查询性能和事务处理的几个角度。对于如何来做接口测试，也掌握得更加熟练。
1. 严寒：在本次实验里尝试了搜索方式的实现，加强了关于数据库的理解。由于个人原因表现并不令自己满意，感谢队友的协助和包容，后续课程里会调整状态，在数据管理的实践操作上加强自己的能力。
1. 陈柏延：
