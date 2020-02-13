from rest_framework import generics
from .serializers import StockSerializer
from .models import Stock
from apps.products.models import Product
from apps.helpers.store import store_products
from rest_framework.permissions import IsAuthenticated
from apps.stores.models import Store
from rest_framework.response import Response
from rest_framework import status

class StockListCreateView(generics.ListCreateAPIView):
    permission_classes =(IsAuthenticated,)
    serializer_class = StockSerializer

    def get_queryset(self):
        try:
            store = Store.objects.get(id=self.kwargs['store_id'])
        except Store.DoesNotExist:
            message = 'Store does not exist'
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        queryset = Stock.objects.filter(
            store=store
        )
        return queryset

    def create(self, request, *args, **kwargs):
        try:
            store = Store.objects.get(id=kwargs['store_id'])
        except Store.DoesNotExist:
            message = 'Store does not exist'
            return Response(message, status=status.HTTP_404_NOT_FOUND)       
        serializer_context = {
            'request': request,
            'store': store
        }
        data = request.data
        serializer = self.serializer_class(
            data=data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save(store=store)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
