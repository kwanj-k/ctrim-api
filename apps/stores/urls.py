from django.urls import path

from .views import (
    StoreListCreateView,
    # StaffListCreateView,
    # UpdateDestroyStoreView,
    StoreAnalysis,
)

app_name = 'store'
urlpatterns = [
    path('stores/', StoreListCreateView.as_view(), name='stores_list'),
    # path('stores/<str:storename>/', UpdateDestroyStoreView.as_view(), name='stores-detail'),
    path('stores/<str:storename>/analysis', StoreAnalysis.as_view(), name='store-analysis'),
    #path('<slug>/staff/', StaffListCreateView.as_view()),
]
