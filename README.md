# mycity
a online education sysytem based on Django+Vue


## 项目简介

在线教育平台

<!--more-->

**软件依赖：**

- WEB框架：Django（1.11.7）、Django REST framework
- 前端框架：Vue（2.5.16）
- 数据库: MySql、redis
- 支付平台：支付宝
- 消息推送平台：微信服务号，电子邮件

**主要功能如下：**

- 允许学生注册、登陆
- 浏览本在线教育平台所提供的课程列表、课程介绍（课程大纲，）
- 学生将课程加入购物车
- 完成购物后，进入结算中心，通过支付宝支付购买课程
- 完成课程购买后，分配导师
- 开始学习，观看本站提供的教学视频
- 通过答疑系统，提交学习中遇到的问题，与同学讨论或者导师答疑
- 完成章节学习后，提交作业
- 导师批改作业并打分
- 模块学习完成后进行考核

## 项目意义

**目标：**

通过互联技术，变革传统教育方式，依赖强大的导师服务系统，提高在线教育的效率与成功率。

**项目策略:**

- 提供具有时间限制的教学服务
- 安排合理的模块化学习
- 聘用高素质的导师，提供优质服务
- 导师对学员一对一在线考核
- 学习周期中全程导师监督（跟进记录）
- 提供高效的答疑解惑服务（12小时）
- 建立完善的奖学金制度
  - 是否按学习计划完成学业
  - 每章节作业完成情况

 

## 项目开发团队与进度

**团队构成：**

- 开发
  - 导师后台，stark组件+rbac ： 1人
  - 管理后台，stark组件+rbac ： 1人
  - 主站
    - vue.js 1人
    - api 村长+1/2文州+1/2Alex+其他 + 村长
- 运维(1人)
- 测试(1人)
- 产品经理(1人)
- UI设计(1人)
- 运营(1人)
- 销售(4人)
- 全职导师(2人)
- 签约讲师（...）

**周期：**

- 7月份项目开始
- 11月份上线
- 11月份~次年5月份： 修Bug，活动支持，广告。。。
- 6月份：开发题库系统

## 数据库设计

**简要描述如下：**

- 课程（13表）
  - 课程大类
  - 课程子类
  - 学位课
    - 讲师
    - 奖学金
  - 专题课（学位课模块表）
  - 价格策略(contenttype)
  - 课程详细(o2o -> 水平分表)
  - 常见问题
  - 课程大纲
  - 章节
  - 课时
  - 作业
- 深科技（4+2）
  - 用户表
  - 用户token
  - 文章来源
  - 文章表
  - 通用评论表
  - 通用收藏表
- 支付相关（4+2）
  - 优惠券表
  - 订单表
  - 订单详情表
  - 文章表
  - 通用评论表
  - 通用收藏表

**Django中实现:**

![img](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif) models.py

 

## 支付流程复盘

支付需求起始于用户点击立即支付或者加入购物车

### 1.添加到购物车

当用户选择需要购买的课程和价格策略后，有两种方式购买课程:

### **1.1 立即购买**

将课程id和选择的价格策略放到redis中，跳到去支付页面，从redis中获取购买课程的id和价格策略id,如果该用户要使用优惠券和贝利,则选择当前用户所拥有并且未使用和没过期的优惠券,得到折后价格,点击去支付完成支付,

### **1.2 添加到购物车中完成支付(post)**

前端需要提供的数据包括：所选课程的id和所选择的价格策略id。约定的数据格式如下：

```
{
    "course_id":1,
    "policy_id":3
}
```

后端获取到所选课程的id和所选择的价格策略id，根据课程id获取到当前课程,然后根据当前课程获取到当前课程所有的价格策略,判断在后端获取到的价格策略id在不在当前课程的价格策略中,不在的话则抛出异常价格策略不存在，在的话继续执行，将该课程所有价格策略的id，时间周期和价格存放到price_policy_list中

```
# 1.在这里获得用户的课程ID与价格策略ID
course_id = int(request.data.get('course_id'))
policy_id = int(request.data.get('policy_id'))

# 2. 获取专题课信息
course = models.Course.objects.get(id=course_id)

# 3.获取课程相关的所有价格策略
price_policy_list = course.price_policy.all()
price_policy_dict = {}
for item in price_policy_list:
    price_policy_dict[item.id] = {
        "period": item.valid_period,
        "period_display": item.get_valid_period_display(),
        "price": item.price
    }
if policy_id not in price_policy_dict:
    raise PricePolicyInvalid('价格策略不合法')
```

 

