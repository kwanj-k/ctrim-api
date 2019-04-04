from django.urls import path

from .views import StoreListCreateView

app_name = 'store'

urlpatterns = [
    path('stores/', StoreListCreateView.as_view())
]
