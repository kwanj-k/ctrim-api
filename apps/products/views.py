from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from .models import Product
from .serializers import ProductSerializer
from django.db.models import Q
from apps.helpers.store import store_products
from apps.stores.models import Store
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

class ProductList(generics.ListCreateAPIView):
    permission_classes =(IsAuthenticated,)
    serializer_class = ProductSerializer

    def get_queryset(self):
        store = get_object_or_404(Store, name=self.kwargs['storename'])
        queryset = Product.objects.filter(
                store=store
                )
        return queryset

    def create(self, request, *args, **kwargs):
        try:
            store = Store.objects.get(name=kwargs['storename'])
        except Store.DoesNotExist:
            message = 'Store does not exist'
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        products = store_products(kwargs['storename'])
        new_product_name = ''.join(self.request.data['name'].split()).lower()
        for product in products:
            if product.store == store:
                name = ''.join(product.name.split()).lower()
                if name == new_product_name:
                    message = 'Product already exists.'
                    return Response(message, status=status.HTTP_400_BAD_REQUEST)
        product_worth = 0
        req_data = self.request.data
        product_worth += req_data['number_of_packages'] * req_data['package_price']
        product_worth += req_data['number_of_pieces'] * req_data['piece_price']
        req_data['product_worth'] = product_worth
        serializer_context = {
            'request': request,
            'store': store
        }
        data = req_data
        serializer = self.serializer_class(
            data=data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save(store=store)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


def get_product(**kwargs):
        storename = kwargs.get('storename', None)
        try:
            store = Store.objects.get(name=storename)
        except Store.DoesNotExist:
            message = 'Store does not exist'
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        queryset = Product.objects.filter(
            store=store,
            name=kwargs['productname']
        ).first()
        return queryset

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes =(IsAuthenticated,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def retrieve(self, request, *args, **kwargs):
        queryset = get_product(**kwargs)
        if not queryset:
            message = 'Product does not exist'
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = get_product(**kwargs)
        if not instance:
            message = 'Product does not exist'
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    
