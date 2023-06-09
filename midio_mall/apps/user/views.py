import json
import re
import json

import redis
from django.contrib.auth.forms import User
from django.db.models import Q

from django.shortcuts import render
from django_redis import get_redis_connection

"""
前端：当用户输入用户名后，失去焦点，发送axios(ajax)请求

后端：
    请求:            接收用户名
    业务逻辑：      
                    根据用户名查询数据库，如果查询结果数量等于0，说明没有注册； 查询结果等于1 ，说明注册
    响应              json
                    {code:0,count:0/1,errmsg:ok}
                    
                    django允许在url中捕获值，若要从URL中捕获值，请使用尖括号。
                    尖括号定义变量名，捕获的值传递给视图函数相同名称的参数
    路由             GET      usernames/<username>/count/
    步骤：
        1.接收用户名
        2.根据用户名查询数据库
        3.返回响应

"""
# Create your views here.

from django.views import View
from apps.user.models import User, Address
from django.http import JsonResponse
import re


class UsernameCountView(View):
    def get(self, request, username):
        # 1.接收用户名
        # 2.根据用户名查询数据库
        count = User.objects.filter(username=username).count()
        if not re.match('[a-zA-Z0-9_-]{5,50}', username):
            return JsonResponse({'code': 200, 'count': count, "errmsg": 'username  model is not use'})
        # 3.返回响应
        return JsonResponse({'code': 0, 'count': count, "errmsg": 'ok'})


"""
前端：	用户输入用户名，密码，确认密码，手机号，是否同意协议后，点击注册按钮
		发送请求

后端：
请求		接收json数据，获取数据
业务逻辑		验证数据，数据入库
响应		JSON{‘code':0,errmsg:'ok'}
路由		POST	register/

步骤：
接受请求（POST---JSON）
对请求进行获取和解码
获取数据
验证数据
数据不为空
数据合规
数据入库
返回响应
"""


class RegistereView(View):
    def post(self, request):

        # 1.接收参数：请求体中的JSON数据 request.body
        json_bytes = request.body  # 从请求体中获取原始的JSON数据，bytes类型的
        json_str = json_bytes.decode()  # 将bytes类型的JSON数据，转成JSON字符串
        body_dict = json.loads(json_str)  # 将JSON字符串，转成python的标准字典
        # json_dict = json.loads(request.body.decode())

        # 获取数据
        username = body_dict.get('username')
        password = body_dict.get('password')
        password2 = body_dict.get('password2')
        mobile = body_dict.get('mobile')
        allow = body_dict.get('allow')
        sms_code = body_dict.get('sms_code')

        # 验证数据
        if not all([username, password, password2, mobile, sms_code, allow]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全000'})
        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_]{5,20}$', username):
            return http.JsonResponse({'code': 400, 'errmsg': 'username格式有误!'})
        # 判断密码是否是8-20个数字
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.JsonResponse({'code': 400, 'errmsg': 'password格式有误!'})
        # 判断两次密码是否一致
        if password != password2:
            return http.JsonResponse({'code': 400, 'errmsg': '两次输入不对!'})
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.JsonResponse({'code': 400, 'errmsg': 'mobile格式有误!'})
        # 判断是否勾选用户协议
        if allow != True:
            return http.JsonResponse({'code': 400, 'errmsg': 'allow格式有误!'})

        # 数据入库
        User.objects.create(
            username=username,
            password=password,
            mobile=mobile,
        )
        # 返回响应
        return http.JsonResponse({'code': 0, 'errmsg': 'ok!'})

    """
    登录
    
    前端：
        当用户把用户密码手机号输入完成后，点击登录按钮，这时，前端会发送一个axios请求
        
    后端：
        请求：接收数据，验证数据
        业务逻辑：验证用户名和密码是否正确， session
        响应：返回json数据， 0 成功，400失败
    
    步骤：
        1.接收数据
        2.验证数据
        3.验证用户名和密码是否正确
        4.session
        5.判断是否记住登录
        6.返回响应
    """


