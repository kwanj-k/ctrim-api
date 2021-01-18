



# from rest_framework import generics
# from .serializers import StockSerializer
# from .models import Stock
# from apps.products.models import Product
# from apps.helpers.store import store_products
# from rest_framework.permissions import IsAuthenticated
# from apps.stores.models import Store
# from rest_framework.response import Response
# from rest_framework import status

# class StockListCreateView(generics.ListCreateAPIView):
#     permission_classes =(IsAuthenticated,)
#     serializer_class = StockSerializer
#     queryset = Store.objects.all()
    
#     def list(self, request, *args, **kwargs):
#         try:
#             store = Store.objects.get(id=self.kwargs['store_id'])
#         except Store.DoesNotExist:
#             message = 'Store does not exist'
#             return Response(message, status=status.HTTP_404_NOT_FOUND)
#         stocks = store.stocks.all()
#         for stock in stocks:
#             value = 0
#             products = stock.products.all()
#             for product in products:
#                 value += product.number_of_packages * product.package_price
#                 value += product.free_pieces * product.piece_price
#             stock.value = value
#         serializer = self.get_serializer(stocks, many=True)
#         return Response(serializer.data)


#     def create(self, request, *args, **kwargs):
#         try:
#             store = Store.objects.get(id=kwargs['store_id'])
#         except Store.DoesNotExist:
#             message = 'Store does not exist'
#             return Response(message, status=status.HTTP_404_NOT_FOUND)     
#         serializer_context = {
#             'request': request,
#             'store': store
#         }
#         data = request.data
#         serializer = self.serializer_class(
#             data=data, context=serializer_context)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(store=store)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