继续将该课程的所有信息主要包括:课程id,课程图片地址,课程标题，所有价格策略，默认价格策略封装在car_dict中

下面是redis中保存用户数据的key

```
SHOPPING_CART_KEY = "luffy_shopping_cart_%s_%s"
PAYMENT_KEY = "luffy_payment_%s_%s"
PAYMENT_COUPON_KEY = "luffy_payment_coupon_%s"
```

 

```
car_key = settings.SHOPPING_CART_KEY % (request.auth.user_id, course_id,)
car_dict = {
    'title': course.name,
    'img': course.course_img,
    'default_policy': policy_id,
    'policy': json.dumps(price_policy_dict)
}
```

完成后，在redis中用户购物车的数据如下：

```
{
    luffy_shopping_car_6_11:{
        'title':'21天入门到放弃',
        'src':'xxx.png',
        'policy':{
            1:{id:'xx'.....},
            2:{id:'xx'.....},
            3:{id:'xx'.....},
            4:{id:'xx'.....},
        },
        'default_policy':3
    },
    luffy_shopping_car_6_13:{
        ...
    }
}
```

修改购物车总的价格策略(patch):

向后台发课程id和要修改为的价格策略id,判断课程是否在购物车中,判断传递过来的价格策略是否在当前课程的价格策略中,在的话将 redis中的当前课程的默认价格策略修改为当前的价格策略具体将上面代码

 

## 结算中心

在用户完成购物车的后，点击结算，前端服务器发送结算数据（"courseids":["1","2"]，1和2对应的就是课程的ID）给我们后端的Django服务器，约定的数据格如下：

```
{
    "courseids":["1","2"]
}
```

**1.获取用户提交的课程id, [1,2]**

判断是否选择要结算的课程,没选择则抛出异常

```
course_id_list = request.data.get('course_list')
if not course_id_list or not isinstance(course_id_list, list):
    raise Exception('请选择要结算的课程')
```

**2.检测购物车中检查是否已经有课程（应该有课程的）**

```
product_dict = redis_pool.conn.hget(settings.LUFFY_SHOPPING_CAR, request.user.id)
if not product_dict:
    raise Exception('购物车无课程')
```

**3.检测购物车中是否有用户要购买的课程**

```
            product_dict = json.loads(product_dict.decode('utf-8'))

            # ###### 课程、价格和优惠券 #######
            policy_course_dict = {}

            # 循环用户传递过来的要结算的课程ID列表
            for course_id in course_id_list:
                course_id = str(course_id)
                product = product_dict.get(course_id)
                if not product:
                    raise Exception('购买的课程必须先加入购物车')
```

如果所结算的课程在购物车中，

4.**获取选中价格策略的价格详细，**

选择购物车中当前课程下的所有价格策略和当前课程的所选择的价格策略相等的价格策略，获取其信息,

```
            # c. 购物车中是否有用户要购买的课程
            product_dict = json.loads(product_dict.decode('utf-8'))

            # ###### 课程、价格和优惠券 #######
            policy_course_dict = {}

            # 循环用户传递过来的要结算的课程ID列表
            for course_id in course_id_list:
                course_id = str(course_id)
                product = product_dict.get(course_id)
                if not product:
                    raise Exception('购买的课程必须先加入购物车')

                # 获取选中价格策略的价格详细
                policy_exist = False
                for policy in product['price_policy_list']:
                    if policy['id'] == product['choice_policy_id']:
                        policy_price = policy['price']
                        policy_period = policy['period']
                        policy_valid_period = policy['valid_period']
                        policy_exist = True
                        break
                if not policy_exist:
                    raise Exception('购物车中的课程无此价格')
```

将上面我们获取的课程信息和价格策略信息封装在policy_course中

```
                policy_course = {
                    'course_id': course_id,
                    'course_name': product['name'],
                    'course_img': product['course_img'],
                    'policy_id': product['choice_policy_id'],
                    'policy_price': policy_price,
                    'policy_period': policy_period,
                    'policy_valid_period': policy_valid_period,
                    'default_coupon_id': 0,
                    'coupon_record_list': {
                        0:{'id': 0, 'text': '请选择优惠券'},
                    },
                }
```

**5.获取当前用户所有的优惠券**

