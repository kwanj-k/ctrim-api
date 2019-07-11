from django.urls import path

from .views import (
    StoreListCreateView,
    # StaffListCreateView,
    UpdateDestroyStoreView
)

app_name = 'store'
urlpatterns = [
    path('stores/', StoreListCreateView.as_view(), name='stores_list'),
    path('stores/<str:storename>/', UpdateDestroyStoreView.as_view(), name='stores-detail'),
    #path('<slug>/staff/', StaffListCreateView.as_view()),
]