class LoginView(View):
    def post(self, request):
        # 1.接收数据
        data = json.loads(request.body.decode())
        username = data.get("username")
        password = data.get("password")
        remembered = data.get("remembered")

        # 2.验证数据
        if not all([username, password]):
            return JsonResponse({"code": 400, "errmsg": "参数不全"})
        # 3.验证用户名和密码是否正确
        # 方法一，通过模型根据用户名来查询
        # User.objects.get(username=username)

        user = User.objects.filter(Q(username=username) | Q(mobile=username) & Q(password=password)).first()
        if user is None:
            return JsonResponse({"code": 400, "errmsg": "用户名或者密码错误！"})
            # 方法二
        #         from django.contrib.auth import authenticate
        # #        authenticate 传递用户名和密码
        # #       如果用户名和密码正确，则返回User信息
        # #       如果不正确，返回none
        # #         user = authenticate(request, username=username, password=password)
        #         user = authenticate(username=username, password=password)
        #         if user is None:
        #             return JsonResponse({"code": 400, "errmsg":"用户名或者密码错误！"})
        #       4.session
        from django.contrib.auth import login
        login(request, user)
        # 判断是否记住登录
        if remembered is not None:
            # 不为空，记住登录
            request.session.set_expiry(None)
        else:
            # 否则不记住登录 浏览器关闭，session过期
            request.session.set_expiry(0)

        # 6.返回响应
        response = JsonResponse({"code": 0, "msg": "OK"})
        # 设置cookie , 用户首页信息展示用的cookies来获取用户名
        response.set_cookie('username', user.username)
        return response

from django.contrib.auth import logout
class LoginOutView(View):
    def get(self,request):
        logout(request)
        response = JsonResponse({"code": 0, "errmsg": "ok"})
        # 删除cookie信息，前端根据cookie信息来判断用户是否登录
        response.delete_cookie('username')
        return response


# 用户中心返回json数据（前后端分离，只用json互交）
from django.contrib.auth.mixins import LoginRequiredMixin,AccessMixin
from utils.views import LoginRequiredJSOMixin
class LoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"code": 400, "errmsg":"please go to login!"})
        return super().dispatch(request, *args, **kwargs)
class CenterView(LoginRequiredMixin, View):
    def get(self,request):
        info_data={
            # request.user 已经登录的用户信息
            "username": request.user.username,
            "mobile": request.user.mobile,
            "email": request.user.email,
            "email_active": request.user.email_active,
        }
        return JsonResponse({"code": 0, "msg": "ok","info_data":info_data})



    """
    用户中心个人信息邮箱部分
    
    前端：当用户输入邮箱后，点击保存，此时发送一个axios请求
    
    后端
        请求          接收请求，获取数据
        业务逻辑       保存邮箱地址，发送一封激活邮件
        响应          json code=0
        
    路由  PUT 
    步骤
        # 1.接收请求
        # 2.获取数据
        # 3.保存邮箱地址
        # 4.发送一封激活邮件
        # 5.返回响应
    """

