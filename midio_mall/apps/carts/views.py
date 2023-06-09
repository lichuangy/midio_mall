import base64
import pickle

import redis.cluster
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
import json

from django_redis import get_redis_connection

from apps.goods.models import SKU

# Create your views here.

"""
1.京东的网站 登录用户可以实现购物车，未登录用户也可以实现购物车   v
    淘宝的网址 必须是登录用户才可以实现购物车                   x
2. 用户点击添加到购物车的摁钮后，发送axios请求，给后端，后端获取数据，查询对应的数据，添加到数据库中，返回响应给前端
    查询用户购物车的所有数据，返回数据响应给前端
2.1 登录用户数据的保存：服务器中      mysql/redis--->mysql redis  mysql+redis
                                    从学习角度考虑，购物车频繁的增删改查---》redis中

    未登录用户数据的保存：客户端中     locationstorage   sessionstorage   cookiestorage
                                            cookie
3.确定保存那些数据？？？
    redis：
        user_id, sku_id(商品id）, count（数量）, selected（选中状态）
    cookie：
        user_id, sku_id, count, selected
4.数据的组织
    redis：
        user_id, sku_id(商品id）, count（数量）, selected（选中状态）
        哈希：
        user_id:
            sku_id:count
            xxx_sku_id:selected
            进一步优化！！！
            为什么要优化呢
            redis的数据保存在内存中 我们应该尽量少的占用redis的空间
            使我们的每一个数据
        原来的-----------------------------------------哈希
        user_1:  商品id为1:10
                 xx_1:True
                 商品id为2:20
                 xx_2:False
                 商品id为3:30
                 xx_3:False

                 占用13个空间
        改进后的---------------------------------------------哈希 + 集合 我们使用这种方案
        user_1:  商品id为1：10
                 商品id为2：20
                 商品id为3：30
                 selected_1:{1, 3}  ---- {1, 3}为集合
                 占用10个空间
        再此改进----------------------------------------哈希
        user_1: 
                1:10
                2:-20
                3:30
                占用7个空间

        记录选中的商品
        1和3 2未选中-------------------------》使用 集合set


    cookie：（浏览器）
        {
            sku_id: {count: xxx, selected: xxx}, 
            sku_id: {count: xxx, selected: xxx},
            }
5. cookie字段转化为字符串保存起来，数据没有加密
base64---6个比特位为一个单元（重新编码）
bytes 0 或者 1
ASCII

a
0110 0001
a a a（8位）--------重新编码------》x y z6位

字典-----------》二进制-----------》base64（对二进制进行处理）

carts = {
    '1':{'count':10, 'selected':True},
    '2':{'count':20, 'selected':False},
}
# 字典转化为bytes类型
import pickle
b = pickle.dumps(carts)
# 对bytes类型的数据进行base64编码
import base64
encode = base64.b64encode(b)
############################# 解码数据 ######################
# 进行数据解码
decode_bytes = base64.b64decode(encode)
# 对解码转换为字典
pickle.loads(decode_bytes)

"""

# 新增购物车


