## 注册用户

#### URL：

POST http://$address$/auth/register

#### Request

Body:

```
{
    "user_id":"$user name$",
    "password":"$user password$"
}
```

| 变量名   | 类型   | 描述     | 是否可为空 |
| -------- | ------ | -------- | ---------- |
| user_id  | string | 用户名   | N          |
| password | string | 登陆密码 | N          |

#### Response

Status Code:

| 码  | 描述                 |
| --- | -------------------- |
| 200 | 注册成功             |
| 512 | 注册失败，用户名重复 |
| 530 | 无效参数             |

Body:

```
{
    "message":"$error message$"
}
```

| 变量名  | 类型   | 描述                       | 是否可为空 |
| ------- | ------ | -------------------------- | ---------- |
| message | string | 返回错误消息，成功时为"ok" | N          |

## 注销用户

#### URL：

POST http://$address$/auth/unregister

#### Request

Body:

```
{
    "user_id":"$user name$",
    "password":"$user password$"
}
```

| 变量名   | 类型   | 描述     | 是否可为空 |
| -------- | ------ | -------- | ---------- |
| user_id  | string | 用户名   | N          |
| password | string | 登陆密码 | N          |

#### Response

Status Code:

| 码  | 描述                               |
| --- | ---------------------------------- |
| 200 | 注销成功                           |
| 401 | 注销失败，用户名不存在或密码不正确 |
| 530 | 无效参数                           |

Body:

```
{
    "message":"$error message$"
}
```

| 变量名  | 类型   | 描述                       | 是否可为空 |
| ------- | ------ | -------------------------- | ---------- |
| message | string | 返回错误消息，成功时为"ok" | N          |

## 用户登录

#### URL：

POST http://$address$/auth/login

#### Request

Body:

```
{
    "user_id":"$user name$",
    "password":"$user password$",
    "terminal":"$terminal code$"
}
```

| 变量名   | 类型   | 描述     | 是否可为空 |
| -------- | ------ | -------- | ---------- |
| user_id  | string | 用户名   | N          |
| password | string | 登陆密码 | N          |
| terminal | string | 终端代码 | N          |

#### Response

Status Code:

| 码  | 描述                       |
| --- | -------------------------- |
| 200 | 登录成功                   |
| 401 | 登录失败，用户名或密码错误 |
| 530 | 无效参数                   |

Body:

```
{
    "message":"$error message$",
    "token":"$access token$"
}
```

| 变量名  | 类型   | 描述                                                                  | 是否可为空   |
| ------- | ------ | --------------------------------------------------------------------- | ------------ |
| message | string | 返回错误消息，成功时为"ok"                                            | N            |
| token   | string | 访问 token，用户登录后每个需要授权的请求应在 headers 中传入这个 token | 成功时不为空 |

#### 说明

1.terminal 标识是哪个设备登录的，不同的设备拥有不同的 ID，测试时可以随机生成。

2.token 是登录后，在客户端中缓存的令牌，在用户登录时由服务端生成，用户在接下来的访问请求时不需要密码。token 会定期地失效，对于不同的设备，token 是不同的。token 只对特定的时期特定的设备是有效的。

## 用户更改密码

#### URL：

POST http://$address$/auth/password

#### Request

Body:

```
{
    "user_id":"$user name$",
    "oldPassword":"$old password$",
    "newPassword":"$new password$"
}
```

| 变量名      | 类型   | 描述         | 是否可为空 |
| ----------- | ------ | ------------ | ---------- |
| user_id     | string | 用户名       | N          |
| oldPassword | string | 旧的登陆密码 | N          |
| newPassword | string | 新的登陆密码 | N          |

#### Response

Status Code:

| 码  | 描述         |
| --- | ------------ |
| 200 | 更改密码成功 |
| 401 | 更改密码失败 |
| 530 | 无效参数     |

Body:

```
{
    "message":"$error message$",
}
```

| 变量名  | 类型   | 描述                       | 是否可为空 |
| ------- | ------ | -------------------------- | ---------- |
| message | string | 返回错误消息，成功时为"ok" | N          |

## 用户登出

#### URL：

POST http://$address$/auth/logout

#### Request

Headers:

| key   | 类型   | 描述       |
| ----- | ------ | ---------- |
| token | string | 访问 token |

Body:

```
{
    "user_id":"$user name$"
}
```

| 变量名  | 类型   | 描述   | 是否可为空 |
| ------- | ------ | ------ | ---------- |
| user_id | string | 用户名 | N          |

#### Response

Status Code:

| 码  | 描述                          |
| --- | ----------------------------- |
| 200 | 登出成功                      |
| 401 | 登出失败，用户名或 token 错误 |
| 530 | 无效参数                      |

Body:

```
{
    "message":"$error message$"
}
```

| 变量名  | 类型   | 描述                       | 是否可为空 |
| ------- | ------ | -------------------------- | ---------- |
| message | string | 返回错误消息，成功时为"ok" | N          |

## 用户按照书名全局/店内精确搜索

#### URL:

POST http://$address$/auth/search_title

#### Request

Body:

```json
{
    "search_key":"search_key",
    "store_id":"store_id"
}

```

属性说明：

| key        | 类型   | 描述                               | 是否可为空 |
| ---------- | ------ | ---------------------------------- | ---------- |
| search_key | string | 用户输入的搜索关键词（此时为书名） | N          |
| store_id   | string | 书店店铺ID                         | Y          |

#### Response

| 码  | 描述                                   |
| --- | -------------------------------------- |
| 200 | 能找到与用户输入的search_key匹配的书籍 |
| 524 | 没有与用户输入的search_key匹配的书籍   |

##### 说明：

1. store_id可为空，当其为空时，说明此时正在进行全局搜索；若不为空，则说明正在某家店铺中进行店内搜索。
2. 考虑到店内搜索，应当是进入店铺后执行的，所以不考虑店铺名不存在的情况。

## 用户按照作者名全局/店内精确搜索

#### URL:

POST http://$address$/auth/search_author

#### Request

Body:

```json
{
    "search_key":"search_key",
    "store_id":"store_id"
}

```

属性说明：

| key        | 类型   | 描述                                 | 是否可为空 |
| ---------- | ------ | ------------------------------------ | ---------- |
| search_key | string | 用户输入的搜索关键词（此时为作者名） | N          |
| store_id   | string | 书店店铺ID                           | Y          |

#### Response

| 码  | 描述                                       |
| --- | ------------------------------------------ |
| 200 | 能找到与用户输入的search_key匹配的作者作品 |
| 525 | 没有与用户输入的search_key匹配的作者作品   |

##### 说明：

1. store_id可为空，当其为空时，说明此时正在进行全局搜索；若不为空，则说明正在某家店铺中进行店内搜索。
2. 考虑到店内搜索，应当是进入店铺后执行的，所以不考虑店铺名不存在的情况。
