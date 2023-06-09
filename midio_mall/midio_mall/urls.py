"""midio_mall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include


# def log(request):
#     import logging
#
#     logger = logging.getLogger('djanbo')
#     logger.info('user has benn login...')
#     logger.warning('redis memmory not satistation!')
#     logger.error('the log not exist!')
#     logger.debug('~~~~~~~~~')
#     return HttpResponse('log')

from utils.converter import UserNameConvert
from django.urls import register_converter

register_converter(UserNameConvert, 'username')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^log/', log),
    # 导入user子应用的路由
    url(r'', include('apps.user.urls')),
    url(r'', include("apps.verifications.urls")),
    url(r'', include("apps.areas.urls")),
    url(r'', include("apps.goods.urls")),
    url(r'', include("apps.carts.urls")),
]
