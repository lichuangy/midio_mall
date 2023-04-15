# 生产者 任务，函数
# 下面的函数需要用celery的实例的 task装饰器来装饰
# 需要celery自动检测制定包

from libs.yuntongxun.smsSDK import SendSmsVerificationCode
from django.core.mail import send_mail
from celery_tasks.celery import app
@app.task
def send_email(subject,message,html_message,from_email,recipient_list):
    send_mail(subject=subject,
              message=message,
              html_message=html_message,
              from_email=from_email,
              recipient_list=recipient_list)