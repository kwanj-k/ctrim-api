from django.conf.urls import url
from django.urls import include, path

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

stock = StockViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy',
    'patch': 'partial_update'
})

stocks_list = StockViewSet.as_view({
    'get': 'list',
})
stock_create = StockViewSet.as_view({
    'post': 'create'
})


urlpatterns = format_suffix_patterns([
    url(r'^products/(?P<pk>[0-9]+)/$', products, name="product"),
    url(r'^products/$', products_list, name='products_list'),
    url(r'^packages/(?P<pk>[0-9]+)/$', packages, name="package"),
    url(r'^packages/$', packages_list, name='packages_list'),
    path('stocks/', stocks_list, name="stocks_list"),
    url(r'^stock/(?P<store_id>[0-9]+)/$', stock_create, name="stock_create"),
    path('stock_detail/<int:pk>/', stock, name="stock_detail"),
])
