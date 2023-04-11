import json
import re
import json
from django.contrib.auth.forms import User
from django.db.models import Q

from django.shortcuts import render
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
from apps.user.models import User
from django.http import JsonResponse
import re
class UsernameCountView(View):
    def get(self, request, username):
        # 1.接收用户名
        # 2.根据用户名查询数据库
        count = User.objects.filter(username=username).count()
        if not re.match('[a-zA-Z0-9_-]{5,50}',username):
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
        if not all([username,password,password2,mobile,sms_code,allow]):
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
        if not all([username,password]):
            return JsonResponse({"code": 400, "errmsg":"参数不全"})
        # 3.验证用户名和密码是否正确
            #方法一，通过模型根据用户名来查询
            # User.objects.get(username=username)

        user = User.objects.filter(Q(username=username)|Q(mobile=username)&Q(password=password)).first()
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
        login(request,user)
        # 判断是否记住登录
        if remembered is not None:
            # 不为空，记住登录
            request.session.set_expiry(None)
        else:
            # 否则不记住登录 浏览器关闭，session过期
            request.session.set_expiry(0)

        # 6.返回响应
        response = JsonResponse({"code":0, "msg":"OK"})
        # 设置cookie , 用户首页信息展示用的cookies来获取用户名
        response.set_cookie('username',user.username)
        return response