"""Product endpoints."""

from rest_framework import status
from rest_framework.renderers import (JSONRenderer)
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated

from apps.helpers.get_response import get_response
from apps.helpers.save_serializer import save_serializer
from apps.helpers.check_resource import check_resource, resource_exists
from apps.stock.models import Product
from apps.stock.serializers import ProductSerializer
from apps.helpers.return_response_data import okay_response


class ProductViewSet(ViewSet):
    """Product viewset."""

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    renderer_class = JSONRenderer
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        """
           Creates a Product.
           If successful, response payload with:
               - status code: 201
               - data
           If unsuccessful, a response payload with:
               - status code: 400
           """
        serializer = ProductSerializer(data=request.data)
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
        Get a Product.
        If successful, response payload with:
            - status code: 200
            - data
  
        If unsuccessful, a response payload with:
            - status code: 404
        """

        return Response(*check_resource(Product, ProductSerializer, pk, request, "Product"))

    def destroy(self, request, pk=None):
        """
        Delete a Product.
        If unsuccessful, a response payload with:
            - status code: 404
        If successful, a response payload with:
            - status code: 200
            - messsage: product deleted successful
        """
        product = resource_exists(Product, pk)
        if not product:
            response_attr = {'format_str': 'Product', 'error_key': 'not_found'}
            data = get_response(**response_attr)
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        data = {
            'status': 'success',
            'message': 'product deleted successfully'
            }
        return Response(data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        """
        Update a product.
        If successful, response payload with:
            - status code: 200
            - data
        If unsuccessful, a response payload with:
            - status
            - error
        """
        product = resource_exists(Product, pk)
        if not product:
            response_attr = {'error_key': 'not_found', 'format_str': 'Product'}
            data = get_response(**response_attr)
            return Response(data, status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, context={'request': request}, data=request.data, partial=True)

        if serializer.is_valid():
            data = save_serializer(serializer)
            return Response(data, status.HTTP_200_OK)
        data = {
            'status': 'error',
            'error': serializer.errors,
            'message': 'Product failed to edit due to the above error/s'
        }
        return Response(data, status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """
        Get all Products.
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

        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
