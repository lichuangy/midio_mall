from django.conf.urls import url

from apps.user.views import UsernameCountView

urlpatterns = [
    # url(r'^admin/', admin.site.urls),

    url(r'^usernames/(?P<username>\w{5,20})/count/$', UsernameCountView.as_view()),

]
