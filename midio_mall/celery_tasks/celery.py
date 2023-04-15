# 为celery的运行， 设置django的环境
import os
from celery import Celery
# os.environ.setdefault(os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mcelery_tasks.settings'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "midio_mall.settings")
# 创建celry实例
app = Celery('celery_tasks')
# 设置broker，加载配置文集来设置broker
app.config_from_object("celery_tasks.config")
# 需要celery自动检测指定包的任务
# 列表中的元素是 tasks的路径
app.autodiscover_tasks(['celery_tasks.sms','celery_tasks.email'])