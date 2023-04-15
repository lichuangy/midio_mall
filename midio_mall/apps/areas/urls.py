from django.conf.urls import url
from apps.areas.views import AreasView, CityView
urlpatterns = [
    url(r'^areas/$', AreasView.as_view()),
    # (?P<username>\w{0,20})
    url(r'^areas/(?P<id>\d+)/', CityView.as_view()),


]