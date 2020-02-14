from django.urls import path
from . import views


app_name = 'stocks'
urlpatterns = [
    path('stocks/<int:store_id>/', views.StockListCreateView.as_view(), name='stocks_list'),
]
