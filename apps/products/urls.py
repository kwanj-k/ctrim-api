from django.urls import path
from . import views

app_name = 'product'
urlpatterns = [
    path('products/<str:storename>/', views.ProductList.as_view(), name='products_list'),
    path(
        'products/<str:storename>/<str:productname>', views.ProductDetail.as_view(), name='product_detail'),
]
