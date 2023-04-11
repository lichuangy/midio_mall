import os
from celery import Celery
os.environ.setdefault(os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mcelery_tasks.settings'))
app = Celery('celery_tasks')
# 设置broker，加载配置文集来设置broker
app.config_from_object("celery_tasks.config")
app.autodiscover_tasks(['celery_tasks.sms'])