class EmailView(LoginRequiredMixin, View):
        # 1.接收请求
    def put(self,request):
        data = json.loads(request.body.decode())
         # 2.获取数据
        email=data.get("email")
        # 验证数据
        # if not re.match(r'^[a-zA-Z0-9_]{5,20}$', username):
        if not re.match(r'^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+$', email):
            return JsonResponse({"code":400, "errmsg":"邮箱格式错误"})
        # 3.保存邮箱地址
        user = request.user
        # request.user 登录用户的 实例对象
        user.email = email
        user.save()
        # 4.发送一封激活邮件 网易：WSRODUFFPQKKOFWO
        from django.core.mail import send_mail

        # 对html_message中的  ？  后面部分数据加密
        from apps.user.utils import generic_email_verify_token
        token=generic_email_verify_token(request.user.username)

        subject='美多商城激活邮件'
        message=""
        # html_message="点击按钮<a href='https://www.baidu.com/token=%s'>激活</a>" % token
        verify_url = "http://www.meiduo.site:8080/success_verify_email.html?token=%s"%token
        html_message ='<p>尊敬的用户您好！</p>'\
                    '<p>感谢您使用midio mall</p>'\
                    '<p>您的邮箱为：%s 请点击此链接激活您的邮箱：</p>'\
                    '<p><a href=%s>%s></a></p>' % (email, verify_url, verify_url)
        from_email='美多商城<lw880699@163.com>'
        recipient_list=['lw880699@163.com','3195792673@qq.com','1443803091@qq.com']

        # send_mail(subject=subject,
        #           message=message,
        #           html_message=html_message,
        #           from_email=from_email,
        #           recipient_list=recipient_list

        from celery_tasks.email.tasks import send_email
        send_email.delay(
            subject=subject,
            message=message,
            html_message=html_message,
            from_email=from_email,
            recipient_list=recipient_list
        )
        """
        1.设置邮件服务器
            例如：163 
                设置——>开启pop3/smpt ——>设置授权码
        2.设置邮件发送的配置信息
            让django的哪个类来发送邮件
            # 固定写法设置Email引擎
            EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
            EMAIL_HOST = 'smtp.163.com' # 163邮箱 SMTP 服务器地址
            EMAIL_PORT = 25 # SMTP服务的端口号
            EMAIL_HOST_USER = 'lw880699@163.com' #你的邮箱，邮件发送者的邮箱
            EMAIL_HOST_PASSWORD = 'None' #你申请的授权码（略）
            EMAIL_USE_TLS = False #与SMTP服务器通信时,是否启用安全模
            
            
        # subject：邮件主题；
        # message：邮件正文内容；
        # from_email：发送邮件者；
        # recipient_list：邮件接受者列表；
        # html_message：带有标签格式的HTML文本。
        """

        # 5.返回响应
        return JsonResponse({'code':0,'errmas':'ok'})



# class EmailVerifyView(View):
#     def put(self,request):
#         params = request.GET
#         token = params.get('token')
#         if token is None:
#             return JsonResponse({'code':400,'errmsg':'参数缺失'})
#         from apps.user.utils import check_verify_token
#         user_id = check_verify_token(token)
#         if user_id is None:
#             return JsonResponse({'code':400,'errmsg':'参数缺失'})
#         user = User.objects.get(id=user_id)
#         user.email_active = True
#         user.save()
#         return JsonResponse({'code':0,'errmsg':'ok'})

class EmailVerifyView(View):
    def put(self, request):
        # 1.接收请求
        params = request.GET
        # 2.获取参数
        token = params.get('token')
        # 3.验证参数
        if token is None:
            return JsonResponse({'code': 400, 'errmsg': '参数缺失'})
        # 4.获取user_id
        from apps.users.utils import check_verify_token
        user_id = check_verify_token(token)
        if user_id is None:
            return JsonResponse({'code': 400, 'errmsg': '参数错误'})
        # 5.根据用户id进行查询数据--------自己尝试使用request.user获取数据
        user = User.objects.get(id=user_id)
        # 6.修改数据
        user.email_active = True
        user.save()
        # 7.返回JSON响应
        return JsonResponse({'code': 0, 'errmsg': 'verify email is ok'})

"""
    需求：
    
    
    前端：
    
    后端
        请求          
        业务逻辑       数据库的增删改查
                        增加（注册）
                            1.接收数据
                            2.验证数据
                            3.数据入库
                            4.返回响应
                        删除
                            1.查询指定数据
                            2.删除数据（物理删除、逻辑删除）
                            3.返回响应
                        更改
                            1.查询指定数据 
                            2.接收数据
                            3.验证数据
                            4.数据更新
                            5.返回响应
                        查询
                            1.查询指定数据
                            2.将对象数据转换成字典数据
                            3.返回响应
                            
    响应
    路由   
    步骤
        # 1.
        # 2.
        # 3.
        # 4.
        # 5.
"""

"""
    需求：
        新增收获地址
    
    前端：
        当用户填写完地址信息，点击增加按钮后，发送axios请求，携带填写的信息    
    后端
        请求          接收请求，获取参数
        业务逻辑       接收数据，数据入库
        响应          返回响应
        
    路由   PosT /address/create/
    步骤
        # 1.接收数据
        # 2.获取参数，验证参数
        # 3.数据入库
        # 4.返回响应
        # 5.
"""

