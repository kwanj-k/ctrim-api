from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated
)
from rest_framework.authentication import TokenAuthentication
import urllib.request
from rest_framework.renderers import BrowsableAPIRenderer,JSONRenderer
from .models import Product
from .serializers import ProductSerializer
import json

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
    permission_classes =(IsAuthenticated,)
    serializer_class = ProductSerializer
    def get_queryset(self):
        queryset = Product.everything.all()
        if self.request.method == 'PUT':
            queryset = Product.objects.all()
            return queryset
        return queryset
