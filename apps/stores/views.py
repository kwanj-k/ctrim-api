"""Stores endpoints."""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import (
    BrowsableAPIRenderer, HTMLFormRenderer,
    JSONRenderer
)

from apps.helpers.get_response import get_response
from apps.helpers.save_serializer import save_serializer
from apps.helpers.check_resource import check_resource, resource_exists
from apps.users.models import User

from .models import Store
from .serializers import StoreSerializer


class StoreViewSet(ViewSet):
    """Store viewset."""

    serializer_class = StoreSerializer
    queryset = Store.objects.all()
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, HTMLFormRenderer)

    def create(self, request):
        """
           Creates an Store.
           If successful, response payload with:
               - status code: 201
               - data
           If unsuccessful, a response payload with:
               - status code: 400
           """
        serializer = StoreSerializer(data=request.data)
        if serializer.is_valid():
            data = save_serializer(serializer, owner=request.user)
            return Response(data, status=status.HTTP_201_CREATED)
        data = {
            'status': 'error'
        }

        data.update({'data': serializer.errors})
        status_code = status.HTTP_400_BAD_REQUEST
        return Response(data, status=status_code)

    def retrieve(self, request, pk=None):
        """
        Get an Store.
        If successful, response payload with:
            - status code: 200
            - data
        If unsuccessful, a response payload with:
            - status code: 404
        """
        return Response(*check_resource(Store, StoreSerializer, pk, request, "Store"))

    def destroy(self, request, pk=None):
        """
        Delete an Store.
        If unsuccessful, a response payload with:
            - status code: 404
        If successful, a response payload with:
            - status code: 200
            - messsage: store deleted successful
        """
        store = resource_exists(Store, pk)
        if not store:
            response_attr = {'format_str': 'Store', 'error_key': 'not_found'}
            data = get_response(**response_attr)
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        store.delete()
        data = {
            'status': 'success',
            'message': 'store deleted successfully'
            }
        return Response(data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        """
        Update an Store.
        If successful, response payload with:
            - status code: 200
            - data
        """
        store = resource_exists(Store, pk)
        if not store:
            response_attr = {'error_key': 'not_found', 'format_str': 'Activity'}
            data = get_response(**response_attr)
            return Response(data, status.HTTP_404_NOT_FOUND)
        serializer = StoreSerializer(store, context={'request': request}, data=request.data, partial=True)

        if serializer.is_valid():
            data = save_serializer(serializer)
            return Response(data, status.HTTP_200_OK)
        data = {
            'status': 'error',
            'error': serializer.errors,
            'message': 'Store failed to edit due to the above error/s'
        }
        return Response(data, status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """
        Get all stores.
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

        stores = Store.objects.all()
        serializer = StoreSerializer(stores, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
