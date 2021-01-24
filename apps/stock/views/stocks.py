"""Stock endpoints."""
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status, filters
from rest_framework.renderers import (JSONRenderer)
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated

from apps.helpers.get_response import get_response
from apps.helpers.save_serializer import save_serializer
from apps.helpers.check_resource import check_resource, resource_exists
from apps.helpers.generate_code import generate_code
from apps.stock.models import Stock, Store
from apps.stock.serializers import StockSerializer
from apps.helpers.return_response_data import okay_response


class StockViewSet(ViewSet):
    """Stock viewset."""

    serializer_class = StockSerializer
    queryset = Stock.objects.all()
    renderer_class = JSONRenderer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['store__id']
    search_fields = ['ref_number', 'stock_type']

    def create(self, request, *args, **kwargs):
        """
           Creates a Stock.
           If successful, response payload with:
               - status code: 201
               - data
           If unsuccessful, a response payload with:
               - status code: 400
        """
        store_id = kwargs.get('store_id', None)
        store = resource_exists(Store, int(store_id))
        if not store:
            response_attr = {'format_str': 'Store', 'error_key': 'not_found'}
            data = get_response(**response_attr)
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        code = generate_code()
        ref_number='STK'+str(code*9)
        serializer_context = {
            'request': request,
            'store': store,
            'ref_number': ref_number
        }
        serializer = self.serializer_class(data=request.data, context=serializer_context)
        if serializer.is_valid():
            serializer.save(store=store, ref_number=ref_number)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        data = {
            'status': 'error'
        }
        data.update({'data': serializer.errors})
        status_code = status.HTTP_400_BAD_REQUEST
        return Response(data, status=status_code)

    def retrieve(self, request, pk=None):
        """
        Get a Stock.
        If successful, response payload with:
            - status code: 200
            - data
  
        If unsuccessful, a response payload with:
            - status code: 404
        """

        return Response(*check_resource(Stock, StockSerializer, pk, request, "Stock"))

    def destroy(self, request, pk=None):
        """
        Delete a Stock.
        If unsuccessful, a response payload with:
            - status code: 404
        If successful, a response payload with:
            - status code: 200
            - messsage: stock deleted successful
        """
        stock = resource_exists(Stock, pk)
        if not stock:
            response_attr = {'format_str': 'Stock', 'error_key': 'not_found'}
            data = get_response(**response_attr)
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        stock.delete()
        data = {
            'status': 'success',
            'message': 'stock deleted successfully'
            }
        return Response(data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        """
        Update a stock.
        If successful, response payload with:
            - status code: 200
            - data
        If unsuccessful, a response payload with:
            - status
            - error
        """
        stock = resource_exists(Stock, pk)
        if not stock:
            response_attr = {'error_key': 'not_found', 'format_str': 'Stock'}
            data = get_response(**response_attr)
            return Response(data, status.HTTP_404_NOT_FOUND)
        serializer = StockSerializer(stock, context={'request': request}, data=request.data, partial=True)

        if serializer.is_valid():
            data = save_serializer(serializer)
            return Response(data, status.HTTP_200_OK)
        data = {
            'status': 'error',
            'error': serializer.errors,
            'message': 'Stock failed to edit due to the above error/s'
        }
        return Response(data, status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """
        Get all Stocks.
        Returns
        -------
        If successful:
            A response payload with:
            - status code: 200
            - data
        If unsuccessful:
            A response payload with:
            - status code: 404
        """

        stocks = Stock.objects.all()
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