```
  user_coupon_list = models.CouponRecord.objects.filter(account=request.user,status=0)
```

**6.区分用户的优惠券种类,课程优惠券添加到课程中；全局优惠券添加到全局**

```
  # ###### 全局优惠券 #######
            global_coupon_record_dict = {}
```

循环遍历当前用户的所有优惠券,判断他们是否过期

```
                begin_date = record.coupon.valid_begin_date
                end_date = record.coupon.valid_end_date
                if begin_date:
                    if current_date < begin_date:
                        continue
                if end_date:
                    if current_date > end_date:
                        continue
```

 

,如果没过期,判断他们是全局优惠券还是针对某个课程的优惠券,区分好是什么优惠券以后还的区分该优惠券是什么类型，

如果是通用券

```
 if record.coupon.coupon_type == 0:
                        temp = {'type': 0, 'text': "通用优惠券", 'id': record.id,
                                'begin_date': begin_date, 'end_date': end_date,
                                'money_equivalent_value': record.coupon.money_equivalent_value}
```

如果是满减券:

```
  elif record.coupon.coupon_type == 1:
                        temp = {'type': 1, 'text': "满减券", 'id': record.id,
                                'begin_date': begin_date, 'end_date': end_date,
                                'minimum_consume': record.coupon.minimum_consume,
                                'money_equivalent_value': record.coupon.money_equivalent_value}
```

如果是折扣券：

```
 elif record.coupon.coupon_type == 2:
                        temp = {'type': 2, 'text': "折扣券", 'id': record.id,
                                'begin_date': begin_date, 'end_date': end_date,
                                'off_percent': record.coupon.off_percent}
```

如果是全局优惠券,则

```
global_coupon_record_dict[record.id] = temp
```

如果但是针对课程的优惠券：

```
 policy_course_dict[cid]['coupon_record_list'][record.id] = temp
```

最后将所有数据封装在user_pay中放到redis上

```
user_pay = {
                'policy_course_dict': policy_course_dict,
                'global_coupon_record_dict': global_coupon_record_dict,
                'default_global_coupon_id': 0,
            }
redis_pool.conn.hset(settings.LUFFY_PAYMENT, request.user.id, json.dumps(user_pay))
```

 user_pay数据结构

```
结算中心 =  {
    用户ID: {
        policy_course_dict:{
            1:{
                'course_id': course_id,
                'course_name': product['name'],
                'course_img': product['course_img'],
                'policy_id': product['choice_policy_id'],
                'policy_price': policy_price,
                'policy_': policy_period, # 30/
                'default_coupon_id': 1,
                'coupon_record_list': {
                    0:{'id': 0, 'text': '请选择优惠券'},
                    1:{'id': 1, 'type':1, 'text': '优惠券1', ..},
                    2:{'id': 2, 'type':2, 'text': '优惠券1', ..},
                    3: {'id': 3, 'type':3, 'text': '优惠券1', ..},
                },
            },
            2:{
                'course_id': course_id,
                'course_name': product['name'],
                'course_img': product['course_img'],
                'policy_id': product['choice_policy_id'],
                'policy_price': policy_price,
                'policy_': policy_period,
                'default_coupon_id': 0,
                'coupon_record_list': {
                    0:{'id': 0, 'text': '请选择优惠券'},
                    1:{'id': 1, 'type':1, 'text': '优惠券1', ..},
                    2:{'id': 2, 'type':2, 'text': '优惠券1', ..},
                    3: {'id': 3, 'type':3, 'text': '优惠券1', ..},
                },
            }
        },
        global_coupon_dict:{
            1:{'type': 0, 'text': "通用优惠券", 'id': 1, ..},
            2:{'type': 0, 'text': "通用优惠券", 'id': 2, ..},
            3:{'type': 0, 'text': "通用优惠券", 'id': 3, ...},
            4:{'type': 0, 'text': "通用优惠券", 'id': 4, ...},
        },
        choice_global_coupon:3
    }         
}
```

## **去支付**

**1.去结算中心获取要结算的所有课程和优惠券**

**2.循环遍历每一个课程**

开始总价格**totalprice**和折扣价**totaldiscount**都为0,

```
总价 = 0
总折扣 = 0
```

2.1.如果该课程没有使用优惠券,则总价格=**totalprice+课程原价,totaldiscount=0，**

