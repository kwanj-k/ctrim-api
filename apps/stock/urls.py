from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from  apps.stock.views import *

app_name = 'stock'

products = ProductViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy',
    'patch': 'partial_update'
})

products_list = ProductViewSet.as_view({
    'get': 'list',
    'post': 'create'
})


urlpatterns = format_suffix_patterns([
    url(r'^products/(?P<pk>[0-9]+)/$', products, name="stores"),
    url(r'^products/$', products_list, name='stores_list'),
])
