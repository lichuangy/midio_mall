from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
"""
注意自定义的认证model类，这个model类必须继承django.contrib.auth.models.AbstractUser类。该类提供了的字段：
 username
password
email
first_name
last_name
"""
class User(AbstractUser):
    mobile = models.CharField(max_length=11,unique=True)
    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户管理'