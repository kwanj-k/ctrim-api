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
from apps.stock.models import Stock, StockProduct, Product, Package
from apps.stock.serializers import StockProductSerializer
from apps.helpers.return_response_data import okay_response


class StockProductViewSet(ViewSet):
    """StockProduct viewset."""

    serializer_class = StockProductSerializer
    queryset = StockProduct.objects.all()
    renderer_class = JSONRenderer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['stock__id']
    search_fields = ['product__name',]

    def create(self, request, *args, **kwargs):
        """
           Creates a StockProduct.
           If successful, response payload with:
               - status code: 201
               - data
           If unsuccessful, a response payload with:
               - status code: 400
        """

        serializer = StockProductSerializer(data=request.data)
        if serializer.is_valid():
            data = save_serializer(serializer)
            return Response(data, status=status.HTTP_201_CREATED)
        data = {
            'status': 'error'
        }

        data.update({'data': serializer.errors})
        status_code = status.HTTP_400_BAD_REQUEST
        return Response(data, status=status_code)


    def retrieve(self, request, pk=None):
        """
        Get a StockProduct.
        If successful, response payload with:
            - status code: 200
            - data
  
        If unsuccessful, a response payload with:
            - status code: 404
        """

        return Response(*check_resource(Stock, StockProductSerializer, pk, request, "StockProduct"))

    def destroy(self, request, pk=None):
        """
        Delete a StockProduct.
        If unsuccessful, a response payload with:
            - status code: 404
        If successful, a response payload with:
            - status code: 200
            - messsage: stock deleted successful
        """
        stockp = resource_exists(StockProduct, pk)
        if not stockp:
            response_attr = {'format_str': 'StockProduct', 'error_key': 'not_found'}
            data = get_response(**response_attr)
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        stockp.delete()
        data = {
            'status': 'success',
            'message': 'StockProduct deleted successfully'
            }
        return Response(data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        """
        Update a StockProduct.
        If successful, response payload with:
            - status code: 200
            - data
        If unsuccessful, a response payload with:
            - status
            - error
        """
        stockp = resource_exists(StockProduct, pk)
        if not stockp:
            response_attr = {'error_key': 'not_found', 'format_str': 'StockProduct'}
            data = get_response(**response_attr)
            return Response(data, status.HTTP_404_NOT_FOUND)
        serializer = StockProductSerializer(stock, context={'request': request}, data=request.data, partial=True)
        if serializer.is_valid():
            data = save_serializer(serializer)
            return Response(data, status.HTTP_200_OK)
        data = {
            'status': 'error',
            'error': serializer.errors,
            'message': 'StockProduct failed to edit due to the above error/s'
        }
        return Response(data, status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """
        Get all StockProducts.
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

        stockp = StockProduct.objects.all()
        serializer = StockProductSerializer(stockp, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
