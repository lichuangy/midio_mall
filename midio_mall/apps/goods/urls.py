from django.conf.urls import url
from apps.goods.views import IndexView, ListView, SearchView,DetailView

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^index', IndexView.as_view()),
    url(r'^list/(?P<category_id>\d+)/skus/', ListView.as_view()),
    url(r'^search/', SearchView()),
    url(r'^detail/(?P<sku_id>\d+)/', DetailView.as_view()),

]