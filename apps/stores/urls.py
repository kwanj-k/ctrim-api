from django.urls import path

from .views import (
    StoreListCreateView,
    StaffListCreateView,
    GetUpdateDestroyStoreView
)

app_name = 'store'

urlpatterns = [
    path('stores/', StoreListCreateView.as_view()),
    path('stores/<str:storename>/', GetUpdateDestroyStoreView.as_view()),
    path('<slug>/staff/', StaffListCreateView.as_view()),
]
