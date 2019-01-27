from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('products/', views.ProductList.as_view(),name='list'),
    path('products/<slug:slug>/',views.ProductDetail.as_view(),name='details'),
    path('tags/', views.TagsAPIView.as_view(), name='tag-list'),
    path('tags/<slug:slug>/', views.TagsDetailAPIView.as_view(), name='tag-details'),
    path('search/', views.SearchFilterListAPIView.as_view(), name='search-field')
]
