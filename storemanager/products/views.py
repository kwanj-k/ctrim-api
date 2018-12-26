from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated
)
import urllib.request
from rest_framework.renderers import BrowsableAPIRenderer,JSONRenderer
from .models import Product
from .serializers import ProductSerializer,ProductGetSerializer
import json

class ProductList(generics.ListCreateAPIView):
    permission_classes =(IsAuthenticated,)
    renderer_classes = (BrowsableAPIRenderer,JSONRenderer,)
    #serializer_class = ProductSerializer
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductGetSerializer
        return ProductSerializer
    def get_queryset(self):
        queryset = Product.everything.all()
        if self.request.method == 'GET':
            queryset = Product.objects.all()
            return queryset
        return queryset


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes =(IsAuthenticated,)
    renderer_classes = (BrowsableAPIRenderer,JSONRenderer,)
    serializer_class = ProductSerializer
    def get_queryset(self):
        queryset = Product.everything.all()
        if self.request.method == 'PUT':
            queryset = Product.objects.all()
            return queryset
        return queryset
