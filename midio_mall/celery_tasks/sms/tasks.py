# 生产者 任务，函数
# 下面的函数需要用celery的实例的 task装饰器来装饰
# 需要celery自动检测制定包

from libs.yuntongxun.smsSDK import SendSmsVerificationCode
from celery_tasks.celery import app
@app.task
def celery_send_sms_code(mobile,code):
    SendSmsVerificationCode().send_message(mobile,[code,5],1)