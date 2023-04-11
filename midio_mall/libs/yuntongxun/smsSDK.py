from ronglian_sms_sdk import SmsSDK
import json

# accId = '2c94887686c00d750186ff32a6680d66','2c94887686c00d75018707d8a6070f9e'
accId = '2c94887686c00d75018707d8a6070f9e'
# accToken = '66947cf7e3684933a6f0393535109ba8','5064357b1ff142b2bd28c97a20aff3c8'
accToken = '5064357b1ff142b2bd28c97a20aff3c8'
# appId = '2c94887686c00d75018707ceb5f60f98','2c94887686c00d75018707d8a7290fa5'
appId = '2c94887686c00d75018707d8a7290fa5'

class SendSmsVerificationCode:
    """发送短信验证码的单例类"""

    def __new__(cls, *args, **kwargs):
        """
        发送短信验证码单例类的初始化方法
        :return: 返回一个发送短信验证码的对象
        """
        # 判断类中发送短信验证码的对象 _instance 是否已经存在
        # 如果不存在, 创建一个发送短信验证码的对象, 并将其作为类属性
        if not hasattr(cls, '_instance'):
            # 创建发送短信验证码的对象
            cls._instance = super(SendSmsVerificationCode, cls).__new__(cls, *args, **kwargs)
            # 创建SmsSDK对象作为 _instance 的对象属性
            cls._instance.sdk = SmsSDK(accId, accToken, appId)
        # 如果存在, 返回发送短信验证码的对象
        return cls._instance

    def send_message(self, mobile, datas, tid='1'):
        """
        发送短信的方法
        @params mobile 字符串类型  mobile = '手机号1,手机号2'
        @params tid tid = '容联云通讯平台创建的模板' 默认模板的编号为1
        @params datas 元组类型  第一个参数为验证码 第二个参数为验证码的有效时间(对于短信模板1)
        :return: 返回发送短信后的响应参数
        """
        # 发送短信
        resp = self.sdk.sendMessage(tid, mobile, datas)
        print(json.loads(resp), type(json.loads(resp)))
        # return resp

# 测试
if __name__ == '__main__':
    sendSmsVerificationCode = SendSmsVerificationCode()
    # sendSmsVerificationCode2 = SendSmsVerificationCode()
    # sendSmsVerificationCode3 = SendSmsVerificationCode()
    # print(sendSmsVerificationCode1)
    # print(sendSmsVerificationCode2)
    # print(sendSmsVerificationCode3)
    sendSmsVerificationCode.send_message('15717151491', ('123456', 5), '1')

    """
    /home/lc/.virtualenvs/py3_django_42/bin/python /home/lc/python/django_py3_42/midio_mall/midio_mall/libs/yuntongxun/smsSDK.py 
Sign plaintext:  2c94887686c00d75018707d8a6070f9e5064357b1ff142b2bd28c97a20aff3c820230323143457
Authorization plaintext: 2c94887686c00d75018707d8a6070f9e:20230323143457
Request url:  https://app.cloopen.com:8883/2013-12-26/Accounts/2c94887686c00d75018707d8a6070f9e/SMS/TemplateSMS?sig=A818452C1576A0F4BBDC93F7ABEE5C0D
Request headers:  {'Content-Type': 'application/json;charset=utf-8', 'Accept': 'application/json', 'Accept-Charset': 'UTF-8', 'Authorization': b'MmM5NDg4NzY4NmMwMGQ3NTAxODcwN2Q4YTYwNzBmOWU6MjAyMzAzMjMxNDM0NTc='}
Request body:  {"to": "15717151491", "appId": "2c94887686c00d75018707d8a7290fa5", "templateId": "1", "datas": ["123456", 5]}
Response body:  {"statusCode":"000000","templateSMS":{"smsMessageSid":"97e8e88d873642898869d0aa11a4f7bd","dateCreated":"20230323143458"}}
{'statusCode': '000000', 'templateSMS': {'smsMessageSid': '97e8e88d873642898869d0aa11a4f7bd', 'dateCreated': '20230323143458'}} <class 'dict'>

Sign plaintext:  2c94887686c00d75018707d8a6070f9e5064357b1ff142b2bd28c97a20aff3c820230323063703
Authorization plaintext: 2c94887686c00d75018707d8a6070f9e:20230323063703
Request url:  https://app.cloopen.com:8883/2013-12-26/Accounts/2c94887686c00d75018707d8a6070f9e/SMS/TemplateSMS?sig=8D4A3CCCE59D4C3D0D162EF9D8012A8E
Request headers:  {'Content-Type': 'application/json;charset=utf-8', 'Accept': 'application/json', 'Accept-Charset': 'UTF-8', 'Authorization': b'MmM5NDg4NzY4NmMwMGQ3NTAxODcwN2Q4YTYwNzBmOWU6MjAyMzAzMjMwNjM3MDM='}
Request body:  {"to": "15715171491", "appId": "2c94887686c00d75018707d8a7290fa5", "templateId": "1", "datas": ["123456", 5]}
Response body:  {"statusCode":"112310","statusMsg":"【短信】应用未上线，模板短信接收号码外呼受限"}
{'statusCode': '112310', 'statusMsg': '【短信】应用未上线，模板短信接收号码外呼受限'} <class 'dict'>

Process finished with exit code 0

    
    """