from django.conf.urls import url

from apps.user.views import UsernameCountView, RegistereView,LoginView,LoginOutView,CenterView,EmailView
from apps.user.views import EmailVerifyView,AddressCreateView

urlpatterns = [
    # url(r'^admin/', admin.site.urls),

    url(r'^usernames/(?P<username>\w{0,20})/count/$', UsernameCountView.as_view()),
    url(r'^register/$', RegistereView.as_view()),
    url(r'^login/', LoginView.as_view()),
    url(r'^logout/', LoginOutView.as_view()),
    url(r'^info/', CenterView.as_view()),
    url(r'^emails/', EmailView.as_view()),
    url(r'^emails/verification/', EmailVerifyView.as_view()),
    url(r'^addresses/create/', AddressCreateView.as_view()),

]
