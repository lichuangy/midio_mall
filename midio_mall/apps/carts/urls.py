from django.conf.urls import url
from apps.carts.views import CatsCreateView
urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^carts/', CatsCreateView.as_view()),

]