class AddressCreateView(LoginRequiredMixin, View):
    def put(self, request, address_id):
        data = json.loads(request.body.decode())
        receiver = data.get('receiver')

        # 1.5 查询到的为未改变的数据 需求：拿到用户输入的数据 TODO
        province = data.get('province')
        city = data.get('city')
        district = data.get('district')

        place = data.get('place')
        mobile = data.get('mobile')
        tel = data.get('tel')
        email = data.get('email')
        # 2. 修改数据
        address = Address.objects.get(id=address_id)
        address.receiver = receiver

        address.province_id = province
        address.city_id = city
        address.district_id = district

        address.place = place
        address.mobile = mobile
        address.tel = tel
        address.email = email

        address.save()
        # 3.封装字典
        address_dict = {
            'receiver': receiver,
            'province': province,
            'city': city,
            'district': district,
            'place': place,
            'mobile': mobile,
            'tel': tel,
            'email': email
        }
        address.save()
        # 4.返回响应
        return JsonResponse({'code': 0, 'message': 'modify address is ok', 'address': address_dict})

    def post(self,request):
        # 1.接收数据
        data = json.loads(request.body.decode())
        # 2.获取参数，验证参数
        receiver = data.get("receiver")
        province_id = data.get("province_id")
        city_id = data.get("city_id")
        district_id = data.get("district_id")
        place = data.get("place")
        mobile = data.get("mobile")
        tel = data.get("tel")
        email = data.get("email")

        user = request.user
        # 验证参数
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return http.HttpResponseBadRequest('缺少必传参数')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseBadRequest('参数mobile有误')
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return http.HttpResponseBadRequest('参数tel有误')
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return http.HttpResponseBadRequest('参数email有误')
        # 3.数据入库
        address = Address.objects.create(
            user=request.user,
            title=receiver,
            receiver=receiver,
            province_id=province_id,
            city_id=city_id,
            district_id=district_id,
            place=place,
            mobile=mobile,
            tel=tel,
            email=email
        )

        # 新增地址成功，将新增的地址响应给前端实现局部刷新
        address_dict = {
            "id": address.id,
            "title": address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email}
         # 返回响应
        return JsonResponse({'code': 0, 'errmsg': '新增地址成功', 'address': address_dict})
# class UpdataView(LoginRequiredJSOMixin,View):
    # def put(self, request, address_id):
    #     # 1.接收数据
    #     data = json.loads(request.body.decode())
    #     receiver = data.get('receiver')
    #
    #     # 1.5 查询到的为未改变的数据 需求：拿到用户输入的数据 TODO
    #     province = data.get('province')
    #     city = data.get('city')
    #     district = data.get('district')
    #
    #     place = data.get('place')
    #     mobile = data.get('mobile')
    #     tel = data.get('tel')
    #     email = data.get('email')
    #     # 2. 修改数据
    #     address = Address.objects.get(id=address_id)
    #     address.receiver = receiver
    #
    #     address.province_id = province
    #     address.city_id = city
    #     address.district_id = district
    #
    #     address.place = place
    #     address.mobile = mobile
    #     address.tel = tel
    #     address.email = email
    #
    #     address.save()
    #     # 3.封装字典
    #     address_dict = {
    #         'receiver': receiver,
    #         'province': province,
    #         'city': city,
    #         'district': district,
    #         'place': place,
    #         'mobile': mobile,
    #         'tel': tel,
    #         'email': email
    #     }
    #     address.save()
    #     # 4.返回响应
    #     return JsonResponse({'code': 0, 'message': 'modify address is ok', 'address': address_dict})

