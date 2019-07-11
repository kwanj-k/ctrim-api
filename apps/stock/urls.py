from django.urls import path
from . import views

urlpatterns = [
    path('stocks/<str:storename>/', views.StockList.as_view(), name='stocks'),
]
