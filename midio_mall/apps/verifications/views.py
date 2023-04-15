from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
"""
前端
    拼接一个url, 然后给img, img发起一个请求
    url：http://ip:port/image_code/uuid/
    
后端
    请求      接收路由中的uuid
    业务逻辑   生成图片验证码和图片二进制，通过redis把图片保存
    响应      返回二进制图片
    
    路由  GET image_code/uuid/
    步骤：
        1.接收uuid
        2.生成图片验证码和图片二进制
        3.通过redis把图片验证码保存起来
        4.返回图片二进制
"""


from django.views import View


# Create your views here.
class ImageCodeView(View):

    def get(self, request, uuid):
        # 1.接收uuid
        # 2.生成图片验证码和图片二进制
        from libs.captcha.captcha import captcha
        # text是图片验证码的内容，用户输入的
        # image是图片二进制
        text, image = captcha.generate_captcha()
        # 导入模块
        from django_redis import get_redis_connection
        # 进行redis的连接
        redis_cli = get_redis_connection('imagecode')
        # 3.通过redis把图片验证码保存起来
        # 指令操作
        # name, time, value
        # key  过期时间 value
        redis_cli.setex(uuid, 200, text)
        return HttpResponse(image, content_type='image/jpeg')
        # 4.返回图片二进制


class SmsCodeView(View):
    def get(self, request, mobile):
        # 1获取请求参数
        image_code = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')
        print("---------")
        print(image_code,uuid)

        # 2验证参数
        if not all([image_code,uuid]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})

        # 3验证图片验证码
        from django_redis import get_redis_connection
        red_cli =get_redis_connection('imagecode')
        redis_image_code = red_cli.get(uuid)
        if redis_image_code is None:
            return JsonResponse({'code': 400, 'errmsg': '图片验证码已过期'})
        if redis_image_code.decode() != image_code:
            return JsonResponse({'code': 400, 'errmsg': '图片验证码错误 !'})
        # 4生成短信验证码
        from random import randint
        sms_code = '%06d'%randint(0,999999)
        print('00')
        # 5保存短信验证码
        red_cli.setex(mobile,300,sms_code)
        print('01')
        # 6发送短信验证码
        # from libs.yuntongxun.sms import CCP
        from libs.yuntongxun.smsSDK import SendSmsVerificationCode
        # CCP().send_template_sms(mobile, [sms_code, 3], 1)
        # SendSmsVerificationCode().send_message(mobile, (sms_code, 5), '1')
        # print('02')
        # 7返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok'})