class CatsCreateView(View):

    """
    前端：点击 添加购物车，前端将商品id，数量 发送给后端axios
    后端：
        请求：         接收数据，验证数据
        业务逻辑：       在数据库中查询商品id是否存在，
                        数据入库
                            登录用户 redis
                                连接redis
                                获取用户id
                                hash
                                set
                            未登录用户
                                cookie
                                cookie字典
                                    转换为bytes
                                    bates类型数据base64编码
                                    设置cookie
                            返回响应

        响应           返回json
        路由            post /carts
        步骤
                1. 接收数据
                2.验证数据
                3.判断用户是否登录
                4.登录用户保存redis
                        数据入库
                        登录用户 redis
                            连接redis
                            获取用户id
                            hash
                            set
                5.未登录用户保存cooike
                    cookie
                    cookie字典
                        转换为bytes
                        bates类型数据base64编码
                        设置cookie
                6.返回响应

    """
        # """
        # 前端：用户点击添加购物车，前端发送一个axios请求给后端
        # 业务逻辑：
        # """

        # 添加商品到购物车
            # 1.接收数据


    def post(self, request):
        # 1.接收数据
        data = json.loads(request.body.decode())
        sku_id = data.get('sku_id')
        count = data.get('count')
        # 2.验证数据
        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '查无此商品'})
        # 2.5 强制类型转换---这里的强制类型转换为了防止使用postman发送请求，不填写数字，然后默认置为1
        try:
            count = int(count)
        except Exception as e:
            print(e)
            count = 1

        # 3.更新数据（数据入库，看看数据库中是否有该商品，有的话不能添加，存储到redis）（登录用户redis，未登录用户cookie）
        # 3.0 判断用户的登录状态
        user = request.user
        if user.is_authenticated:  # 认证用户
            # 3.1 登录用户保存redis
            # 3.2 连接redis
            redis_cli = get_redis_connection('carts')
            pipeline = redis_cli.pipeline()  # 设置pipline后，pipline就相当于redis_cli，注意此处为pipeline

            # 3.25 累加的操作
            pipeline.hincrby('carts_%s' % user.id, sku_id, count)

            # 3.3 操作hash hset key key value ------ carts_user.id    sku_id   count
            # redis_cli.hset('carts_%s' % user.id, sku_id, count)
            # 3.4 操作set（不能重复）（没有顺序，不能修改, string类型）
            # 默认选中
            pipeline.sadd('selected_%s' % user.id, sku_id)
            # 记得执行pipline
            pipeline.execute()

            # 返回响应
            return JsonResponse({'code': 0, 'errmsg': 'set carts is ok for login user'})

        else:  # 未认证用户
            # 3.5 未登录用户保存到cookie
            # 3.55 先读取cookie数据，判断新增的商品有咩有在购物车中  ------先判断cookie中有没有数据
            cookie_carts = request.COOKIES.get('carts')
            if cookie_carts:  # 有数据的话，转换为正常的数据（字典数据）
                carts = pickle.loads(base64.b64decode(cookie_carts))
            else:  # 没有数据的话，建立一个新的空字典
                # 3.6 现有cookie字典
                carts = {}
            # carts = {sku_id1: { count:xxx, selected:xxx}, sku_id2: {count:xxx, selected:xxx}}
            if sku_id in carts:  # 判断加入购物车的商品的id是否在购物车中(字典遍历的是key）
                # 购物车中已经有商品id   在购物车中的话要改变 商品的count  没有在购物车中的话，直接赋值count即可
                origin_count = carts[sku_id]['count']
                count += origin_count
                # carts[sku_id] = {
                #     'count': count,
                #     'selected': True,
                #
                # }

            # 购物车没有商品，不管在不再购物车中，都要对字典进行改变的操作
            carts[sku_id] = {
                'count': count,
                'selected': True
            }

            # 字典--->二进制字典--->二进制 重新编码的字典 --->重新编码的 字典（该字典并不是原来的字典）

            # 3.7 字典转化为bytes（再加密字典）(此时为str类型)
            carts_bytes = pickle.dumps(carts)
            # 3.8 bytes类型用base64重新编码(6位为一个，非str类型）
            base64encode = base64.b64encode(carts_bytes)
            # 3.9 设置cookie（加密为了cookie中显示时是加密的信息）
            response = JsonResponse({'code': 0, 'errmsg': 'set carts is ok for not login user'})
            response.set_cookie('carts', base64encode.decode(),
                                max_age=3600 * 24 * 12)
            # decode作用将byte转为str，因为value数据为str数据，这个decode（）不影响，base64和pickle的转换数据效果，但是cookies设定的时候要加
            # 返回响应
            return response

    """
      # 1.判断用户是否登录
      # 2.登录用户查询redis
      #     2.1 连接redis
      #     2.2 hash        {sku_id:count}
      #     2.3 set         
      #     2.4 遍历判断
      # 4. 根据商品id查询商品信息
      # 5. 将对象数据转换为字典数据
      # 6. 返回响应
      # 
      # 3.未登录用户查询cookie
      #     3.1 读取cookie数据
      #     3.2 判断是否存在购物车数据
      #         如果存在，则解码            
      #         如果不存在，初始化空字典
      # 4. 根据商品id查询商品信息
      # 5. 将对象数据转换为字典数据
      # 6. 返回响应
      """

    def get(self,request):
        # 1.判断用户是否登录
        user = request.user
        if user.is_authenticated:
        # 2.登录用户查询redis
        #     2.1 连接redis
            redis_cli = get_redis_connection('carts')
        #     2.2 hash        {sku_id:count,sku_id:count...}
            sku_id_count = redis_cli.hgetall('cart_%s' % user.id)
        #     2.3 set
            select_ids = redis_cli.smembers('selected_%s' % user.id)
            carts = {}
        #     2.4 遍历判断
            for sku_id,count in sku_id_count.items():
                carts[sku_id] = {
                    'count':count,
                    'selected':sku_id in select_ids
                }
        # 4. 根据商品id查询商品信息
        # 5. 将对象数据转换为字典数据
        # 6. 返回响应
        else:
        # 3.未登录用户查询cookie
        #     3.1 读取cookie数据
            carts_cookies = request.COOKIES.get('carts')
        #     3.2 判断是否存在购物车数据
            if carts_cookies is not None:
        #         如果存在，则解码
                carts = pickle.loads(base64.b64decode(carts_cookies))
            else:
        #         如果不存在，初始化空字典
                carts = {}
        # 4. 根据商品id查询商品信息
        sku_ids = carts.keys()
        skus = SKU.objects.filter(id__in=sku_ids)
        sku_list = []
        for sku in skus:
        # 5. 将对象数据转换为字典数据
            sku_list.append({
                'id':sku.id,
                'name':sku.name,
                'count': carts[sku.id]['count'],
                'selected': carts[sku.id]['selected'],  # 将True，转True，方便json解析
                'default_image_url':'http://192.168.44.130:8888/' + sku.default_image_url,
                'price':str(sku.price), # 从Decimal('10.2')中取出'10.2'，方便json解析
                'amount':sku.price*carts[sku.id]['count'],
            })
        # 6. 返回响应
        return JsonResponse({'code':200,'errmsg':'ok','cart_skus':sku_list})


    """
        修改购物车<------------------------------------------------->
        1.获取用户信息
        2.接收数据
        3.验证数据
        4.登录用户更新redis
        4.1 连接redis
        4.2 hash
        4.3 set
        4.4 返回响应
        5.未登录用户更新cookie
        5.1 先读取购物车数据
        5.2 判断有没有
        5.3 有的话解密数据
        5.4 没有的话则初始化一个字典
        5.5 更新数据
        5.6 重新对字典进行编码和pickle加密
        5.7 设置cookie
        5.8 返回响应

        """
    # 修改购物车

    def put(self,request):

        # 1.获取用户信息
        user = request.user
        # 2.接收数据
        data = json.loads(request.body.decode())
        sku_id = data.get('sku_id')
        count = data.get('count')
        selected = data.get('selected')
        # 3.验证数据
        if not all([sku_id,count]):
            return JsonResponse({'code':400,'errmsg':'缺少参数'})
        try:
            SKU.objects.get(id=sku_id)
        except SKU.DoseNotExist:
            return JsonResponse({'code':400,'errmsg':'商品不存在！'})

        count = int(count)
        if user.is_authenticated:

            # 4.登录用户更新redis
            # 4.1 连接redis
            redis_cli = get_redis_connection('carts')
            # 4.2 hash
            redis_cli.hset('carts_%s'%user.id,count)
            # 4.3 set
            if selected:
                redis_cli.sadd('selected_%s' % user.id, sku_id)
            else:
                redis_cli.srem('selected_%s' % user.id, sku_id)
            # 4.4 返回响应
            return JsonResponse({'code':200,'errmsg':'ok','cart_sku':{'count':count,'selected':'selected'}})

        else:
            # 5.未登录用户更新cookie
            # 5.1 先读取购物车数据
            cookie_cart = request.COOKIES.get('carts')
            # 5.2 判断有没有
            if cookie_cart is not None:
            # 5.3 有的话解密数据
                carts = pickle.loads(base64.b64decode(cookie_cart))
            # 5.4 没有的话则初始化一个字典
            else:
                carts = {}
        # 5.5 更新数据
        if sku_id in carts:
            carts[sku_id]={

                'count': count,
                'selected': selected
            }
        # 5.6 重新对字典进行编码和pickle加密
        new_carts = base64.b64encode(pickle.dumps(carts))
        # 5.7 设置cookie
        response = JsonResponse({'code':0,'errmsg':'ok','cart_sku':{'count':count,'selected':selected}})
        response.set_cookie('carts',new_carts.decode(),max_age=3600*24*14)
        # 5.8 返回响应
        return response


    """
    1.接收请求
    2.验证参数
    3.根据用户登录状态
    4.登录用户操作redis
    4.1 连接redis
    4.2 hash
    4.3 set
    4.4 返回响应
    5.未登录用户操作cookie
    5.1 读取cookie中的购物车数据
    5.2 判断数据是否存在，存在则解码
    5.3 不存在初始化字典
    5.4 删除数据
    5.5 对字典数据进行base64和加密处理
    5.6 设置cookie
    5.7 返回响应
    """
    def delete(self, request):
        user = request.user
        # 1.接收请求
        data = json.loads(request.body.decode())
        # 2.验证参数
        sku_id = data.get('sku_id')
        # 3.根据用户登录状态
        try:
            SKU.objects.get(pk=sku_id)  # pk ---> primary key
        except SKU.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '没有此商品'})
        # 4.登录用户操作redis
        if user.is_authenticated:
            # 4.1 连接redis
            redis_cli = get_redis_connection('carts')
            # 4.2 hash
            redis_cli.hdel('carts_%s' % user.id, sku_id)
            # 4.3 set
            redis_cli.srem('selected_%s' % user.id, sku_id)
            # 4.4 返回响应
            return JsonResponse({'code': 0, 'errmsg': 'ok'})
        else:
            # 5.未登录用户操作cookie
            # 5.1 读取cookie中的购物车数据
            cookie_cart = request.COOKIES.get('carts')
            # 5.2 判断数据是否存在，存在则解码
            if cookie_cart is not None:
                carts = pickle.loads(base64.b64decode(cookie_cart))
            # 5.3 不存在初始化字典
            else:
                carts = {}
            # 5.4 删除数据
            del carts[sku_id]
            # 5.5 对字典数据进行base64和加密处理
            new_carts = base64.b64encode(pickle.dumps(carts))
            # 5.6 设置cookie
            response = JsonResponse({'code':0, 'errmsg': 'ok'})
            response.set_cookie('carts', new_carts.decode(), max_age=3600*24*14)
            # 5.7 返回响应
            return response


