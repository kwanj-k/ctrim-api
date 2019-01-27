from rest_framework import generics,status
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated
)
from common.permissions import IsOwnerOrReadOnly
from rest_framework.authentication import TokenAuthentication
import urllib.request
from rest_framework.renderers import BrowsableAPIRenderer,JSONRenderer
from .models import Product,Tag
from .serializers import ProductSerializer,TagSerializer
import json
from django.db.models import Q
from rest_framework.response import Response
from django.utils.text import slugify
# django-filter
# from django_filters.rest_framework import FilterSet, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter

class ProductList(generics.ListCreateAPIView):
    permission_classes =(IsAuthenticated,)
    serializer_class = ProductSerializer
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    def get_queryset(self):
        queryset = Product.everything.all()
        if self.request.method == 'GET':
            queryset = Product.objects.all()
            return queryset
        return queryset


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes =(IsAuthenticated,IsOwnerOrReadOnly)
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        if slug:
            queryset = Product.objects.filter(
					Q(slug__icontains=slug) |
					Q(slug__iexact=slug)
				)
        else:
            queryset = Product.objects.all()
        if self.request.method == 'PUT':
            queryset = Product.everything.all()
            return queryset
        return queryset


class TagsAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()
    renderer_names = ('tag', 'tags')
    serializer_class = TagSerializer

class TagsDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    renderer_names = ('tag', 'tags')
    serializer_class = TagSerializer
    lookup_field = 'slug'

class ProductFilter(filters.FilterSet):
    tag = filters.CharFilter(field_name='tags__tag', lookup_expr='exact')
    username = filters.CharFilter(field_name='owner__username', lookup_expr='exact')
    name = filters.CharFilter(field_name='name', lookup_expr='exact')

    class Meta:
        model = Product
        fields = ['tag', 'username', 'name']

class SearchFilterListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    queryset = Product.objects.all()
    renderer_names = ("product", "products",)

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = ProductFilter
    search_fields = ('tags__tag', 'owner__username', 'name', 'category')
    ordering_fields = ('owner__username', 'name')