# 地址展示的实现
class AddressView(LoginRequiredJSOMixin, View):
    def get(self, request):
        # 1.查询指定数据
        user = request.user
        # 1.1 addresses = user.addresses
        addresses = Address.objects.filter(user_id=user.id, is_deleted=0)

        # 2.转化为字典数据
        address_list = []
        for address in addresses:
            address_list.append({
                'id': address.id,
                'title': address.title,
                'receiver': address.receiver,
                'province': address.province.name,
                'city': address.city.name,
                'district': address.district.name,
                'place': address.place,
                'mobile': address.mobile,
                'tel': address.tel,
                'email': address.email
            })
        # 返回响应
        return JsonResponse({'code': 0, 'errmsg': 'display address info is ok',
                             'addresses': address_list})


########################## 最近浏览记录 #################
"""
一 根据页面效果，分析需求
    1.最近浏览记录 只有登录用户才可以访问 只记录登录用户的浏览信息
    2.浏览记录应该有顺序
    3.没有分页

二 功能
    功能：
        1：在用户访问商品详情的时候，添加浏览记录
        2：在个人中心，展示浏览记录

三 具体分析
    问题1：保存那些数据？用户id，商品id，顺序（访问时间）---根据商品id来进行查询
    问题2：保存在哪里？一般要保存在数据库（缺点：慢，会频繁操作数据库）
                    最好保存在redis中
        保存在两个库中都可以，看公司具体的安排，服务器内存比较大，mysql + redis

    user_id,sku_id,顺序

    redis： 5中数据类型
    key：value

    string：x
    hash：x
    list：v（去重，不能重复）
    set：x
    zset：权重：值
"""
"""
添加浏览记录：
    前端：当登录用户，访问某一个具体SKU页面的时候，发送一个axios请求，请求携带sku_id
    后端：
        请求：接收请求，获取请求参数，验证参数
        业务逻辑：连接redis，先去重，再保存到redis中，redis中只保存5条记录
        响应：返回JSON
        路由： POST browse_histories
        步骤：
            1：接收请求
            2：获取请求参数
            3：验证参数
            4：连接redis       list
            5：去重
            6：保存到redis中
            7：只保存5条记录
            8：返回响应
"""
# 添加 用户浏览商品记录

from utils.views import LoginRequiredJSOMixin
from apps.goods.models import SKU
class UserHistoryView(LoginRequiredJSOMixin,View):
    def post(self,request):
        # 1：接收请求
        user = request.user
        # 2：获取请求参数
        data = json.loads(request.body.decode())
        sku_id = data.get('sku_id')
        # 3：验证参数
        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoseNotExist:
            return JsonResponse({'code':400,'errmsg':'商品不存在！'})
        # 4：连接redis
        # list

        redis_cli = get_redis_connection('history')
        # 5：去重(先删除再保存）
        try:
            redis_cli.lrem('history_%s' % user.id, 0, sku_id)
        finally:
            # 6：保存到redis中
            redis_cli.lpush('history_%s' % user.id, sku_id)
            # 7：只保存5条记录
            redis_cli.ltrim('history_%s' % user.id, 0, 4)
            # 8：返回响应
            return JsonResponse({'code': 0, 'errmsg': 'ok'})

    def get(self, request):
        # 1.连接redis
        redis_cli = get_redis_connection('history')
        # 2.获取redis数据
        ids = redis_cli.lrange('history_%s' % request.user.id, 0, 4)
        # 3.根据商品id进行数据查询
        history_list = []
        for sku_id in ids:
            sku = SKU.objects.get(id=sku_id)
         # 4.将对象转化为字典
            history_list.append({
                'id': sku.id,
                'name': sku.name,
                'default_image_url': sku.default_image.url,
                'price': sku.price,
                })
        # 5.返回JSON
        return JsonResponse({'code': 0, 'errmsg': 'set display history is ok', 'skus': history_list})

    """
    展示用户浏览记录
        前端：
            用户在访问浏览记录的时候，会发送axios请求，请求会携带session信息
        后端：
            请求：
            业务逻辑：连接redis，获取redis数据（获取商品id），根据商品id进行查询，将对象转化为字典
                    根据商品id进行数据查询
            响应：JSON
            路由：GET 与添加 浏览记录的路由相同
            步骤：
                1.连接redis
                2.获取redis数据
                3.根据商品id进行数据查询
                4.将对象转化为字典
                5.返回JSON
    """