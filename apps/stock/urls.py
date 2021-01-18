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

packages = PackageViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy',
    'patch': 'partial_update'
})

packages_list = PackageViewSet.as_view({
    'get': 'list',
    'post': 'create'
})


urlpatterns = format_suffix_patterns([
    url(r'^products/(?P<pk>[0-9]+)/$', products, name="products"),
    url(r'^products/$', products_list, name='products_list'),
    url(r'^packages/(?P<pk>[0-9]+)/$', packages, name="packages"),
    url(r'^packages/$', packages_list, name='packages_list'),
])
