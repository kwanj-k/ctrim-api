from django.urls import path
from . import views

urlpatterns = [
    path('stocks/<int:store_id>/', views.StockListCreateView.as_view(), name='stocks'),
]
