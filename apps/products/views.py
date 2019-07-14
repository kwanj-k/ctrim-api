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


# class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes =(IsAuthenticated,IsOwnerOrReadOnly)
#     serializer_class = ProductSerializer
#     lookup_field = 'slug'

#     def get_queryset(self):
#         slug = self.kwargs.get('slug')
#         if slug:
#             queryset = Product.objects.filter(
# 					Q(slug__icontains=slug) |
# 					Q(slug__iexact=slug)
# 				)
#         else:
#             queryset = Product.objects.all()
#         if self.request.method == 'PUT':
#             queryset = Product.everything.all()
#             return queryset
#         return queryset
