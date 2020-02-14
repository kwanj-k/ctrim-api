from django.urls import path

from . import views

app_name = 'products'
urlpatterns = [
    path('products/<int:stock_id>/', views.ProductListCreateView.as_view(), name='products_list'),
]
