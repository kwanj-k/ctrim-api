"""Package endpoints."""

from rest_framework import status
from rest_framework.renderers import (JSONRenderer)
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated


from apps.helpers.get_response import get_response
from apps.helpers.save_serializer import save_serializer
from apps.helpers.check_resource import check_resource, resource_exists
from apps.stock.models import Package
from apps.stock.serializers import PackageSerializer
from apps.helpers.return_response_data import okay_response


class PackageViewSet(ViewSet):
    """Package viewset."""

    serializer_class = PackageSerializer
    queryset = Package.objects.all()
    renderer_class = JSONRenderer
    permission_classes = (IsAuthenticated,)


    def create(self, request):
        """
           Creates a Package.
           If successful, response payload with:
               - status code: 201
               - data
           If unsuccessful, a response payload with:
               - status code: 400
           """
        serializer = PackageSerializer(data=request.data)
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
        Get an Package.
        If successful, response payload with:
            - status code: 200
            - data
  
        If unsuccessful, a response payload with:
            - status code: 404
        """

        return Response(*check_resource(Package, PackageSerializer, pk, request, "Package"))

    def destroy(self, request, pk=None):
        """
        Delete an Package.
        If unsuccessful, a response payload with:
            - status code: 404
        If successful, a response payload with:
            - status code: 200
            - messsage: package deleted successful
        """
        package = resource_exists(Package, pk)
        if not package:
            response_attr = {'format_str': 'Package', 'error_key': 'not_found'}
            data = get_response(**response_attr)
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        package.delete()
        data = {
            'status': 'success',
            'message': 'package deleted successfully'
            }
        return Response(data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        """
        Update a Package.
        If successful, response payload with:
            - status code: 200
            - data
        If unsuccessful, a response payload with:
            - status
            - error
        """
        package = resource_exists(Package, pk)
        if not package:
            response_attr = {'error_key': 'not_found', 'format_str': 'Package'}
            data = get_response(**response_attr)
            return Response(data, status.HTTP_404_NOT_FOUND)
        serializer = PackageSerializer(package, context={'request': request}, data=request.data, partial=True)

        if serializer.is_valid():
            data = save_serializer(serializer)
            return Response(data, status.HTTP_200_OK)
        data = {
            'status': 'error',
            'error': serializer.errors,
            'message': 'Package failed to edit due to the above error/s'
        }
        return Response(data, status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """
        Get all Packages.
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

        packages = Package.objects.all()
        serializer = PackageSerializer(packages,many=True)
        return Response(serializer.data, status.HTTP_200_OK)
