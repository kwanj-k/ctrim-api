from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import StoreViewSet

app_name = 'stores'

stores = StoreViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy',
    'patch': 'partial_update'
})

stores_list = StoreViewSet.as_view({
    'get': 'list',
    'post': 'create'
})


urlpatterns = format_suffix_patterns([
    url(r'^stores/(?P<pk>[0-9]+)/$', stores, name="stores"),
    url(r'^stores/$', stores_list, name='stores_list'),
])
