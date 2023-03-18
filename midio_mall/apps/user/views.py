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
class UsernameCountView(View):
    def get(self, request, username):
        # 1.接收用户名
        # 2.根据用户名查询数据库
        count = User.objects.filter(username=username).count()
        # 3.返回响应
        return JsonResponse({'code': 0, 'count': count, "errmsg": 'ok'})
