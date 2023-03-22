from django.conf.urls import url
from apps.verifications.views import ImageCodeView

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # 图形验证码
    url(r'^image_codes/(?P<uuid>[\w-]+)/$', ImageCodeView.as_view()),

]
