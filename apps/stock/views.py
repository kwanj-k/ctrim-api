from rest_framework import generics
from .serializers import StockSerializer
from .models import Stock
from apps.products.models import Product
from apps.helpers.store import store_products
from rest_framework.permissions import IsAuthenticated
from apps.stores.models import Store
from rest_framework.response import Response
from rest_framework import status

class StockList(generics.ListCreateAPIView):
    permission_classes =(IsAuthenticated,)
    serializer_class = StockSerializer

    def get_queryset(self):
        try:
            store = Store.objects.get(name=self.kwargs['storename'])
        except Store.DoesNotExist:
            message = 'Store does not exist'
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        queryset = Stock.objects.filter(
            store=store
        )
        return queryset

    def create(self, request, *args, **kwargs):
        try:
            store = Store.objects.get(name=kwargs['storename'])
        except Store.DoesNotExist:
            message = 'Store does not exist'
            return Response(message, status=status.HTTP_404_NOT_FOUND)       
        serializer_context = {
            'request': request,
            'store': store
        }
        data = request.data
        net = 0
        for pk in request.data['products']:
            product = Product.objects.get(pk=pk)
            net += product.number_of_packages * product.package_price
            net += product.number_of_pieces * product.piece_price
        serializer = self.serializer_class(
            data=data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save(store=store, net_worth=net)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
