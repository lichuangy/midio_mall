from django.conf.urls import url

from apps.user.views import UsernameCountView, RegistereView,LoginView

urlpatterns = [
    # url(r'^admin/', admin.site.urls),

    url(r'^usernames/(?P<username>\w{0,20})/count/$', UsernameCountView.as_view()),
    url(r'^register/$', RegistereView.as_view()),
    url(r'^login/', LoginView.as_view()),

]
