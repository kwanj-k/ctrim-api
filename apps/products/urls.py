from django.urls import path
from . import views

urlpatterns = [
    path('products/<str:storename>/', views.ProductList.as_view(), name='list'),
    path(
        'products/<slug:slug>', views.ProductDetail.as_view(), name='details'),
]
