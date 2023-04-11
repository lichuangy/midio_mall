from django.conf.urls import url
from apps.verifications.views import ImageCodeView, SmsCodeView

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # 图形验证码
    url(r'^image_codes/(?P<uuid>[\w-]+)/$', ImageCodeView.as_view()),
    # 短信验证码
    url(r'^sms_codes/(?P<mobile>[\w-]+)/$', SmsCodeView.as_view()),
    # url(r'^sms_codes/(?P<mobile>[\w-]+)//$', SmsCodeView.as_view()),

]
