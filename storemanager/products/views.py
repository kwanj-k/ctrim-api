from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated
)
from common.permissions import IsOwnerOrReadOnly
from rest_framework.authentication import TokenAuthentication
import urllib.request
from rest_framework.renderers import BrowsableAPIRenderer,JSONRenderer
from .models import Product
from .serializers import ProductSerializer
import json
from django.db.models import Q

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
