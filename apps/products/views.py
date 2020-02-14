from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from .models import Product
from .serializers import ProductSerializer
from apps.stock.models import Stock


class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)


    def get_queryset(self, *args, **kwargs):
        try:
            stock = Stock.objects.get(id=self.kwargs['stock_id'])
        except Stock.DoesNotExist:
            message = 'Stock does not exist'
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        queryset = stock.products.all()
        return queryset

    def create(self, request, *args, **kwargs):
        try:
            stock = Stock.objects.get(id=kwargs['stock_id'])
        except Stock.DoesNotExist:
            message = 'Stock does not exist'
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        data = request.data
        data['name'] = ''.join(data['name'].split()).lower()
        try:
            product = Product.objects.get(
                name=data['name'],
                stock=stock
            )
        except Product.DoesNotExist:
            product = None
            pass
        if product:
            message = 'Product already exists'
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        serializer_context = {
            'request': request,
            'stock': stock
        }
        serializer = self.serializer_class(
            data=data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save(stock=stock)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
