from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from .models import Product
from .serializers import ProductSerializer
from apps.stores.models import Store


class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)


    def get_queryset(self, *args, **kwargs):
        try:
            store = Store.objects.get(id=kwargs['store_id'])
        except Store.DoesNotExist:
            message = 'Store does not exist'
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        queryset = Product.objects.filter(store=store)
        return queryset

    def create(self, request, *args, **kwargs):
        try:
            store = Store.objects.get(name=kwargs['storename'])
        except Store.DoesNotExist:
            message = 'Store does not exist'
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        products = self.get_queryset()
        new_product_name = ''.join(self.request.data['name'].split()).lower()
        data = request.data
        serializer_context = {
            'request': request,
            'store': store
        }
        serializer = self.serializer_class(
            data=data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save(store=store)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