```
b. 循环购买的所有课程
    
    当前时间 = datetime.datetime.now()
    当前日期 = datetime.datetime.now().date
    ****课程信息 = [] *****
    ****使用的优惠券ID列表 = [] *****
    for course_id,values in policy_course_dict.items():
        课程原价 = values['policy_price']
        使用的优惠券ID = values['default_coupon_id']
        discount = 0
        
        # 未使用优惠券
            temp = {
                课程ID: 1,
                原价: 10,
                折扣价：10,
                有效期：30
            }
            课程信息.append(temp)
            
            总价 += 课程原价
            折扣 += discount
```

2.3.如果使用了优惠券,则需要去判断所使用的优惠券是否已经过期，或是否已经被使用,如果过期了或者被使用了就抛出异常,否则继续往下执行,判断该优惠券的类型

```
如果使用了优惠券:
            去数据库查询:指定优惠券是否已经使用、是否已经过期
            如果优惠券可不用：
                raise Exception('优惠券不可用')
            
            
            如果是通用优惠券：
                discount = 通用优惠券(如果大于课程原价，课程原价)
            elif 如果是满减优惠券：
                if 价格是否大于最小满减要求:
                    discount = 通用优惠券(如果大于课程原价，课程原价)
            elif 如果是折扣优惠券：
                discount = 课程原价 * (1-折扣)
            使用的优惠券ID列表.append(绑定可以的优惠券ID)
            
            temp = {
                课程ID: 1,
                原价: 10,
                折扣价：9,
                有效期：30
            }
            课程信息.append(temp)
            
            总价 += 课程原价
            折扣 += discount
```

到此为止 

```
pay = 总价 - 总折扣
```

**3.继续计算看是否使用全局优惠券**

```
全站优惠券ID = choice_global_coupon
    数据库获取并检查是否可用（优惠券是否已经使用、是否已经过期）
    如果优惠券可不用:
        raise('全站优惠券不可用')
        
    g_discount = 0
    如果是通用优惠券：
        g_discount = 通用优惠券(如果大于pay，pay)
    elif 如果是满减优惠券：
        if 价格是否大于最小满减要求:
            g_discount = 通用优惠券(如果大于pay，pay)
    elif 如果是折扣优惠券：
        g_discount = pay * (1- 折扣)
    
    总折扣 += g_discount
    使用的优惠券ID列表.append(全站优惠券ID)
```

**4.贝利支付**

```
    if balance <= request.user.balance:
        总折扣 += balance
```

**5.总结算**

```
总价 - 总折扣 = alipay
if alipay ==0:
        贝里&优惠券 
        pay_type = 0
    else:
        支付宝支付
        pay_type = 1
```

如果最后支付=0，就直接修改支付状态为已支付，否则改为待支付

 

**6.点击立即支付以后 进行数据库操作**

```
事务：
        
        # 1. 创建订单表
             order_obj = models.Order.objects.create(....status=0) # pay_type = 0
             或
             order_obj = models.Order.objects.create(....status=1) # pay_type = 1
             
        # 2. 生成订单详细
            
            for item in 课程信息：
                detail_obj = models.OrderDetail.objects.create(order_obj,课程ID,原价和折扣价)
                models.EnrolledCourse.objects.create(...当前时间,当前时间+30,status=1)
            
        # 3. 处理优惠券
            models.CouponRecord.objects.filter(account=request.user,status=0,id__in=使用的优惠券ID列表]).update(status=1,order=order_obj)
        
        # 4. 处理贝里交易
            models.Account.objects.filter(id=reuqest.user.id).update(balance=F(balance)-balance)
            models.TransactionRecord.objects.create(amount=balance,balance=request.user.balance,transaction_type=1,content_object=order_obj)      
```

点击立即支付要生成订单，订单根据前面支付是否等于0来判断支付状态是否要修改为已支付或者待支付；生成订单详情，循环课程信息，写入课程的原价，折后价，视频的有效期，即订单的有效期，对优惠券进行处理，把该用户已使用的优惠券状态改为已使用；：修改贝里，该账户的贝里减去使用的贝里，并更新贝里消费记录表，显示账户的消费金额，账户的余额等。

**最后**

```
if pay_type==1:
        生成支付宝链接（自动生成自己的订单号），并返回给前端Vue
# ##################################### 支付宝的回调 ######################################
def callback(request,*args,**kwargs):
models.Order.objects.filter(订单号).update(status=0)
```

 

## 项目源码

[我的GitHub](https://github.com/hyyc554/mycity)
